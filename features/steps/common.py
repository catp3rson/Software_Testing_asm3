# -*- coding: utf-8 -*-
from behave import *
from utils.user_session import UserSession

"""
Steps that are re-used very often
"""


@given("user is logged in")
def user_logged_in(context):
    if not context.userSession.isLoggedIn():
        context.userSession.logIn()
    assert len(context.userSession.getSessKey()) == 10
    # copy the cookies from context.userSession to
    # context.driver to use the session
    cookies = context.userSession.getCookies()
    print(context.userSession.config["SSO_DOMAIN"][8:])
    # set cookies for SSO_DOMAIN
    context.driver.get(context.userSession.config["SSO_DOMAIN"] + "/cas/login")
    context.driver.add_cookie(
        {
            "name": "CASTGC",
            "value": cookies["CASTGC"],
            "domain": context.userSession.config["SSO_DOMAIN"][8:],
            "sameSite": "Strict",
        }
    )
    context.driver.add_cookie(
        {
            "name": "JSESSIONID",
            "value": cookies["JSESSIONID"],
            "domain": context.userSession.config["SSO_DOMAIN"][8:],
            "sameSite": "Strict",
        }
    )
    # set cookies for BKEL_DOMAIN
    context.driver.get(context.userSession.config["BKEL_DOMAIN"])
    context.driver.add_cookie(
        {
            "name": "MoodleSession",
            "value": cookies["MoodleSession"],
            "domain": context.userSession.config["BKEL_DOMAIN"][8:],
            "sameSite": "Strict",
        }
    )
    context.driver.add_cookie(
        {
            "name": "MOODLEID1_",
            "value": cookies["MOODLEID1_"],
            "domain": context.userSession.config["BKEL_DOMAIN"][8:],
            "sameSite": "Strict",
        }
    )


@when("user visits the home page of BKeL")
def visit_bkel_home(context):
    context.driver.get(context.userSession.config["BKEL_DOMAIN"])
    assert context.driver.title == "BKEL - HỆ THỐNG HỖ TRỢ GIẢNG DẠY VÀ HỌC TẬP"
