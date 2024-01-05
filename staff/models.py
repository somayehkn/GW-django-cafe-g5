from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import UserManager

# custom user
class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=255)
    roll = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email", "full_name","roll"]
    
    objects = UserManager()
    
    def __str__(self) -> str:
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
class staff_user(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=11)


class Staff(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20,null=True)
    phone_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class OTPCODE(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.phone_number} - {self.code} - {self.created}"

