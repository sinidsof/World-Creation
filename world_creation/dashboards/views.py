from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task, Feedback

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

# Функция за обработка на обратна връзка от криейтора
@login_required
def creator_dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    feedbacks = Feedback.objects.filter(super_creator=request.user)

    context = {
        'tasks': tasks,
        'feedbacks': feedbacks,
    }

    return render(request, 'dashboards/creator_dashboard.html', context)

# Функция за обработка на фийдбек от супер криейтор
@login_required
def super_creator_dashboard(request):
    if request.user.role != 'super_creator':
        return redirect('home')  # Пренасочване, ако не е супер криейтор

    if request.method == 'POST' and 'super_creator_feedback' in request.POST:
        task_id = request.POST.get('task_id')
        feedback_message = request.POST.get('super_creator_feedback')

        if task_id and feedback_message:
            task = get_object_or_404(Task, id=task_id)

            # Създаване на фийдбек от супер криейтор
            if create_super_creator_feedback(task, request.user, feedback_message):
                messages.success(request, 'Обратната връзка беше успешно изпратена!')
            else:
                messages.error(request, 'Възникна грешка при изпращането на обратната връзка.')

        else:
            messages.error(request, 'Моля попълнете всички полета за обратната връзка.')

        return redirect('super_creator_dashboard')

    # Всички задачи за супер криейтора
    tasks = Task.objects.all()
    context = {
        'tasks': tasks,
    }

    return render(request, 'dashboards/super_creator_dashboard.html', context)
