# Skill: Assertion Patterns

> **When to load**: Writing test validations, using addSuccessReport/addFailureReport,
> checking isElementPresent, or any scenario with negative assertions (element should NOT exist).

## Rule 1: Anti-False-Positive — Two-Phase Assertion (D23)

### INCORRECT — naked negative (passes when UI never loaded):
```java
// If popup never opened, TRASHED_ROW won't exist → test "passes" incorrectly
if (!actions.isElementPresent(TRASHED_CHANGE_ROW)) {
    addSuccessReport("Trashed change excluded from popup");  // FALSE POSITIVE!
}
```

### CORRECT — positive anchor first, then negative check:
```java
// Phase 1: Verify the correct UI state was reached
if (!actions.isElementPresent(POPUP_HEADER)) {
    addFailureReport("Popup never opened — cannot verify exclusion", "");
    return;
}
// Phase 2: NOW safe to check absence
if (!actions.isElementPresent(TRASHED_CHANGE_ROW)) {
    addSuccessReport("Trashed change correctly excluded from popup");
} else {
    addFailureReport("Trashed change visible in popup", "Should have been excluded");
}
```

### Real codebase example (DetailsView.java — attach then verify detach):
```java
// First verify attach succeeded (positive anchor):
if (actions.isElementPresent(
        ChangeLocators.ChangeListview.SELECT_CHECKBOX_WITH_ENTITYID.apply(
            LocalStorage.getAsString("requestid")))) {
    addSuccessReport("Request associated under Requests Caused by Change");
} else {
    addFailureReport("Request not associated", "Request not found");
}

// Then perform detach and verify removal (negative assertion is now safe):
actions.click(ChangeLocators.ChangeDetailsview.ATTACH_DETACH_REQUEST.apply(
    ChangeConstants.DetailsPageConstants.REQUESTS_DETACH));

if (!actions.isElementPresent(
        ChangeLocators.ChangeListview.SELECT_CHECKBOX_WITH_ENTITYID.apply(
            LocalStorage.getAsString("requestid")))) {
    addSuccessReport("Request detached successfully");
} else {
    addFailureReport("Request still visible after detach", "Detach failed");
}
```

## Rule 2: Report Method Usage

### addReport() — smart variant:
```java
// Inspects failureMessage.length():
//   == 0 → calls addSuccessReport(message)
//   >  0 → calls addFailureReport(message, failureMessage)
addReport("Step completed");
// clearFailureMessage() is called automatically inside every addReport()
```

### addSuccessReport(message):
```java
addSuccessReport("SDPOD_001: Change title verified in detail view");
```

### addFailureReport(message, detail):
```java
addFailureReport("Change title mismatch",
    "Expected: " + expected + ", Got: " + actual);
```

## Rule 3: validate.textContent — Check Return Value

### INCORRECT — ignoring the return value:
```java
actions.validate.textContent(TITLE_LOCATOR, expectedTitle);
addSuccessReport("Title verified");  // passes even if textContent returned false!
```

### CORRECT — check the boolean:
```java
if (actions.validate.textContent(TITLE_LOCATOR, expectedTitle)) {
    addSuccessReport("Title matches expected value");
} else {
    addFailureReport("Title mismatch", "Expected: " + expectedTitle);
}
```

## Rule 4: Report Wrapping — Every Test Method (D19)

```java
public void myTestMethod() throws Exception {
    report.startMethodFlowInStepsToReproduce(
        AutomaterUtil.getPascalValueFromCamelCase(getMethodName()));
    try {
        // ... test logic ...
    } catch (Exception exception) {
        addFailureReport("Internal error: " + getMethodName(), exception.getMessage());
    } finally {
        report.endMethodFlowInStepsToReproduce();
    }
}
```

## Rule 5: Accumulating Failures (Multi-Step Validation)

```java
StringBuilder failureMessage = new StringBuilder();

// Step 1
if (!actions.validate.textContent(TITLE_LOC, expectedTitle)) {
    failureMessage.append("Title mismatch. ");
}
// Step 2
if (!actions.validate.textContent(STATUS_LOC, expectedStatus)) {
    failureMessage.append("Status mismatch. ");
}
// Step 3
if (!actions.isElementPresent(EXPECTED_TAB)) {
    failureMessage.append("Expected tab not visible. ");
}

// Final verdict
if (failureMessage.length() == 0) {
    addSuccessReport("All validations passed");
} else {
    addFailureReport("Validation failures", failureMessage.toString());
}
```

## Common Assertion Patterns

| What to verify | Method | Return |
|---|---|---|
| Element exists | `actions.isElementPresent(locator)` | boolean |
| Text content | `actions.validate.textContent(locator, text)` | Boolean |
| Alert message | `actions.validate.successMessageInAlert(msg)` | void (throws) |
| Field value in DV | `actions.detailsView.verifyFieldInDetailsPage(field, value)` | boolean |
| Title in DV | `actions.detailsView.verifyTitleInDetailsPage(title)` | boolean |
