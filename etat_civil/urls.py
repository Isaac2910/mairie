from django.urls import path
from . import views

urlpatterns = [
    path('', views.agent_login, name='login'),
    path('logout/', views.agent_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('acte/<int:acte_id>/', views.detail_acte, name='detail_acte'),
    path('acte/<int:acte_id>/telecharger/', views.telecharger_acte, name='telecharger_acte'),
    #path('actes/', views.liste_actes, name='liste_actes'),
    path('agent/<int:id>/profil/', views.agent_profil, name='agent_profil'),
]


