from django.core.exceptions import ValidationError
from django.db import models
from world_creation import settings


# Create your models here.

class Task(models.Model):
    TASK_TYPES = (
        ('creativity', 'Креативност'),
        ('relaxation', 'Отдих'),
        ('physical', 'Физическа активност'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    task_type = models.CharField(max_length=20, choices=TASK_TYPES)
    estimated_time = models.PositiveIntegerField(help_text="Време за изпълнение в минути")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks_created'  # Потребителят, който създава задачата
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_tasks",
        null=True, blank=True  # Може да е празно
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.estimated_time <= 0:
            raise ValidationError('Времето за изпълнение на задачата трябва да бъде положително число.')

    def __str__(self):
        return f"{self.title} ({self.get_task_type_display()})"


