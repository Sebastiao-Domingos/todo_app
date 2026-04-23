from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tasks/', views.task_list, name='list'),
    path('tasks/create/', views.task_create, name='create'),
    path('tasks/<int:pk>/edit/', views.task_edit, name='edit'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='delete'),
    path('tasks/<int:pk>/toggle/', views.task_toggle, name='toggle'),
    path('tasks/<int:pk>/status/', views.task_update_status, name='update_status'),
    path('tasks/reorder/', views.task_reorder, name='reorder'),
    path('kanban/', views.kanban, name='kanban'),
    path('categories/', views.category_list, name='categories'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('profile/', views.profile, name='profile'),
]
