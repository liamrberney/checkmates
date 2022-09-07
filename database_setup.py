#!/usr/bin/env python3
import sqlite3
import traceback

#this script modifies the database
#edit it to add new tables or new columns to an existing table

def sql_exec(query):
    con=sqlite3.connect("main.db")
    cur=con.cursor()
    cur.execute(query)
    con.commit()
    data=cur.fetchall()
    con.close()
    return data


def main():
    try:
        sql_file = open("users.sql")
        query = sql_file.read().split(';')
        for q in query:
            sql_exec(q)
    except:
        print(traceback.format_exc())
    
    try:
        sql_file = open("friends.sql")
        query = sql_file.read().split(';')
        for q in query:
            sql_exec(q)
    except:
        print(traceback.format_exc())
    try:
        sql_file = open("history.sql")
        query = sql_file.read().split(';')
        for q in query:
            sql_exec(q)
    except:
        print(traceback.format_exc())
    try:
        sql_file = open("games.sql")
        query = sql_file.read().split(';')
        for q in query:
            sql_exec(q)
    except:
        print(traceback.format_exc())
    try:
        sql_file = open("variants.sql")
        query = sql_file.read().split(';')
        for q in query:
            sql_exec(q)
    except:
        print(traceback.format_exc())

    try:
        sql_file = open("swipe.sql")
        query = sql_file.read().split(';')
        for q in query:
            sql_exec(q)
    except:
        print(traceback.format_exc())

    try:
        sql_file = open("test.sql")
        query = sql_file.read().split(';')
        for q in query:
            sql_exec(q)
    except:
        print(traceback.format_exc())
    
    #try:
    #    sql_exec("DROP TABLE IF EXISTS users")
    #except:
    #    print(traceback.format_exc())
    #query="create table users(name text,username text,pwhash text,img_url text)" 
    #sql_exec(query) 
    # Saved in case of issues in the future
    

if __name__ == '__main__':
	main()