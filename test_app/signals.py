from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Article


@receiver(post_save, sender=Article)
def update_user_on_article_save(sender, instance, created, **kwargs):
    if created:
        emails = Article.objects.filter(
            category=instance.category
        ).values_list('email', flat=True)

        subject = f'Новое объявление в категории {instance.category}'

        text_content = (
            f'Объявление: {instance.title}\n'
            f'Ссылка на источник : http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'Объявление: {instance.title}<br>'
            f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
            f'Ссылка на источник </a>'
        )
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()



