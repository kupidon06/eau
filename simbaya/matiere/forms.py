from django.forms import ModelForm
from .models import Matiere

class Matiers(ModelForm):
    class Meta():
        model=Matiere
        fields=['rouleaux','emballage']

