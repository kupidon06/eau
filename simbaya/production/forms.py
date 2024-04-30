from django.forms import ModelForm
from .models import production

class productions(ModelForm):
    class Meta():
        model=production
        fields=['initiale','nombre_roulaux','nombre_emballage','poids','produit']


