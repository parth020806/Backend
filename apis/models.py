from django.db import models


from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Create your models here.

class UserInfoModel(models.Model):
    username = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=20, null=True)
    aadhar = models.CharField(max_length=20, null=True)
    address = models.TextField(null=True)
    parent_referral_code = models.CharField(max_length=100, null=True)
    user_referral_code = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    signup_timestamp = models.DateTimeField(default=timezone.now)
    login_timestamp = models.DateTimeField(null=True, blank=True)
    def set_login_timestamp(self):
        self.login_timestamp = timezone.now()
        self.save()
    login_token = models.CharField(max_length=100, null=True, blank=True)
    secret_question = models.CharField(max_length=100, null=True)
    answer = models.CharField(max_length=100, null=True)

class ContactModel(models.Model):
    email = models.CharField(max_length=100, null=True)
    message = models.TextField(max_length=100, null=True)

    def __str__(self):
        return self.email

