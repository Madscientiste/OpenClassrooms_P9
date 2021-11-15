from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.request import HttpRequest
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.db import IntegrityError

from .forms import SignUpForm
from .models import User, UserFollows


class LoginRequired(LoginRequiredMixin):
    login_url = "/acc/login"


class FollowsPage(LoginRequired, TemplateView):
    template_name = "pages/follows.html"

    def get_followers(self, user):
        followers = UserFollows.objects.filter(followed_user=user)
        return followers.values_list("user__username", flat=True)

    def get_following(self, user):
        following = UserFollows.objects.filter(user=user)
        return following.values_list("followed_user__username", flat=True)

    def get(self, req: HttpRequest):
        following = self.get_following(req.user)
        followers = self.get_followers(req.user)

        return render(req, self.template_name, {"following": following, "followers": followers})

    def post(self, req: HttpRequest):
        following = self.get_following(req.user)
        followers = self.get_followers(req.user)

        try_follow = req.POST.get("follow", None)
        un_follow = req.POST.get("un_follow", None)
        follow_back = req.POST.get("follow_back", None)

        error = None

        try:
            if try_follow or follow_back:
                user = User.objects.get(username=try_follow or follow_back)

                if user:
                    user_follows = UserFollows(user=req.user, followed_user=user)
                    user_follows.save()

            elif un_follow:
                user = User.objects.get(username=un_follow)

                if user:
                    obj = UserFollows.objects.filter(user=req.user, followed_user=user)
                    obj.delete()

        except IntegrityError:
            error = "You are already following this user"
        except User.DoesNotExist:
            error = "User does not exist"

        return render(req, self.template_name, {"error": error, "following": following, "followers": followers})


class RegisterPage(TemplateView):
    template_name = "accounts/register.html"

    def get(self, req: HttpRequest):
        register_form = SignUpForm()
        return render(req, self.template_name, {"form": register_form})

    def post(self, req: HttpRequest):
        register_form = SignUpForm(req.POST, req.FILES)

        if register_form.is_valid():
            user = register_form.save()
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
        username = req.POST.get("username", None)
        password = req.POST.get("password", None)

        user = authenticate(req, username=username, password=password)

        if user is not None:
            login(req, user)
            return redirect("/posts/flux/")

        return render(req, self.template_name, {"error": "Invalid username or password"})

class LogoutUser(TemplateView):
    def get(self, req: HttpRequest):
        logout(req)
        return redirect("/acc/login")
