# Generated by Django 5.0.6 on 2024-05-28 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Agenda', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sala',
            name='capacidade',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='cpf',
            field=models.IntegerField(),
        ),
    ]