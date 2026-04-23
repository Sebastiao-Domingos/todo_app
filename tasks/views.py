from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import json
from .models import Task, Category, UserProfile
from .forms import TaskForm, CategoryForm

def get_or_create_profile(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile

def home(request):
    if request.user.is_authenticated:
        return redirect('tasks:dashboard')
    return redirect('accounts:login')

@login_required
def dashboard(request):
    user = request.user
    today = timezone.now().date()
    tasks = Task.objects.filter(user=user)

    # Stats
    total = tasks.count()
    done = tasks.filter(status='done').count()
    pending = tasks.filter(status='pending').count()
    in_progress = tasks.filter(status='in_progress').count()
    overdue = tasks.filter(status__in=['pending','in_progress'], due_date__lt=today).count()
    completion_rate = round(((done / total )* 100) if total > 0 else 0)

    # Due today / this week
    due_today = tasks.filter(due_date=today, status__in=['pending','in_progress'])
    due_this_week = tasks.filter(due_date__range=[today, today + timedelta(days=7)], status__in=['pending','in_progress'])

    # Recent activity (last 5 updated)
    recent = tasks.order_by('-updated_at')[:5]

    # Tasks by priority
    high_count = tasks.filter(priority='high', status__in=['pending','in_progress']).count()
    medium_count = tasks.filter(priority='medium', status__in=['pending','in_progress']).count()
    low_count = tasks.filter(priority='low', status__in=['pending','in_progress']).count()

    # Tasks per category
    categories_data = Category.objects.filter(user=user).annotate(
        total=Count('task'),
        done_count=Count('task', filter=Q(task__status='done'))
    )

    # Weekly completion chart data (last 7 days)
    weekly_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        count = tasks.filter(status='done', updated_at__date=day).count()
        weekly_data.append({'day': day.strftime('%d/%m'), 'count': count})

    profile = get_or_create_profile(user)

    context = {
        'stats': {
            'total': total, 'done': done, 'pending': pending,
            'in_progress': in_progress, 'overdue': overdue,
            'completion_rate': completion_rate,
        },
        'due_today': due_today,
        'due_this_week': due_this_week,
        'recent': recent,
        'priority_data': {'high': high_count, 'medium': medium_count, 'low': low_count},
        'categories_data': categories_data,
        'weekly_data': json.dumps(weekly_data),
        'profile': profile,
    }
    return render(request, 'tasks/dashboard.html', context)

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    category_filter = request.GET.get('category', '')
    search_query = request.GET.get('q', '')

    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    if category_filter:
        tasks = tasks.filter(category_id=category_filter)
    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    total = Task.objects.filter(user=request.user).count()
    done = Task.objects.filter(user=request.user, status='done').count()
    pending = Task.objects.filter(user=request.user, status='pending').count()
    in_progress = Task.objects.filter(user=request.user, status='in_progress').count()

    categories = Category.objects.filter(user=request.user)
    form = TaskForm(user=request.user)

    context = {
        'tasks': tasks,
        'form': form,
        'categories': categories,
        'stats': {'total': total, 'done': done, 'pending': pending, 'in_progress': in_progress},
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'category_filter': category_filter,
        'search_query': search_query,
        'overdue_count': Task.objects.filter(
            user=request.user, status__in=['pending','in_progress'],
            due_date__lt=timezone.now().date()
        ).count(),
    }
    return render(request, 'tasks/list.html', context)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'id': task.pk, 'title': task.title})
            messages.success(request, _('Tarefa criada com sucesso!'))
        else:
            messages.error(request, _('Erro ao criar tarefa.'))
    return redirect('tasks:list')

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Tarefa atualizada!'))
            return redirect('tasks:list')
    else:
        form = TaskForm(instance=task, user=request.user)
    categories = Category.objects.filter(user=request.user)
    return render(request, 'tasks/edit.html', {'form': form, 'task': task, 'categories': categories})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        messages.success(request, _('Tarefa excluída!'))
    return redirect('tasks:list')

@login_required
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.status = 'pending' if task.status == 'done' else 'done'
        task.save()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': task.status, 'is_done': task.is_done})
    return redirect('tasks:list')

@login_required
def task_reorder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for item in data.get('order', []):
                Task.objects.filter(pk=item['id'], user=request.user).update(order=item['order'])
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})

@login_required
def kanban(request):
    pending = Task.objects.filter(user=request.user, status='pending').order_by('order', '-created_at')
    in_progress = Task.objects.filter(user=request.user, status='in_progress').order_by('order', '-created_at')
    done = Task.objects.filter(user=request.user, status='done').order_by('order', '-created_at')
    form = TaskForm(user=request.user)
    categories = Category.objects.filter(user=request.user)
    return render(request, 'tasks/kanban.html', {
        'pending': pending,
        'in_progress': in_progress,
        'done': done,
        'form': form,
        'categories': categories,
    })

@login_required
def task_update_status(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk, user=request.user)
        data = json.loads(request.body)
        new_status = data.get('status')
        if new_status in ['pending', 'in_progress', 'done']:
            task.status = new_status
            task.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user).annotate(task_count=Count('task'))
    form = CategoryForm()
    return render(request, 'tasks/categories.html', {'categories': categories, 'form': form})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.user = request.user
            cat.save()
            messages.success(request, _('Categoria criada!'))
    return redirect('tasks:categories')

@login_required
def category_delete(request, pk):
    cat = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        cat.delete()
        messages.success(request, _('Categoria excluída!'))
    return redirect('tasks:categories')

@login_required
def profile(request):
    prof = get_or_create_profile(request.user)
    if request.method == 'POST':
        bio = request.POST.get('bio', '')
        color = request.POST.get('avatar_color', '#7c3aed')
        notify = request.POST.get('notify_overdue') == 'on'
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        prof.bio = bio[:200]
        prof.avatar_color = color
        prof.notify_overdue = notify
        prof.save()
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save()
        messages.success(request, _('Perfil atualizado!'))
        return redirect('tasks:profile')
    return render(request, 'tasks/profile.html', {'prof': prof, 'color_list': ['#7c3aed','#6366f1','#0ea5e9','#10b981','#f59e0b','#ef4444','#ec4899','#8b5cf6']})
