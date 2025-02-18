from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ActeEtatCivil, ActeNaissance, ActeMariage, ActeDeces, AgentMunicipal
from .forms import LoginForm  
from django.http import HttpResponse

from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator





#vue login
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


#vue de deconnection
@login_required
def agent_logout(request):
    """ Vue pour la déconnexion """
    logout(request)
    return redirect('login')



#v detail
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

#vue doc pdf
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


#v  profil
@login_required
def agent_profil(request, id):
    # Récupérer l'agent par son ID
    agent = get_object_or_404(AgentMunicipal, pk=id)

    # Renvoyer les informations dans le template
    return render(request, 'agent_profil.html', {'agent': agent})



#vue de l'accueil
@login_required
def dashboard(request):
    """ Vue principale avec filtrage et pagination """
    type_acte = request.GET.get('type_acte')
    numero_acte = request.GET.get('numero_acte')
    
    
    # Récupération des actes avec filtrage
    queryset = ActeEtatCivil.objects.all()

    if type_acte:
        queryset = queryset.filter(type_acte=type_acte)
    if numero_acte:
        queryset = queryset.filter(numero_acte__icontains=numero_acte)
    
    # Pagination
    paginator = Paginator(queryset, 2)  # 10 actes par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'actes': page_obj}

    # Si c'est une requête AJAX, renvoyer seulement le tableau
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'actes/partials/liste_actes_table.html', context)

    # Sinon, afficher la page complète avec le formulaire et la pagination
    return render(request, "dashboard.html", context)
