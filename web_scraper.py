# coding: UTF-8

# @Author: Paweł Pierzchlewicz
# @Project: ZWZT - Problem Search

'''Web scraper z nastawieniem na wyszukiwanie problemów społecznych. Przekazywany do web crawler-a.'''

import requests
from bs4 import BeautifulSoup


class Web_Scrapper():
	def __init__(self, url, thread_name="none", synonym=False, town=False):
		
		s = requests.Session()
		s.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
		#print(url)
		self.page = s.get(url)
		self.soup = BeautifulSoup(self.page.content, "html.parser")

		if(synonym):
			self.synonym_list = []
			self.synonim = self.soup.find_all('a',class_= "load_word")
			for synonyms in self.synonim:
				self.synonym_list.append(synonyms.get_text())

		elif(town):
			self.meta_list = []
			for i in self.soup.find_all('meta'):
				self.meta_list.append(i.get('content'))
			

		else:
			self.links = self.soup.find_all("a")
			self.links_list = []
			for i in self.links:
				self.links_list.append(i.get('href'))
			self.words = self.soup.find_all("p")
			self.word_list = []
			for i in self.words:
				self.word_list.append(i.get_text())
			#self.date = self.soup.find_all("date")
			
		
		
		#print("{}: Scrape Successful".format(thread_name))

	def get_synonym(self):
		#print(self.synonym_list)
		return self.synonym_list

#for i in ['technologia', '/', 'technologia', 'technologia', 'technologia', 'technologia','technologia' ,'technologia']:
	#web_scraper = Web_Scrapper("https://www.synonimy.pl/synonim/{}/".format(i), True)
	#web_scraper.get_synonym()