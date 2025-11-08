from django.contrib import admin
from usuarios.models import Usuario

# Register your models here.

#registrando o modelo de usuario
admin.site.register(Usuario)