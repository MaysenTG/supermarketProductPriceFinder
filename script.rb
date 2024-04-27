require 'bundler/setup'
# Bundler.require(:default)

require 'yaml'
require 'erb'
require 'httparty'
require 'dotenv'
require 'action_mailer'


# ==========================Supermarket price finder============================


# Load environment variables from .env file
Dotenv.load

# =================================Variables====================================
GMAIL_USERNAME=ENV['GMAIL_USERNAME'] # Sets the from and to email address
GMAIL_PASSWORD=ENV['GMAIL_PASSWORD'] # Sets the password for the email

PRICE_GOAL = 6.00   #Sets the price goal for the product

# =============================================================================

# Load SMTP settings from YAML file
smtp_settings = YAML.load_file('smtp_settings.yml')
ActionMailer::Base.smtp_settings = smtp_settings.symbolize_keys
ActionMailer::Base.delivery_method = :smtp

class SMTPSettings
  def self.load
    smtp_settings = YAML.load_file('smtp_settings.yml')
    smtp_settings['user_name'] = GMAIL_USERNAME
    smtp_settings['password'] = GMAIL_PASSWORD
    ActionMailer::Base.smtp_settings = smtp_settings.symbolize_keys
    ActionMailer::Base.delivery_method = :smtp
  end
end

class PiePriceMailer < ActionMailer::Base
  include HTTParty
  default from: GMAIL_USERNAME

  def pie_price(pie_price)
    @pie_price = pie_price
    mail(to: GMAIL_USERNAME, subject: 'Countdown Mince and Cheese pie price') do |format|
      format.html { render plain: ERB.new(File.read('pie_price.erb')).result(binding) }
    end
  end
end

class PiePriceClient
  PRODUCT_STOCK_CODE = 148886
  include HTTParty

  base_uri 'https://www.countdown.co.nz/api/v1/products'

  def self.fetch
    get("/#{PRODUCT_STOCK_CODE}", headers: { 'X-Requested-With' => 'OnlineShopping.WebApp', 'User-Agent' => 'price-finder/0.0.1' })
  end

  def self.find_price
    response = fetch
    parsed_response = JSON.parse(response.body)
    parsed_response['price']['salePrice'] || parsed_response['price']['originalPrice']
  end
end

SMTPSettings.load
price = PiePriceClient.find_price
PiePriceMailer.pie_price(price).deliver_now
