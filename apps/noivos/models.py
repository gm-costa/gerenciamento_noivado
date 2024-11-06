import secrets
from django.db import models
from django.urls import reverse


class Convidado(models.Model):
    status_choices = (
        ('A', 'Aguardando confirmação'),
        ('C', 'Confirmado'),
        ('R', 'Recusado')
    )

    nome_convidado = models.CharField(max_length=100)
    whatsapp = models.CharField(max_length=25, blank=True, null=True)
    maximo_acompanhantes = models.PositiveIntegerField(default=0)
    token = models.CharField(max_length=25)
    status = models.CharField(max_length=1, choices=status_choices, default='A')

    def __str__(self):
        return self.nome_convidado

    @property
    def link_convite(self):
        return f'http://127.0.0.1:8000{reverse("convidados")}?token={self.token}'
    
    @property
    def status_color(self):
        color = ''
        if self.status == 'A':
            color = 'indigo'
        elif self.status == 'C':
            color = 'green'
        else:
            color = 'red'

        return color

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(16)
        super(Convidado, self).save(*args, **kwargs)


class Presente(models.Model):
    nome_presente = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='presentes')
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    importancia = models.PositiveSmallIntegerField()
    reservado = models.BooleanField(default=False)
    reservado_por = models.ForeignKey(Convidado, null=True, blank=True, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.nome_presente


class Acompanhante(models.Model):
    nome = models.CharField(max_length=100)
    convidado = models.ForeignKey(Convidado, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nome
