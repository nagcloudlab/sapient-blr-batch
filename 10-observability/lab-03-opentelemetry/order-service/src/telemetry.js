const { NodeSDK } = require("@opentelemetry/sdk-node");
const { getNodeAutoInstrumentations } = require("@opentelemetry/auto-instrumentations-node");
const { OTLPTraceExporter } = require("@opentelemetry/exporter-trace-otlp-http");
const { OTLPMetricExporter } = require("@opentelemetry/exporter-metrics-otlp-http");
const { OTLPLogExporter } = require("@opentelemetry/exporter-logs-otlp-http");
const { Resource } = require("@opentelemetry/resources");
const { SEMRESATTRS_SERVICE_NAME } = require("@opentelemetry/semantic-conventions");
const { PeriodicExportingMetricReader } = require("@opentelemetry/sdk-metrics");
const { BatchLogRecordProcessor } = require("@opentelemetry/sdk-logs");

const OTEL_ENDPOINT =
  process.env.OTEL_EXPORTER_OTLP_ENDPOINT || "http://localhost:4318";

const resource = new Resource({
  [SEMRESATTRS_SERVICE_NAME]: "order-service",
});

// ---- TRACES ----
const traceExporter = new OTLPTraceExporter({
  url: `${OTEL_ENDPOINT}/v1/traces`,
});

// ---- METRICS ----
const metricExporter = new OTLPMetricExporter({
  url: `${OTEL_ENDPOINT}/v1/metrics`,
});

const metricReader = new PeriodicExportingMetricReader({
  exporter: metricExporter,
  exportIntervalMillis: 10000, // export every 10 seconds
});

// ---- LOGS ----
const logExporter = new OTLPLogExporter({
  url: `${OTEL_ENDPOINT}/v1/logs`,
});

const logProcessor = new BatchLogRecordProcessor(logExporter);

// ---- SDK (all 3 signals) ----
const sdk = new NodeSDK({
  resource,
  traceExporter,
  metricReader,
  logRecordProcessor: logProcessor,
  instrumentations: [
    getNodeAutoInstrumentations({
      "@opentelemetry/instrumentation-fs": { enabled: false },
    }),
  ],
});

sdk.start();
console.log("OpenTelemetry initialized: TRACES + METRICS + LOGS");

process.on("SIGTERM", () => sdk.shutdown());
