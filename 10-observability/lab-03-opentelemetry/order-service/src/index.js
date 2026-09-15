const express = require("express");
const axios = require("axios");
const { v4: uuidv4 } = require("uuid");
const { trace, SpanStatusCode, metrics } = require("@opentelemetry/api");
const { logs, SeverityNumber } = require("@opentelemetry/api-logs");

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;
const PAYMENT_SERVICE_URL =
  process.env.PAYMENT_SERVICE_URL || "http://localhost:8080";

// ---- OTel Tracer (for custom spans) ----
const tracer = trace.getTracer("order-service");

// ---- OTel Meter (for custom metrics) ----
const meter = metrics.getMeter("order-service");

const ordersCounter = meter.createCounter("orders_created_total", {
  description: "Total number of orders created",
});

const paymentDuration = meter.createHistogram("payment_call_duration_ms", {
  description: "Duration of payment service calls in ms",
  unit: "ms",
});

const paymentErrors = meter.createCounter("payment_errors_total", {
  description: "Total payment service errors",
});

// ---- OTel Logger ----
const logger = logs.getLogger("order-service");

function otelLog(level, severityNumber, message, attributes = {}) {
  logger.emit({
    severityNumber,
    severityText: level,
    body: message,
    attributes: { service: "order-service", ...attributes },
  });
  // Also log to console for container visibility
  console.log(JSON.stringify({ level, message, ...attributes }));
}

const orders = new Map();

// Request duration middleware (auto-instrumented by OTel, but we add custom attributes)
app.use((req, res, next) => {
  const start = Date.now();
  res.on("finish", () => {
    const duration = Date.now() - start;
    if (res.statusCode >= 400) {
      otelLog("WARN", SeverityNumber.WARN, "HTTP Request", {
        method: req.method,
        path: req.path,
        statusCode: res.statusCode,
        duration,
      });
    }
  });
  next();
});

app.get("/health", (req, res) => {
  res.json({ status: "UP", service: "order-service" });
});

app.post("/orders", async (req, res) => {
  const { item, quantity, price } = req.body;

  if (!item || !quantity || !price) {
    otelLog("WARN", SeverityNumber.WARN, "Invalid order request - missing fields", {
      body: JSON.stringify(req.body),
    });
    return res.status(400).json({ error: "item, quantity, and price are required" });
  }

  // Custom span for order processing
  const span = tracer.startSpan("process-order");

  const order = {
    id: uuidv4(),
    item,
    quantity,
    price,
    totalAmount: quantity * price,
    status: "CREATED",
    createdAt: new Date().toISOString(),
  };

  span.setAttribute("order.id", order.id);
  span.setAttribute("order.item", item);
  span.setAttribute("order.quantity", quantity);
  span.setAttribute("order.total_amount", order.totalAmount);

  otelLog("INFO", SeverityNumber.INFO, "Order created", {
    orderId: order.id,
    item,
    quantity,
    totalAmount: order.totalAmount,
  });

  const paymentStart = Date.now();

  try {
    const paymentResponse = await axios.post(
      `${PAYMENT_SERVICE_URL}/payments`,
      { orderId: order.id, amount: order.totalAmount },
      { timeout: 5000 }
    );

    paymentDuration.record(Date.now() - paymentStart);

    order.paymentId = paymentResponse.data.id;
    order.status = paymentResponse.data.status === "COMPLETED" ? "CONFIRMED" : "PAYMENT_FAILED";

    span.setAttribute("order.payment_id", order.paymentId);
    span.setAttribute("order.status", order.status);

    if (order.status === "CONFIRMED") {
      otelLog("INFO", SeverityNumber.INFO, "Payment successful", {
        orderId: order.id,
        paymentId: order.paymentId,
      });
    } else {
      span.setStatus({ code: SpanStatusCode.ERROR, message: "Payment declined" });
      otelLog("WARN", SeverityNumber.WARN, "Payment declined", {
        orderId: order.id,
        paymentId: order.paymentId,
      });
    }
  } catch (err) {
    paymentDuration.record(Date.now() - paymentStart);
    order.status = "PAYMENT_FAILED";

    const errorType = err.code === "ECONNABORTED" ? "timeout"
      : err.response?.status === 500 ? "server_error"
      : "connection_error";

    span.setAttribute("error.type", errorType);
    span.setStatus({ code: SpanStatusCode.ERROR, message: err.message });
    span.recordException(err);
    paymentErrors.add(1, { error_type: errorType });

    otelLog("ERROR", SeverityNumber.ERROR, `Payment ${errorType}`, {
      orderId: order.id,
      error: err.message,
    });
  }

  ordersCounter.add(1, { status: order.status });
  span.end();
  orders.set(order.id, order);
  res.status(201).json(order);
});

app.get("/orders", (req, res) => {
  res.json(Array.from(orders.values()));
});

app.get("/orders/:id", (req, res) => {
  const order = orders.get(req.params.id);
  if (!order) {
    otelLog("WARN", SeverityNumber.WARN, "Order not found", { orderId: req.params.id });
    return res.status(404).json({ error: "Order not found" });
  }
  res.json(order);
});

app.listen(PORT, () => {
  otelLog("INFO", SeverityNumber.INFO, "Server started", { port: PORT });
});
