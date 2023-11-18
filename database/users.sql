CREATE TABLE USERS (
    user_id INTEGER
                PRIMARY KEY
                AUTOINCREMENT,
    user        TEXT
                NOT NULL
                UNIQUE,
    password    TEXT
                NOT NULL
);
