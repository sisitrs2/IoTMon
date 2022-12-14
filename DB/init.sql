---------- PRODUCTION ----------

INSERT INTO areas(name) VALUES("Area1");
INSERT INTO areas(name) VALUES("Area2");
INSERT INTO types(name) VALUES("DevA");
INSERT INTO types(name) VALUES("DevB");
INSERT INTO users(username, password, area_id) VALUES("user1", "user1", 1);
INSERT INTO users(username, password, area_id) VALUES("user2", "user2", 2);
INSERT INTO users(username, password, admin) VALUES("admin", "admin", 1);
INSERT INTO device_users(username, password, type_id, permissions) VALUES("view", "view", 1, "READ");
INSERT INTO device_users(username, password, type_id, permissions) VALUES("baba", "baba", 1, "READ");
INSERT INTO device_users(username, password, type_id, permissions) VALUES("bobo", "bobo", 1, "READ");
INSERT INTO device_users(username, password, type_id, permissions) VALUES("admin", "admin", 2, "READ");
INSERT INTO devices(name, address, type_id, version, batteries, temperature, voltage, current, status, data, lastscan, link, device_user_id, area_id) 
VALUES("Baba", "1.1.1.1", 1, "1.0", 1, "26", "54.23", "34.52", "OK", "", "08/08/2022 12:56:12", "http://1.1.1.1/", 1, 1);
INSERT INTO devices(name, address, type_id, version, batteries, temperature, voltage, current, status, data, lastscan, link, device_user_id, area_id) 
VALUES("Lole", "1.1.1.2", 2, "1.0", 1, "23", "54.52", "54.63", "Alert", "", "08/08/2022 12:56:12", "http://1.1.1.2/", 2, 1);
INSERT INTO devices(name, address, type_id, version, batteries, temperature, voltage, current, status, data, lastscan, link, device_user_id, area_id) 
VALUES("Nemo", "1.1.1.3", 1, "1.0", 2, "29", "54.65", "35.25", "Unaccessible", "", "08/08/2022 12:56:12", "http://1.1.1.3/", 1, 1);
INSERT INTO devices(name, address, type_id, version, batteries, temperature, voltage, current, status, data, lastscan, link, device_user_id, area_id) 
VALUES("Olala", "1.1.2.1", 2, "1.0", 3, "-", "-", "-", "OK", "Couldn't connect.", "08/08/2022 12:56:12", "http://1.1.2.1/", 2, 2);
INSERT INTO devices(name, address, type_id, version, batteries, temperature, voltage, current, status, data, lastscan, link, device_user_id, area_id) 
VALUES("Moko", "1.1.1.4", 2, "1.0", 1, "29", "54.87", "25.43", "OK", "Power Outage", "08/08/2022 12:56:12", "http://1.1.1.4/", 2, 1);
INSERT INTO devices(name, address, type_id, version, batteries, temperature, voltage, current, status, data, lastscan, link, device_user_id, area_id) 
VALUES("Lurem", "1.1.1.5", 1, "1.0", 2, "25", "53.92", "55.13", "OK", "", "08/08/2022 12:56:12", "http://1.1.1.5/", 1, 1);
INSERT INTO alarms(data, lastscan, device_id, area_id, relevant) 
VALUES("Power outage.", "08/08/2022 12:56:12", 2, 1, 1);
INSERT INTO alarms(data, lastscan, device_id, area_id, relevant) 
VALUES("Couldn't connect.", "08/08/2022 12:56:12", 3, 1, 0);