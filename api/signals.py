from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

from .models import Vote, Content


@receiver(post_save, sender=Vote)
def update_average_vote(sender, instance, **kwargs):
    content = instance.content
    new_average = content.votes.aggregate(Avg("score"))["score__avg"]
    Content.objects.filter(id=content.id).update(average_vote=new_average)
