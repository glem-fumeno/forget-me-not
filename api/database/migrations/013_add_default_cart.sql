CREATE TABLE metadata_ (
    metadata_id_ INTEGER PRIMARY KEY,
    cart_id_ REFERENCES carts_(cart_id_) ON DELETE CASCADE
)
