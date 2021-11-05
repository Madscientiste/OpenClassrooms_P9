from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.CurrentPosts.as_view()),
    path("create/", views.CreatePost.as_view()),
    path("review/<str:post_id>", views.ReviewPosts.as_view()),
    path("request/", views.RequestPost.as_view()),
    path("flux/", views.FluxPage.as_view()),
]
