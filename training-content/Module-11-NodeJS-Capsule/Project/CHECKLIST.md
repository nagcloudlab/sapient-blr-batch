# Module 11 Checklist -- Participant Submission

## Bug Fixes
- [ ] Bug #1: `GET /api/restaurants` returns 200 with restaurant array (async/await added)
- [ ] Bug #2: Async errors are caught and forwarded to error handler middleware
- [ ] Bug #3: `POST /api/restaurants` creates a document in MongoDB (parameter name fixed)
- [ ] Bug #4: Invalid POST requests return 400 with error details (validation return added)
- [ ] Bug #5: `.env` values are loaded before `process.env` is accessed

## Feature Additions
- [ ] `DELETE /api/restaurants/:id` soft-deletes (sets `isActive: false`)
- [ ] Deactivated restaurants do not appear in GET listing
- [ ] `GET /api/restaurants/:id/menu` returns menu array
- [ ] Menu endpoint supports `?category=` filter
- [ ] Non-existent restaurant returns 404 for both new endpoints

## Testing Evidence
- [ ] All 7 endpoints tested via Postman or curl
- [ ] Postman collection exported or screenshots attached
- [ ] Edge cases tested: invalid ID, missing fields, empty body

## Presentation
- [ ] Root-cause analysis documented for each bug (2-3 sentences)
- [ ] Live demo prepared showing all endpoints
- [ ] Team presentation delivered (5-7 minutes)

## MCQ Assessment
- [ ] MCQ completed covering Modules 09-11

## Self-Check Questions
1. Why does Express not catch errors thrown inside `async` route handlers automatically?
2. What is the difference between `deleteOne()` and soft-delete in a production system?
3. Why must `dotenv.config()` be called before any `process.env` access?
4. What HTTP status code should a create endpoint return, and why?
5. How does Express identify an error-handling middleware function?
6. What is the risk of using variable name `data` when the parameter is `restaurantData`?
