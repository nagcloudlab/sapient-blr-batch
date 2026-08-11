
// cjs

const express = require('express');
const todoRoutes = require('./routes/todoRoutes');
const authRoutes = require('./routes/authRoutes');
const authMiddleware = require('./middleware/authMiddleware');
const cors = require('cors');


const app = express();
app.use(cors({
    origin: 'http://localhost:5173',
}));
app.use('/auth', authRoutes)
app.use('/api/v1/todos', authMiddleware, todoRoutes);


app.listen(process.env.PORT || 3000, () => {
    console.log('Server is running on port 3000');
});