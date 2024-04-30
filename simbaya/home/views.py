from django.shortcuts import render,reverse,redirect
from vente.models import sell
from production.models import production
from depenses.models import spend
from matiere.models import Matiere
from django.utils import timezone
from django.db.models import Sum, Avg
from django.db.models.functions import TruncDay
from django.shortcuts import render
import json
from django.contrib.auth.decorators import login_required


@login_required(login_url='/admin/login')
def ventes_mois_en_cours(request):
    today = timezone.now()
    mois_en_cours = today.month
    annee_en_cours = today.year

    # Get vehicle sales data
    ventes_mois_en_cours = sell.objects.filter(
        date__month=mois_en_cours,
        date__year=annee_en_cours
    ).values('Vehicule').annotate(total_ventes=Sum('vendu'))
    vehicle_sales_data = json.dumps(list(ventes_mois_en_cours))

    # Get profitability data with date formatted
    rentabilite = production.objects.filter(
        date__month=mois_en_cours,
        date__year=annee_en_cours
    ).annotate(day=TruncDay('date')).values('day').annotate(renta=Avg('rentabilité'))
    rentabilite_data = [{'date': item['day'].strftime('%Y-%m-%d'), 'renta': item['renta']} for item in rentabilite]
    profitability_data = json.dumps(rentabilite_data)

    # Calculate the average profitability
    average_profitability = production.objects.filter(
        date__month=mois_en_cours,
        date__year=annee_en_cours
    ).aggregate(avg_rentabilite=Avg('rentabilité'))['avg_rentabilite'] or 0

    # Other data processing...
    vente = sell.objects.filter(
        date__month=mois_en_cours,
        date__year=annee_en_cours
    ).aggregate(vente=Sum('Somme_gnf'))['vente'] or 0
    depense = spend.objects.filter(
        date__month=mois_en_cours,
        date__year=annee_en_cours
    ).aggregate(depensé=Sum('Somme_gnf'))['depensé'] or 0

    # Quantity at the factory for the current day
    factory_quantity_today = production.objects.filter(date=today.date()).first()
    factory_quantity_today_value = factory_quantity_today.usine if factory_quantity_today else 0

    # Get latest stock information
    if Matiere.objects.all().last() is not None:
        stock_e = Matiere.objects.all().last().stock_emballage or 0
        stock_r = Matiere.objects.all().last().stock_rouleaux or 0
    else:
        stock_e = 0
        stock_r = 0

    context = {
        'vehicle_sales_data': vehicle_sales_data,
        'profitability_data': profitability_data,
        'average_profitability': average_profitability,
        'vente': vente,
        'depense': depense,
        'rapport': vente - depense,
        'stock_r': stock_r,
        'stock_e': stock_e,
        'factory_quantity_today': factory_quantity_today_value
    }

    return render(request, 'dashboard/index.html', context)





@login_required(login_url='/admin/login')

def rap(request):
    # Pour ce mois
    recapitulatif = sell.objects.values('date__month', 'date__year').annotate(total_vente=Sum('Somme_gnf')).order_by('-date__year', '-date__month')
    recap_depenses = spend.objects.values('date__month', 'date__year').annotate(total_depense=Sum('Somme_gnf')).order_by('-date__year', '-date__month')

    # Liste pour les résultats formatés
    resultats_formatte = []

    for vente in recapitulatif:
        mois = vente['date__month']
        annee = vente['date__year']
        montant_vente = vente['total_vente']

        # Trouver la dépense correspondante
        depense = next((dep for dep in recap_depenses if dep['date__month'] == mois and dep['date__year'] == annee), None)
        montant_depense = depense['total_depense'] if depense else 0

        difference = montant_vente - montant_depense

        resultats_formatte.append({
            'mois_annee': f"{mois}-{annee}",
            'mois': mois,
            'annee': annee,
            'difference': difference
        })

    context = {'resultats': resultats_formatte}
    return render(request, 'home/rapport.html', context)




@login_required(login_url='/admin/login')

def details(request, pk):
    # Séparer 'pk' en mois et année
    mois, annee = map(int, pk.split('-'))  # Convertit chaque partie en entier

    # Filtrer les ventes et dépenses par mois et année
    mois_vente = sell.objects.filter(date__month=mois, date__year=annee)
    mois_depense = spend.objects.filter(date__month=mois, date__year=annee)

    # Calculer le récapitulatif des ventes et dépenses
    recapitulatif_vente = mois_vente.values('date').annotate(total_vente=Sum('Somme_gnf')).order_by('date')
    recapitulatif_depense = mois_depense.values('date').annotate(total_depense=Sum('Somme_gnf')).order_by('date')

    somme_vente = recapitulatif_vente.aggregate(total_vente_mois=Sum('total_vente'))['total_vente_mois'] or 0
    somme_depense = recapitulatif_depense.aggregate(total_depense_mois=Sum('total_depense'))['total_depense_mois'] or 0
    benefice = somme_vente - somme_depense

    context = {
        'vente': recapitulatif_vente,
        'depenses': recapitulatif_depense,
        'mois_vente': somme_vente,
        'mois_depense': somme_depense,
        'benef': benefice
    }

    return render(request, 'home/details.html', context)


@login_required(login_url='/admin/login')
def recherche(request):
    # Filtrer les ventes et les dépenses pour le mois donné
    mois_vente = sell.objects.all()  # You may need to adjust this query based on your needs
    mois_depense = spend.objects.all()  # Similarly, adjust this query

    # Vue pour effectuer une recherche parmi les ventes
    ventes_par_mois = mois_vente.values('date').annotate(total_vente=Sum('Somme_gnf')).order_by('date')
    depenses_par_mois = mois_depense.values('date').annotate(total_depense=Sum('Somme_gnf')).order_by('date')

    recherche_term = request.GET.get('q')

    if recherche_term:
        # Filtrer les ventes et les dépenses en fonction du terme de recherche

        ventes_par_vehicule= ventes_par_mois.filter(Vehicule_id=recherche_term)
        depenses_par_vehicule = depenses_par_mois.filter(actif_id=recherche_term)

        # Si des données sont trouvées après la recherche, rediriger vers la première date trouvée
        if ventes_par_mois.exists() and depenses_par_mois.exists():
            date_trouvee = ventes_par_vehicule.first()['date'].month
            url = reverse('details', kwargs={'pk': date_trouvee})
            return redirect(url)

    # Calculer les totaux des ventes et dépenses pour le mois
    recapitulatif_vente = ventes_par_vehicule.values('date').annotate(total_vente=Sum('Somme_gnf')).order_by('date')
    recapitulatif_depense = depenses_par_vehicule.values('date').annotate(total_depense=Sum('Somme_gnf')).order_by('date')
    
    somme_vente = recapitulatif_vente.aggregate(total_vente_mois=Sum('total_vente'))['total_vente_mois'] or 0
    somme_depense = recapitulatif_depense.aggregate(total_depense_mois=Sum('total_depense'))['total_depense_mois'] or 0
    benefice = somme_vente - somme_depense
    vehicule=request.GET.get('q')

    context = {'vente': recapitulatif_vente, 'depenses': recapitulatif_depense,
               'mois_vente': somme_vente, 'v':vehicule,'mois_depense': somme_depense, 'benef': benefice}
    
    return render(request, 'home/details.html', context)