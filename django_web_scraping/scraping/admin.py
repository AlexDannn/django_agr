from django.contrib import admin

from .models import News
# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    fieldsets = [
            ("News", {"fields": ["title", "link", "published"]}),
            ("Source", {"fields": ["source"]}),
            ]

admin.site.register(News, NewsAdmin)
