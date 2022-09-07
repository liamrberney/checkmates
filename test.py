import sqlite3
import traceback



# use this function to execute arbtrary sql commands
# returns the result as an array of tuples
def sql_exec(query):
    con = sqlite3.connect("main.db")
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    data = cur.fetchall()
    con.close()
    return data

def add_history(user1, user2, user1Score, user2Score):
    query = "ALTER TABLE history ADD COLUMN "+user1+";"
    sql_exec(query)
    try:
        sql_file = open("new_history.sql")
        query = sql_file.read().split(';')
        for q in query:
            q = q.replace("?", user2)
            q = q.replace("%", user1Score)
            q = q.replace("&", user2Score)
            q = q.replace("~", user1)
            sql_exec(q)
    except:
        print(traceback.format_exc())


add_match("X", "Y", "W", "L")