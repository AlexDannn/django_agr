from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, default="Other")
    link = models.CharField(max_length=200, default="", unique=True)
    published = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source = models.CharField(max_length=30, default="", blank=True, null=True)
    
