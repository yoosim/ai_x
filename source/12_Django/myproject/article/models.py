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

  photo = models.ImageField(verbose_name="사진",
                            blank=True,  # DB에는 파일명 _media/ 폴더에 저장
                            upload_to="article/%Y/%m/%d") #_media/article/2025/08/19 폴더에 저장
  
  # DB에는 "_media/article/2025/08/19/a.jpg"첨부파일은 upload_to에 저장

  def __str__(self):
    return self.title
  def get_absolute_url(self):
      # return reverse("article:list") # create, update 후 url로 이동
      return reverse("article:detail", args=[self.id]) # create, update 후 상세보기 페이지로 이동
  
  def delete(self, *args, **kwargs): 
    # DB 삭제 전 self.photo 파일 삭제 
    if self.photo: # 파일 첨부 여부
      file_path = os.path.join(settings.BASE_DIR,'_media', str(self.photo))
      print(file_path, "파일 지우고, DB delete")
      if os.path.exists(file_path):
        os.remove(file_path) # 파일 삭제 
    super().delete(args,kwargs)   # DB에서 현재 instance delete
  def save(self, *args, **kwargs):
    if self.pk: # 수정 여부(create가 아님)
      old_instance = get_object_or_404(Article, pk=self.pk)
      if old_instance.photo and old_instance.photo != self.photo : # DB에 photo가 있는지, 수정될 photo가 DB와 다를때
        file_path = os.path.join(settings.MEDIA_ROOT, str(old_instance.photo))
        if os.path.exists(file_path):
          os.remove(file_path)
    super().save(args, kwargs)
      



  class Meta:
      ordering = ['-id'] # id 내림차순 정렬
