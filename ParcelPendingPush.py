#!/usr/bin/python3

#
# Watch ParcelPending for packages and send push notifications with PushOver upon delivery.
# Currently used in cronjob, could add a while loop and use as a service.
#

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import pushover
 
site_login = "https://my.parcelpending.com/login"
parcels = "https://my.parcelpending.com/parcel-history?package_status=1001"
username = ""
password = ""
 
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(10)
 
def Notify(package):
    ps = pushover.PushoverClient("./push")
    try:
        ps.send_message(package, title="Parcel Pending")
    except:
        print(package)
 
def Login():
    driver.get(site_login)
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_tag_name("button").click()
 
def GetParcels():
    driver.get(parcels)
    package_panel = driver.find_element_by_xpath("//section[@class='panel'][2]")
    if package_panel.text == "There are no packages that match the specified criteria.":
        print("No packages")
    else:
        table = driver.find_element_by_xpath("/html/body/section/div/section/section/section[2]/div/div[1]/table/tbody")
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            col = row.find_elements(By.TAG_NAME, "td")
            parcel = col[2]
            Notify(parcel.text)
 
Login()
GetParcels()
driver.quit()
