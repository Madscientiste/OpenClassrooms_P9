from django.http.request import HttpRequest
from django.shortcuts import render
from django.views.generic.base import TemplateView

from accounts.views import LoginRequired
from posts.models import Review, Ticket


class FluxPage(LoginRequired, TemplateView):
    template_name = "pages/flux.html"

    def get(self, req: HttpRequest):
        tickets = Ticket.objects.all()
        reviews = Review.objects.all()

        posts = [*tickets, *reviews]

        return render(req, self.template_name, {"posts": posts})
