# Module 11: Node.js Capsule -- Lab Setup

## Prerequisites

- Node.js 18 or higher (`node -v` to confirm)
- MongoDB 7.0 running locally
- curl or Postman

## Running the Starter Code

```bash
# Ensure MongoDB is running first
cd Labs/starter-code
npm install
npm start
```

Server starts on port 3000. This capsule brings together routing, middleware, validation, and error
handling -- bugs span multiple files.

## Verifying Your Fixes

Test the full CRUD cycle plus the specific features listed in `lab-exercises.md`:

```bash
# Full CRUD
curl -X POST http://localhost:3000/api/orders -H "Content-Type: application/json" \
  -d '{"customerId":"cust1","items":[{"menuItemId":"item1","qty":2}]}'
curl http://localhost:3000/api/orders
curl -X DELETE http://localhost:3000/api/orders/<id>

# Soft delete -- item should still appear with deleted:true flag
curl http://localhost:3000/api/orders/<id>
```

Validation test -- should return 400, not 500:
```bash
curl -X POST http://localhost:3000/api/orders -H "Content-Type: application/json" -d '{}'
```

## Expected Behavior

- Full CRUD operations work without unhandled exceptions.
- Invalid payloads return `400 Bad Request` with a descriptive message, not a `500`.
- Deleted records are soft-deleted (`deleted: true`) and excluded from list responses.
- Centralised error handler middleware catches all errors and formats them consistently.

## Troubleshooting

**Validation errors returning 500:** The validation middleware is not calling `next(err)` correctly --
ensure validation failures call `next` with a structured error object.

**Soft delete not working:** Check that the delete route sets `deleted: true` using `findByIdAndUpdate`
rather than `findByIdAndDelete`.
