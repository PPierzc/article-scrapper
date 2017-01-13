# coding: UTF-8

# @Author: Paweł Pierzchlewicz
# @Project: ZWZT - Problem Search

'''Web crawler, który odbiera dane od scrapera i przetwarza je aby tworzyć bazę słów dla różnych tematów'''

#Takes title, splits it by ' ' and compares with imported dictionary of words

import web_scraper as ws
import database

import sys

urls = [["temp_url", True]]
useless_words = ['a', 'że', 'czy', 'na', 'i','z','to','lub', 'co', 'bo', 'w', 'się', 'tu', 'nie']
punctuation = [u',',u'.',u'"',u"'",u'?',u'!',u'-','/', ':', u'', '(', ')']

class Web_Crawler(object):

	#Global variables, or imported variables
	

	def __init__(self, url, life, action='s', synonym_dict={}): #'u' is unspuervised and 's' is supervised
#<------------------------Set Class Variables----------------------->
		self.url = url
		self.life = life
		self.word_dict = {}
		self.word_list = []
		self.url_list = []
		self.scrape_url = ws.Web_Scrapper(url)
		self.synonym_dict = synonym_dict

#<------------------------Making of the route----------------------->
	def new_route(self):
#Import urls from database
	
#Extract into a list
		
		for i in self.scrape_url.links_list:
			self.url_list.append(i)

#Update imported urls
		temp_vector = urls
		for i in self.url_list:
			for j in temp_vector:
				if i == j[0]:
					break
				elif j == urls[-1][0]:
					urls.append([i, False])

	
#When finished with rest of operations push a crawler (create new instance) into each url with life value decreased -------------------> TODO later
		for i in urls:
			if i[1] == False:
				crawl = Web_Crawler(i[0], self.life-1, 'u')

#<------------------------Word Vector----------------------->
	def word_vector(self, thread_name, normalized=False):
		self.thread_name = thread_name

#Import text
		self.words = self.scrape_url.word_list
		#print(self.words)
		temp = [item for sublist in self.words for item in sublist]
		#print(temp)
				#self.words.split()

#Set words
		for i in self.words:
			self.word_list.append(i.split())
		self.word_list = [item for sublist in self.word_list for item in sublist]

#Lower all letters
		self.word_list = [item.lower() for item in self.word_list]


#Remove punctuation
		temp_vector = self.word_list
		for ID, i in enumerate(temp_vector):
			for j in punctuation:
				if j in list(i):
					self.word_list[ID] = i.strip(j)
					break

#Remove useless words LETTER 'w' doesn't work
		#print(self.word_list)
		temp_vector = self.word_list
		for i in temp_vector:
			if len(i) > 3:
				continue
			for j in useless_words:
				if i == j:
					self.word_list.remove(i)
					break

#Set dictionary for words in title
		total_words = len(self.words)
		for i in self.word_list:

			if i in self.word_dict.keys():
				self.word_dict[i] += 1.
			else:
				self.word_dict[i] = 1.



#Save into a dicitonary key is the word, value is the list of synonims
		length_of_dict = float(len(self.word_dict))
		self.word_dict[u''] = 0
		del self.word_dict[u'']
		for count, i in enumerate(self.word_dict):
			if i not in self.synonym_dict:
				if(i != '/' or i != '.' or i != u''):
					self.synonym_dict[i] = self.find_synonyms(i)
				count = int((count/length_of_dict)*100)
				sys.stdout.write("{}: {}%\r".format(self.thread_name, count))
				sys.stdout.flush()
			
			

#Set dictionary of words in respect to synonims
		#print(self.word_list)
		for i in self.word_dict:
			for j in self.word_dict:
				for l in self.synonym_dict[j]:
					if i == l:
						self.word_dict[i] += self.word_dict[j]
						self.word_dict[j] = 0.
						break

		#Make set of synonims
		word_dict_syn = {}
		for i in self.word_dict:
			set_syn = set(i)
			set_syn.update(self.synonym_dict[i])
			set_syn = list(set_syn)
			word_dict_syn[i] = self.word_dict[i]
			

#Delete zero values
		self.cleared_word_dict = {}
		for i in word_dict_syn:
			if word_dict_syn[i] != 0:
				self.cleared_word_dict[i] = word_dict_syn[i]


#Normalize the vector
		word_dict_normalized = {}
		for i in self.cleared_word_dict:
			word_dict_normalized[i] = (self.cleared_word_dict[i]/total_words)*100

		return_dict = {}
		if not normalized:
			#{'spoleczny': [['spoleczenstwo', 'spolecznosc'],1]}
			for i in self.cleared_word_dict:
				return_dict[i] = [self.synonym_dict[i], self.cleared_word_dict[i]]
			return return_dict, self.synonym_dict

		else:
			
			for i in word_dict_normalized:
				return_dict[i] = [self.synonym_dict[i], word_dict_normalized[i]]
			return return_dict, self.synonym_dict

		#for i in word_dict_normalized:
		#	print("{:.2f}%: {} {} ".format(word_dict_normalized[i], i.encode('utf-8'), self.synonym_dict[i]))


	#<------------------------Find Synonyms----------------------->
	#Scrape synonim page for a word
	def find_synonyms(self, word):
		
		synonym_list = []
		if word != '.':
			synonyms = ws.Web_Scrapper(u"https://www.synonimy.pl/synonim/{}/".format(word), self.thread_name, True)
		synonyms = synonyms.get_synonym()
	#Place the synonims in a list of synonims
		for i in synonyms:
			synonym_list.append(i)
		return synonym_list

	#Unsupervised Learning
	def find(self, what):
		pass
#Compare words in title with dictionary of title words

#Return new dictionary

'''
crawl = Web_Crawler("http://literat.ug.edu.pl/amwiersz/0002.htm", 5)
#crawl.find_synonyms("Społeczeństwo")
print(crawl.word_vector(True))'''
