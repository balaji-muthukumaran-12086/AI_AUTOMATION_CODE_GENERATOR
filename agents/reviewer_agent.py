"""
reviewer_agent.py
-----------------
Reviewer Agent: Validates generated Java code against the AutomaterSelenium
framework grammar and coding conventions.

Checks:
  1. @AutomaterScenario has all required fields (id, group, description, dataIds)
  2. Test ID format: SDP_XXX_XXX_XXXNNN
  3. try/catch/finally structure present
  4. addSuccessReport / addFailureReport used correctly
  5. No hardcoded CSS selectors or string values
  6. report.start/end MethodFlowInStepsToReproduce present
  7. No duplicate scenario IDs

If issues found → sends revision requests back to CoderAgent.
"""

import re
import os
from typing import Any
from pathlib import Path

from langchain_core.messages import SystemMessage, HumanMessage

from agents.state import AgentState
from agents.llm_factory import get_llm


# ── Static checks (regex-based) ────────────────────────────────────────────

CHECKS = [
    {
        'name': 'has_automater_scenario',
        'pattern': r'@AutomaterScenario',
        'required': True,
        'message': 'Missing @AutomaterScenario annotation',
    },
    {
        'name': 'has_id',
        'pattern': r'id\s*=\s*"SDPOD_AUTO_',
        'required': True,
        'message': 'Missing or malformed test ID (must follow SDPOD_AUTO_<MODULE>_<AREA>_NNN format)',
    },
    {
        'name': 'has_description',
        'pattern': r'description\s*=\s*"[^"]{5,}"',
        'required': True,
        'message': 'Missing or too-short description',
    },
    {
        'name': 'has_data_ids',
        'pattern': r'dataIds\s*=\s*\{',
        'required': True,
        'message': 'Missing dataIds field',
    },
    {
        'name': 'has_try_catch',
        'pattern': r'try\s*\{',
        'required': True,
        'message': 'Missing try block',
    },
    {
        'name': 'has_catch',
        'pattern': r'catch\s*\(\s*Exception',
        'required': True,
        'message': 'Missing catch(Exception ...) block',
    },
    {
        'name': 'has_finally',
        'pattern': r'finally\s*\{',
        'required': True,
        'message': 'Missing finally block',
    },
    {
        'name': 'has_report_start',
        'pattern': r'report\.startMethodFlowInStepsToReproduce',
        'required': True,
        'message': 'Missing report.startMethodFlowInStepsToReproduce() call',
    },
    {
        'name': 'has_report_end',
        'pattern': r'report\.endMethodFlowInStepsToReproduce',
        'required': True,
        'message': 'Missing report.endMethodFlowInStepsToReproduce() in finally',
    },
    {
        'name': 'has_success_or_failure_report',
        'pattern': r'addSuccessReport|addFailureReport|addReport',
        'required': True,
        'message': 'Missing addSuccessReport/addFailureReport call',
    },
    {
        'name': 'no_hardcoded_locators',
        'pattern': r'By\.(xpath|cssSelector|id)\s*\(\s*"',
        'required': False,   # present = problem
        'message': 'Hardcoded Selenium locators found — use Locators.java constants',
    },
    {
        'name': 'no_system_out',
        'pattern': r'System\.out\.print',
        'required': False,
        'message': 'System.out.println found — use addCaseFlow/report methods instead',
    },
]


