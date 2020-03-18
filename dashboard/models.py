from django.db import models
from django.contrib.auth.models import User, Group, Permission

# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_role')
    full_name = models.CharField(max_length=500, null=True, blank=True)
    email = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.full_name

