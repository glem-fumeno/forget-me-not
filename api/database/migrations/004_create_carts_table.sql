CREATE TABLE carts_ (
    cart_id_ INTEGER PRIMARY KEY AUTOINCREMENT,
    name_ TEXT NOT NULL UNIQUE,
    icon_ TEXT NOT NULL
);

CREATE TABLE carts_users_ (
    user_id_ INTEGER,
    cart_id_ INTEGER,
    FOREIGN KEY(user_id_) REFERENCES users_(user_id_),
    FOREIGN KEY(cart_id_) REFERENCES carts_(cart_id_)
);

CREATE TABLE carts_items_ (
    cart_id_ INTEGER,
    item_id_ INTEGER,
    FOREIGN KEY(cart_id_) REFERENCES carts_(cart_id_),
    FOREIGN KEY(item_id_) REFERENCES items_(item_id_)
);
