SELECT a.username AS user1, b.username AS user2, 
    69 *
    DEGREES(ACOS(MIN(1.0, COS(RADIANS(a.lat))
         * COS(RADIANS(b.lat))
         * COS(RADIANS(a.long - b.long))
         + SIN(RADIANS(a.lat))
         * SIN(RADIANS(b.lat))))) AS distance
FROM users AS a
JOIN users AS b ON a.rowid <> b.rowid AND a.rowid < b.rowid
WHERE distance < 1000
ORDER BY distance DESC LIMIT 10;