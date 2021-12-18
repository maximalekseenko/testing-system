from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
#app
from tasks.models import Module


class Group(models.Model):
    author          = models.ForeignKey(User, related_name="author", on_delete=models.CASCADE, null=True)
    name            = models.CharField(max_length=32, default="")
    description     = models.CharField(max_length=1024, default="")
    creation_date   = models.DateTimeField(default=timezone.now())
    id              = models.CharField(max_length=16, unique=True, primary_key = True)
    # moduls
    moduls          = models.ManyToManyField(Module, related_name="moduls", blank=True)
    moduls_data     = models.JSONField(default={})
    # memers
    mem             = models.ManyToManyField(User, related_name="mem", blank=True)
    mem_adm         = models.ManyToManyField(User, related_name="mem_adm", blank=True)
    mem_req         = models.ManyToManyField(User, related_name="mem_req", blank=True)
    
