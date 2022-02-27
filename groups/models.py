from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
#app
from tasks.models import Module

    
class UserMark(models.Model):
    user            = models.ManyToManyField(User, related_name="user")
    mark            = models.IntegerField()
    creation_date   = models.DateTimeField(default=timezone.now())
    is_before_deadline = models.BooleanField(default=True)


class ModuleData(models.Model):
    module          = models.ForeignKey(Module, related_name="module", on_delete=models.CASCADE, blank=True)
    user_marks      = models.ManyToManyField(UserMark, related_name="user_marks", blank=True)
    deadline        = models.DateTimeField(default=timezone.now())


class Group(models.Model):
    author          = models.ForeignKey(User, related_name="group_author", on_delete=models.CASCADE, null=True)
    name            = models.CharField(max_length=32, default="")
    description     = models.CharField(max_length=1024, default="")
    creation_date   = models.DateTimeField(default=timezone.now())
    id              = models.CharField(max_length=16, unique=True, primary_key = True)
    # moduls
    moduls_data     = models.ManyToManyField(ModuleData, related_name="moduls_data", blank=True)
    # memers
    members         = models.ManyToManyField(User, related_name="members", blank=True)
    members_pending = models.ManyToManyField(User, related_name="member_pending", blank=True)