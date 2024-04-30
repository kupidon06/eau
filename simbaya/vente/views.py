# views.py
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse
from django.db.models import Sum
from django.contrib import messages

from .forms import seller, PaymentForm  # Ensure you have the correct form names
from .models import sell
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

    context = {
        'sales_data': sales,
        'spends_data': spends,
        'date': pk,
        'total_sales': sales.aggregate(Sum('Somme_gnf'))['Somme_gnf__sum'] or 0,
        'total_spends': spends.aggregate(Sum('Somme_gnf'))['Somme_gnf__sum'] or 0,
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


