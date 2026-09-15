const express = require("express");
const axios = require("axios");
const { v4: uuidv4 } = require("uuid");
const winston = require("winston");

// ---- Structured Logger ----
const logger = winston.createLogger({
  level: "info",
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: { service: "order-service" },
  transports: [new winston.transports.Console()],
});

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;
const PAYMENT_SERVICE_URL =
  process.env.PAYMENT_SERVICE_URL || "http://localhost:8080";

const orders = new Map();

// Request logging middleware
app.use((req, res, next) => {
  const start = Date.now();
  res.on("finish", () => {
    const duration = Date.now() - start;
    const logData = {
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration,
    };
    if (res.statusCode >= 500) {
      logger.error("HTTP Request", logData);
    } else if (res.statusCode >= 400) {
      logger.warn("HTTP Request", logData);
    } else {
      logger.info("HTTP Request", logData);
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
    logger.warn("Invalid order request - missing fields", {
      hasItem: !!item,
      hasQuantity: !!quantity,
      hasPrice: !!price,
      body: req.body,
    });
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

  logger.info("Order created", {
    orderId: order.id,
    item,
    quantity,
    totalAmount: order.totalAmount,
  });

  try {
    const paymentResponse = await axios.post(
      `${PAYMENT_SERVICE_URL}/payments`,
      { orderId: order.id, amount: order.totalAmount },
      { timeout: 5000 }
    );

    order.paymentId = paymentResponse.data.id;
    order.status = paymentResponse.data.status === "COMPLETED" ? "CONFIRMED" : "PAYMENT_FAILED";

    if (order.status === "CONFIRMED") {
      logger.info("Payment successful", {
        orderId: order.id,
        paymentId: order.paymentId,
        amount: order.totalAmount,
      });
    } else {
      logger.warn("Payment declined", {
        orderId: order.id,
        paymentId: order.paymentId,
        paymentStatus: paymentResponse.data.status,
        amount: order.totalAmount,
      });
    }
  } catch (err) {
    order.status = "PAYMENT_FAILED";

    if (err.code === "ECONNABORTED") {
      logger.error("Payment service TIMEOUT", {
        orderId: order.id,
        timeout: 5000,
        error: err.message,
      });
    } else if (err.response?.status === 500) {
      logger.error("Payment service INTERNAL ERROR", {
        orderId: order.id,
        statusCode: 500,
        error: err.message,
      });
    } else if (err.code === "ECONNREFUSED") {
      logger.error("Payment service UNREACHABLE", {
        orderId: order.id,
        error: "Connection refused - service may be down",
      });
    } else {
      logger.error("Payment service call failed", {
        orderId: order.id,
        error: err.message,
        statusCode: err.response?.status,
      });
    }
  }

  orders.set(order.id, order);
  res.status(201).json(order);
});

app.get("/orders", (req, res) => {
  res.json(Array.from(orders.values()));
});

app.get("/orders/:id", (req, res) => {
  const order = orders.get(req.params.id);
  if (!order) {
    logger.warn("Order not found", { orderId: req.params.id });
    return res.status(404).json({ error: "Order not found" });
  }
  res.json(order);
});

app.listen(PORT, () => {
  logger.info("Server started", { port: PORT });
});
