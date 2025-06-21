CREATE TABLE items_ (
    item_id_ INTEGER PRIMARY KEY AUTOINCREMENT,
    name_ TEXT NOT NULL UNIQUE,
    icon_ TEXT NOT NULL
);

CREATE TABLE items_users_ (
    user_id_ INTEGER,
    item_id_ INTEGER,
    FOREIGN KEY(user_id_) REFERENCES users_(user_id_),
    FOREIGN KEY(item_id_) REFERENCES items_(item_id_)
);
