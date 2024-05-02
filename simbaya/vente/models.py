from django.db import models
from decimal import Decimal

class voitures(models.Model):
    v = models.CharField(max_length=500, primary_key=True, default='aucun')
    prime = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))  # Prime rate for each vehicle

    def __str__(self):
        return self.v

class Prix(models.Model):
    prix = models.DecimalField(max_digits=10, decimal_places=2, primary_key=True)

    def __str__(self):
        return str(self.prix)

class sell(models.Model):
    Vehicule = models.ForeignKey(voitures, on_delete=models.PROTECT, null=True)
    vente = models.IntegerField(null=True)
    prime = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))
    sortie = models.IntegerField(blank=True, null=True)
    vendu = models.IntegerField(null=True)
    retourner = models.IntegerField(null=True)
    credit = models.IntegerField(blank=True, null=True, default=0)
    Somme_gnf = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    statut_credit = models.CharField(max_length=30, null=True, blank=True)
    date = models.DateField(null=True, blank=True, auto_now_add=True)

    def __str__(self):
        return f'Sale on {self.date}'

    def save(self, *args, **kwargs):
        self.prime = self.Vehicule.prime  # Use the prime from the associated vehicle

        self.sortie = self.vente
        last_price = Prix.objects.last().prix if Prix.objects.exists() else Decimal('0')
        self.Somme_gnf = (Decimal(self.vendu) * last_price) - (
                        self.prime * last_price * Decimal(self.vendu)) - Decimal(self.credit)

        if self.credit != 0:
            self.statut_credit = 'non payé'
        else:
            self.statut_credit = 'payé'

        if self.statut_credit == 'payé':
            self.credit = 0

        super(sell, self).save(*args, **kwargs)
