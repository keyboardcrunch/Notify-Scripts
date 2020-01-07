#!/usr/bin/python3

#
# Watch ParcelPending for packages and send push notifications with PushOver or Telegram upon delivery.
# Currently used in cronjob, could add a while loop and use as a service.
#

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

# global variables
notify_service = "telegram" # telegram, pushover
secrets_path = "/home/user/.mysecrets.ini"
site_login = "https://my.parcelpending.com/login"
package_history = "https://my.parcelpending.com/parcel-history?package_status=1001"

def PONotify(package):
    import pushover
    ps = pushover.PushoverClient(secrets_path)
    ps.send_message(package, title="Parcel Pending")

def TGNotify(tgapi, tguser, package):
    import telebot
    bot = telebot.AsyncTeleBot(tgapi)
    bot.send_message(tguser, package)
 
def GetParcels(ppuser, pppass):
    packages = []
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(10)
    driver.get(site_login)
    driver.find_element_by_name("username").send_keys(ppuser)
    driver.find_element_by_name("password").send_keys(pppass)
    driver.find_element_by_tag_name("button").click()
    driver.get(package_history)
    package_panel = driver.find_element_by_xpath("//section[@class='panel'][2]")
    if package_panel.text == "There are no packages that match the specified criteria.":
        print("No packages")
        driver.quit()
        quit()
    else:
        table = driver.find_element_by_xpath("/html/body/section/div/section/section/section[2]/div/div[1]/table/tbody")
        table_data = table.text
        for line in table_data.split('\n\n'):
            if line.startswith('Package Code:'):
                packages.append(line)
        driver.quit()
        return packages
    

if __name__ == "__main__":
    import configparser
    config = configparser.ConfigParser()
    config.read(secrets_path)
    username = config['parcelpending']['username']
    password = config['parcelpending']['password']

    p = GetParcels(username, password)
    for parcel in p:
        if notify_service == "pushover":
            PONotify(parcel)
        if notify_service == "telegram":
            tgapi = config['telegram']["notifybot"]
            tguser = config['telegram']["unaffiliatedcyber"]
            TGNotify(tgapi, tguser, parcel)
        else:
            print(parcel)
