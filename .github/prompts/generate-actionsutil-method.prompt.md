---
description: "Generate a new ActionsUtil method for reusable UI operations"
agent: "test-generator"
---

Generate an ActionsUtil method for `{{input}}` using this EXACT pattern:

## BEFORE creating — check existing:

```bash
grep -n "public static" "$SRC/.../utils/{Entity}ActionsUtil.java"
cat config/entity_inventory/{module}_{entity}.yaml | grep -A20 'actions_util_methods'
```

**If a method with the same click sequence exists but with different string → PARAMETERIZE it.**

## Method declaration — EXACT structure:

```java
public static void {descriptiveActionName}(String {param}) throws Exception {
    // One complete named UI operation — NOT a single click, NOT an entire test
    actions.click({Entity}Locators.{Section}.{LOCATOR});
    actions.click({Entity}Locators.{Section}.{OPTION_LOCATOR}.apply({param}));
}
```

## Rules:

1. **Class**: `public final class {Entity}ActionsUtil extends Utilities` — ALL methods `public static`
2. **No redundant waits**: `actions.click()` already calls `waitForAjaxComplete()` — NEVER add between clicks
3. **No thin wrappers**: If the method is just one `actions.click()` → don't create it, call directly
4. **Parameterize**: If two operations differ by one string only → ONE method with a parameter
5. **No modify existing**: NEVER change an existing public static method — create a new one

## CORRECT example (from ChangeActionsUtil.java):

```java
public static void navigateToChangesListView() throws Exception {
    actions.navigate.toModule(ModuleConstants.CHANGES);
    actions.setTableView(GlobalConstants.listView.LISTVIEW);
}

public static void clickLHSSubtab(String subtab) throws Exception {
    actions.click(ChangeLocators.ChangeDetailsview.LHS_SUBTAB.apply(subtab));
}
```

## FORBIDDEN:

```java
// Single-click wrapper — unnecessary
public static void clickSaveButton() { actions.click(SAVE_BUTTON); }

// Duplicate — same flow, different string
public static void openAttachParentPopup() { /* click dropdown, click "Parent" */ }
public static void openAttachChildPopup()  { /* click dropdown, click "Child"  */ }
// → CORRECT: openAttachPopup(String type)
```
