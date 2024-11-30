from django.db import models

from world_creation import settings
from world_creation.tasks.models import Task


# Create your models here.
class Feedback(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="feedbacks")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='creator_feedback', on_delete=models.CASCADE
    )
    super_creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='super_creator_feedback', on_delete=models.CASCADE
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)  # Поле за индикация дали е прегледано

    def __str__(self):
        return f"Feedback for {self.task.title} by {self.creator.username}"


class SelfAssessment(models.Model):
    task = models.ForeignKey(Task, related_name="self_assessments", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comments = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Self-assessment for {self.task.title} by {self.user.username}"