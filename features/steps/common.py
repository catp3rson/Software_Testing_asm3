# -*- coding: utf-8 -*-
from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


"""
Steps or functions that are re-used very often
"""


@given("user is logged in")
def user_logged_in(context):
    context.userSession.logIn()
    # confirm that user is logged in
    context.driver.get(context.config["BKEL_DOMAIN"])
    wait = WebDriverWait(context.driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "user-action-menu")))


@when("user visits the home page of BKeL")
def visit_bkel_home(context):
    if context.driver.current_url != context.config["BKEL_DOMAIN"] + "/":
        context.driver.get(context.config["BKEL_DOMAIN"])
        assert context.driver.current_url == context.config["BKEL_DOMAIN"] + "/"


@when("user sets English as their preferred language")
def prefer_english(context):
    context.driver.get(context.config["BKEL_DOMAIN"] + "/?lang=en")
    wait = WebDriverWait(context.driver, 10)
    navItem = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//a[contains(@class,'nav-link active') and @role='menuitem']")
        )
    )
    assert navItem.text == "HOME"
