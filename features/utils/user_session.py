# -*- coding: utf-8 -*-
import requests
import re
from urllib.parse import urlunparse, urlencode
from collections import namedtuple

Components = namedtuple(
    typename="Components",
    field_names=["scheme", "netloc", "path", "params", "query", "fragment"],
)


class UserSession:
    def __init__(self, domains: dict[str, dict[str, str]]):
        if not ("SSO" in domains and "BKEL" in domains):
            raise Exception("Domains needed for authentication are not specified")
        if not ("name" in domains["SSO"] and "name" in domains["BKEL"]):
            raise Exception("Domain names are not specified")
        if not ("username" in domains["SSO"] and "password" in domains["SSO"]):
            raise Exception("Credentials needed for authentication are not specified")
        self.domains = domains
        self.session = None
        self.sessKey = None

    def logIn(self, force: bool = False) -> tuple[dict, str]:
        """
        Log in to BKeL via SSO service without interacting with the Web UI
        """
        if self.session is not None:
            if force:
                self.logOut()
            else:
                return (self.session.cookies.get_dict(), self.sessKey)
        self.session = requests.Session()
        # get JSESSIONID
        self.session.get(url=self.buildUrl("SSO", path="/cas/login"))
        # get CSRF token
        response = self.session.get(url=self.buildUrl("SSO", path="cas/login"))
        tmp = re.search(r'"(LT-\d+-[A-Za-z0-9]+)"', response.text)
        lt = tmp.group(1)
        tmp = re.search(r'name="execution" value="(.*?)"', response.text)
        execution = tmp.group(1)
        # authenticate
        response = self.session.post(
            url=self.buildUrl("SSO", path="/cas/login"),
            data={
                "username": self.domains["SSO"]["username"],
                "password": self.domains["SSO"]["password"],
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
            url=self.buildUrl(
                "BKEL", path="/login/index.php", query={"authCAS": "CAS"}
            ),
            allow_redirects=True,
        )
        # extract sessKey
        tmp = re.search(r'"sesskey":"(.*?)"', response.text)
        self.sessKey = tmp.group(1)
        return (self.session.cookies.get_dict(), self.sessKey)

    def logOut(self) -> bool:
        """
        Log out of BKeL and SSO service.
        Return True if succeeded.
        """
        if self.session is None:
            return False
        self.session.get(
            url=self.buildUrl(
                "BKEL", path="/login/logout.php", query={"sesskey": self.sessKey}
            ),
            allow_redirects=True,
        )
        self.session = self.sessKey = None
        return True

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

    def buildUrl(
        self,
        domain: str,
        scheme: str = "https",
        path: str = "/",
        params: dict = None,
        query: dict = None,
        fragment: str = "",
    ):
        if not (domain == "SSO" or domain == "BKEL"):
            raise Exception("Unknown domain")
        return urlunparse(
            Components(
                scheme=scheme,
                netloc=self.domains[domain]["name"],
                path=path,
                params=urlencode(params) if params is not None else "",
                query=urlencode(query) if query is not None else "",
                fragment=fragment,
            )
        )
