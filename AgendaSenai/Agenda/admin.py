from django.contrib import admin
from .models import Agendamento, Sala, Usuario,Homepage, Agenda, Login

# Register your models here.

admin.site.register(Agendamento)
admin.site.register(Sala)
admin.site.register(Usuario)
admin.site.register(Homepage)
admin.site.register(Agenda)
admin.site.register(Login)
