from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile

class SignupForm(UserCreationForm):
  phone_number = forms.CharField(label="전화", max_length=20)
  address      = forms.CharField(label="주소", max_length=100)
  class Meta(UserCreationForm.Meta):
    fields = UserCreationForm.Meta.fields + ('email',) # fields는 튜플이나 리스트로 넣어야 함 

  def save(self, commit=True):
    user = super().save()
    Profile = Profile(user=user,
                      phone_number = self.cleaned_data.get("phone_number"),
                      address      = self.cleaned_data.get("address"))
    Profile.save()
    return user