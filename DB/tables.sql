CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type INTEGER NOT NULL DEFAULT 0,
    username text NOT NULL,
    password text,
    permissions text NOT NULL DEFAULT '-',
    attain text DEFAULT "-",
    relevant INTEGER NOT NULL DEFAULT 1,
    found_on text,
    server_id INTEGER,
    device_id INTEGER,
    other TEXT,
    FOREIGN KEY(server_id) REFERENCES servers(id),
    FOREIGN KEY(device_id) REFERENCES netdevices(id)
);