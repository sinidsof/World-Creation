from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .forms import TaskForm, SelfAssessmentForm, EditForm
from .models import Task, SelfAssessment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView



class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.get_queryset().exists():
            messages.info(self.request, 'Нямате задачи в момента.')
        return context


@login_required
def create_task(request):
    # Ако потребителят не е супер създател или криейтор, го пренасочваме
    if request.user.role not in ['super_creator', 'co_creator']:
        return redirect('home')  # Ако не е супер създател или криейтор, го пренасочваме

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)

            # Ако е супер създател, задаваме задачата да е възложена на криейтор
            if request.user.role == 'super_creator':
                task.created_by = request.user  # Задаваме създателя на задачата
                task.save()
                messages.success(request, "Задачата беше успешно създадена!")
                return redirect('super_creator_dashboard')  # Пренасочване към дашборда на супер създателя

            # Ако е криейтор, задаваме създателя на задачата и го запазваме
            elif request.user.role == 'co_creator':
                task.created_by = request.user  # Задаваме създателя на задачата
                task.assigned_to = request.user  # Криейторът може да се назначи на собствена задача
                task.save()
                messages.success(request, "Задачата беше успешно създадена!")
                return redirect('creator_dashboard')  # Пренасочване към дашборда на криейтора

    else:
        form = TaskForm(user=request.user)

    return render(request, 'tasks/create_task.html', {'form': form})


class EditTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = EditForm
    template_name = 'tasks/edit_task.html'

    def get_object(self, queryset=None):
        task_id = self.kwargs.get('task_id')
        return Task.objects.get(id=task_id)


    def get_success_url(self):
        return reverse_lazy('task_list')



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




class SelfAssessmentView(LoginRequiredMixin, FormView):
    model = SelfAssessment
    form_class = SelfAssessmentForm
    template_name = 'tasks/self_assessment.html'

    def get_initial(self):
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        self_assessment = SelfAssessment.objects.filter(task=task, user=self.request.user).first()
        return {'task': task, 'form': SelfAssessmentForm(instance=self_assessment)}

    def form_valid(self, form):
        self_assessment = form.save(commit=False)
        self_assessment.task = self.get_initial()['task']
        self_assessment.user = self.request.user
        self_assessment.save()
        return redirect('creator_dashboard')

