# Module 11: Node.js Capsule Project -- FoodExpress Restaurant Service

## Sustain Context

The client escalated:

> "The Restaurant Service we deployed is in critical state. The GET endpoint crashes with a 500, POST silently fails to persist data, the environment config is broken causing staging to hit prod DB, and we are missing two endpoints the mobile team needs. This is a full-day emergency sprint. Reproduce every issue, fix it, test via Postman, document root causes, and present to the team by end of day. We also need the MCQ results for Node.js competency sign-off."

---

## Tasks

| # | Ticket | Type | Issue | File(s) |
|---|--------|------|-------|---------|
| 1 | FOOD-31 | BUG | `GET /restaurants` returns 500 -- async/await missing on service call | `routes/restaurants.js`, `services/restaurantService.js` |
| 2 | FOOD-31b | BUG | Async errors bypass error handler middleware -- no try/catch or wrapper | `routes/restaurants.js` |
| 3 | FOOD-32 | BUG | `POST /restaurants` returns 201 but saves nothing -- parameter name mismatch in service | `services/restaurantService.js` |
| 4 | FOOD-32b | BUG | Validation middleware does not block invalid requests -- missing `return` | `middleware/validateRequest.js` |
| 5 | FOOD-34 | BUG | dotenv loaded too late -- `process.env` values are `undefined` at startup | `config/index.js`, `server.js` |
| 6 | FOOD-33a | FEATURE | Add `DELETE /api/restaurants/:id` soft-delete endpoint | `routes/restaurants.js`, `services/restaurantService.js` |
| 7 | FOOD-33b | FEATURE | Add `GET /api/restaurants/:id/menu` endpoint with category filter | `routes/restaurants.js`, `services/restaurantService.js` |

## Deliverables

- [ ] All 5 bugs fixed, 2 features added
- [ ] Each endpoint tested via Postman (screenshots or exported collection)
- [ ] Root-cause analysis document (2-3 sentences per bug)
- [ ] Team presentation (5-7 min) with live demo
- [ ] MCQ assessment completed (Modules 09-11)
