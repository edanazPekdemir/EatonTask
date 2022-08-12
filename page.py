from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import logging


class LoginPage:
    def __init__(self, driver, webPage):
        self.driver = driver
        self.webPage = webPage

    def enterWebPage(self):
        self.driver.get(self.webPage)
        self.driver.maximize_window()

    def getUserName(self):
        element = self.driver.find_element(By.XPATH, "//div[@id='login_credentials']")
        users = element.text.split("\n")
        return users[1]

    def getPassword(self):
        element = self.driver.find_element(By.XPATH, "//div[@class='login_password']")
        passwords = element.text.split("\n")
        return passwords[1]

    def login(self):
        self.driver.find_element(By.XPATH, "//input[@name='user-name']").send_keys(self.getUserName())
        self.driver.find_element(By.XPATH, "//input[@name='password']").send_keys(self.getPassword())
        self.driver.find_element(By.XPATH, "//input[@name='login-button' and @value='Login']").click()


class MainPage:
    def __init__(self, driver):
        self.driver = driver

    def addToChart(self, item):
        chartTextStart = "//button[@name='add-to-cart-sauce-labs-"
        chartTextEnd = "']"
        self.driver.find_element(By.XPATH, chartTextStart + item + chartTextEnd).click()

    def enterChart(self):
        self.driver.find_element(By.XPATH, "//a[@class='shopping_cart_link']").click()


class ChartPage:
    def __init__(self, driver):
        self.driver = driver

    def getLastItem(self):
        lst = self.driver.find_elements(By.XPATH, "//button[text()='Remove']")
        return lst[-1]

    def popLastItem(self):
        self.getLastItem().click()

    def enterCheckOut(self):
        self.driver.find_element(By.XPATH, "//button[@name='checkout']").click()


class CheckOut:
    def __init__(self, driver):
        self.driver = driver
        logging.basicConfig(filename = "app.txt",
                            filemode = "w",
                            format = "%(asctime)s %(levelname)s - TC name : %(funcName)15s - %(message)s ",
                            level=logging.INFO,
                            datefmt = "%d-%b-%y %H:%M:%S")

    def confirmCheckout(self, fname, lname, zip):
        self.driver.find_element(By.XPATH, "//input[@name='firstName']").send_keys(fname)
        self.driver.find_element(By.XPATH, "//input[@name='lastName']").send_keys(lname)
        self.driver.find_element(By.XPATH, "//input[@name='postalCode']").send_keys(zip)
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//input[@name='continue']").click()
        return self.getErrorMessage()

    def getErrorMessage(self):
        try:
            element = self.driver.find_element(By.XPATH, "//div[@class='error-message-container error']")
            err = element.text
            self.driver.refresh()
            return err
        except NoSuchElementException:
            return "No Error"

    def clickFinish(self):
        self.driver.find_element(By.XPATH, "//button[@name='finish']").click()

    def backHome(self):
        self.driver.find_element(By.XPATH, "//button[@name='back-to-products']").click()

    def runNegativeTestCases(self):
        self.TC_Empty()
        self.TC_NoPostalCode()
        self.TC_NoName()
        self.TC_NoLastName()
        self.TC_OnlyName()
        self.TC_OnlyLastName()
        self.TC_OnlyPostal()

    def runPositiveTestCase(self):
        self.TC_AllFields()

    def TC_AllFields(self):
        expectedError = "No Error"
        err = self.confirmCheckout("name", "last name", "123123")
        if expectedError == err:
            logging.info("Test Passed with err = " + err )
        else:
            logging.error("Test Failed err = " + err + " Expected = " + expectedError)

    def TC_Empty(self):
        expectedError = "Error: First Name is required"
        err = self.confirmCheckout("", "", "")
        if expectedError == err:
            logging.info("Test Passed with err = " + err )
        else:
            logging.error("Test Failed err = " + err + " Expected = " + expectedError)

    def TC_NoPostalCode(self):
        expectedError = "Error: Postal Code is required"
        err = self.confirmCheckout("test name", "test lastname", "")
        if expectedError == err:
            logging.info("Test Passed with err = " + err )
        else:
            logging.error("Test Failed err = " + err + " Expected = " + expectedError)

    def TC_NoLastName(self):
        expectedError = "Error: Last Name is required"
        err = self.confirmCheckout("test name", "", "123123")
        if expectedError == err:
            logging.info("Test Passed with err = " + err )
        else:
            logging.error("Test Failed err = " + err + " Expected = " + expectedError)

    def TC_NoName(self):
        expectedError = "Error: First Name is required"
        err = self.confirmCheckout("", "last name", "123123")
        if expectedError == err:
            logging.info("Test Passed with err = " + err )
        else:
            logging.error("Test Failed err = " + err + " Expected = " + expectedError)

    def TC_OnlyName(self):
        expectedError = "Error: Last Name is required"
        err = self.confirmCheckout("first name", "", "")
        if expectedError == err:
            logging.info("Test Passed with err = " + err )
        else:
            logging.error("Test Failed err = " + err + " Expected = " + expectedError)

    def TC_OnlyLastName(self):
        expectedError = "Error: First Name is required"
        err = self.confirmCheckout("", "last name", "")
        if expectedError == err:
            logging.info("Test Passed with err = " + err )
        else:
            logging.error("Test Failed err = " + err + " Expected = " + expectedError)

    def TC_OnlyPostal(self):
        expectedError = "Error: First Name is required"
        err = self.confirmCheckout("", "", "123123")
        if expectedError == err:
            logging.info("Test Passed with err = " + err )
        else:
            logging.error("Test Failed err = " + err + " Expected = " + expectedError)

