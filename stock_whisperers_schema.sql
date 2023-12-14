CREATE DATABASE stock_whisperers IF NOT EXISTS

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50),
    registration_date TIMESTAMP,
    last_login TIMESTAMP,
    profile_picture VARCHAR(255), 
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS live_posts (
    post_id SERIAL,
    content VARCHAR(255),
    user_id INTEGER,
    date TIMESTAMP,

    PRIMARY KEY (post_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

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
    post_id INT REFERENCES post(post_id) ON DELETE CASCADE,
    parent_comment_id INT,
    FOREIGN KEY (parent_comment_id) REFERENCES comment(comment_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS likes (
    post_id INT,
    user_id INT,
    PRIMARY KEY (post_id, user_id),
    FOREIGN KEY (post_id) REFERENCES post(post_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS friendships (
    friendship_id SERIAL,
    user1_username VARCHAR(255) NOT NULL,
    user2_username VARCHAR(255) NOT NULL,
    FOREIGN KEY (user1_username) REFERENCES users(username) ON DELETE CASCADE,
    FOREIGN KEY (user2_username) REFERENCES users(username) ON DELETE CASCADE,
    CONSTRAINT unique_user_follow UNIQUE (user1_username, user2_username),
    CONSTRAINT check_user_follow CHECK (user1_username != user2_username)
);

CREATE TABLE IF NOT EXISTS comment_likes (
    comment_id INT,
    user_id INT,
    PRIMARY KEY (comment_id, user_id),
    FOREIGN KEY (comment_id) REFERENCES comment(comment_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
); 
