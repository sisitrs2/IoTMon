---------- PRODUCTION ----------

INSERT INTO areas(name) VALUES("Area1");
INSERT INTO areas(name) VALUES("Area2");
INSERT INTO types(name) VALUES("DevA");
INSERT INTO types(name) VALUES("DevB");
INSERT INTO users(username, password, area_id) VALUES("admin1", "admin", 1);
INSERT INTO users(username, password, area_id) VALUES("admin2", "admin", 2);
INSERT INTO device_users(username, password, type_id, permissions) VALUES("view", "view", 1, "READ");
INSERT INTO device_users(username, password, type_id, permissions) VALUES("baba", "baba", 1, "READ");
INSERT INTO device_users(username, password, type_id, permissions) VALUES("bobo", "bobo", 1, "READ");
INSERT INTO device_users(username, password, type_id, permissions) VALUES("admin", "admin", 2, "READ");
INSERT INTO devices(name, address, type_id, version, temperature, voltage, current, status, data, lastscan, link, device_user_id, area_id) 
VALUES("Baba", "1.1.1.1", 1, "1.0", "26", "54.23", "34.52A", "Battery", "Power Outage", "08/08/2022 12:56:12", "http://1.1.1.1/", 1, 1);
INSERT INTO devices(name, address, type_id, version, temperature, voltage, current, status, data, lastscan, link, device_user_id, area_id) 
VALUES("Baba", "1.1.1.2", 2, "1.0", "23", "54.52", "54.63A", "Power", "", "08/08/2022 12:56:12", "http://1.1.1.2/", 2, 1);
INSERT INTO devices(name, address, type_id, version, temperature, voltage, current, status, data, lastscan, link, device_user_id, area_id) 
VALUES("Baba", "1.1.1.3", 1, "1.0", "29", "54.65", "35.25A", "Power", "", "08/08/2022 12:56:12", "http://1.1.1.3/", 1, 1);
INSERT INTO devices(name, address, type_id, version, temperature, voltage, current, status, data, lastscan, link, device_user_id, area_id) 
VALUES("Baba", "1.1.2.1", 2, "1.0", "-", "-", "-", "Unaccessable", "Couldn't connect.", "08/08/2022 12:56:12", "http://1.1.2.1/", 2, 1);
INSERT INTO devices(name, address, type_id, version, temperature, voltage, current, status, data, lastscan, link, device_user_id, area_id) 
VALUES("Baba", "1.1.1.4", 2, "1.0", "29", "54.87", "25.43A", "Battery", "Power Outage", "08/08/2022 12:56:12", "http://1.1.1.4/", 2, 1);
INSERT INTO devices(name, address, type_id, version, temperature, voltage, current, status, data, lastscan, link, device_user_id, area_id) 
VALUES("Baba", "1.1.1.5", 1, "1.0", "25", "53.92", "55.13A", "Power", "", "08/08/2022 12:56:12", "http://1.1.1.5/", 1, 1);