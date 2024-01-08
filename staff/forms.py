from django import forms

from django import forms
import django
django.setup()
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from customer.models import Category


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)
    
    
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name' , 'roll')
    
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] and cd["password2"] and cd["password1"] != cd['password2']:
            raise ValidationError("passwords dont match")
        return cd["password2"]
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="you can change password using <a href=\"../password/\">this form.</a>")
    
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'password', 'last_login' , 'roll')
        
        
class UserRegister(forms.Form):
    roll = forms.CharField(max_length = 11)
    email = forms.EmailField()
    full_name = forms.CharField(max_length = 50)
    phone = forms.CharField(max_length = 50)
    password = forms.CharField(max_length=10 , widget=forms.PasswordInput)
    
class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()
    
class LoginForm(forms.Form):
    phone = forms.CharField(max_length=11)
    password = forms.CharField(max_length=10,widget=forms.PasswordInput)

# class Form_Category(forms.ModelForm):
#     name = forms.CharField(label='نام دسته', widget=forms.TextInput(attrs={'placeholder': 'نام دسته را وارد کنید'}))
#     description = forms.CharField(label='توضیحات', widget=forms.Textarea(attrs={'placeholder': 'توضیحات را وارد کنید'}))
#     image = forms.ImageField(label='تصویر', widget=forms.FileInput(attrs={'placeholder': 'تصویر را انتخاب کنید'}))

#     class Meta:
#         model = Category
#         fields = ["name","description", "image"]


