# Test Pattern Templates
# ======================
# Standard patterns the AI MUST follow for each test type.
# Each template shows the required structure, assertions, and pitfalls to avoid.
#
# Usage: AI reads the relevant template before generating any scenario of that type.
# Templates reference framework APIs and follow all rules from framework_rules.md.

---

## Pattern: CRUD — Create Entity via UI Form

### Flow:
```
preProcess: (none needed — "NoPreprocess" or create prerequisites like templates)
test method:
  1. Navigate to module
  2. Click "New" / global action
  3. Fill form via fillInputForAnEntity()
  4. Submit
  5. Validate success alert
  6. Validate details page fields match input data
```

### Template:
```java
@AutomaterScenario(
    id = "...", group = "NoPreprocess", priority = Priority.MEDIUM,
    dataIds = {}, tags = {}, description = "Create <entity> via UI form",
    owner = OwnerConstants.XXX, runType = ScenarioRunType.USER_BASED
)
public void create<Entity>() throws Exception {
    create<Entity>Impl();
}

// In Base.java:
protected void create<Entity>Impl() throws Exception {
    JSONObject inputData = getTestCaseData(<Entity>DataConstants.<InnerClass>.CREATE_KEY);

    actions.navigate.toModule(getModuleName());
    actions.navigate.toGlobalActionInListview("New <Entity>");

    actions.formBuilder.fillInputForAnEntity(true, fields, inputData);
    actions.formBuilder.submit();

    actions.validate.successMessageInAlertAndClose("<Entity> added successfully");

    // Validate key fields on details page
    String title = inputData.getJSONObject("data").getString("title");
    if (actions.detailsView.verifyTitleInDetailsPage(title)) {
        addSuccessReport("Title matches input: " + title);
    } else {
        addFailureReport("Title mismatch", "Expected: " + title);
    }
}
```

### Pitfalls:
- Missing `runType = ScenarioRunType.USER_BASED` → defaults to PORTAL_BASED → test skipped
- Boolean fields silently skipped by fillInputForAnEntity → must click manually
- Lookup fields must be `{"name": "Value"}` in data JSON, never flat strings

---

## Pattern: Details View — Verify Field Values

### Flow:
```
preProcess: "create" group — creates entity via API, stores ID
test method:
  1. Navigate to details page using stored ID
  2. Read field values via detailsView API
  3. Compare against expected values
```

### Template:
```java
@AutomaterScenario(
    id = "...", group = "create",
    dataIds = {<Entity>AnnotationConstants.Data.CREATE_API},
    priority = Priority.MEDIUM, tags = {},
    description = "Verify <entity> detail view field values",
    owner = OwnerConstants.XXX, runType = ScenarioRunType.USER_BASED
)
public void verifyDetailViewFields() throws Exception {
    verifyDetailViewFieldsImpl();
}

// In Base.java:
protected void verifyDetailViewFieldsImpl() throws Exception {
    String entityId = getEntityId();
    actions.navigate.toModule(getModuleName());
    actions.navigate.toDetailsPageUsingRecordId(entityId);

    // Verify title
    String expectedTitle = LocalStorage.getAsString("<entity>Name");
    if (actions.detailsView.verifyTitleInDetailsPage(expectedTitle)) {
        addSuccessReport("Title verified: " + expectedTitle);
    } else {
        addFailureReport("Title mismatch", "Expected: " + expectedTitle
            + ", Got: " + actions.detailsView.getTitle());
    }

    // Verify RHS field
    String status = actions.detailsView.getValueFromRhsDetails("Status");
    if ("Open".equals(status)) {
        addSuccessReport("Status is Open");
    } else {
        addFailureReport("Status mismatch", "Expected: Open, Got: " + status);
    }
}
```

---

## Pattern: Linking / Association via UI

### Flow:
```
preProcess: Create 2+ entities via API (parent + child or source + target)
            Store IDs and names in LocalStorage
            DO NOT link via API — linking is the feature under test
test method:
  1. Navigate to source entity details page
  2. Open Associations tab
  3. Click Attach dropdown → select association type
  4. Search for target entity in popup
  5. Select and save
  6. POSITIVE ANCHOR: verify association row appeared
  7. Validate association details (name, ID, count)
```

