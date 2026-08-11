
const express = require('express');
const { ObjectId } = require('mongodb');
const router = express.Router();

function toApiTodo(todoDoc) {
    return {
        id: todoDoc._id.toString(),
        title: todoDoc.title,
        completed: Boolean(todoDoc.completed)
    };
}

function parseTodoId(rawId) {
    return ObjectId.isValid(rawId) ? new ObjectId(rawId) : null;
}

function getTodosCollection(req) {
    return req.app.locals.todosCollection;
}

router
    .get('/', async (req, res) => {
        const todosCollection = getTodosCollection(req);
        const limit = Number(req.query.count || 0);

        const cursor = todosCollection
            .find({})
            .sort({ _id: -1 });

        if (Number.isFinite(limit) && limit > 0) {
            cursor.limit(limit);
        }

        const todos = await cursor.toArray();
        return res.json(todos.map(toApiTodo));
    })
    .get('/:todoId', async (req, res) => {
        const todoId = parseTodoId(req.params.todoId);
        if (!todoId) {
            return res.status(400).json({ error: 'Invalid todo id' });
        }

        const todosCollection = getTodosCollection(req);
        const todo = await todosCollection.findOne({ _id: todoId });
        if (!todo) {
            return res.status(404).json({ error: 'Todo not found' });
        }

        return res.json(toApiTodo(todo));
    })
    .post('/', async (req, res) => {
        const { title, completed = false } = req.body;
        if (!title || typeof title !== 'string') {
            return res.status(400).json({ error: 'title is required and must be a string' });
        }

        if (typeof completed !== 'boolean') {
            return res.status(400).json({ error: 'completed must be a boolean' });
        }

        const todosCollection = getTodosCollection(req);
        const newTodo = {
            title: title.trim(),
            completed
        };

        const result = await todosCollection.insertOne(newTodo);
        return res.status(201).json({
            id: result.insertedId.toString(),
            title: newTodo.title,
            completed: newTodo.completed
        });
    })
    .put('/:todoId', async (req, res) => {
        const todoId = parseTodoId(req.params.todoId);
        if (!todoId) {
            return res.status(400).json({ error: 'Invalid todo id' });
        }

        const { title, completed } = req.body;
        if (!title || typeof title !== 'string') {
            return res.status(400).json({ error: 'title is required and must be a string' });
        }

        if (typeof completed !== 'boolean') {
            return res.status(400).json({ error: 'completed must be a boolean' });
        }

        const todosCollection = getTodosCollection(req);
        const updateResult = await todosCollection.updateOne(
            { _id: todoId },
            { $set: { title: title.trim(), completed } }
        );

        if (updateResult.matchedCount === 0) {
            return res.status(404).json({ error: 'Todo not found' });
        }

        const updatedTodo = await todosCollection.findOne({ _id: todoId });
        return res.json(toApiTodo(updatedTodo));
    })
    .delete('/:todoId', async (req, res) => {
        const todoId = parseTodoId(req.params.todoId);
        if (!todoId) {
            return res.status(400).json({ error: 'Invalid todo id' });
        }

        const todosCollection = getTodosCollection(req);
        const deletedTodo = await todosCollection.findOne({ _id: todoId });
        if (!deletedTodo) {
            return res.status(404).json({ error: 'Todo not found' });
        }

        await todosCollection.deleteOne({ _id: todoId });
        return res.json(toApiTodo(deletedTodo));
    });

module.exports = router;
