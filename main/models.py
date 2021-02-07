from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             blank=True, null=True) 
    name = models.CharField(max_length=64, default = "Задание")
    content = models.CharField(max_length=512, default = "")
    options = []
    answers = []