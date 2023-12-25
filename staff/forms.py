from django import forms
from customer.models import Category

class Form_Category(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__" #["image","description","name_category"]