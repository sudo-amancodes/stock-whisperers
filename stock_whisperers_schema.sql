CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    username VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(50),
    registration_date TIMESTAMP,
    profile_picture VARCHAR(255), 
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS live_posts (
    post_id SERIAL,
    content VARCHAR(255),
    user_id INTEGER,
    date TIMESTAMP,

    PRIMARY KEY (post_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


