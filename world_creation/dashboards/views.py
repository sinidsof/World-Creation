from urllib.parse import urlencode
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Task, Feedback
from ..tasks.models import SelfAssessment


# Логика за споделяне на постижения
def handle_share_achievement(request):
    task_id = request.POST.get('task_id')
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)

    if not task.shared:
        task.shared = True
        task.save()

        # Добавяне на next параметър към URL
    next_url = reverse('creator_dashboard')
    gallery_url = reverse('gallery')
    redirect_url = f"{gallery_url}?{urlencode({'next': next_url})}"
    return redirect(redirect_url)

# Логика за качване на изображение
def handle_image_upload(request):
    task_id = request.POST.get('task_id')
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)

    if 'image' in request.FILES:
        task.image = request.FILES['image']
        task.save()

    return redirect('creator_dashboard')

@login_required
def creator_dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    feedbacks = Feedback.objects.filter(task__in=tasks)
    self_assessments = SelfAssessment.objects.filter(user=request.user)

    if request.method == 'POST':
        # Определяне на действие според POST заявката
        if 'share_achievement' in request.POST:
            return handle_share_achievement(request)
        if 'image' in request.FILES:
            return handle_image_upload(request)

    context = {
        'tasks': tasks,
        'feedbacks': feedbacks,
        'self_assessments': self_assessments,
    }

    return render(request, 'dashboards/creator_dashboard.html', context)




# Функция за обработка на фийдбек от супер криейтор
def create_super_creator_feedback(task, super_creator, message):
    try:
        Feedback.objects.create(
            task=task,
            creator=task.assigned_to,  # Криейторът, на когото е възложена задачата
            super_creator=super_creator,  # Супер криейторът, който добавя фийдбек
            message=message
        )
        return True
    except Exception as e:
        return False


# Функция за обработка на фийдбек от супер криейтор
@login_required
def super_creator_dashboard(request):
    tasks = Task.objects.all()

    if request.method == 'POST' and 'super_creator_feedback' in request.POST:
        task_id = request.POST.get('task_id')
        feedback_message = request.POST.get('super_creator_feedback')

        if task_id and feedback_message:
            task = get_object_or_404(Task, id=task_id)
            create_super_creator_feedback(task, request.user, feedback_message)

        return redirect('super_creator_dashboard')  # Презареждане след изпращане

    context = {
        'tasks': tasks,
    }

    return render(request, 'dashboards/super_creator_dashboard.html', context)



