Feature: User Authentication
  As a new user
  I want to create an account and log in
  So that I can manage my personal tasks

  Scenario: Successful user registration
    Given I am on the registration page
    When I enter a valid email "newuser@example.com"
    And I enter a secure password "SecurePass123!"
    And I enter my full name "New User"
    And I click the register button
    Then I should see a success message
    And I should be redirected to the login page

  Scenario: Registration with duplicate email
    Given I am on the registration page
    And a user with email "existing@example.com" already exists
    When I enter the email "existing@example.com"
    And I enter a secure password "SecurePass123!"
    And I click the register button
    Then I should see an error message "already exists"
    And I should remain on the registration page

  Scenario: Registration with invalid email format
    Given I am on the registration page
    When I enter an invalid email "not-an-email"
    And I enter a secure password "SecurePass123!"
    And I click the register button
    Then I should see a validation error for email
    And I should remain on the registration page

  Scenario: Registration with missing password
    Given I am on the registration page
    When I enter a valid email "user@example.com"
    And I leave the password field empty
    And I click the register button
    Then I should see a validation error for password
    And I should remain on the registration page

  Scenario: Successful login
    Given a user with email "login@example.com" and password "LoginPass123!" exists
    And I am on the login page
    When I enter the email "login@example.com"
    And I enter the password "LoginPass123!"
    And I click the login button
    Then I should see a success message
    And I should be redirected to the dashboard
    And a JWT token should be stored in local storage

  Scenario: Login with wrong password
    Given a user with email "user@example.com" and password "CorrectPass123!" exists
    And I am on the login page
    When I enter the email "user@example.com"
    And I enter the wrong password "WrongPass123!"
    And I click the login button
    Then I should see an error message "Incorrect email or password"
    And I should remain on the login page
    And no JWT token should be stored

  Scenario: Login with non-existent user
    Given I am on the login page
    When I enter the email "nonexistent@example.com"
    And I enter any password "SomePass123!"
    And I click the login button
    Then I should see an error message "Incorrect email or password"
    And I should remain on the login page

  Scenario: Access protected route without authentication
    Given I am not logged in
    When I try to visit the dashboard page
    Then I should be redirected to the login page
    And I should not see my tasks

  Scenario: Logout
    Given I am logged in as a user
    And I am on the dashboard page
    When I click the logout button
    Then I should be redirected to the login page
    And the JWT token should be removed from local storage
    And I should no longer have access to the dashboard
