# -*- coding: utf-8 -*-
from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils.driver_handler import DriverHandler
from common import *


@then("system displays the file manager")
def file_manager_displayed(context):
    DriverHandler.waitDriver(
        context.driver,
        EC.visibility_of_element_located((By.CLASS_NAME, "filemanager-container")),
    )


@when("user selects '(.*?)' to upload")
def select_file_and_upload(context, filename):
    # append filename with random string to avoid
    # conflict with previously uploaded files
    randFile = context.fileHandler.prepareFile(context, filename)
    fileUpload = DriverHandler.waitDriver(
        context.driver, EC.presence_of_element_located((By.NAME, "repo_upload_file"))
    )
    fileUpload.send_keys(randFile)
    uploadBtn = DriverHandler.waitDriver(
        context.driver, EC.element_to_be_clickable((By.CLASS_NAME, "fp-upload-btn"))
    )
    uploadBtn.click()


@then("user sees '(.*?)' in the list of uploaded files")
def see_uploaded_file(context, filename):
    _, randFilename = context.fileHandler.getRandFile(context, filename, True)
    DriverHandler.waitDriver(
        context.driver,
        EC.presence_of_element_located(
            (
                By.XPATH,
                f"//*[text()='{randFilename}' and contains(@class,'fp-filename')]",
            )
        ),
    )


@given("user has already uploaded '(.*?)'")
def already_uploaded_file(context, filename):
    click_on_usermenu_option(context, "Private files")
    file_manager_displayed(context)
    click_unique_text_button(context, "Add...")
    select_file_and_upload(context, filename)
    click_unique_text_button(context, "Save changes")
    see_uploaded_file(context, filename)
