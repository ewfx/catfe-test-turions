Feature: Login to Parabank
  As a user, I want to log into Parabank so that I can access my account.

  Scenario: Valid Login
    Given the user is on the Parabank login page
    When the user enters valid credentials
    And clicks on the login button
    Then the user should be redirected to the Accounts Overview page

  Scenario: Invalid Login
    Given the user is on the Parabank login page
    When the user enters invalid credentials
    And clicks on the login button
    Then the user should see an error message
