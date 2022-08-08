---------- PRODUCTION ----------

INSERT INTO areas(name) VALUES("Area1");
INSERT INTO areas(name) VALUES("Area2");
INSERT INTO users(username, password, area_id) VALUES("admin1", "admin", 1);
INSERT INTO users(username, password, area_id) VALUES("admin2", "admin", 2);
INSERT INTO devices(name, address, type, version, link) VALUES("Baba", "1.1.1.1", "DevA", "1.0", "http://1.1.1.1/");
