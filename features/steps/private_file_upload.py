# -*- coding: utf-8 -*-
import os
from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@when("user clicks on 'Private files' in user menu")
def access_private_files(context):
    link = context.driver.find_element(
        By.XPATH, "//*[text()[contains(.,'Private files')]]"
    )
    context.driver.execute_script("arguments[0].click();", link)
    wait = WebDriverWait(context.driver, 10)
    wait.until(
        lambda _: context.driver.current_url
        == context.userSession.config["BKEL_DOMAIN"] + "/user/files.php"
    )


@then("system displays the file manager")
def file_manager_displayed(context):
    wait = WebDriverWait(context.driver, 10)
    wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "filemanager-container"))
    )


@when("user clicks on the 'Add file' button of file manager")
def click_add_file_btn(context):
    wait = WebDriverWait(context.driver, 10)
    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".fp-toolbar .fp-btn-add"))
    ).click()


@when("user selects '{filename}' to upload")
def select_file_and_upload(context, filename):
    wait = WebDriverWait(context.driver, 10)
    fileUpload = wait.until(EC.element_to_be_clickable((By.NAME, "repo_upload_file")))
    fileUpload.send_keys(os.getcwd() + f"/test_data/private_file_upload/{filename}")
    uploadBtn = context.driver.find_element(By.CLASS_NAME, "fp-upload-btn")
    uploadBtn.click()


@when("user clicks on 'Save changes' button")
def click_save_btn(context):
    wait = WebDriverWait(context.driver, 10)
    saveBtn = wait.until(EC.element_to_be_clickable((By.NAME, "submitbutton")))
    context.driver.execute_script("arguments[0].click();", saveBtn)


@then("user sees '{filename}' in the list of uploaded files")
def see_uploaded_file(context, filename):
    wait = WebDriverWait(context.driver, 20)
    wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                f"//*[text()='{filename}' and contains(@class,'fp-filename')]",
            )
        )
    )
