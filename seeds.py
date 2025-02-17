from django.contrib.auth import get_user_model
from etat_civil.models import AgentMunicipal, ActeEtatCivil, ActeNaissance, ActeMariage, ActeDeces
from django.utils import timezone

# Création des agents municipaux
agents = [
    {"username": "jdoe", "matricule": "AGT001", "fonction": "Officier d'état civil"},
    {"username": "asmith", "matricule": "AGT002", "fonction": "Secrétaire municipal"},
    {"username": "mdupont", "matricule": "AGT003", "fonction": "Archiviste"},
]

for agent_data in agents:
    agent, created = AgentMunicipal.objects.get_or_create(
        username=agent_data["username"],
        matricule=agent_data["matricule"],
        fonction=agent_data["fonction"]
    )
    if created:
        agent.set_password("password123")  # Définir un mot de passe par défaut
        agent.save()

# Création des actes d'état civil
actes = [
    {"type_acte": "naissance", "numero_acte": "N001", "agent_responsable": AgentMunicipal.objects.get(matricule="AGT001")},
    {"type_acte": "mariage", "numero_acte": "M001", "agent_responsable": AgentMunicipal.objects.get(matricule="AGT002")},
    {"type_acte": "deces", "numero_acte": "D001", "agent_responsable": AgentMunicipal.objects.get(matricule="AGT003")},
]

for acte_data in actes:
    ActeEtatCivil.objects.get_or_create(
        type_acte=acte_data["type_acte"],
        numero_acte=acte_data["numero_acte"],
        agent_responsable=acte_data["agent_responsable"]
    )

# Création des actes spécifiques
ActeNaissance.objects.get_or_create(
    acte=ActeEtatCivil.objects.get(numero_acte="N001"),
    nom="Doe", prenom="John", date_naissance=timezone.now().date(),
    lieu_naissance="Libreville", nom_pere="Jean Doe", nom_mere="Marie Doe"
)

ActeMariage.objects.get_or_create(
    acte=ActeEtatCivil.objects.get(numero_acte="M001"),
    nom_conjoint1="Alice", nom_conjoint2="Bob", date_mariage=timezone.now().date(),
    lieu_mariage="Libreville"
)

ActeDeces.objects.get_or_create(
    acte=ActeEtatCivil.objects.get(numero_acte="D001"),
    nom="Martin", date_deces=timezone.now().date(),
    lieu_deces="Libreville", cause_deces="Cause naturelle"
)

print("Données de test insérées avec succès !")
