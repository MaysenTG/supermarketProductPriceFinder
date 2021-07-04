
import applescript as applescript
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


# =========================== Change Variables below for personalization ==========================

# Declare variables
url = "https://shop.countdown.co.nz/shop/productdetails?stockcode=279224&name=irvines-chilled-pie-6pk-mince-cheese"
phoneNum = "0273102660"
sendMessage = False   # Set to False if you don't want the iMessage to be sent
productPriceGoal = 6.0   #Sets the price goal of the product for the applescript generator
selectedStore = "Countdown Cambridge".strip()




# Scripts required for seamless iMessage sending
changeMacSelectedAppScript = """if application "Safari" is running then
    tell application "Safari"
        activate
    end tell
    end if"""
quitMessagesScript = """tell application "Messages"
    quit
end tell"""



# Change browser to headless
options = Options()
#options.headless = True

# Disable images for faster testing
chrome_prefs = {}
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
options.experimental_options["prefs"] = chrome_prefs


# Initiate web driver
browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
browser.get(url)


# Sends a script to AppleScript to send an iMessage to the selected phone number.
def script_run(script, changeOpenApp, closeMessages):
    applescript.run(changeOpenApp)
    applescript.run(script)
    applescript.run(closeMessages)


# Function to return the script depending on the price of product
def setScript(priceOfPie):
    if(priceOfPie <= 6.00):
        script = """tell application "Messages"
            set myid to get id of first service
            set theBuddy to buddy \"""" + phoneNum + """\" of service id myid
            send """ + "\"Go buy a mince and cheese pie! They're only: $" + str(priceOfPie) + "\"" + """ to theBuddy
        end tell"""

    elif(priceOfPie > 6.00):
        script = """tell application "Messages"
            set myid to get id of first service
            set theBuddy to buddy "greenwood.maysen@gmail.com" of service id myid
            send """ + "\"Pies are too expensive at: $" + str(priceOfPie) + "\"" + """ to theBuddy
        end tell"""

    return script

# This function uses selenium to change the location of the store to your preferred store.
# You will need to check the website and make sure you enter the store name correctly at the top of this program
def checkLocation(browser):
    time.sleep(2)
    # If store name isn't cambridge, change it
    if(browser.find_element_by_tag_name("fulfilment-bar > span > span > strong").text.strip() != selectedStore):
        changeStore = browser.find_element_by_css_selector("fulfilment-bar > span > a")
        changeStore.click()

        # Change shopping method (pickup is easiest for setting region
        # browser.find_element_by_xpath("//input[@id='method-pickup']").click()
        browser.find_element_by_id("method-pickup").click()

        # Change store buttons in  "book a timeslot" page
        browser.find_element_by_tag_name("fulfilment-method-selection + fieldset > p > button").click()

        time.sleep(2)

        # Click select region button
        # Waikato is the 9th item in the list of regions
        selectRegion = Select(browser.find_element_by_tag_name("form-dropdown > div > select"))
        selectRegion.select_by_index(9)

        # Find store name
        # Selects the second element of the list (Corresponds to Countdown Cambridge, for example)
        # browser.find_element_by_css_selector("fulfilment-address-selector > ul > li:nth-child(2) > button").click()
        # This line finds the element based on its ID, which is below for Countdown Cambridge
        # browser.find_element_by_id("address-selection-button--1332617").click()
        # browser.find_element_by_xpath("//button//strong[text()='"+selectedStore+"']").click()
        browser.find_element_by_xpath("//button//strong[contains(.,'" + selectedStore + "')]").click()
        #strongElement.find_element_by_xpath("..").click()


        # Go back to pie page - Click back arrow 2 times
        browser.back()
        browser.back()
    else:
        print("Already in " + selectedStore + " store")


checkLocation(browser)
time.sleep(1)

# Set price to what's found on website
mainPriceDom = browser.find_element_by_tag_name("em")
centPriceDom = browser.find_element_by_css_selector("em + span")

priceOfPie = float(mainPriceDom.text+"."+centPriceDom.text.strip())
print("Found price of mince and cheese pies! They're $"+str(priceOfPie))
browser.quit()

# Run scripts to send iMessage to myself
def shouldRun(sendMessage):
    if(sendMessage):
        script = setScript(priceOfPie)
        script_run(script, changeMacSelectedAppScript, quitMessagesScript)
    else:
        print("Message sending was disabled")