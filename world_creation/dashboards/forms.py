from django import forms
from .models import Feedback, SelfAssessment


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Напишете вашето мнение за задачата...'
            }),
        }

class SelfAssessmentForm(forms.ModelForm):
    class Meta:
        model = SelfAssessment
        fields = ['rating', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Напишете вашето мнение за задачата...'
            }),
        }