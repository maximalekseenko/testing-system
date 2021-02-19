from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name            = models.CharField(max_length=64, default="Новый gruppa", blank=True)
    members         = models.ManyToManyField(User, blank=True)
