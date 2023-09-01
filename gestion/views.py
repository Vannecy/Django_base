# Vues (views.py)
from django.shortcuts import render, redirect, get_object_or_404
from .models import Trading, Player,Team, Messagerie, Profil
from .forms import PlayerForm, TradingForm,ComposeMessageForm,ComposeInitialMessageForm, DeleteMessagesForm, ProfilForm, TeamForm,DeleteMessagesForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from django.http import HttpResponseNotFound
from .tests import generate_offensive_player_profile,generate_random_birthdate,generate_defensive_player_profile,generate_goalkipper_player_profile
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def home(request):   

    team = Team.objects.all()
    team = random.choice(team)
    player_profile = generate_offensive_player_profile()
    date_obj = datetime.strptime(player_profile['Birthday'], "%d/%m/%Y")
    
    player = Player(nationnality=player_profile['Nationnality'], name=player_profile['Name'],second_name=player_profile['Second_name'],player_team=team,value=player_profile['Value'],price=0,date_de_naissance=date_obj,size=player_profile['taille'],weight=player_profile['poids'],feet=player_profile['Feet'], style=player_profile['Style'],main_position=player_profile['Poste'],general=player_profile['General'],attaque=player_profile['Attaque'],defense=player_profile['Defense'],)
    player.save()
    team = Team.objects.all()
    team = random.choice(team)
    player_profile = generate_defensive_player_profile()
    date_obj = datetime.strptime(player_profile['Birthday'], "%d/%m/%Y")
    player = Player(nationnality=player_profile['Nationnality'],name=player_profile['Name'],second_name=player_profile['Second_name'],player_team=team,value=player_profile['Value'],price=0,date_de_naissance=date_obj,size=player_profile['taille'],weight=player_profile['poids'],feet=player_profile['Feet'], style=player_profile['Style'],main_position=player_profile['Poste'],general=player_profile['General'],attaque=player_profile['Attaque'],defense=player_profile['Defense'],)
    player.save()


    return render(request, 'home.html')

@login_required(login_url='/auth/inscription/')
def profil(request):
    profil = Profil.objects.filter(user_profil=request.user).first()
    team_form = TeamForm()
    profil_form = ProfilForm()

    if request.method == 'POST':
        if profil and not profil.team_profil:
            # Si un profil existe mais pas d'équipe, associez l'équipe au profil
            team_form = TeamForm(request.POST)
            if team_form.is_valid():
                team_name = team_form.cleaned_data['team_name']
                print('team nammmmmmmme', team_name)
                team = Team(name=team_name, owner=request.user, budget=50000)
                team.save()
                team.save()
                profil.team_profil = team
                profil.save()
                return redirect('gestion:profil')
        else:
            # Si ni un profil ni une équipe n'existent, créez-les
            team_form = TeamForm(request.POST)
            profil_form = ProfilForm(request.POST)
            if team_form.is_valid() and profil_form.is_valid():
                team_name = team_form.cleaned_data['team_name']
                print('team nammmmmmmme', team_name)
                team = Team(name=team_name, owner=request.user, budget=50000)
                team.save()
                profil_name = profil_form.cleaned_data['profil_name']
                profil = Profil(name=profil_name, user_profil=request.user, team_profil=team)
                profil.save()
                return redirect('gestion:profil')

    return render(request, 'profil.html', {'team_form': team_form, 'profil_form': profil_form, 'profil': profil })


#Messagerie---------------------------------------------------------------
@login_required(login_url='/auth/inscription/')
def messagerie(request):
    user = request.user
    status_filter = request.GET.get('status')
    from_filter = request.GET.get('from')
    trading_number_filter = request.GET.get('trading_number')
    delete_form = DeleteMessagesForm(request.POST or None)
    
    messages = Messagerie.objects.filter(recever=user)
    
    if request.method == 'POST':
        if 'delete_selected' in request.POST:
            delete_form = DeleteMessagesForm(request.POST)
            if delete_form.is_valid():
                selected_messages = delete_form.cleaned_data.get('selected_messages')
                if selected_messages:
                    Messagerie.objects.filter(id__in=selected_messages).delete()
    
    if status_filter == 'unread':
        messages = messages.filter(status='non lus')
    elif status_filter == 'read':
        messages = messages.filter(status='lus')
    elif status_filter == 'replied':
        messages = messages.filter(status='repondu')
    
    if from_filter:
        messages = messages.filter(sender__username__icontains=from_filter)
    
    if trading_number_filter:
        messages = messages.filter(trading_number_id=trading_number_filter)
    
    return render(request, 'messagerie.html', {
        'messages': messages,
        'status_filter': status_filter,
        'from_filter': from_filter,
        'trading_number_filter': trading_number_filter,
        'delete_form': delete_form,  # Passer le formulaire au modèle
    })

@login_required(login_url='/auth/inscription/')
def message_detail(request, messagerie_id):
    message = get_object_or_404(Messagerie, pk=messagerie_id)
    message.status = 'lus'
    message.save()
    trading = message.trading_number
    
    
    return render(request, 'message_detail.html', {'message': message, 'trading':trading})
