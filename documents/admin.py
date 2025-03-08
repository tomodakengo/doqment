from django.contrib import admin
from .models import Project, SectionTemplate, Document, DocumentSection


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'owner__username')
    list_filter = ('created_at',)


@admin.register(SectionTemplate)
class SectionTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'form_type', 'order', 'created_at')
    search_fields = ('title', 'description', 'project__name')
    list_filter = ('form_type', 'created_at')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'created_by', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'project__name', 'created_by__username')
    list_filter = ('created_at',)


@admin.register(DocumentSection)
class DocumentSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'document', 'order', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'document__title')
    list_filter = ('created_at',)
