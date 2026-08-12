

function logger(req, res, next) {
    const start = +Date.now();
    const url = req.originalUrl;
    const method = req.method;
    const stream = process.stdout;
    res.on('finish', () => {
        const duration = +Date.now() - start;
        stream.write(`${method} ${url} ${res.statusCode} ${duration}ms\n`);
    });
    next();
}

module.exports = logger; // cjs
// export default logger; // esm