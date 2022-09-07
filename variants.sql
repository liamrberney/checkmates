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