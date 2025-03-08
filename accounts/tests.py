from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.forms import SignUpForm, LoginForm

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
        # GETリクエストのテスト
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

        # 正しい認証情報でのPOSTリクエストのテスト
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # リダイレクト
        self.assertRedirects(response, reverse('dashboard'))

        # 間違った認証情報でのPOSTリクエストのテスト
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertContains(response, "ユーザー名またはパスワードが正しくありません")

    def test_signup_view(self):
        """サインアップビューのテスト"""
        # GETリクエストのテスト
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

        # 有効なデータでのPOSTリクエストのテスト
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)  # リダイレクト
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

        # 無効なデータでのPOSTリクエストのテスト
        response = self.client.post(reverse('signup'), {
            'username': 'anotheruser',
            'email': 'invalid-email',
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
        
        # ログアウト後はログインページにリダイレクトされるはず
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        
        # セッションがクリアされていることを確認
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_dashboard_view(self):
        """ダッシュボードビューのテスト"""
        # ログインしていない状態でのアクセス
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # リダイレクト
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")
        
        # ログイン状態でのアクセス
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')


class SignUpFormTest(TestCase):
    """サインアップフォームのテストクラス"""

    def test_signup_form_valid_data(self):
        """有効なデータでのフォームテスト"""
        form = SignUpForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpassword123'))

    def test_signup_form_invalid_data(self):
        """無効なデータでのフォームテスト"""
        # パスワードが一致しない場合
        form = SignUpForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'differentpassword'
        })
        
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        
        # 無効なメールアドレスの場合
        form = SignUpForm(data={
            'username': 'testuser',
            'email': 'invalid-email',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        
        # ユーザー名が空の場合
        form = SignUpForm(data={
            'username': '',
            'email': 'test@example.com',
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
        form = SignUpForm(data={
            'username': 'existinguser',
            'email': 'another@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('既に存在するユーザー名です', str(form.errors['username']))


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
        form = LoginForm(data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        
        self.assertTrue(form.is_valid())
        
        # フォームの認証メソッドをテスト
        user = form.authenticate_user()
        self.assertEqual(user, self.user)

    def test_login_form_invalid_data(self):
        """無効なデータでのフォームテスト"""
        # 存在しないユーザー名
        form = LoginForm(data={
            'username': 'nonexistentuser',
            'password': 'testpassword'
        })
        
        self.assertTrue(form.is_valid())  # フォーム自体は有効（フィールド検証は通過）
        self.assertIsNone(form.authenticate_user())  # しかし認証は失敗
        
        # 間違ったパスワード
        form = LoginForm(data={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        self.assertTrue(form.is_valid())  # フォーム自体は有効
        self.assertIsNone(form.authenticate_user())  # しかし認証は失敗
        
        # 空のユーザー名
        form = LoginForm(data={
            'username': '',
            'password': 'testpassword'
        })
        
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        
        # 空のパスワード
        form = LoginForm(data={
            'username': 'testuser',
            'password': ''
        })
        
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
