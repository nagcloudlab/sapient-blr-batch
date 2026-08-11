const http = require('http');

// ─── Configuration ───
const TOTAL_REQUESTS = 500;
const CONCURRENCY = 50;

async function runLoadTest(url, label) {
  const latencies = [];
  let completed = 0;
  let errors = 0;

  const start = Date.now();

  function makeRequest() {
    return new Promise((resolve) => {
      const reqStart = Date.now();
      const req = http.get(url, (res) => {
        let body = '';
        res.on('data', (chunk) => (body += chunk));
        res.on('end', () => {
          latencies.push(Date.now() - reqStart);
          completed++;
          resolve();
        });
      });
      req.on('error', () => {
        errors++;
        completed++;
        resolve();
      });
      req.setTimeout(10000, () => {
        errors++;
        completed++;
        req.destroy();
        resolve();
      });
    });
  }

  // Run requests with controlled concurrency
  const queue = [];
  for (let i = 0; i < TOTAL_REQUESTS; i++) {
    queue.push(makeRequest());
    // Limit in-flight requests
    if (queue.length >= CONCURRENCY) {
      await Promise.race(queue);
      // Remove settled promises
      for (let j = queue.length - 1; j >= 0; j--) {
        const status = await Promise.race([queue[j].then(() => 'done'), Promise.resolve('pending')]);
        if (status === 'done') queue.splice(j, 1);
      }
    }
  }
  await Promise.all(queue);

  const totalTime = Date.now() - start;
  latencies.sort((a, b) => a - b);

  const avg = latencies.reduce((s, v) => s + v, 0) / latencies.length;
  const p50 = latencies[Math.floor(latencies.length * 0.5)];
  const p95 = latencies[Math.floor(latencies.length * 0.95)];
  const p99 = latencies[Math.floor(latencies.length * 0.99)];
  const min = latencies[0];
  const max = latencies[latencies.length - 1];
  const throughput = ((completed - errors) / (totalTime / 1000)).toFixed(1);

  return { label, totalTime, completed, errors, avg, p50, p95, p99, min, max, throughput };
}

function printResults(r) {
  console.log(`\n${'='.repeat(55)}`);
  console.log(`  ${r.label}`);
  console.log(`${'='.repeat(55)}`);
  console.log(`  Total requests  : ${r.completed}`);
  console.log(`  Errors          : ${r.errors}`);
  console.log(`  Total time      : ${r.totalTime} ms`);
  console.log(`  Throughput      : ${r.throughput} req/sec`);
  console.log(`  ─────────────────────────────────────`);
  console.log(`  Latency (ms):`);
  console.log(`    Min           : ${r.min}`);
  console.log(`    Avg           : ${r.avg.toFixed(1)}`);
  console.log(`    P50 (median)  : ${r.p50}`);
  console.log(`    P95           : ${r.p95}`);
  console.log(`    P99           : ${r.p99}`);
  console.log(`    Max           : ${r.max}`);
}

function printComparison(blocking, nonBlocking) {
  console.log(`\n${'='.repeat(55)}`);
  console.log(`  COMPARISON SUMMARY`);
  console.log(`${'='.repeat(55)}`);
  const throughputRatio = (nonBlocking.throughput / blocking.throughput).toFixed(2);
  const latencyRatio = (blocking.avg / nonBlocking.avg).toFixed(2);
  console.log(`  Throughput gain  : ${throughputRatio}x  (non-blocking is faster)`);
  console.log(`  Avg latency diff : ${latencyRatio}x  (blocking is slower)`);
  console.log(`  P95 blocking     : ${blocking.p95} ms`);
  console.log(`  P95 non-blocking : ${nonBlocking.p95} ms`);
  console.log(`${'='.repeat(55)}`);
  console.log(`\n  Conclusion: Non-blocking I/O handles concurrent`);
  console.log(`  requests far better because it doesn't hold up`);
  console.log(`  the event loop while waiting for file I/O.\n`);
}

async function main() {
  console.log(`\nLoad Test: ${TOTAL_REQUESTS} requests, ${CONCURRENCY} concurrent\n`);

  // Warm up
  console.log('Warming up blocking server...');
  await runLoadTest('http://localhost:3001/api/products', 'warmup');

  console.log('Warming up non-blocking server...');
  await runLoadTest('http://localhost:3002/api/products', 'warmup');

  // Actual tests
  console.log('\nRunning blocking server load test...');
  const blocking = await runLoadTest('http://localhost:3001/api/products', 'BLOCKING SERVER (port 3001)');

  console.log('Running non-blocking server load test...');
  const nonBlocking = await runLoadTest('http://localhost:3002/api/products', 'NON-BLOCKING SERVER (port 3002)');

  printResults(blocking);
  printResults(nonBlocking);
  printComparison(blocking, nonBlocking);
}

main().catch(console.error);
