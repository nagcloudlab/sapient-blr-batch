
const express = require('express');
const router = express.Router();

const todos = require('../data/todos.json'); // Import the todos array from data/todos.js

// const todos = [
//     { id: 1, title: 'Learn Express', completed: false },
//     { id: 2, title: 'Build a REST API', completed: false },
//     { id: 3, title: 'Deploy to Heroku', completed: false },
//     { id: 4, title: 'Learn React', completed: false },
//     { id: 5, title: 'Build a React App', completed: false },
//     { id: 6, title: 'Learn Redux', completed: false },
//     { id: 7, title: 'Build a Redux App', completed: false },
//     { id: 8, title: 'Learn TypeScript', completed: false },
//     { id: 9, title: 'Build a TypeScript App', completed: false },
//     { id: 10, title: 'Learn GraphQL', completed: false },
//     { id: 11, title: 'Build a GraphQL API', completed: false },
//     { id: 12, title: 'Learn Next.js', completed: false },
//     { id: 13, title: 'Build a Next.js App', completed: false },
//     { id: 14, title: 'Learn Gatsby', completed: false },
//     { id: 15, title: 'Build a Gatsby App', completed: false },
//     { id: 16, title: 'Learn Vue.js', completed: false },
//     { id: 17, title: 'Build a Vue.js App', completed: false },
//     { id: 18, title: 'Learn Angular', completed: false },
//     { id: 19, title: 'Build an Angular App', completed: false },
//     { id: 20, title: 'Learn Svelte', completed: false },
// ];

router
    .get("/", (req, res) => {
        //const count = req.query.count || 20;
        //res.json(todos.slice(0, count));
        return res.json(todos);
    })
    .get('/:todoId', (req, res) => {
        const id = parseInt(req.params.todoId, 10);
        const todo = todos.find(todo => todo.id === id);
        if (todo) {
            res.json(todo);
        } else {
            res.status(404).json({ error: 'Todo not found' });
        }
    })
    .post('/', express.json(), (req, res) => {
        const { id, title, completed } = req.body; // destructuring
        if (id && title && typeof completed === 'boolean') {
            const newTodo = { id, title, completed };
            todos.push(newTodo);
            res.status(201).json(newTodo);
        } else {
            res.status(400).json({ error: 'Invalid todo data' });
        }
    })
    .delete('/:todoId', (req, res) => {
        const id = parseInt(req.params.todoId, 10);
        const index = todos.findIndex(todo => todo.id === id);
        if (index !== -1) {
            const deletedTodo = todos.splice(index, 1)[0];
            res.json(deletedTodo);
        } else {
            res.status(404).json({ error: 'Todo not found' });
        }
    });
module.exports = router;
