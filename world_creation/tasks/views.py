from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required

from ..dashboards.forms import SelfAssessmentForm


@login_required  # Това ще принуди потребителя да бъде влязъл, за да зареди задачите
def task_list(request):
    # Проверка дали потребителят е влязъл в системата
    if request.user.is_authenticated:
        tasks = Task.objects.filter(created_by=request.user)

        # Проверка дали има задачи
        if tasks.exists():
            return render(request, 'tasks/task_list.html', {'tasks': tasks})
        else:
            messages.info(request, 'Нямате задачи в момента.')
            return render(request, 'tasks/task_list.html', {'tasks': []})  # Показваме празен списък с задачи
    else:
        # Ако потребителят е анонимен, пренасочваме го към страницата за логин
        messages.error(request, 'Моля, влезте в системата, за да видите задачите си.')
        return redirect('login')  # Заменете 'login' с името на URL-то за логин




@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)  # Подаваме текущия потребител към формата
        if form.is_valid():
            task = form.save(commit=False)  # Не записваме веднага, за да можем да добавим допълнителни стойности

            # Задаваме текущия потребител като създател
            task.created_by = request.user

            # Проверка дали има избран потребител за възлагане, ако няма, възлагаме на създателя
            if not task.assigned_to:
                task.assigned_to = request.user

            # Ако текущият потребител е супер криейтор, той може да възлага задачи на други потребители
            if request.user.role == 'super_creator':
                # Ако супер криейторът не задава себе си за изпълнител, проверяваме дали има право да възлага
                if task.assigned_to and task.assigned_to != request.user:
                    # Проверяваме дали потребителят за възлагане има роля 'creator'
                    if task.assigned_to.role != 'creator':
                        messages.error(request, "Можете да възлагате задачи само на създатели.")
                        return redirect('create_task')

            task.save()  # Записваме задачата в базата данни

            # Съобщение за успешното създаване на задачата
            messages.success(request, 'Задачата беше успешно създадена!')
            return redirect('task_list')  # Пренасочваме към списъка с задачи
        else:
            # Ако формата е невалидна, показваме съобщение за грешка
            messages.error(request, 'Попълнете правилно всички полета на задачата.')
            # Показваме всички грешки за всяко поле
            for field in form.errors:
                messages.error(request, f"Полето {field} има следните грешки: {form.errors[field]}")
    else:
        # Ако заявката е GET, създаваме нова форма, като подаваме текущия потребител
        form = TaskForm(user=request.user)

    return render(request, 'tasks/create_task.html', {'form': form})



def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)  # Вземаме задачата по нейния ID (pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()  # Записваме редактираната задача
            return redirect('task_list')  # Пренасочваме към списъка с задачи или друго място
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})

def delete_task(request, task_id):
    # Изтегляне на задачата по ID
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        # Изтриване на задачата при POST заявка
        task.delete()
        messages.success(request, "Задачата беше успешно изтрита!")
        return redirect('task_list')  # Пренасочване към списъка със задачи

    # Ако е GET заявка, показваме потвърдителен екран
    return render(request, 'tasks/confirm_delete.html', {'task': task})

def self_assessment(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = SelfAssessmentForm(request.POST)
        if form.is_valid():
            # Създаване на нов обект SelfAssessment
            self_assessment = form.save(commit=False)
            self_assessment.task = task
            self_assessment.user = request.user  # Свързване с текущия потребител
            self_assessment.save()

            return redirect('assessment_feedback', task_id=task.id, self_assessment_id=self_assessment.id)  # Пренасочване към страницата за обратна връзка
    else:
        form = SelfAssessmentForm()

    return render(request, 'self_assessment.html', {'form': form, 'task': task})