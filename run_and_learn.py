"""
run_and_learn.py
----------------
Sequential test runner with per-test learning extraction.

Runs each test from tests_to_run.json one at a time, monitors stdout/stderr
live, extracts learnings via LearningAgent after each test, and injects
product-knowledge observations from source-code analysis.

Usage:
    python run_and_learn.py 2>&1 | tee /tmp/run_and_learn.log
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from config.project_config import (
    BASE_DIR, PROJECT_NAME, DEPS_DIR,
    SDP_URL, SDP_PORTAL, SDP_ADMIN_EMAIL, SDP_ADMIN_PASS,
    TESTS_TO_RUN_PATH,
    TEST_EXECUTION_TIMEOUT,
)
from agents.runner_agent import RunnerAgent, RunResult
from agents.learning_agent import LearningAgent
from agents.state import AgentState

# ── Static product-knowledge annotations per method ──────────────────────
# Derived from reading Java source files before running.
# These are injected alongside LLM-extracted learnings.

PRODUCT_ANNOTATIONS = {
    "createWorkflowOfIncidentRequest": {
        "product_area": "Admin > Automation > Workflows > Incident Request",
        "module": "admin.automation.workflows",
        "what_it_tests": (
            "End-to-end workflow creation via the Workflows canvas UI for Incident Requests. "
            "Creates a workflow with multiple node types: Notification, Field Update (impact/urgency/priority), "
            "Task, Wait-For, Fork, Join, and Approval. Then links the workflow to an Incident Template via API, "
            "creates an IR, navigates to the IR detail view, triggers each node by updating fields, "
            "and verifies: notification fired, field updates applied, tasks created, status → Closed, "
            "workflow marked complete. Finally, deletes and restores the workflow."
        ),
        "framework_methods_exercised": [
            "AdminActionsUtil.gotoentity('Workflows')          → navigates to Admin > Automation > Workflows listview",
            "WorkflowsActionsUtil.*                             → drags nodes onto canvas, connects them, configures each",
            "actions.navigate.toModule(ModuleConstants.REQUESTS) → switches to Requests module",
            "actions.navigate.toSubTabInDetailsPage()           → switches between tabs in IR details",
            "actions.formBuilder.fillSelectField()              → fills select dropdown (impact field)",
            "verifyWaitForNode()                                → polls until 'Wait For' node activates",
            "verifyNotification(title)                          → checks notification panel for expected subject",
            "verifyFieldUpdate(field, value)                    → reads field from detail view, compares to expected",
            "verifyTask(title, bool)                            → checks task created/completed in task panel",
            "verifyStatus('Closed')                             → reads status field on IR details",
            "verifyWorkflowComplete()                           → verifies workflow progress indicator shows 100%",
            "deleteAndRestoreWorkflow(name)                     → deletes then restores from recycle bin",
            "restAPI.getEntityIdUsingSearchCriteria()           → REST: searches workflow by name to get its ID",
            "IncidentTemplateAPIUtil.createIncidentTemplate()   → REST: creates incident template linked to workflow",
            "RequestAPIUtil.createIR()                          → REST: creates incident request using the template",
        ],
        "locators_involved": [
            "WorkflowsLocators.* (workflow canvas, node drag handles, connection arrows)",
            "RequestLocators.Listview.PAGE_COUNT (pagination info)",
            "SDPCommonLocators.ButtonLocators.BTN_BYNAME_SPAN.apply('New Incident')",
        ],
        "data_keys": [
            "WorkflowsDataConstants.WorkflowsData.CREATE_INCIDENT_REQUEST_WORKFLOW",
            "IncidentTemplateDataConstants.IncidentTemplateData.REQUEST_TEMPLATE",
            "RequestDataConstants.RequestData.CREATE_REQUEST_FOR_WORKFLOW",
            "TimerDataConstants.TimerData.LIST_INFO_CRITERIA_NAME_SEARCH",
        ],
        "known_complexity": "HIGH — multi-step, canvas drag-drop, polling, async node activation, 10-20 min typical runtime",
        "preprocess_group": "No preprocess",
        "note": "Thread.sleep(10000) used before priority node verification — timing-sensitive scenario",
    },

    "checkAllAssetTriggerForAccesspoint": {
        "product_area": "Admin > Automation > Triggers > Asset Triggers",
        "module": "admin.automation.triggers",
        "what_it_tests": (
            "Verifies that an Asset Trigger (with Notification action) fires correctly when a new "
            "Access Point asset is created. preProcess (group='createAssetTrigger') creates:\n"
            "  1. A Notification rule via API (TriggerAPIUtil.createNotificationViaAPI)\n"
            "  2. A Trigger via REST API ('wftriggers') that fires on asset creation, criteria: created_by=technician\n"
            "Then the test:\n"
            "  1. Creates the Access Point product type via API if not exists (AssetAPIUtil.checkAndCreateProduct)\n"
            "  2. Navigates to Assets listview\n"
            "  3. Selects 'Access Point' product type from left accordion\n"
            "  4. Clicks 'New Asset', fills form via fillInputForAnEntity and submits\n"
            "  5. Calls verifyNotification() to confirm trigger fired"
        ),
        "framework_methods_exercised": [
            "TriggerAPIUtil.getEntityIdforCriteriaValue()        → REST lookup of 'All Assets' product type ID",
            "TriggerAPIUtil.createNotificationViaAPI()           → REST POST to create notification rule",
            "restAPI.createAndGetAPIResponse('wftriggers', ...)  → REST POST to create trigger with criteria",
            "AssetAPIUtil.checkAndCreateProduct()                → REST: creates product type if not exists",
            "actions.navigate.toModule(ModuleConstants.ASSETS)   → navigates to Assets module",
            "AssetActionsUtil.searchAndSelectProductTypeInAccordian() → left sidebar product-type filter",
            "SDPCloudActions.isMSP()                             → checks if portal is MSP mode",
            "actions.click(AssetLocators.Listview.LISTVIEW_BUTTONS.apply('New Asset'))",
            "actions.formBuilder.fillInputForAnEntity()          → fills name, serial, type from asset_data.json",
            "formBuilder.submit()                                 → submits create form",
            "verifyNotification()                                 → checks notification bell / trigger audit",
        ],
        "locators_involved": [
            "AssetLocators.Listview.LISTVIEW_BUTTONS.apply(AssetConstants.ListviewGlobalActions.NEW_ASSET)",
            "AdditionalFieldsLocators (used in MSP-mode customer selection)",
            "TriggersLocators.Listview (for checking trigger status)",
        ],
        "data_keys": [
            "AssetDataConstants.AssetData.CREATE_ACCESS_POINT_ASSET",
            "TriggersDataConstants.TriggersData.NOTIFICATION_DATA_FOR_TRIGGER_SUBENTITY",
            "TriggersDataConstants.TriggersData.CUSTOM_DATA_FOR_TRIGGER_SUBENTITY_WITH_NOTIFICATION_ACTIONS_ONLY",
        ],
        "preprocess_group": "createAssetTrigger",
        "note": "LocalStorage keys: 'technician', 'triggerName', 'triggerId', 'entityId', 'moduleName', 'criteriaCondition', 'criteriaField', 'criteriaValue'",
        "known_complexity": "MEDIUM — preprocess API calls + UI create + trigger verification",
    },

    "filterUdfByDataTypeNumeric": {
        "product_area": "Admin > Customization > Additional Fields (UDF) > Project Module",
        "module": "admin.customization.additionalfields",
        "what_it_tests": (
            "Verifies the 'Filter by Data Type: Numeric' functionality on the Additional Fields listview "
            "for the Project module. Steps:\n"
            "  1. Navigates to Admin > Customization > Additional Fields\n"
            "  2. Selects 'Project' module from left panel (AdditionalFieldsActionsUtil.selectModule)\n"
            "  3. Clicks the 'Data Type' filter dropdown\n"
            "  4. Selects 'Numeric' from dropdown\n"
            "  5. Reads table settings to get page count (records shown)\n"
            "  6. Counts all UDF rows where the type badge = Numeric (using XPATH count)\n"
            "  7. Asserts count == page count (filter shows exactly the right results)\n"
        ),
        "framework_methods_exercised": [
            "AdminActionsUtil.gotoentity(AdminConstants.SubModule.ADDITIONALFIELDS) → navigate to UDF page",
            "AdditionalFieldsActionsUtil.selectModule(moduleName)  → click 'Project' in left panel",
            "actions.click(AdditionalFieldsLocators.DATA_TYPE_FILTER) → open filter dropdown",
            "actions.click(AdditionalFieldsLocators.DATA_TYPE_FILTER_DROPDOWN.apply('Numeric')) → select type",
            "getTestCaseData(AdditionalFieldsDataConstants.AdditionalFieldsData.FIELDFILTERS) → load filter config",
            "AutomaterUtil.getValueAsArrayFromInputUsingAPIPath()   → extract numeric subtypes list from JSON",
            "actions.listView.setTableSettings()                    → set page size to max for full count",
            "actions.getText(RequestLocators.Listview.PAGE_COUNT)   → read 'X of Y' pagination text",
            "AdditionalFieldsActionsUtil.getCount(locator)          → count matching rows by XPath",
            "addSuccessReport / addFailureReport                    → record result",
        ],
        "locators_involved": [
            "AdditionalFieldsLocators.DATA_TYPE_FILTER",
            "AdditionalFieldsLocators.DATA_TYPE_FILTER_DROPDOWN.apply(filterType)",
            "AdditionalFieldsLocators.UDF_WITH_SPECIFIC_TYPE_COUNT.apply(type)",
            "RequestLocators.Listview.PAGE_COUNT  (shared locator reused in UDF page)",
        ],
        "data_keys": [
            "AdditionalFieldsDataConstants.AdditionalFieldsData.FIELDFILTERS",
            "RequestDataConstants.RequestData.TABLE_SETTINGS",
        ],
        "preprocess_group": "UDF_project_group1",
        "note": (
            "UDF_project_group1 preProcess likely creates Numeric UDF(s) via API beforehand. "
            "Uses report.startMethodFlowInStepsToReproduce / endMethodFlowInStepsToReproduce lifecycle. "
            "PAGE_COUNT locator is shared from Requests module — demonstrating locator reuse across modules."
        ),
        "known_complexity": "LOW — mostly read + count verification, no drag-drop or async waiting",
    },
}


def print_separator(label: str):
    width = 72
    print("\n" + "=" * width)
    print(f"  {label}")
    print("=" * width)


def run_and_learn():
    # ── Load tests ─────────────────────────────────────────────────────
    tests_path = Path(TESTS_TO_RUN_PATH)
    if not tests_path.exists():
        print(f"[run_and_learn] ❌ tests_to_run.json not found at {tests_path}")
        sys.exit(1)

    data = json.loads(tests_path.read_text(encoding="utf-8"))
    tests = [{k: v for k, v in t.items() if not k.startswith("_")} for t in data.get("tests", [])]
    print(f"[run_and_learn] 📋 Loaded {len(tests)} test(s) from tests_to_run.json")

    # ── Init runner ────────────────────────────────────────────────────
    runner = RunnerAgent()
    learner = LearningAgent()

    all_results: list[RunResult] = []
    session_start = datetime.now()

    for idx, test_cfg in enumerate(tests, start=1):
        entity_class = test_cfg.get("entity_class", "?")
        method_name  = test_cfg.get("method_name", "?")

        print_separator(f"TEST {idx}/{len(tests)}: {entity_class}.{method_name}")

        # ── Print pre-run product knowledge ───────────────────────────
        ann = PRODUCT_ANNOTATIONS.get(method_name, {})
        if ann:
            print(f"\n📘 PRODUCT KNOWLEDGE (pre-run, from source analysis):")
            print(f"   Product Area : {ann.get('product_area', '-')}")
            print(f"   Complexity   : {ann.get('known_complexity', '-')}")
            print(f"   What it tests:")
            for line in ann.get('what_it_tests', '').strip().split('\n'):
                print(f"     {line}")
            print(f"   Preprocess   : group='{ann.get('preprocess_group', '-')}'")
            if ann.get('note'):
                print(f"   Note         : {ann['note']}")

        # ── Resolve config (replace placeholders) ─────────────────────
        cfg = {
            "entity_class":  entity_class,
            "method_name":   method_name,
            "url":           test_cfg.get("url",           SDP_URL),
            "admin_mail_id": test_cfg.get("admin_mail_id", SDP_ADMIN_EMAIL),
            "email_id":      test_cfg.get("email_id",      SDP_ADMIN_EMAIL),
            "portal_name":   test_cfg.get("portal_name",   SDP_PORTAL),
            "skip_compile":  test_cfg.get("skip_compile",  True),
        }
        for k, v in cfg.items():
            if isinstance(v, str):
                cfg[k] = v.replace("$(SDP_URL)", SDP_URL)\
                           .replace("$(SDP_PORTAL)", SDP_PORTAL)\
                           .replace("$(SDP_ADMIN_EMAIL)", SDP_ADMIN_EMAIL)\
                           .replace("$(SDP_ADMIN_PASS)", SDP_ADMIN_PASS)

        # ── Execute test ───────────────────────────────────────────────
        print(f"\n▶  Starting {entity_class}.{method_name} at {datetime.now().strftime('%H:%M:%S')}")
        print(f"   Timeout: {TEST_EXECUTION_TIMEOUT}s ({TEST_EXECUTION_TIMEOUT // 60}m)\n")
        t_start = time.time()

        result: RunResult = runner.run_test(
            entity_class=cfg["entity_class"],
            method_name=cfg["method_name"],
            url=cfg["url"],
            admin_mail_id=cfg["admin_mail_id"],
            email_id=cfg["email_id"],
            portal_name=cfg["portal_name"],
            skip_compile=cfg["skip_compile"],
        )

        elapsed = time.time() - t_start
        status_icon = "✅" if result.success else "❌"
        print(f"\n{status_icon} RESULT: {'PASSED' if result.success else 'FAILED'} "
              f"| {entity_class}.{method_name} | {elapsed:.1f}s")
        if result.report_path:
            print(f"   Report: {result.report_path}")
        if not result.success and result.error:
            print(f"   Error : {result.error[:500]}")
        if result.stdout:
            # Show last 60 lines of stdout for context
            lines = result.stdout.strip().splitlines()
            tail = lines[-60:] if len(lines) > 60 else lines
            print(f"\n   --- stdout tail ({len(tail)} lines) ---")
            for ln in tail:
                print(f"   {ln}")

        all_results.append(result)

        # ── Post-run annotations ───────────────────────────────────────
        if ann:
            print(f"\n📗 FRAMEWORK METHODS EXERCISED (from source analysis):")
            for m in ann.get("framework_methods_exercised", []):
                print(f"   • {m}")
            print(f"\n   KEY LOCATORS: {', '.join(ann.get('locators_involved', ['-']))}")
            print(f"   KEY DATA KEYS: {', '.join(ann.get('data_keys', ['-']))}")

        # ── Extract learnings via LearningAgent ────────────────────────
        print(f"\n🧠 Running LearningAgent on {entity_class}.{method_name}...")
        try:
            result_dict = result.to_dict() if hasattr(result, 'to_dict') else vars(result)
            # Inject product annotations so the LLM gets full scenario context
            result_dict["product_context"] = ann  # may be {} if no annotation exists
            # Build minimal state — TypedDict is not enforced at runtime
            state: AgentState = {
                "batch_run_results": [result_dict],
                "batch_run_configs": [cfg],
                "learnings": [],
                "messages": [],
                "errors": [],
                "learning_iteration": 0,
            }  # type: ignore[typeddict-item]
            state = learner.run(state)
            stored = state.get("learnings", [])
            print(f"   LearningAgent complete — {len(stored)} learning(s) extracted.")
        except Exception as e:
            print(f"   ⚠️  LearningAgent error: {e}")

        # ── Persist product annotations to knowledge base ──────────────
        if ann:
            _persist_product_knowledge(entity_class, method_name, ann, result)

        print(f"\n{'─' * 72}")

    # ── Final summary ──────────────────────────────────────────────────
    total_elapsed = (datetime.now() - session_start).total_seconds()
    passed = sum(1 for r in all_results if r.success)
    failed = len(all_results) - passed

    print_separator("SESSION SUMMARY")
    print(f"  Total tests : {len(all_results)}")
    print(f"  Passed      : {passed} ✅")
    print(f"  Failed      : {failed} ❌")
    print(f"  Total time  : {total_elapsed:.0f}s ({total_elapsed / 60:.1f}m)")
    print(f"  Learnings   : {Path(BASE_DIR) / 'logs' / 'learnings.jsonl'}")
    print(f"  Rules file  : {Path(BASE_DIR) / 'config' / 'framework_rules.md'}")
    print(f"  Knowledge   : {Path(BASE_DIR) / 'config' / 'framework_knowledge.md'}")

    return passed == len(all_results)


def _persist_product_knowledge(entity_class: str, method_name: str, ann: dict, result: RunResult):
    """
    Append a product knowledge block to framework_knowledge.md for this scenario.
    This captures what the scenario tests and what framework methods it exercises.
    """
    import threading
    from pathlib import Path as _Path

    knowledge_file = _Path(BASE_DIR) / "config" / "framework_knowledge.md"
    if not knowledge_file.exists():
        return

    existing = knowledge_file.read_text(encoding="utf-8")
    marker = f"### {entity_class}.{method_name}"
    if marker in existing:
        print(f"   ℹ️  Product knowledge for {entity_class}.{method_name} already in framework_knowledge.md — skipped.")
        return

    status_str = "PASSED ✅" if result.success else "FAILED ❌"
    block = f"""
{marker}
**Product Area**: {ann.get('product_area', '-')}
**Status (last run)**: {status_str}
**Complexity**: {ann.get('known_complexity', '-')}
**Preprocess Group**: `{ann.get('preprocess_group', '-')}`

**What it tests**:
{ann.get('what_it_tests', '').strip()}

**Key framework methods**:
{chr(10).join('- `' + m + '`' for m in ann.get('framework_methods_exercised', []))}

**Key locators**: {', '.join('`' + l + '`' for l in ann.get('locators_involved', []))}
**Key data constants**: {', '.join('`' + d + '`' for d in ann.get('data_keys', []))}
**Notes**: {ann.get('note', '-')}

---
"""

    with open(knowledge_file, "a", encoding="utf-8") as f:
        f.write(block)
    print(f"   ✍️  Product knowledge for {entity_class}.{method_name} written to framework_knowledge.md")


if __name__ == "__main__":
    success = run_and_learn()
    sys.exit(0 if success else 1)
