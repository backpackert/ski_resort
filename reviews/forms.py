from .models import Review
from django.forms import ModelForm, TextInput, DateInput, Textarea


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['brief', 'full_text', 'date', 'user']

        widgets = {
            'brief': TextInput(attrs={
                'class': "form control",
                'placeholder': 'Brief review'
            }),
            'full_text': Textarea(attrs={
                'class': "form control",
                'placeholder': 'Write your review'
            }),
            'date': DateInput(format='%d/%m/%Y'),
            'user': TextInput(attrs={
                'class': "form control",
                'placeholder': 'Your name/nick'
            })

        }
