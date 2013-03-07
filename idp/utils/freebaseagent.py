import json
import urllib

class FreebaseAgent(object):
	"""Helper class to retrieve IMDb ids from freebase.

	Currently only supports movies. TV series support will 
	hopefully be added if need arises.
	"""

	def __init__(self):
		super(FreebaseAgent, self).__init__()
		self.API_KEY = 'YOUR-API-KEY-GOES-HERE' #TODO read these values from config
		self.topic_service_url = 'https://www.googleapis.com/freebase/v1/topic' 
		self.search_service_url = 'https://www.googleapis.com/freebase/v1/search'

	def getImdbId(self, movieName):
		"""Returns the IMDb id of a movie, given its title.

		The returned title is the one with the highest
		freebase confidence score.

		Returns None if no such movie exists in freebase.
		"""
		mid = self.getTopicId(movieName)
		topic = self.getTopic(mid)
		return topic

	def getTopicId(self, name, entityType='/film/film'):
		"""Gets the topic id (aka mid, freebase id) of a title. 
		"""
		params = {
		  'query': name,
		  'type': entityType,
		  'limit': 1
		}
		url = self.search_service_url + '?' + urllib.urlencode(params)
		response = json.loads(urllib.urlopen(url).read())

		for result in response.get('result'):
			mid = result.get('mid', None)
			return mid
		return None

	def getTopic(self, mid):
		"""Gets the IMDb id of a freebase topic. Returns None if no
		such thing exists.
		"""
		params = {
		  'filter': '/type/object/key'
		}
		url = self.topic_service_url + mid + '?' + urllib.urlencode(params)
		topic = json.loads(urllib.urlopen(url).read())

		for property in topic['property']:
		 	for value in topic['property'][property]['values']:
				if value['text'].startswith('/authority/imdb/title'):
					return value['text'].split('/')[-1]



if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(description="Retrieve imdb id from freebase.")
	parser.add_argument('movieName', help='The name of the movie')
	args = parser.parse_args()

	agent = FreebaseAgent()
	mid = agent.getTopicId(args.movieName)
	print 'freebase topic id (mid) is', mid
	topic = agent.getTopic(mid)
	print 'imdb id is', topic, 'so the url is http://www.imdb.com/title/'+topic
	print agent.getImdbId(args.movieName)