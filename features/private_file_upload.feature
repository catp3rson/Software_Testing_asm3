@multibrowser
Feature: upload private files
  Background:
    Given user is logged in
    When user visits the home page of BKeL
    And user sets English as their preferred language

  Scenario: normal flow
    When user clicks on 'Private files' in user menu
    Then system displays the file manager
    When user clicks on 'Add...' button of file manager
    And user selects 'normal.txt' to upload
    And user clicks on 'Save changes' button
    Then user sees 'normal.txt' in the list of uploaded files

  Scenario: alternative flow 1 - duplicated filename
    Given user has already uploaded 'duplicated.txt'
    When user clicks on 'Private files' in user menu
    Then system displays the file manager
    When user clicks on 'Add...' button of file manager
    And user selects 'duplicated.txt' to upload
    And user clicks on 'Save changes' button
    Then system displays a dialog saying that 'A file with that name has already been attached'
    When user clicks on 'Overwrite' button on the dialog
    Then user sees 'duplicated.txt' in the list of uploaded files
