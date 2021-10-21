from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout


from accounts.models import Accounts


def home_screen(request):
	context = {}
	#context['debug_mode'] = settings.DEBUG
	#context['debug'] = DEBUG
	#context['room_id'] = "1"
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
		
			
		# Set the template variables to the values
		#context['is_self'] = is_self
		#context['is_friend'] = is_friend
		#context['request_sent'] = request_sent
		#context['friend_requests'] = friend_requests
		context['BASE_URL'] = settings.BASE_URL
		print(context)
		return render(request, "home/profile.html", context)
