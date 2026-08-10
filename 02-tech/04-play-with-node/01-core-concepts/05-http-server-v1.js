

const http = require('http');

const httpServer = http.createServer(); // EventEmitter

httpServer.on('request', (req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('Hello World\n');
});


httpServer.listen(3000, () => {
    console.log('Server is listening on port 3000');
});
