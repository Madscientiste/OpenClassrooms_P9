from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.utils.html import strip_tags
from django.views.generic.base import TemplateView

from accounts.views import LoginRequired
from posts.models import Review, Ticket
from posts.forms import ReviewForm, TicketForm


class CreateReply(LoginRequired, TemplateView):
    template_name = "posts/form.html"

    def get(self, req: HttpRequest, post_id):
        form = ReviewForm()
        ticket = Ticket.objects.filter(id=post_id).first() if not post_id == "none" else None
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
