# Gen-AI Prompt Engineering: Final Session

**Training:** Publicis Sapient Sustain Engineering — Day 46 (Final Session)
**Duration:** 3 hours | **Delivery:** Instructor-led demo | **Model:** GPT-4o
**Audience:** 27 developers who completed 45-day SRE training and used ChatGPT for capsule projects

## Philosophy

> "You've been driving a car for months. Today we open the hood."

## Setup (Instructor Only)

```bash
pip install openai
export OPENAI_API_KEY="your-key"
python3 setup_check.py
```

## Module Flow

### Part 1: Prompt Engineering Techniques (90 min)

| # | Module | File | Time | Key Concept | Teaching Tip |
|---|--------|------|------|-------------|--------------|
| 1 | The Gap | `01_the_gap.py` | 15m | Context is everything | Ask who's typed vague prompts |
| 2 | Prompt Anatomy | `02_prompt_anatomy.py` | 10m | 6-part framework | Write parts on whiteboard |
| 3 | System vs User | `03_system_vs_user.py` | 15m | System prompt = .env | The "aha" moment |
| 4 | Zero-Shot | `04_zero_shot.py` | 10m | Direct but limited | Bridge to few-shot |
| 5 | Few-Shot | `05_few_shot.py` | 10m | Teaching by example | Compare with zero-shot |
| 6 | Chain-of-Thought | `06_chain_of_thought.py` | 15m | Show your reasoning | PR review analogy |
| 7 | Self-Consistency | `07_self_consistency.py` | 10m | AI is probabilistic | Temperature demo |

### Part 2: Production Patterns (45 min)

| # | Module | File | Time | Key Concept | Teaching Tip |
|---|--------|------|------|-------------|--------------|
| 8 | Structured Output | `08_structured_output.py` | 15m | JSON for pipelines | ServiceNow connection |
| 9 | Prompt Chaining | `09_prompt_chaining.py` | 15m | Microservices for AI | Their favorite analogy |
| 10 | Incident Responder | `10_incident_responder.py` | 15m | All techniques combined | Go slow — climax |

### Part 3: Trust & Verification (20 min)

| # | Module | File | Time | Key Concept | Teaching Tip |
|---|--------|------|------|-------------|--------------|
| 11 | Hallucination Lab | `11_hallucination_lab.py` | 15m | AI lies confidently | Uses BOTH GPT-4o + mini |
| 12 | Capstone Challenge | `12_capstone_challenge.py` | 5m | Skill is in the question | Quick scoring exercise |

### Part 4: Advanced — AI in Your Daily Work (30 min)

| # | Module | File | Time | Key Concept | Teaching Tip |
|---|--------|------|------|-------------|--------------|
| 13 | AI Code Reviewer | `13_ai_code_reviewer.py` | 10m | YOUR rubric, YOUR standards | Mirrors their capsule reviews |
| 14 | AI Test Generator | `14_ai_test_generator.py` | 10m | AI types, you think | Connects to QE/QC training |
| 15 | AI Post-Mortem | `15_ai_postmortem.py` | 10m | Incident to document in 60s | Connects SRE + ITSM + comms |

### Part 5: RAG, DevOps & Toolkit (45 min)

| # | Module | File | Time | Key Concept | Teaching Tip |
|---|--------|------|------|-------------|--------------|
| 16 | RAG: Your Knowledge | `16_rag_runbook.py` | 15m | Inject YOUR docs into AI | The "enterprise AI" moment |
| 17 | DevOps with Gen-AI | `17_devops_genai.py` | 15m | App spec -> entire infra stack | Grand finale |
| 18 | Prompt Library | `18_prompt_library.py` | 15m | Copy-paste templates for daily work | They walk away with this |
| 19 | MCP: AI + Systems | `19_mcp_demo.py` | 15m | Connect AI to live production systems | The "future of SRE" moment |
| 20 | AI Agents | `20_ai_agents.py` | 15m | Autonomous Think->Act->Observe loop | The grand finale of the journey |

**Total: ~3.5 hours** (with discussion time at each pause)

## Running

```bash
python3 01_the_gap.py        # Start here, run sequentially
python3 02_prompt_anatomy.py
# ... through ...
python3 17_devops_genai.py
```

Press ENTER between demos — built-in pauses with teaching tips.

## Story Arc

```
Modules 1-7:   TECHNIQUES    — How to talk to AI effectively
Modules 8-9:   PATTERNS      — How AI fits into production systems
Module 10:     CLIMAX        — Everything combined into one SRE workflow
Module 11:     PLOT TWIST    — AI fails spectacularly (trust but verify)
Module 12:     CHALLENGE     — Students prove their skills
Modules 13-15: DAILY WORK    — AI for code review, testing, post-mortems
Module 16:     ENTERPRISE    — RAG: inject YOUR knowledge into AI
Module 17:     GRAND FINALE  — DevOps: app spec -> full infra stack
Module 18:     TAKEAWAY      — Prompt library: copy-paste templates for daily work
Module 19:     THE FUTURE    — MCP: connect AI directly to production systems
Module 20:     GRAND FINALE  — AI Agents: autonomous Think->Act->Observe
```

## Key Design

- **Single model (GPT-4o)** for all modules except Module 11
- **Module 11 uses GPT-4o + GPT-4o-mini** to compare hallucination behavior
- **Teaching tips** built into every pause point
- **Teaching points** highlight what to emphasize after each demo
- All examples use their capsule project domain (Spring Boot + MongoDB + Docker + K8s + ServiceNow)
- Advanced modules (13-15) directly mirror their 45-day training activities
