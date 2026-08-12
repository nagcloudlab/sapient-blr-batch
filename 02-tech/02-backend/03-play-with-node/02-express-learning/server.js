
const express = require('express');
const app = express();
// const logger = require('./middleware/logger');
const morgan = require('morgan');
const { MongoClient } = require('mongodb');

const todosRouter = require('./routes/todos');

app.use(morgan('dev'));
app.use(express.static('public'));
app.use(express.json());
app.use('/todos', todosRouter);
app.use('/api/todos', todosRouter);
app.get('/users', (req, res) => {
    const users = [
        { id: 1, name: 'Alice' },
        { id: 2, name: 'Bob' },
        { id: 3, name: 'Charlie' }
    ];
    res.json(users);
});




const MONGO_URI = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017';
const DB_NAME = process.env.DB_NAME || 'todosdb';
const PORT = Number(process.env.PORT || 3000);

async function startServer() {
    const client = new MongoClient(MONGO_URI);
    await client.connect();

    const db = client.db(DB_NAME);
    app.locals.todosCollection = db.collection('todos');

    app.listen(PORT, () => {
        console.log(`Server is running on port ${PORT}`);
        console.log(`Connected to MongoDB at ${MONGO_URI}/${DB_NAME}`);
    });
}

startServer().catch((error) => {
    console.error('Failed to start server:', error);
    process.exit(1);
});