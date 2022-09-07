SELECT DISTINCT user2, name, img_url, bios, distance, variant, time_control, ELO2 FROM 
(SELECT DISTINCT u1.rowid, u1.username AS user1, u1.time_control as t1, a.variant AS v1, 
b.variant AS v2, u2.username AS user2,u2.name, u2.img_url, u2.bios, u2.ELO as ELO2, 
    (u1.lat-u2.lat)*(u1.lat-u2.lat)*69+(u1.lon-u2.lon)*(u1.lon-u2.lon)*(1-(u1.lat)*(u1.lat)/2 + (u1.lat)*(u1.lat)*(u1.lat)*(u1.lat)/24-(u1.lat)*(u1.lat)*(u1.lat)*(u1.lat)*(u1.lat)*(u1.lat)/720)*69 as distance,
u2.variant AS variant, u2.time_control as time_control, ABS(u1.ELO-u2.ELO) AS delta_ELO, ABS(u1.time_control-u2.time_control) AS delta_T
FROM variants AS a, variants AS b, users AS u1, users AS u2
INNER JOIN variants ON a.variant = u1.variant
WHERE user1 = "~" AND user1 <> user2 AND b.variant = u2.variant
ORDER BY u1.rowid ASC, (distance is NULL) DESC, distance ASC, (b.variant = a.variant) OR (b.variant="Classic") ASC, 
(a.specialWin=b.specialWin) + (a.specialGame=b.specialGame) + (a.specialRules=b.specialRules) ASC,
delta_ELO DESC, delta_T DESC) AS matches, swipe 
WHERE (matches.user2 IN (SELECT DISTINCT ~ FROM swipe)) IS NULL OR ((matches.user2 IN (SELECT DISTINCT ~ FROM swipe)) = 0);