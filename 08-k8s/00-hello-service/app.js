
const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
    const hostIpAddress = req.socket.localAddress;
    res.json({
        message: "Hello,",
        hostIpAddress: hostIpAddress
    });
});

app.listen(port, () => {
    console.log(`Server is running on http://0.0.0.0:${port}`);
});