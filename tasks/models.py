from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Task(models.Model):
    name          = models.CharField(max_length=64, default = "Имя")
    content       = models.CharField(max_length=512, default = "Условие")
    #answer
    answer        = models.IntegerField(default = 0)
    options       = models.CharField(max_length=255, default = "")


class Module(models.Model):
    name          = models.CharField(max_length=64, default="Новый модуль")
    author        = models.ForeignKey(User, on_delete=models.CASCADE)
    description   = models.CharField(max_length=1024, default="AAAA")
    creation_date = models.DateTimeField(default=timezone.now())
    #vars
    tasks         = models.JSONField(default={'-1':{'type':'', 'options':[], 'answers':[]}})
    #key
    id            = models.CharField(max_length=16, unique=True, primary_key = True)
    
    #to be ahihilated
    def is_assigned(self, user:User):
        groups = self.assigned_to.filter(members__id=user.id)
        return len(groups)>0
    
