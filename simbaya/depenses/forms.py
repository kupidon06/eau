from django.forms import ModelForm
from .models import spend
from django import forms

class spender(ModelForm):
    class Meta():
        model=spend

        fields=['actif','detail','Somme_gnf']
        widgets = {
            'actif': forms.Select(attrs={'class': 'form-control'}),
            'detail': forms.TextInput(attrs={'class': 'form-control'}),
            'Somme_gnf': forms.TextInput(attrs={'class': 'form-control'}),
        }