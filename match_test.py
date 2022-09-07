#!/usr/bin/env python3
import sys
import traceback
import sqlite3
def sql_exec(query):
    con=sqlite3.connect("main.db")
    cur=con.cursor()
    cur.execute(query)
    con.commit()
    data=cur.fetchall()
    con.close()
    return data

def sql_get_column_names(table_name):
    query="pragma table_info("+table_name+")"
    data=sql_exec(query)
    names=[]
    for d in data:
        names.append(d[1])
    return names

def main(argv, arc):
    try:
        query = "SELECT IIF ((SELECT COUNT(*) AS CNTREC FROM pragma_table_info('friends') WHERE name='"+argv[1]+"') > 0, 1, 0);"
        data=sql_exec(query)
        if (data[0][0] == 0):
            query = "ALTER TABLE friends ADD COLUMN "+argv[1]+";"
            sql_exec(query)
        sql_file = open("new_friend.sql")
        query = sql_file.read().split(';')
        for q in query:
            q = q.replace("?", argv[2])
            q = q.replace("~",argv[1])
            sql_exec(q)
        query="select * from "+"friends"
        data=sql_exec(query)
        print('\t'.join(map(str, sql_get_column_names("friends"))))
        for d in data:
            print('\t'.join(map(str, d)))
    except:
        print(traceback.format_exc())

if __name__ == '__main__':
	main(sys.argv, len(sys.argv))