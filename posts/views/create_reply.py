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
        review_form = ReviewForm()
        ticket_form = TicketForm()
        ctx = {}

        ticket = Ticket.objects.filter(id=post_id).first() if not post_id == "none" else None
        ctx["ticket"] = ticket
        ctx["review_form"] = review_form

        if not ticket:
            ctx["ticket_form"] = ticket_form

        return render(req, self.template_name, ctx)

    def post(self, req: HttpRequest, post_id):
        ctx = {}

        ticket = Ticket.objects.filter(id=post_id).first() if not post_id == "none" else None
        ctx["ticket"] = ticket

        review_form = ReviewForm(req.POST)
        ctx["review_form"] = review_form

        ctx["form_errors"] = []

        if not ticket:
            ticket_form = TicketForm(req.POST, req.FILES)
            ctx["ticket_form"] = ticket_form

            tf_valid = ticket_form.is_valid()
            rf_valid = review_form.is_valid()

            if rf_valid and tf_valid:
                ticket = Ticket.objects.create(**ticket_form.cleaned_data, is_blocked=True, user=req.user)
                Review.objects.create(**review_form.cleaned_data, ticket=ticket, user=req.user)
                return redirect("/")

            ctx["form_errors"] += [f"{key.capitalize()} : {strip_tags(value)}" for key, value in ticket_form.errors.items()]

        else:
            rf_valid = review_form.is_valid()

            if rf_valid:
                ticket.is_blocked = True
                Review.objects.create(**review_form.cleaned_data, ticket=ticket, user=req.user)
                ticket.save()

                return redirect("/")

            ctx["form_errors"] += [f"{key.capitalize()} : {strip_tags(value)}" for key, value in review_form.errors.items()]

        return render(req, self.template_name, ctx)