REVIEW_SYSTEM_PROMPT = """You are a senior Java test automation engineer reviewing
AutomaterSelenium test code for Zoho ServiceDesk Plus.

FRAMEWORK RULES (verify every one):

1.  ID format: SDPOD_AUTO_<MODULE>_<AREA>_NNN (e.g. SDPOD_AUTO_SOL_CREATE_059). NEVER SDP_.
2.  Two-layer architecture:
      <Entity> extends <Entity>Base extends Entity
      - <Entity>.java: ONLY @Override + @AutomaterScenario + super.method() — zero logic
      - <Entity>Base.java: ALL implementation logic lives here
3.  Wrapper MUST have @Override AND super.methodName() — body must contain ONLY super.method()
4.  First line of EVERY implementation method:
      report.startMethodFlowInStepsToReproduce(AutomaterVariables.SCENARIO_START.apply(getMethodName()));
      NOT AutomaterUtil.getPascalValueFromCamelCase(...) — that is WRONG.
5.  report.endMethodFlowInStepsToReproduce() MUST be in the finally block
6.  BOTH addSuccessReport() AND addFailureReport() must be present (if/else branches)
7.  group value MUST match an existing branch in preProcess() — never invent new group strings
8.  dataIds[] values MUST be string constants from <Entity>AnnotationConstants.Data interface
9.  UI data loaded via: getTestCaseData(DataConstants.EntityData.CONSTANT) — existing constants only
10. preProcess data loaded via: getTestCaseDataUsingCaseId(dataIds[0]) — for API setup
11. LocalStorage.store(key, id) in preProcess → LocalStorage.fetch(key) in implementation
12. NEVER hardcode By.xpath / By.cssSelector / By.id — use Locators.java constants
13. NEVER use System.out.println — use report.addCaseFlow()
14. Datetime fields: actions.formBuilder.fillDateField() separately, NOT inside fillInputForAnEntity()
15. NEVER invent Field, Locator, or Constants names not present in the provided context
16. actions.listView.doAction() does NOT exist — use rowAction(entityID, actionName) instead
17. actions.listView.selectRecord() does NOT exist — use navigate.toDetailsPageUsingRecordId(id) instead
18. getEntityId() only valid after preProcess stores the ID via LocalStorage.store(getName(), id)
19. Navigate methods all return `this` — chaining is valid
20. For Solution: submit button = SolutionLocators.SolutionCreateForm.SOLUTION_ADD (unapproved)
    or SOLUTION_ADD_APPROVE (approved) — NOT actions.formBuilder.submit()
21. ALWAYS use SolutionActionsUtil.pageSetup() for list view setup, and SolutionActionsUtil.searchSolutionUsingId()
    for searching. Never inline this logic in Base methods. Add new methods to ActionsUtil if missing.

Review the provided Java code and identify all issues.

Return a JSON array of issues (empty [] if none):
[{ "severity": "ERROR|WARNING|INFO", "issue": "description", "fix": "suggested fix" }]

ERROR = must fix before merge
WARNING = should fix
INFO = style suggestion
"""


class ReviewerAgent:

    def __init__(self, llm: Any = None, base_dir: str = None):
        self.base = Path(base_dir) if base_dir else Path(__file__).resolve().parents[1]
        self.llm = llm or get_llm(
            temperature=0,
        )

    def _static_check(self, code: str) -> list[dict]:
        """Fast regex-based static checks."""
        issues = []
        for check in CHECKS:
            found = bool(re.search(check['pattern'], code))
            if check['required'] and not found:
                issues.append({
                    'severity': 'ERROR',
                    'check': check['name'],
                    'issue': check['message'],
                    'fix': f"Add {check['name']} to the generated code",
                })
            elif not check['required'] and found:
                issues.append({
                    'severity': 'WARNING',
                    'check': check['name'],
                    'issue': check['message'],
                    'fix': 'Refactor to use framework constants',
                })
        return issues

    def _llm_review(self, code: str, description: str) -> list[dict]:
        """LLM-based semantic review."""
        try:
            prompt = f"Test description: {description}\n\nJava code to review:\n```java\n{code}\n```"
            response = self.llm.invoke([
                SystemMessage(content=REVIEW_SYSTEM_PROMPT),
                HumanMessage(content=prompt),
            ])
            raw = response.content.strip()
            if raw.startswith('```'):
                raw = raw.split('\n', 1)[1].rsplit('```', 1)[0]
            import json
            return json.loads(raw)
        except Exception as e:
            return [{'severity': 'WARNING', 'issue': f'LLM review failed: {e}', 'fix': ''}]

    def run(self, state: AgentState) -> AgentState:
        """LangGraph node function."""
        generated = state.get('generated_code', [])
        state['messages'] = [
            "[ReviewerAgent] Reviewing generated code..."
        ]

        review_results = []
        revision_requests = []

        for gen in generated:
            if gen.get('status') == 'error':
                continue

            code = gen.get('code', '')
            module_path = gen.get('module_path', '')
            descriptions = [s.get('description', '') for s in gen.get('scenarios', [])]

            # Static checks
            static_issues = self._static_check(code)

            # LLM review
            llm_issues = self._llm_review(code, '; '.join(descriptions))

            all_issues = static_issues + llm_issues
            errors = [i for i in all_issues if i.get('severity') == 'ERROR']
            approved = len(errors) == 0

            review_results.append({
                'module_path': module_path,
                'issues': all_issues,
                'approved': approved,
                'error_count': len(errors),
                'warning_count': len([i for i in all_issues if i.get('severity') == 'WARNING']),
            })

            if not approved and state.get('revision_count', 0) < state.get('max_revisions', 2):
                revision_requests.append({
                    'module_path': module_path,
                    'original_code': code,
                    'fix_instructions': '\n'.join(
                        f"[{i['severity']}] {i['issue']} → {i.get('fix', '')}"
                        for i in errors
                    ),
                })

        state['review_results'] = review_results
        state['revision_requests'] = revision_requests

        approved_count = sum(1 for r in review_results if r['approved'])
        state['messages'] = [
            f"[ReviewerAgent] {approved_count}/{len(review_results)} approved. "
            f"{len(revision_requests)} revision(s) needed."
        ]
        return state
