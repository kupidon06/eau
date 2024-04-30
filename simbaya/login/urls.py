from django.urls import path
from . import home

urlpatterns = [
    # Page principale pour l'ajout de productin
    path('login/', home.login_view, name='login'),

    # Liste des productions pour une date spécifique
    path('logout/', home.logout_view, name='logout'),

]
