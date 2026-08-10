


const express = require('express');
const app = express();
// const logger = require('./middleware/logger');
const morgan = require('morgan');

const todosRouter = require('./routes/todos');

app.use(morgan('dev'));
app.use(express.static('public'));
app.use(morgan('dev'));
app.use(express.static('public'));
app.use('/todos', todosRouter);
app.get('/users', (req, res) => {
    const users = [
        { id: 1, name: 'Alice' },
        { id: 2, name: 'Bob' },
        { id: 3, name: 'Charlie' }
    ];
    res.json(users);
});




app.listen(3000, () => {
    console.log('Server is running on port 3000');
});