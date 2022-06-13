from django import forms
from django.db import models
from django.forms import ValidationError
from django.urls import reverse

from fingerprint.views import baixarDigital, salvarDigital


class FingerPrintField(models.CharField):
    def clean(self, value, model_instance):
        if value != '' or value is not None:
            caracteristicas = baixarDigital()
            if caracteristicas == 1:
                raise forms.ValidationError('Não foi possível salvar a digital!')
        return value

class Usuario(models.Model):
    identidade = models.CharField(max_length=64)
    nome = models.CharField(max_length=128)
    senha = models.CharField(max_length=8)
    salvar_digital = FingerPrintField(
        blank=True, max_length=512, help_text='Deixe em branco se não quiser salvar a digital')

    def __str__(self):
        return self.nome + " (" + self.identidade + ")"

    def get_absolute_url(self):
        return reverse("web:usuario_detalhes", args=[self.pk])


class Porta(models.Model):
    nome = models.CharField(max_length=128)
    descricao = models.CharField(max_length=256)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse("web:porta_detalhes", args=[self.pk])


class Permissao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    porta = models.ForeignKey(Porta, on_delete=models.CASCADE)
    impressao_digital = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = 'permissoes'

    def __str__(self):
        return self.usuario + " acessa " + self.porta

    def get_absolute_url(self):
        return reverse("web:permissao_detalhes", args=[self.pk])


class Acesso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    porta = models.ForeignKey(Porta, on_delete=models.CASCADE)
    horario = models.DateTimeField()
    entrada_ou_saida = models.BooleanField(default=True)
    biometria_ou_senha = models.BooleanField(default=True)

    def __str__(self):
        return self.usuario + " acessou " + self.porta + " em " + self.horario

    def get_absolute_url(self):
        return reverse("web:acesso_detalhes", args=[self.pk])
