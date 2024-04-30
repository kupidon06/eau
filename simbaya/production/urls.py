from django.urls import path
from . import views

urlpatterns = [
    # Page principale pour l'ajout de productin
    path('', views.produite, name='production'),

    # Liste des productions pour une date spécifique
    path('liste_productions/', views.list_production, name='list_production'),

    # Modification d'une production spécifique
    path('modif_production/<str:pk>/', views.update, name='update_production'),

    # Suppression d'une production spécifique
    path('suprimer_production/<str:pk>/', views.remove, name='remove_production'),

    # Vue de recherche pour filtrer les productions
    path('recherche_production/', views.recherche, name='recherche_production'),
    # Générer un fichier Excel pour les ventes d'une date spécifique

]
