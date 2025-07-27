ALTER TABLE carts_items_ ADD COLUMN origin_new_ TEXT NOT NULL DEFAULT '';
UPDATE carts_items_ SET origin_new_ = COALESCE(origin_, '');
ALTER TABLE carts_items_ DROP COLUMN origin_;
ALTER TABLE carts_items_ RENAME COLUMN origin_new_ TO origin_;
