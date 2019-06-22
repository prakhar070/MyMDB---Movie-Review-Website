from django.contrib import admin
from .models import Movie,Role, Person, MovieImage, Vote, Comment

# Register your models here.

admin.site.register(Movie)
admin.site.register(Role)
admin.site.register(Person)
admin.site.register(MovieImage)
admin.site.register(Vote)
admin.site.register(Comment)

