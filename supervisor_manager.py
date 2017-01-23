# coding: UTF-8

# @Author: Paweł Pierzchlewicz
# @Project: ZWZT - Problem Search

import threading

import web_crawler as wc
import problem_rank as functions
import database

import sys

class Supervisor_Manager(object):

	def __init__(self, subject):
		self.subject = subject
		self.database = [['problem', database.get_word_dict('articles')]] #'''subject title, dictionary for this subject'''
		print(self.database)
		self.subject_vectors = []
		self.synonym_dict = database.get_word_dict('synonyms', True)
		self.synonym_dict[0] = []
		self.crawl_url_list = []

	def get_vector(self, url, thread_name):
		self.url = url
		crawl = wc.Web_Crawler(self.url, 5, synonym_dict=self.synonym_dict)
		crawl.new_route()
		self.crawl_url_list.append(crawl.url_list)
		self.crawl_vector = crawl.word_vector(thread_name)
		self.synonym_dict.update(self.crawl_vector[1])
		return self.crawl_vector[0]

	def update_subject(self, url, thread_name):
		subject_dict = {}
		for i in self.database:
			if i[0] == self.subject:
				subject_dict = i[1]
			else:
				subject_dict = {}

		subject_dict = functions.word_vector(self.get_vector(url, thread_name), subject_dict, 1)

		self.subject_vectors.append([self.subject, subject_dict])

	def update_database(self):

		subject_dict = {0:0}
		length = len(self.subject_vectors)
		print(length)
		for i in range(0,length):
			m = self.subject_vectors[i]
			for j in range(i, length):
				j = self.subject_vectors[j]
				if m[0] == j[0]:
					for l in m[1]:
						synonims = False
						for k in j[1]:
							print(l)
							print(k)
							if l == k:
								synonims = True
								if l in subject_dict:
									subject_dict[l] += (m[1][l] + j[1][k])
									j[1][k] = 0.0
									m[1][l] = 0.0
								else:
									subject_dict[l] = (m[1][l] + j[1][k])
									j[1][k] = 0.0
									m[1][l] = 0.0
					
						if synonims is False:						
							if l in subject_dict:
								subject_dict[l] += m[1][l]
							else:
								subject_dict[l] = m[1][l]
							if k in subject_dict:
								subject_dict[k] += j[1][k]
							else:
								subject_dict[k] = j[1][k]
		

		for i in subject_dict:
			for j in subject_dict:
				for l in self.synonym_dict[j]:
					if i == l:
						subject_dict[i] += subject_dict[j]
						subject_dict[j] = 0.0
						break


		cleared_subject_dict = {}
		for i in subject_dict:
			if subject_dict[i] != 0.0:
				cleared_subject_dict[i] = subject_dict[i]

		print(subject_dict)

		#normalize
		total = 0.0
		for i in cleared_subject_dict:
			total += cleared_subject_dict[i]

		normalized_dict = {}
		for i in cleared_subject_dict:
			normalized_dict[i] = cleared_subject_dict[i]/total

		for ID, i in enumerate(self.database):
			if i[0] == self.subject:
				self.database[ID] = [self.subject, cleared_subject_dict] #normalized_dict]
			elif i == self.database[-1]:
				self.database.append([self.subject, cleared_subject_dict]) #normalized_dict])

		#print("The finished database: {}".format(self.database))

	def add_urls(self, url_database, urls_scrape):
		for i in urls_scrape:
			if i not in url_database:
				database.add_new_url_scrape(i)

	def add_synonims(self):
		database.add_word_dict('synonim', self.synonym_dict)


sup = Supervisor_Manager('problem')


#printing logo
print(' ______   _____    _______   _______   _____   _____   _____  ')
print('|__  __| |  _  \  |  ___  | |  ___  | |  _  \ |  ___| |  _  \\')
print('  |  |   | |_| |  | |   | | | |   | | | |_| | | |__   | |_| |')
print('  |  |   |  _  /  | |   | | | |   | | |  ___/ |  __|  |  _  /')
print('  |  |   | | \ \  | |___| | | |___| | | |     | |___  | | \ \\')
print('  |__|   |_|  \_\ |_______| |_______| |_|     |_____| |_|  \_\ \n')

#create new subject (temporary)

#multi threading same problem 
#'http://wiadomosci.gazeta.pl/wiadomosci/7,114883,21197367,historyk-wykluczony-z-debaty-po-telefonie-z-ministerstwa-praktyki.html', 'http://wiadomosci.gazeta.pl/wiadomosci/7,114883,21200424,owsiak-chwali-sie-darami-od-gen-rozanskiemu-przekazal-wosp.html', 
urls = ['http://next.gazeta.pl/next/7,151243,21197966,gigantyczny-robot-na-granicy-korei-polnocnej-czerpie-z-transformersow.html']
#urls= ['http://dziennikzachodni.pl/artykul/3935309,dopalacze-mocarz-niszcza-mozg-handlarze-z-katowic,id,t.html', 'http://dziennikzachodni.pl/artykul/9016949,pzemoc-w-szkole-to-problem,id,t.html', 'http://polskatimes.pl/artykul/3934563,dopalaczami-mocarz-handlowali-18letnia-dziewczyna-i-20letni-chlopak,id,t.html']
#urls = ['http://literat.ug.edu.pl/amwiersz/0022.htm', 'http://literat.ug.edu.pl/amwiersz/0002.htm', 'http://wiadomosci.onet.pl/tylko-w-onecie/onet-ujawnia-jak-mateusz-kijowski-wystawial-faktury-kod-owi/wjrnf73', 'http://eurosport.onet.pl/zimowe/skoki-narciarskie/turniej-czterech-skoczni-swietne-wiesci-z-innsbrucka-kamil-stoch-nie-ma-zlaman/1nwjd2', 'http://biznes.onet.pl/gielda/wiadomosci/rafal-antczak-kim-jest-nowy-prezes-gpw-liberalny-ekonomista/j3dlst']

#Prepare url list for multithreading
length_urls = len(urls)


threads = []

#Assign urls to threads\
count = 0
for i in urls:
	count += 1

	if count <= 3:
		threads.append(threading.Thread(target = sup.update_subject, args = (i, "Thread-{}".format(count))))
	else:
		#print(threads)
		count = 1
		for thread in threads:
			thread.start()
			
		for thread in threads:
			thread.join()

		threads = []
			
		thread_database = threading.Thread(target = sup.update_database)
		thread_database.start()
		thread_database.join()
		threads.append(threading.Thread(target = sup.update_subject, args = (i, "Thread-{}".format(count))))

	if i == urls[-1]:
		count = 0
		for thread in threads:
			thread.start()
		
		for thread in threads:
			thread.join()

		threads = []
			
		thread_database = threading.Thread(target = sup.update_database)
		thread_database.start()
		thread_database.join()

	database.add_word_dict('synonyms', sup.synonym_dict)

print("The elements that are to be updated: {}".format(sup.database))
database.add_word_dict('articles', sup.database[-1][-1])

'''set_url = set()
set_url.add(tuple(sup.crawl_url_list))
set_url = list(set_url)
sup.add_urls(database.get_word_dict('urls_crawl'))
'''
'''except Exception, e:
	print("ERROR: Unable to execute new thread")
	print(e)'''