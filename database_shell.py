#!/usr/bin/env python3
import sqlite3
import traceback
import sys


def main(argv):
	if len(argv)==1: name="main.db"
	else: name="db.sqlite3"

	con=sqlite3.connect(name)
	cur=con.cursor()
	print("this is an sql shell for interacting with the database")
	print("try running: select * from users")
	while True:
		query=input(">> ")
		try:
			cur.execute(query)
			rsp=cur.fetchall()
			for r in rsp:
				print(r)
		except:
			print(traceback.format_exc())
		con.commit()

if __name__ == '__main__':
	main(sys.argv)