from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class AccountsViewsTest(TestCase):
    """
    アカウント関連ビューのテスト
    """
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
    
    def test_login_view(self):
        """
        ログインビューのテスト
        """
        # GET
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        
        # POST - 正しい認証情報
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 302)  # リダイレクト
        
        # ログイン状態の確認
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
        # POST - 誤った認証情報
        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 200)  # エラーメッセージと共に再表示
        self.assertFalse(response.context['user'].is_authenticated)
    
    def test_signup_view(self):
        """
        サインアップビューのテスト
        """
        # GET
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        
        # POST - 有効なデータ
        signup_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(reverse('signup'), signup_data)
        self.assertEqual(response.status_code, 302)  # リダイレクト
        
        # 新しいユーザーが作成されたことを確認
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # POST - 無効なデータ（パスワードが一致しない）
        signup_data = {
            'username': 'anotheruser',
            'email': 'another@example.com',
            'password1': 'password123',
            'password2': 'password456'
        }
        response = self.client.post(reverse('signup'), signup_data)
        self.assertEqual(response.status_code, 200)  # エラーメッセージと共に再表示
        
        # ユーザーが作成されていないことを確認
        self.assertFalse(User.objects.filter(username='anotheruser').exists())
    
    def test_logout_view(self):
        """
        ログアウトビューのテスト
        """
        # ログイン
        self.client.login(username='testuser', password='testpassword')
        
        # ログアウト
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # リダイレクト
        
        # ログアウト状態の確認
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # ログインページにリダイレクト
    
    def test_dashboard_view(self):
        """
        ダッシュボードビューのテスト
        """
        # 未ログイン状態
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # ログインページにリダイレクト
        
        # ログイン
        self.client.login(username='testuser', password='testpassword')
        
        # ログイン状態
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html') 