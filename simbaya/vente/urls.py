from django.urls import path
from . import views

urlpatterns = [
    # Page principale pour l'ajout de ventes
    path('', views.ventes, name='vente'),

    # Liste des ventes pour une date spécifique
    path('liste_vente/<str:pk>/', views.list_vente, name='list_vente'),

    # Modification d'une vente spécifique
    path('modif_ventes/<str:pk>/', views.update, name='update_vente'),

    # Suppression d'une vente spécifique
    path('suprimer/<str:pk>/', views.remove, name='remove_vente'),

    # Vue de recherche pour filtrer les ventes
    path('ma_vue/', views.recherche, name='ma_vue'),

    # Tableau récapitulatif des ventes par jour
    path('liste_jours/', views.tableau_recapitulatif, name='list_jours'),

    # Générer un fichier Excel pour les ventes d'une date spécifique
    path('fichier/<str:pk>/', views.fichier, name='generer_fichier_excel'),

    # Page de gestion des crédits
    path('credit/', views.credit, name='credit'),

    # Liste des ventes à crédit pour un véhicule spécifique
    path('liste_credit/<str:pk>/', views.list_credit, name='list_credit'),

]
