#this module contains elasticsearch specific code
import logging

from django.conf import settings
from elasticsearch import Elasticsearch, TransportError
from elasticsearch.helpers import streaming_bulk

FAILED_TO_LOAD_ERROR = 'Failed to load {}:{!r}'
logger = logging.getLogger(__name__)


def get_client():
	return Elasticsearch(hosts=[{'host':settings.ES_HOST,'port':settings.ES_PORT,}])

#loading our movie model into the Elasticsearch using streaming_bulk 
def bulk_load(movies):
	all_ok = True
	es_movies = (q.as_elasticsearch_dict() for q in movies)
	for ok,result in streaming_bulk(get_client(), es_movies, index=settings.ES_INDEX, raise_on_error=False):
		#in this step for loop will log any error that occurs while loading the movie
		if not ok:
			all_ok = False
			action, result = result.popitem()
			logger.error(FAILED_TO_LOAD_ERROR.format(result['_id'],result))
	return all_ok