from django import forms
from customer.models import Category

class Form_Category(forms.ModelForm):
    name = forms.CharField(label='نام دسته', widget=forms.TextInput(attrs={'placeholder': 'نام دسته را وارد کنید'}))
    description = forms.CharField(label='توضیحات', widget=forms.Textarea(attrs={'placeholder': 'توضیحات را وارد کنید'}))
    image = forms.ImageField(label='تصویر', widget=forms.FileInput(attrs={'placeholder': 'تصویر را انتخاب کنید'}))

    class Meta:
        model = Category
        fields = ["name","description", "image"]

    