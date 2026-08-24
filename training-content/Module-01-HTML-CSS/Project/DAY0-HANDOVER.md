# Welcome to FoodExpress -- Your Application for the Next 43 Days

## The Scenario

You have just joined the **Sustain Engineering team** at Publicis Sapient.

A development team spent 6 months building **FoodExpress** -- a food delivery platform. They have now moved on to their next project.

**You are taking over.**

Your job: Keep it running. Fix bugs. Make improvements. Handle incidents. Deploy safely. Monitor health. Respond to the client.

---

## What is FoodExpress?

An online food delivery platform where customers can:

- Browse restaurants and their menus
- Search by cuisine, rating, and location
- Add items to a cart
- Place orders with payment
- Track delivery status in real time

---

## Architecture Overview

```
Browser / Mobile
       |
  React Frontend  (port 80)
       |
  +-----------+     +-----------+     +-----------+     +-----------+
  | Restaurant|     |   Cart    |     |   Order   |     | Delivery  |
  | Service   |     | Service   |     | Service   |     | Service   |
  | Node:3000 |     | Node:3001 |     | Java:8080 |     | Node:3002 |
  | MongoDB   |     | MongoDB   |     | MySQL     |     | MongoDB   |
  +-----------+     +-----------+     +-----------+     +-----------+
                                                              |
                                                     +-----------+
                                                     |  Payment  |
                                                     | Service   |
                                                     | Node:3003 |
                                                     | Ext. GW   |
                                                     +-----------+
```

---

## Services

| Service              | Technology              | Database         | Port | Purpose                                      |
|----------------------|-------------------------|------------------|------|----------------------------------------------|
| Frontend             | React + Bootstrap       | --               | 80   | Customer-facing UI                           |
| Restaurant Service   | Node.js + Express       | MongoDB          | 3000 | Restaurant listings, menus, search           |
| Cart Service         | Node.js + Express       | MongoDB          | 3001 | Cart management, item totals                 |
| Order Service        | Java + Spring Boot      | MySQL            | 8080 | Order creation, history, status updates      |
| Delivery Service     | Node.js + Express       | MongoDB          | 3002 | Driver assignment, delivery tracking         |
| Payment Service      | Node.js + Express       | External Gateway | 3003 | Payment processing, refunds                  |

---

## Current Status (from outgoing dev team)

- Application is **live** and serving customers
- Approximately 800 food orders per day
- Known issues exist (backlog attached below)
- No monitoring setup yet
- Deployments are currently manual
- No CI/CD pipeline in place
- Basic documentation exists but is incomplete

---

## Known Issues (Your Backlog)

1. Mobile UI has layout problems on the restaurant listing page
2. Cart has calculation bugs -- NaN totals appear, duplicate items are not merged
3. Restaurant search is case-sensitive (customers cannot find "Pizza" by typing "pizza")
4. Some API endpoints return 500 errors under load
5. "We think there is a memory issue somewhere but did not have time to investigate"
6. Database queries are getting slower as order data grows

---

## Your Team

Work in teams of 3-4 people. Over the next 43 days your team will rotate through these responsibilities:

| Responsibility   | Description                                                  |
|------------------|--------------------------------------------------------------|
| Bug Fixes        | Triage and resolve defects from the backlog                  |
| Enhancements     | Implement small improvements requested by the client         |
| Performance      | Identify and fix slow queries, memory leaks, bottlenecks     |
| Incidents        | Respond to production alerts and outages                     |
| Deployment       | Run release pipelines, manage rollbacks                      |
| Documentation    | Write runbooks, update API docs, maintain the wiki           |
| Monitoring       | Set up dashboards, alerts, and SLO tracking                  |

---

## Today's Task

1. Read this document thoroughly.
2. Discuss with your team: "What questions would you ask the outgoing dev team?"
3. Write down 5 questions you would want answered before they leave.
4. Set a personal goal: "By Day 43, I will be able to ___"

---

## Ground Rules

- **No ticket, no work** -- from Day 17 onwards, every task must have a Jira ticket.
- **No deploy without tests** -- from Day 14 onwards, all changes require passing tests before release.
- **Document everything** -- if you fixed it, write it down. If you deployed it, log it.
- **Ask for help early** -- struggling for 30 minutes or more? Ask your trainer or a peer.
