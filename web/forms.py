from django import forms

from web.models import Usuario


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = "__all__"
        widgets = {'senha': forms.PasswordInput(render_value=True)}
