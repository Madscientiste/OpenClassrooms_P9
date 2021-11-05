from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path("ayayadmin/", admin.site.urls),
    path("acc/", include("accounts.urls")),
    path("posts/", include("posts.urls")),
    path("", views.HomePage.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
