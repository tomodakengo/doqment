from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from .models import Project, SectionTemplate, Document, DocumentSection
from .forms import ProjectForm, SectionTemplateForm, DocumentForm, DocumentSectionForm
from core.utils import generate_test_document


class ProjectListView(LoginRequiredMixin, ListView):
    """
    プロジェクト一覧ビュー
    """
    model = Project
    template_name = 'documents/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class ProjectDetailView(LoginRequiredMixin, DetailView):
    """
    プロジェクト詳細ビュー
    """
    model = Project
    template_name = 'documents/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_templates'] = self.object.section_templates.all()
        context['documents'] = self.object.documents.all()
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """
    プロジェクト作成ビュー
    """
    model = Project
    form_class = ProjectForm
    template_name = 'documents/project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """
    プロジェクト更新ビュー
    """
    model = Project
    form_class = ProjectForm
    template_name = 'documents/project_form.html'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """
    プロジェクト削除ビュー
    """
    model = Project
    template_name = 'documents/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class SectionTemplateCreateView(LoginRequiredMixin, CreateView):
    """
    セクションテンプレート作成ビュー
    """
    model = SectionTemplate
    form_class = SectionTemplateForm
    template_name = 'documents/section_template_form.html'

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'], owner=self.request.user)
        form.instance.project = project
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, pk=self.kwargs['project_pk'], owner=self.request.user)
        return context

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.kwargs['project_pk']})


class SectionTemplateUpdateView(LoginRequiredMixin, UpdateView):
    """
    セクションテンプレート更新ビュー
    """
    model = SectionTemplate
    form_class = SectionTemplateForm
    template_name = 'documents/section_template_form.html'

    def get_queryset(self):
        return SectionTemplate.objects.filter(project__owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.object.project
        return context

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.project.pk})


class SectionTemplateDeleteView(LoginRequiredMixin, DeleteView):
    """
    セクションテンプレート削除ビュー
    """
    model = SectionTemplate
    template_name = 'documents/section_template_confirm_delete.html'

    def get_queryset(self):
        return SectionTemplate.objects.filter(project__owner=self.request.user)

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.project.pk})


class DocumentCreateView(LoginRequiredMixin, CreateView):
    """
    ドキュメント作成ビュー
    """
    model = Document
    form_class = DocumentForm
    template_name = 'documents/document_form.html'

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'], owner=self.request.user)
        form.instance.project = project
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, pk=self.kwargs['project_pk'], owner=self.request.user)
        return context

    def get_success_url(self):
        return reverse('document_detail', kwargs={'pk': self.object.pk})


class DocumentDetailView(LoginRequiredMixin, DetailView):
    """
    ドキュメント詳細ビュー
    """
    model = Document
    template_name = 'documents/document_detail.html'
    context_object_name = 'document'

    def get_queryset(self):
        return Document.objects.filter(project__owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = self.object.sections.all()
        return context


class DocumentUpdateView(LoginRequiredMixin, UpdateView):
    """
    ドキュメント更新ビュー
    """
    model = Document
    form_class = DocumentForm
    template_name = 'documents/document_form.html'

    def get_queryset(self):
        return Document.objects.filter(project__owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.object.project
        return context

    def get_success_url(self):
        return reverse('document_detail', kwargs={'pk': self.object.pk})


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    """
    ドキュメント削除ビュー
    """
    model = Document
    template_name = 'documents/document_confirm_delete.html'

    def get_queryset(self):
        return Document.objects.filter(project__owner=self.request.user)

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.project.pk})


@login_required
def generate_document_sections(request, pk):
    """
    ドキュメントセクションを生成するビュー
    """
    document = get_object_or_404(Document, pk=pk, project__owner=request.user)
    
    if request.method == 'POST':
        # 既存のセクションを削除
        document.sections.all().delete()
        
        # プロジェクトのセクションテンプレートを取得
        section_templates = document.project.section_templates.all()
        
        # OpenAI APIを使用してセクションを生成
        sections_content = generate_test_document(document.product_description, section_templates)
        
        # 生成されたセクションを保存
        for template in section_templates:
            content = sections_content.get(template.id, '')
            DocumentSection.objects.create(
                document=document,
                template=template,
                title=template.title,
                content=content,
                order=template.order
            )
        
        return redirect('document_detail', pk=document.pk)
    
    return render(request, 'documents/generate_confirm.html', {'document': document})


class DocumentSectionUpdateView(LoginRequiredMixin, UpdateView):
    """
    ドキュメントセクション更新ビュー
    """
    model = DocumentSection
    form_class = DocumentSectionForm
    template_name = 'documents/document_section_form.html'

    def get_queryset(self):
        return DocumentSection.objects.filter(document__project__owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document'] = self.object.document
        return context

    def get_success_url(self):
        return reverse('document_detail', kwargs={'pk': self.object.document.pk})
