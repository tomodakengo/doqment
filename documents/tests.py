from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from documents.models import Project, SectionTemplate, Document, DocumentSection, GenerationTask
from documents.forms import ProjectForm, SectionTemplateForm, DocumentForm, DocumentSectionForm

# Model Tests
class ProjectModelTest(TestCase):
    """Projectモデルのテスト"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test project description',
            owner=self.user
        )

    def test_project_creation(self):
        self.assertEqual(self.project.name, 'Test Project')
        self.assertEqual(self.project.description, 'Test project description')
        self.assertEqual(self.project.owner, self.user)

    def test_project_str(self):
        self.assertEqual(str(self.project), 'Test Project')

class DocumentModelTest(TestCase):
    """Documentモデルのテスト"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test project description',
            owner=self.user
        )
        self.document = Document.objects.create(
            title='Test Document',
            project=self.project,
            created_by=self.user
        )

    def test_document_creation(self):
        self.assertEqual(self.document.title, 'Test Document')
        self.assertEqual(self.document.project, self.project)
        self.assertEqual(self.document.created_by, self.user)

    def test_document_str(self):
        self.assertEqual(str(self.document), 'Test Document')

# Form Tests
class ProjectFormTest(TestCase):
    """ProjectFormのテスト"""
    
    def test_project_form_valid(self):
        form_data = {
            'name': 'テストプロジェクト',
            'description': 'テスト用のプロジェクトです',
            'template_type': 'test_specification'
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_project_form_invalid(self):
        form_data = {
            'name': '',  # 名前は必須
            'description': 'テスト用のプロジェクトです',
            'template_type': 'test_specification'
        }
        form = ProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

# View Tests
class ProjectViewsTest(TestCase):
    """プロジェクト関連ビューのテスト"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.project = Project.objects.create(
            name='テストプロジェクト',
            description='テスト用のプロジェクトです',
            owner=self.user
        )
        self.client.login(username='testuser', password='testpassword')

    def test_project_list_view(self):
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/project_list.html')
        self.assertContains(response, 'テストプロジェクト')

    def test_project_detail_view(self):
        response = self.client.get(reverse('project_detail', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/project_detail.html')
        self.assertContains(response, 'テストプロジェクト')
