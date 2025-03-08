from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from documents.models import Project


class HomeView(TemplateView):
    """
    ホームページビュー
    """
    template_name = 'core/home.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    ダッシュボードビュー
    """
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(owner=self.request.user)
        return context
