from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import UserManagers
from django.utils import timezone

# Create your models here.


class User(AbstractBaseUser,PermissionsMixin):
    phone_number = models.CharField(max_length=11,unique=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['full_name','email']

    objects = UserManagers()

    def __str__(self):  
        return str(self.phone_number)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_lable):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

class Admin(models.Model):
    user_id = models.OneToOneField('User' , on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    permission_level_id = models.OneToOneField('Permission_level' , on_delete=models.CASCADE)

    def __str__(self):
        return f"Admin: {self.user_id.full_name} - {self.city}"

class Permission_level(models.Model):
    level_name = models.SmallIntegerField(default=3)
    can_manage_all = models.BooleanField(default=False)
    can_approve_driver = models.BooleanField(default=False)
    can_manage_travel = models.BooleanField(default=True)


    def __str__(self):
        return str(self.level_name)

    def save(self, *args,**kwargs):
        values = [self.can_manage_all,self.can_approve_driver,self.can_manage_travel]
        if self.can_manage_all :
            self.can_approve_driver = True
            self.can_manage_travel = True
            self.level_name = 1
        elif self.can_approve_driver:
            self.can_manage_travel = True
            self.level_name = 2
        else:
            self.level_name = 3
        super().save(*args, **kwargs)


class Driver_Documents(models.Model):
    user_id = models.OneToOneField('User',on_delete=models.CASCADE)
    license_number = models.CharField(max_length=255)
    license_expiry = models.DateField()
    health_card_number = models.CharField(max_length=255)
    health_card_expiry = models.DateField()
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateField(blank=True,null=True)

    def __str__(self):
        return f"Driver Documents for {self.user_id.full_name}"

    def save(self,*args,**kwargs):
        if self.is_approved:
            self.approved_at = timezone.now()
        super().save(*args,**kwargs)

class Vehicle(models.Model):
    model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=8,unique=True)
    color = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    seats = models.SmallIntegerField(default=1)
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.model} in {self.location}"

