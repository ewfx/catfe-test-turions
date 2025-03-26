Feature: Test Generation
  As a QA Engineer
  I want to generate test scenarios from step definitions
  So that I can automate test creation

  Scenario: Generate tests from valid step definitions
    Given I am on the test generation page
    When I enter valid step definitions in the textarea:
      """
      Given a user is logged in
      When they click the profile button
      Then the profile page should load
      """
    And I click the "Generate Tests" button
    Then I should see generated test scenarios containing:
      | Scenario Name        | Description                          |
      | Profile Navigation   | Verify profile page loads on click   |
    And each scenario should have:
      | Step Type | Content                     |
      | Given     | a user is logged in         |
      | When      | they click the profile button |
      | Then      | the profile page should load |

  Scenario: Validate empty step definitions
    Given I am on the test generation page
    When I leave the step definitions textarea empty
    And I click the "Generate Tests" button
    Then I should see an error message "Please enter step definitions"