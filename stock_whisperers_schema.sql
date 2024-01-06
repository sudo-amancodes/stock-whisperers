CREATE DATABASE stock_whisperers;

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    registration_date TIMESTAMP,
    last_login TIMESTAMP,
    profile_picture VARCHAR(255), 
    trader_tally INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS tokens (
    user_id INT PRIMARY KEY REFERENCES users(user_id),
    total_tokens INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS investments (
    investment_type VARCHAR(255) NOT NULL,
    stock_name VARCHAR(255) NOT NULL,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    tokens_invested INTEGER NOT NULL,
    investment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    current_price FLOAT NOT NULL,
    PRIMARY KEY (investment_type, stock_name)
);

CREATE TABLE IF NOT EXISTS watchlist (
    watchlist_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    ticker_symbol VARCHAR(10) NOT NULL UNIQUE,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    user1_id INTEGER NOT NULL,
    user2_id INTEGER NOT NULL,
    FOREIGN KEY (user1_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (user2_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT unique_user_follow UNIQUE (user1_id, user2_id),
    CONSTRAINT check_user_follow CHECK (user1_id != user2_id)
);

CREATE TABLE IF NOT EXISTS comment_likes (
    comment_id INT,
    user_id INT,
    PRIMARY KEY (comment_id, user_id),
    FOREIGN KEY (comment_id) REFERENCES comment(comment_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
); 
