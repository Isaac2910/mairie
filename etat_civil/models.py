from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class AgentMunicipal(AbstractUser):
    """ Modèle représentant un agent municipal qui gère les actes """
    matricule = models.CharField(max_length=20, unique=True)
    fonction = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.username} - {self.fonction}"
    
    
    
    # Ajouter un `related_name` pour éviter le conflit
    groups = models.ManyToManyField(
        Group,
        related_name='agentmunicipal_set',  #  nom unique
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='agentmunicipal_permissions',  #  nom unique
        blank=True,
    )

    def __str__(self):
        return f"{self.username} - {self.fonction}"


class ActeEtatCivil(models.Model):
    """ Modèle générique pour tous les actes d’état civil """
    TYPE_ACTE_CHOICES = [
        ('naissance', 'Acte de Naissance'),
        ('mariage', 'Acte de Mariage'),
        ('deces', 'Acte de Décès'),
    ]
    
    type_acte = models.CharField(max_length=10, choices=TYPE_ACTE_CHOICES)
    numero_acte = models.CharField(max_length=50, unique=True)
    date_enregistrement = models.DateField(auto_now_add=True)
    agent_responsable = models.ForeignKey(AgentMunicipal, on_delete=models.SET_NULL, null=True)
    document_pdf = models.FileField(upload_to='actes/', blank=True, null=True)  # Stockage du PDF
    
    def __str__(self):
        return f"{self.get_type_acte_display()} - {self.numero_acte}"


class ActeNaissance(models.Model):
    """ Acte de naissance lié à un acte d’état civil """
    acte = models.OneToOneField(ActeEtatCivil, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=150)
    nom_pere = models.CharField(max_length=100, blank=True, null=True)
    nom_mere = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Naissance {self.nom} {self.prenom} - {self.acte.numero_acte}"


class ActeMariage(models.Model):
    """ Acte de mariage lié à un acte d’état civil """
    acte = models.OneToOneField(ActeEtatCivil, on_delete=models.CASCADE)
    nom_conjoint1 = models.CharField(max_length=100)
    nom_conjoint2 = models.CharField(max_length=100)
    date_mariage = models.DateField()
    lieu_mariage = models.CharField(max_length=150)

    def __str__(self):
        return f"Mariage {self.nom_conjoint1} & {self.nom_conjoint2} - {self.acte.numero_acte}"


class ActeDeces(models.Model):
    """ Acte de décès lié à un acte d’état civil """
    acte = models.OneToOneField(ActeEtatCivil, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    date_deces = models.DateField()
    lieu_deces = models.CharField(max_length=150)
    cause_deces = models.TextField()

    def __str__(self):
        return f"Décès {self.nom} - {self.acte.numero_acte}"
