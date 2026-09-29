# Phase 2: The Journey
## Enhance the UPI Service: Frontend -> Backend -> DB -> Tests -> DevOps

Each step revisits a skill you learnt in the 44-day programme -- now supercharged with AI. At every step, AI helps -- and at every step, you'll see where HUMAN judgment is still essential.

---

## 2.1 Frontend Enhancement (Week 1-2: HTML, CSS, JavaScript)

### Concept: AI Code Generation + AI Tools Landscape

```
The dashboard is basic. Rebuild it as a multi-page SSR app with Express routing:

1. Server-side routes (each renders the same EJS template with a `page` variable):
   - GET /          --> home (card grid linking to other pages)
   - GET /pay       --> send money form
   - GET /balance   --> check balance form
   - GET /transactions --> live transaction table with auto-refresh
   - GET /history   --> per-account transaction history with running balance
   - GET /rag       --> RAG search page (separate EJS file)

2. Apple-style light theme:
   - White cards on #f5f5f7 background, 18px rounded corners
   - Frosted glass navbar with backdrop blur, active page highlighted
   - System font stack (-apple-system, SF Pro)
   - Status badges: green for success, red for failed, amber for pending
   - Transaction table with Txn ID column
   - Amount in Indian format (Rs 1,500.00)

3. Each page shows only its own content (no scrolling past other sections)

4. JavaScript (no page reloads within a page):
   - Pay form: fetch() to POST /api/pay, toast notifications
   - Transactions: auto-refresh every 3 seconds via fetch + DOM update
   - History: select account, view filtered transactions with running balance
   - Refund button on successful transactions
```

After generation, restart the server and test in the browser.

### AI Tools -- When to Use Which

```
Typing code line by line?         --> GitHub Copilot (inline autocomplete)
Need explanation or design help?  --> ChatGPT / Claude.ai (chat)
Multi-file project, refactoring?  --> Claude Code (terminal agent)
AI-native IDE experience?         --> Cursor / Windsurf
Quick UI prototype?               --> v0.dev / Bolt
AWS / GCP specific?               --> Amazon Q / Gemini Code Assist
```

Key difference:
- **Assistant** (ChatGPT) -- you copy-paste AI's response
- **Agent** (Claude Code) -- AI reads files, writes code, runs tests

> **HUMAN + AI:** AI generates a dashboard in 30 seconds. But did it use `addEventListener` or inline `onclick`? AI optimizes for "looks right", not "best practice".

---

## 2.2 Backend + AI API Integration (Week 3-4: Java, Node.js)

### Concept: System Prompts + Building with AI APIs + Temperature

```
Add a new feature to the UPI service:

POST /api/txn/:txnId/explain
- Takes a transaction's data (amount, status, timestamps, payer VPA, payee VPA)
- Calls the Anthropic API (Claude) to generate a human-friendly explanation
- Like Google Pay's "Payment to Priya was successful" but more detailed

Example response:
"Your payment of Rs 500.00 to priya@paytm for 'Lunch split' was completed
successfully at 2:15 PM. The amount has been debited from your account
rahul@ybl. Transaction reference: TXN1695900001234."

Implementation requirements:
- Use @anthropic-ai/sdk package
- API key from environment variable ANTHROPIC_API_KEY (never hardcode)
- System prompt: "You are a UPI payment assistant. Generate clear, friendly
  transaction explanations in 1-2 sentences. Use Indian Rupee format (Rs).
  Never reveal internal system details or other users' data."
- temperature: 0.3 (factual, not creative)
- max_tokens: 150 (short responses)
- Fallback: if API fails, return a simple template-based message
- Add comments explaining WHY each parameter is set the way it is
```

### Understanding the Generated Code

- `process.env.ANTHROPIC_API_KEY` -- **never hardcode**, env vars only
- `system: "You are a UPI..."` -- **system prompt** controls personality, rules, boundaries
- `temperature: 0.3` -- low = factual, consistent. Financial text = same answer every time
- `max_tokens: 150` -- controls cost + prevents rambling. ~2 sentences
- `try/catch + fallback` -- AI APIs **will** go down. Always have a non-AI fallback
- Output validation -- what if AI mentions another customer's name? Validate first

