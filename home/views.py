from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout


from accounts.models import Accounts


def home_screen(request):
	context = {}

	return render(request, "home/home.html", context)


@login_required
def profile_view(request, *args, **kwargs):
	context = {}
	user_id = kwargs.get("user_id")
	try:
		account = Accounts.objects.get(pk=user_id)
	except:
		return HttpResponse("User doesn't exist.")
	if account:
		context['id'] = account.id
		context['username'] = account.username
		context['email'] = account.email
		
		context['BASE_URL'] = settings.BASE_URL
		print(context)
		return render(request, "home/profile.html", context)
