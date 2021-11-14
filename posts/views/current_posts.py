from django.http.request import HttpRequest
from django.shortcuts import render
from django.views.generic.base import TemplateView

from accounts.views import LoginRequired
from posts.models import Review, Ticket


class CurrentPosts(LoginRequired, TemplateView):
    template_name = "posts/index.html"

    def get(self, req: HttpRequest):
        tickets = Ticket.objects.filter(user=req.user)
        reviews = Review.objects.filter(user=req.user)

        posts = [*tickets, *reviews]

        return render(req, self.template_name, {"posts": posts})
