from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import UserProfile


class SignUpView(CreateView):
    """
    ユーザー登録ビュー
    """
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # ユーザープロファイルを作成
        UserProfile.objects.create(user=self.object)
        return response


class CustomLoginView(LoginView):
    """
    ログインビュー
    """
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    """
    ログアウトビュー
    """
    next_page = reverse_lazy('home')
