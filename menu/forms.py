from django import forms
from .models import Testimonial

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'designation', 'image', 'review_text', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'আপনার নাম'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'আপনার পেশা (উদা: ছাত্র/চাকরিজীবী)'}),
            'review_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'আপনার অভিজ্ঞতা লিখুন...'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }