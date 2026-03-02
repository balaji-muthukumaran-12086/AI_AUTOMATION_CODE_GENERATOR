# Feature Specification: Solution Approval Workflow

**Module:** Solutions  
**Feature Area:** Solution creation and approval  
**Document Type:** Feature Specification  

---

## Overview

The Solution module in ServiceDesk Plus allows technicians to create knowledge articles
(called Solutions) and submit them for approval. Approvers can then approve or reject
the submission. Once approved, solutions become visible to end users through the
self-service portal.

---

## Feature: Create Solution and Submit for Approval

### Description
A technician creates a new solution with a title, content, topic, and template, then
submits it for approval. The system should show the solution status as
"Awaiting Approval" in the detail view.

### Acceptance Criteria
1. Technician navigates to Solutions module and clicks New.
2. Fills in title (unique), content/description, selects a topic, and selects a template.
3. Clicks "Add And Approve" to submit for approval.
4. System shows success notification.
5. Solution detail view shows title correctly and status is "Awaiting Approval".

---

## Feature: Create Private Unapproved Solution

### Description
A technician creates a new private (not public) solution without submitting for approval.
The solution should be saved as a draft with unapproved status.

### Acceptance Criteria
1. Technician navigates to Solutions module and clicks New.
2. Fills in title (with unique timestamp suffix) and content using default template.
3. Does NOT check the "Is Public" checkbox — solution remains private.
4. Clicks "Add" (not "Add And Approve") to save without approval.
5. Solution detail view displays the correct title.
6. Solution status shows as unapproved/pending.

---

## Feature: Share Approved Public Solution

### Description
After an approved public solution is created, the technician can share it with
specific users or groups from the detail view using the Share action.

### Acceptance Criteria
1. An approved public solution exists in the system.
2. Technician opens the solution's detail view.
3. Clicks the "Share" button in the action bar.
4. A popup appears to select recipients.
5. Technician selects recipients and confirms.
6. System shows "Solutions shared" success message.

---

## Notes for Test Generation

- Module path: `modules/solutions/solution`
- All solution titles should use `$(unique_string)` placeholder for uniqueness.
- Template selection uses the default solution template unless specified.
- The "Is Public" flag is a checkbox — must be handled via explicit click, not fillInputForAnEntity.
- Approval is triggered via the "Add And Approve" button (use XPath: `normalize-space(text())='Add And Approve'`).
- Save without approval uses the "Add" button (use XPath: `normalize-space(text())='Add'`).
