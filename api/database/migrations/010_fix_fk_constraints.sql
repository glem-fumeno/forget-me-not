PRAGMA foreign_keys=off;
-- USER SESSIONS
CREATE TABLE users_sessions_new_ (
    user_id_ INTEGER,
    token_ TEXT NOT NULL UNIQUE,
    FOREIGN KEY(user_id_) REFERENCES users_(user_id_) ON DELETE CASCADE
);

INSERT INTO users_sessions_new_ SELECT * FROM users_sessions_;
DROP TABLE users_sessions_;
ALTER TABLE users_sessions_new_ RENAME TO users_sessions_;

-- ITEMS USERS
DROP TABLE items_users_;

-- CARTS USERS
CREATE TABLE carts_users_new_ (
    user_id_ INTEGER,
    cart_id_ INTEGER,
    FOREIGN KEY(user_id_) REFERENCES users_(user_id_) ON DELETE CASCADE,
    FOREIGN KEY(cart_id_) REFERENCES carts_(cart_id_) ON DELETE CASCADE
);

INSERT INTO carts_users_new_ SELECT * FROM carts_users_;
DROP TABLE carts_users_;
ALTER TABLE carts_users_new_ RENAME TO carts_users_;

-- CARTS ITEMS
CREATE TABLE carts_items_new_ (
    item_id_ INTEGER,
    cart_id_ INTEGER,
    origin_ TEXT,
    FOREIGN KEY(item_id_) REFERENCES items_(item_id_) ON DELETE CASCADE,
    FOREIGN KEY(cart_id_) REFERENCES carts_(cart_id_) ON DELETE CASCADE
);

INSERT INTO carts_items_new_ SELECT * FROM carts_items_;
DROP TABLE carts_items_;
ALTER TABLE carts_items_new_ RENAME TO carts_items_;

-- RECIPES USERS
CREATE TABLE recipes_users_new_ (
    user_id_ INTEGER,
    recipe_id_ INTEGER,
    FOREIGN KEY(user_id_) REFERENCES users_(user_id_) ON DELETE CASCADE,
    FOREIGN KEY(recipe_id_) REFERENCES recipes_(recipe_id_) ON DELETE CASCADE
);

INSERT INTO recipes_users_new_ SELECT * FROM recipes_users_;
DROP TABLE recipes_users_;
ALTER TABLE recipes_users_new_ RENAME TO recipes_users_;

-- RECIPES ITEMS
CREATE TABLE recipes_items_new_ (
    item_id_ INTEGER,
    recipe_id_ INTEGER,
    FOREIGN KEY(item_id_) REFERENCES items_(item_id_) ON DELETE CASCADE,
    FOREIGN KEY(recipe_id_) REFERENCES recipes_(recipe_id_) ON DELETE CASCADE
);

INSERT INTO recipes_items_new_ SELECT * FROM recipes_items_;
DROP TABLE recipes_items_;
ALTER TABLE recipes_items_new_ RENAME TO recipes_items_;

-- USERS
CREATE TABLE users_new_ (
    user_id_ INTEGER PRIMARY KEY AUTOINCREMENT,
    username_ TEXT,
    email_ TEXT NOT NULL UNIQUE,
    password_ TEXT NOT NULL,
    role_ TEXT DEFAULT 'new',
    cart_id_ INTEGER,
    FOREIGN KEY(cart_id_) REFERENCES carts_(cart_id_) ON DELETE SET NULL
);

INSERT INTO users_new_ SELECT * FROM users_;
DROP TABLE users_;
ALTER TABLE users_new_ RENAME TO users_;

PRAGMA foreign_keys=on;
