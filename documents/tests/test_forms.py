from django.test import TestCase
from django.contrib.auth.models import User
from documents.models import Project, SectionTemplate, Document
from documents.forms import ProjectForm, SectionTemplateForm, DocumentForm, DocumentSectionForm


class ProjectFormTest(TestCase):
    """
    ProjectFormのテスト
    """
    
    def test_project_form_valid(self):
        """
        有効なデータでフォームが正しく検証されることをテスト
        """
        form_data = {
            'name': 'テストプロジェクト',
            'description': 'テスト用のプロジェクトです',
            'template_type': 'test_specification'
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_project_form_invalid(self):
        """
        無効なデータでフォームが正しく検証されることをテスト
        """
        # 名前が空の場合
        form_data = {
            'name': '',
            'description': 'テスト用のプロジェクトです',
            'template_type': 'test_specification'
        }
        form = ProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class SectionTemplateFormTest(TestCase):
    """
    SectionTemplateFormのテスト
    """
    
    def test_section_template_form_valid(self):
        """
        有効なデータでフォームが正しく検証されることをテスト
        """
        form_data = {
            'title': 'テストセクション',
            'description': 'テスト用のセクションです',
            'form_type': 'textarea',
            'content_guidelines': 'テスト用のガイドラインです',
            'ai_prompt': 'テスト用のAIプロンプトです',
            'order': 1
        }
        form = SectionTemplateForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_section_template_form_invalid(self):
        """
        無効なデータでフォームが正しく検証されることをテスト
        """
        # タイトルが空の場合
        form_data = {
            'title': '',
            'description': 'テスト用のセクションです',
            'form_type': 'textarea',
            'content_guidelines': 'テスト用のガイドラインです',
            'ai_prompt': 'テスト用のAIプロンプトです',
            'order': 1
        }
        form = SectionTemplateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)


class DocumentFormTest(TestCase):
    """
    DocumentFormのテスト
    """
    
    def test_document_form_valid(self):
        """
        有効なデータでフォームが正しく検証されることをテスト
        """
        form_data = {
            'title': 'テストドキュメント',
            'description': 'テスト用のドキュメントです',
            'product_description': 'テスト用の製品説明です'
        }
        form = DocumentForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_document_form_invalid(self):
        """
        無効なデータでフォームが正しく検証されることをテスト
        """
        # タイトルが空の場合
        form_data = {
            'title': '',
            'description': 'テスト用のドキュメントです',
            'product_description': 'テスト用の製品説明です'
        }
        form = DocumentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)


class DocumentSectionFormTest(TestCase):
    """
    DocumentSectionFormのテスト
    """
    
    def test_document_section_form_valid(self):
        """
        有効なデータでフォームが正しく検証されることをテスト
        """
        form_data = {
            'title': 'テストセクション',
            'content': 'テスト用のコンテンツです'
        }
        form = DocumentSectionForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_document_section_form_invalid(self):
        """
        無効なデータでフォームが正しく検証されることをテスト
        """
        # タイトルが空の場合
        form_data = {
            'title': '',
            'content': 'テスト用のコンテンツです'
        }
        form = DocumentSectionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors) 