from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    """
    ユーザー登録フォーム
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-zinc-300 rounded-md focus:outline-none focus:ring-2 focus:ring-zinc-700'}),
        label='ユーザー名'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border border-zinc-300 rounded-md focus:outline-none focus:ring-2 focus:ring-zinc-700'}),
        label='パスワード'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border border-zinc-300 rounded-md focus:outline-none focus:ring-2 focus:ring-zinc-700'}),
        label='パスワード（確認）'
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    """
    ログインフォーム
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-zinc-300 rounded-md focus:outline-none focus:ring-2 focus:ring-zinc-700'}),
        label='ユーザー名'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border border-zinc-300 rounded-md focus:outline-none focus:ring-2 focus:ring-zinc-700'}),
        label='パスワード'
    ) 