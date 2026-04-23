from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Task, Category

inputStyle = 'w-full px-4 py-3 rounded-xl border border-border bg-surface text-text placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-primary transition'
inputStyle2 = 'w-full px-4 py-3 rounded-xl border border-border bg-surface text-text focus:outline-none focus:ring-2 focus:ring-primary transition'
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status', 'category', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': inputStyle,
                'placeholder': _('Título da tarefa...')
            }),
            'description': forms.Textarea(attrs={
                'class': inputStyle,
                'rows': 3,
                'placeholder': _('Descrição (opcional)...')
            }),
            'priority': forms.Select(attrs={
                'class': inputStyle2,
            }),
            'status': forms.Select(attrs={
                'class': inputStyle2,
            }),
            'category': forms.Select(attrs={
                'class': inputStyle2,
            }),
            'due_date': forms.DateInput(attrs={
                'class': inputStyle2,
                'type': 'date'
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
        self.fields['category'].required = False

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'color']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': inputStyle,
                'placeholder': _('Nome da categoria...')
            }),
            'color': forms.TextInput(attrs={
                'class': 'w-16 h-10 rounded-lg border border-border cursor-pointer',
                'type': 'color'
            }),
        }
