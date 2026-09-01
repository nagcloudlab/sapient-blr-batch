#!/bin/bash
# =============================================================
# FAULT INJECTION: Simulate Memory Leak
# Purpose: Start a Node.js process that slowly consumes memory
# Used in: M37 (Final)
# Safety:  Capped at 512MB max, auto-stops after 10 minutes,
#          killed with stop command
# Requires: Node.js installed
# =============================================================

ACTION=${1:-help}
GROWTH_MB_PER_SEC=${2:-5}   # Default: 5MB per second
MAX_MB=${3:-512}            # Default: stop at 512MB

LEAK_SCRIPT="/tmp/foodexpress-memory-leak.js"
PID_FILE="/tmp/foodexpress-memory-leak.pid"

show_help() {
    echo "Usage: $0 {start|stop|status} [mb_per_sec] [max_mb]"
    echo ""
    echo "  start [rate] [max]  - Start memory leak simulation"
    echo "  stop                - Stop the leak and free memory"
    echo "  status              - Check current memory usage"
    echo ""
    echo "Examples:"
    echo "  $0 start 5 512    # Grow 5MB/sec, stop at 512MB"
    echo "  $0 start 10 256   # Grow 10MB/sec, stop at 256MB"
    echo "  $0 stop           # Kill the leak process"
}

case "$ACTION" in
    start)
        echo "[FAULT INJECTION] Starting memory leak simulation..."
        echo "  Growth rate: ${GROWTH_MB_PER_SEC}MB/sec"
        echo "  Max memory: ${MAX_MB}MB"

        # Create the leak script
        cat > "$LEAK_SCRIPT" << 'LEAK_EOF'
const RATE = parseInt(process.env.GROWTH_RATE || '5');
const MAX = parseInt(process.env.MAX_MB || '512');
const AUTO_STOP_MIN = 10;

const leakedData = [];
let totalMB = 0;

console.log(`[MEMORY LEAK] Starting: ${RATE}MB/sec, max ${MAX}MB, auto-stop in ${AUTO_STOP_MIN} min`);

const interval = setInterval(() => {
    // Allocate ~1MB per iteration
    for (let i = 0; i < RATE; i++) {
        leakedData.push(Buffer.alloc(1024 * 1024, 'X'));
        totalMB++;
    }

    const usage = process.memoryUsage();
    const heapMB = Math.round(usage.heapUsed / 1024 / 1024);
    const rssMB = Math.round(usage.rss / 1024 / 1024);

    console.log(`[MEMORY LEAK] Heap: ${heapMB}MB | RSS: ${rssMB}MB | Allocated: ${totalMB}MB`);

    if (totalMB >= MAX) {
        console.log(`[MEMORY LEAK] Reached ${MAX}MB limit. Stopping growth (holding memory).`);
        clearInterval(interval);
    }
}, 1000);

// Auto-stop after 10 minutes for safety
setTimeout(() => {
    console.log(`[MEMORY LEAK] Auto-stop after ${AUTO_STOP_MIN} minutes. Exiting.`);
    process.exit(0);
}, AUTO_STOP_MIN * 60 * 1000);

process.on('SIGTERM', () => {
    console.log('[MEMORY LEAK] Received SIGTERM. Cleaning up and exiting.');
    process.exit(0);
});
LEAK_EOF

        # Start the leak
        GROWTH_RATE=$GROWTH_MB_PER_SEC MAX_MB=$MAX_MB \
            node --max-old-space-size=$((MAX_MB + 128)) "$LEAK_SCRIPT" &
        echo $! > "$PID_FILE"

        echo ""
        echo "[FAULT INJECTED] Memory leak running (PID: $(cat $PID_FILE))."
        echo "[INFO] Monitor with: top -p $(cat $PID_FILE)"
        echo "[INFO] Or: watch -n 1 'ps -o pid,rss,vsz,comm -p $(cat $PID_FILE)'"
        echo "[INFO] Auto-stops after 10 minutes or at ${MAX_MB}MB."
        echo "[INFO] Run '$0 stop' to clean up."
        ;;

    stop)
        echo "[RECOVERY] Stopping memory leak..."
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            kill $PID 2>/dev/null
            rm -f "$PID_FILE" "$LEAK_SCRIPT"
            echo "[CLEANUP] Leak process stopped (PID: $PID). Memory freed."
        else
            echo "[INFO] No PID file found. Checking for orphaned processes..."
            pkill -f "foodexpress-memory-leak" 2>/dev/null
            rm -f "$LEAK_SCRIPT"
            echo "[CLEANUP] Done."
        fi
        ;;

    status)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if kill -0 $PID 2>/dev/null; then
                RSS=$(ps -o rss= -p $PID 2>/dev/null)
                RSS_MB=$((RSS / 1024))
                echo "[FAULT ACTIVE] Memory leak running (PID: $PID, RSS: ${RSS_MB}MB)."
            else
                echo "[STALE] PID file exists but process has stopped."
                rm -f "$PID_FILE"
            fi
        else
            echo "[NO FAULT] Memory leak is not running."
        fi
        ;;

    *)
        show_help
        ;;
esac
