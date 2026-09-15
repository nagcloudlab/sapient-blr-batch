const http = require("http");

const PORT = 9095;
let alertHistory = [];

const server = http.createServer((req, res) => {
  if (req.method === "POST" && req.url === "/alerts") {
    let body = "";
    req.on("data", (chunk) => (body += chunk));
    req.on("end", () => {
      try {
        const payload = JSON.parse(body);
        const timestamp = new Date().toISOString();
        const alerts = Array.isArray(payload) ? payload : payload.alerts || [payload];

        alerts.forEach((alert) => {
          const entry = {
            time: timestamp,
            status: alert.status,
            name: alert.labels?.alertname,
            severity: alert.labels?.severity,
            service: alert.labels?.service || alert.labels?.job,
            summary: alert.annotations?.summary,
            description: alert.annotations?.description,
          };
          alertHistory.push(entry);

          const icon = alert.status === "firing" ? "FIRING" : "RESOLVED";
          const sev = alert.labels?.severity?.toUpperCase() || "UNKNOWN";
          console.log(
            `[${timestamp}] ${icon} [${sev}] ${entry.name} - ${entry.summary}`
          );
          if (entry.description) {
            console.log(`  -> ${entry.description}`);
          }
        });
      } catch (e) {
        console.error("Failed to parse alert:", e.message);
      }
      res.writeHead(200);
      res.end("OK");
    });
  } else if (req.method === "GET" && req.url === "/alerts") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify(alertHistory, null, 2));
  } else if (req.method === "GET" && req.url === "/") {
    res.writeHead(200, { "Content-Type": "text/html" });
    res.end(`
      <html><head><title>Alert Logger</title>
      <meta http-equiv="refresh" content="5">
      <style>
        body { font-family: monospace; background: #1a1a2e; color: #eee; padding: 20px; }
        h1 { color: #e94560; }
        .alert { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .firing { background: #4a1526; border-left: 4px solid #e94560; }
        .resolved { background: #1a3a2a; border-left: 4px solid #2ecc71; }
        .critical { color: #e94560; }
        .warning { color: #f39c12; }
        .time { color: #888; font-size: 12px; }
      </style></head><body>
      <h1>Alert Logger</h1>
      <p>Total alerts received: ${alertHistory.length}</p>
      ${alertHistory
        .slice(-50)
        .reverse()
        .map(
          (a) => `
        <div class="alert ${a.status}">
          <span class="time">${a.time}</span>
          <span class="${a.severity}">[${(a.severity || "").toUpperCase()}]</span>
          <strong>${a.status?.toUpperCase()}: ${a.name}</strong>
          <br/>${a.summary || ""}
          <br/><small>${a.description || ""}</small>
        </div>`
        )
        .join("")}
      </body></html>
    `);
  } else {
    res.writeHead(404);
    res.end("Not Found");
  }
});

server.listen(PORT, () => {
  console.log(`Alert webhook logger running on port ${PORT}`);
  console.log(`  Web UI: http://localhost:${PORT}`);
  console.log(`  Waiting for alerts...`);
});
