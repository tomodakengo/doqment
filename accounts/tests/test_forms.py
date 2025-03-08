from django.test import TestCase
from django.contrib.auth.models import User
from accounts.forms import SignUpForm, LoginForm


class SignUpFormTest(TestCase):
    """
    サインアップフォームのテスト
    """
    
    def test_signup_form_valid_data(self):
        """
        有効なデータでのフォーム検証テスト
        """
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_signup_form_invalid_data(self):
        """
        無効なデータでのフォーム検証テスト
        """
        # パスワードが一致しない
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'differentpassword'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        
        # メールアドレスが無効
        form_data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_signup_form_duplicate_username(self):
        """
        既存ユーザー名でのフォーム検証テスト
        """
        # 既存ユーザーの作成
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existingpassword'
        )
        
        # 既存ユーザー名でフォーム検証
        form_data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class LoginFormTest(TestCase):
    """
    ログインフォームのテスト
    """
    
    def setUp(self):
        # テスト用ユーザーの作成
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
    
    def test_login_form_valid_data(self):
        """
        有効なデータでのフォーム検証テスト
        """
        form_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_login_form_invalid_data(self):
        """
        無効なデータでのフォーム検証テスト
        """
        # ユーザー名が空
        form_data = {
            'username': '',
            'password': 'testpassword'
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        
        # パスワードが空
        form_data = {
            'username': 'testuser',
            'password': ''
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors) 