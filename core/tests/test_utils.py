from django.test import TestCase
from unittest.mock import patch, MagicMock
from core.utils import generate_test_document, generate_test_document_with_progress
from documents.models import Project, SectionTemplate
from django.contrib.auth.models import User


class MockTemplate:
    """
    テスト用のモックテンプレート
    """
    def __init__(self, id, title, description="", content_guidelines="", ai_prompt=""):
        self.id = id
        self.title = title
        self.description = description
        self.content_guidelines = content_guidelines
        self.ai_prompt = ai_prompt


class GenerateTestDocumentTest(TestCase):
    """
    generate_test_documentのテスト
    """
    
    @patch('core.utils.openai.ChatCompletion.create')
    def test_generate_test_document(self, mock_create):
        """
        generate_test_documentが正しく動作することをテスト
        """
        # モックの設定
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "テスト用のコンテンツ"
        mock_response.usage.total_tokens = 100
        mock_create.return_value = mock_response
        
        # テスト用のテンプレート
        templates = [
            MockTemplate(1, "テストセクション1"),
            MockTemplate(2, "テストセクション2")
        ]
        
        # 関数の実行
        result = generate_test_document("テスト用の製品説明", templates)
        
        # 結果の検証
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1], "テスト用のコンテンツ")
        self.assertEqual(result[2], "テスト用のコンテンツ")
        
        # モックが正しく呼び出されたことを確認
        self.assertEqual(mock_create.call_count, 2)
    
    @patch('core.utils.openai.ChatCompletion.create')
    def test_generate_test_document_error(self, mock_create):
        """
        エラーが発生した場合のテスト
        """
        # モックの設定
        mock_create.side_effect = Exception("テストエラー")
        
        # テスト用のテンプレート
        templates = [MockTemplate(1, "テストセクション")]
        
        # 関数の実行
        result = generate_test_document("テスト用の製品説明", templates)
        
        # 結果の検証
        self.assertEqual(len(result), 1)
        self.assertIn("エラーが発生しました", result[1])
        self.assertIn("テストエラー", result[1])


class GenerateTestDocumentWithProgressTest(TestCase):
    """
    generate_test_document_with_progressのテスト
    """
    
    @patch('core.utils.openai.ChatCompletion.create')
    @patch('core.utils.time.sleep')  # sleep関数をモック化
    def test_generate_test_document_with_progress(self, mock_sleep, mock_create):
        """
        generate_test_document_with_progressが正しく動作することをテスト
        """
        # モックの設定
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "テスト用のコンテンツ"
        mock_response.usage.total_tokens = 100
        mock_create.return_value = mock_response
        
        # プログレスコールバックのモック
        progress_callback = MagicMock()
        
        # テスト用のテンプレート
        templates = [
            MockTemplate(1, "テストセクション1"),
            MockTemplate(2, "テストセクション2")
        ]
        
        # 関数の実行
        result = generate_test_document_with_progress("テスト用の製品説明", templates, progress_callback)
        
        # 結果の検証
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1], "テスト用のコンテンツ")
        self.assertEqual(result[2], "テスト用のコンテンツ")
        
        # モックが正しく呼び出されたことを確認
        self.assertEqual(mock_create.call_count, 2)
        
        # プログレスコールバックが正しく呼び出されたことを確認
        # 各テンプレートに対して4回呼び出される（開始時、APIリクエスト時、レスポンス受信時、完了時）
        self.assertEqual(progress_callback.call_count, 8)
        
        # sleepが呼び出されたことを確認
        self.assertEqual(mock_sleep.call_count, 2) 