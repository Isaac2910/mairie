from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ActeEtatCivil, ActeNaissance, ActeMariage, ActeDeces
from .forms import LoginForm  # À créer
from django.http import HttpResponse

def agent_login(request):
    """ Vue pour la connexion des agents municipaux """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            print("Utilisateur authentifié:", user)  # Debug

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            print("Formulaire non valide :", form.errors)  # Debug
    else:
        form = LoginForm()
    
    return render(request, "auth/login.html", {"form": form})
def agent_login(request):
    """ Vue pour la connexion des agents municipaux """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            print("Utilisateur authentifié:", user)  # Debug

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            print("Formulaire non valide :", form.errors)  # Debug
    else:
        form = LoginForm()
    
    return render(request, "auth/login.html", {"form": form})


@login_required
def agent_logout(request):
    """ Vue pour la déconnexion """
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    """ Vue principale après connexion """
    actes = ActeEtatCivil.objects.all().order_by('-date_enregistrement')
    return render(request, "dashboard.html", {"actes": actes})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ActeEtatCivil, ActeNaissance, ActeMariage, ActeDeces

@login_required
def detail_acte(request, acte_id):
    """ Vue pour afficher les détails d’un acte d’état civil """
    acte = get_object_or_404(ActeEtatCivil, id=acte_id)

    if acte.type_acte == "naissance":
        details = get_object_or_404(ActeNaissance, acte=acte)
    elif acte.type_acte == "mariage":
        details = get_object_or_404(ActeMariage, acte=acte)
    elif acte.type_acte == "deces":
        details = get_object_or_404(ActeDeces, acte=acte)
    else:
        details = None

    return render(request, "actes/detail.html", {"acte": acte, "details": details})

@login_required
def telecharger_acte(request, acte_id):
    """ Vue pour télécharger un acte en PDF """
    acte = get_object_or_404(ActeEtatCivil, id=acte_id)
    if acte.document_pdf:
        response = HttpResponse(acte.document_pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{acte.numero_acte}.pdf"'
        return response
    messages.error(request, "Aucun document PDF disponible pour cet acte.")
    return redirect('detail_acte', acte_id=acte_id)


from django.http import JsonResponse
from django.db.models import Q
from .models import ActeEtatCivil

@login_required
def rechercher_actes(request):
    """ Vue pour la recherche avancée d'actes """
    query = request.GET.get('q', '')
    type_acte = request.GET.get('type_acte', '')
    date_debut = request.GET.get('date_debut', '')
    date_fin = request.GET.get('date_fin', '')
    agent = request.GET.get('agent', '')

    actes = ActeEtatCivil.objects.all()

    if query:
        actes = actes.filter(
            Q(numero_acte__icontains=query) |
            Q(type_acte__icontains=query) |
            Q(agent_responsable__username__icontains=query)
        )

    if type_acte:
        actes = actes.filter(type_acte=type_acte)

    if date_debut and date_fin:
        actes = actes.filter(date_enregistrement__range=[date_debut, date_fin])

    if agent:
        actes = actes.filter(agent_responsable__username__icontains=agent)

    # Serialisation des résultats
    results = [
        {
            "id": acte.id,
            "type": acte.get_type_acte_display(),
            "numero": acte.numero_acte,
            "date": acte.date_enregistrement.strftime("%d/%m/%Y"),
            "agent": acte.agent_responsable.username if acte.agent_responsable else "Inconnu",
        }
        for acte in actes
    ]

    return JsonResponse({"results": results})



from django.shortcuts import render, get_object_or_404
from .models import AgentMunicipal

def agent_profil(request, id):
    # Récupérer l'agent par son ID
    agent = get_object_or_404(AgentMunicipal, pk=id)

    # Renvoyer les informations dans le template
    return render(request, 'agent_profil.html', {'agent': agent})
