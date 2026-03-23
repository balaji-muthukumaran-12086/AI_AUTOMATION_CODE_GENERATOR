---
applyTo: "**/*Locators.java"
---
# Skill: Locator Patterns

> **When to load**: Writing XPath locators, working with Select2 dropdowns, popup tables,
> or diagnosing NoSuchElementException / locator-related test failures.

## Rule 1: Exact Text Match — normalize-space (D18)

### INCORRECT — contains() matches too broadly:
```java
// Matches "Add", "Add And Approve", "Add Note" — all of them
Locator ADD_BUTTON = new Locator(
    By.xpath("//button[contains(text(),'Add')]"),
    "Add button"
);
```

### CORRECT — exact match:
```java
Locator ADD_BUTTON = new Locator(
    By.xpath("//button[normalize-space(text())='Add']"),
    "Add button"
);
```

## Rule 2: Locator Interface Pattern (from ChangeLocators.java)

### Static locator:
```java
public interface ChangeLocators {
    interface ChangeListview {
        Locator FRAME_ZE_NOTIFICATION = new Locator(
            By.xpath("//*[@class='ze_area wcag-focus-visible']"),
            "Editor Iframe"
        );
    }
}
```

### Dynamic locator (Function):
```java
Function<String, Locator> CLICK_ROW_ACTIONS = (entityId) -> new Locator(
    By.xpath("//*[@data-row-id='" + entityId + "']/descendant::span[@class='global-actions-ico']"),
    "Click row actions of change " + entityId
);
```

### Two-parameter locator (BiFunction):
```java
BiFunction<String, String, Locator> CELL = (row, col) -> new Locator(
    By.xpath("//tr[" + row + "]/td[" + col + "]"),
    "Cell at row " + row + ", col " + col
);
```

## Rule 3: Select2 Dropdowns — Renders at Body Level

### INCORRECT — searching inside parent dialog:
```java
// Select2 <li> elements are NOT inside the dialog — they're at <body> level
By.xpath("//div[@class='dialog']//div[contains(@class,'select2-result-label')]")
```

### CORRECT — search at body level:
```java
By.xpath("//div[contains(@class,'select2-result-label')]")
// Or with text match:
By.xpath("//div[contains(@class,'select2-result-label') and text()='High']")
```

## Rule 4: Popup Table Actions — Use popUp.listView (D14)

### INCORRECT — searches the main page behind the popup:
```java
actions.listView.columnSearch("Title", changeName);  // wrong scope!
```

### CORRECT — searches inside the popup:
```java
actions.popUp.listView.columnSearch("Title", changeName);
```

> Framework popup filter methods (`selectFilterUsingSearch`) only work for `slide-down-popup`.
> For custom popups (e.g., `association-dialog-popup`), use custom module locators.

## Rule 5: Checkbox/Boolean — Manual Click Required (D11)

`fillInputForAnEntity` silently skips: `checkbox`, `radio`, `selectonly`, `selectaction`,
`mappedfield`, `systemSelect`, `selectRelationship`, `ipaddress`.

### INCORRECT — relying on fillInputForAnEntity:
```json
// In data.json — will be SILENTLY SKIPPED
"is_public": true
```

### CORRECT — explicit click in test method:
```java
actions.click(SolutionLocators.SolutionForm.IS_PUBLIC_CHECKBOX);
```

## Rule 6: NEVER Hardcode Locators in Base Files

### INCORRECT — inline locator in test method:
```java
actions.click(new Locator(By.xpath("//button[@id='save']"), "Save"));
```

### CORRECT — defined in Locators.java, referenced by constant:
```java
// In ChangeLocators.java:
Locator SAVE_BUTTON = new Locator(By.xpath("//button[@id='save']"), "Save");

// In test method:
actions.click(ChangeLocators.ChangeForm.SAVE_BUTTON);
```

## Common XPath Patterns for SDP UI

| Element | XPath |
|---------|-------|
| Module title (h1) | `//div[@id='details-middle-container']/descendant::h1` |
| Data attribute row | `//*[@data-row-id='{id}']` |
| Tab by name | `//*[@data-tabname='{tab}']` |
| RHS panel field | `//div[contains(@class,'rhs-field')]//span[text()='{field}']` |
| Alert message | `//div[contains(@class,'alert')]` |
| Confirm dialog | `//div[@class='modal-content']` |
