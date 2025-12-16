from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """Колдонуучунун толук профили"""
    USER_TYPE_CHOICES = [
        ('seeker', 'Жумуш издеген'),
        ('employer', 'Жумуш берүүчү'),
        ('both', 'Экөө тең'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='seeker')
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True, verbose_name='Жайгашкан жер')
    bio = models.TextField(blank=True, verbose_name='Өзү жөнүндө')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профилдер'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Жаңы колдонуучу катталганда автоматтык түрдө профиль түзүү"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Колдонуучу сакталганда профилди да сактоо"""
    instance.profile.save()
