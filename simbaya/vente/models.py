from django.db import models
from decimal import Decimal
from django.db.models import Sum
from production.models import production



class voitures(models.Model):
    v = models.CharField(max_length=500, primary_key=True, default='aucun')

    def __str__(self):
        return self.v


class Prix(models.Model):
    prix = models.DecimalField(max_digits=10, decimal_places=2, primary_key=True)  # Changed to DecimalField

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

    PRIME_CITROEN = Decimal('0.1')
    PRIME_DEFAULT = Decimal('0.0')

    def __str__(self):
        return f'Sale on {self.date}'

    def save(self, *args, **kwargs):
        if not self.id :
            produc = production.objects.filter(date=self.date).first()
            if produc is None:
                raise ValueError("It's impossible to register without production on the same day.")

            total_sold_today = sell.objects.filter(date=self.date).aggregate(Sum('vendu'))['vendu__sum'] or 0
            if self.id:
                if total_sold_today + self.vendu > produc.sortie:
                    raise ValueError("Selling these units exceeds the stock available.")

            if self.Vehicule.v in ['Toyota', 'Ford', 'Citroen Jumper']:  # Assuming v contains the brand name
                self.prime = self.PRIME_CITROEN
            else:
                self.prime = self.PRIME_DEFAULT

            self.sortie = self.vente
            last_price = Prix.objects.last().prix if Prix.objects.exists() else Decimal('0')  # Ensure there's a fallback
            self.somme_gnf = (Decimal(self.vendu) * last_price) - (self.prime * last_price * Decimal(self.vendu)) - Decimal(
                self.credit)

            if self.credit != 0:
                self.statut_credit = 'non payé'
            else:
                self.statut_credit = 'payé'

            if self.statut_credit == 'payé':
                self.credit = 0

            super(sell, self).save(*args, **kwargs)





