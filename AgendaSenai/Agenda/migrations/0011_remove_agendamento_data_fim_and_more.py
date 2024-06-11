# Generated by Django 5.0.6 on 2024-06-11 19:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Agenda', '0010_rename_foto_sala_foto_sala'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agendamento',
            name='data_fim',
        ),
        migrations.RemoveField(
            model_name='agendamento',
            name='data_inicio',
        ),
        migrations.AddField(
            model_name='agendamento',
            name='data',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]