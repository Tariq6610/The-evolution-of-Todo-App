Feature: Task Management
  As an authenticated user
  I want to create, view, update, and delete my tasks
  So that I can manage my personal todo items

  Background:
    Given I am logged in as "user@example.com"

  Scenario: Create a new task with minimal data
    When I navigate to the dashboard
    And I enter a task title "Buy groceries"
    And I click the "Add Task" button
    Then I should see the task "Buy groceries" in my task list
    And the task should have status "PENDING"
    And the task should have priority "MEDIUM"

  Scenario: Create a task with all fields
    When I navigate to the dashboard
    And I enter a task title "Complete project report"
    And I enter a description "Finish the quarterly report by Friday"
    And I select priority "HIGH"
    And I add tags "work,urgent"
    And I click the "Add Task" button
    Then I should see the task "Complete project report" in my task list
    And the task should have description "Finish the quarterly report by Friday"
    And the task should have priority "HIGH"
    And the task should have tags "work,urgent"

  Scenario: Create task with empty title
    When I navigate to the dashboard
    And I leave the title field empty
    And I click the "Add Task" button
    Then I should see a validation error for the title field
    And the task should not be added to my list

  Scenario: View all my tasks
    Given I have created tasks:
      | title            | priority | status     |
      | Buy groceries     | MEDIUM    | PENDING     |
      | Complete project  | HIGH      | COMPLETED   |
      | Call mom         | LOW       | PENDING     |
    When I navigate to the dashboard
    Then I should see 3 tasks in my list
    And I should see task "Buy groceries"
    And I should see task "Complete project"
    And I should see task "Call mom"
    And the tasks should be ordered by creation date

  Scenario: Update an existing task
    Given I have created a task "Buy groceries" with priority "MEDIUM"
    When I click the edit button for task "Buy groceries"
    And I change the title to "Buy groceries and milk"
    And I change the priority to "HIGH"
    And I save the changes
    Then I should see the updated task "Buy groceries and milk" in my list
    And the task should have priority "HIGH"
    And the updated_at timestamp should be recent

  Scenario: Delete a task
    Given I have created a task "Old completed task"
    When I click the delete button for task "Old completed task"
    And I confirm the deletion
    Then I should not see task "Old completed task" in my list
    And I should see a success message confirming deletion

  Scenario: Cancel task deletion
    Given I have created a task "Maybe delete this"
    When I click the delete button for task "Maybe delete this"
    And I cancel the deletion dialog
    Then I should still see task "Maybe delete this" in my list
    And the task should remain unchanged

  Scenario: Toggle task status to completed
    Given I have created a task "Finish documentation"
    And the task has status "PENDING"
    When I click the checkbox for task "Finish documentation"
    Then the task status should change to "COMPLETED"
    And the task title should be crossed out
    And the updated_at timestamp should be recent

  Scenario: Toggle task status back to pending
    Given I have created a task "Reopen this task"
    And the task has status "COMPLETED"
    When I click the checkbox for task "Reopen this task"
    Then the task status should change to "PENDING"
    And the task title should not be crossed out
    And the updated_at timestamp should be recent

  Scenario: Access tasks without authentication
    Given I am not logged in
    When I try to navigate to the dashboard
    Then I should be redirected to the login page
    And I should not see any tasks

  Scenario: Task persistence across sessions
    Given I have created a task "Persistent task"
    And I log out
    When I log back in as "user@example.com"
    Then I should see task "Persistent task" in my task list
    And the task data should be unchanged

  Scenario: Multiple status toggles
    Given I have created a task "Toggle me multiple times"
    When I click the checkbox for the task 3 times
    Then the task status should be "PENDING"  # Started as PENDING
    And the updated_at timestamp should be recent
