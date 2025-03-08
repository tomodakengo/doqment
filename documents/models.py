from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
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
