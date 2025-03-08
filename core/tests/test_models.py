from django.test import TestCase
from core.models import OpenAIRequest


class OpenAIRequestModelTest(TestCase):
    """
    OpenAIRequestモデルのテスト
    """
    
    def setUp(self):
        self.openai_request = OpenAIRequest.objects.create(
            prompt='テスト用のプロンプト',
            response='テスト用のレスポンス',
            tokens_used=100
        )
    
    def test_openai_request_creation(self):
        """
        OpenAIRequestが正しく作成されることをテスト
        """
        self.assertEqual(self.openai_request.prompt, 'テスト用のプロンプト')
        self.assertEqual(self.openai_request.response, 'テスト用のレスポンス')
        self.assertEqual(self.openai_request.tokens_used, 100)
    
    def test_openai_request_str(self):
        """
        __str__メソッドが正しく動作することをテスト
        """
        expected_str = f"OpenAI Request {self.openai_request.id} - {self.openai_request.created_at}"
        self.assertEqual(str(self.openai_request), expected_str) 