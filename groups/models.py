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
    members         = models.ManyToManyField(User, related_name="members", blank=True)
    members_pending = models.ManyToManyField(User, related_name="members_pending", blank=True)
    
