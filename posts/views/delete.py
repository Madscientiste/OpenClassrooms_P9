from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.utils.html import strip_tags
from django.views.generic.base import TemplateView

from accounts.views import LoginRequired
from posts.models import Review, Ticket
from posts.forms import ReviewForm, TicketForm


class DeletePost(LoginRequired, TemplateView):
    def get(self, req: HttpRequest, post_type, post_id):
        if post_type == "review" or post_type == "ticket":
            instance = Ticket if post_type == "ticket" else Review
            post = instance.objects.get(id=post_id)

            if post:
                if post_type == "ticket":
                    post.image.delete(save=True)
                else:
                    post.ticket.is_blocked = False
                    post.ticket.save()

                post.delete()

        return redirect("/posts/")
