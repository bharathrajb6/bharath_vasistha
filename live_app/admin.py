from django.contrib import admin



from .models import player
from .models import ranking
from .models import teams
from .models import live

# Register your models here.
admin.site.register(player)
admin.site.register(teams)
admin.site.register(ranking)
admin.site.register(live)


