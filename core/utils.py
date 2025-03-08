import os
import openai
import time
from django.conf import settings
from .models import OpenAIRequest

# OpenAI APIキーを設定
openai.api_key = os.environ.get('OPENAI_API_KEY')


def generate_test_document(product_description, section_templates):
    """
    OpenAI APIを使用してテスト文書を生成する
    
    Args:
        product_description (str): 製品説明
        section_templates (list): セクションテンプレートのリスト
        
    Returns:
        dict: 生成されたセクションの内容
    """
    sections_content = {}
    
    for template in section_templates:
        # プロンプトを作成
        prompt = f"""
製品説明:
{product_description}

セクション: {template.title}
説明: {template.description}
ガイドライン: {template.content_guidelines}

{template.ai_prompt if template.ai_prompt else '以下のセクションの内容を生成してください。'}

以下の点に注意して、ISO/IEC/IEEE 29119標準に準拠した高品質なテスト文書を生成してください：
1. 具体的かつ明確な内容を記述してください
2. テスト対象の製品特性を考慮してください
3. 実用的で実施可能な内容にしてください
4. 論理的な構成と適切な専門用語を使用してください
5. 必要に応じて箇条書きや表形式を使用して読みやすくしてください
        """
        
        try:
            # OpenAI APIを呼び出し
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "あなたはISO/IEC/IEEE 29119標準に基づいたテスト文書を生成する専門家です。テスト計画、テスト仕様書、テスト結果報告書などの文書を作成するための豊富な知識と経験を持っています。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.5,
            )
            
            # レスポンスからコンテンツを取得
            content = response.choices[0].message.content
            
            # トークン使用量を計算
            tokens_used = response.usage.total_tokens
            
            # OpenAIRequestモデルに保存
            OpenAIRequest.objects.create(
                prompt=prompt,
                response=content,
                tokens_used=tokens_used
            )
            
            # 結果を辞書に追加
            sections_content[template.id] = content
            
        except Exception as e:
            # エラーが発生した場合はエラーメッセージを返す
            sections_content[template.id] = f"エラーが発生しました: {str(e)}"
    
    return sections_content


def generate_test_document_with_progress(product_description, section_templates, progress_callback=None):
    """
    OpenAI APIを使用してテスト文書を生成し、進捗状況を更新する
    
    Args:
        product_description (str): 製品説明
        section_templates (list): セクションテンプレートのリスト
        progress_callback (function): 進捗状況を更新するコールバック関数
            引数: section_index (int), section_progress (int)
        
    Returns:
        dict: 生成されたセクションの内容
    """
    sections_content = {}
    
    for i, template in enumerate(section_templates):
        # 進捗状況を更新（セクション開始時）
        if progress_callback:
            progress_callback(i, 0)
        
        # プロンプトを作成
        prompt = f"""
製品説明:
{product_description}

セクション: {template.title}
説明: {template.description}
ガイドライン: {template.content_guidelines}

{template.ai_prompt if template.ai_prompt else '以下のセクションの内容を生成してください。'}

以下の点に注意して、ISO/IEC/IEEE 29119標準に準拠した高品質なテスト文書を生成してください：
1. 具体的かつ明確な内容を記述してください
2. テスト対象の製品特性を考慮してください
3. 実用的で実施可能な内容にしてください
4. 論理的な構成と適切な専門用語を使用してください
5. 必要に応じて箇条書きや表形式を使用して読みやすくしてください
        """
        
        try:
            # 進捗状況を更新（APIリクエスト開始時）
            if progress_callback:
                progress_callback(i, 10)
            
            # OpenAI APIを呼び出し
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "あなたはISO/IEC/IEEE 29119標準に基づいたテスト文書を生成する専門家です。テスト計画、テスト仕様書、テスト結果報告書などの文書を作成するための豊富な知識と経験を持っています。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.5,
            )
            
            # 進捗状況を更新（APIレスポンス受信時）
            if progress_callback:
                progress_callback(i, 50)
            
            # レスポンスからコンテンツを取得
            content = response.choices[0].message.content
            
            # トークン使用量を計算
            tokens_used = response.usage.total_tokens
            
            # 進捗状況を更新（データベース保存前）
            if progress_callback:
                progress_callback(i, 75)
            
            # OpenAIRequestモデルに保存
            OpenAIRequest.objects.create(
                prompt=prompt,
                response=content,
                tokens_used=tokens_used
            )
            
            # 結果を辞書に追加
            sections_content[template.id] = content
            
            # 進捗状況を更新（セクション完了時）
            if progress_callback:
                progress_callback(i, 100)
                
            # 少し待機して、進捗状況の変化を視覚的に確認できるようにする
            time.sleep(0.5)
            
        except Exception as e:
            # エラーが発生した場合はエラーメッセージを返す
            sections_content[template.id] = f"エラーが発生しました: {str(e)}"
    
    return sections_content 