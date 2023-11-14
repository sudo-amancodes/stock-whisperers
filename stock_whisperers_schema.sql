CREATE TABLE IF NOT EXISTS post (
    post_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    date_posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    likes INT NOT NULL DEFAULT 0,
    file_upload VARCHAR(255),
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS comment (
    comment_id SERIAL PRIMARY KEY,
    content TEXT,
    date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    likes INT NOT NULL DEFAULT 0,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    post_id INT REFERENCES post(post_id) ON DELETE CASCADE
);