from django import forms


from .models import Task, SelfAssessment
from ..accounts.models import CustomUser


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'task_type', 'estimated_time', 'assigned_to', 'image']

    def __init__(self, *args, **kwargs):
        # Извличаме текущия потребител и action параметъра
        user = kwargs.pop('user', None)
        action = kwargs.pop('action', None)  # Ново: екстракция на действие от kwargs
        super().__init__(*args, **kwargs)

        # Задаваме CSS класове и placeholder-и за полетата
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Въведете заглавие на задачата'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Опишете задачата',
            'rows': 3
        })
        self.fields['task_type'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Изберете тип задача'
        })
        self.fields['estimated_time'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пример: 30'
        })
        self.fields['image'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Изберете изображение'
        })

        # Ограничаваме избора за 'assigned_to' в зависимост от ролята на потребителя
        if user and 'assigned_to' in self.fields:
            if user.role == 'super_creator':
                # Супер създателят може да възлага задачи на други потребители (освен себе си)
                self.fields['assigned_to'].queryset = CustomUser.objects.exclude(id=user.id)
            elif user.role == 'creator':
                # Криейторът не може да възлага задачи и полето е скрито
                self.fields['assigned_to'].widget = forms.HiddenInput()
                self.fields['assigned_to'].queryset = CustomUser.objects.none()  # Няма опция за избор



class EditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'task_type', 'estimated_time']

    def __init__(self, *args, **kwargs):
        # Извличаме текущия потребител и action параметъра
        user = kwargs.pop('user', None)
        action = kwargs.pop('action', None)  # Ново: екстракция на действие от kwargs
        super().__init__(*args, **kwargs)

        # Задаваме CSS класове и placeholder-и за полетата
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Въведете заглавие на задачата'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Опишете задачата',
            'rows': 3
        })
        self.fields['task_type'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Изберете тип задача'
        })
        self.fields['estimated_time'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пример: 30'
        })



class SelfAssessmentForm(forms.ModelForm):
    class Meta:
        model = SelfAssessment
        fields = ['rating', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Напишете вашето мнение за задачата...',
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Задаваме CSS класове и placeholder-и за полето 'rating'
        self.fields['rating'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Изберете оценка (1-5)'
        })