from accounts.models import Accounts
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from .tokens import generate_token

from .forms import RegistrationForm, AccountLoginForm



def signup_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated: 
        return HttpResponse("You are already authenticated as " + str(user.email))

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            form.save()
            #account = authenticate(email=email, password=raw_password)
            #login(request, account)
            #destination = get_redirect_if_exists(request)
            #if destination:
            #	return redirect(destination)
            #return redirect('home')
            new_user = Accounts.objects.get(email=email, username=username)
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.is_active = False

            new_user.save()

            current_site = get_current_site(request)
            email_subject = "Carsify- Confirmation Mail!"
            message = render_to_string('accounts/email_confirmation.html',{
                    'name': new_user.username,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                    'token': generate_token.make_token(new_user)
            })
            email = EmailMessage(
                email_subject, 
                message,
                settings.EMAIL_HOST_USER,
                [new_user.email],
            )
            email.fail_silently = True
            email.send()

            return render(request, 'accounts/signup_verify.html', {'name': new_user.username})


        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'accounts/signup.html', context)




def login_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated: 
        return redirect("home:home")

    if request.POST:
        form = AccountLoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect("home:home")
        else:
             context['login_form'] = form
        
    else:
        form = AccountLoginForm()
        context['login_form'] = form

    return render(request, "accounts/login.html", context)




@login_required
def logout_view(request):
	logout(request)
	return redirect("home:home")



def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect




def verify(request):
     return render(request, 'accounts/signup_verify.html')




def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        new_user = Accounts.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, Accounts.DoesNotExist):
        new_user = None

    if new_user is not None and generate_token.check_token(new_user, token):
        new_user.is_active = True
        new_user.save() 
        return redirect('accounts:login')
    else:
        return HttpResponse("Activation Failed!")