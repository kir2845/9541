from django.db.models.signals import m2m_changed
from django.conf import settings
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from News_from_Ozersk.models import NewCategory
from Ozersk_News_Portal.settings import SITE_URL
from django.template.loader import render_to_string


def send_notifications(preview, pk, name, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject = name,
        body = '',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content,'text/html')
    msg.send()

@receiver(m2m_changed, sender=NewCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()
        subscribers = [s.email for s in subscribers]
        send_notifications(instance.preview(), instance.pk, instance.name, subscribers)