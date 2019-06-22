from django.core.management import BaseCommand
from movies.service import elasticsearch
from movies.models import Movie


#creating a custom management command
class Command(BaseCommand):
	help = 'Load all the movies into elasticsearch'

	def handle(self, *args, **options):
		queryset = Movie.objects.all()
		all_loaded = elasticsearch.bulk_load(queryset)
		if all_loaded:
			self.stdout.write(self.style.success('Successfully loaded all the movies into elasticsearch'))
		else:
			self.stdout.write(self.style.WARNING('Some movies not loaded Successfully, see logged errors'))
