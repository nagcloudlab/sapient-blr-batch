# QuickTicket Event Booking API

A Node.js REST API for event booking built with Express and MongoDB.

## Prerequisites

- **Node.js** (v18 or above) - should already be installed
- **MongoDB** (setup instructions below)

---

## Step 1: Setup MongoDB (No Admin Rights Required)

Since you don't have admin rights, we'll use **MongoDB as a standalone binary** (no installation needed).

### Download MongoDB Community Server

1. Go to: https://www.mongodb.com/try/download/community
2. Select:
   - **Version:** 8.0 (latest)
   - **Platform:** Windows x64
   - **Package:** ZIP
3. Click **Download** (choose the `.zip` option, NOT the `.msi` installer)

### Extract and Setup

1. Extract the downloaded ZIP file to a folder, e.g., `C:\Users\<your-username>\mongodb`
2. Inside the extracted folder, find the `bin` directory containing `mongod.exe` and `mongos.exe`
3. Create a folder for your database data:
   ```cmd
   mkdir C:\Users\<your-username>\mongodb-data
   ```

### Download MongoDB Shell (mongosh)

1. Go to: https://www.mongodb.com/try/download/shell
2. Select **Windows x64 ZIP** and download
3. Extract and copy `mongosh.exe` into your `C:\Users\<your-username>\mongodb\bin` folder

### Start MongoDB Server

Open a **Command Prompt** (not PowerShell) and run:

```cmd
C:\Users\<your-username>\mongodb\bin\mongod.exe --dbpath C:\Users\<your-username>\mongodb-data
```

> **Keep this terminal open** - MongoDB needs to keep running while you work.

You should see a message ending with something like:
```
Waiting for connections
```

### Verify MongoDB is Running (Optional)

Open a **second terminal** and run:

```cmd
C:\Users\<your-username>\mongodb\bin\mongosh.exe
```

If you see the `test>` prompt, MongoDB is working. Type `exit` to close.

---

## Step 2: Setup the Node.js Application

Open a **new terminal** (keep MongoDB running in the other one) and navigate to the starter-code folder:

```cmd
cd path-to-starter-code
```

### Install Dependencies

```cmd
npm install
```

### Start the Application

```cmd
npm start
```

You should see:
```
QuickTicket API running on port 3000
Connected to MongoDB
```

> If you see a MongoDB connection error, make sure `mongod` is running in the other terminal.

---

## Step 3: Seed Sample Data

Open another terminal and run mongosh, then paste:

```cmd
C:\Users\<your-username>\mongodb\bin\mongosh.exe
```

Once you see the `test>` prompt, paste the following:

```js
use quickticket

db.events.insertMany([
  { name: "Rock Fest 2026", description: "Annual rock music festival", category: "concert", date: new Date("2026-09-15"), venue: "Palace Grounds", price: 1500, capacity: 5000, availableSeats: 3200 },
  { name: "IPL Final", description: "Cricket league final match", category: "sports", date: new Date("2026-10-01"), venue: "Chinnaswamy Stadium", price: 2500, capacity: 40000, availableSeats: 5000 },
  { name: "Shakespeare Live", description: "Hamlet performed live", category: "theatre", date: new Date("2026-09-20"), venue: "Ranga Shankara", price: 800, capacity: 300, availableSeats: 150 },
  { name: "Tech Summit 2026", description: "Developer conference", category: "conference", date: new Date("2026-11-05"), venue: "NIMHANS Convention Centre", price: 3000, capacity: 2000, availableSeats: 1200 },
  { name: "Dussehra Mela", description: "Cultural festival", category: "festival", date: new Date("2026-10-10"), venue: "Lalbagh", price: 0, capacity: 10000, availableSeats: 8000 }
])
```

---

## Step 4: Test the API

Use **Postman**, **curl**, or any REST client.

### Register a User

```
POST http://localhost:3000/api/auth/register
Content-Type: application/json

{
  "name": "Test User",
  "email": "test@example.com",
  "password": "password123"
}
```

### Login

```
POST http://localhost:3000/api/auth/login
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "password123"
}
```

Copy the `token` from the response.

### Get All Events (Protected - Requires Token)

```
GET http://localhost:3000/api/events
Authorization: Bearer <your-token-here>
```

---

## Project Structure

```
starter-code/
  server.js           # Express app setup, DB connection (DO NOT MODIFY)
  package.json         # Dependencies (DO NOT MODIFY)
  models/
    Event.js           # Mongoose Event model
  routes/
    auth.js            # Register & Login routes
    events.js          # CRUD routes for events
  middleware/
    auth.js            # JWT authentication middleware
```

---

## Assessment Rules

- Fix bugs only in these 4 files: `routes/events.js`, `middleware/auth.js`, `models/Event.js`, `routes/auth.js`
- Do **NOT** modify `server.js` or `package.json`
- Do **NOT** add new npm packages
- `npm start` must work after your fixes
- Push all fixed files to your assigned branch before the timer ends

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `mongod` not recognized | Use the full path: `C:\Users\<your-username>\mongodb\bin\mongod.exe` |
| Port 27017 already in use | Another MongoDB instance is running. Close it or use a different port with `--port 27018` |
| `npm install` fails with permission error | Try `npm install --no-optional` |
| `bcrypt` fails to install | Run `npm install` again. If it persists, check that Node.js matches your OS architecture (x64) |
| Cannot connect to MongoDB | Ensure `mongod` is running in a separate terminal window |
