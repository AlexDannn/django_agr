from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Scrap(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('scrap-detail', kwargs={'pk': self.pk})
