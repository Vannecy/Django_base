# Vues (views.py)
from django.shortcuts import render, redirect, get_object_or_404
from .models import Trading, Player,Team, Messagerie, Profil
from .forms import PlayerForm, TradingForm,ComposeMessageForm,ComposeInitialMessageForm, DeleteMessagesForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from django.http import HttpResponseNotFound

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def home(request):   
    if request.user.team_set.exists():
        print("exist")
    return render(request, 'home.html')

def profil(request): 
    profil = Profil.objects.filter(user_profil=request.user).first()
    
    return render(request, 'profil.html', {'profil':profil})





#Messagerie---------------------------------------------------------------
def messagerie(request):
    user = request.user
    status_filter = request.GET.get('status')
    from_filter = request.GET.get('from')  # Récupérer la valeur du champ 'from'
    trading_number_filter = request.GET.get('trading_number')  # Récupérer la valeur du champ 'trading_number'
    delete_form = DeleteMessagesForm(request.POST or None)
                
    messages = Messagerie.objects.filter(recever=user)
    if 'delete_selected' in request.POST:
            selected_messages = delete_form.cleaned_data['selected_messages']
            print(selected_messages)
            # Bouclez à travers les messages sélectionnés et supprimez-les
    # Appliquer les filtres en fonction des valeurs des champs de recherche
    if status_filter == 'unread':
        messages = messages.filter(status='non lus')
    elif status_filter == 'read':
        messages = messages.filter(status='lus')
    elif status_filter == 'replied':
        messages = messages.filter(status='repondu')
    
    if from_filter:  # Vérifier si 'from_filter' est défini
        messages = messages.filter(sender__username__icontains=from_filter)  # Filtrer par nom d'utilisateur (from)
    
    if trading_number_filter:  # Vérifier si 'trading_number_filter' est défini
        print(trading_number_filter)

        messages = messages.filter(trading_number_id=trading_number_filter)
    
    return render(request, 'messagerie.html', {
        'messages': messages,
        'status_filter': status_filter,
        'from_filter': from_filter,  # Passer 'from_filter' au modèle pour pré-remplir le champ de recherche
        'trading_number_filter': trading_number_filter,  # Passer 'trading_number_filter' au modèle pour pré-remplir le champ de recherche
    })



def message_detail(request, messagerie_id):
    message = get_object_or_404(Messagerie, pk=messagerie_id)
    message.status = 'lus'
    message.save()
    trading = message.trading_number
    
    
    return render(request, 'message_detail.html', {'message': message, 'trading':trading})
def create_message(request):
    if request.method == 'POST':
        form = ComposeInitialMessageForm(request.POST)
        if form.is_valid():
            sender = request.user
            text = form.cleaned_data['text']
            subject = form.cleaned_data['subject']
            receiver_name = form.cleaned_data['receiver']

            try:
                # Vérifiez si l'équipe spécifiée dans le champ "From" existe
                receiver_team = Team.objects.get(name=receiver_name)

                # Créez le message avec l'équipe en tant que destinataire
                message = Messagerie(sender=sender, status='non lus', recever=receiver_team.owner, subject=subject, text=text, trading_number=None)
                message.save()

                return redirect('gestion:messagerie')

            except Team.DoesNotExist:
                # L'équipe spécifiée n'existe pas, ajoutez une erreur au formulaire
                form.add_error('receiver', "L'équipe spécifiée n'existe pas.")
    else:
        form = ComposeInitialMessageForm()

    return render(request, 'response_message.html', {'form': form})

def confirm_delete_message(request, message_id):
    message = Messagerie.objects.get(pk=message_id)
    if request.method == "POST":
        # Traitez la logique de suppression ici
        message.delete()
        return redirect('gestion:message_deleted')  # Redirigez vers la page de confirmation de suppression

    return render(request, 'confirm_delete_message.html', {'message_id': message_id})

def delete_message(request, message_id):
    
    message = Messagerie.objects.get(id=message_id)
    message.delete()

    return redirect('gestion:messagerie')

def delete_selected_messages(request):
    if request.method == 'POST':
        selected_messages = request.POST.getlist('selected_messages')
        # Supprimer les messages sélectionnés
        Messagerie.objects.filter(id__in=selected_messages).delete()
        return redirect('gestion:messagerie')

    return HttpResponseNotFound("Page not found")

