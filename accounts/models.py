from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# UserData
class UserProfile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type   = models.CharField(max_length=32)
    status      = models.CharField(max_length=64, default='exist')
    bio         = models.CharField(max_length=64, default='just born')
    
def create_profile(sender,**kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])
post_save.connect(create_profile, sender=User)
# UserData-end