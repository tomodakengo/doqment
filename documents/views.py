from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.contrib import messages
from .models import Project, SectionTemplate, Document, DocumentSection, GenerationTask
from .forms import ProjectForm, SectionTemplateForm, DocumentForm, DocumentSectionForm
from .default_templates import DEFAULT_TEMPLATES
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
        response = super().form_valid(form)
        
        # デフォルトのセクションテンプレートを追加
        template_type = form.instance.template_type
        if template_type != 'custom' and template_type in DEFAULT_TEMPLATES:
            template_data = DEFAULT_TEMPLATES[template_type]
            for section_data in template_data['sections']:
                SectionTemplate.objects.create(
                    project=self.object,
                    title=section_data['title'],
                    description=section_data['description'],
                    form_type=section_data['form_type'],
                    content_guidelines=section_data['content_guidelines'],
                    ai_prompt=section_data['ai_prompt'],
                    order=section_data['order']
                )
            messages.success(self.request, f"{template_data['name']}のデフォルトセクションを追加しました。")
        
        return response


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


@login_required
def add_section_template(request, project_pk):
    """
    セクションテンプレートを動的に追加するAJAXビュー
    """
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        project = get_object_or_404(Project, pk=project_pk, owner=request.user)
        
        # 最大の順序を取得
        max_order = project.section_templates.aggregate(models.Max('order'))['order__max'] or 0
        
        # 新しいセクションテンプレートを作成
        template = SectionTemplate.objects.create(
            project=project,
            title=request.POST.get('title', '新しいセクション'),
            description=request.POST.get('description', ''),
            form_type=request.POST.get('form_type', 'textarea'),
            content_guidelines=request.POST.get('content_guidelines', ''),
            ai_prompt=request.POST.get('ai_prompt', ''),
            order=max_order + 1
        )
        
        return JsonResponse({
            'success': True,
            'template_id': template.id,
            'template_title': template.title,
            'template_order': template.order
        })
    
    return JsonResponse({'success': False, 'error': '不正なリクエストです。'})


@login_required
def update_section_template_order(request):
    """
    セクションテンプレートの順序を更新するAJAXビュー
    """
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        template_ids = request.POST.getlist('template_ids[]')
        
        for i, template_id in enumerate(template_ids):
            template = get_object_or_404(SectionTemplate, pk=template_id, project__owner=request.user)
            template.order = i + 1
            template.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': '不正なリクエストです。'})


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
        # 新しい生成タスクを作成
        task = GenerationTask.objects.create(
            document=document,
            status='pending',
            progress=0
        )
        
        # Celeryタスクを開始
        from .tasks import generate_document_sections_task
        celery_task = generate_document_sections_task.delay(document.id, task.id)
        
        # タスクIDを保存
        task.task_id = celery_task.id
        task.save()
        
        # 進捗状況ページにリダイレクト
        return redirect('document_generation_status', pk=document.pk, task_id=task.id)
    
    return render(request, 'documents/generate_confirm.html', {'document': document})


@login_required
def document_generation_status(request, pk, task_id):
    """
    ドキュメント生成の進捗状況を表示するビュー
    """
    document = get_object_or_404(Document, pk=pk, project__owner=request.user)
    task = get_object_or_404(GenerationTask, id=task_id, document=document)
    
    return render(request, 'documents/generation_status.html', {
        'document': document,
        'task': task
    })


@login_required
def get_generation_status(request, task_id):
    """
    生成タスクの進捗状況を取得するAPIビュー
    """
    task = get_object_or_404(GenerationTask, id=task_id, document__project__owner=request.user)
    
    data = {
        'status': task.status,
        'progress': task.progress,
        'total_sections': task.total_sections,
        'completed_sections': task.completed_sections,
        'error_message': task.error_message
    }
    
    # タスクが完了している場合はドキュメント詳細ページのURLを含める
    if task.status == 'completed':
        data['redirect_url'] = reverse('document_detail', kwargs={'pk': task.document.id})
    
    return JsonResponse(data)


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
