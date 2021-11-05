from django import forms
from .models import Review, Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class ReviewForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Review
        fields = ["title", "description", "rating"]
