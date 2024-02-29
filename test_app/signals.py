from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import UserResponse


@receiver(pre_save,sender=UserResponse)
def my_handler(sender,instance,created,**kwargs):
    if not instance.status:
        mail = instance.author.email
        send_mail(
            'subject here',
            'Here is the message.',
            'host@mail.ru',
            [mail],
            fail_silently=False,
        )
        return
    mail = instance.article.author.email
    send_mail(
        'subject here',
        'Here is the message.',
        'host@mail.ru',
        [mail],
        fail_silently=False,

    )


