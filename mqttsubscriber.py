import paho.mqtt.client as mqtt
import os

PROJECT_NAME = 'DjangoSCAR'


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("scaruser", "scaruser")
    client.connect("localhost", 1883)
    client.loop_forever()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("scar/acesso")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    from web.models import Acesso

    fields = msg.payload.decode().split(",")
    print(msg.topic, fields)
    Acesso.objects.create(usuario_id=fields[0], porta_id=fields[1], biometria_ou_senha=True if fields[2] else False)


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % PROJECT_NAME)
    import django
    django.setup()
    main()
