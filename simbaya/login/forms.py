from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Téléphone", "class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe", "class": "form-control"}))
