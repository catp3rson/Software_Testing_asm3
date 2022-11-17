# -*- coding: utf-8 -*-
from behave import *
from selenium.webdriver.common.by import By

"""
Steps that are re-used very often
"""


@given("user is logged in")
def user_logged_in(context):
    if not context.userSession.isLoggedIn():
        context.userSession.logIn()
        # copy the cookies from context.userSession to
        # context.driver to use the session
        cookies = context.userSession.getCookies()

        # set cookies for BKEL_DOMAIN
        context.driver.get(context.userSession.config["BKEL_DOMAIN"])
        context.driver.delete_cookie("MoodleSession")
        context.driver.add_cookie(
            {
                "name": "MOODLEID1_",
                "value": cookies["MOODLEID1_"],
            }
        )
        context.driver.add_cookie(
            {"name": "MoodleSession", "value": cookies["MoodleSession"]}
        )
        context.driver.refresh()
        context.driver.find_element(By.ID, "user-action-menu")


@when("user visits the home page of BKeL")
def visit_bkel_home(context):
    context.driver.get(context.userSession.config["BKEL_DOMAIN"])
    assert context.driver.current_url == context.userSession.config["BKEL_DOMAIN"] + "/"
    assert context.driver.title == "BKEL - HỆ THỐNG HỖ TRỢ GIẢNG DẠY VÀ HỌC TẬP"
