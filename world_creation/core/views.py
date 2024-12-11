from django.shortcuts import render

from world_creation.tasks.models import Task


# Create your views here.
def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')
def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')


def gallery(request):
    # Вземи всички задачи, които имат изображения и са споделени
    tasks_with_images = Task.objects.filter(shared=True).exclude(image__isnull=True)

    context = {
        'tasks_with_images': tasks_with_images,
    }
    return render(request, 'core/gallery.html', context)


def feedback(request):
    return render(request, 'core/feedback.html')


