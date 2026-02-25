"""
coverage_report.py
------------------
Generates a coverage heatmap report showing:
  - Which modules have the most / fewest tests
  - Which CRUD operations are covered per entity
  - Which modules have NO negative / edge case tests
  - Duplicate density (potential redundancy)
  - Suggested gap areas

Output: evaluation/coverage_report.json + coverage_report.html
"""

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime


# ── CRUD coverage heuristics ───────────────────────────────────────────────

CRUD_KEYWORDS = {
    'CREATE': ['create', 'add', 'new', 'insert'],
    'READ':   ['view', 'list', 'get', 'display', 'search', 'filter', 'sort'],
    'UPDATE': ['edit', 'update', 'modify', 'change', 'set'],
    'DELETE': ['delete', 'remove', 'trash', 'bulk delete'],
    'VALIDATE': ['validate', 'verify', 'check', 'assert'],
    'NEGATIVE': ['invalid', 'negative', 'error', 'fail', 'empty', 'null', 'missing'],
    'EDGE': ['edge', 'boundary', 'max', 'min', 'special char', 'long', 'concurrent'],
    'ROLE': ['permission', 'role', 'access', 'unauthorized', 'admin', 'technician'],
}


def classify_scenario(description: str) -> list[str]:
    """Infer coverage categories from scenario description."""
    desc_lower = description.lower()
    categories = []
    for cat, keywords in CRUD_KEYWORDS.items():
        if any(kw in desc_lower for kw in keywords):
            categories.append(cat)
    return categories or ['OTHER']


# ── Main report builder ────────────────────────────────────────────────────

def generate_coverage_report(
    module_index_path: str,
    output_dir: str = None,
) -> dict:
    with open(module_index_path, encoding='utf-8') as f:
        index = json.load(f)

    if output_dir is None:
        output_dir = str(Path(module_index_path).parent.parent.parent / 'evaluation')
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    modules_data = index.get('modules', {})
    report = {
        'generated_at': datetime.now().isoformat(),
        'total_modules': len(modules_data),
        'total_scenarios': sum(m.get('scenario_count', 0) for m in modules_data.values()),
        'modules': {},
        'gaps': [],
        'summary': {},
    }

    # Per-module analysis
    all_category_counts = defaultdict(int)

    for mp, mod in modules_data.items():
        scenarios = mod.get('scenarios', [])
        scenario_count = len(scenarios)

        # Coverage categories
        coverage = defaultdict(int)
        for sc in scenarios:
            for cat in classify_scenario(sc.get('description', '')):
                coverage[cat] += 1
                all_category_counts[cat] += 1

        # Coverage completeness score (0-100)
        covered_ops = sum(1 for op in ['CREATE', 'READ', 'UPDATE', 'DELETE']
                          if coverage[op] > 0)
        completeness = int((covered_ops / 4) * 100)

        # Identify gaps
        missing_ops = [op for op in ['CREATE', 'READ', 'UPDATE', 'DELETE']
                       if coverage[op] == 0]
        has_negative = coverage['NEGATIVE'] > 0
        has_role = coverage['ROLE'] > 0

        report['modules'][mp] = {
            'entity': mod.get('entity', ''),
            'module': mod.get('module', ''),
            'scenario_count': scenario_count,
            'coverage': dict(coverage),
            'completeness_pct': completeness,
            'missing_crud_ops': missing_ops,
            'has_negative_tests': has_negative,
            'has_role_tests': has_role,
            'risk_level': _compute_risk(scenario_count, completeness, has_negative),
        }

        # Gap analysis
        if missing_ops:
            report['gaps'].append({
                'module': mp,
                'entity': mod.get('entity', ''),
                'gap_type': 'MISSING_CRUD',
                'detail': f"Missing {', '.join(missing_ops)} scenarios",
                'severity': 'HIGH' if 'CREATE' in missing_ops else 'MEDIUM',
            })
        if not has_negative:
            report['gaps'].append({
                'module': mp,
                'entity': mod.get('entity', ''),
                'gap_type': 'NO_NEGATIVE_TESTS',
                'detail': 'No negative / error scenario found',
                'severity': 'MEDIUM',
            })
        if not has_role and scenario_count > 5:
            report['gaps'].append({
                'module': mp,
                'entity': mod.get('entity', ''),
                'gap_type': 'NO_ROLE_TESTS',
                'detail': 'No role-based permission tests found',
                'severity': 'LOW',
            })
        if scenario_count == 0:
            report['gaps'].append({
                'module': mp,
                'entity': mod.get('entity', ''),
                'gap_type': 'ZERO_COVERAGE',
                'detail': 'No test scenarios found for this module',
                'severity': 'CRITICAL',
            })

    # Sort gaps by severity
    severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
    report['gaps'].sort(key=lambda g: severity_order.get(g['severity'], 4))

    # Summary stats
    report['summary'] = {
        'category_distribution': dict(all_category_counts),
        'critical_gaps': sum(1 for g in report['gaps'] if g['severity'] == 'CRITICAL'),
        'high_gaps': sum(1 for g in report['gaps'] if g['severity'] == 'HIGH'),
        'medium_gaps': sum(1 for g in report['gaps'] if g['severity'] == 'MEDIUM'),
        'low_gaps': sum(1 for g in report['gaps'] if g['severity'] == 'LOW'),
        'avg_scenarios_per_module': (
            report['total_scenarios'] / report['total_modules']
            if report['total_modules'] else 0
        ),
        'modules_with_zero_coverage': sum(
            1 for m in report['modules'].values() if m['scenario_count'] == 0
        ),
        'top_10_most_tested': sorted(
            [(mp, m['scenario_count']) for mp, m in report['modules'].items()],
            key=lambda x: -x[1]
        )[:10],
        'top_10_least_tested': sorted(
            [(mp, m['scenario_count']) for mp, m in report['modules'].items()
             if m['scenario_count'] > 0],
            key=lambda x: x[1]
        )[:10],
    }

    # Write JSON
    json_path = Path(output_dir) / 'coverage_report.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Write HTML
    html_path = Path(output_dir) / 'coverage_report.html'
    _write_html_report(report, str(html_path))

    print(f"  ✅ Coverage report:")
    print(f"     Modules:   {report['total_modules']}")
    print(f"     Scenarios: {report['total_scenarios']}")
    print(f"     Critical gaps: {report['summary']['critical_gaps']}")
    print(f"     High gaps:     {report['summary']['high_gaps']}")
    print(f"     JSON: {json_path}")
    print(f"     HTML: {html_path}")

    return report


