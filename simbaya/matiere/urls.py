from django.urls import path
from . import views

urlpatterns = [
    # Page principale pour l'ajout de productin
    path('', views.ajout, name='stock'),

    # Liste des productions pour une date spécifique
    path('liste_stocks/', views.stock, name='list_stock'),

    # Modification d'une production spécifique
    path('modif_stock/<str:pk>/', views.update, name='update_stock'),

    # Suppression d'une production spécifique
    path('suprimer_stock/<str:pk>/', views.remove, name='remove_stock'),

    # Vue de recherche pour filtrer les productions
   
    # Générer un fichier Excel pour les ventes d'une date spécifique

]
