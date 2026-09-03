#!/bin/bash
# =============================================================
# FAULT INJECTION: Simulate Disk Full
# Purpose: Create a large temporary file to fill disk space
# Used in: M34 (MidStage)
# Safety:  Creates file in /tmp, auto-limited to 500MB max,
#          easy cleanup with stop command
# =============================================================

ACTION=${1:-help}
FILL_SIZE=${2:-500}  # Default: 500MB
FILL_FILE="/tmp/foodexpress-disk-fill.dat"

show_help() {
    echo "Usage: $0 {start|stop|status} [size_mb]"
    echo ""
    echo "  start [size_mb]  - Create a large file to consume disk space (default: 500MB)"
    echo "  stop             - Remove the large file and free space"
    echo "  status           - Show current disk usage"
    echo ""
    echo "Examples:"
    echo "  $0 start 500    # Fill 500MB of disk space"
    echo "  $0 start 200    # Fill 200MB of disk space"
    echo "  $0 stop         # Clean up and free space"
}

case "$ACTION" in
    start)
        # Safety: cap at 1GB to prevent actual disk issues
        if [ "$FILL_SIZE" -gt 1000 ]; then
            echo "[SAFETY] Maximum fill size is 1000MB. Using 1000MB."
            FILL_SIZE=1000
        fi

        echo "[FAULT INJECTION] Creating ${FILL_SIZE}MB file to simulate disk full..."
        echo "[INFO] File location: $FILL_FILE"

        # Show disk space before
        echo ""
        echo "Disk space BEFORE:"
        df -h / | head -2
        echo ""

        # Create the file using dd (fallocate not available everywhere)
        dd if=/dev/zero of="$FILL_FILE" bs=1M count=$FILL_SIZE status=progress 2>&1

        echo ""
        echo "[FAULT INJECTED] ${FILL_SIZE}MB consumed."
        echo ""
        echo "Disk space AFTER:"
        df -h / | head -2
        echo ""
        echo "[INFO] Participants should investigate disk usage (df -h, du -sh /tmp/*)."
        echo "[INFO] Run '$0 stop' to clean up when ready."
        ;;

    stop)
        echo "[RECOVERY] Removing disk fill file..."
        if [ -f "$FILL_FILE" ]; then
            SIZE=$(du -h "$FILL_FILE" | cut -f1)
            rm -f "$FILL_FILE"
            echo "[CLEANUP] Removed $FILL_FILE ($SIZE freed)."
        else
            echo "[INFO] No fill file found. Nothing to clean up."
        fi

        echo ""
        echo "Current disk space:"
        df -h / | head -2
        ;;

    status)
        echo "[STATUS] Current disk usage:"
        df -h / | head -2
        echo ""
        if [ -f "$FILL_FILE" ]; then
            echo "[FAULT ACTIVE] Fill file exists: $(du -h "$FILL_FILE" | cut -f1)"
        else
            echo "[NO FAULT] No fill file present."
        fi
        ;;

    *)
        show_help
        ;;
esac
