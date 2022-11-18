Feature: upload private files
  Background:
    Given user is logged in
    When user visits the home page of BKeL
    And user sets English as their preferred language

  @multibrowser
  Scenario: normal flow
    When user clicks on 'Private files' in user menu
    Then system displays the file manager
    When user clicks on the 'Add file' button of file manager
    And user selects 'normal.txt' to upload
    And user clicks on 'Save changes' button
    Then user sees 'normal.txt' in the list of uploaded files
