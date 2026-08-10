# Module 10: Node.js Part 2 -- Lab Setup

## Prerequisites

- Node.js 18 or higher (`node -v` to confirm)
- MongoDB 7.0 running locally (`mongod --version` to confirm)
- curl or Postman

## Running the Starter Code

```bash
# Start MongoDB (if not running as a service)
mongod --dbpath /data/db

# In a second terminal
cd Labs/starter-code
npm install
npm start
```

The server connects to MongoDB on `mongodb://localhost:27017/foodexpress` by default.

## Verifying Your Fixes

```bash
# List restaurants
curl http://localhost:3000/api/restaurants

# Create a restaurant
curl -X POST http://localhost:3000/api/restaurants \
  -H "Content-Type: application/json" \
  -d '{"name":"Burger Hub","cuisine":"American","rating":4.2}'

# Update a restaurant (replace <id> with a real _id from the list)
curl -X PUT http://localhost:3000/api/restaurants/<id> \
  -H "Content-Type: application/json" \
  -d '{"rating":4.5}'
```

## Expected Behavior

- `GET /api/restaurants` returns a JSON array (empty array if no data yet, not an error).
- `POST` creates a document and returns `201` with the new document including its `_id`.
- `PUT` updates the specified document and returns the updated version.
- `DELETE` removes the document and returns `204 No Content`.
- Connection errors are logged to the console, not swallowed silently.

## Troubleshooting

**`MongoServerError: connect ECONNREFUSED`:** MongoDB is not running. Start `mongod` in a separate
terminal before starting the app.

**Route returns `404` for valid paths:** Check that the Express router file is imported and mounted
in `app.js` with the correct base path (e.g., `app.use('/api/restaurants', restaurantRouter)`).
