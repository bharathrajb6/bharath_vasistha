from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from live.models import live, teams, player, ranking
import operator
import pyttsx3

team_name = ''


def preview(request):
    return render(request, 'preview.html')


def add_live(request):
    engine = pyttsx3.init()
    if request.method == 'POST':
        team_name = request.POST['team']
        p_name = request.POST['player']
        # par = request.POST['par']
        hole1 = request.POST['hole1']
        hole2 = request.POST['hole2']
        hole3 = request.POST['hole3']
        hole4 = request.POST['hole4']

        play = player.objects.get(player_name=p_name)
        team_n = teams.objects.get(team_name=team_name)

        print(play)

        liv = live.objects.all()
        for i in liv:
            if i.player.player_name == p_name:
                liv = i
                break

        print(liv)
        try:

            liv.hole1 = hole1
            liv.hole2 = hole2
            liv.hole3 = hole3
            liv.hole4 = hole4
            # liv.par = par
            liv.total = int(hole1) + int(hole2) + int(hole3) + int(hole4)
            liv.save()
        except:
            liv = live(teams=team_n, player=play, hole1=int(hole1), hole2=int(hole2), hole3=int(hole3),
                       hole4=int(hole4),
                       total=int(hole1) + int(hole2) + int(hole3) + int(hole4))
            liv.save()

        engine.say("LiveScore is updated")
        engine.runAndWait()
        messages.info(request, 'Livescore is updated')
        return redirect('admin_menu')

    else:

        p = player.objects.all()
        tms = teams.objects.all()

        return render(request, 'add_live.html', {'data': p, 'team': tms})


def players(request):
    pl = player.objects.all()
    return render(request, 'players.html', {'data': pl})


def delete_player(request):
    engine = pyttsx3.init()
    if request.method == 'POST':

        team_name = request.POST['team']
        player_name = request.POST['player_name']
        if player.objects.filter(teams=team_name, player_name=player_name).exists():
            obj = player.objects.filter(teams=team_name, player_name=player_name)
            obj.delete()

            engine.say("Player is deleted successfully")
            engine.runAndWait()

            messages.info(request, 'Player is deleted successfully')
            return redirect('admin_menu')
        else:

            engine.say("Please select team name")
            engine.runAndWait()
            messages.info(request, 'Please select team name')
            return redirect('delete_player')
    else:

        tms = teams.objects.all()
        pl = player.objects.all()

        return render(request, 'delete_player.html', {'team': tms, 'data': pl})


def delete_team(request):
    engine = pyttsx3.init()
    if request.method == 'POST':
        name = request.POST['team']

        obj = teams.objects.filter(team_name=name)
        obj.delete()
        engine.say("Team is  Successfully Deleted")
        engine.runAndWait()
        messages.info(request, 'Team is  Successfully Deleted')
        return redirect('admin_menu')

    else:
        te = teams.objects.all()
        return render(request, 'delete_team.html', {'de': te})


def team(request):
    te = teams.objects.all()
    return render(request, 'team.html', {'d': te})


def team_create(request):
    engine = pyttsx3.init()
    if request.method == "POST":
        name = request.POST['name']
        no_of_players = request.POST['total']

        if teams.objects.filter(team_name=name).exists():
            engine.say("This Team already exists !!")
            engine.runAndWait()
            messages.info(request, 'This Team already exists !!')
            return redirect('team_create')
        else:
            entry = teams(team_name=name, no_of_players=no_of_players)
            entry.save()
            engine.say("Team is Successfully Created")
            engine.runAndWait()
            messages.info(request, 'Team is Successfully Created')
            return redirect('admin_menu')


    else:
        return render(request, 'team_create.html')


def admin_menu(request):
    return render(request, 'admin_menu.html')


def admins(request):
    engine = pyttsx3.init()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == 'admin':
            if password == 'livescoredbms':
                engine.say("Welcome Admin")
                engine.runAndWait()
                return redirect('admin_menu')
            else:
                engine.say("Password is incorrect Please enter the correct password")
                engine.runAndWait()
                messages.info(request, 'Incorrect Password')
                return redirect('admins')
        else:
            engine.say("Username is not  exist")
            engine.runAndWait()
            messages.info(request, 'Username is not exist')
            return redirect('admins')

    else:
        return render(request, 'admins.html')


def home(request):
    return render(request, 'home.html', {'name': user_name})


user1 = ''


