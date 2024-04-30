# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import spender  # Assurez-vous d'utiliser le nom correct du formulaire
from .models import spend
from django.db.models import Sum

from PIL import Image

def depenses(request):
    # Vue pour ajouter de nouvelles ventes
    form = spender()  # Assurez-vous d'utiliser le nom correct du formulaire
    if request.method == 'POST':
        form = spender(request.POST)
        if form.is_valid():
            form.save()
            return redirect('depenses')

    context = {'form': form}
    return render(request, 'depenses/depenses.html', context)

def update_depenses(request, pk):
    # Vue pour mettre à jour une vente spécifique
    vendu = spend.objects.get(id=pk)
    form = spender(instance=vendu)
    if request.method == 'POST':
        form = spender(request.POST, instance=vendu)
        if form.is_valid():
            form.save()
            return redirect('depenses')

    context = {'form': form}
    return render(request, 'depenses/depenses.html', context)
def remove_depenses(request, pk):
    # Vue pour supprimer une vente spécifique
    data = spend.objects.get(id=pk)
    data.delete()
    return redirect('list_depense_day')

def recherche(request):
    # Vue pour effectuer une recherche parmi les ventes
    donnée = spend.objects.all()
    reshearch = request.GET.get('q')
    if reshearch:
        donnée = donnée.filter(date__icontains=reshearch)

    context = {'datap': donnée}
    return render(request, 'depenses/list.html', context)
def tableau_recapitulatif(request):
    # Vue pour afficher un tableau récapitulatif des ventes par jour
    recapitulatif = spend.objects.values('date').annotate(total_vente=Sum('Somme_gnf')).order_by('date')
    context = {'datap': recapitulatif}
    return render(request, 'depenses/day.html', context)
def list_depenses(request, pk):
    # Vue pour afficher la liste des ventes pour une date spécifique
    
    datau = spend.objects.filter(date=pk)
    data = spend.objects.filter(date=pk)
    datau = datau.first().date
    context = {'datap': data, 'datau': datau}
    return render(request, 'depenses/list.html', context)
def fichier(request):
   recapitulatif = spend.objects.values('date').annotate(total_vente=Sum('Somme_gnf')).order_by('date')
   context = {'datap': recapitulatif}
   return render(request, 'depenses/print.html', context)

