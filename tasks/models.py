from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Module(models.Model):
    name            = models.CharField(max_length=64, default="Новый модуль")
    author          = models.ForeignKey(User, on_delete=models.CASCADE)
    description     = models.CharField(max_length=1024, default="AAAA")
    creation_date   = models.DateTimeField(default=timezone.now())
    # tasks
    tasks_data      = models.JSONField(default=dict)
    is_tasks_rnd    = models.BooleanField(default=False)
    # key
    id              = models.CharField(max_length=16, unique=True, primary_key=True)
    
