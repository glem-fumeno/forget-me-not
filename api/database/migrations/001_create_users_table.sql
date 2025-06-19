CREATE TABLE users_ (
    user_id_ INTEGER PRIMARY KEY AUTOINCREMENT,
    username_ TEXT,
    email_ TEXT NOT NULL UNIQUE,
    password_ TEXT NOT NULL
);

CREATE TABLE users_sessions_ (
    user_id_ INTEGER,
    token_ TEXT NOT NULL UNIQUE,
    FOREIGN KEY(user_id_) REFERENCES users_(user_id_)
);
