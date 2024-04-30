from django import forms
from .models import sell

class seller(forms.ModelForm):
    class Meta():
        model=sell
        fields=['Vehicule','vente','vendu','retourner','credit']
        widgets = {
            'Vehicule': forms.Select(attrs={'class': 'form-control'}),
        }



class PaymentForm(forms.Form):
    payment_amount = forms.DecimalField(decimal_places=2, max_digits=10, help_text="Enter the amount to be paid")
        
