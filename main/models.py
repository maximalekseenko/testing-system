from django.db import models

class Task(models.Model): 
    name = models.CharField(max_length=64, default = "Задание")
    content = models.CharField(max_length=512, default = "")
    options = []
    answers = []