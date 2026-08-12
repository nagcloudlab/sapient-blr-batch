
// cjs

const express = require('express');
const todoRoutes = require('./routes/todoRoutes');
const authRoutes = require('./routes/authRoutes');
const authMiddleware = require('./middleware/authMiddleware');
const cors = require('cors');
const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');


const app = express();

const swaggerSpec = swaggerJsdoc({
    definition: {
        openapi: '3.0.0',
        info: {
            title: 'Todo API',
            version: '1.0.0',
            description: 'REST API documentation for auth and todos.'
        },
        servers: [
            {
                url: 'http://localhost:3000'
            }
        ],
        components: {
            securitySchemes: {
                bearerAuth: {
                    type: 'http',
                    scheme: 'bearer',
                    bearerFormat: 'JWT'
                }
            }
        },
        paths: {
            '/auth/register': {
                post: {
                    tags: ['Auth'],
                    summary: 'Register a new user',
                    requestBody: {
                        required: true,
                        content: {
                            'application/json': {
                                schema: {
                                    type: 'object',
                                    required: ['username', 'password', 'name'],
                                    properties: {
                                        username: { type: 'string', example: 'john_doe' },
                                        password: { type: 'string', example: 'strongPassword123' },
                                        name: { type: 'string', example: 'John Doe' }
                                    }
                                }
                            }
                        }
                    },
                    responses: {
                        '201': { description: 'User registered successfully' },
                        '400': { description: 'User already exists' },
                        '500': { description: 'Internal server error' }
                    }
                }
            },
            '/auth/login': {
                post: {
                    tags: ['Auth'],
                    summary: 'Login and receive JWT token',
                    requestBody: {
                        required: true,
                        content: {
                            'application/json': {
                                schema: {
                                    type: 'object',
                                    required: ['username', 'password'],
                                    properties: {
                                        username: { type: 'string', example: 'john_doe' },
                                        password: { type: 'string', example: 'strongPassword123' }
                                    }
                                }
                            }
                        }
                    },
                    responses: {
                        '200': { description: 'Login successful with token' },
                        '400': { description: 'Invalid username or password' },
                        '500': { description: 'Internal server error' }
                    }
                }
            },
            '/api/v1/todos': {
                get: {
                    tags: ['Todos'],
                    summary: 'Get all todos for the logged-in user',
                    security: [{ bearerAuth: [] }],
                    responses: {
                        '200': { description: 'Todo list fetched successfully' },
                        '401': { description: 'Unauthorized' },
                        '500': { description: 'Internal server error' }
                    }
                },
                post: {
                    tags: ['Todos'],
                    summary: 'Create a new todo',
                    security: [{ bearerAuth: [] }],
                    requestBody: {
                        required: true,
                        content: {
                            'application/json': {
                                schema: {
                                    type: 'object',
                                    properties: {
                                        title: { type: 'string', example: 'Finish API docs' },
                                        completed: { type: 'boolean', example: false }
                                    }
                                }
                            }
                        }
                    },
                    responses: {
                        '201': { description: 'Todo created successfully' },
                        '401': { description: 'Unauthorized' },
                        '500': { description: 'Internal server error' }
                    }
                }
            },
            '/api/v1/todos/{id}': {
                get: {
                    tags: ['Todos'],
                    summary: 'Get a single todo by id',
                    security: [{ bearerAuth: [] }],
                    parameters: [
                        {
                            name: 'id',
                            in: 'path',
                            required: true,
                            schema: { type: 'string' }
                        }
                    ],
                    responses: {
                        '200': { description: 'Todo fetched successfully' },
                        '404': { description: 'Todo not found' },
                        '401': { description: 'Unauthorized' },
                        '500': { description: 'Internal server error' }
                    }
                },
                put: {
                    tags: ['Todos'],
                    summary: 'Update a todo by id',
                    security: [{ bearerAuth: [] }],
                    parameters: [
                        {
                            name: 'id',
                            in: 'path',
                            required: true,
                            schema: { type: 'string' }
                        }
                    ],
                    requestBody: {
                        required: true,
                        content: {
                            'application/json': {
                                schema: {
                                    type: 'object',
                                    properties: {
                                        title: { type: 'string', example: 'Updated todo title' },
                                        completed: { type: 'boolean', example: true }
                                    }
                                }
                            }
                        }
                    },
                    responses: {
                        '200': { description: 'Todo updated successfully' },
                        '404': { description: 'Todo not found' },
                        '401': { description: 'Unauthorized' },
                        '500': { description: 'Internal server error' }
                    }
                },
                delete: {
                    tags: ['Todos'],
                    summary: 'Delete a todo by id',
                    security: [{ bearerAuth: [] }],
                    parameters: [
                        {
                            name: 'id',
                            in: 'path',
                            required: true,
                            schema: { type: 'string' }
                        }
                    ],
                    responses: {
                        '200': { description: 'Todo deleted successfully' },
                        '404': { description: 'Todo not found' },
                        '401': { description: 'Unauthorized' },
                        '500': { description: 'Internal server error' }
                    }
                }
            }
        }
    },
    apis: []
});

app.use(cors({
    origin: 'http://localhost:5173',
}));
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));
app.get('/api-docs.json', (req, res) => {
    res.setHeader('Content-Type', 'application/json');
    res.send(swaggerSpec);
});
app.use('/auth', authRoutes)
app.use('/api/v1/todos', authMiddleware, todoRoutes);


app.listen(process.env.PORT || 3000, () => {
    console.log('Server is running on port 3000');
});