### Template:
```java
// preProcess group creates TWO changes via API:
// LocalStorage: getName() → sourceChangeId, "targetChangeName" → name, "targetChangeId" → id

protected void linkParentChangeImpl() throws Exception {
    String targetName = LocalStorage.getAsString("targetChangeName");
    String targetId = LocalStorage.getAsString("targetChangeId");

    // Navigate to source change
    actions.navigate.toModule(getModuleName());
    actions.navigate.toDetailsPageUsingRecordId(getEntityId());

    // Open Associations tab
    <Entity>ActionsUtil.openAssociationsTab();

    // POSITIVE ANCHOR: Associations tab loaded
    if (!actions.isElementPresent(<Entity>Locators.Associations.TAB_HEADER)) {
        addFailureReport("Associations tab did not load");
        return;
    }

    // Link via UI (the feature under test)
    <Entity>ActionsUtil.attachParentChange(targetName);

    // Verify link appeared
    if (actions.isElementPresent(<Entity>Locators.Associations.PARENT_CHANGE_ROW)) {
        addSuccessReport("Parent change linked: " + targetName);
    } else {
        addFailureReport("Parent change not linked", "Expected: " + targetName);
    }
}
```

### Pitfalls:
- NEVER link in preProcess via API — linking IS the feature under test
- Check api_registry.yaml — most linking endpoints don't exist in V3
- Popup search uses `actions.popUp.listView.columnSearch()` NOT `actions.listView.columnSearch()`

---

## Pattern: Trash Exclusion — Verify Trashed Entity Not in Popup/List

### Flow:
```
preProcess: Create entity via API → trash it via API → create another entity (active)
            Both IDs/names in LocalStorage
test method:
  1. Navigate to context where popup/list appears
  2. Open the popup/list
  3. POSITIVE ANCHOR: popup/list loaded (header visible, or active entity visible)
  4. NEGATIVE TEST: trashed entity NOT in the popup/list
  5. Verify active entity IS in the popup/list (double confirmation)
```

### Template:
```java
protected void verifyTrashedNotInPopupImpl() throws Exception {
    String trashedName = LocalStorage.getAsString("trashedChangeName");
    String activeName = LocalStorage.getAsString("activeChangeName");

    actions.navigate.toModule(getModuleName());
    actions.navigate.toDetailsPageUsingRecordId(getEntityId());

    // Open the popup where linking happens
    <Entity>ActionsUtil.openAssociationsTab();
    <Entity>ActionsUtil.openAttachPopup("Child Changes");

    // POSITIVE ANCHOR: popup opened (MANDATORY before any negative assertion)
    if (!actions.isElementPresent(<Entity>Locators.Popup.POPUP_HEADER)) {
        addFailureReport("Linking popup did not open — cannot verify trash exclusion");
        return;  // ← CRITICAL: do not proceed to negative assertion
    }
    addSuccessReport("Popup opened successfully");

    // Search for ACTIVE entity first (proves search works)
    actions.popUp.listView.columnSearch("Title", activeName);
    if (actions.isElementPresent(<Entity>Locators.Popup.FIRST_ROW)) {
        addSuccessReport("Active entity found in popup: " + activeName);
    } else {
        addFailureReport("Active entity missing from popup", activeName);
        return;
    }

    // NOW safe: search for TRASHED entity (must NOT appear)
    actions.popUp.listView.columnSearch("Title", trashedName);
    if (!actions.isElementPresent(<Entity>Locators.Popup.FIRST_ROW)) {
        addSuccessReport("Trashed entity correctly excluded: " + trashedName);
    } else {
        addFailureReport("Trashed entity found in popup", trashedName + " should be excluded");
    }
}
```

### Pitfalls:
- MOST COMMON FALSE POSITIVE: `!isElementPresent` succeeds because popup never opened
- ALWAYS anchor with positive proof BEFORE negative assertion
- Use `actions.popUp.listView.*` for popup interactions, not `actions.listView.*`

---

## Pattern: RBAC — Role-Based Access Permission Test

### Flow:
```
preProcess:
  1. deleteScenarioUser(TEST_USER_N) — clean slate
  2. createUserByRole(TECHNICIAN, module, roleKey, user) — create role user
  3. Create test data in admin session
test method:
  1. switchUser(user) — switch to role user
  2. Navigate to the feature under test
  3. Verify what the role CAN do (positive)
  4. Verify what the role CANNOT do (with positive anchor!)
  5. switchToAdminSession() — clean up
```

