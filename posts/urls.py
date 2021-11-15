from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.CurrentPosts.as_view()),
    path("flux/", views.FluxPage.as_view()),
    path("create/", views.CreateTicket.as_view()),
    path("reply/<str:post_id>", views.CreateReply.as_view()),
    path("edit/<str:post_type>/<str:post_id>", views.EditPost.as_view()),
    path("delete/<str:post_type>/<str:post_id>", views.DeletePost.as_view()),
]
