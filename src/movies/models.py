from django.db import models
from django.db.models.aggregates import Sum
from django.conf import settings
from uuid import uuid4

# Create your models here.
'''
class PersonManager(models.Manager):
	def all_with_prefetched_movies(self):
		qs = self.get_queryset()
		qs = qs.prefetch_related('directed', 'writing_credits', 'roles')
		return qs
'''
class Person(models.Model):
	first_name = models.CharField(max_length = 140)
	last_name = models.CharField(max_length = 140)
	born = models.DateField()
	died = models.DateField(blank=True, null=True)
	#defining the custom made manager
	#objects = PersonManager()

	class Meta:
		ordering = ('last_name', 'first_name')

		def __str__(self):
			if self.died:
				return '{}, {} ({}-{})'.format(self.last_name, self.first_name, self.born, self.died)
			return '{}, {} ({})'.format(self.last_name, self.first_name, self.born)


'''
class MovieManager(models.Manager):

	def all_with_related_persons(self):
		qs = self.get_queryset()
		qs = qs.select_related('director')
		qs = qs.prefetch_related('writers', 'actors')
		return qs

	def all_with_related_persons_and_score(self):
		qs = self.all_with_related_persons()
		qs = self.prefetch_related('votes')
		return qs

	def top_movies(self, limit):
		qs = self.get_queryset()
		qs = qs.exclude(score=0)
		qs = qs.order_by('-score')
		qs = qs[:limit]
		return qs
'''

class Movie(models.Model):
	NOT_RATED = 0
	RATED_G = 1
	RATED_PG = 2
	RATED_R = 3
	RATINGS = ((NOT_RATED,'NR - NOT RATED'),(RATED_G, 'G - General Audiences'), (RATED_PG, 'PG - Parental Guidance'), (RATED_R, 'R - Restricted'))

	score = models.IntegerField(default=0, blank=True, null=True)
	visits = models.IntegerField(default=0, blank=True, null=True)
	title = models.CharField(max_length = 140)
	plot = models.TextField()
	year = models.PositiveIntegerField()
	rating = models.IntegerField(choices = RATINGS,default = NOT_RATED)
	runtime = models.PositiveIntegerField()
	website = models.URLField(blank= True)

	#relationships
	director = models.ForeignKey(to='Person', on_delete=models.SET_NULL, related_name='directed', null=True, blank=True)
	writers = models.ManyToManyField(to='Person', related_name='writing_credits', blank=True)
	actors = models.ManyToManyField(to='Person', through='Role',related_name='acting_credits', blank=True)
	
	#defining the custom made manager
	#objects = MovieManager()
	def as_elasticsearch_dict(self):
		return {
			'_id':self.id,
			'_type':'doc',
			'text':'{}\n{}'.format(self.title, self.plot),
			'title':self.title,
			'id':self.id,
			'year':self.year,
			'runtime':self.runtime,
		}

	class Meta:
		ordering = ('-year', 'title')

	def __str__(self):
		return '{} ({})'.format(self.title, self.year)



class Role(models.Model):
	movie = models.ForeignKey(to='Movie', related_name='roles', on_delete=models.DO_NOTHING)
	person = models.ForeignKey(to='Person',related_name='roles', on_delete=models.DO_NOTHING)
	name = models.CharField(max_length=140)

	def __str__(self):
		return "{} {} {} ".format(self.movie__id, self.person__id, self.name)

	class Meta:
		unique_together = ('movie', 'person', 'name')


class VoteManager(models.Manager):
	def get_vote_or_unsaved_blank_vote(self, movie, user):
		try:
			return Vote.objects.get(movie=movie, user=user)

		except Vote.DoesNotExist:
			return Vote(movie=movie, user=user)

			
class Vote(models.Model):
	CHOICES = ((1,"like"),(-1,"dislike"))
	value = models.SmallIntegerField(choices = CHOICES)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votes', on_delete = models.CASCADE )
	movie = models.ForeignKey(Movie, related_name='votes', on_delete = models.CASCADE)
	voted_on = models.DateField(auto_now = True)
	objects = VoteManager()
	#enforcing one person one vote for a particular movie
	class Meta:
		unique_together = ('user', 'movie')


class MovieImage(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
	image = models.ImageField(upload_to = 'images/%Y/%m/%d')
	uploaded = models.DateTimeField(auto_now_add = True)
	movie = models.ForeignKey(Movie, related_name="images",on_delete = models.CASCADE, blank=True)
