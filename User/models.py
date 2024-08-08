from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, fname, lname, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), fname=fname, lname=lname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fname, lname, password=None):
        user = self.create_user(email, fname, lname, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    token = models.CharField(max_length=36, blank=True, null=True)
    preference = models.JSONField(default=list)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'lname']

    def __str__(self):
        return self.email
