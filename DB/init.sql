---------- PRODUCTION ----------

INSERT INTO areas(name) VALUES("Area1");
INSERT INTO areas(name) VALUES("Area2");
INSERT INTO users(username, password, area_id) VALUES("admin1", "admin", 1);
INSERT INTO users(username, password, area_id) VALUES("admin2", "admin", 2);
INSERT INTO device_users(username, password, type, permissions) VALUES("view", "view", "DevA", "READ");
INSERT INTO device_users(username, password, type, permissions) VALUES("admin", "admin", "DevB", "READ");
INSERT INTO devices(name, address, type, version, link, device_user_id, area_id) VALUES("Baba", "1.1.1.1", "DevA", "1.0", "http://1.1.1.1/", 1, 1);