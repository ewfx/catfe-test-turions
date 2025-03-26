Feature: Test Suite Management
  As a QA Lead
  I want to organize generated tests into suites
  So that I can manage test cases effectively

  Scenario: View test suite details
    Given I navigate from the home page
    When I click "Start updating" on the dashboard
    And I select the "User Authentication" test suite
    Then I should be on the "/test-suite/F001" page
    And I should see the following test scenarios:
      | Scenario Name           |
      | Valid Login             |
      | Invalid Credentials     |
      | Password Reset Request  |
    And each scenario should display:
      - Scenario description
      - Given/When/Then steps
      - Edit button

  Scenario: Filter test scenarios
    Given I am viewing the "User Authentication" test suite
    When I filter by tag "Security"
    Then I should only see scenarios tagged "Security"