# -*- coding: utf-8 -*-
from selenium import webdriver
from typing import Union, Any
from selenium import webdriver
from collections import namedtuple
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.user_session import UserSession

BrowserDriver = Union[webdriver.Chrome, webdriver.Firefox, webdriver.Edge]
Browser = namedtuple(
    typename="Browser", field_names=["driverType", "driverManager", "optionType"]
)


class DriverHandler(UserSession):
    SUPPORTED_BROWSERS = {
        "CHROME": Browser(
            driverType=webdriver.Chrome,
            driverManager=ChromeDriverManager,
            optionType=webdriver.ChromeOptions,
        ),
        "FIREFOX": Browser(
            driverType=webdriver.Firefox,
            driverManager=GeckoDriverManager,
            optionType=webdriver.FirefoxOptions,
        ),
        "EDGE": Browser(
            driverType=webdriver.Edge,
            driverManager=EdgeChromiumDriverManager,
            optionType=webdriver.EdgeOptions,
        ),
    }
    SUPPORTED_CONFIGS = {"HEADLESS", "WINDOW_SIZE", "MAXIMIZE_WINDOW"}

    def __init__(self, config: dict) -> None:
        super().__init__(config["DOMAINS"])
        if set(config["DEFAULT_CONFIG"].keys()) != self.SUPPORTED_CONFIGS:
            raise Exception(
                f"Default values for some supported configuration options are not specified"
            )
        self.defaultConfig = config["DEFAULT_CONFIG"]
        self.configs = config["BROWSERS"]
        self.drivers = {}
        for browserName in self.configs:
            self.drivers[browserName] = self.genDriver(browserName)
        self.defaultDriver = self.drivers[config["DEFAULT_BROWSER"]]

    def __del__(self) -> None:
        self.quitDrivers()

    def __getConfig(self, browserName: str, option: str):
        if option not in self.SUPPORTED_CONFIGS:
            raise Exception(f"Configuration option is not supported: {option}")
        return self.configs[browserName].get(option, self.defaultConfig[option])

    def genDriver(self, browserName: str) -> BrowserDriver:
        browser = self.SUPPORTED_BROWSERS.get(browserName)
        if browser is None:
            raise Exception(f"Browser is not supported: {browserName}")
        options = browser.optionType()
        options.headless = self.__getConfig(browserName, "HEADLESS")
        driver = browser.driverType(browser.driverManager().install(), options=options)
        driver.set_window_size(*self.__getConfig(browserName, "WINDOW_SIZE"))
        if self.__getConfig(browserName, "MAXIMIZE_WINDOW"):
            driver.maximize_window()
        return driver

    def logInDriver(
        self, browser: Union[str, BrowserDriver] = None, force: bool = False
    ) -> None:
        cookies, _ = self.logIn(force)
        if browser is not None:
            if isinstance(browser, str):
                driver = self.getDriver(browser)
                if driver is None:
                    raise Exception(f"Driver of type {browser} does not exist.")
            else:
                driver = browser
            driver.get(self.buildUrl("BKEL"))
            driver.delete_cookie("MoodleSession")
            driver.delete_cookie("MOODLEID1_")
            driver.add_cookie(
                {
                    "name": "MOODLEID1_",
                    "value": cookies["MOODLEID1_"],
                }
            )
            driver.add_cookie(
                {"name": "MoodleSession", "value": cookies["MoodleSession"]}
            )
        else:
            # transfer cookies to all drivers
            for driver in list(self.drivers.values()):
                driver.get(self.buildUrl("BKEL"))
                driver.delete_cookie("MoodleSession")
                driver.delete_cookie("MOODLEID1_")
                driver.add_cookie(
                    {
                        "name": "MOODLEID1_",
                        "value": cookies["MOODLEID1_"],
                    }
                )
                driver.add_cookie(
                    {"name": "MoodleSession", "value": cookies["MoodleSession"]}
                )

    def logOutDriver(self, browserName: str = None) -> None:
        self.logOut()

        if browserName is not None:
            driver = self.getDriver(browserName)
            if driver is None:
                raise Exception(f"Driver of type {browserName} does not exist.")
            driver.get(self.buildUrl("BKEL"))
            driver.delete_cookie("MoodleSession")
            driver.delete_cookie("MOODLEID1_")
        else:
            for driver in list(self.drivers.values()):
                driver.get(self.buildUrl("BKEL"))
                driver.delete_cookie("MoodleSession")
                driver.delete_cookie("MOODLEID1_")

    def addDriver(self, driver: BrowserDriver, replace: bool = True) -> bool:
        """
        Add new driver into the list of drivers.
        Return True if succeeded.
        """
        browserName = type(driver).rsplit(".", 1)[1].upper()
        if browserName not in self.config["BROWSERS"]:
            raise Exception("Browser type is not included in configuration.")
        if replace:
            self.drivers[browserName] = driver
            return True
        else:
            if browserName not in self.drivers:
                self.drivers[browserName] = driver
                return True
        return False

    def removeDriver(self, browserName: str) -> bool:
        """
        Remove driver of browser of type browserName.
        Return True if succeeded.
        """
        if browserName in self.drivers:
            self.drivers.pop(browserName)
            return True
        return False

    def listDrivers(self) -> list:
        return list(self.drivers.values())

    def getDriver(self, browserName: str) -> BrowserDriver:
        if browserName in self.drivers:
            return None
        return self.drivers[browserName]

    def getDefaultDriver(self) -> BrowserDriver:
        return self.defaultDriver

    def quitDrivers(self) -> None:
        self.logOut()
        for driver in list(self.drivers.values()):
            driver.quit()

    @staticmethod
    def waitDriver(
        driver: BrowserDriver, condition: Any = None, timeout: int = 10
    ) -> Any:
        if condition is None:
            driver.implicitly_wait(timeout)
            return None
        else:
            wait = WebDriverWait(driver, timeout)
            return wait.until(condition)

    @staticmethod
    def waitDriverVisit(driver: BrowserDriver, url: str, timeout: int = 10) -> None:
        driver.get(url)
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.url_to_be(url))
