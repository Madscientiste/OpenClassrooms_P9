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
        tickets = Ticket.objects.filter(user=req.user)
        reviews = Review.objects.filter(user=req.user)

        posts = [*tickets, *reviews]

        return render(req, self.template_name, {"posts": posts})

    def post(self, req: HttpRequest):
        delete = req.POST.get("delete", None)
        edit = req.POST.get("edit", None)
        is_ticket = req.POST.get("type") == "ticket"

        model = Ticket if is_ticket else Review
        ticket = model.objects.get(id=delete or edit)

        form = TicketForm if is_ticket else ReviewForm
        form = form(instance=ticket)

        if delete:
            ticket.delete()
            return redirect("/posts")
        elif edit:
            return render(req, "posts/form.html", {"form": form, "form_type": "update"})


class ReviewPosts(LoginRequired, TemplateView):
    template_name = "posts/form.html"

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
        return render(req, self.template_name, {"ticket": ticket_form, "error": errors})


class CreatePost(LoginRequired, TemplateView):
    template_name = "posts/form.html"

    def get(self, req: HttpRequest):
        ticket_form = ReviewForm(req.POST, req.FILES)
        return render(req, self.template_name, {"form": ticket_form, "form_type": "create"})

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

        return render(req, self.template_name, {"form": ticket_form, "form_type": "create"})


class RequestPost(LoginRequired, TemplateView):
    template_name = "posts/form.html"

    def get(self, req: HttpRequest):
        ticket_form = TicketForm()
        return render(req, self.template_name, {"form": ticket_form, "form_type": "request"})

    def post(self, req: HttpRequest):
        ticket_form = TicketForm(req.POST, req.FILES)

        if ticket_form.is_valid():
            data = ticket_form.cleaned_data
            Ticket.objects.create(**data, user=req.user)

            return redirect("/posts/flux/")

        errors = [f"{key.capitalize()} : {strip_tags(value)}" for key, value in ticket_form.errors.items()]
        return render(req, self.template_name, {"form": ticket_form, "form_type": "request", "errors": errors})
