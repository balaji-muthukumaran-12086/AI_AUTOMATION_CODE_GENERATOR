"""
Run all 34 failed tests sequentially, updating tests_to_run.json after each.
"""
import json, os, sys, subprocess, time

sys.path.insert(0, os.path.dirname(__file__))
from config.project_config import (SDP_URL, SDP_ADMIN_EMAIL, SDP_EMAIL_ID, 
                                   SDP_PORTAL, SDP_ADMIN_PASS, PROJECT_NAME)

JSON_PATH = f'{PROJECT_NAME}/tests_to_run.json'
REPORTS_DIR = f'{PROJECT_NAME}/reports'

def get_result_from_report(method_name):
    """Check latest ScenarioReport.html for PASS/FAIL."""
    matching = sorted([d for d in os.listdir(REPORTS_DIR) 
                      if d.startswith(f'LOCAL_{method_name}_')], reverse=True)
    if not matching:
        return None
    html_path = os.path.join(REPORTS_DIR, matching[0], 'ScenarioReport.html')
    if not os.path.isfile(html_path):
        return None
    with open(html_path) as f:
        content = f.read()
    if 'data-result="FAIL"' in content:
        return 'FAIL'
    elif 'data-result="PASS"' in content:
        return 'PASS'
    return None

def update_run_config(entity_class, method_name):
    """Rewrite run_test.py RUN_CONFIG to target the given test."""
    with open('run_test.py') as f:
        content = f.read()
    
    import re
    content = re.sub(r'"entity_class":\s*"[^"]*"', f'"entity_class":  "{entity_class}"', content)
    content = re.sub(r'"method_name":\s*"[^"]*"', f'"method_name": "{method_name}"', content)
    
    with open('run_test.py', 'w') as f:
        f.write(content)

def run_test(entity_class, method_name):
    """Run a single test and return PASS/FAIL."""
    update_run_config(entity_class, method_name)
    print(f'\n{"="*60}')
    print(f'  RUNNING: {entity_class}.{method_name}')
    print(f'{"="*60}')
    
    result = subprocess.run(
        ['.venv/bin/python', 'run_test.py'],
        capture_output=True, text=True, timeout=600
    )
    
    # Check report
    status = get_result_from_report(method_name)
    return status or ('PASS' if result.returncode == 0 else 'FAIL')

def main():
    with open(JSON_PATH) as f:
        data = json.load(f)
    
    failed_tests = [(t['entity_class'], t['method_name'], i) 
                    for i, t in enumerate(data['tests']) 
                    if t.get('status') and 'FAIL' in str(t.get('status'))]
    
    print(f'Found {len(failed_tests)} failed tests to re-run.')
    
    # Map entity classes to Java class names
    class_map = {'ChangeDetailsView': 'DetailsView', 'ChangeListView': 'ListView'}
    
    passed = 0
    still_fail = 0
    
    for idx, (ec, method, json_idx) in enumerate(failed_tests, 1):
        java_class = class_map.get(ec, ec)
        print(f'\n[{idx}/{len(failed_tests)}] {java_class}.{method}')
        
        try:
            status = run_test(java_class, method)
        except subprocess.TimeoutExpired:
            status = 'FAIL'
            print(f'  TIMEOUT after 600s', flush=True)
        except Exception as e:
            status = 'FAIL'
            print(f'  ERROR: {e}')
        
        # Update JSON
        data['tests'][json_idx]['status'] = status
        with open(JSON_PATH, 'w') as f:
            json.dump(data, f, indent=2)
        
        if status == 'PASS':
            passed += 1
            print(f'  ✓ PASS')
        else:
            still_fail += 1
            print(f'  ✗ FAIL')
        
        print(f'  Progress: {passed} PASS / {still_fail} FAIL / {len(failed_tests) - idx} remaining')
    
    print(f'\n{"="*60}')
    print(f'  BATCH COMPLETE: {passed} PASS / {still_fail} FAIL out of {len(failed_tests)}')
    print(f'{"="*60}')

if __name__ == '__main__':
    main()