@login_required(login_url='/auth/inscription/')
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
@login_required(login_url='/auth/inscription/')
def delete_message(request, message_id):
    
    message = Messagerie.objects.get(id=message_id)
    message.delete()

    return redirect('gestion:messagerie')
@login_required(login_url='/auth/inscription/')
def delete_selected_messages(request):
    if request.method == 'POST':
        delete_form = DeleteMessagesForm(request.POST)
        if delete_form.is_valid():
            selected_messages = delete_form.cleaned_data['selected_messages']
            Messagerie.objects.filter(id__in=selected_messages).delete()
    return redirect('gestion:messagerie')
@login_required(login_url='/auth/inscription/')
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
@login_required(login_url='/auth/inscription/')
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
@login_required(login_url='/auth/inscription/')
def create_team(request):
    if not request.user.team_set.exists():
        if request.method == 'POST':
            form = TeamForm(request.POST)
            form2 = ProfilForm(request.POST)
            if form.is_valid() and form2.is_valid():             
                team = form.save(commit=False)  # Crée l'instance du joueur sans enregistrer
                team.owner = request.user  # Définit le propriétaire comme l'utilisateur connecté
                team.budget = 500000             
                team.save()  # Enregistre le joueur avec le propriétaire
                name = f'{team.owner} team'
                profil = Profil(name=name, user_profil=request.user, team_profil=team)
                profil.save()
                return redirect('profil:home')  # Redirigez vers la liste des joueurs
        else:
            form = TeamForm()
            form2 = ProfilForm()
        return render(request, 'profil.html', {'form': form})
    else:
        message = 'Vous avez deja une equipe'
        return render(request, 'home.html', {'message': message})

def player_list(request):
    players = Player.objects.all()
    search_name = request.GET.get('search_name')
    search_nationnality = request.GET.get('search_nationnality')
    search_team = request.GET.get('search_team')
    search_poste = request.GET.get('search_poste')
    search_foot = request.GET.get('search_foot')
    search_style = request.GET.get('search_style')
    search_general_min = request.GET.get('search_general_min')
    search_general_max = request.GET.get('search_general_max')
    sort_by = request.GET.get('sort_by')

    # Créez un objet Q vide pour les filtres
    filters = Q()

    if search_foot:
        filters &= Q(feet=search_foot)

    if search_name:
        filters &= Q(name__istartswith=search_name)

    if search_nationnality:
        filters &= Q(nationnality__istartswith=search_nationnality)

    if search_team:
        filters &= Q(player_team__name__istartswith=search_team)

    if search_style:
        filters &= Q(style=search_style)

    if search_poste:
        filters &= Q(main_position=search_poste)

    if search_general_min:
        filters &= Q(general__gte=search_general_min)

    if search_general_max:
        filters &= Q(general__lte=search_general_max)

    # Appliquez les filtres uniquement si au moins un champ de recherche est spécifié
    if search_foot or search_name or search_style or search_general_min or search_general_max or search_poste or search_team or search_nationnality:
        players = players.filter(filters)
    if sort_by:
        if sort_by == 'name':
            players = players.order_by('name')
        elif sort_by == 'team':
            players = players.order_by('player_team__name')
        elif sort_by == 'user':
            players = players.order_by('player_team__owner__username')
        elif sort_by == 'price':
            players = players.order_by('price')
        elif sort_by == 'style':
            players = players.order_by('style')
        elif sort_by == 'general':
            players = players.order_by('general')
        elif sort_by == 'foot':
            players = players.order_by('feet')
        elif sort_by == 'nationnality':
            players = players.order_by('nationnality')
    # Créez un objet Paginator avec 15 joueurs par page
    paginator = Paginator(players, 15)

    page = request.GET.get('page')
    
    try:
        players = paginator.page(page)
    except PageNotAnInteger:
        # Si la page n'est pas un entier, affichez la première page
        players = paginator.page(1)
    except EmptyPage:
        # Si la page est hors limites (par exemple, 9999), affichez la dernière page
        players = paginator.page(paginator.num_pages)

    teams = Team.objects.all()
    player = Player()
    
    return render(request, 'player_list.html', {
        'player': player,
        'players': players,
        'teams': teams,
        'search_name': search_name,
        'search_foot': search_foot,
        'search_style': search_style,
        'search_general_min': search_general_min,
        'search_general_max': search_general_max,
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
    players = Player.objects.filter(player_team=team)
    
    return render(request, 'team_detail.html', {'team': team, 'players':players})


#Trading-----------------------------------------------------------------------------------------------------------------------------------------------


@login_required(login_url='/auth/inscription/')
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
@login_required(login_url='/auth/inscription/')
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
    


@login_required(login_url='/auth/inscription/')
def accept_trading(request, trading_id):
    trading = get_object_or_404(Trading, pk=trading_id)

    # Vérifiez si l'utilisateur est le propriétaire du joueur ou de l'équipe du joueur
    if request.user == trading.player.player_team.owner or request.user == trading.player.owner:
        trading.is_accepted = True
        trading.save()

    return redirect('gestion:trading_list')