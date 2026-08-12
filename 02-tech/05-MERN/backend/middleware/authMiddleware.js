

// define AuthMiddleware function
// extract jwt token from request headers
// verify the token using jwt.verify method
// if token is valid, attach user information to request object
// if token is invalid or missing, return 401 Unauthorized response

const jwt = require('jsonwebtoken');

const AuthMiddleware = (req, res, next) => {
    console.log('AuthMiddleware invoked');
    const token = req.headers['authorization'];

    // split the token if it starts with 'Bearer '
    if (token && token.startsWith('Bearer ')) {
        token = token.slice(7, token.length).trimLeft();
    }

    if (!token) {
        return res.status(401).json({ message: 'Access denied. No token provided.' });
    }

    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET || 'your_jwt_secret');
        req.user = decoded; // attach user info to request object
        next(); // proceed to the next middleware or route handler
    } catch (err) {
        return res.status(401).json({ message: 'Invalid token.' });
    }
};

module.exports = AuthMiddleware;