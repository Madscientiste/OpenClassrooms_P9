from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import URLField
from .models import User

avatar_example = "eg: https://cdn.myanimelist.net/images/userimages/5696390.jpg"


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "avatar")