### Anatomy of a Good System Prompt

```
"You are a UPI payment assistant.        <-- ROLE
 Generate clear, friendly explanations   <-- TASK
 in 1-2 sentences.                       <-- FORMAT
 Use Indian Rupee format (Rs).           <-- CONSTRAINT
 Never reveal internal system details    <-- BOUNDARY
 or other users' data."                  <-- SAFETY
```

Test it:

```bash
# Make a payment first
curl -X POST http://localhost:3000/api/pay \
  -H "Content-Type: application/json" \
  -d '{"payer_vpa":"rahul@ybl","payee_vpa":"priya@paytm","amount":500,"note":"Lunch split"}'

# Wait 3 seconds, then explain (replace TXN_ID with actual ID from above)
curl -X POST http://localhost:3000/api/txn/TXN_ID/explain
```

> **HUMAN + AI:** AI writes the integration. But WHO chose the system prompt? WHO decided temperature 0.3? WHO designed the fallback? You. The API is the engine, you're the architect.

---

## 2.3 Database -- Natural Language to SQL (Week 3: SQL, MongoDB)

### Concept: NL-to-SQL + Hallucination

```
Write SQL queries for these business questions about our UPI transaction database.

Schema (SQLite):
- transactions: txn_id TEXT, payer_vpa TEXT, payee_vpa TEXT, amount REAL,
  note TEXT, status TEXT (SUCCESS/FAILED/PENDING/PROCESSING/REFUNDED),
  type TEXT (PAYMENT/REFUND), created_at TEXT, updated_at TEXT
- accounts: vpa TEXT, name TEXT, balance REAL

Queries needed:
1. Top 5 payees by total amount received this month
2. Hourly transaction volume for capacity planning (group by hour of day)
3. Failed transaction rate by hour (to detect outage patterns)
4. Average transaction amount by bank (extract bank from VPA: user@BANK)
5. Find potential fraud: accounts with more than 5 failed transactions in 1 hour
6. Settlement report: net amount per VPA (received minus sent) for today
```

### Critical Review -- Finding Hallucinations

Check the AI-generated queries for:

- **Top 5 payees** -- is the date filter correct for SQLite?
- **Hourly volume** -- what timezone? AI defaults to UTC, India is IST (+5:30)
- **Bank extraction** -- what if a VPA has no `@`? Silent failure
- **Fraud detection** -- is the "1 hour" window timezone-aware?
- **Settlement** -- did it include or exclude refunded transactions?

### Why AI Hallucinates on Queries

