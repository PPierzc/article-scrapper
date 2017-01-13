#coding: utf-8

import sqlite3

connection =  sqlite3.connect('database.db')
cursor = connection.cursor()

def initialize_new():
	cursor.execute('''CREATE TABLE urls_crawl (url, checked)''')
	cursor.execute('''CREATE TABLE urls (url, town, problem_rank)''')
	cursor.execute('''CREATE TABLE users (id, town, url1, url2, url3, url4, url5)''')
	cursor.execute('''CREATE TABLE synonyms (word, dictionary)''')
	connection.commit()

def close():
	connection.close()

def add_new_subject(subject):
	cursor.execute('''CREATE TABLE {} (word, no_occurances)'''.format(subject))

def get_word_dict(subject, synonim=False):
	word_dict = {}
	for i in cursor.execute('''SELECT * FROM '{}' '''.format(subject)):
		if not synonim:
			word_dict[i[0]] = float(i[1])
		else:
			word_dict[i[0]] = i[1].split()
	return word_dict

def add_word_dict(subject, word_dict):
	cursor.execute('''DROP TABLE {}'''.format(subject))
	cursor.execute('''CREATE TABLE {} (word, no_occurances)'''.format(subject))
	for i in word_dict:
		if type(word_dict[i]) is list:
			i_list_string = ''
			for word in word_dict[i]:
				i_list_string += ' {}'.format(i)

			execution = '''INSERT INTO {} (word, no_occurances) VALUES ('{}', '{}')'''.format(subject, i, i_list_string)
		
		else:
			execution = '''INSERT INTO {} (word, no_occurances) VALUES ('{}', '{}')'''.format(subject, i, word_dict[i])
		cursor.execute(execution)
	connection.commit()
	print("database updated")

def add_new_url_scrape(url):
	cursor.execute('''INSERT INTO urls_crawl VALUES ('{}', 'False')'''.format(url))
	connection.commit()

def add_new_url(url, town, problem_rank):
	cursor.execute('''INSERT INTO urls VALUES ('{}', '{}', '{}')'''.format(url, town, problem_rank))
	connection.commit()

def show_table(table_title):
	for i in cursor.execute('''SELECT * FROM '{}' '''.format(table_title)):
		print(i)

def drop(table):
	cursor.execute('''DROP TABLE {}'''.format(table))

def reset(): #test
	drop('articles')
	add_new_subject('articles')


def get_max(n):
	word_dict = get_word_dict('articles')
	for i in range(n):
		max_value = [i for i in word_dict if word_dict[i] == max(word_dict.values())]
		print(max_value[0])
		print(word_dict[max_value[0]])
		print("")
		word_dict[max_value[0]] = 0

#get_max(5)
#print(word_dict)
#add_word_dict('synonyms', {'halo': ['hej', 'ho']})

for i in cursor.execute('''SELECT * FROM 'synonyms' '''):
	print(i)