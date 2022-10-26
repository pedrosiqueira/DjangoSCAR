import paho.mqtt.publish as publish
from django import forms
from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse
from fingerprint.views import baixarDigital


def getFieldsValues(instance):
    fields = {}
    for field in instance.__class__._meta.get_fields():
        try:
            fields[field.name] = getattr(instance, field.name)
        except Exception as ex:  # Catch field does not exist exception
            pass
    return fields


def toMQTTMessage(instance):
    message = ""
    for field in instance.__class__._meta.get_fields():
        try:
            message += str(getattr(instance, field.name))+","
        except Exception as ex:  # Catch field does not exist exception
            pass
    return message


class FingerPrintField(models.CharField):
    def clean(self, value, model_instance):
        if value != '' or value is not None:
            caracteristicas = baixarDigital()
            if caracteristicas == 1:
                raise forms.ValidationError('Não foi possível salvar a digital!')
        return value  # #todo retornar caracteristicas compactada


class Usuario(models.Model):
    identidade = models.CharField(max_length=64, unique=True)
    nome = models.CharField(max_length=128)
    senha = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9999)])
    impressao_digital = FingerPrintField(blank=True, max_length=512, help_text='Deixe em branco se não quiser salvar a digital')

    def __str__(self):
        return self.nome + " (" + self.identidade + ")"

    def get_absolute_url(self):
        return reverse("web:usuario_detalhes", args=[self.pk])

    def save(self, *args, **kwargs):
        """Identify the changed fields https://stackoverflow.com/a/55005137/4072641"""
        fields = {}
        if self.pk:  # If self.pk is not None then it's an update.
            fields = getFieldsValues(self.__class__.objects.get(pk=self.pk))
        super().save(*args, **kwargs)  # só depois salvar no banco que posso enviar os dados para as portas
        send = False  # se não houve mudanças, ou usuário acabou de se cadastrar, não envia para as portas
        for field in fields:
            try:
                if fields[field] != getattr(self, field):  # se algum campo de fato foi modificado
                    send = True
                    break
            except Exception as ex:  # Catch field does not exist exception
                pass

        if send:  # envia para cada porta que tem o usuário cadastrado
            permissoes = Permissao.objects.filter(usuario=self)
            for permissao in permissoes:
                topic = "scar/portas/"+str(permissao.porta.pk)+"/usuarios/update"
                msg = toMQTTMessage(self)
                publish.single(topic, msg, hostname="localhost", port=1883, auth={'username': "scaruser", 'password': 'scaruser'})
                fields = permissoes = None


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

    class Meta:
        verbose_name_plural = 'permissoes'
        unique_together = ("usuario", "porta")

    def __str__(self):
        return str(self.usuario) + " acessa " + str(self.porta)

    def get_absolute_url(self):
        return reverse("web:permissao_detalhes", args=[self.pk])

    def save(self, *args, **kwargs):
        """Identify the changed fields https://stackoverflow.com/a/55005137/4072641"""
        fields = {}
        if self.pk:  # If self.pk is not None then it's an update.
            fields = getFieldsValues(self.__class__.objects.get(pk=self.pk))  # get old fields values
        super().save(*args, **kwargs)
        topic = "scar/portas/"+str(self.porta.pk)+"/usuarios/add"
        msg = toMQTTMessage(self.usuario)
        publish.single(topic, msg, hostname="localhost", port=1883, auth={'username': "scaruser", 'password': 'scaruser'})
        if fields != {}:
            topic = "scar/portas/"+str(fields['porta'].pk)+"/usuarios/delete"
            msg = fields['usuario'].pk
            publish.single(topic, msg, hostname="localhost", port=1883, auth={'username': "scaruser", 'password': 'scaruser'})


class Acesso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    porta = models.ForeignKey(Porta, on_delete=models.CASCADE)
    horario = models.DateTimeField()
    biometria_ou_senha = models.BooleanField(default=True)

    def __str__(self):
        return str(self.usuario) + " acessou " + str(self.porta) + " em " + str(self.horario)

    def get_absolute_url(self):
        return reverse("web:acesso_detalhes", args=[self.pk])
