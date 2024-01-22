-- DROP TABLE users;
-- CREATE TABLE users(
--     id SERIAL PRIMARY KEY,
--     username VARCHAR(100) UNIQUE,
--     email VARCHAR(100) UNIQUE,
--     user_password VARCHAR(100)
-- );
-- INSERT INTO users (username, email, user_password) VALUES ('Niki', 'niki.g@gmail.com', '2006!@abcd');
-- DROP TABLE tasks;
-- CREATE TABLE tasks(
--     id SERIAL PRIMARY KEY,
--     task_name VARCHAR(255) NOT NULL,
--     task_description TEXT NOT NULL,
--     is_completed BOOLEAN NOT NULL,
--     user_id INTEGER REFERENCES users(id) NOT NULL
-- );

SELECT * FROM users;
SELECT * FROM tasks;