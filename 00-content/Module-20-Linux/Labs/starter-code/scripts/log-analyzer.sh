#!/bin/bash
#
# FoodExpress Log Analyzer Script
#
# CONTAINS BUGS - Find and fix them!
#
# BUG 1: grep pattern is wrong - looking for 'ERROR' but logs use 'error' (case mismatch)
# BUG 2: Date format mismatch - script uses MM/DD/YYYY but logs use YYYY-MM-DD
# BUG 3: Output redirect overwrites instead of appends - loses previous analysis

LOG_DIR="/var/log/foodexpress"
APP_LOG="$LOG_DIR/application.log"
REPORT_FILE="/tmp/foodexpress-analysis.txt"

# BUG 2: Date format mismatch
# Log files use ISO format: 2026-07-27 (YYYY-MM-DD)
# But this script generates: 07/27/2026 (MM/DD/YYYY)
TODAY=$(date '+%m/%d/%Y')

echo "=== FoodExpress Log Analysis ==="
echo "Date: $TODAY"
echo "Analyzing: $APP_LOG"
echo ""

# Check if log file exists
if [ ! -f "$APP_LOG" ]; then
    echo "Log file not found: $APP_LOG"
    exit 1
fi

# BUG 1: Case-sensitive grep - logs use lowercase 'error' but pattern is 'ERROR'
# Sample log line: "2026-07-27 10:15:32 [error] OrderService - Failed to process order"
# This grep will find 0 matches because of case mismatch
echo "=== Error Summary ==="
ERROR_COUNT=$(grep -c "ERROR" "$APP_LOG")
echo "Total errors: $ERROR_COUNT"

# BUG 3: Using > (overwrite) instead of >> (append)
# Each section overwrites the previous one in the report file!
echo "Error count: $ERROR_COUNT" > $REPORT_FILE

echo ""
echo "=== Top Error Messages ==="
# BUG 1: Same case mismatch issue
grep "ERROR" "$APP_LOG" | awk '{print $5, $6, $7}' | sort | uniq -c | sort -rn | head -10

# BUG 3: This overwrites the error count written above!
echo "=== Top Errors ===" > $REPORT_FILE
grep "ERROR" "$APP_LOG" | awk '{print $5, $6, $7}' | sort | uniq -c | sort -rn | head -10 > $REPORT_FILE

echo ""
echo "=== Response Time Analysis ==="
# BUG 2: Date format mismatch - won't find today's entries
grep "$TODAY" "$APP_LOG" | grep "response_time" | awk -F'=' '{print $2}' | \
    awk '{ sum += $1; count++ } END { if(count>0) print "Average response time:", sum/count, "ms" }'

echo ""
echo "=== 5xx Errors ==="
grep "HTTP/1.1\" 5" "$APP_LOG" | wc -l

# BUG 3: Overwrites again!
echo "=== 5xx Errors ===" > $REPORT_FILE
grep "HTTP/1.1\" 5" "$APP_LOG" | wc -l > $REPORT_FILE

echo ""
echo "Report saved to: $REPORT_FILE"
