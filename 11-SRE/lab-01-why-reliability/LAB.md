# Lab 01: Why Reliability Matters

## Objective

Experience what happens when a service is unreliable. You'll generate traffic to a
real service, watch it fail, and understand the business impact of poor reliability.

---

## Part 1: Start the Services

Start the order-service and payment-service stack.

```bash
cd ../services
docker compose up -d --build
```

Verify everything is running:
```bash
curl http://localhost:3000/health
curl http://localhost:8080/health
```

---

## Part 2: The Happy Path

Place a few orders manually:

```bash
# Place an order
curl -s -X POST http://localhost:3000/orders \
  -H "Content-Type: application/json" \
  -d '{"item": "Biryani", "quantity": 2, "price": 350}' | jq .
```

Do this 5 times. Note how many succeed vs fail. The payment service has built-in
random failures (5% errors, 5% slow, 10% declined).

**Question for the class:** If 1 in 4 orders fails, would you keep using this app?

---

## Part 3: Generate Real Traffic

Run the load generator to simulate 100 customers ordering food:

```bash
# Generate 100 orders rapidly
for i in $(seq 1 100); do
  curl -s -X POST http://localhost:3000/orders \
    -H "Content-Type: application/json" \
    -d "{\"item\": \"Biryani\", \"quantity\": $((RANDOM % 5 + 1)), \"price\": 350}" \
    -o /dev/null -w "Order $i: HTTP %{http_code} in %{time_total}s\n" &
done
wait
echo "--- All 100 orders sent ---"
```

Now check the results:

```bash
# How many orders were created?
curl -s http://localhost:3000/orders | jq length

# How many CONFIRMED vs PAYMENT_FAILED?
curl -s http://localhost:3000/orders | jq '[group_by(.status)[] | {status: .[0].status, count: length}]'
```

---

## Part 4: Calculate the Business Impact

Fill in this table based on your results:

```
+------------------------------------------+------------------+
| Metric                                   | Your Value       |
+------------------------------------------+------------------+
| Total orders sent                        | 100              |
| Orders CONFIRMED                         | ____             |
| Orders PAYMENT_FAILED                    | ____             |
| Success rate (%)                         | ____             |
| Average order value (INR)                | ____             |
| Revenue lost to failures (INR)           | ____             |
| If this runs 24/7, daily revenue loss    | ____             |
+------------------------------------------+------------------+
```

### Discussion Questions

1. **What caused the failures?** (Look at docker logs)
   ```bash
   cd ../services && docker compose logs payment-service 2>&1 | grep -E "ERROR|DECLINED|TIMEOUT" | tail -20
   ```

2. **Is it acceptable to lose 25% of orders?** What percentage would be acceptable?

3. **How do you even know there's a problem?** Without monitoring, would you know
   orders are failing right now?

4. **Who decides what "reliable enough" means?** The developer? The business? The user?

---

## Key Takeaways

```
Problem                          SRE Solution (upcoming labs)
─────────────────────────────    ──────────────────────────────
"How unreliable are we?"     --> SLIs (Lab 02)
"How reliable should we be?" --> SLOs (Lab 02)
"How much failure is OK?"    --> Error Budgets (Lab 03)
"How do we detect failure?"  --> Monitoring & Alerting (Lab 04)
"What do we do when it fails?"--> Incident Response (Lab 05)
"How do we prevent repeats?" --> Post-Mortems (Lab 06)
"How do we reduce manual work?"--> Toil Reduction (Lab 07)
"How do we test resilience?" --> Chaos Engineering (Lab 08)
```

> **Core SRE insight:** 100% reliability is impossible AND undesirable.
> The question isn't "will it fail?" but "how much failure can we tolerate?"

---

## Cleanup

Don't stop the services -- we'll use them in the next lab.
