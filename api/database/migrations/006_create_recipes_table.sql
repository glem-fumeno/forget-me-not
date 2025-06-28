CREATE TABLE recipes_ (
    recipe_id_ INTEGER PRIMARY KEY AUTOINCREMENT,
    name_ TEXT NOT NULL,
    icon_ TEXT NOT NULL
);

CREATE TABLE recipes_users_ (
    user_id_ INTEGER,
    recipe_id_ INTEGER,
    FOREIGN KEY(user_id_) REFERENCES users_(user_id_),
    FOREIGN KEY(recipe_id_) REFERENCES recipes_(recipe_id_)
);

CREATE TABLE recipes_items_ (
    recipe_id_ INTEGER,
    item_id_ INTEGER,
    FOREIGN KEY(recipe_id_) REFERENCES recipes_(recipe_id_),
    FOREIGN KEY(item_id_) REFERENCES items_(item_id_)
);
