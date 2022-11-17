# -*- coding: utf-8 -*-
import requests
import re
from utils.config import CONFIG


class UserSession:
    def __init__(self):
        self.session = None
        self.config = None

    def setConfig(self, config: dict) -> None:
        if not (config["SSO_USERNAME"] and config["SSO_PASSWORD"]):
            raise Exception("Credentials needed for authentication are not set")
        self.config = config

    def logIn(self) -> None:
        """
        Log in to BKeL via SSO service without interacting with the Web UI
        """
        if self.config is None:
            raise Exception("Configurations needed for authentication are not set")
        if self.session is not None:
            self.logOut()
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

    def logOut(self) -> None:
        """
        Log out of BKeL and SSO service
        """
        if self.session is None:
            return
        self.session.get(
            url=self.config["BKEL_DOMAIN"] + "/login/logout.php?sesskey={self.sessKey}",
            allow_redirects=True,
        )
        self.session = None

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


if __name__ == "__main__":
    us = UserSession()
    us.setConfig(CONFIG)
    us.logIn()
    cookies, sessKey = us.getSessionInfo()
    print(cookies)
    assert len(sessKey) == 10
    assert cookies["CASTGC"].startswith("TGT-") and cookies["CASTGC"].endswith(
        "-sso.hcmut.edu.vn"
    )
    us.logOut()
