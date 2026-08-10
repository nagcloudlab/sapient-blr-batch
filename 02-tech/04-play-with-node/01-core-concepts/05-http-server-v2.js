

const http = require('http');
const fs = require('fs');

const httpServer = http.createServer(); // EventEmitter

httpServer.on('request', (req, res) => {
    console.log(`Received request: ${req.method} ${req.url}`);


    // fs.readFile('./ppt/node.pdf', (err, data) => {
    //     if (err) {
    //         res.writeHead(500, { 'Content-Type': 'text/plain' });
    //         res.end('Internal Server Error\n');
    //         return;
    //     }
    //     res.writeHead(200, { 'Content-Type': 'application/pdf' });
    //     res.end(data);
    // });

    const readStream = fs.createReadStream('./ppt/node.pdf');
    readStream.pipe(res); // res is a writable stream

});


httpServer.listen(3000, () => {
    console.log('Server is listening on port 3000');
});
