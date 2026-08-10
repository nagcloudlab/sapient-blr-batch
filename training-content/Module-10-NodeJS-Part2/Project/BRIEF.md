# Module 10: Node.js (Part 2) -- Express Routes and MongoDB Integration

## Sustain Context

The client escalated:

> "The Restaurant Service core is stable now but we need the API layer and database. The Express routes have issues -- wrong HTTP verbs, missing middleware, and routes in the wrong order. The MongoDB integration has query bugs and missing indexes that make search painfully slow. Half-day sprint to get this production-ready."

---

## Tasks

| # | Type | Issue | File |
|---|------|-------|------|
| 1 | BUG | `POST /restaurants` mapped as GET -- creates nothing | `routes/restaurants.js` |
| 2 | BUG | Missing `express.json()` middleware -- req.body is undefined | `server.js` |
| 3 | BUG | Catch-all route `/*` defined before specific routes -- everything returns 404 | `server.js` |
| 4 | BUG | MongoDB `find({ status: "active" })` returns nothing -- field is `isActive` | `services/restaurantService.js` |
| 5 | BUG | MongoDB `updateOne` uses `$push` instead of `$set` for updating restaurant name | `services/restaurantService.js` |
| 6 | ENH | Add Express API routes for restaurant CRUD and menu retrieval | `routes/restaurants.js` |
| 7 | ENH | Add MongoDB index on `cuisine` field for fast filtering | `db/setup.js` |

## Deliverables

- [ ] All 5 bugs fixed, 2 enhancements added
- [ ] API tested via Postman or curl
- [ ] MongoDB queries return correct results
- [ ] Brief root-cause notes for each bug
