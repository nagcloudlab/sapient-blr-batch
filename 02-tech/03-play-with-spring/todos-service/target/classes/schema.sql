

--   - todo: {
--             id: string,
--             title: string,
--             description: string,
--             status: string, // e.g., "pending", "completed"
--             createdAt: Date,
--             updatedAt: Date
--         }
--         - user: {
--             id: string,
--             name: string,
--             email: string,
--             password: string, // hashed
--             createdAt: Date,
--             updatedAt: Date
--         }

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO todos (title, description, status, user_id) VALUES
('Buy groceries', 'Milk, Bread, Eggs', 'PENDING', null),
('Complete project report', 'Finalize the report and submit it', 'COMPLETED', null),
('Workout', 'Go for a run in the park', 'PENDING', null);