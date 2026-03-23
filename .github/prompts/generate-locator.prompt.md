---
description: "Generate a new XPath locator constant in *Locators.java"
agent: "test-generator"
---

Generate a locator for `{{input}}` using this EXACT pattern:

## Static locator (no parameters):

```java
Locator BUTTON_NAME = new Locator(
    By.xpath("//button[normalize-space(text())='Save']"),
    "Description of Save button"
);
```

## Dynamic locator (takes a parameter):

```java
Function<String, Locator> ROW_BY_ID = (entityId) -> new Locator(
    By.xpath("//*[@data-row-id='" + entityId + "']"),
    "Row for entity " + entityId
);
```

## Two-parameter locator:

```java
BiFunction<String, String, Locator> CELL_VALUE = (row, col) -> new Locator(
    By.xpath("//tr[" + row + "]/td[" + col + "]"),
    "Cell at row " + row + ", col " + col
);
```

## XPath rules:

| Pattern | Use |
|---|---|
| `normalize-space(text())='X'` | Exact button/link text match |
| `contains(@class,'x')` | CSS class match |
| `@data-row-id` / `@data-tabname` | Data attribute match |
| `descendant::` | Search inside a container |

## FORBIDDEN:

```java
// Contains for button text — matches "Add" AND "Add And Approve"
By.xpath("//button[contains(text(),'Add')]")
// → CORRECT: By.xpath("//button[normalize-space(text())='Add']")

// Hardcoded By.xpath in Base files — must be in Locators.java
actions.click(new Locator(By.xpath("//div"), "inline"))
// → CORRECT: Use ChangeLocators.Section.CONSTANT_NAME

// Select2 inside parent — it's at body level
By.xpath("//div[@class='dialog']//div[@class='select2-result-label']")
// → CORRECT: By.xpath("//div[contains(@class,'select2-result-label')]")
```
