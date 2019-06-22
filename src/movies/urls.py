from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	
	# urls relating to user login and registration
	path('', views.MovieList.as_view(template_name="movies/list.html"), name="list"),
	path('movie/<int:pk>', views.MovieDetail.as_view(template_name="movies/detail.html"), name="detail"),
	path('movie/<int:movie_id>/vote', views.CreateVote.as_view(), name="CreateVote"),
	path('movie/<int:movie_id>/vote/<int:pk>', views.UpdateVote.as_view(), name="UpdateVote"),
	path('movie/<int:movie_id>/image/upload', views.MovieImageUpload.as_view(), name="MovieImageUpload"),
	path('movie/<int:movie_id>/comment', views.AddComment.as_view(), name="AddComment"),
]