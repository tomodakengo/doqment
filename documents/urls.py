from django.urls import path
from .views import (
    ProjectListView, ProjectDetailView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView,
    SectionTemplateCreateView, SectionTemplateUpdateView, SectionTemplateDeleteView,
    DocumentCreateView, DocumentDetailView, DocumentUpdateView, DocumentDeleteView,
    DocumentSectionUpdateView, generate_document_sections, document_generation_status, get_generation_status,
    add_section_template, update_section_template_order
)

urlpatterns = [
    # プロジェクト関連のURL
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/create/', ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    
    # セクションテンプレート関連のURL
    path('projects/<int:project_pk>/templates/create/', SectionTemplateCreateView.as_view(), name='section_template_create'),
    path('templates/<int:pk>/update/', SectionTemplateUpdateView.as_view(), name='section_template_update'),
    path('templates/<int:pk>/delete/', SectionTemplateDeleteView.as_view(), name='section_template_delete'),
    path('projects/<int:project_pk>/templates/add/', add_section_template, name='add_section_template'),
    path('templates/update-order/', update_section_template_order, name='update_section_template_order'),
    
    # ドキュメント関連のURL
    path('projects/<int:project_pk>/documents/create/', DocumentCreateView.as_view(), name='document_create'),
    path('documents/<int:pk>/', DocumentDetailView.as_view(), name='document_detail'),
    path('documents/<int:pk>/update/', DocumentUpdateView.as_view(), name='document_update'),
    path('documents/<int:pk>/delete/', DocumentDeleteView.as_view(), name='document_delete'),
    path('documents/<int:pk>/generate/', generate_document_sections, name='generate_document_sections'),
    path('documents/<int:pk>/generation-status/<int:task_id>/', document_generation_status, name='document_generation_status'),
    path('api/generation-status/<int:task_id>/', get_generation_status, name='get_generation_status'),
    
    # ドキュメントセクション関連のURL
    path('sections/<int:pk>/update/', DocumentSectionUpdateView.as_view(), name='document_section_update'),
] 