from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.utils.html import strip_tags
from django.views.generic.base import TemplateView

from accounts.views import LoginRequired
from posts.models import Review, Ticket
from posts.forms import ReviewForm, TicketForm


class FluxPage(LoginRequired, TemplateView):
    template_name = "pages/flux.html"

    def get(self, req: HttpRequest):
        tickets = Ticket.objects.all()
        reviews = Review.objects.all()

        posts = [*tickets, *reviews]

        return render(req, self.template_name, {"posts": posts})
