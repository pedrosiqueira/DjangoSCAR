import paho.mqtt.publish as publish
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from web.models import Permissao, Usuario


@receiver([post_delete], sender=Permissao)
def permissoes_deleted(sender, instance, **kwargs):
    topic = "scar/portas/"+str(instance.porta.pk)+"/usuarios/delete"
    msg = instance.usuario.pk
    publish.single(topic, msg, hostname="localhost", port=1883, auth={'username': "scaruser", 'password': 'scaruser'})


@receiver([post_delete], sender=Usuario)
def usuarios_deleted(sender, instance, **kwargs):
    permissoes = Permissao.objects.filter(usuario=instance)
    for permissao in permissoes:
        topic = "scar/portas/"+str(permissao.porta.pk)+"/usuarios/delete"
        msg = instance.pk
        publish.single(topic, msg, hostname="localhost", port=1883, auth={'username': "scaruser", 'password': 'scaruser'})
