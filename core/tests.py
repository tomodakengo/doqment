from django.test import TestCase
from django.contrib.auth.models import User
from core.models import OpenAIRequest

# Test models
class OpenAIRequestModelTest(TestCase):
    def setUp(self):
        self.request = OpenAIRequest.objects.create(
            prompt='Test prompt',
            response='Test response',
            tokens_used=100
        )

    def test_request_creation(self):
        self.assertEqual(self.request.prompt, 'Test prompt')
        self.assertEqual(self.request.response, 'Test response')
        self.assertEqual(self.request.tokens_used, 100)

    def test_request_str(self):
        self.assertIn(f"OpenAI Request {self.request.id}", str(self.request))
