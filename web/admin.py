from django.contrib import admin

from web.forms import UsuarioForm
from web.models import Acesso, Permissao, Porta, Usuario

admin.site.register(Porta)
admin.site.register(Permissao)
admin.site.register(Acesso)


class PermissaoInline(admin.TabularInline):
    model = Permissao


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    form = UsuarioForm
    inlines = [PermissaoInline]
    ordering = ['nome']
