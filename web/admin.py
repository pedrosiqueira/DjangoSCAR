from django.contrib import admin

from web.forms import UsuarioForm
from web.models import Acesso, Permissao, Porta, Usuario

admin.site.register(Permissao)
admin.site.register(Acesso)


class PermissaoInline(admin.TabularInline):
    model = Permissao


@admin.register(Porta)
class PortaAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    ordering = ['nome']
    inlines = [PermissaoInline]


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    form = UsuarioForm
    inlines = [PermissaoInline]
    ordering = ['nome']