### Template:
```java
// preProcess group:
protected boolean preProcess(String group, String[] dataIds) {
    if ("createRoleUser".equalsIgnoreCase(group)) {
        try {
            deleteScenarioUser(ScenarioUsers.TEST_USER_3);
            User user = scenarioDetails.getUser(ScenarioUsers.TEST_USER_3);
            actions.createUserByRole(AutomaterConstants.TECHNICIAN,
                getModuleName(), "ViewOnly_Role", user);
            LocalStorage.store("techName", user.getDisplayId());

            // Create entity for the user to view
            JSONObject data = getTestCaseDataUsingCaseId(dataIds[0]);
            JSONObject resp = restAPI.createAndGetResponse(getName(), getModuleName(), getInputData(data));
            LocalStorage.store(getName(), resp.getString("id"));
            LocalStorage.store("<entity>Name", resp.getString("title"));
            return true;
        } catch (Exception e) {
            report.addCaseFlow("preProcess failed: " + e.getMessage());
            addFailureReport("preProcess failed", e.getMessage());
            return false;
        }
    }
    return super.preProcess(group, dataIds);
}

// Test method:
protected void verifyViewOnlyCannotEditImpl() throws Exception {
    User user = scenarioDetails.getUser(ScenarioUsers.TEST_USER_3);
    actions.switchUser(user);

    actions.navigate.toModule(getModuleName());
    actions.navigate.toDetailsPageUsingRecordId(getEntityId());

    // POSITIVE: page loaded (anchor)
    String title = LocalStorage.getAsString("<entity>Name");
    if (actions.detailsView.verifyTitleInDetailsPage(title)) {
        addSuccessReport("Details page loaded for view-only user");
    } else {
        addFailureReport("Details page did not load");
        switchToAdminSession();
        return;
    }

    // NEGATIVE (with anchor proven): Edit button should not be visible
    if (!actions.isElementPresent(<Entity>Locators.EDIT_BUTTON)) {
        addSuccessReport("Edit button correctly hidden for view-only role");
    } else {
        addFailureReport("Edit button visible for view-only role", "Should be hidden");
    }

    switchToAdminSession();
}
```

### Pitfalls:
- NEVER test RBAC as admin — admin always has all permissions
- ALWAYS call deleteScenarioUser BEFORE createUserByRole
- Double negative: "verify user CANNOT" → still needs positive anchor first

---

## Pattern: List View — Column Search, Filter, Sort

### Flow:
```
preProcess: Create entity via API (provides a known record in the list)
test method:
  1. Navigate to module (lands on list view)
  2. Apply filter/sort/column search
  3. Verify expected record appears
  4. Verify record count, field values, column order as needed
```

### Template:
```java
protected void verifyColumnSearchImpl() throws Exception {
    String entityName = LocalStorage.getAsString("<entity>Name");

    actions.navigate.toModule(getModuleName());

    // Column search
    actions.listView.columnSearch("Title", entityName);

    // Verify result
    String firstRowTitle = actions.listView.getFieldValueFromFirstRow("title");
    if (entityName.equals(firstRowTitle)) {
        addSuccessReport("Column search found: " + entityName);
    } else {
        addFailureReport("Column search mismatch",
            "Expected: " + entityName + ", Got: " + firstRowTitle);
    }
}
```

---

## Pattern: Spot Edit — Inline Field Edit on Details Page

### Flow:
```
preProcess: Create entity via API
test method:
  1. Navigate to details page
  2. Spot-edit a field (click → type → save)
  3. Refresh/re-read the field
  4. Verify new value persists
```

### Template:
```java
protected void spotEditPriorityImpl() throws Exception {
    actions.navigate.toModule(getModuleName());
    actions.navigate.toDetailsPageUsingRecordId(getEntityId());

    String newValue = "High";
    actions.detailsView.spotEditFieldUsingSearch("Priority", newValue);

    // Verify
    String actual = actions.detailsView.getValueFromRhsDetails("Priority");
    if (newValue.equals(actual)) {
        addSuccessReport("Spot edit priority changed to: " + newValue);
    } else {
        addFailureReport("Spot edit failed", "Expected: " + newValue + ", Got: " + actual);
    }
}
```

---

## Pattern: Bulk Action — Select Multiple Records + Apply Action

### Flow:
```
preProcess: Create 2+ entities via API
test method:
  1. Navigate to module list view
  2. Select checkboxes for target records
  3. Click bulk action button
  4. Choose action from dropdown
  5. Confirm if needed
  6. Verify action applied (status change, deletion, etc.)
```

### Template:
```java
protected void bulkCloseImpl() throws Exception {
    actions.navigate.toModule(getModuleName());

    // Select records
    actions.listView.selectCheckBoxInListViewPage("1");
    actions.listView.selectCheckBoxInListViewPage("2");

    // Apply bulk action
    actions.listView.clickBulkActionButton("Close");
    // Handle confirmation dialog if present
    actions.click(CommonLocators.CONFIRM_YES);

    actions.validate.successMessageInAlertAndClose("updated successfully");
    addSuccessReport("Bulk close applied successfully");
}
```
