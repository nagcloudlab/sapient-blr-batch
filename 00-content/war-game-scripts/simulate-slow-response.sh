#!/bin/bash
# =============================================================
# FAULT INJECTION: Simulate Slow Response
# Purpose: Start a proxy that adds artificial delay to responses
# Used in: M34 (MidStage), M37 (Final)
# Safety:  Runs a simple Node.js proxy; killed with stop command
# Requires: Node.js installed
# =============================================================

ACTION=${1:-help}
DELAY_MS=${2:-3000}       # Default: 3 second delay
TARGET_PORT=${3:-3000}    # Service to slow down
PROXY_PORT=${4:-9000}     # Proxy listens on this port

PROXY_SCRIPT="/tmp/foodexpress-slow-proxy.js"
PID_FILE="/tmp/foodexpress-slow-proxy.pid"

show_help() {
    echo "Usage: $0 {start|stop|status} [delay_ms] [target_port] [proxy_port]"
    echo ""
    echo "  start [delay] [target] [proxy]  - Start slow proxy"
    echo "  stop                            - Stop the proxy"
    echo "  status                          - Check if proxy is running"
    echo ""
    echo "Examples:"
    echo "  $0 start 3000 3000 9000   # 3s delay, proxy port 9000 -> service port 3000"
    echo "  $0 start 5000 8080 9080   # 5s delay, proxy port 9080 -> service port 8080"
    echo "  $0 stop                   # Stop the proxy"
    echo ""
    echo "After starting, point clients to port $PROXY_PORT instead of $TARGET_PORT."
}

case "$ACTION" in
    start)
        echo "[FAULT INJECTION] Starting slow proxy..."
        echo "  Delay: ${DELAY_MS}ms"
        echo "  Target: localhost:${TARGET_PORT}"
        echo "  Proxy:  localhost:${PROXY_PORT}"

        # Create the proxy script
        cat > "$PROXY_SCRIPT" << 'PROXY_EOF'
const http = require('http');
const DELAY = parseInt(process.env.DELAY_MS || '3000');
const TARGET = parseInt(process.env.TARGET_PORT || '3000');
const PORT = parseInt(process.env.PROXY_PORT || '9000');

const server = http.createServer((req, res) => {
    console.log(`[SLOW PROXY] ${req.method} ${req.url} -- adding ${DELAY}ms delay`);

    setTimeout(() => {
        const options = {
            hostname: 'localhost',
            port: TARGET,
            path: req.url,
            method: req.method,
            headers: req.headers
        };

        const proxy = http.request(options, (proxyRes) => {
            res.writeHead(proxyRes.statusCode, proxyRes.headers);
            proxyRes.pipe(res);
        });

        proxy.on('error', (err) => {
            res.writeHead(502);
            res.end(`Proxy error: ${err.message}`);
        });

        req.pipe(proxy);
    }, DELAY);
});

server.listen(PORT, () => {
    console.log(`[SLOW PROXY] Listening on port ${PORT}, forwarding to ${TARGET} with ${DELAY}ms delay`);
});
PROXY_EOF

        # Start the proxy
        DELAY_MS=$DELAY_MS TARGET_PORT=$TARGET_PORT PROXY_PORT=$PROXY_PORT \
            node "$PROXY_SCRIPT" &
        echo $! > "$PID_FILE"

        echo ""
        echo "[FAULT INJECTED] Proxy running (PID: $(cat $PID_FILE))."
        echo "[INFO] Point clients to http://localhost:$PROXY_PORT to experience the delay."
        echo "[INFO] Run '$0 stop' to remove the delay."
        ;;

    stop)
        echo "[RECOVERY] Stopping slow proxy..."
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            kill $PID 2>/dev/null
            rm -f "$PID_FILE" "$PROXY_SCRIPT"
            echo "[CLEANUP] Proxy stopped (PID: $PID). Artifacts removed."
        else
            echo "[INFO] No proxy PID file found. Checking for orphaned processes..."
            pkill -f "foodexpress-slow-proxy" 2>/dev/null
            rm -f "$PROXY_SCRIPT"
            echo "[CLEANUP] Done."
        fi
        ;;

    status)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if kill -0 $PID 2>/dev/null; then
                echo "[FAULT ACTIVE] Slow proxy running (PID: $PID)."
            else
                echo "[STALE] PID file exists but process is not running."
            fi
        else
            echo "[NO FAULT] Slow proxy is not running."
        fi
        ;;

    *)
        show_help
        ;;
esac
