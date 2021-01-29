from django.db import models

class test1(models.Model):
    val1 = models.IntegerField(default = 0)
    val2 = models.BooleanField(default = False)