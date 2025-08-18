import os.path
from django.db import models
import time
from datetime import datetime
from django.urls import reverse
from myproject import settings
from django.shortcuts import get_object_or_404
STATUS_CHOICES = (
  ('d', 'Draft'),
  ('p', 'Published'),
  ('w', 'Withdrawn'),
)

class Article(models.Model):
  title = models.CharField(verbose_name="제목",max_length=100)
  body = models.TextField(verbose_name="본문")
  status =  models.CharField(max_length=1, choices=STATUS_CHOICES)

  def __str__(self):
    return self.title
  def get_absolute_url(self):
      # return reverse("article:list") # create, update 후 url로 이동
      return reverse("article:detail", args=[self.id]) # create, update 후 상세보기 페이지로 이동
