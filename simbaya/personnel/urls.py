from django.urls import path

from . import views

urlpatterns=[
    path('',views.personnel,name='personnel'),
    path('liste/',views.list_personnel,name='liste_personnel'),
    path('update/<str:pk>',views.update,name='update'),
    path('liste/<str:pk>',views.remove,name='remove'),
    path('personnels/',views.recherche, name='personnels'),
    path('salaire/<str:pk>/', views.fichier, name='generer_salaire'),


]