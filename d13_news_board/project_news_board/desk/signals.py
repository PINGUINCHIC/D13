from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Reply, UserProfile


@receiver(post_save, sender=Reply)
def reply_announcer(sender, instance, created, **kwargs):
    message_1 = f'Оставлен отклик на объявление "{instance.post.title}" пользователем {instance.author.name}'
    email_box_1 = instance.post.author.name.email

    print(message_1)
    print(f'Автор объявления {instance.post.author} получит письмо на почту {email_box_1}')
    if created:
        send_mail(subject='На Ваше объявление оставлен отклик',
                  message=message_1,
                  from_email=None,
                  recipient_list=[email_box_1, ])

    if instance.approved:
        message_2 = f'Отклик на объявление "{instance.post.title}" одобрен автором {instance.post.author.name}'
        email_box_2 = instance.author.name.email

        send_mail(subject='Ваш отклик одобрен автором',
                  message=message_2,
                  from_email=None,
                  recipient_list=[email_box_2, ])


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()
