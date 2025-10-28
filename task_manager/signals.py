from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Task


@receiver(pre_save, sender=Task)
def store_old_status(sender, instance, **kwargs):
    """Сохраняем старый статус перед сохранением"""
    if instance.pk:
        try:
            old = Task.objects.get(pk=instance.pk)
            instance._old_status = old.status
        except Task.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Task)
def send_task_status_notification(sender, instance, created, **kwargs):
    """Отправляем email при изменении статуса"""
    if created:
        return

    old_status = getattr(instance, '_old_status', None)
    new_status = instance.status

    if old_status != new_status:
        subject = f'Обновление статуса задачи: {instance.title}'
        message = f'Статус вашей задачи "{instance.title}" изменён на: {instance.get_status_display()}'
        recipient_email = instance.owner.email

        if recipient_email:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=False,
            )