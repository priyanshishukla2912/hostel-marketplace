from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    room_no = models.CharField(max_length=10)
    is_verified = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name