def _compute_risk(scenario_count: int, completeness: int, has_negative: bool) -> str:
    if scenario_count == 0:
        return 'CRITICAL'
    if completeness < 25 or (scenario_count < 3 and not has_negative):
        return 'HIGH'
    if completeness < 50 or not has_negative:
        return 'MEDIUM'
    return 'LOW'


def _write_html_report(report: dict, path: str) -> None:
    """Write a simple but readable HTML coverage dashboard."""
    rows = []
    for mp, m in sorted(report['modules'].items(),
                        key=lambda x: x[1]['scenario_count'], reverse=True):
        risk_color = {
            'CRITICAL': '#dc3545', 'HIGH': '#fd7e14',
            'MEDIUM': '#ffc107', 'LOW': '#28a745'
        }.get(m['risk_level'], '#6c757d')

        cov = m.get('coverage', {})
        crud_cells = ''.join(
            f'<td style="color:{"green" if cov.get(op, 0) > 0 else "red"}">'
            f'{"✓" if cov.get(op, 0) > 0 else "✗"}</td>'
            for op in ['CREATE', 'READ', 'UPDATE', 'DELETE', 'VALIDATE', 'NEGATIVE', 'ROLE']
        )
        rows.append(
            f'<tr>'
            f'<td>{mp}</td>'
            f'<td>{m["scenario_count"]}</td>'
            f'<td>{m["completeness_pct"]}%</td>'
            f'{crud_cells}'
            f'<td style="color:{risk_color};font-weight:bold">{m["risk_level"]}</td>'
            f'</tr>'
        )

    html = f"""<!DOCTYPE html>
<html><head>
<title>AutomaterSelenium Coverage Report</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 20px; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 12px; }}
  th, td {{ border: 1px solid #ddd; padding: 6px 8px; text-align: center; }}
  th {{ background: #343a40; color: white; }}
  tr:hover {{ background: #f5f5f5; }}
  .stat {{ display: inline-block; margin: 10px; padding: 15px; background: #f8f9fa;
           border-radius: 8px; text-align: center; min-width: 120px; }}
  .stat-value {{ font-size: 2em; font-weight: bold; }}
  h2 {{ color: #343a40; }}
</style>
</head><body>
<h1>🧪 AutomaterSelenium Coverage Report</h1>
<p>Generated: {report['generated_at']}</p>

<div>
  <div class="stat"><div class="stat-value">{report['total_modules']}</div>Modules</div>
  <div class="stat"><div class="stat-value">{report['total_scenarios']}</div>Scenarios</div>
  <div class="stat" style="background:#ffe0e0">
    <div class="stat-value" style="color:red">{report['summary']['critical_gaps']}</div>
    Critical Gaps</div>
  <div class="stat" style="background:#fff3cd">
    <div class="stat-value" style="color:orange">{report['summary']['high_gaps']}</div>
    High Gaps</div>
</div>

<h2>Module Coverage</h2>
<table>
  <tr>
    <th>Module Path</th><th>Scenarios</th><th>Completeness</th>
    <th>CREATE</th><th>READ</th><th>UPDATE</th><th>DELETE</th>
    <th>VALIDATE</th><th>NEGATIVE</th><th>ROLE</th><th>Risk</th>
  </tr>
  {''.join(rows)}
</table>

<h2>Coverage Gaps ({len(report['gaps'])} total)</h2>
<table>
  <tr><th>Module</th><th>Gap Type</th><th>Detail</th><th>Severity</th></tr>
  {''.join(
    '<tr><td>{}</td><td>{}</td><td>{}</td><td style="color:{}">{}</td></tr>'.format(
        g["module"], g["gap_type"], g["detail"],
        {"CRITICAL":"red","HIGH":"orange","MEDIUM":"#b8860b","LOW":"green"}.get(g["severity"],"black"),
        g["severity"]
    )
    for g in report['gaps'][:100]
  )}
</table>
</body></html>"""

    Path(path).write_text(html, encoding='utf-8')


if __name__ == '__main__':
    base = Path(__file__).resolve().parents[1]
    generate_coverage_report(
        str(base / 'knowledge_base' / 'raw' / 'module_index.json'),
        str(base / 'evaluation'),
    )
