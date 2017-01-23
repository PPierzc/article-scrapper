import sqlite3

connection =  sqlite3.connect('database.db')
cursor = connection.cursor()

while (1 > 0):
	command = input("Your SQL command: ")
	for i in cursor.execute('''{}'''.format(command)):
		print(i)

connection.commit()
