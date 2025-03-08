import os
from celery import Celery

# Djangoの設定モジュールをCeleryのデフォルト設定として設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doqment.settings')

app = Celery('doqment')

# 設定モジュールの設定値をCeleryの名前空間から読み込む
app.config_from_object('django.conf:settings', namespace='CELERY')

# 登録されたDjangoアプリケーションからタスクを自動的に検出
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}') 