CREATE TABLE IF NOT EXISTS areas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL
);

CREATE TABLE IF NOT EXISTS types (
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
    type_id INTEGER NOT NULL,
    permissions text NOT NULL DEFAULT '-',
    FOREIGN KEY(type_id) REFERENCES types(id)
);

CREATE TABLE IF NOT EXISTS devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    address text NOT NULL,
    type_id INTEGER NOT NULL,
    version text DEFAULT '-',
    temperature text DEFAULT '-',
    voltage text DEFAULT '-',
    current text DEFAULT '-',
    status text DEFAULT '-',
    lastscan text DEFAULT '-',
    link text NOT NULL DEFUALT '#',
    area_id INTEGER,
    device_user_id INTEGER,
    FOREIGN KEY(device_user_id) REFERENCES device_users(id),
    FOREIGN KEY(type_id) REFERENCES types(id),
    FOREIGN KEY(area_id) REFERENCES areas(id)
);