






const http = require('http');

const httpServer = http.createServer();

const todos = [
    { id: 1, title: 'Learn Node.js', completed: false },
    { id: 2, title: 'Build a REST API', completed: false },
    { id: 3, title: 'Write tests', completed: false },
];

httpServer.on('request', (req, res) => {
    // GET /todos
    if (req.method === 'GET' && req.url === '/todos') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(todos));
    }

    // POST /todos
    else if (req.method === 'POST' && req.url === '/todos') {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });
        req.on('end', () => {
            const newTodo = JSON.parse(body);
            newTodo.id = todos.length + 1;
            todos.push(newTodo);
            res.writeHead(201, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify(newTodo));
        });
    }
    // Handle other routes
    else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found');
    }

});

httpServer.listen(3000, () => {
    console.log('Server is listening on port 3000');
});