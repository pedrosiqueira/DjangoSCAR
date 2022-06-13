from django.contrib import admin

from web.models import Acesso, Permissao, Porta, Usuario

admin.site.register(Usuario)
admin.site.register(Porta)
admin.site.register(Permissao)
admin.site.register(Acesso)