- No access to your actual data or date formats
- Guesses column names (often right -- which is DANGEROUS)
- Assumes UTC (you're in IST)
- Doesn't know your business rules
- "Syntactically correct" != "Logically correct"

**Defense:**
- Always provide your exact schema
- Specify timezone
- Test on staging, NEVER production
- Restrict to SELECT only

> **HUMAN + AI:** Confident, syntactically correct SQL that gives WRONG results. In fintech, wrong queries = wrong money.

---

## 2.4 Testing (Week 4: QE/QC, Jest, Postman)

### Concept: AI Test Generation + Trust Matrix

```
Write comprehensive tests for the UPI Transaction Service using Jest + supertest.

Create tests/api.test.js with these categories:

1. POST /api/pay -- Happy path
   - Valid payment, verify balance debit/credit, verify txn record created

2. POST /api/pay -- Validation errors
   - Missing fields, invalid VPA format, amount <= 0, amount > 100000
   - Same payer and payee, insufficient balance

3. GET /api/txn/:txnId -- Status check
   - Valid txn returns correct data, non-existent returns 404

4. POST /api/refund/:txnId -- Refund
   - Successful refund, double refund prevented, cannot refund failed txn

5. Security tests
   - SQL injection in VPA: "rahul@ybl'; DROP TABLE accounts;--"
   - XSS in note: "<script>alert('xss')</script>"
   - Integer overflow in amount

Setup: fresh database before each test. Teardown after.
```

Run the tests. Some pass, some fail. Each failure is a learning moment:
- Failing + code is wrong = AI **exposed** a bug
- Failing + wrong assertion = AI **assumed** ideal behavior, not actual

### Trust Matrix -- When to Trust AI Output

The question isn't "can AI do this?" It's "what happens if AI gets it WRONG?"

```
HIGH TRUST (use after quick scan):
  [x] Test generation         -- Wrong test = harmless
  [x] Boilerplate CRUD        -- Structural, easy to verify
  [x] Documentation, README   -- Low risk if slightly wrong
  [x] .gitignore, configs     -- Standard patterns

MEDIUM TRUST (always review carefully):
  [~] Business logic          -- Payment calculations, status transitions
  [~] Database queries        -- Timezone, edge cases, PII
  [~] Docker / K8s YAML       -- Architecture assumptions
  [~] CI/CD pipeline config   -- Credentials, environments

LOW TRUST (starting point ONLY):
  [!] Security code           -- Wrong auth = breach
  [!] Financial calculations  -- Wrong amount = money lost
  [!] Compliance / regulatory -- Wrong NPCI rule = fine
  [!] Production diagnosis    -- Missing YOUR system context
  [!] Infrastructure / IAM    -- Wrong permissions = security hole
```

> **HUMAN + AI:** AI generated 20+ tests in 30 seconds. But it tested what SHOULD happen, not what DOES happen.

---

## 2.5 DevOps Pipeline (Week 6-8: Git, Docker, Jenkins, K8s, Ansible)

### Concept: AI in DevOps + AI Limitations

```
Generate the complete deployment pipeline for this UPI Service:

1. Dockerfile -- Multi-stage build, Node 18 Alpine, non-root user, health check
2. docker-compose.yml -- App with volume mount for SQLite persistence
3. Jenkinsfile -- Lint, Test, Build Image, Push, Deploy stages
4. k8s/deployment.yaml -- 3 replicas, resource limits, readiness/liveness probes
5. k8s/service.yaml -- ClusterIP service on port 3000
6. ansible/deploy.yml -- Deploy to a fresh Ubuntu server
7. .dockerignore
8. .github/workflows/ci.yml -- GitHub Actions workflow
```

### Review Checklist

- **Dockerfile** -- `node:18-alpine` or just `node:18`? (alpine = 10x smaller)
- **docker-compose** -- volume for SQLite data? (otherwise data lost on restart)
- **Jenkinsfile** -- credentials hardcoded or parameterized?
- **K8s deployment** -- resource limits realistic? (AI picks 256Mi, doesn't know your load)
- **K8s deployment** -- namespace specified? (defaults to 'default')
- **Ansible** -- uses `apt` or `yum`? (AI guessed your OS)

### The Architecture Flaw AI Won't Catch

Look at the K8s deployment: **3 replicas with SQLite.**

- SQLite = file-based, single-writer database
- 3 K8s replicas = 3 separate SQLite files
- User pays Rs 500 via Pod 1 -- Pod 2 and Pod 3 don't see it
- Balance is wrong. Money disappears.

AI generated **PERFECT YAML** that would **BREAK the entire payment system**.

### AI in the DevOps Pipeline

```
CODE --> BUILD --> TEST --> DEPLOY --> MONITOR
  |       |        |        |          |
  AI      AI       AI       AI         AI
  |       |        |        |          |
HUMAN   HUMAN    HUMAN    HUMAN      HUMAN
```

### The 80/20 Rule

- AI handles 80% -- boilerplate, file structure, syntax, common patterns
- You handle 20% -- architecture, distributed state, capacity, compliance

> **HUMAN + AI:** That 20% is where the engineer earns their salary.

The UPI service is built, enhanced, tested, and pipeline-ready. In Phase 3, it goes to production -- and things break.

---

## Phase 2 Concepts

| # | Concept |
|---|---------|
| 9 | AI Tools Landscape (Copilot vs Claude Code vs ChatGPT vs Cursor) |
| 10 | AI Code Generation (Frontend + Backend) |
| 11 | System Prompts (anatomy and best practices) |
| 12 | Building with AI APIs (Anthropic SDK) |
| 13 | Temperature & Sampling |
| 14 | NL-to-SQL |
| 15 | Hallucination (live proof with database queries) |
| 16 | Trust Matrix (High / Medium / Low) |
| 17 | AI Test Generation |
| 18 | AI in DevOps Pipeline |
| 19 | AI Limitations -- the 80/20 rule |
