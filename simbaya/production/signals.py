# production/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from vente.models import sell
from .models import production

@receiver(post_save, sender=sell)
def update_production_on_save(sender, instance, created, **kwargs):
    update_production(instance)

@receiver(post_delete, sender=sell)
def update_production_on_delete(sender, instance, **kwargs):
    update_production(instance)

def update_production(instance):
    date = instance.date
    somme_sorties = sell.objects.filter(date=date).aggregate(Sum('vendu'))['vendu__sum'] or 0
    retourner_sorties = sell.objects.filter(date=date).aggregate(Sum('retourner'))['retourner__sum'] or 0
    somme_sorties-=retourner_sorties



    production_obj, created = production.objects.get_or_create(date=date)
    production_obj.sortie = somme_sorties
    production_obj.save()
