# Requirement Document — [Feature/Task Title]

> **Template version**: 1.0  
> **Created**: [YYYY-MM-DD]  
> **Author**: [Name]  
> **Status**: Draft | In Review | Approved | In Progress | Done

---

## 1. Overview

**Objective**: [One paragraph describing what this feature/task accomplishes]

**Trigger**: [What initiated this work — user request, bug report, CSV use-case doc, etc.]

---

## 2. Scope

### In Scope
- [ ] [List every specific deliverable]
- [ ] [Be explicit — "generate 5 test scenarios for Change DetailsView"]
- [ ] [Include file names if known]

### Out of Scope
- [ ] [What this task does NOT cover]
- [ ] [Explicitly exclude to prevent scope creep]

---

## 3. Prerequisites

| Prerequisite | Status | Notes |
|-------------|--------|-------|
| Project cloned and configured | ✅/❌ | `$PROJECT_NAME` in `.env` |
| Framework compiled | ✅/❌ | `setup_framework_bin.sh` run |
| Use-case CSV available | ✅/❌ | Path: `$PROJECT_NAME/Testcase/...` |
| Existing entity files read | ✅/❌ | List which files were reviewed |

---

## 4. Requirements

### 4.1 Functional Requirements

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|-------------------|
| FR-01 | [What needs to work] | HIGH/MED/LOW | [How to verify it works] |
| FR-02 | | | |

### 4.2 Technical Requirements

| ID | Requirement | Notes |
|----|------------|-------|
| TR-01 | [Framework constraint, e.g. "must use ActionsUtil pattern"] | See `framework_rules.md §FR_ACTIONSUTIL` |
| TR-02 | | |

---

## 5. Affected Files

| File | Action | Description |
|------|--------|-------------|
| `modules/<module>/<entity>/Entity.java` | MODIFY | Add new @AutomaterScenario method |
| `modules/<module>/<entity>/EntityBase.java` | MODIFY | Add test implementation |
| `resources/entity/data/<module>/<entity>_data.json` | MODIFY | Add test data entries |
| `modules/<module>/<entity>/common/EntityLocators.java` | MODIFY | Add new locators |

> **IMPORTANT**: List ALL files upfront. This prevents mid-session discovery of forgotten files
> that forces re-reading context and wastes tokens.

---

## 6. Data Requirements

| Data Key (snake_case) | Purpose | Placeholders Used |
|----------------------|---------|-------------------|
| `create_entity_api` | preProcess entity creation | `$(unique_string)` |
| `verify_entity_dv` | UI verification data | `$(custom_entity_name)` |

---

## 7. Estimation

| Metric | Value |
|--------|-------|
| Files to modify | [N] |
| New scenarios | [N] |
| New data entries | [N] |
| New locators | [N] |
| Estimated phases | [N] |
| Estimated sessions | [N] |

---

## 8. Sign-Off

- [ ] Requirements reviewed by author
- [ ] All affected files identified
- [ ] Data requirements finalized
- [ ] Ready for implementation plan creation
