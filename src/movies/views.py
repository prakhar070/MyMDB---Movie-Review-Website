from django.shortcuts import render, reverse, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import FormMixin
from .models import Movie,Person,Vote
from .forms import VoteForm,MovieImageForm
from django.core.exceptions import ValidationError

#from .models import Vote
from django.db.models import F
# Create your views here.

#view displaying a list of movies
class MovieList(ListView):
	model = Movie
	paginate_by = 10

	def get_queryset(self):
		sort_by = self.request.GET.get('sort_by')
		if sort_by is None:
			return Movie.objects.all()
		elif sort_by == 'Rating':
			return Movie.objects.all().order_by('-score')
		elif sort_by == 'Popularity':
			return Movie.objects.all().order_by('-visits')
		elif sort_by == 'Latest':
			return Movie.objects.all().order_by('-year')


class MovieDetail(DetailView):
	queryset = Movie.objects.all()

	#overriding the base class function
	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		#updating the visits field of the movie object
		Movie.objects.filter(id=self.kwargs['pk']).update(visits=F('visits')+1)

		if self.request.user.is_authenticated:
			# to fetch object due to SingleObjectMixin of detailView
			imageform = MovieImageForm({'user': self.request.user.id, 'movie':self.kwargs['pk'] })
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





