# Supermarket Product Price Finder
This ruby script fetches the price of a product on Countdown (Woolsworth now I guess??) every Monday morning and emails me the current price. In this case, the product is a 6pk of mince and cheese pies.


## To use this application:
1. Clone the repo (`git clone https://github.com/MaysenTG/supermarketProductPriceFinder.git`)
2. Add your email address to the `.env` file along with a Gmail app password (create one [here](https://myaccount.google.com/apppasswords))
3. Run `bundle install` to install all required gems
4. Run the program using `ruby script.rb`

## Want to change the product?
Visit your favourite product on Countdown and copy the number from the `stockcode` param in the URL.
