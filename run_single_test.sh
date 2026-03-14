#!/usr/bin/env bash
# run_single_test.sh — Run a single test by method name without editing run_test.py
# Usage: ./run_single_test.sh <method_name> [entity_class]
# Returns: PASS or FAIL + report path

set -euo pipefail

METHOD="${1:?Usage: $0 <method_name> [entity_class]}"
ENTITY="${2:-DetailsView}"

cd "$(dirname "$0")"

# Temporarily patch run_test.py with the target method
sed -i "s/\"method_name\":.*$/\"method_name\":   \"${METHOD}\",/" run_test.py
sed -i "s/\"entity_class\":.*$/\"entity_class\":  \"${ENTITY}\",/" run_test.py

# Run and capture output
OUTPUT=$(.venv/bin/python run_test.py 2>&1) || true

# Find the latest report directory for this method
REPORT_DIR=$(find SDPLIVE_LINKING_CHANGE_AI/reports -maxdepth 1 -type d -name "LOCAL_${METHOD}_*" | sort | tail -1)

# Check result from ScenarioReport.html — use the scenario-result element, not CSS
RESULT="UNKNOWN"
REPORT_FILE="${REPORT_DIR:+$REPORT_DIR/ScenarioReport.html}"

if [[ -z "$REPORT_DIR" ]]; then
    RESULT="FAIL"
    echo "WARNING: No report directory found for LOCAL_${METHOD}_*"
    echo "ScenarioReport.html not found — marking as FAIL"
elif [[ ! -f "$REPORT_DIR/ScenarioReport.html" ]]; then
    RESULT="FAIL"
    echo "WARNING: ScenarioReport.html not found at $REPORT_DIR/"
    echo "ScenarioReport.html not found — marking as FAIL"
else
    # The authoritative result is in: <div class="scenario-result FAIL" id="scenario-result" ...>
    # or <div class="scenario-result PASS" id="scenario-result" ...>
    SCENARIO_RESULT=$(grep -oP 'scenario-result\s+\K(PASS|FAIL)' "$REPORT_DIR/ScenarioReport.html" 2>/dev/null | head -1 || true)
    if [[ "$SCENARIO_RESULT" == "PASS" ]]; then
        RESULT="PASS"
    elif [[ "$SCENARIO_RESULT" == "FAIL" ]]; then
        RESULT="FAIL"
    elif grep -q '$$Failure' "$REPORT_DIR/ScenarioReport.html" 2>/dev/null; then
        RESULT="FAIL"
    elif grep -q 'data-result="FAIL"' "$REPORT_DIR/ScenarioReport.html" 2>/dev/null; then
        RESULT="FAIL"
    elif grep -q 'data-result="PASS"' "$REPORT_DIR/ScenarioReport.html" 2>/dev/null; then
        RESULT="PASS"
    fi
fi

# Fallback: check stdout for signals
if [[ "$RESULT" == "UNKNOWN" ]]; then
    if echo "$OUTPUT" | grep -q '$$Failure'; then
        RESULT="FAIL"
    elif echo "$OUTPUT" | grep -q 'BUILD SUCCESSFUL'; then
        RESULT="PASS"
    elif echo "$OUTPUT" | grep -q 'BUILD FAILED\|NullPointerException\|NoSuchElementException\|TimeoutException'; then
        RESULT="FAIL"
    else
        # No positive signal found — default to FAIL (prevents false PASS)
        RESULT="FAIL"
        echo "WARNING: No definitive result signal found — defaulting to FAIL"
    fi
fi

echo "=== TEST RESULT ==="
echo "Method: ${ENTITY}.${METHOD}"
echo "Result: ${RESULT}"
if [[ -n "$REPORT_DIR" && -f "$REPORT_DIR/ScenarioReport.html" ]]; then
    echo "Report: ${REPORT_DIR}/ScenarioReport.html"
else
    echo "Report: NOT FOUND"
fi

# Print failure details if any
if [[ "$RESULT" == "FAIL" && -n "$REPORT_DIR" && -f "$REPORT_DIR/ScenarioReport.html" ]]; then
    echo "--- Failure Details ---"
    grep -oP 'Failure[^<]*|Not able to[^<]*|Exception[^<]*' "$REPORT_DIR/ScenarioReport.html" 2>/dev/null | head -5
elif [[ "$RESULT" == "FAIL" ]]; then
    echo "--- Failure Details ---"
    echo "ScenarioReport.html not found — check stdout for error details"
fi

# Print key stdout lines
echo "--- Last Output Lines ---"
echo "$OUTPUT" | grep -E '(PASS|FAIL|Success|Failure|Exception|Error|Screenshot|Report)' | tail -10

exit 0
