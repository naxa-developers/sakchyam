from django.db import models
from django.contrib.auth.models import User, Group, Permission

# Create your models here.


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_role')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='user_role')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='user_role')

    def __str__(self):
        return self.user.username

