from django.db import models
from django.contrib.auth.models import User


class Mark(models.Model):
    author          = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    comment         = models.CharField(max_length=32, default = "")
    mark            = models.CharField(max_length=16, default = "")


class Answer(models.Model):
    author          = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    content         = models.CharField(max_length=32, default = "")


class Task(models.Model):
    title           = models.CharField(max_length=64, default = "Имя")
    author          = models.ForeignKey(to=User, on_delete=models.CASCADE) 
    content         = models.CharField(max_length=512, default = "Условие")
    #answers
    correct_answer  = models.CharField(max_length=32, default = "-1")
    answer_type     = models.CharField(max_length=32, default = "option")
    options_answer  = models.ManyToManyField(Answer)
    marks           = models.ManyToManyField(Mark)
    #other
    creation_date   = models.DateTimeField(auto_now_add=True)


class Module(models.Model):
    name            = models.CharField(max_length=64, default="Новый модуль")
    author          = models.ForeignKey(to=User, related_name="author_id", on_delete=models.CASCADE)
    tasks           = models.ManyToManyField(to=Task, related_name="tasks_id")
    assigned_to     = models.ManyToManyField(to=User, related_name="assigned_to_id")
    
    
