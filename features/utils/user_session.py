# -*- coding: utf-8 -*-
import requests
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class UserSession:
    def __init__(self):
        self.session = None
        self.sessKey = None
        self.config = None
        self.drivers = []

    def setConfig(self, config: dict) -> None:
        if not (config["SSO_USERNAME"] and config["SSO_PASSWORD"]):
            raise Exception("Credentials needed for authentication are not set")
        if len(config["BROWSERS"]) == 0:
            config["BROWSERS"].append("CHROME")
        self.config = config
        for browserName in config["BROWSERS"]:
            self.drivers.append(self.__genDriver(browserName))

    def logIn(self, force=False) -> None:
        """
        Log in to BKeL via SSO service without interacting with the Web UI
        """
        if self.config is None:
            raise Exception("Configurations needed for authentication are not set")
        if self.session is not None:
            if force:
                self.logOut()
            else:
                return
        self.session = requests.Session()
        # get JSESSIONID
        self.session.get(url=self.config["SSO_DOMAIN"] + "/cas/login")
        # get CSRF token
        response = self.session.get(url=self.config["SSO_DOMAIN"] + "/cas/login")
        tmp = re.search(r'"(LT-\d+-[A-Za-z0-9]+)"', response.text)
        lt = tmp.group(1)
        tmp = re.search(r'name="execution" value="(.*?)"', response.text)
        execution = tmp.group(1)
        # authenticate
        response = self.session.post(
            url=self.config["SSO_DOMAIN"] + "/cas/login",
            data={
                "username": self.config["SSO_USERNAME"],
                "password": self.config["SSO_PASSWORD"],
                "lt": lt,
                "execution": execution,
                "_eventId": "submit",
                "submit": "Login",
            },
        )
        if not self.session.cookies.get("CASTGC"):
            raise Exception("Failed to log in via SSO service")
        # log in to BKeL
        response = self.session.get(
            url=self.config["BKEL_DOMAIN"] + "/login/index.php?authCAS=CAS",
            allow_redirects=True,
        )
        # extract sessKey
        tmp = re.search(r'"sesskey":"(.*?)"', response.text)
        self.sessKey = tmp.group(1)

        # transfer cookies to drivers
        cookies = self.session.cookies.get_dict()
        for driver in self.drivers:
            driver.get(self.config["BKEL_DOMAIN"])
            driver.add_cookie(
                {
                    "name": "MOODLEID1_",
                    "value": cookies["MOODLEID1_"],
                }
            )
            driver.add_cookie(
                {"name": "MoodleSession", "value": cookies["MoodleSession"]}
            )

    def logOut(self) -> None:
        """
        Log out of BKeL and SSO service
        """
        if self.session is None:
            return
        self.session.get(
            url=self.config["BKEL_DOMAIN"]
            + f"/login/logout.php?sesskey={self.sessKey}",
            allow_redirects=True,
        )
        self.session = self.sessKey = None
        # remove cookies from browsers
        for driver in self.drivers:
            driver.delete_cookie("MOODLEID1_")
            driver.delete_cookie("MoodleSession")

    def closeBrowsers(self) -> None:
        """
        Call close() on all drivers. Should be called at the very end.
        """
        for driver in self.drivers:
            driver.close()

    def getSessionInfo(self) -> tuple[dict, str]:
        """
        Return all information related to the current session (if user is logged in)
        """
        if self.session is None:
            return None
        return (self.session.cookies.get_dict(), self.sessKey)

    def getSessKey(self) -> str:
        return self.sessKey

    def getCookies(self) -> dict:
        return self.session.cookies.get_dict()

    def isLoggedIn(self) -> bool:
        return self.session is not None

    def __genDriver(self, browserName: str):
        if browserName == "CHROME":
            options = webdriver.ChromeOptions()
            options.headless = True
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        elif browserName == "FIREFOX":
            options = webdriver.FirefoxOptions()
            options.headless = True
            driver = webdriver.Firefox(
                GeckoDriverManager().install(),
                options=options,
            )
        elif browserName == "EDGE":
            options = webdriver.EdgeOptions()
            options.headless = True
            driver = webdriver.Edge(
                EdgeChromiumDriverManager().install(), options=options
            )
        else:
            raise Exception("Browser type is not supported.")

        driver.set_window_size(1920, 1080)
        driver.maximize_window()
        return driver
