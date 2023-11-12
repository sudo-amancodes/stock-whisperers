CREATE Table if not exists users(
    user_id SERIAL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    username VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(50),
    registration_date TIMESTAMP,
    profile_picture VARCHAR(255)
);

