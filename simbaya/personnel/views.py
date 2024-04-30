
from django.shortcuts import render,redirect
from .forms import personnels
from .models import pers
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/admin/login')
def personnel(request):
    form=personnels()
    
    if request.method=='POST':
        form=personnels(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_personnel')
    
   
    
    context={'form':form,}

    return render (request,'personnel/personnel.html',context)


@login_required(login_url='/admin/login')
def fichier(request, pk):
    perso = pers.objects.get(id=pk)
  
    data = pers.objects.filter(id=pk)
    nom=data.first().Nom
    prenom=data.first().Prenom
    num=data.first().Telephone
    poste=data.first().poste
    salaire=data.first().salaire
    


    #-------------------------------------------------------------------------------------------
    
    #-----------------------------------------------------------------------------------------------------
   

   
    context = {'nom':nom,'prenom':prenom,'num':num,'poste':poste,'salaire':salaire}
    return render(request, 'personnel/print.html', context)
@login_required(login_url='/admin/login')
def list_personnel(request):
    data=pers.objects.all()
    context={'datap':data}

    return render (request,'personnel/list.html',context)

@login_required(login_url='/admin/login')
def update(request,pk):
    perso = pers.objects.get(id=pk)
    form=personnels(instance=perso)
    if request.method=='POST':
        form=personnels(request.POST,instance=perso)
        if form.is_valid:
            form.save(request)
            return redirect('liste_personnel')
    context={'form':form}
    
   
    return render(request,'personnel/personnel.html',context)

@login_required(login_url='/admin/login')
def remove(request,pk) :
    data=pers.objects.get(id=pk)
    data.delete()
    return redirect('liste_personnel')

@login_required(login_url='/admin/login')

def recherche(request):
    # Récupérer tous les éléments sans filtre initial
    donnée = pers.objects.all()

    # Code de recherche ici si un terme de recherche est fourni
    reshearch= request.GET.get('q')
    if reshearch:
        # Filtrer les éléments en fonction du terme de recherche
        donnée = donnée.filter(Nom__icontains=reshearch)

    context = {'datap': donnée}
    return render(request, 'personnel/list.html', context)
# views.py

@login_required(login_url='/admin/login')
def generer_fichier_excel(request, pk):
        return