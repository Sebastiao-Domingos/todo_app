from .models import Task
from django.utils import timezone

def overdue_count(request):
    if request.user.is_authenticated:
        count = Task.objects.filter(
            user=request.user,
            status__in=['pending', 'in_progress'],
            due_date__lt=timezone.now().date()
        ).count()
        return {'overdue_count': count}
    return {'overdue_count': 0}
