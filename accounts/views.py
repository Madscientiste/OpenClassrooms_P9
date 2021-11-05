from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.request import HttpRequest
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import SignUpForm


class LoginRequired(LoginRequiredMixin):
    login_url = "/acc/login"


class FollowsPage(LoginRequired, TemplateView):
    template_name = "pages/follows.html"

    def get(self, req: HttpRequest):
        print(req.user.avatar_url)
        return render(req, self.template_name)


class RegisterPage(TemplateView):
    template_name = "accounts/register.html"

    def get(self, req: HttpRequest):
        register_form = SignUpForm()
        return render(req, self.template_name, {"form": register_form})

    def post(self, req: HttpRequest):
        register_form = SignUpForm(req.POST)

        if register_form.is_valid():
            user = register_form.save()
            user.refresh_from_db()

            user.save()
            raw_password = register_form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=raw_password)
            login(req, user)

            return redirect("/posts/flux/")

        return render(req, self.template_name, {"form": register_form})


class LoginPage(TemplateView):
    template_name = "accounts/login.html"

    def get(self, req: HttpRequest):
        print(req.user.is_authenticated)

        return render(req, self.template_name)

    def post(self, req: HttpRequest):
        username = req.POST["username"]
        password = req.POST["password"]

        user = authenticate(req, username=username, password=password)

        if user:
            print("attempting to login the user")
            login(req, user)

            return redirect("/posts/flux/")
        else:
            return render(req, self.template_name, {"error": "wrong password or username"})


class LogoutUser(TemplateView):
    def get(self, req: HttpRequest):
        logout(req)
        return redirect("/acc/login")
