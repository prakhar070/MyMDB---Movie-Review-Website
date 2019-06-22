from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import FormMixin
from .models import Movie,Person,Vote
from .forms import VoteForm,MovieImageForm, CommentForm
from django.core.exceptions import ValidationError
from taggit.models import Tag
#from .models import Vote
from django.db.models import F
from django.db.models import Count
# Create your views here.

#view displaying a list of movies
class MovieList(ListView):
	model = Movie
	paginate_by = 10
	sort_by = None
	tag = None

	def get_queryset(self):
		self.sort_by = self.request.GET.get('sort_by')
		self.tag = self.request.GET.get('tag')
		queryset = Movie.objects.all()
				

		print ("sort_by and tag are {} {}".format(self.sort_by, self.tag))
		if self.sort_by == 'Rating':
			queryset = queryset.order_by('-score')
		elif self.sort_by == 'Popularity':
			queryset = queryset.order_by('-visits')
		elif self.sort_by == 'Latest':
			queryset = queryset.order_by('-year')

		if self.tag is not None:
			tag = get_object_or_404(Tag, slug=self.tag)
			queryset = queryset.filter(tags__in=[tag])

		return queryset


	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx['tags'] = Movie.tags.all() 
		ctx['sort_by'] = self.sort_by
		ctx['tag'] = self.tag
		return ctx


class MovieDetail(DetailView):
	queryset = Movie.objects.all()

	#overriding the base class function
	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		#updating the visits field of the movie object
		Movie.objects.filter(id=self.kwargs['pk']).update(visits=F('visits')+1)
		similar_tags = self.object.tags.values_list('id', flat=True)
		similar_movies = Movie.objects.filter(tags__in=similar_tags).exclude(id=self.object.id)
		similar_movies = similar_movies.annotate(same_tags=Count('tags')).order_by('-same_tags','-year')[:4]
		if self.request.user.is_authenticated:
			# to fetch object due to SingleObjectMixin of detailView
			imageform = MovieImageForm({'user': self.request.user.id, 'movie':self.kwargs['pk'] })
			commentform = CommentForm()
			vote = Vote.objects.get_vote_or_unsaved_blank_vote(movie=self.object, user=self.request.user)
			if vote.id:
				vote_form_url = reverse('UpdateVote', kwargs={'movie_id':vote.movie.id, 'pk':vote.id})
			else:
				vote_form_url = reverse('CreateVote', kwargs={'movie_id':self.object.id})

			#we could have done something like if form.isvalid in order to check the validity of the form
			vote_form = VoteForm(instance=vote)
			ctx['vote_form']=vote_form
			ctx['vote_form_url']=vote_form_url
			ctx['imageform']=imageform
			ctx['commentform']=commentform
		ctx['similar_movies'] = similar_movies
		return ctx
	

class CreateVote(LoginRequiredMixin, CreateView):
	form_class = VoteForm

	def get_initial(self):
		# url of the form : movie/<int:movie_id>/vote
		initial = super().get_initial()
		#for providing initial values to the form
		initial['user'] = self.request.user
		initial['movie'] = Movie.objects.get(id=self.kwargs['movie_id'])
		return initial

	#after success go to this url
	def get_success_url(self):
		movie_id = self.kwargs['movie_id']
		return reverse('detail', kwargs={'pk':movie_id})

	def form_valid(self, form):
		Movie.objects.filter(id=self.kwargs['movie_id']).update(score = F('score')+int(form.cleaned_data['value']))
		return super().form_valid(form)

	#if the form was invalid then go to this url
	def render_to_response(self, context=None, **response_kwargs):
		movie_id = self.kwargs['movie_id']
		return redirect(to = reverse('detail', kwargs={'pk':movie_id}))


class UpdateVote(LoginRequiredMixin, UpdateView):
	#url form - movie/<int:movie_id>/vote/<int:pk>
	form_class = VoteForm
	queryset = Vote.objects.all()

	def get_object(self, queryset=None):
		vote = super().get_object(queryset)
		user = self.request.user
		if vote.user != user:
			raise PermissionDenied('cannot change another person\'s vote')
		return vote	

	def form_valid(self, form):
		movie = Movie.objects.get(id=self.kwargs['movie_id'])
		if int(form.cleaned_data['value']) != Vote.objects.get(movie=movie,user=self.request.user).value:
			Movie.objects.filter(id=self.kwargs['movie_id']).update(score = F('score')+2*int(form.cleaned_data['value']))
		return super().form_valid(form)

	#after success go to this url
	def get_success_url(self):
		movie_id = self.kwargs['movie_id']
		return reverse('detail', kwargs={'pk':movie_id})

	#if the form was invalid then go to this url
	def render_to_response(self, context, **response_kwargs):
		return redirect(to = reverse('detail', kwargs={'pk':movie_id}))


class MovieImageUpload(LoginRequiredMixin, CreateView):
	form_class = MovieImageForm

	def render_to_rerrrrrrsponse(self, context, **response_kwargs):
		movie_id = self.kwargs['movie_id']
		return redirect(to=reverse('detail', kwargs={'pk':movie_id}))

	def get_success_url(self):
		movie_id = self.kwargs['movie_id']
		return reverse('detail', kwargs={'pk':movie_id})

class AddComment(LoginRequiredMixin, CreateView):
	form_class = CommentForm

	def get_initial(self):
		# url of the form : movie/<int:movie_id>/vote
		initial = super().get_initial()
		#for providing initial values to the form
		initial['user'] = self.request.user.id
		initial['movie'] = self.kwargs['movie_id']
		return initial

	#after success go to this url
	def get_success_url(self):
		movie_id = self.kwargs['movie_id']
		return reverse('detail', kwargs={'pk':movie_id})

	def get_form_kwargs(self):
		kwargs = {
			'initial': self.get_initial(),
			'prefix': self.get_prefix(),
		}

		if self.request.method in ('POST', 'PUT'):
			kwargs.update({
				'data': self.request.POST,
				'files': self.request.FILES,
			})
		print("kwargs are {}".format(kwargs))
		return super().get_form_kwargs()

	#if the form was invalid then go to this url
	def render_to_response(self, context=None, **response_kwargs):
		movie_id = self.kwargs['movie_id']
		return redirect(to = reverse('detail', kwargs={'pk':movie_id}))







