# Vues (views.py)
from django.shortcuts import render, redirect, get_object_or_404
from .models import Trading, Player,Team
from .forms import PlayerForm, TradingForm



def propose_trading(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    
    if request.method == 'POST':
        form = TradingForm(request.POST)
        if form.is_valid():
            proposed_value = form.cleaned_data['proposed_value']
            trading = Trading(player=player, buyer=request.user, seller=player.player_team.owner, proposed_value=proposed_value)
            trading.save()
            return redirect('gestion:trading_list')
    else:
        form = TradingForm()
    
    return render(request, 'propose_trading.html', {'player': player, 'form': form})


def gestion(request):
    players = Player.objects.all()
    teams = Team.objects.all()
    return render(request, 'gestion.html', {'players': players, 'teams':teams})

from .forms import PlayerForm, TeamForm

def create_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)  # Crée l'instance du joueur sans enregistrer
            player.player_team = form.cleaned_data['player_team']
            player.save()  # Enregistre le joueur avec le propriétaire
            return redirect('gestion:gestion')  # Redirigez vers la liste des joueurs
    else:
        form = PlayerForm()
    return render(request, 'create_player.html', {'form': form})

def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)  # Crée l'instance du joueur sans enregistrer
            team.owner = request.user  # Définit le propriétaire comme l'utilisateur connecté
            team.save()  # Enregistre le joueur avec le propriétaire
            return redirect('gestion:gestion')  # Redirigez vers la liste des joueurs
    else:
        form = TeamForm()
    return render(request, 'create_team.html', {'form': form})

def player_list(request):
    players = Player.objects.all()
    teams = Team.objects.all()
    return render(request, 'gestion.html', {'players': players, 'teams':teams})

def trading_list(request):
    tradings =Trading.objects.all()
    
    return render(request, 'trading_list.html', {'tradings': tradings,})




def manage_trading(request, trading_id):
    trading = get_object_or_404(Trading, pk=trading_id, seller=request.user)
    
    if request.method == 'POST':
        action = request.POST['action']
        
        if action == 'accept':
            trading.is_accepted = True
            trading.save()
        elif action == 'reject':
            trading.is_accepted = False
            trading.save()
        elif action == 'propose':
            new_value = request.POST['new_value']
            trading.proposed_value = new_value
            trading.save()
            
        return redirect('gestion:trading_list')
    
    return render(request, 'manage_trading.html', {'trading': trading})


def accept_trading(request, trading_id):
    trading = get_object_or_404(Trading, pk=trading_id)

    # Vérifiez si l'utilisateur est le propriétaire du joueur ou de l'équipe du joueur
    if request.user == trading.player.player_team.owner or request.user == trading.player.owner:
        trading.is_accepted = True
        trading.save()

    return redirect('gestion:trading_list')