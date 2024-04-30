# views.py
from django.shortcuts import render, redirect
from .forms import Matiers
from .models import Matiere
from django.db.models import Sum

def ajout(request):
    # Vue pour ajouter de nouvelles ventes
    form = Matiers()
    if request.method == 'POST':
        form = Matiers(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock')

    context = {'form': form}
    return render(request, 'production/stock.html', context)

def stock(request):
    # Vue pour afficher la liste des ventes pour une date spécifique
    data = Matiere.objects.all()
    context = {'data': data}
    return render(request, 'production/matiere.html', context)

def update(request, pk):
    # Vue pour mettre à jour une production spécifique
    produit = Matiere.objects.get(id=pk)
    form = Matiers(instance=produit)
    if request.method == 'POST':
        form = Matiers(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('list_stock')

    context = {'form': form}
    return render(request, 'production/stockup.html', context)

def remove(request, pk):
    # Vue pour supprimer une production spécifique
    data = Matiere.objects.get(id=pk)
    data.delete()
    return redirect('list_production')


    