from django.urls import path
from . import views
urlpatterns = [
    path('',views.preview,name='preview'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('home.html', views.home,name='home'),
    path('live.html',views.Live,name='Live'),
    path('data',views.Live,name='Live'),
    path('ranking.html',views.Ranking,name='Ranking'),
    path('create_player',views.create_player,name='create_player'),
    path('account.html',views.account,name='account'),
    path('admins',views.admins,name='admins'),
    path('team',views.team,name='team'),
    path('team_create',views.team_create,name='team_create'),
    path('delete_team',views.delete_team,name='delete_team'),
    path('admin_menu',views.admin_menu,name='admin_menu'),
    path('delete_player',views.delete_player,name='delete_player'),
    path('players',views.players,name='players'),
    path('add_live',views.add_live,name='add_live'),
    path('forgot',views.forgot,name='forgot'),
    path('logout',views.logout,name='logout')
]