def response_message(request, receiver_id, trading_number,message_id):
   
    receiver = User.objects.get(id=receiver_id)  # Assurez-vous d'importer le modèle User
    trading = Trading.objects.get(id=trading_number)
    player = trading.player
    
    initial_data = {
        'receiver': receiver,
        'subject': '',
        'trading_number': trading_number,
        
    }

    if request.method == 'POST':
        form = ComposeMessageForm(request.POST, initial=initial_data)
        if form.is_valid():
            sender = request.user
            if sender == trading.buyer:
                recever = trading.seller
            else:
                recever=trading.buyer
            text = form.cleaned_data['text']
            subject = form.cleaned_data['subject']

            message_repondus = Messagerie.objects.get(id=message_id)
            message_repondus.status = 'repondu'
            message_repondus.save()
            message_reponse = Messagerie(sender=sender,status='non lus', recever=recever, subject=subject, text=text, trading_number=trading)
            #trading.contre_proposition_price = form.cleaned_data['proposed_amount']
            if trading.talking_to == trading.seller:
                trading.talking_to = trading.buyer
            else:
                trading.talking_to = trading.seller 
            trading.save()
            message_reponse.save()
            
            
            return redirect('gestion:messagerie')
    else:
        form = ComposeMessageForm(initial=initial_data)
        proposed_value= trading.proposed_value

    return render(request, 'response_message.html', {'form': form, 'proposed_value':proposed_value, 'receiver':receiver, 'trading_number':trading_number, 'player':player, })

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
    if not request.user.team_set.exists():
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
    else:
        message = 'Vous avez deja une equipe'
        return render(request, 'home.html', {'message': message})

def player_list(request):
    players = Player.objects.all()

    search_name = request.GET.get('search_name')
    sort_by = request.GET.get('sort_by')

    if search_name:
        players = players.filter(name__istartswith=search_name)
    else:
        if sort_by == 'name':
            players = players.order_by('name')
        elif sort_by == 'team':
            players = players.order_by('player_team')
        elif sort_by == 'user':
            players = players.order_by('player_team__owner')
        elif sort_by == 'price':
            players = players.order_by('value')

    teams = Team.objects.all()
    return render(request, 'player_list.html', {
        'players': players,
        'teams': teams,
        'search_name': search_name,
        'sort_by': sort_by,
    })



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
            trading = Trading(player=player, buyer=request.user, seller=player.player_team.owner, proposed_value=proposed_value, talking_to = player.player_team.owner)
            message = Messagerie(trading_number=trading,sender=request.user,recever=player.player_team.owner,subject=f'Nouvelle offre pour {player}', text = f'Hello, {request.user} propose you {proposed_value} for {player}', is_original=True)
            
            trading.save()
            message.save()
            return redirect('gestion:trading_list')
    else:
        form = TradingForm()
    
    return render(request, 'propose_trading.html', {'player': player, 'form': form})

from django.db.models import Q

def trading_list(request):
    user = request.user
    sort_by = request.GET.get('sort_by')
    status_accepted = request.GET.get('status_accepted')
    status_rejected = request.GET.get('status_rejected')
    status_pending = request.GET.get('status_pending')
    status_closed = request.GET.get('status_closed')  # Nouveau paramètre de filtre
    status_proposed = request.GET.get('status_proposed')  # Nouveau paramètre de filtre

    buyer_tradings = Trading.objects.filter(buyer=user)
    seller_tradings = Trading.objects.filter(seller=user)

    q_objects = Q()

    if status_accepted:
        q_objects |= Q(status_trading='accepted')
    if status_rejected:
        q_objects |= Q(status_trading='rejected')
    if status_pending:
        q_objects |= Q(status_trading='pending')
    if status_closed:
        q_objects |= Q(status_trading='closed')  # Filtrer par le nouveau statut "closed"
    if status_proposed:
        q_objects |= Q(status_trading='proposed')  # Filtrer par le nouveau statut "proposed"

    buyer_tradings = buyer_tradings.filter(q_objects)
    seller_tradings = seller_tradings.filter(q_objects)

    if sort_by == 'status':
        buyer_tradings = buyer_tradings.order_by('status_trading')
        seller_tradings = seller_tradings.order_by('status_trading')
    elif sort_by == 'price':
        buyer_tradings = buyer_tradings.order_by('sell_price')
        seller_tradings = seller_tradings.order_by('sell_price')

    return render(request, 'trading_list.html', {
        'buyer_tradings': buyer_tradings,
        'seller_tradings': seller_tradings,
        'sort_by': sort_by,
        'status_accepted': status_accepted,
        'status_rejected': status_rejected,
        'status_pending': status_pending,
        'status_closed': status_closed,
        'status_proposed': status_proposed,
    })



