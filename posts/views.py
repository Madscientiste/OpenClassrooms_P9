from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.utils.html import strip_tags
from django.views.generic.base import TemplateView

from accounts.views import LoginRequired
from .models import Review, Ticket
from .forms import ReviewForm, TicketForm


class FluxPage(LoginRequired, TemplateView):
    template_name = "pages/flux.html"

    def get(self, req: HttpRequest):
        tickets = Ticket.objects.all()
        reviews = Review.objects.all()

        posts = [*tickets, *reviews]

        return render(req, self.template_name, {"posts": posts})


class CurrentPosts(LoginRequired, TemplateView):
    template_name = "posts/index.html"

    def get(self, req: HttpRequest):
        return render(req, self.template_name)


class ReviewPosts(LoginRequired, TemplateView):
    template_name = "posts/create.html"

    def get(self, req: HttpRequest, post_id):
        ticket = Ticket.objects.filter(id=post_id).first()

        if not ticket:
            return redirect("/posts/request/")
        else:
            return render(req, self.template_name, {"ticket": ticket})

    def post(self, req: HttpRequest, post_id):
        ticket_form = ReviewForm(req.POST, req.FILES)
        ticket = Ticket.objects.filter(id=post_id).first()

        if ticket_form.is_valid() and ticket:
            rating = {**ticket_form.cleaned_data}
            del rating["image"]
            rating = Review.objects.create(**rating, ticket=ticket, user=req.user)

            return redirect("/posts/flux/")

        errors = [f"{key.capitalize()} : {strip_tags(value)}" for key, value in ticket_form.errors.items()]
        return render(req, self.template_name, {"errors": errors})


class CreatePost(LoginRequired, TemplateView):
    template_name = "posts/create.html"

    def get(self, req: HttpRequest):
        return render(req, self.template_name)

    def post(self, req: HttpRequest):
        ticket_form = ReviewForm(req.POST, req.FILES)

        if ticket_form.is_valid():
            ticket = {**ticket_form.cleaned_data}
            del ticket["rating"]
            ticket = Ticket.objects.create(**ticket, user=req.user)

            rating = {**ticket_form.cleaned_data}
            del rating["image"]
            rating = Review.objects.create(**rating, ticket=ticket, user=req.user)

            return redirect("/posts/flux/")

        errors = [f"{key.capitalize()} : {strip_tags(value)}" for key, value in ticket_form.errors.items()]
        return render(req, self.template_name, {"errors": errors})


class RequestPost(LoginRequired, TemplateView):
    template_name = "posts/request.html"

    def get(self, req: HttpRequest):
        return render(req, self.template_name)

    def post(self, req: HttpRequest):
        ticket_form = TicketForm(req.POST, req.FILES)

        if ticket_form.is_valid():
            data = ticket_form.cleaned_data
            Ticket.objects.create(**data, user=req.user)

            return redirect("/posts/flux/")

        errors = [f"{key.capitalize()} : {strip_tags(value)}" for key, value in ticket_form.errors.items()]
        return render(req, self.template_name, {"errors": errors})
