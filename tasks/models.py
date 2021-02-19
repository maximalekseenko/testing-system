from django.db import models
from django.contrib.auth.models import User
#app
from main.models import Group


class Mark(models.Model):
    author              = models.ForeignKey(User, on_delete=models.CASCADE)
    comment             = models.CharField(max_length=32, default = "")
    mark                = models.IntegerField(default = 0)


class Answer(models.Model):
    content             = models.CharField(max_length=32, default = "")


class Task(models.Model):
    title               = models.CharField(max_length=64, default = "Имя")
    content             = models.CharField(max_length=512, default = "Условие")
    #answer
    correct_answer      = models.CharField(max_length=32, default = "-1")
    answer_type         = models.CharField(max_length=32, default = "input")
    options_answer      = models.ManyToManyField(Answer)
    ANSWER_TYPE_CHOICES = [('CH', 'choise'), ('IN', 'input'), ('MC', 'm_choise')]
    answer_type         = models.CharField(max_length=2, choices=ANSWER_TYPE_CHOICES, default='IN')


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
    
