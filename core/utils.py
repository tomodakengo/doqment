import os
import openai
from django.conf import settings
from .models import OpenAIRequest

# OpenAI APIキーを設定
openai.api_key = settings.OPENAI_API_KEY


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
ガイドライン: {template.content_guidelines}

{template.ai_prompt if template.ai_prompt else '以下のセクションの内容を生成してください。'}

ISO/IEC/IEEE 29119標準に準拠したテスト文書を生成してください。
        """
        
        try:
            # OpenAI APIを呼び出し
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "あなたはISO/IEC/IEEE 29119標準に基づいたテスト文書を生成する専門家です。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7,
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