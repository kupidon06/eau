# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from .models import production
from vente.models import sell

@receiver(post_save, sender=sell)
def mettre_a_jour_production(sender, instance, created, **kwargs):
    # If the instance is created, update the production model
    if created:
        date = instance.date
        somme_sorties = sell.objects.filter(date=date).aggregate(Sum('sortie'))['sortie__sum'] or 0

        # Get or create the production object for the given date
        production_obj, _ = production.objects.get_or_create(date=date)

        # Update the production object with the sum of outputs
       
        production_obj.sortie = somme_sorties

        # Save the updated production object
        production_obj.save()

    else:  # If the instance is not created, handle the update logic
        date = instance.date
        somme_sorties = sell.objects.filter(date=date).aggregate(Sum('sortie'))['sortie__sum'] or 0

        # Try to get the existing production object for the given date
        try:
            production_obj = production.objects.get(date=date)
        except production.DoesNotExist:
            # If the production object does not exist, create it
            production_obj = production.objects.create(
                date=date,
                initiale=0,
                nombre_emballage=0,
                nombre_roulaux=0,
                poids=1,
                produit=0,
                sortie=somme_sorties
            )

        # Update the production object with the sum of outputs
        production_obj.sortie = somme_sorties

        # Save the updated production object
        production_obj.save()
