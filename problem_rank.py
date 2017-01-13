# coding: UTF-8

# @Author: Paweł Pierzchlewicz
# @Project: ZWZT - Problem Search

#import tables with word vectors
# coding: utf-8
import math

problem_spoleczny_dict = {'projekt': 0.2, 'spoleczenstwo': 0.7, 'działamy': 0.06, 'wilki': 0.04} #Imported table {word:10, word:11, etc.}
ekologia_dict = {'ziemia': 0.7, 'węgiel': 0.04, 'zagrozenie': 0.06}
word_vectors = [['problem_spoleczny', problem_spoleczny_dict],['Ekologia', ekologia_dict]]
__word_vector = {'projekt': 0.2, 'ekologia': 0.5, 'spoleczny': 0.3, 'chleb': 0.0}

def problem_rank(word_vector, synonyms):
	layer1 = word_vectors
	layer2 = []

	for i in layer1: #Create a vector with max values for each word_vector
		temp_problem_rank = 0
		for j in i[1]:
			for l in word_vector:
				if j in synonyms[l] or l == j: #Checks for synonyms
					temp_problem_rank += math.log(word_vector.get(l)**0.6 + 1)*i[1].get(j)
					break
		layer2.append([temp_problem_rank, i[0]])

#	print(layer2)
	max_value = max(layer2)
	return max_value

#print(problem_rank(__word_vector, {'spoleczny': ['spoleczenstwo', 'spolecznosc'], 'projekt':['dzialanie', 'biznes'], 'ekologia':['zielen', 'co2', 'ziemia'], 'chleb':['bułka', 'pieczywo']}))

def word_vector(words, subject_dict_un, learning_iter):

	#print(subject_dict_un)
	#Add the words to the subject
	words_keys = words.keys()
	total_words = len(words_keys)

		#Set for synonyms
	temp_words = words
	for i in words_keys:
		for j in words_keys:
			if i in words.keys():
				for l in words[i][0]:
					if j == l:
						words[i][1] += words[j][1]
						del words[j]
						break

	words_keys = words.keys()

	for i in words_keys:
		for k in range(0, int(words[i][1])):
			if i in subject_dict_un.keys():
				#print(subject_dict_un[i])
				subject_dict_un[i] += float(subject_dict_un[i]) + (0.9)**(learning_iter-1)
			else:
				subject_dict_un[i] = 1.0

	learning_iter += 1

	#Get total length
	total_value = 0
	for i in subject_dict_un:
		total_value += float(subject_dict_un[i]) 

	#Normalize the vector
	'''subject_dict_normalized = {}
	for i in subject_dict_un:
		subject_dict_normalized[i] = subject_dict_un[i]/total_value'''

	return subject_dict_un#_normalized

#print(word_vector({'spoleczny': [['spoleczenstwo', 'spolecznosc'],1], 'projekt':[['dzialanie', 'biznes','oj'],1], 'ekologia':[['zielen', 'co2', 'ziemia'],1], 'chleb':[['bułka', 'pieczywo'],1], 'pieczywo':[['chleb', 'bułka'],1]}, {}, 1))
