# -*- coding: utf-8 -*-
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from utils.user_session import UserSession
from utils.config import CONFIG


def before_all(context):
    # prepare user session
    context.userSession = UserSession()
    context.userSession.setConfig(CONFIG)
    # prepare headless browser
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    context.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


def after_all(context):
    if context.userSession.isLoggedIn():
        context.userSession.logOut()
    context.driver.close()
