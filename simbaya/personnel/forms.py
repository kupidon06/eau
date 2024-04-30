from django.forms import ModelForm
from .models import pers


class personnels(ModelForm):
    class Meta():
        model=pers
        fields='__all__'