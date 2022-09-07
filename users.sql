DROP TABLE IF EXISTS users;

CREATE TABLE users(rowid INTEGER PRIMARY KEY AUTOINCREMENT, username text, name text, pwhash text, 
img_url text, lat float DEFAULT NULL, lon float DEFAULT NULL, bios text, variant text DEFAULT "Classic" NOT NULL, time_control int, 
ELO int DEFAULT 1200 NOT NULL, win INT DEFAULT 0 NOT NULL, loss INT DEFAULT 0 NOT NULL, draw INT DEFAULT 0 NOT NULL, 
total INT DEFAULT 0 NOT NULL, phone text, email text);

--INSERT INTO users(name, username, pwhash, img_url, address, bios, matches)
--VALUES ("Bob", "Joe", "****", "./x.png", "111 BumBum Street", "", "");