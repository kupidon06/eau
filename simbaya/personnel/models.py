from django.db import models

# Create your models here.
class pers(models.Model):
    situation={('Marié',('Marié')),('Celibataire',('celibataire'))}
    place={('Vendeur',('vendeur')),('Chauffeur',('chauffeur')),('Ouvrier',('Ouvrier'))}
    how={('Pourcentage',('Pourcentage')),('Salarié',('salarié'))}
    Nom=models.CharField(max_length=500,null=True)
    Prenom=models.CharField(max_length=500,null=True)
    Telephone=models.CharField(max_length=500,null=True)
    mail=models.CharField(max_length=500,null=True)
    situation=models.CharField(max_length=500,null=True,choices=situation)
    poste=models.CharField(max_length=200,null=True,choices=place)
    salaire=models.CharField(max_length=200,null=True)
    regime=models.CharField(max_length=200,null=True,choices=how)
    identité=models.ImageField(null=True,upload_to='.')
    def __str__(self):
        return self.Nom




   
