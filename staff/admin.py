from django.contrib import admin
from .models import User, staff_user , OTPCODE
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
# Register your models here.
@admin.register(OTPCODE)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number' , 'code' , 'created')
    
    
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    
    list_display = ('email', 'phone_number','roll','is_admin')
    list_filter = ('is_admin',)
    
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'full_name','roll' ,'password')}),
        ('Permissions', {'fields': ('is_active', 'is_admin','last_login','groups','user_permissions')}),
    )

    add_fieldsets = (
        (None, {'fields':('phone_number', 'email', 'full_name','roll','password1', 'password2')}),
    )
    search_fields = ('email', 'full_name')
    ordering = ('full_name',)
    filter_horizontal = ('groups','user_permissions')
    
    def __str__(self) -> str:
        return super().__str__()
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(staff_user)