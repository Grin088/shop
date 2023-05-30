from django import forms
from .models import Review


class ReviewFrom(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5, required=True)
    review_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=True)

    class Meta:
        model = Review
        fields = ['rating', 'review_text']
