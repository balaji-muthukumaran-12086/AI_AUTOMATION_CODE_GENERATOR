# Feature Document: [Feature Name]

> **Purpose**: This document gives the AI agent product knowledge about a feature's behavior,
> UI flows, API endpoints, business rules, and edge cases. Place it alongside your use-case CSV
> in `{PROJECT}/Testcase/` so the test-generator loads it as context before generating code.

---

## Module & Entity

| Field | Value |
|-------|-------|
| **Module** | Changes / Requests / Solutions / Problems / Releases / Assets / Admin / etc. |
| **Entity / Sub-Module** | e.g., Linking Changes, Approval Workflow, Notes, Worklogs |
| **Branch** | (optional) Link to the feature branch |
| **Change/Story ID** | (optional) Internal tracking ID |

---

## Requirement Summary

<!-- 2-5 sentences describing what the feature does and why it exists -->

---

## UI Flow

<!-- Step-by-step description of how a user interacts with this feature in the UI.
     Include: which page/tab, what buttons/menus, what forms, what confirmations.
     This directly informs the generated test method's click/navigate sequence. -->

### Primary Flow
1. Navigate to [Module] → [Entity] detail view
2. Click [Tab/Button name]
3. ...
4. Verify [expected outcome]

### Alternative Flows (if any)
- Flow for [variation]: ...

---

## API Endpoints

<!-- List the REST API endpoints used by this feature.
     This directly informs preProcess data creation and APIUtil methods. -->

| Operation | Method | Path | Input Wrapper | Notes |
|-----------|--------|------|---------------|-------|
| Create | POST | `api/v3/<module>` | `{"<entity>": {...}}` | |
| Read | GET | `api/v3/<module>/<id>` | — | |
| Update | PUT | `api/v3/<module>/<id>` | `{"<entity>": {...}}` | |
| Delete | DELETE | `api/v3/<module>/<id>` | — | |
| Sub-resource | POST | `api/v3/<module>/<id>/<sub>` | `{"<sub>": {...}}` | |

---

## Business Rules & Constraints

<!-- List permission requirements, validation rules, field dependencies, etc.
     This informs RBAC group setup, edge-case scenarios, and error validations. -->

- Rule 1: ...
- Rule 2: ...
- Permission: Requires [role] to perform [action]

---

## UI Elements & Locators (if known)

<!-- Optional: DOM details that help generate accurate XPath locators.
     Tab names, button IDs, container classes, table structures, etc. -->

| Element | Selector/Attribute | Notes |
|---------|-------------------|-------|
| Tab | `data-tabname="associations"` | Left panel |
| Button | `name="save-button"` | Form submit |
| Popup | `.slide-down-popup` | Search popup |

---

## Edge Cases & Known Gotchas

<!-- Anything non-obvious that a test writer should know.
     Failed API patterns, misleading UI states, timing issues, etc. -->

- Edge case 1: ...
- Edge case 2: ...

---

## Related Entities / Dependencies

<!-- Other entities this feature interacts with.
     Helps the generator understand cross-module preProcess needs. -->

- Depends on: [Entity A] must exist before [this feature] can be tested
- Affects: [Entity B] is modified when [action] is performed
