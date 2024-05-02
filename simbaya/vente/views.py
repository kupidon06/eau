# views.py
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse
from django.db.models import Sum
from django.contrib import messages
from django.utils.timezone import make_aware
from datetime import datetime
from django.db.models.functions import TruncMonth
from datetime import timedelta
import calendar


from .forms import seller, PaymentForm,car,price  # Ensure you have the correct form names
from .models import sell,voitures,Prix
from depenses.models import spend
from production.models import production
from django.contrib.auth.decorators import login_required

@login_required(login_url='/admin/login')
def ventes(request):
    form = seller()
    if request.method == 'POST':
        form = seller(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vente')
    context = {'form': form}
    return render(request, 'vente/vente.html', context)


@login_required(login_url='/admin/login')
def fichier(request, pk):
    spends = spend.objects.filter(date=pk)
    sales = sell.objects.filter(date=pk)
    production_day = production.objects.filter(date=pk).first()

    # Calcul des totaux pour les ventes
    total_sales = sales.aggregate(Sum('Somme_gnf'))['Somme_gnf__sum'] or 0
    total_sold_units = sales.aggregate(Sum('vendu'))['vendu__sum'] or 0
    total_credit = sales.aggregate(Sum('credit'))['credit__sum'] or 0
    total_out = sales.aggregate(Sum('sortie'))['sortie__sum'] or 0
    total_retour = sales.aggregate(Sum('retourner'))['retourner__sum'] or 0

    # Calcul des totaux pour les dépenses
    total_spends = spends.aggregate(Sum('Somme_gnf'))['Somme_gnf__sum'] or 0

    # Calcul du revenu total (recette)
    total_revenue = total_sales - total_spends

    context = {
        'sales_data': sales,
        'spends_data': spends,
        'date': pk,
        'total_sales': total_sales,
        'total_sold_units': total_sold_units,
        'total_credit': total_credit,
        'total_out': total_out,
        'total_retour': total_retour,
        'total_spends': total_spends,
        'total_revenue': total_revenue,
        'production': production_day.produit if production_day else 0,
        'initial': production_day.initiale if production_day else 0,
        'usine': production_day.usine if production_day else 0,
    }

    return render(request, 'vente/print.html', context)


@login_required(login_url='/admin/login')
def list_vente(request, pk):
    sales = sell.objects.filter(date=pk)
    date = sales.first().date if sales.exists() else None
    return render(request, 'vente/list.html', {'sales': sales, 'date': date})


@login_required(login_url='/admin/login')
def update(request, pk):
    sale_instance = get_object_or_404(sell, id=pk)
    form = seller(instance=sale_instance)
    if request.method == 'POST':
        form = seller(request.POST, instance=sale_instance)
        if form.is_valid():
            form.save()
            return redirect('vente')
    return render(request, 'vente/update.html', {'form': form})


@login_required(login_url='/admin/login')
def remove(request, pk):
    sale = get_object_or_404(sell, id=pk)
    sale.delete()
    return redirect('list_jours')


@login_required(login_url='/admin/login')
def recherche(request):
    query = request.GET.get('q')
    if query:
        sales = sell.objects.filter(date__icontains=query)
        if sales.exists():
            return redirect('list_vente', pk=sales.first().date)
    else:
        sales = sell.objects.all()
    return render(request, 'vente/list.html', {'sales': sales})
@login_required(login_url='/admin/login')


def tableau_recapitulatif(request):
    summary = sell.objects.values('date').annotate(total_sales=Sum('Somme_gnf')).order_by('-date')
    return render(request, 'vente/day.html', {'summary': summary})




@login_required(login_url='/admin/login')
def list_credit(request, pk):
    credit_sales = sell.objects.filter(Vehicule=pk).order_by('date')  # Fetch credits sorted by date

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_amount = form.cleaned_data['payment_amount']
            remaining_amount = payment_amount

            for sale in credit_sales:
                if sale.credit > 0 and remaining_amount > 0:
                    if remaining_amount >= sale.credit:
                        remaining_amount -= sale.credit
                        sale.credit = 0
                    else:
                        sale.credit -= remaining_amount
                        remaining_amount = 0
                    sale.save()
                    if remaining_amount <= 0:
                        break

            if remaining_amount < payment_amount:  # Check if any payment was applied
                message = f'Credit has been updated, {payment_amount - remaining_amount} GNF used.'
                messages.success(request, message)
            else:
                messages.error(request, "No applicable credit to pay off.")

            return redirect('list_credit', pk=pk)  # Assuming you have a named URL to redirect back to the credit list
        else:
            messages.error(request, "Invalid payment amount.")
    else:
        form = PaymentForm(initial={'payment_amount': 0})

    return render(request, 'credit/list.html', {'form': form, 'credit_sales': credit_sales})


@login_required(login_url='/admin/login')
def credit(request):
    credit_summary = sell.objects.values('Vehicule').annotate(total_credit=Sum('credit'))
    return render(request, 'credit/credit.html', {'credit_summary': credit_summary})


@login_required(login_url='/admin/login')
def add_car(request):
    form = car()
    if request.method == 'POST':
        form = car(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vente')
    context = {'form': form}
    return render(request, 'voitures/add.html', context)


@login_required(login_url='/admin/login')
def update_car(request, pk):
    sale_instance = get_object_or_404(voitures, v=pk)
    form = car(instance=sale_instance)
    if request.method == 'POST':
        form = car(request.POST, instance=sale_instance)
        if form.is_valid():
            form.save()
            return redirect('vente')
    return render(request, 'voitures/add.html', {'form': form})

@login_required(login_url='/admin/login')
def remove_car(request, pk):
    sale = get_object_or_404(voitures, v=pk)
    sale.delete()
    return redirect('list_jours')


@login_required(login_url='/admin/login')
def list_car(request):
    summary = voitures.objects.all()
    return render(request, 'voitures/list.html', {'summary': summary})



@login_required(login_url='/admin/login')
def add_price(request):
    form = price()
    if request.method == 'POST':
        form = price(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vente')
    context = {'form': form}
    return render(request, 'price/add.html', context)


def tableau_mensuel_livraison(request):
    summary = sell.objects.filter(prime=0.0).annotate(
        month=TruncMonth('date')  # This truncates the date to the first day of the month
    ).values('month').annotate(
        total_sales=Sum('Somme_gnf')
    ).order_by('-month').exclude(Vehicule='Usine')

    # Format the month for clearer display
    for item in summary:
        item['month'] = item['month'].strftime('%Y-%m')  # Formats the month as Year-Month, e.g., 2023-05

    return render(request, 'livraison/month.html', {'summary': summary})


@login_required(login_url='/admin/login/')
def list_livraison(request, pk):
    french_months = ["janvier", "février", "mars", "avril", "mai", "juin",
                     "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
    # Assume pk is in the format "YYYY-MM"
    target_date = make_aware(datetime.strptime(pk, "%Y-%m"))
    month_start = target_date.replace(day=1)
    next_month_start = (month_start + timedelta(days=32)).replace(day=1)
    standard_date = month_start.strftime("%Y-%m")  # '2024-05' for example
    french_date = f"{french_months[month_start.month - 1]} {month_start.year}"  # 'mai 2024'

    sales = sell.objects.filter(
        date__gte=month_start,
        date__lt=next_month_start,
        prime=0.0
    ).exclude(Vehicule='Usine')
    date = month_start.strftime("%Y-%m")  # Formats the month as Year-Month, e.g., 2024-05

    return render(request, 'livraison/list.html', {'sales': sales, 'date': date,'french_date':french_date})

@login_required(login_url='/admin/login')
def print_livraison(request, pk):
    # French month names
    french_months = ["janvier", "février", "mars", "avril", "mai", "juin",
                     "juillet", "août", "septembre", "octobre", "novembre", "décembre"]

    # Assuming that pk is in the format "YYYY-MM"
    target_date = make_aware(datetime.strptime(pk, "%Y-%m"))
    month_start = target_date.replace(day=1)
    next_month_start = (month_start + timedelta(days=32)).replace(day=1)

    # Retrieving sales for the specified month, excluding those for "Vehicule Usine" if prime is 0.0
    sales = sell.objects.filter(
        date__gte=month_start,
        date__lt=next_month_start,
        prime=0.0
    ).exclude(Vehicule='Usine')  # Assuming 'vehicule' is the field name

    # Calculating totals
    total_sold_units = sum(sale.vendu for sale in sales if sale.vendu is not None)
    total_sum_gnf = sum(sale.Somme_gnf for sale in sales if sale.Somme_gnf is not None)
    total_credit_gnf = sum(sale.credit for sale in sales if sale.credit is not None)
    total_revenue = total_sum_gnf - total_credit_gnf  # Calculate net revenue if necessary

    # Formatting dates
    standard_date = month_start.strftime("%Y-%m")  # '2024-05' for example
    french_date = f"{french_months[month_start.month - 1]} {month_start.year}"  # 'mai 2024'

    # Preparing context for the template
    context = {
        'sales': sales,
        'standard_date': standard_date,
        'french_date': french_date,
        'total_sold_units': total_sold_units,
        'total_sum_gnf': total_sum_gnf,
        'total_credit_gnf': total_credit_gnf,
        'total_revenue': total_revenue
    }

    return render(request, 'livraison/print.html', context)