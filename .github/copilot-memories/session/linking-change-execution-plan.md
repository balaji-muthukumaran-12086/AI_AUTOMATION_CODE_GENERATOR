# Linking Change Test Generation — Execution Plan

## Project: SDPLIVE_LINKING_CHANGE_AI_GENERATED
## CSV: Linking_Changes_UseCase_API_Mappings.csv
## Date: March 11, 2026

---

## CSV Analysis Summary
- **Total rows**: 361
- **UI To-be-automated = Yes**: 212 rows
- **Module**: Changes (all rows)

## Completed Batches

### BATCH 0: Infrastructure — DONE
- ChangeLocators.java: LinkingChange interface (~95 locators)
- ChangeActionsUtil.java: 11 linking utility methods
- ChangeAPIUtil.java: 3 API methods
- ChangeAnnotationConstants.java: 1 group + 3 data constants
- ChangeDataConstants.java: 3 TestCaseData entries (manual)
- Change.java: `createMultipleChangeForLinking` preProcess group
- change_data.json: 3 entries (link_parent, link_child, api_valid_input)

### BATCH 1: Associations Page (7 methods, 15 cases) — DONE in DetailsView.java
### BATCH 2: Parent Change Popup (5 methods, 17 cases) — DONE in DetailsView.java
### BATCH 3: Child Changes Popup (3 methods, 11 cases) — DONE in DetailsView.java
### BATCH 4: Detach Operations (4 methods, 8 cases) — DONE in DetailsView.java
### BATCH 5: RHS Panel (3 methods, 10 cases) — DONE in DetailsView.java
### BATCH 6: List View (4 methods, 13 cases) — DONE in ListView.java
### BATCH 7: Detail Page Badges (2 methods, 5 cases) — DONE in DetailsView.java
### BATCH 8: Linking Constraints (3 methods, 11 cases) — DONE in DetailsView.java
### BATCH 9: Closure Rules (1 method, 4 cases) — DONE in DetailsView.java
### BATCH 10: History (2 methods, 10 cases) — DONE in DetailsView.java

## Summary
- **Total methods**: 34 (30 in DetailsView.java + 4 in ListView.java)
- **Total CSV IDs covered**: ~95 unique use-case IDs (including sub-IDs like UI_010a, UI_010b, etc.)
- **Compilation**: Zero new errors (all errors are pre-existing cross-module dependencies)
- **tests_to_run.json**: 34 entries written
- **Import fix**: Changed `import base.SwitchToUserSession` → `import base.common.SwitchToUserSession`

## Remaining Batches (not yet implemented)
- BATCH 11: Trash (TRASH_* — 13 cases)
- BATCH 12: Scoping/RBAC (RBAC_* — 8 cases)
- BATCH 13: Remaining (MSP, Lookup, Edge, Regression, Sandbox — ~80+ cases)

### BATCH 1: Associations Page (15 cases → ~5 methods)
**CSV IDs**: SDPOD_LNKCHG_UI_001 through UI_010e
**Target**: DetailsView.java
**Grouped methods**:
1. `verifyAssociationsPageLayout` — UI_001,UI_002,UI_003,UI_004,UI_006,UI_010d
2. `verifyAssociationsPagePagination` — UI_005,UI_007,UI_008
3. `verifyAssociationsPageAfterLinkingParent` — UI_010a,UI_010b,UI_010c
4. `verifyExternalLinkOpensDetailPage` — UI_010
5. `verifyAssociationsPageBreadcrumbAndTooltip` — UI_009,UI_010e

### BATCH 2: Parent Change Popup (17 cases → ~6 methods)
**CSV IDs**: SDPOD_LNKCHG_UI_011 through UI_023d
**Target**: DetailsView.java
**Grouped methods**:
1. `verifyParentChangePopupLayout` — UI_011,UI_012,UI_013
2. `verifyAttachParentChangeAndConfirm` — UI_014,UI_015,UI_016
3. `verifyParentPopupSearchAndCancel` — UI_017,UI_018,UI_019,UI_020,UI_021
4. `verifyExistingParentNotRelisted` — UI_022,UI_023b,UI_023c,UI_023d
5. `verifyClosedChangeCannotAttach` — UI_023
6. `verifyEmptySelectionValidation` — UI_023a

### BATCH 3: Child Changes Popup (11 cases → ~4 methods)
**CSV IDs**: SDPOD_LNKCHG_UI_024 through UI_031c
**Target**: DetailsView.java
**Grouped methods**:
1. `verifyChildChangesPopupLayout` — UI_024,UI_025
2. `verifyAttachMultipleChildChanges` — UI_026,UI_027,UI_028,UI_029
3. `verifyChildPopupFiltersAndValidation` — UI_030,UI_031,UI_031a,UI_031b
4. `verifyChildChangeLinkingLimit` — UI_031c

