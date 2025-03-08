from django.urls import path
from .views import (
    ProjectListView, ProjectDetailView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView,
    SectionTemplateCreateView, SectionTemplateUpdateView, SectionTemplateDeleteView,
    DocumentCreateView, DocumentDetailView, DocumentUpdateView, DocumentDeleteView,
    DocumentSectionUpdateView, generate_document_sections
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
    
    # ドキュメント関連のURL
    path('projects/<int:project_pk>/documents/create/', DocumentCreateView.as_view(), name='document_create'),
    path('documents/<int:pk>/', DocumentDetailView.as_view(), name='document_detail'),
    path('documents/<int:pk>/update/', DocumentUpdateView.as_view(), name='document_update'),
    path('documents/<int:pk>/delete/', DocumentDeleteView.as_view(), name='document_delete'),
    path('documents/<int:pk>/generate/', generate_document_sections, name='generate_document_sections'),
    
    # ドキュメントセクション関連のURL
    path('sections/<int:pk>/update/', DocumentSectionUpdateView.as_view(), name='document_section_update'),
] 