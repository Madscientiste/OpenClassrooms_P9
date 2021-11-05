from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.LoginPage.as_view()),
    path("register/", views.RegisterPage.as_view()),
    path("logout/", views.LogoutUser.as_view()),
    path("follows/", views.FollowsPage.as_view()),
]
