#!/bin/bash
#
# FoodExpress Log Analyzer Script (FIXED)
#
# ALL BUGS FIXED:
# FIX 1: Using grep -i for case-insensitive matching
# FIX 2: Corrected date format to YYYY-MM-DD (ISO format matching logs)
# FIX 3: Using >> (append) instead of > (overwrite) for report file

LOG_DIR="/var/log/foodexpress"
APP_LOG="$LOG_DIR/application.log"
REPORT_FILE="/tmp/foodexpress-analysis.txt"

# FIX 2: Corrected date format to match log format (YYYY-MM-DD)
TODAY=$(date '+%Y-%m-%d')

# FIX 3: Start fresh report with > for the header only, then >> for the rest
echo "=== FoodExpress Log Analysis ===" > "$REPORT_FILE"
echo "Date: $TODAY" >> "$REPORT_FILE"
echo "Analyzing: $APP_LOG" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "=== FoodExpress Log Analysis ==="
echo "Date: $TODAY"
echo "Analyzing: $APP_LOG"
echo ""

# Check if log file exists
if [ ! -f "$APP_LOG" ]; then
    echo "Log file not found: $APP_LOG"
    exit 1
fi

# FIX 1: Using -i flag for case-insensitive grep
# Now matches 'error', 'ERROR', 'Error', etc.
echo "=== Error Summary ==="
ERROR_COUNT=$(grep -ci "error" "$APP_LOG")
echo "Total errors: $ERROR_COUNT"

# FIX 3: Using >> to append
echo "Error count: $ERROR_COUNT" >> "$REPORT_FILE"

echo ""
echo "=== Top Error Messages ==="
# FIX 1: Case-insensitive grep
grep -i "error" "$APP_LOG" | awk '{print $5, $6, $7}' | sort | uniq -c | sort -rn | head -10

# FIX 3: Append instead of overwrite
echo "=== Top Errors ===" >> "$REPORT_FILE"
grep -i "error" "$APP_LOG" | awk '{print $5, $6, $7}' | sort | uniq -c | sort -rn | head -10 >> "$REPORT_FILE"

echo ""
echo "=== Response Time Analysis ==="
# FIX 2: Now uses correct date format to find today's entries
grep "$TODAY" "$APP_LOG" | grep "response_time" | awk -F'=' '{print $2}' | \
    awk '{ sum += $1; count++ } END { if(count>0) print "Average response time:", sum/count, "ms" }'

echo ""
echo "=== 5xx Errors ==="
grep "HTTP/1.1\" 5" "$APP_LOG" | wc -l

# FIX 3: Append instead of overwrite
echo "=== 5xx Errors ===" >> "$REPORT_FILE"
grep "HTTP/1.1\" 5" "$APP_LOG" | wc -l >> "$REPORT_FILE"

echo ""
echo "Report saved to: $REPORT_FILE"