def forgot(request):
    engine = pyttsx3.init()
    if request.method == "POST":
        global user1
        user1 = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        try:
            us = User.objects.get(username=user1)
        except:
            us = None
        if us is None:
            engine.say("Please check you username")
            engine.runAndWait()
            return render(request, 'forgot.html')

        elif pass1 == pass2 and us.email == email:
            us.set_password(pass1)
            us.save()
            auth.login(request, us)
            engine.say("Password Reset Successful")
            engine.runAndWait()
            return redirect('login')
        elif pass1 != pass2:
            engine.say("Password is mismatched")
            engine.runAndWait()
            return redirect('forgot')
        else:
            engine.say("Mismatched username or password")
            engine.runAndWait()
            return redirect('forgot')
    else:
        return render(request, 'forgot.html')


def create_player(request):
    engine = pyttsx3.init()
    if request.method == 'POST':
        team = request.POST['team']
        name = request.POST['name']
        gender = request.POST['gender']
        nation = request.POST['nation']
        to = request.POST['no']

        if name.isalpha():
            if nation.isalpha():
                tm = teams.objects.get(team_name=team)
                print(tm)
                pl = player.objects.all()
                li = []
                for i in pl:
                    if i.teams == tm:
                        li.append(i)
                print(len(li))
                print(tm.no_of_players)
                if tm.no_of_players > len(li):
                    if not player.objects.filter(teams=tm, player_name=name).exists():

                        pla = player(teams=tm, player_name=name, gender=gender, nationality=nation, total_matches=to)
                        pla.save()
                        rank = ranking(teams=tm, player=pla, total_matches=to)
                        rank.save()
                        liv = live(teams=tm, player=pla)
                        liv.save()
                        engine.say("Player Information is added successfully")
                        engine.runAndWait()
                        messages.info(request, 'Player Information is added successfully')
                        return redirect('admin_menu')
                    else:
                        engine.say("Player is already exists")
                        engine.runAndWait()
                        messages.info(request, 'Player is already exists')
                        return redirect('create_player')



                else:
                    engine.say("No of players are exceeded in this team")
                    engine.runAndWait()

                    messages.info(request, 'No of players are exceeded in this team')
                    return redirect('create_player')
            else:
                engine.say("Nation cannot be a integer")
                engine.runAndWait()
                messages.info(request, 'Nation cannot be a integer')
                return redirect('create_player')
        else:
            engine.say("Username cannot be a integer")
            engine.runAndWait()
            messages.info(request, 'Username cannot be a integer')
            return redirect('create_player')

    else:
        tm = teams.objects.all()
        return render(request, 'create_player.html', {'team': tm})


def Live(request):
    de = live.objects.all()
    return render(request, 'live.html', {'data': de})


def Ranking(request):
    pl = player.objects.all()
    te = teams.objects.all()
    li = live.objects.all()
    list1 = []
    for i in pl:
        l = live.objects.get(player=i)
        k = l.total / 4
        rank = ranking.objects.get(player=i)
        rank.average = k
        rank.save()
    rnk = ranking.objects.order_by(Coalesce('average', 'player').desc())
    return render(request, 'ranking.html', {'data': rnk})

user_name = ''

def logout(request):
    auth.logout(request)
    return redirect('login')

def account(request):
    ac = User.objects.get(username=user_name)

    return render(request, 'account.html',{'acc':ac})






def login(request):
    global user_name
    engine = pyttsx3.init()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            engine.say("Login Successfully")
            engine.runAndWait()
            user_name = username

            # messages.info(request,'Login Successfully')
            return redirect('home')
        else:
            engine.say("Username or Password is not exist !!!")
            engine.runAndWait()
            messages.info(request, 'Username or Password is not exist !!!')
            return redirect('login')
    else:
        return render(request, 'login.html')


def register(request):
    engine = pyttsx3.init()
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:

            if User.objects.filter(username=username).exists():
                engine.say("Username is taken.Please select another username ")
                engine.runAndWait()
                messages.info(request, "Username Taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                engine.say("This email is already exists ")
                engine.runAndWait()
                messages.info(request, 'Email Exists')
                return redirect('register')
            elif len(password1) < 8 and len(password2) < 8:
                engine.say("Password length should be 8 or more")
                engine.runAndWait()
                return redirect('register')

            elif username.isdecimal():
                engine.say("Username cannot be integer")
                engine.runAndWait()
                messages.info(request, 'Username cannot be integer')
                return redirect('register')
            elif not first_name.isalpha() or not last_name.isalpha():
                engine.say("Name cannot be integer")
                engine.runAndWait()
                messages.info(request, 'Name cannot be integer')
                return redirect('register')
            else:
                global user_name
                user_name = username
                user = User.objects.create_user(email=email, username=username, password=password1,
                                                first_name=first_name, last_name=last_name)
                user.save();
                engine.say("User is created successfully")
                engine.runAndWait()
                messages.info(request, 'User is created successfully')
                return redirect('home.html')
        else:
            engine.say("Password is not matching")
            engine.runAndWait()
            messages.info(request, 'Password is not matching')
            return render(request, 'register.html')
    else:
        return render(request, 'register.html')
