from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from documents.models import Project, SectionTemplate, Document, DocumentSection, GenerationTask


class ProjectViewsTest(TestCase):
    """
    プロジェクト関連ビューのテスト
    """
    
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
            owner=self.user,
            template_type='test_specification'
        )
        
        # ログイン
        self.client.login(username='testuser', password='testpassword')
    
    def test_project_list_view(self):
        """
        プロジェクト一覧ビューのテスト
        """
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/project_list.html')
        self.assertContains(response, 'テストプロジェクト')
    
    def test_project_detail_view(self):
        """
        プロジェクト詳細ビューのテスト
        """
        response = self.client.get(reverse('project_detail', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/project_detail.html')
        self.assertContains(response, 'テストプロジェクト')
    
    def test_project_create_view(self):
        """
        プロジェクト作成ビューのテスト
        """
        # GET
        response = self.client.get(reverse('project_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/project_form.html')
        
        # POST
        project_data = {
            'name': '新しいプロジェクト',
            'description': '新しいプロジェクトの説明',
            'template_type': 'test_plan'
        }
        response = self.client.post(reverse('project_create'), project_data)
        self.assertEqual(response.status_code, 302)  # リダイレクト
        
        # 新しいプロジェクトが作成されたことを確認
        self.assertTrue(Project.objects.filter(name='新しいプロジェクト').exists())
    
    def test_project_update_view(self):
        """
        プロジェクト更新ビューのテスト
        """
        # GET
        response = self.client.get(reverse('project_update', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/project_form.html')
        
        # POST
        updated_data = {
            'name': '更新されたプロジェクト',
            'description': '更新された説明',
            'template_type': 'test_report'
        }
        response = self.client.post(reverse('project_update', args=[self.project.id]), updated_data)
        self.assertEqual(response.status_code, 302)  # リダイレクト
        
        # プロジェクトが更新されたことを確認
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, '更新されたプロジェクト')
        self.assertEqual(self.project.description, '更新された説明')
        self.assertEqual(self.project.template_type, 'test_report')
    
    def test_project_delete_view(self):
        """
        プロジェクト削除ビューのテスト
        """
        # GET
        response = self.client.get(reverse('project_delete', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/project_confirm_delete.html')
        
        # POST
        response = self.client.post(reverse('project_delete', args=[self.project.id]))
        self.assertEqual(response.status_code, 302)  # リダイレクト
        
        # プロジェクトが削除されたことを確認
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())


class SectionTemplateViewsTest(TestCase):
    """
    セクションテンプレート関連ビューのテスト
    """
    
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
        self.section_template = SectionTemplate.objects.create(
            project=self.project,
            title='テストセクション',
            description='テスト用のセクションです',
            form_type='textarea',
            content_guidelines='テスト用のガイドラインです',
            ai_prompt='テスト用のAIプロンプトです',
            order=1
        )
        
        # ログイン
        self.client.login(username='testuser', password='testpassword')
    
    def test_section_template_create_view(self):
        """
        セクションテンプレート作成ビューのテスト
        """
        # GET
        response = self.client.get(reverse('section_template_create', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/section_template_form.html')
        
        # POST
        template_data = {
            'title': '新しいセクション',
            'description': '新しいセクションの説明',
            'form_type': 'markdown',
            'content_guidelines': '新しいガイドライン',
            'ai_prompt': '新しいAIプロンプト',
            'order': 2
        }
        response = self.client.post(reverse('section_template_create', args=[self.project.id]), template_data)
        self.assertEqual(response.status_code, 302)  # リダイレクト
        
        # 新しいセクションテンプレートが作成されたことを確認
        self.assertTrue(SectionTemplate.objects.filter(title='新しいセクション').exists())
    
    def test_section_template_update_view(self):
        """
        セクションテンプレート更新ビューのテスト
        """
        # GET
        response = self.client.get(reverse('section_template_update', args=[self.section_template.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/section_template_form.html')
        
        # POST
        updated_data = {
            'title': '更新されたセクション',
            'description': '更新された説明',
            'form_type': 'table',
            'content_guidelines': '更新されたガイドライン',
            'ai_prompt': '更新されたAIプロンプト',
            'order': 3
        }
        response = self.client.post(reverse('section_template_update', args=[self.section_template.id]), updated_data)
        self.assertEqual(response.status_code, 302)  # リダイレクト
        
        # セクションテンプレートが更新されたことを確認
        self.section_template.refresh_from_db()
        self.assertEqual(self.section_template.title, '更新されたセクション')
        self.assertEqual(self.section_template.form_type, 'table')
    
    def test_section_template_delete_view(self):
        """
        セクションテンプレート削除ビューのテスト
        """
        # GET
        response = self.client.get(reverse('section_template_delete', args=[self.section_template.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/section_template_confirm_delete.html')
        
        # POST
        response = self.client.post(reverse('section_template_delete', args=[self.section_template.id]))
        self.assertEqual(response.status_code, 302)  # リダイレクト
        
        # セクションテンプレートが削除されたことを確認
        self.assertFalse(SectionTemplate.objects.filter(id=self.section_template.id).exists())


class DocumentViewsTest(TestCase):
    """
    ドキュメント関連ビューのテスト
    """
    
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
        self.document = Document.objects.create(
            project=self.project,
            title='テストドキュメント',
            description='テスト用のドキュメントです',
            product_description='テスト用の製品説明です',
            created_by=self.user
        )
        self.section_template = SectionTemplate.objects.create(
            project=self.project,
            title='テストセクション',
            description='テスト用のセクションです',
            form_type='textarea',
            order=1
        )
        self.document_section = DocumentSection.objects.create(
            document=self.document,
            template=self.section_template,
            title='テストセクション',
            content='テスト用のコンテンツです',
            order=1
        )
        
        # ログイン
        self.client.login(username='testuser', password='testpassword')
    
    def test_document_detail_view(self):
        """
        ドキュメント詳細ビューのテスト
        """
        response = self.client.get(reverse('document_detail', args=[self.document.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/document_detail.html')
        self.assertContains(response, 'テストドキュメント')
        self.assertContains(response, 'テストセクション')
    
    def test_document_create_view(self):
        """
        ドキュメント作成ビューのテスト
        """
        # GET
        response = self.client.get(reverse('document_create', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/document_form.html')
        
        # POST
        document_data = {
            'title': '新しいドキュメント',
            'description': '新しいドキュメントの説明',
            'product_description': '新しい製品説明'
        }
        response = self.client.post(reverse('document_create', args=[self.project.id]), document_data)
        self.assertEqual(response.status_code, 302)  # リダイレクト
        
        # 新しいドキュメントが作成されたことを確認
        self.assertTrue(Document.objects.filter(title='新しいドキュメント').exists())
    
    def test_document_update_view(self):
        """
        ドキュメント更新ビューのテスト
        """
        # GET
        response = self.client.get(reverse('document_update', args=[self.document.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/document_form.html')
        
        # POST
        updated_data = {
            'title': '更新されたドキュメント',
            'description': '更新された説明',
            'product_description': '更新された製品説明'
        }
        response = self.client.post(reverse('document_update', args=[self.document.id]), updated_data)
        self.assertEqual(response.status_code, 302)  # リダイレクト
        
        # ドキュメントが更新されたことを確認
        self.document.refresh_from_db()
        self.assertEqual(self.document.title, '更新されたドキュメント')
        self.assertEqual(self.document.description, '更新された説明')
    
    def test_document_delete_view(self):
        """
        ドキュメント削除ビューのテスト
        """
        # GET
        response = self.client.get(reverse('document_delete', args=[self.document.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/document_confirm_delete.html')
        
        # POST
        response = self.client.post(reverse('document_delete', args=[self.document.id]))
        self.assertEqual(response.status_code, 302)  # リダイレクト
        
        # ドキュメントが削除されたことを確認
        self.assertFalse(Document.objects.filter(id=self.document.id).exists())
    
    def test_document_section_update_view(self):
        """
        ドキュメントセクション更新ビューのテスト
        """
        # GET
        response = self.client.get(reverse('document_section_update', args=[self.document_section.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/document_section_form.html')
        
        # POST
        updated_data = {
            'title': '更新されたセクション',
            'content': '更新されたコンテンツ'
        }
        response = self.client.post(reverse('document_section_update', args=[self.document_section.id]), updated_data)
        self.assertEqual(response.status_code, 302)  # リダイレクト
        
        # ドキュメントセクションが更新されたことを確認
        self.document_section.refresh_from_db()
        self.assertEqual(self.document_section.title, '更新されたセクション')
        self.assertEqual(self.document_section.content, '更新されたコンテンツ') 