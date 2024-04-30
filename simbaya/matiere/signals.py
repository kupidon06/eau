# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F, Sum
from .models import Matiere
from production.models import production
from datetime import datetime

@receiver(post_save, sender=production)
def mettre_a_jour_stock(sender, instance, created, **kwargs):
    # Récupérer les totaux actuels de rouleaux et emballage
    stock_r = Matiere.objects.aggregate(Sum('rouleaux'))['rouleaux__sum'] or 0
    stock_e = Matiere.objects.aggregate(Sum('emballage'))['emballage__sum'] or 0

    # Récupérer les totaux de la production
    emballage = production.objects.aggregate(Sum('nombre_emballage'))['nombre_emballage__sum'] or 0
    rou = production.objects.aggregate(Sum('nombre_roulaux'))['nombre_roulaux__sum'] or 0
    date=Matiere.objects.all().last().date

    # Mise à jour des stocks en utilisant F() pour éviter les problèmes de concurrence
    Matiere.objects.filter(date=date).update(
        stock_rouleaux=stock_r - rou,
        stock_emballage= stock_e - emballage
    )
    # Si l'instance est créée, créer un nouvel objet Matiere si nécessaire
    