### BATCH 4: Detach Tests (8 cases → ~4 methods)
**CSV IDs**: SDPOD_LNKCHG_UI_032 through UI_036c
**Target**: DetailsView.java
**Grouped methods**:
1. `verifyDetachParentChange` — UI_032,UI_036b
2. `verifyDetachChildChanges` — UI_033,UI_034
3. `verifyDetachConfirmationCancel` — UI_035
4. `verifyDetachValidationAndClosedChange` — UI_036,UI_036a,UI_036c

### BATCH 5: RHS Panel (10 cases → ~3 methods)
**CSV IDs**: SDPOD_LNKCHG_UI_037 through UI_042d
**Target**: DetailsView.java
**Grouped methods**:
1. `verifyRHSLinkedChangesCount` — UI_037,UI_038,UI_039,UI_040,UI_042a
2. `verifyRHSTrashedChangeExcluded` — UI_041
3. `verifyRHSExistingAssociationsIntact` — UI_042,UI_042b,UI_042c,UI_042d

### BATCH 6: List View (13 cases → ~4 methods)
**CSV IDs**: SDPOD_LNKCHG_UI_043 through UI_050e
**Target**: ListView.java
**Grouped methods**:
1. `verifyAssociatedChangesColumnInListView` — UI_043,UI_048,UI_050c,UI_050d
2. `verifyChildChangesTooltipAndOverlay` — UI_044,UI_045,UI_049,UI_050,UI_050e
3. `verifyParentChangePopoverInListView` — UI_046,UI_050a,UI_050b
4. `verifyAssociatedChangesNotInExport` — UI_047

### BATCH 7: Detail Page Badges (5 cases → ~2 methods)
**CSV IDs**: SDPOD_LNKCHG_UI_051 through UI_055
**Target**: DetailsView.java
**Grouped methods**:
1. `verifyParentChildBadgeInDetailPage` — UI_051,UI_052,UI_053,UI_054
2. `verifyBadgeStyling` — UI_055

### BATCH 8: History Tests (16 BL cases → ~4 methods)
**CSV IDs**: SDPOD_LNKCHG_BL_004 through BL_007
**Target**: DetailsView.java

### BATCH 9: Closure Rules (4 cases → ~2 methods)
**CSV IDs**: SDPOD_LNKCHG_BL_001 through BL_001c
**Target**: DetailsView.java

### BATCH 10: Linking Constraints (11 cases → ~4 methods)
**CSV IDs**: SDPOD_LNKCHG_CONST_001 through CONST_011b
**Target**: DetailsView.java

### BATCH 11: Trash/Restore (14 cases → ~5 methods)
**CSV IDs**: SDPOD_LNKCHG_TRASH_001 through TRASH_009f
**Target**: DetailsView.java

### BATCH 12: RBAC/Scoping (8 cases → ~3 methods)
**CSV IDs**: SDPOD_LNKCHG_RBAC_001 through RBAC_007d
**Target**: DetailsView.java

### BATCH 13: Regression/Edge/Other
**Remaining tests sorted by priority**

---

## Progress Tracking

| Batch | Status | Methods | Tests Covered | Notes |
|-------|--------|---------|---------------|-------|
| 0 Infrastructure | 🔄 IN PROGRESS | — | — | Locators, utils, data, preProcess |
| 1 Associations Page | ⬜ PENDING | ~5 | 15 | |
| 2 Parent Popup | ⬜ PENDING | ~6 | 17 | |
| 3 Child Popup | ⬜ PENDING | ~4 | 11 | |
| 4 Detach | ⬜ PENDING | ~4 | 8 | |
| 5 RHS Panel | ⬜ PENDING | ~3 | 10 | |
| 6 List View | ⬜ PENDING | ~4 | 13 | |
| 7 Detail Badges | ⬜ PENDING | ~2 | 5 | |
| 8 History | ⬜ PENDING | ~4 | 16 | |
| 9 Closure Rules | ⬜ PENDING | ~2 | 4 | |
| 10 Constraints | ⬜ PENDING | ~4 | 11 | |
| 11 Trash/Restore | ⬜ PENDING | ~5 | 14 | |
| 12 RBAC | ⬜ PENDING | ~3 | 8 | |
| 13 Remaining | ⬜ PENDING | TBD | ~80 | Lookup, MSP, Edge, etc. |

## Estimated Methods: ~46 core methods covering ~132 primary UI test cases
## Remaining ~80 (Lookup/MSP/Regression/etc.) will follow after core is stable
