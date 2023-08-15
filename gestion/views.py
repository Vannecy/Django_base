# Vues (views.py)
from django.shortcuts import render, redirect, get_object_or_404
from .models import Trading, Player,Team, Messagerie
from .forms import PlayerForm, TradingForm,ComposeMessageForm
from django.contrib.auth.models import User

def home(request):   
    return render(request, 'home.html')

def profil(request): 
    return render(request, 'profil.html')





#Messagerie---------------------------------------------------------------
def messagerie(request):
    user = request.user
    messages = Messagerie.objects.filter(recever=user) | Messagerie.objects.filter(sender=user)
    
    return render(request, 'messagerie.html', {'messages': messages})



def message_detail(request, messagerie_id):
    message = get_object_or_404(Messagerie, pk=messagerie_id)
    message.status = 'lus'
    message.save()
    return render(request, 'message_detail.html', {'message': message})


def compose_message(request, receiver_id, trading_number):
    print(trading_number)
    receiver = User.objects.get(id=receiver_id)  # Assurez-vous d'importer le modèle User
    trading = Trading.objects.get(id=trading_number)
    initial_data = {
        'receiver': receiver,
        'subject': '',
        'trading_number': trading_number
    }

    if request.method == 'POST':
        form = ComposeMessageForm(request.POST, initial=initial_data)
        if form.is_valid():
            sender = request.user
            text = form.cleaned_data['text']
            subject = form.cleaned_data['subject']

            
            message = Messagerie(sender=sender,status='non lus', recever=receiver, subject=subject, text=text, trading_number=trading)
            trading.proposed_value = form.cleaned_data['proposed_amount']
            trading.save()
            message.save()
            
            return redirect('gestion:messagerie')
    else:
        form = ComposeMessageForm(initial=initial_data)
        proposed_value= trading.proposed_value

    return render(request, 'compose_message.html', {'form': form, 'proposed_value':proposed_value})

#Messagerie---------------------------------------------------------------
from .forms import PlayerForm, TeamForm

def create_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)  # Crée l'instance du joueur sans enregistrer
            player.player_team = form.cleaned_data['player_team']
            player.save()  # Enregistre le joueur avec le propriétaire
            return redirect('gestion:home')  # Redirigez vers la liste des joueurs
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
            return redirect('gestion:home')  # Redirigez vers la liste des joueurs
    else:
        form = TeamForm()
    return render(request, 'create_team.html', {'form': form})

def player_list(request):
    players = Player.objects.all()
    teams = Team.objects.all()
    return render(request, 'player_list.html', {'players': players, 'teams':teams})
def team_list(request):
    players = Player.objects.all()
    teams = Team.objects.all()
    return render(request, 'team_list.html', {'players': players, 'teams':teams})

def player_detail(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    return render(request, 'player_detail.html', {'player': player})

def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return render(request, 'team_detail.html', {'team': team})


#Trading-----------------------------------------------------------------------------------------------------------------------------------------------
from django.utils import timezone
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

def trading_list(request):

    user = request.user
    buyer_tradings = Trading.objects.filter(buyer=user)
    seller_tradings = Trading.objects.filter(seller=user)
    
    return render(request, 'trading_list.html', {'buyer_tradings': buyer_tradings, 'seller_tradings': seller_tradings})



def manage_trading(request, trading_id):
    trading = get_object_or_404(Trading, pk=trading_id)
    
    if request.method == 'POST':
        action = request.POST['action']
        
        if action == 'accept':
            trading.is_accepted = True
            trading.sell_price = trading.proposed_value
        elif action == 'reject':
            trading.is_accepted = False
            trading.status = 'rejected'
        elif action == 'propose':
            new_value = request.POST['new_value']
            trading.contre_proposition_price = new_value
        
        trading.save()
        
        # Send a message to the buyer or seller
        if action == 'propose' or action == 'accept' or action == 'reject':
            recipient = trading.buyer if request.user == trading.seller else trading.seller
            subject = f"Trading Update for {trading.player.name}"
            text = f"Your trading proposal for {trading.player.name} has been {action}."
            if action == 'propose':
                text += f" New proposed value: ${new_value}"
            message = Messagerie(sender=request.user, recever=recipient, subject=subject, text=text, trading_number = trading)
            message.save()
            return redirect('gestion:trading_list')
    
    is_buyer = request.user == trading.buyer
    is_seller = request.user == trading.seller
    
    return render(request, 'manage_trading.html', {'trading': trading, 'is_buyer': is_buyer, 'is_seller': is_seller})



def accept_trading(request, trading_id):
    trading = get_object_or_404(Trading, pk=trading_id)

    # Vérifiez si l'utilisateur est le propriétaire du joueur ou de l'équipe du joueur
    if request.user == trading.player.player_team.owner or request.user == trading.player.owner:
        trading.is_accepted = True
        trading.save()

    return redirect('gestion:trading_list')