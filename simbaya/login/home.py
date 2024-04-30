from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from .forms import LoginForm

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST" and form.is_valid():
        phone = form.cleaned_data.get("phone")
        password = form.cleaned_data.get("password")
        user = authenticate(request, phone=phone, password=password)

        if user is not None:

            login(request, user)
            return redirect("ventes_mois_en_cours")
        else:
            msg = 'Invalid credentials or account not activated.'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})

@login_required(login_url='/admin/login')
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('login')
