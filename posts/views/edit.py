from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.utils.html import strip_tags
from django.views.generic.base import TemplateView

from accounts.views import LoginRequired
from posts.models import Review, Ticket
from posts.forms import ReviewForm, TicketForm


class EditPost(LoginRequired, TemplateView):
    template_name = "posts/form.html"

    def get(self, req: HttpRequest, post_type, post_id):
        if post_type == "review" or post_type == "ticket":
            instance = Ticket if post_type == "ticket" else Review
            form = TicketForm if post_type == "ticket" else ReviewForm

            post = instance.objects.get(id=post_id)

            if post:
                form = form(instance=post)
                return render(
                    req,
                    self.template_name,
                    {"form": form, "post": post, "ticket": getattr(post, "ticket", None)},
                )

        return redirect("/posts/")

    def post(self, req: HttpRequest, post_type, post_id):
        if post_type == "review" or post_type == "ticket":
            instance = Ticket if post_type == "ticket" else Review
            form = TicketForm if post_type == "ticket" else ReviewForm

            post = instance.objects.get(id=post_id)

            if post:
                form = form(req.POST, instance=post)

                if form.is_valid():
                    form.save()
                    return redirect("/posts/")
                else:
                    form_error = [f"{key.capitalize()} : {strip_tags(value)}" for key, value in form.errors.items()]
                    return render(
                        req,
                        self.template_name,
                        {"form": form, "post": post, "ticket": getattr(post, "ticket", None), "form_error": form_error},
                    )

        return redirect("/posts/")
