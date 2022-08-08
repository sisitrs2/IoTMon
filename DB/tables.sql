CREATE TABLE IF NOT EXISTS areas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username text NOT NULL,
    password text,
    area_id INTEGER,
    FOREIGN KEY(area_id) REFERENCES areas(id)
);

CREATE TABLE IF NOT EXISTS device_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username text NOT NULL,
    password text,
    permissions text NOT NULL DEFAULT '-'
);

CREATE TABLE IF NOT EXISTS devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    address text NOT NULL,
    type text NOT NULL,
    version text DEFAULT '-',
    link text NOT NULL,
    area_id INTEGER,
    device_user_id INTEGER,
    FOREIGN KEY(device_user_id) REFERENCES device_users(id),
    FOREIGN KEY(area_id) REFERENCES areas(id)
);