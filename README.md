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

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。 