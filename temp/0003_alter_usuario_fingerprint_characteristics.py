# Generated by Django 4.0.5 on 2022-06-11 21:53

from django.db import migrations, models
import web.models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_alter_permissao_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='fingerprint_characteristics',
            field=models.CharField(max_length=512, null=True, validators=[web.models.validar_impressao_digital]),
        ),
    ]
