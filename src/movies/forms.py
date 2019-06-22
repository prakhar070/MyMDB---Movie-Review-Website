from django import forms
from django.db.models import Count
from .models import Vote, Movie, MovieImage, Comment
from django.contrib.auth import get_user_model 
#from django.core.validators import MaxValueValidator

class VoteForm(forms.ModelForm):
	user = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=get_user_model().objects.all())
	movie = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=Movie.objects.all())
	value = forms.ChoiceField(widget=forms.RadioSelect, choices=Vote.CHOICES, label='Vote')

	class Meta:
		model = Vote
		fields = ('value','user','movie')


class MovieImageForm(forms.ModelForm):
	user = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=get_user_model().objects.all())
	movie = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=Movie.objects.all())

	class Meta:
		model = MovieImage
		fields = ('user', 'movie','image')


class CommentForm(forms.ModelForm):
	user = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=get_user_model().objects.all())
	movie = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=Movie.objects.all())

	class Meta:
		model = Comment
		fields = ('user','movie', 'body')

