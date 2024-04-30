from django.contrib import admin
from .models import sell
from .models import voitures
from .models import Prix

# Register your models here.
admin.site.register(sell)
admin.site.register(voitures)
admin.site.register(Prix)