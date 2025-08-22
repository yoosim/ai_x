from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
  user = models.OneToOneField(User,
          on_delete=models.CASCADE) # User가 삭제될 때, profile은 어떻게 할지?
  phone_number = models.CharField(verbose_name="전화", max_length=20)
  address      = models.CharField(verbose_name="주소", max_length=100)
  def __str__(self):
    return "{}({}-{})".format(self.user.username,
                              self.phone_number,
                              self.address)
  
# 이벤트 처리==signals사용(post_save) : profile.save() 성공시 가입인사를 메일로 전송
from django.db.models.signals import post_save
from django.core.mail import send_mail
from  decouple import config
def on_send_mail(sender, **kwargs):
  print('★ on_send_mail', kwargs) 
  if kwargs['created']: # True : 회원가입한 경우 / False : 각종 회원정보 수정
    user = kwargs['instance'].user  # sender 
    if not user.email: # 회원가입시 메일 입력 안 함
      print('★ 메일 주소가 없어서 전송되지 않음')
      return
    # 메일 전송
    subject = f"{user.username}님 가입해주셔서 감사합니다."
    body = f"안녕하세요 {user.username}님\n\n 가입인사를 받으시면 최고의 서비스듣 드립니다.\n\n 감사합니다.(메일내용)"
    bodyhtml = f"<p>안녕하세요 {user.username}님</p><p>가입인사를 받으시면 최고의 서비스듣 드립니다.</p><p>감사합니다.(메일내용)</p>"
    # settings.py에 EMAIL_BACKEND 설정 
    send_mail(
      subject=subject,
      message=body,
      from_email="uuuuimm091@gmail.com",
      recipient_list=[user.email],
      html_message=bodyhtml,
      fail_silently=False, # 메일 전송이 안 되었을 경우, 아무일도 하지 않음 (히스토리 등)

    )

# on_send_mail 함수와  post_save로 연결 # on_send_mail은 메일 전송시 실행되는 함수
post_save.connect(on_send_mail, sender=Profile)