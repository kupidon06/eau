from django.db import models

from django.db.models import Sum


class production(models.Model):
    
    initiale=models.IntegerField(null=True)
    nombre_roulaux=models.IntegerField(null=True)
    nombre_emballage=models.IntegerField(null=True)
    poids=models.FloatField(null=True)
    produit=models.IntegerField(null=True)
    date=models.DateField(null=True,blank=True,auto_now_add=True,unique=True)
    sortie=models.IntegerField(blank=True,null=True)
   
    usine=models.IntegerField(blank=True,null=True)
   
    rentabilité=models.FloatField(blank=True,null=True)
   
    def __str__(self):
        return (f'Production du {self.date}')

    def save(self, *args, **kwargs):
        # Effectuer une opération lors de l'enregistrement du modèle
        

         self.rentabilité=self.produit/self.poids
         if self.sortie !=None:
            self.usine=self.initiale+self.produit-self.sortie
            
         else:
            self.usine=self.initiale+self.produit
           
         super(production,self).save(*args, **kwargs)
         
    
       

        # Appeler la méthode save() du modèle parent pour effectuer l'enregistrement réel
        

    





# Create your models here.
