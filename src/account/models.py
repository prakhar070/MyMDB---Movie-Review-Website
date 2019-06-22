from django.db import models
from django.conf import settings

# model to represent profile of MyMDB users
class Profile(models.Model):
	#including the user model in our model in a one to one way
	# we can access all the fields of a user using user.<fieldname> now
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	#additional fields
	date_of_birth = models.DateField(null=True)
	photo = models.ImageField(upload_to = 'users/%Y/%m/%d', blank=True, null=True)

