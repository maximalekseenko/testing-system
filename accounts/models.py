from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# UserData
class UserProfile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type   = models.CharField(max_length=20, default='guest')
    desription  = models.CharField(max_length=100, default="no description... yet.")

    
def create_profile(sender,**kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])
post_save.connect(create_profile, sender=User)
# UserData-end