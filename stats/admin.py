from django.contrib import admin

# Register your models here.

from stats.models import Player, FantasyPrediction, Form,PowerPlay,PlayerTeam,MiddleOvers,DeathOvers,Matchups,City,Position,AgainstTeam
# Register your models here.
admin.site.register(Player)
admin.site.register(PlayerTeam)
admin.site.register(AgainstTeam)
admin.site.register(PowerPlay)
admin.site.register(MiddleOvers)
admin.site.register(DeathOvers)
admin.site.register(Matchups)
admin.site.register(City)
admin.site.register(Position)
admin.site.register(Form)
admin.site.register(FantasyPrediction)