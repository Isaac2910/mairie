from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AgentMunicipal, ActeEtatCivil, ActeNaissance, ActeMariage, ActeDeces

@admin.register(AgentMunicipal)
class AgentMunicipalAdmin(UserAdmin):
    list_display = ('username', 'matricule', 'fonction', 'is_staff', 'is_active')
    search_fields = ('username', 'matricule', 'fonction')
    list_filter = ('is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {'fields': ('matricule', 'fonction')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {'fields': ('matricule', 'fonction')}),
    )

@admin.register(ActeEtatCivil)
class ActeEtatCivilAdmin(admin.ModelAdmin):
    list_display = ('type_acte', 'numero_acte', 'date_enregistrement', 'agent_responsable')
    search_fields = ('numero_acte',)
    list_filter = ('type_acte', 'date_enregistrement')

@admin.register(ActeNaissance)
class ActeNaissanceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'date_naissance', 'lieu_naissance', 'acte')
    search_fields = ('nom', 'prenom', 'acte__numero_acte')
    list_filter = ('date_naissance', 'lieu_naissance')

@admin.register(ActeMariage)
class ActeMariageAdmin(admin.ModelAdmin):
    list_display = ('nom_conjoint1', 'nom_conjoint2', 'date_mariage', 'lieu_mariage', 'acte')
    search_fields = ('nom_conjoint1', 'nom_conjoint2', 'acte__numero_acte')
    list_filter = ('date_mariage', 'lieu_mariage')

@admin.register(ActeDeces)
class ActeDecesAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_deces', 'lieu_deces', 'acte')
    search_fields = ('nom', 'acte__numero_acte')
    list_filter = ('date_deces', 'lieu_deces')
