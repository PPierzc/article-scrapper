# coding: utf-8

import scipy.spatial.distance as dist

import web_scraper as ws

class Town_Determine(object):
	"""docstring for Town_Determine"""
	def __init__(self, town, town_global_coordinates):
		self.town = town
		self.tgc = town_global_coordinates

	def get_coordinates(self):
		url = 'https://www.google.pl/maps/place/{}'.format(self.town)
		scrape = ws.Web_Scrapper(url, town=True)
		#print(scrape.meta_list)
		for i in scrape.meta_list:
			if 'https://maps.google.com/maps/api/staticmap' in i:
				meta = i
		meta_list = meta.split('&')
		for i in meta_list:
			if 'center' in i:
				i = i.split('=')
				i = i[1].split('%2C')
				self.coordinates = [float(i[0]), float(i[1])]

	def determine_closest(self):
		self.get_coordinates()
		distances = {}
		for i in self.tgc:
			distances[i] = dist.euclidean(self.coordinates, self.tgc[i])

		smallest_dist = min(distances.values())
		closest_town = [k for k in distances if distances[k] == smallest_dist]
		print(closest_town)


td = Town_Determine('Świnoujście', {'Warsaw': [52.232606289062204, 20.781016711291045], 'Gdańsk': [54.360762957249314, 18.40835349339906], 'Kraków': [50.0464284278981, 19.724694226515123]})

td.determine_closest()
		