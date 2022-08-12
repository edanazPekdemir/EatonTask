from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from page import LoginPage
from page import MainPage
from page import ChartPage
from page import CheckOut
import time

print("Test Started!")

s = Service("C:/chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=s)

loginPage = LoginPage(driver, "https://www.saucedemo.com/")
mainPage = MainPage(driver)
chartPage = ChartPage(driver)
checkOut = CheckOut(driver)

loginPage.enterWebPage()
time.sleep(1)
loginPage.login()
time.sleep(1)

mainPage.addToChart("backpack")
time.sleep(1)
mainPage.addToChart("bolt-t-shirt")
time.sleep(1)
mainPage.addToChart("onesie")
time.sleep(1)
mainPage.enterChart()
time.sleep(1)

chartPage.popLastItem()
time.sleep(1)
chartPage.enterCheckOut()
time.sleep(1)

checkOut.runNegativeTestCases()
time.sleep(1)
checkOut.runPositiveTestCase()
time.sleep(1)
checkOut.clickFinish()
time.sleep(1)
checkOut.backHome()
time.sleep(1)

driver.close()
print("Test Finished!")
