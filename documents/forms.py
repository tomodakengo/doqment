from django import forms
from .models import Project, SectionTemplate, Document, DocumentSection


class ProjectForm(forms.ModelForm):
    """
    プロジェクト作成・編集フォーム
    """
    class Meta:
        model = Project
        fields = ['name', 'description', 'template_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-700 text-gray-900'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-700 text-gray-900', 'rows': 4}),
            'template_type': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-700 text-gray-900'}),
        }
        labels = {
            'name': 'プロジェクト名',
            'description': '説明',
            'template_type': 'テンプレートタイプ',
        }


class SectionTemplateForm(forms.ModelForm):
    """
    セクションテンプレート作成・編集フォーム
    """
    class Meta:
        model = SectionTemplate
        fields = ['title', 'description', 'form_type', 'content_guidelines', 'ai_prompt', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-700 text-gray-900'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-700 text-gray-900', 'rows': 2}),
            'form_type': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-700 text-gray-900'}),
            'content_guidelines': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-700 text-gray-900', 'rows': 4}),
            'ai_prompt': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-700 text-gray-900', 'rows': 4}),
            'order': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-700 text-gray-900'}),
        }
        labels = {
            'title': 'タイトル',
            'description': '説明',
            'form_type': 'フォームタイプ',
            'content_guidelines': 'コンテンツガイドライン',
            'ai_prompt': 'AIプロンプト',
            'order': '表示順',
        }


class DocumentForm(forms.ModelForm):
    """
    ドキュメント作成・編集フォーム
    """
    class Meta:
        model = Document
        fields = ['title', 'description', 'product_description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-700 text-gray-900'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-700 text-gray-900', 'rows': 2}),
            'product_description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-700 text-gray-900', 'rows': 6}),
        }
        labels = {
            'title': 'タイトル',
            'description': '説明',
            'product_description': '製品説明',
        }


class DocumentSectionForm(forms.ModelForm):
    """
    ドキュメントセクション編集フォーム
    """
    class Meta:
        model = DocumentSection
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-700 text-gray-900'}),
            'content': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-700 text-gray-900', 'rows': 10}),
        }
        labels = {
            'title': 'タイトル',
            'content': '内容',
        } 