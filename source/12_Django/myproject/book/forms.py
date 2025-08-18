from django import forms
from django.core.validators import MinLengthValidator
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from .models import Book

def min_length_3_validator(value):
  if len(value)<3:
    raise forms.ValidationError('3글자 이상 입력하세요')   # raise 리턴이 아님 다른곳으로 넘어감
  
class Bookform(forms.Form): # 객체 생성
  title = forms.CharField(label="책제목")
  author = forms.CharField(label="글쓴이",
                            validators=[min_length_3_validator])
  
  publisher = forms.CharField(label="출판사",required=False) # 입력 안 해도 되도록 
  sales = forms.IntegerField(label="판매가",
                              initial=1000,
                              validators=[MinValueValidator(0),
                                          MaxValueValidator(100000)])
  def save(self, comit=True): # false book만 리턴, true는 저장하고 리턴
    book = Book(**self.cleaned_data) # cleaned_data 입력데이트들을 검증 완료 데이터
    if comit:
      book.save()
      return book

class BookModelForm(forms.ModelForm):
  class Meta:
    model = Book
    fields = ['title','author','publisher','sales']
    # fields = '__all__//'/