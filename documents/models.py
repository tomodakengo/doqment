from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    TEMPLATE_CHOICES = [
        ('test_plan', 'テスト計画書'),
        ('test_specification', 'テスト仕様書'),
        ('test_report', 'テスト結果報告書'),
        ('custom', 'カスタム'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    template_type = models.CharField(max_length=50, choices=TEMPLATE_CHOICES, default='test_specification')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SectionTemplate(models.Model):
    FORM_TYPE_CHOICES = [
        ('text', 'テキスト'),
        ('textarea', 'テキストエリア'),
        ('markdown', 'マークダウン'),
        ('table', 'テーブル'),
        ('list', 'リスト'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='section_templates')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    form_type = models.CharField(max_length=20, choices=FORM_TYPE_CHOICES, default='textarea')
    content_guidelines = models.TextField(blank=True)
    ai_prompt = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.project.name} - {self.title}"


class Document(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    product_description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class DocumentSection(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='sections')
    template = models.ForeignKey(SectionTemplate, on_delete=models.SET_NULL, null=True, related_name='document_sections')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.document.title} - {self.title}"


class GenerationTask(models.Model):
    STATUS_CHOICES = [
        ('pending', '待機中'),
        ('processing', '処理中'),
        ('completed', '完了'),
        ('failed', '失敗'),
    ]
    
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='generation_tasks')
    task_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    progress = models.IntegerField(default=0)  # 0-100の進捗率
    total_sections = models.IntegerField(default=0)
    completed_sections = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Generation Task for {self.document.title} ({self.status})"
