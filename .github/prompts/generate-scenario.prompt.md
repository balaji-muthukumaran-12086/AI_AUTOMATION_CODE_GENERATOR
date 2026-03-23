---
description: "Generate a single @AutomaterScenario test method following all framework conventions"
agent: "test-generator"
---

Generate a test scenario for `{{input}}` using this EXACT structure:

## 1. Annotation — ALL fields required (NEVER omit runType):

```java
@AutomaterScenario(
    id          = "{SCENARIO_ID}",                          // from CSV or next sequential ID
    group       = {Entity}AnnotationConstants.Group.{GROUP}, // MUST match existing preProcess()
    priority    = Priority.{HIGH|MEDIUM|LOW},
    dataIds     = {{Entity}AnnotationConstants.Data.{KEY}},  // {} if group needs no data
    tags        = {GlobalConstants.Tags.BOTH_SDPMSP},
    description = "{plain English description}",
    owner       = OwnerConstants.{OWNER},
    runType     = ScenarioRunType.USER_BASED,               // NEVER omit — default is PORTAL_BASED
    switchOn    = SwitchToUserSession.AFTER_PRE_PROCESS     // omit only if default is correct
)
```

## 2. Method body — EXACT pattern:

```java
public void {descriptiveMethodName}() throws Exception {
    report.startMethodFlowInStepsToReproduce(AutomaterUtil.getPascalValueFromCamelCase(getMethodName()));
    try {
        // Step 1: Load data (ONLY via DataConstants — NEVER raw strings)
        JSONObject inputData = getTestCaseData({Entity}DataConstants.{InnerClass}.{KEY});

        // Step 2: Navigate + interact (ONLY via ActionsUtil — NEVER inline actions.click)
        {Entity}ActionsUtil.{utilMethod}();

        // Step 3: Validate with POSITIVE ANCHOR before any negative check
        if (actions.isElementPresent({EXPECTED_ELEMENT})) {
            addSuccessReport("{ID}: {what was verified}");
        } else {
            addFailureReport("{what failed}", "{detail}");
        }
    } catch (Exception exception) {
        addFailureReport("Internal error: " + getMethodName(), exception.getMessage());
    } finally {
        report.endMethodFlowInStepsToReproduce();
    }
}
```

## 3. Rules enforced by this template:

- D4: `runType` ALWAYS explicit
- D5: Data loaded via `DataConstants` constant, never raw string
- D8: All UI actions via ActionsUtil methods
- D12: Zero API calls in test body (API = preProcess only)
- D19: Report wrapping with start/end flow
- D23: Positive anchor before negative assertions
