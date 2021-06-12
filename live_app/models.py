from django.db import models as mo

class teams(mo.Model):

    team_name = mo.CharField(max_length=5, default='')
    no_of_players = mo.IntegerField(default=0)

    def __str__(self):
        return self.team_name

class player(mo.Model):

    teams=mo.ForeignKey(to=teams,on_delete=mo.CASCADE,default='')
    player_name = mo.CharField(max_length=15,default='')
    gender = mo.CharField(max_length=20,default='')
    nationality = mo.CharField(max_length=10, default='')
    total_matches = mo.IntegerField(default=0)

    def __str__(self):
        return self.player_name

class ranking(mo.Model):

    teams = mo.ForeignKey(to=teams, on_delete=mo.CASCADE)
    player = mo.ForeignKey(to=player, on_delete=mo.CASCADE)
    average = mo.FloatField(default=0)
    total_matches = mo.IntegerField(default=0)
    def __str__(self):
        return str(self.average)

class live(mo.Model):
    teams = mo.ForeignKey(to=teams, on_delete=mo.CASCADE)
    player = mo.ForeignKey(to=player, on_delete=mo.CASCADE)

    hole1 = mo.IntegerField(default=0)
    hole2 = mo.IntegerField(default=0)
    hole3 = mo.IntegerField(default=0)
    hole4 = mo.IntegerField(default=0)
    total = mo.IntegerField(default=0)
    winner = mo.FloatField(default=0)
    def __str__(self):
        return self.player.player_name
