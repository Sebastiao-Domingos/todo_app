from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

INPUT_CLASS = 'w-full px-4 py-3 rounded-xl border border-border bg-surface text-text placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-primary transition'

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': _('Utilizador')}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': INPUT_CLASS, 'placeholder': _('Senha')}))

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Email'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': INPUT_CLASS, 'placeholder': _('Nome de utilizador')})
        self.fields['password1'].widget.attrs.update({'class': INPUT_CLASS, 'placeholder': _('Senha')})
        self.fields['password2'].widget.attrs.update({'class': INPUT_CLASS, 'placeholder': _('Confirmar senha')})
