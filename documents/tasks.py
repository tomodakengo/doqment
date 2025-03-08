from celery import shared_task
from .models import Document, DocumentSection, GenerationTask, SectionTemplate
from core.utils import generate_test_document_with_progress


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
        
        # 進捗状況を更新する関数
        def update_progress(section_index, section_progress):
            # セクションごとの進捗状況を計算
            # section_indexは0から始まるので、完了したセクション数は+1する
            completed_sections = section_index
            
            # 現在処理中のセクションの進捗状況（0-100）
            current_section_progress = section_progress
            
            # 全体の進捗状況を計算
            # 完了したセクションは100%として計算し、現在処理中のセクションは部分的に計算
            overall_progress = int(((completed_sections * 100) + current_section_progress) / total_sections)
            
            # 進捗状況を更新
            task.completed_sections = completed_sections
            task.progress = min(overall_progress, 99)  # 完全に完了するまでは99%まで
            task.save()
        
        # OpenAI APIを使用してセクションを生成（進捗状況を更新しながら）
        sections_content = generate_test_document_with_progress(
            document.product_description, 
            section_templates,
            update_progress
        )
        
        # 生成されたセクションを保存
        for i, template in enumerate(section_templates):
            content = sections_content.get(template.id, '')
            DocumentSection.objects.create(
                document=document,
                template=template,
                title=template.title,
                content=content,
                order=template.order
            )
        
        # タスクを完了としてマーク
        task.status = 'completed'
        task.progress = 100
        task.completed_sections = total_sections
        task.save()
        
    except Exception as e:
        # エラーが発生した場合
        if task_id:
            task = GenerationTask.objects.get(id=task_id)
            task.status = 'failed'
            task.error_message = str(e)
            task.save()
        raise 