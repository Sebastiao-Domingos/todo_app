from django.contrib import admin
from django.utils.html import format_html
from .models import Task, Category, UserProfile
from django.utils.translation import gettext_lazy as _

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['colored_name', 'user', 'task_count']
    list_filter = ['user']
    search_fields = ['name']

    def colored_name(self, obj):
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;border-radius:6px;font-weight:600">{}</span>',
            obj.color, obj.name
        )
    colored_name.short_description = _('Categoria')

    def task_count(self, obj):
        return obj.task_set.count()
    task_count.short_description = _('Tarefas')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'priority_badge', 'status_badge', 'due_date', 'is_overdue_display', 'created_at']
    list_filter = ['status', 'priority', 'user', 'category']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
    list_editable = []
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    fieldsets = (
        (_('Informações Básicas'), {'fields': ('title', 'description', 'user')}),
        (_('Detalhes'), {'fields': ('priority', 'status', 'category', 'due_date', 'order')}),
        (_('Datas'), {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def priority_badge(self, obj):
        colors = {'high': '#ef4444', 'medium': '#f59e0b', 'low': '#10b981'}
        labels = {'high': '▲ Alta', 'medium': '● Média', 'low': '▼ Baixa'}
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600">{}</span>',
            colors.get(obj.priority, '#ccc'), labels.get(obj.priority, obj.priority)
        )
    priority_badge.short_description = _('Prioridade')

    def status_badge(self, obj):
        colors = {'done': '#10b981', 'in_progress': '#3b82f6', 'pending': '#6b7280'}
        labels = {'done': '✓ Concluída', 'in_progress': '⚡ Em andamento', 'pending': '○ Pendente'}
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600">{}</span>',
            colors.get(obj.status, '#ccc'), labels.get(obj.status, obj.status)
        )
    status_badge.short_description = _('Status')

    def is_overdue_display(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color:#ef4444;font-weight:bold">⚠ Atrasada</span>')
        return '—'
    is_overdue_display.short_description = _('Atraso')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'colored_avatar', 'notify_overdue']
    list_filter = ['notify_overdue']

    def colored_avatar(self, obj):
        return format_html(
            '<div style="width:28px;height:28px;border-radius:8px;background:{};display:inline-flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:13px">{}</div>',
            obj.avatar_color, obj.user.username[0].upper()
        )
    colored_avatar.short_description = _('Avatar')

# Customize admin site
admin.site.site_header = 'TaskFlow Admin'
admin.site.site_title = 'TaskFlow'
admin.site.index_title = 'Painel de Administração'
