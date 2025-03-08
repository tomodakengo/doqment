from celery import shared_task
from .models import Document, DocumentSection, GenerationTask, SectionTemplate
from core.utils import generate_test_document


@shared_task
def generate_document_sections_task(document_id, task_id):
    """
    ドキュメントセクションを生成するCeleryタスク
    """
    try:
        # タスクと関連するドキュメントを取得
        task = GenerationTask.objects.get(id=task_id)
        document = Document.objects.get(id=document_id)
        
        # タスクのステータスを更新
        task.status = 'processing'
        task.save()
        
        # 既存のセクションを削除
        document.sections.all().delete()
        
        # プロジェクトのセクションテンプレートを取得
        section_templates = document.project.section_templates.all()
        
        # 合計セクション数を設定
        total_sections = section_templates.count()
        task.total_sections = total_sections
        task.save()
        
        if total_sections == 0:
            task.status = 'completed'
            task.progress = 100
            task.save()
            return
        
        # OpenAI APIを使用してセクションを生成
        sections_content = generate_test_document(document.product_description, section_templates)
        
        # 生成されたセクションを保存
        completed_sections = 0
        for template in section_templates:
            content = sections_content.get(template.id, '')
            DocumentSection.objects.create(
                document=document,
                template=template,
                title=template.title,
                content=content,
                order=template.order
            )
            
            # 進捗状況を更新
            completed_sections += 1
            progress = int((completed_sections / total_sections) * 100)
            
            task.completed_sections = completed_sections
            task.progress = progress
            task.save()
        
        # タスクを完了としてマーク
        task.status = 'completed'
        task.progress = 100
        task.save()
        
    except Exception as e:
        # エラーが発生した場合
        if task_id:
            task = GenerationTask.objects.get(id=task_id)
            task.status = 'failed'
            task.error_message = str(e)
            task.save()
        raise 