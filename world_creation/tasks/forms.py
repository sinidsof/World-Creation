from django import forms
from world_creation.accounts.models import CustomUser
from world_creation.tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'task_type', 'estimated_time', 'assigned_to']

    def __init__(self, *args, **kwargs):
        # Извличаме текущия потребител
        user = kwargs.pop('user', None)
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
        self.fields['assigned_to'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Изберете потребител за назначаване'
        })

        # Ограничаваме избора за 'assigned_to' в зависимост от ролята на потребителя
        if user and 'assigned_to' in self.fields:
            if user.role == 'super_creator':
                # Супер създателите могат да виждат всички потребители
                self.fields['assigned_to'].queryset = CustomUser.objects.exclude(id=user.id)
            else:
                # Останалите потребители нямат достъп до това поле
                self.fields['assigned_to'].queryset = CustomUser.objects.none()


