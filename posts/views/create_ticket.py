from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.utils.html import strip_tags
from django.views.generic.base import TemplateView

from accounts.views import LoginRequired
from posts.models import Ticket
from posts.forms import TicketForm


class CreateTicket(LoginRequired, TemplateView):
    template_name = "posts/form.html"

    def get(self, req: HttpRequest) -> HttpRequest:
        ticket_form = TicketForm()
        return render(req, self.template_name, {"ticket_form": ticket_form})

    def post(self, req: HttpRequest):
        ticket_form = TicketForm(req.POST, req.FILES)

        if ticket_form.is_valid():
            data = ticket_form.cleaned_data
            Ticket.objects.create(**data, user=req.user)

            return redirect("/posts/flux/")

        form_error = [f"{key.capitalize()} : {strip_tags(value)}" for key, value in ticket_form.errors.items()]
        return render(req, self.template_name, {"ticket_form": ticket_form, "form_errors": form_error})
