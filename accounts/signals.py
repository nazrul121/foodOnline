from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
   
    if created:
        UserProfile.objects.create(user=instance)
        print('Profile created when user is created')
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print('Profile update')
        except:
            # Create the userprofile if not exist
            UserProfile.objects.create(user=instance)
            print('User created without Profile creating. SO one profile is created')


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    pass
# post_save.connect(post_save_create_profile_receiver, sender=User)