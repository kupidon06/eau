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

    #les voitures
    path('car/', views.add_car, name='ajout de voiture'),

    path('update_car/<str:pk>/', views.update_car, name='modification de voiture'),

    path('remove_car/<str:pk>/', views.remove_car, name='suprimer de voiture'),

    path('liste_car/', views.list_car, name='list_car'),

    #le prix
    #les voitures
    path('prix/', views.add_price, name='add_price'),


    #les livraisons

    # Tableau récapitulatif des livraison  par moi
    path('liste_mois/', views.tableau_mensuel_livraison, name='list_mois'),

    path('liste_livraison/<str:pk>/', views.list_livraison, name='list_livraison'),
    path('print_livraison/<str:pk>/', views.print_livraison, name='print_livraison'),



]
