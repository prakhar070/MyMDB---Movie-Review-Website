from django.http import HttpResponse
from django.shortcuts import reverse, render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile


# view to register a new person
def register(request):
	if request.method == "POST":
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()
			#associating the user with an empty profile
			Profile.objects.create(user=new_user)
			print("yipeeeeeeeeeeeeeeeee")
			return render(request, "account/register_done.html",{'new_user':new_user} )
	else:
		print("whaccccccckkkkkkkkkkkkkkkkk")
		user_form = UserRegistrationForm()
	return render(request, "account/register.html", {'user_form':user_form})


@login_required
def edit(request):
	#request.user gives the user associated with the request
	if request.method == "POST":
		user_form = UserEditForm(instance=request.user, data=request.POST)
		profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Profile Updated Successfully ')
		else:
			messages.error(request, 'Error Updating your profile')
			
	else:
		#we are assigning an instance to the user
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)

	return render(request, 'account/edit.html', {'user_form':user_form,'profile_form':profile_form})
