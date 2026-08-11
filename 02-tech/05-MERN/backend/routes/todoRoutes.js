
// define express router
const express = require('express');
const router = express.Router();
const AuthMiddleware = require('../middleware/authMiddleware');

// create MongoClient instance

const { MongoClient } = require('mongodb');
const ObjectId = require('mongodb').ObjectId;
const client = new MongoClient('mongodb://localhost:27017');

/*

db.todos.insertMany([
    { title: 'Buy groceries', completed: false },
    { title: 'Clean the house', completed: true },
    { title: 'Finish project', completed: false }
])

*/

router
    .get('/', async (req, res) => {
        try {
            await client.connect();
            const db = client.db('todosdb');
            const todosCollection = db.collection('todos');
            const userId = req.user.userId; // Assuming userId is stored in the token payload
            const todos = await todosCollection.find({ userId }).toArray(); // Fetch todos for the specific user
            res.json(todos);
        } catch (err) {
            console.error(err);
            res.status(500).send('Internal Server Error');
        }
    })
    .get('/', AuthMiddleware, async (req, res) => {
        try {
            await client.connect();
            const db = client.db('todosdb');
            const todosCollection = db.collection('todos');
            const todos = await todosCollection.find({ userId: req.user.userId }).toArray();
            res.json(todos);
        } catch (err) {
            console.error(err);
            res.status(500).send('Internal Server Error');
        }
    })
    .get('/:id', async (req, res) => {
        try {
            await client.connect();
            const db = client.db('todosdb');
            const todosCollection = db.collection('todos');
            const userId = req.user.userId; // Assuming userId is stored in the token payload
            const todo = await todosCollection.findOne({ _id: new ObjectId(req.params.id), userId });
            if (!todo) {
                return res.status(404).send('Todo not found');
            }
            res.json(todo);
        } catch (err) {
            console.error(err);
            res.status(500).send('Internal Server Error');
        }
    })
    .post('/', express.json(), AuthMiddleware, async (req, res) => {
        try {
            await client.connect();
            const db = client.db('todosdb');
            const todosCollection = db.collection('todos');
            const userId = req.user.userId; // Assuming userId is stored in the token payload
            const todoData = { ...req.body, userId }; // Attach userId to the todo data
            const result = await todosCollection.insertOne(todoData);
            res.status(201).json(result);
        } catch (err) {
            console.error(err);
            res.status(500).send('Internal Server Error');
        }
    })
    .put('/:id', express.json(), AuthMiddleware, async (req, res) => {
        try {
            await client.connect();
            const db = client.db('todosdb');
            const todosCollection = db.collection('todos');
            const result = await todosCollection.updateOne(
                { _id: new ObjectId(req.params.id), userId: req.user.userId },
                { $set: req.body }
            );
            if (result.matchedCount === 0) {
                return res.status(404).send('Todo not found');
            }
            res.json(result);
        } catch (err) {
            console.error(err);
            res.status(500).send('Internal Server Error');
        }
    })
    .delete('/:id', AuthMiddleware, async (req, res) => {
        try {
            await client.connect();
            const db = client.db('todosdb');
            const todosCollection = db.collection('todos');
            const result = await todosCollection.deleteOne({ _id: new ObjectId(req.params.id) });
            if (result.deletedCount === 0) {
                return res.status(404).send('Todo not found');
            }
            res.json(result);
        } catch (err) {
            console.error(err);
            res.status(500).send('Internal Server Error');
        }
    });


module.exports = router;

