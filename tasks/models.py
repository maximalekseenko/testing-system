from django.db import models
from django.contrib.auth.models import User
#app
from main.models import Group


class Mark(models.Model):
    author              = models.ForeignKey(User, on_delete=models.CASCADE)
    comment             = models.CharField(max_length=32, default = "")
    mark                = models.IntegerField(default = 0)


class Task(models.Model):
    name                = models.CharField(max_length=64, default = "Имя")
    content             = models.CharField(max_length=512, default = "Условие")
    #answer
    answer              = models.IntegerField(default = 0)
    options             = models.CharField(max_length=255, default = "")


class Module(models.Model):
    name                = models.CharField(max_length=64, default="Новый модуль")
    author              = models.ForeignKey(User, on_delete=models.CASCADE)
    #lists
    marks               = models.ManyToManyField(Mark, blank=True)
    tasks               = models.ManyToManyField(Task, blank=True)
    assigned_to         = models.ManyToManyField(Group, blank=True)
    #data
    creation_date       = models.DateTimeField(auto_now_add=True)
    #bool
    is_active           = models.BooleanField(default=True)
    is_public           = models.BooleanField(default=False)
    
    def is_assigned(self, user:User):
        groups = self.assigned_to.filter(members__id=user.id)
        return len(groups)>0
    
