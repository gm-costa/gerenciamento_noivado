# Generated by Django 5.1.2 on 2024-11-02 02:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noivos', '0002_convidado'),
    ]

    operations = [
        migrations.AddField(
            model_name='presente',
            name='reservado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='noivos.convidado'),
        ),
    ]
