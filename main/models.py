from django.db import models
from django.contrib.auth.models import User


class UserNote(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    note          = models.CharField(max_length=32, default = "")
