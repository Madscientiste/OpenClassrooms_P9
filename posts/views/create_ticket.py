from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.utils.html import strip_tags
from django.views.generic.base import TemplateView

from accounts.views import LoginRequired
from posts.models import Review, Ticket
from posts.forms import ReviewForm, TicketForm


class CreateTicket(LoginRequired, TemplateView):
    template_name = "posts/form.html"

    def get(self, req: HttpRequest) -> HttpRequest:
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
