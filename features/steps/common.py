# -*- coding: utf-8 -*-
from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils.driver_handler import DriverHandler

"""
Steps or functions that are re-used very often
"""
use_step_matcher("re")  # allow using regular expressions


@given("user is logged in")
def user_logged_in(context):
    context.driverHandler.logInDriver(context.driver)
    # confirm that user is logged in
    DriverHandler.waitDriverVisit(
        context.driver, context.driverHandler.buildUrl("BKEL")
    )
    DriverHandler.waitDriver(
        context.driver, EC.presence_of_element_located((By.ID, "user-action-menu"))
    )


@when("user visits the home page of BKeL")
def visit_bkel_home(context):
    homeUrl = context.driverHandler.buildUrl("BKEL")
    if context.driver.current_url != homeUrl:
        DriverHandler.waitDriverVisit(context.driver, homeUrl)


@when("user sets English as their preferred language")
def prefer_english(context):
    DriverHandler.waitDriverVisit(
        context.driver, context.driverHandler.buildUrl("BKEL", query={"lang": "en"})
    )
    navItem = context.driverHandler.waitDriver(
        context.driver,
        EC.visibility_of_element_located(
            (By.XPATH, "//a[contains(@class,'nav-link active') and @role='menuitem']")
        ),
    )
    assert navItem.text == "HOME"


@when("user clicks on '(.*?)' in user menu")
def click_on_usermenu_option(context, option):
    link = DriverHandler.waitDriver(
        context.driver,
        EC.presence_of_element_located(
            (
                By.XPATH,
                f"//div[@id='user-action-menu']//*[text()[contains(.,'{option}')]]",
            )
        ),
    )
    context.driver.execute_script("arguments[0].click();", link)
    DriverHandler.waitDriverVisit(
        context.driver, context.driverHandler.buildUrl("BKEL", path="/user/files.php")
    )


@when("user clicks on '(.*?)' button.*")
def click_unique_text_button(context, buttonText):
    """
    Click on button with unique text.
    The argument buttonText must be unique in order to determine the right element.
    """
    btn = DriverHandler.waitDriver(
        context.driver,
        EC.element_to_be_clickable(
            (
                By.XPATH,
                f"//*[contains(@class,'btn') and ((text()='{buttonText}') or (@value='{buttonText}') or (@title='{buttonText}'))]",
            )
        ),
    )
    context.driver.execute_script("arguments[0].click();", btn)


@then("system displays a dialog saying that '(.*?)'")
def system_display_dialog(context, dialogText):
    DriverHandler.waitDriver(
        context.driver,
        EC.presence_of_all_elements_located(
            (By.XPATH, f"//*[contains(@class,'dialogue')]//*[text()='{dialogText}']")
        ),
    )
