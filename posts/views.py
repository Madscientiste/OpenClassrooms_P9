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
        instance = model.objects.get(id=delete or edit)

        form = TicketForm if is_ticket else ReviewForm
        form = form(instance=instance)

        if delete:
            if not is_ticket:
                instance.ticket.is_blocked = False
                instance.ticket.save()
            instance.delete()

            return redirect("/posts")
        elif edit:
            return render(req, "posts/form.html", {"form": form, "form_type": "update"})


class ReviewPosts(LoginRequired, TemplateView):
    template_name = "posts/form.html"

    def get(self, req: HttpRequest, post_id):
        form = ReviewForm()
        ticket = Ticket.objects.filter(id=post_id).first()

        if not ticket:
            return redirect("/posts/request/")
        else:
            return render(req, self.template_name, {"form": form, "ticket": ticket})

    def post(self, req: HttpRequest, post_id):
        form = ReviewForm(req.POST, req.FILES)
        ticket = Ticket.objects.filter(id=post_id).first()

        if form.is_valid() and ticket:
            Review.objects.create(**form.cleaned_data, ticket=ticket, user=req.user)
            ticket.is_blocked = True
            ticket.save()
            return redirect("/posts/flux/")

        form_error = [f"{key.capitalize()} : {strip_tags(value)}" for key, value in form.errors.items()]
        return render(req, self.template_name, {"form": form, "form_error": form_error})


class CreatePost(LoginRequired, TemplateView):
    template_name = "posts/form.html"

    def get(self, req: HttpRequest):
        form = ReviewForm()
        return render(req, self.template_name, {"form": form})

    def post(self, req: HttpRequest):
        form = ReviewForm(req.POST, req.FILES)

        if form.is_valid():
            ticket = {**form.cleaned_data}
            del ticket["rating"]
            ticket = Ticket.objects.create(**ticket, user=req.user)

            rating = {**form.cleaned_data}
            del rating["image"]
            rating = Review.objects.create(**rating, ticket=ticket, user=req.user)

            return redirect("/posts/flux/")

        form_error = [f"{key.capitalize()} : {strip_tags(value)}" for key, value in form.errors.items()]
        return render(req, self.template_name, {"form": form, "form_error": form_error})


class RequestPost(LoginRequired, TemplateView):
    template_name = "posts/form.html"

    def get(self, req: HttpRequest):
        form = TicketForm()
        return render(req, self.template_name, {"form": form})

    def post(self, req: HttpRequest):
        form = TicketForm(req.POST, req.FILES)

        if form.is_valid():
            data = form.cleaned_data
            Ticket.objects.create(**data, user=req.user)

            return redirect("/posts/flux/")

        form_error = [f"{key.capitalize()} : {strip_tags(value)}" for key, value in form.errors.items()]
        return render(req, self.template_name, {"form": form, "form_error": form_error})
