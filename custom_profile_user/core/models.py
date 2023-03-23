from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from phone_field import PhoneField # облегчает добавления с полей с номерами телефонов

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    birthday = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=150)
    photo = models.ImageField(upload_to='profile_pics')
    bio = models.TextField()

    # дескриптор str с возможностью возврата username
    def __str__(self):
        return self.user.username

# сигнал post_save - накладываетсы на моедль пользователя
# когда у нас создается новый пользователь он приходит в эту функцию и обрабатывается
@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    # если пользователь сосздануспешно в таком случае
    # мы сосздаем для него новый instance профайл
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
