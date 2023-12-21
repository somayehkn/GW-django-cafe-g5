from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import UserManager,AbstractBaseUser,PermissionsMixin


# Create your models here.
class CustumerUserManager(UserManager):
    def _create_user(self , phone ,password,**extra_fields):
        if not phone:
            raise ValueError('User must have a phone')
        
        user = self.model(phone = phone)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self,phone=None,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(phone,password,**extra_fields)
            
    def create_superuser(self,phone=None,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(phone,password,**extra_fields)
    
    
class User(AbstractBaseUser,PermissionsMixin):
    phone = models.CharField(max_length=12 ,default='', blank=True, unique=True)
    name = models.CharField(max_length=100,blank=True)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    objects=CustumerUserManager()
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'
    
    def get_full_name(self):
        return self.name


class Staff(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20,null=True)
    phone_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    