from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Ticket(models.Model):
    is_blocked = models.BooleanField(default=False)
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="covers/")
    time_created = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    time_created = models.DateTimeField(auto_now_add=True)
