from django.contrib import admin

# Register your models here.

from stats.models import Player, PowerPlay,PlayerTeam,MiddleOvers,DeathOvers
# Register your models here.
admin.site.register(Player)
admin.site.register(PlayerTeam)
admin.site.register(PowerPlay)
admin.site.register(MiddleOvers)
admin.site.register(DeathOvers)
