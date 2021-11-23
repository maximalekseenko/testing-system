from django.db import models
from django.contrib.auth.models import User
from tasks.models import Module


class Group(models.Model):
    name    = models.CharField(max_length=64, default="Новый gruppa", blank=True)
    author  = models.ForeignKey(User, related_name="author", on_delete=models.CASCADE, null=True)
    members = models.ManyToManyField(User, related_name="members", blank=True)
    moduls  = models.ManyToManyField(Module, related_name="moduls", blank=True)