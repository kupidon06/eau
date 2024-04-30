from django.urls import path
from . import views

urlpatterns=[
    path('',views.depenses,name="depenses"),

    path('liste_depenses/<str:pk>/', views.list_depenses, name='list_depenses'),
    

    # Modification d'une vente spécifique
    path('modif_depenses/<str:pk>/', views.update_depenses, name='update_depenses'),

    # Suppression d'une vente spécifique
    path('suprimer/<str:pk>/', views.remove_depenses, name='remove_depenses'),

    # Vue de recherche pour filtrer les ventes
    path('depenses:/', views.recherche, name='ma_vue_depense'),

    # Tableau récapitulatif des ventes par jour
    path('liste_depense_day/', views.tableau_recapitulatif, name='list_depense_day'),
    path('print_liste_depense_day/', views.fichier, name='print_list_depense_day'),

    # Générer un fichier Excel pour les ventes d'une date spécifique
    #path('generer_fichier_excel_depenses/<str:pk>/', views.generer_fichier_excel, name='generer_fichier_excel_depenses'),

]