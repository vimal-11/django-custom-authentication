from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import Accounts


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = Accounts
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2' )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Accounts.objects.get(email=email)
        except Accounts.DoesNotExist:
            return email
        raise forms.ValidationError(f'Email {email} already exists.')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Accounts.objects.get(username=username)
        except Accounts.DoesNotExist:
            return username
        raise forms.ValidationError(f'Username {username} already exists.')


class AccountLoginForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Accounts
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")