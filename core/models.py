from django.db import models

# Create your models here.

class OpenAIRequest(models.Model):
    prompt = models.TextField()
    response = models.TextField()
    tokens_used = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OpenAI Request {self.id} - {self.created_at}"
