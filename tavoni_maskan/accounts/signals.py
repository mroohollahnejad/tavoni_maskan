from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Profile

@receiver(user_logged_in)
def increment_login_count(sender, request, user, **kwargs):
    profile, created = Profile.objects.get_or_create(user=user)
    profile.login_count += 1
    profile.save()
