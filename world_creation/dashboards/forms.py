from django import forms
from .models import Feedback
from .models import Task


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


class TaskImageUploadForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ShareAchievementForm(forms.Form):
    task_id = forms.IntegerField(widget=forms.HiddenInput())

class TaskImageUploadForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['image']  # Само изображението

