Feature: upload private files
  Background:
    Given user is logged in
    When user visits the home page of BKeL
    And user sets English as their preferred language

  Scenario: normal flow
    And user clicks on 'Private files' in user menu
    And user clicks on the 'Add file' button of file manager
    And user selects 'normal.txt' to upload and clicks upload button
    And user clicks on 'Save changes' button
    Then user sees 'normal.txt' in the list of uploaded files
