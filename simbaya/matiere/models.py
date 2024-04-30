from django.db import models
from vente.models import sell
from django.db.models import Sum,F
from production.models import production

# Define choices outside the class


class Matiere(models.Model):
   
    rouleaux = models.IntegerField(null=True)
    
    emballage= models.IntegerField(null=True)
    stock_rouleaux = models.IntegerField(blank=True, null=True)
    stock_emballage = models.IntegerField(blank=True, null=True)
    date = models.DateField(null=True, blank=True, auto_now_add=True)

    def save(self, *args, **kwargs):
        # Récupérer l'objet Matiere actuel
        stock_e = Matiere.objects.all().aggregate(Sum('emballage'))['emballage__sum'] or 0
        stock_r = Matiere.objects.all().aggregate(Sum('rouleaux'))['rouleaux__sum'] or 0

        # Récupérer les totaux de la production
        emballage = production.objects.aggregate(Sum('nombre_emballage'))['nombre_emballage__sum'] or 0
        rou = production.objects.aggregate(Sum('nombre_roulaux'))['nombre_roulaux__sum'] or 0

        # Mettre à jour les stocks en utilisant F() pour éviter les problèmes de concurrence
        self.stock_rouleaux = self.rouleaux+(stock_r - rou)
        self.stock_emballage=self.emballage+(stock_e - emballage)

        # Appeler la méthode save de la classe parente pour enregistrer les modifications
        super(Matiere, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.date)
        
