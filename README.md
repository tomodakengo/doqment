# Doqment

ISO/IEC/IEEE 29119標準に基づいたテスト仕様書とテスト計画を自動生成するウェブアプリケーション。

## 機能

- OpenAI APIを使用したテスト文書の自動生成
- セクションタイトル、コンテンツガイドライン、フォームタイプ、AIプロンプトのカスタマイズ
- プロジェクトごとのセクションテンプレートのカスタマイズと保存
- ユーザー認証システム（ユーザー名/パスワード）
- クリーンでモノクロマチックなデザイン

## 技術スタック

- フロントエンド: Django (HTML/JavaScript with Tailwind CSS)
- バックエンド: Django (Python)
- データベース: PostgreSQL
- 認証: 基本的なユーザー名/パスワード認証
- 統合: OpenAI API
- コンテナ化: Docker

## 開発環境のセットアップ

### 前提条件

- Docker と Docker Compose がインストールされていること
- OpenAI API キー

### インストール手順

1. リポジトリをクローンする:
   ```
   git clone <repository-url>
   cd doqment
   ```

2. 環境変数を設定する:
   `.env` ファイルを編集して、OpenAI API キーを設定します:
   ```
   OPENAI_API_KEY=your-openai-api-key
   ```

3. Docker コンテナをビルドして起動する:
   ```
   docker-compose up --build
   ```

4. マイグレーションを実行する:
   ```
   docker-compose exec web python manage.py migrate
   ```

5. スーパーユーザーを作成する:
   ```
   docker-compose exec web python manage.py createsuperuser
   ```

6. ブラウザで http://localhost:8000 にアクセスしてアプリケーションを使用する

## 使用方法

1. アカウントを作成してログインする
2. 新しいプロジェクトを作成する
3. テスト文書のテンプレートをカスタマイズする
4. 製品説明を入力してテスト仕様書を生成する
5. 必要に応じて生成された文書を編集する

## テスト

Doqmentプロジェクトには包括的なテストスイートが含まれています。テストは以下のように実行できます：

### 全てのテストを実行

```bash
python manage.py test
```

### 特定のアプリケーションのテストを実行

```bash
python manage.py test accounts
python manage.py test documents
python manage.py test core
```

### 特定のテストクラスを実行

```bash
python manage.py test documents.tests.test_models.ProjectModelTest
```

### カバレッジレポートの生成

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

より詳細なHTMLレポートを生成するには：

```bash
coverage html
```

その後、`htmlcov/index.html`をブラウザで開いてレポートを確認できます。

### CI/CD

このプロジェクトはGitHub Actionsを使用して継続的インテグレーションを実装しています。プッシュやプルリクエストが行われると、自動的にテストが実行されます。GitHub Actionsの設定は`.github/workflows/django-tests.yml`で確認できます。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。 