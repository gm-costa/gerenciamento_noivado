# Generated by Django 5.1.2 on 2024-11-01 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Presente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_presente', models.CharField(max_length=100)),
                ('foto', models.ImageField(upload_to='presentes')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=6)),
                ('importancia', models.PositiveSmallIntegerField()),
                ('reservado', models.BooleanField(default=False)),
            ],
        ),
    ]
