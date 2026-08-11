// define express router
const express = require('express');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const router = express.Router();

// create MongoClient instance

const { MongoClient } = require('mongodb');
const ObjectId = require('mongodb').ObjectId;
const client = new MongoClient('mongodb://localhost:27017');


router
    .post('/register', express.json(), async (req, res) => {
        try {
            await client.connect();
            const db = client.db('todosdb');
            const usersCollection = db.collection('users');

            const { username, password, name } = req.body;

            // Check if user already exists
            const existingUser = await usersCollection.findOne({ username });
            if (existingUser) {
                return res.status(400).json({ message: 'User already exists' });
            }

            // Insert new user
            const hashedPassword = await bcrypt.hash(password, 10);
            const result = await usersCollection.insertOne({ username, password: hashedPassword, name });
            res.status(201).json({ message: 'User registered successfully', userId: result.insertedId });
        } catch (error) {
            console.error(error);
            res.status(500).json({ message: 'Internal server error' });
        } finally {
            await client.close();
        }
    })
    .post('/login', express.json(), async (req, res) => {
        try {
            await client.connect();
            const db = client.db('todosdb');
            const usersCollection = db.collection('users');

            const { username, password } = req.body;

            // Find user by username
            const user = await usersCollection.findOne({ username });
            if (!user) {
                return res.status(400).json({ message: 'Invalid username or password' });
            }

            // Compare passwords
            const isPasswordValid = await bcrypt.compare(password, user.password);
            if (!isPasswordValid) {
                return res.status(400).json({ message: 'Invalid username or password' });
            }

            const token = jwt.sign({ userId: user._id, foo: "bar" }, 'your_jwt_secret', { expiresIn: '1h' });
            res.status(200).json({ message: 'Login successful', userId: user._id, token });

        } catch (error) {
            console.error(error);
            res.status(500).json({ message: 'Internal server error' });
        } finally {
            await client.close();
        }
    });


module.exports = router;