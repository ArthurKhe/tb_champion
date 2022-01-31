from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Event, Sport_type


@receiver(post_save, sender=Event)
def create_event_handler(sender, instance, created, **kwargs):
    if created:
        sport_id = instance.sport_type_id.id
        s_type = Sport_type.objects.get(pk=sport_id)
        s_type.count = Event.objects.filter(sport_type_id=sport_id).count()
        s_type.save()


@receiver(post_delete, sender=Event)
def delete_event_handler(sender, instance, **kwargs):
    sport_id = instance.sport_type_id.id
    s_type = Sport_type.objects.get(pk=sport_id)
    s_type.count = Event.objects.filter(sport_type_id=sport_id).count()
    s_type.save()
