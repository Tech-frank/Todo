from django.shortcuts import render
from django.http import JsonResponse
import json
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

@login_required
def index(request):
    filter_val = request.GET.get('filter', 'all')
    tasks = Task.objects.all().order_by('order')

    if filter_val == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_val == 'incomplete':
        tasks = tasks.filter(completed=False)

    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'todo/index.html', {
        'tasks': tasks,
        'form': form,
        'filter': filter_val,
    })

    
@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/edit.html', {'form': form, 'task': task})
@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('index')
@login_required
def update_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for i, task_id in enumerate(data.get('task_ids', [])):
            task = Task.objects.get(id=task_id)
            task.order = i
            task.save()
        return JsonResponse({'status': 'ok'})
    
    from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'todo/register.html', {'form': form})
@login_required
def toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect('index')