from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.http import HttpRequest


class HomePage(LoginRequiredMixin, TemplateView):
    login_url = "acc/login/"

    def get(self, req: HttpRequest):
        return redirect("/posts/flux")
