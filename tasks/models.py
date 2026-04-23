from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(_('nome'), max_length=100)
    color = models.CharField(_('cor'), max_length=7, default='#6366f1')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        verbose_name = _('Categoria')
        verbose_name_plural = _('Categorias')
        ordering = ['name']

    def __str__(self):
        return self.name

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', _('Baixa')),
        ('medium', _('Média')),
        ('high', _('Alta')),
    ]
    STATUS_CHOICES = [
        ('pending', _('Pendente')),
        ('in_progress', _('Em andamento')),
        ('done', _('Concluída')),
    ]

    title = models.CharField(_('título'), max_length=200)
    description = models.TextField(_('descrição'), blank=True)
    priority = models.CharField(_('prioridade'), max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('categoria'))
    due_date = models.DateField(_('data de vencimento'), null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('atualizado em'), auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    class Meta:
        verbose_name = _('Tarefa')
        verbose_name_plural = _('Tarefas')
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    @property
    def is_done(self):
        return self.status == 'done'

    @property
    def is_overdue(self):
        from django.utils import timezone
        if self.due_date and self.status != 'done':
            return self.due_date < timezone.now().date()
        return False

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar_color = models.CharField(max_length=7, default='#7c3aed')
    bio = models.TextField(blank=True, max_length=200)
    notify_overdue = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} profile'
