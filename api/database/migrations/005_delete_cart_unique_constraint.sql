PRAGMA foreign_keys=off;

BEGIN TRANSACTION;

ALTER TABLE carts_ RENAME TO carts_old_;

CREATE TABLE carts_ (
    cart_id_ INTEGER PRIMARY KEY AUTOINCREMENT,
    name_ TEXT NOT NULL,
    icon_ TEXT NOT NULL
);

INSERT INTO carts_ SELECT * FROM carts_old_;

DROP TABLE carts_old_;

COMMIT;

PRAGMA foreign_keys=on;
