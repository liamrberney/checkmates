DROP TABLE IF EXISTS variants;
CREATE TABLE variants
	("id" INT, "variant" TEXT, "specialWin" TEXT, "specialGame" TEXT, "specialRules" TEXT);

INSERT INTO variants
	("id", "variant", "specialWin", "specialGame", "specialRules")
VALUEs
	(1, "Classic", 0, 0, 0),
	(2, "Shogi", 0, 0, 1),
	(3, "Chaturanga", 0, 0, 1),
	(4, "Chess 960", 0, 1, 1),
	(5, "King of the Hill", 1, 1, 0),
	(6, "3 Check", 1, 1, 0),
	(7, "Racing Kings", 1, 1, 1);
    
DROP TABLE IF EXISTS users;
CREATE TABLE users(rowid INTEGER PRIMARY KEY AUTOINCREMENT, username text, name text, pwhash text, 
img_url text, lat float, lon float, bios text, variant text DEFAULT "Classic" NOT NULL, time_control int, 
ELO int DEFAULT 1200 NOT NULL, win INT DEFAULT 0 NOT NULL, loss INT DEFAULT 0 NOT NULL, draw INT DEFAULT 0 NOT NULL, 
total INT DEFAULT 0 NOT NULL, phone text, email text);


INSERT INTO users
	("username", "name","pwhash" ,"img_url", "lat", "lon", "bios", "variant", "time_control", "ELO")
VALUES
	("A", "AA","password", "/media/A.jpg", 34.44444, 84.3434, "bioA", "Classic", 100, 1200),
	("B", "BB","password", "/media/B.png", 42.4666667, 1.4666667, "bioB", "Shogi", 200, 1300),
	("C", "CC","password", "/media/C.png", 32.534167, 66.07805, "bioC", "Chaturanga", 1006, 1250),
	("D", "DD","password", "/media/D.png", 36.948889, 66.328611, "bioD", "Chess 960", 50, 1100),
	("E", "EE","password", "/media/E.png", 35.088056, 69.046389, "bioE", "King of the Hill", 20, 1000),
	("F", "FF","password", "/media/F.png", 36.083056, 69.0525, "bioF", "3 Check", 200, 950),
	("G", "GG","password", "/media/G.png", 31.015833, 61.860278, "bioG", "Racing Kings", 150, 900),
    ("H", "HH","password", "/media/H.png", 31.015833, 61.860278, "bioH", "Shogi", 170, 850),
    ("I", "II","password", "/media/I.png", 31.015833, 61.860278, "bioI", "Classic", 250, 1600),
    ("J", "JJ","password", "/media/J.png", NULL, NULL, "bioJ", "Classic", NULL, 1600),
    ("K", "KK","password", "/media/K.png", 31.015833, 61.860278, "bioK", "Classic", NULL, 1600);



SELECT user2, name, img_url, bios, distance, variant, time_control, ELO2 FROM 
(SELECT DISTINCT u1.rowid, u1.username AS user1, u1.time_control as t1, a.variant AS v1, 
b.variant AS v2, u2.username AS user2,u2.name, u2.img_url, u2.bios, u2.ELO as ELO2, 
    (u1.lon-u2.lon)*(u1.lon-u2.lon)+(u1.lat-u2.lat)*(u1.lat-u2.lat) as distance,
u2.variant AS variant, u2.time_control as time_control, ABS(u1.ELO-u2.ELO) AS delta_ELO, ABS(u1.time_control-u2.time_control) AS delta_T
FROM variants AS a, variants AS b, users AS u1, users AS u2
INNER JOIN variants ON a.variant = u1.variant
WHERE user1 = "A" AND user1 <> user2 AND b.variant = u2.variant
ORDER BY u1.rowid ASC, (distance is NULL) ASC, distance ASC, (b.variant = a.variant) OR (b.variant="Classic") DESC, 
(a.specialWin=b.specialWin) + (a.specialGame=b.specialGame) + (a.specialRules=b.specialRules) DESC,
delta_ELO ASC, (delta_T is NULL) OR (delta_T > 150) ASC, delta_T ASC) AS matches;


ALTER TABLE friends ADD COLUMN "A";
ALTER TABLE friends ADD COLUMN "B";
ALTER TABLE friends ADD COLUMN "C";
ALTER TABLE friends ADD COLUMN "D";
ALTER TABLE friends ADD COLUMN "E";
ALTER TABLE friends ADD COLUMN "F";
ALTER TABLE friends ADD COLUMN "G";
ALTER TABLE friends ADD COLUMN "H";
ALTER TABLE friends ADD COLUMN "I";
ALTER TABLE friends ADD COLUMN "J";
ALTER TABLE friends ADD COLUMN "K";

ALTER TABLE history ADD COLUMN "A";
ALTER TABLE history ADD COLUMN "B";
ALTER TABLE history ADD COLUMN "C";
ALTER TABLE history ADD COLUMN "D";
ALTER TABLE history ADD COLUMN "E";
ALTER TABLE history ADD COLUMN "F";
ALTER TABLE history ADD COLUMN "G";
ALTER TABLE history ADD COLUMN "H";
ALTER TABLE history ADD COLUMN "I";
ALTER TABLE history ADD COLUMN "J";
ALTER TABLE history ADD COLUMN "K";

ALTER TABLE games ADD COLUMN "A";
ALTER TABLE games ADD COLUMN "B";
ALTER TABLE games ADD COLUMN "C";
ALTER TABLE games ADD COLUMN "D";
ALTER TABLE games ADD COLUMN "E";
ALTER TABLE games ADD COLUMN "F";
ALTER TABLE games ADD COLUMN "G";
ALTER TABLE games ADD COLUMN "H";
ALTER TABLE games ADD COLUMN "I";
ALTER TABLE games ADD COLUMN "J";
ALTER TABLE games ADD COLUMN "K";