@login_required
def manage_trading(request, trading_id):
    trading = get_object_or_404(Trading, id=trading_id)
    seller_profil = Profil.objects.filter(user_profil=trading.seller).first()
    buyer_profil = Profil.objects.filter(user_profil=trading.buyer).first()
    print("acheteur",buyer_profil)
    print("vendeur",seller_profil)
    if trading.talking_to == trading.seller:
        message_sender = trading.seller
        message_recever = trading.buyer
    else:
        message_sender = trading.buyer
        message_recever = trading.seller

    
    if request.method == 'POST':
        action = request.POST.get('action')    
        if action == 'accept':
            trading.is_accepted = True
            trading.status_trading = 'accepted'
            trading.sell_price = trading.proposed_value
            trading.talking_to = None
            trading.player
            trading.info = f'Transfert accepte pour un montant de {trading.sell_price} euros'
            message = Messagerie(trading_number=trading,sender=message_sender,recever=message_recever,subject=f'Re: Offre {trading.player} accepted', text = f'Hello, {message_recever} le transfert de {trading.player} est accepte', is_original=False)
            message.save()
            if seller_profil.team_profil.budget > trading.sell_price:
                seller_profil.team_profil.budget+=trading.sell_price
                buyer_profil.team_profil.budget-=trading.sell_price
                try:
                    buyer_profil.team_profil.save()
                    seller_profil.team_profil.save()
                    trading.save()
                except Exception as e:
                    print("Erreur lors de la sauvegarde : ", e)
            else:
                error_message = "Pas assez d'argent pour effectuer la transaction."
                return render(request, 'manage_trading.html', { 'trading_id': trading_id,'error_message': error_message})    
            
        elif action == 'reject':
            trading.status_trading = 'rejected'
            if trading.talking_to == trading.buyer:
                trading.talking_to = trading.seller
                trading.info = f'{trading.buyer} a refuse la contre proposition de {trading.contre_proposition_price}'
            else:
                trading.talking_to = trading.buyer
                trading.info = f'{trading.seller} a refuse la contre proposition de {trading.contre_proposition_price}'
            message = Messagerie(trading_number=trading,sender=message_sender,recever=message_recever,subject=f'Re: Offre pour {trading.player} rejected', text = f'Hello, {message_recever} le montant propose est rejete', is_original=False)
            message.save()
            trading.save()      


        elif action == 'counter':
            new_value = request.POST.get('new_value')
            trading.status_trading = 'pending'
            if new_value is not None:
                trading.contre_proposition_price = new_value
            if trading.talking_to == trading.buyer:
                trading.talking_to = trading.seller
                trading.info = f'Nouvelle contre proposition de {trading.buyer} de {trading.contre_proposition_price} euros'
            else:
                trading.talking_to = trading.buyer
                trading.info = f'Nouvelle contre proposition de {trading.seller} de {trading.contre_proposition_price} euros'
            message = Messagerie(trading_number=trading,sender=message_sender,recever=message_recever,subject=f'Re: Contre offre pour {trading.player}', text = f'Hello, {message_recever}, il y a une contre offre de {new_value} pour{trading.player}', is_original=False)
            message.save()
            trading.save()    

        elif action == 'accept_counter':
            trading.proposed_value = trading.contre_proposition_price
            trading.contre_proposition_price = None
            trading.is_accepted = True
            trading.status_trading = 'accepted'
            trading.sell_price = trading.proposed_value
            trading.talking_to = None
            trading.info = f'Transfert accepte pour un montant de {trading.sell_price} euros'
            message = Messagerie(trading_number=trading,sender=message_sender,recever=message_recever,subject=f'Re: Contre offre pour {trading.player} accepte', text = f'Hello, {message_recever} le montant propose est accepte', is_original=False)

            trading.save()
            message.save()

        elif action == 'close':     
            trading.is_accepted = False
            trading.status_trading = 'closed' 
            trading.talking_to = None
            trading.info = f'Le vendeur a mis fin a la negociation'
            message = Messagerie(trading_number=trading,sender=message_sender,recever=message_recever,subject=f'Re: Offre pour {trading.player} closed', text = f'Hello, {message_recever} transfert est clos', is_original=False)
            message.save()
            trading.save()   
    context = {
        'trading': trading,       
    }
    return render(request, 'manage_trading.html', context)
    



def accept_trading(request, trading_id):
    trading = get_object_or_404(Trading, pk=trading_id)

    # Vérifiez si l'utilisateur est le propriétaire du joueur ou de l'équipe du joueur
    if request.user == trading.player.player_team.owner or request.user == trading.player.owner:
        trading.is_accepted = True
        trading.save()

    return redirect('gestion:trading_list')