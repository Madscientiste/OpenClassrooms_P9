from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.shortcuts import render
from django.views.generic.base import TemplateView

from accounts.views import LoginRequired
from posts.models import Review, Ticket
from accounts.models import UserFollows


class FluxPage(LoginRequired, TemplateView):
    template_name = "pages/flux.html"

    def get(self, req: HttpRequest):
        following = UserFollows.objects.filter(user=req.user)
        following = following.values_list("followed_user", flat=True)

        # add self to following so we can see our own reviews
        following = list(following) + [req.user.id]

        reviews = Review.objects.filter(user__in=following)
        tickets = Ticket.objects.filter(user__in=following)

        posts = [*reviews, *tickets]

        return render(req, self.template_name, {"posts": posts})
