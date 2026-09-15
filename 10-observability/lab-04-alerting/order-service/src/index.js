const express = require("express");
const axios = require("axios");
const { v4: uuidv4 } = require("uuid");
const client = require("prom-client");

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;
const PAYMENT_SERVICE_URL =
  process.env.PAYMENT_SERVICE_URL || "http://localhost:8080";

// ---- Prometheus Metrics ----
const register = new client.Registry();
client.collectDefaultMetrics({ register });

const httpRequestDuration = new client.Histogram({
  name: "http_request_duration_seconds",
  help: "Duration of HTTP requests in seconds",
  labelNames: ["method", "route", "status_code"],
  buckets: [0.01, 0.05, 0.1, 0.3, 0.5, 1, 2, 5],
  registers: [register],
});

const ordersCreatedTotal = new client.Counter({
  name: "orders_created_total",
  help: "Total number of orders created",
  labelNames: ["status"],
  registers: [register],
});

const paymentCallDuration = new client.Histogram({
  name: "payment_service_call_duration_seconds",
  help: "Duration of calls to payment service",
  buckets: [0.05, 0.1, 0.25, 0.5, 1, 2, 5],
  registers: [register],
});

const paymentCallErrors = new client.Counter({
  name: "payment_service_errors_total",
  help: "Total errors when calling payment service",
  labelNames: ["error_type"],
  registers: [register],
});

// Middleware to track request duration
app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer();
  res.on("finish", () => {
    end({ method: req.method, route: req.route?.path || req.path, status_code: res.statusCode });
  });
  next();
});

// In-memory store
const orders = new Map();

// Metrics endpoint
app.get("/metrics", async (req, res) => {
  res.set("Content-Type", register.contentType);
  res.end(await register.metrics());
});

// Health check
app.get("/health", (req, res) => {
  res.json({ status: "UP", service: "order-service" });
});

// Create order
app.post("/orders", async (req, res) => {
  const { item, quantity, price } = req.body;

  if (!item || !quantity || !price) {
    return res.status(400).json({ error: "item, quantity, and price are required" });
  }

  const order = {
    id: uuidv4(),
    item,
    quantity,
    price,
    totalAmount: quantity * price,
    status: "CREATED",
    createdAt: new Date().toISOString(),
  };

  console.log(`Creating order ${order.id} for ${quantity}x ${item}`);

  try {
    const paymentTimer = paymentCallDuration.startTimer();
    const paymentResponse = await axios.post(
      `${PAYMENT_SERVICE_URL}/payments`,
      { orderId: order.id, amount: order.totalAmount },
      { timeout: 5000 }
    );
    paymentTimer();

    order.paymentId = paymentResponse.data.id;
    order.status = paymentResponse.data.status === "COMPLETED" ? "CONFIRMED" : "PAYMENT_FAILED";
  } catch (err) {
    if (err.code === "ECONNABORTED") {
      paymentCallErrors.inc({ error_type: "timeout" });
      console.error(`Payment TIMEOUT for order ${order.id}`);
    } else if (err.response?.status === 500) {
      paymentCallErrors.inc({ error_type: "server_error" });
      console.error(`Payment SERVER ERROR for order ${order.id}`);
    } else if (err.code === "ECONNREFUSED") {
      paymentCallErrors.inc({ error_type: "connection_refused" });
      console.error(`Payment SERVICE DOWN for order ${order.id}`);
    } else {
      paymentCallErrors.inc({ error_type: "unknown" });
      console.error(`Payment UNKNOWN ERROR for order ${order.id}: ${err.message}`);
    }
    order.status = "PAYMENT_FAILED";
  }

  ordersCreatedTotal.inc({ status: order.status });
  orders.set(order.id, order);
  res.status(201).json(order);
});

// Get all orders
app.get("/orders", (req, res) => {
  res.json(Array.from(orders.values()));
});

// Get order by ID
app.get("/orders/:id", (req, res) => {
  const order = orders.get(req.params.id);
  if (!order) return res.status(404).json({ error: "Order not found" });
  res.json(order);
});

app.listen(PORT, () => {
  console.log(`Order Service running on port ${PORT}`);
});
