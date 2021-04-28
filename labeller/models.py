from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Snippet(models.Model):
    text = models.TextField()
    entity = models.CharField(max_length=63)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

class Evaluated_Snippet(models.Model):
    evaluator = models.ForeignKey(User, related_name='evaluated_snippets', on_delete=models.RESTRICT, blank=True)
    snippet = models.ForeignKey(Snippet, related_name='evaluated_snippets', on_delete=models.RESTRICT, blank=True)
    is_spam = models.BooleanField(default=False)
    entity = models.CharField(max_length=63)
    is_harmful = models.BooleanField(default=False)
    is_opinion = models.BooleanField(default=False)
    is_fact = models.BooleanField(default=False)
    product_mention = models.BooleanField(default=False)
    extracted_span = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)


