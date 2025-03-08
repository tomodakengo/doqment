from django.contrib import admin
from .models import OpenAIRequest


@admin.register(OpenAIRequest)
class OpenAIRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'tokens_used', 'created_at')
    search_fields = ('prompt', 'response')
    list_filter = ('created_at',)
