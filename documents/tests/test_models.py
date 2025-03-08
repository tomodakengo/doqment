from django.test import TestCase
from django.contrib.auth.models import User
from documents.models import Project, SectionTemplate, Document, DocumentSection, GenerationTask


class ProjectModelTest(TestCase):
    """
    Projectモデルのテスト
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test project description',
            created_by=self.user
        )
    
    def test_project_creation(self):
        """
        プロジェクト作成のテスト
        """
        self.assertEqual(self.project.name, 'Test Project')
        self.assertEqual(self.project.description, 'Test project description')
        self.assertEqual(self.project.created_by, self.user)
        self.assertEqual(self.project.template_type, 'test_specification')  # デフォルト値
    
    def test_project_str(self):
        """
        プロジェクトの文字列表現のテスト
        """
        self.assertEqual(str(self.project), 'Test Project')


class SectionTemplateModelTest(TestCase):
    """
    SectionTemplateモデルのテスト
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test project description',
            created_by=self.user
        )
        self.section_template = SectionTemplate.objects.create(
            project=self.project,
            title='Test Section',
            description='Test section description',
            form_type='text',
            content_guidelines='Test content guidelines',
            ai_prompt='Test AI prompt',
            order=1
        )
    
    def test_section_template_creation(self):
        """
        セクションテンプレート作成のテスト
        """
        self.assertEqual(self.section_template.project, self.project)
        self.assertEqual(self.section_template.title, 'Test Section')
        self.assertEqual(self.section_template.description, 'Test section description')
        self.assertEqual(self.section_template.form_type, 'text')
        self.assertEqual(self.section_template.content_guidelines, 'Test content guidelines')
        self.assertEqual(self.section_template.ai_prompt, 'Test AI prompt')
        self.assertEqual(self.section_template.order, 1)
    
    def test_section_template_str(self):
        """
        セクションテンプレートの文字列表現のテスト
        """
        expected_str = f'Test Section (Test Project)'
        self.assertEqual(str(self.section_template), expected_str)


class DocumentModelTest(TestCase):
    """
    Documentモデルのテスト
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test project description',
            created_by=self.user
        )
        self.document = Document.objects.create(
            project=self.project,
            title='Test Document',
            created_by=self.user
        )
    
    def test_document_creation(self):
        """
        ドキュメント作成のテスト
        """
        self.assertEqual(self.document.project, self.project)
        self.assertEqual(self.document.title, 'Test Document')
        self.assertEqual(self.document.created_by, self.user)
        self.assertIsNotNone(self.document.created_at)
        self.assertIsNotNone(self.document.updated_at)
    
    def test_document_str(self):
        """
        ドキュメントの文字列表現のテスト
        """
        self.assertEqual(str(self.document), 'Test Document')


class DocumentSectionModelTest(TestCase):
    """
    DocumentSectionモデルのテスト
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test project description',
            created_by=self.user
        )
        self.document = Document.objects.create(
            project=self.project,
            title='Test Document',
            created_by=self.user
        )
        self.section_template = SectionTemplate.objects.create(
            project=self.project,
            title='Test Section Template',
            description='Test template description',
            form_type='text',
            content_guidelines='Test content guidelines',
            ai_prompt='Test AI prompt',
            order=1
        )
        self.document_section = DocumentSection.objects.create(
            document=self.document,
            title='Test Section',
            content='Test content',
            section_template=self.section_template,
            order=1
        )
    
    def test_document_section_creation(self):
        """
        ドキュメントセクション作成のテスト
        """
        self.assertEqual(self.document_section.document, self.document)
        self.assertEqual(self.document_section.title, 'Test Section')
        self.assertEqual(self.document_section.content, 'Test content')
        self.assertEqual(self.document_section.section_template, self.section_template)
        self.assertEqual(self.document_section.order, 1)
        self.assertFalse(self.document_section.is_generating)
        self.assertEqual(self.document_section.generation_progress, 0)
    
    def test_document_section_str(self):
        """
        ドキュメントセクションの文字列表現のテスト
        """
        expected_str = f'Test Section (Test Document)'
        self.assertEqual(str(self.document_section), expected_str)


class GenerationTaskModelTest(TestCase):
    """
    GenerationTaskモデルのテスト
    """
    
    def setUp(self):
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
        self.document = Document.objects.create(
            project=self.project,
            title='テストドキュメント',
            description='テスト用のドキュメントです',
            created_by=self.user
        )
        self.task = GenerationTask.objects.create(
            document=self.document,
            task_id='test-task-id',
            status='processing',
            progress=50,
            total_sections=10,
            completed_sections=5
        )
    
    def test_generation_task_creation(self):
        """
        生成タスクが正しく作成されることをテスト
        """
        self.assertEqual(self.task.task_id, 'test-task-id')
        self.assertEqual(self.task.status, 'processing')
        self.assertEqual(self.task.progress, 50)
        self.assertEqual(self.task.total_sections, 10)
        self.assertEqual(self.task.completed_sections, 5)
    
    def test_generation_task_str(self):
        """
        __str__メソッドが正しく動作することをテスト
        """
        self.assertEqual(str(self.task), f"Generation Task for テストドキュメント (processing)") 