from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.forms import CustomUserCreationForm, CustomAuthenticationForm

class AccountsViewsTest(TestCase):
    """アカウント関連のビューをテストするクラス"""

    def setUp(self):
        """テスト用のユーザーを作成"""
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_login_view(self):
        """ログインビューのテスト"""
        # GETリクエストのテスト - ログインしていない状態
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

        # 正しい認証情報でのPOSTリクエストのテスト
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # リダイレクト
        # ログイン後はダッシュボードにリダイレクトされるはず

        # ログアウトしてから再テスト
        self.client.logout()

        # 間違った認証情報でのPOSTリクエストのテスト
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_signup_view(self):
        """サインアップビューのテスト"""
        # GETリクエストのテスト
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

        # 有効なデータでのPOSTリクエストのテスト
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)  # リダイレクト
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

        # 無効なデータでのPOSTリクエストのテスト
        response = self.client.post(reverse('signup'), {
            'username': 'anotheruser',
            'password1': 'pass123',
            'password2': 'pass456'  # パスワードが一致しない
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertFalse(User.objects.filter(username='anotheruser').exists())

    def test_logout_view(self):
        """ログアウトビューのテスト"""
        # ユーザーをログインさせる
        self.client.login(username='testuser', password='testpassword')
        
        # ログアウトリクエストを送信
        response = self.client.get(reverse('logout'))
        
        # ログアウト後はホームページにリダイレクトされるはず
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        
        # セッションがクリアされていることを確認
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_dashboard_view(self):
        """ダッシュボードビューのテスト"""
        # ログインしていない状態でのアクセス
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # リダイレクト
        
        # ログイン状態でのアクセス
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/dashboard.html')


class SignUpFormTest(TestCase):
    """サインアップフォームのテストクラス"""

    def test_signup_form_valid_data(self):
        """有効なデータでのフォームテスト"""
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpassword123'))

    def test_signup_form_invalid_data(self):
        """無効なデータでのフォームテスト"""
        # パスワードが一致しない場合
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'differentpassword'
        })
        
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        
        # ユーザー名が空の場合
        form = CustomUserCreationForm(data={
            'username': '',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_signup_form_duplicate_username(self):
        """既存のユーザー名でのフォームテスト"""
        # 最初のユーザーを作成
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existingpassword'
        )
        
        # 同じユーザー名で別のユーザーを作成しようとする
        form = CustomUserCreationForm(data={
            'username': 'existinguser',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class LoginFormTest(TestCase):
    """ログインフォームのテストクラス"""

    def setUp(self):
        """テスト用ユーザーの作成"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_login_form_valid_data(self):
        """有効なデータでのフォームテスト"""
        form = CustomAuthenticationForm(data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        
        self.assertTrue(form.is_valid())

    def test_login_form_invalid_data(self):
        """無効なデータでのフォームテスト"""
        # 存在しないユーザー名
        form = CustomAuthenticationForm(data={
            'username': 'nonexistentuser',
            'password': 'testpassword'
        })
        
        self.assertFalse(form.is_valid())
        
        # 間違ったパスワード
        form = CustomAuthenticationForm(data={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        self.assertFalse(form.is_valid())
        
        # 空のユーザー名
        form = CustomAuthenticationForm(data={
            'username': '',
            'password': 'testpassword'
        })
        
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        
        # 空のパスワード
        form = CustomAuthenticationForm(data={
            'username': 'testuser',
            'password': ''
        })
        
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
