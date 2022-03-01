from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Answer(models.Model):
    value           = models.CharField(max_length=64, default="")
    is_correct      = models.BooleanField(default=False)



class Task(models.Model):
    class AnswerTypes(models.TextChoices):
        ONE = 'one'
        MULTY = 'multy'
        TEXT = 'text'
    
    name            = models.CharField(max_length=64, default="")
    condition       = models.CharField(max_length=1024, default="")
    type            = models.CharField(max_length=8, choices=AnswerTypes.choices, default=AnswerTypes.ONE,)
    answers         = models.ManyToManyField(Answer, related_name="answers", blank=True)
    is_answer_rnd   = models.BooleanField(default=False)

    def delete(self):
        self.answers.all().delete()
        super().delete()



class Module(models.Model):
    name            = models.CharField(max_length=64, default="")
    author          = models.ForeignKey(User, on_delete=models.CASCADE)
    description     = models.CharField(max_length=1024, default="")
    creation_date   = models.DateTimeField(default=timezone.now())
    # tasks
    tasks           = models.ManyToManyField(Task, related_name="tasks", blank=True)
    is_tasks_rnd    = models.BooleanField(default=False)
    # key
    id              = models.CharField(max_length=16, unique=True, primary_key=True)

    def delete(self):
        self.tasks.all().delete()
        super().delete()