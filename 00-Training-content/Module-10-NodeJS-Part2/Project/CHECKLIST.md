# Module 10 Checklist -- Participant Submission

## Bug Fixes
- [ ] Bug #1: `POST /api/restaurants` creates a new restaurant (not mapped as GET)
- [ ] Bug #2: `req.body` contains parsed JSON in POST/PUT handlers
- [ ] Bug #3: Specific routes respond correctly (catch-all only triggers for unknown paths)
- [ ] Bug #4: Active restaurant query returns results (correct field name)
- [ ] Bug #5: Update restaurant name uses `$set` (not `$push`)

## Enhancements
- [ ] CRUD routes working: GET list, GET by ID, POST create, PUT update, DELETE
- [ ] MongoDB index created on `cuisine` field
- [ ] Filtered query `GET /api/restaurants?cuisine=Italian` uses the index

## Testing Evidence
- [ ] API tested via Postman or curl (screenshots or exported collection)
- [ ] MongoDB queries verified in shell or Compass

## Self-Check Questions
1. Why does Express route order matter?
2. What does `express.json()` middleware do internally?
3. What is the difference between `$set` and `$push` in MongoDB?
4. When should you add an index to a MongoDB collection?
5. What HTTP status codes should CREATE, UPDATE, and DELETE return?
