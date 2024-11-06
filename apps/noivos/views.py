from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Convidado, Presente


def home(request):
    if request.method == "POST":
        nome_presente = request.POST.get('nome_presente')
        foto = request.FILES.get('foto')
        preco = request.POST.get('preco')
        importancia = int(request.POST.get('importancia'))

        if not all([nome_presente, foto, preco, importancia]):
            messages.add_message(request, messages.WARNING, 'Preencha todos os campos.')
            return redirect(reverse('home'))
        
        if importancia < 1 or importancia > 5:
            return redirect(reverse('home'))

        presente = Presente(
            nome_presente = nome_presente,
            foto = foto,
            preco = preco,
            importancia=importancia,
        )

        try:
            presente.save()
            messages.add_message(request, messages.SUCCESS, 'Presente cadastrado com sucesso.')
        except Exception as e:
            messages.add_message(request, messages.ERROR, f'Erro: {e}')

        return redirect(reverse('home'))

    else:
        presentes = Presente.objects.all()
        nao_reservado = Presente.objects.filter(reservado=False).count()
        reservado = Presente.objects.filter(reservado=True).count()
        context = {'presentes': presentes, 'data': [nao_reservado, reservado]}

        return render(request, 'home.html', context)

def lista_convidados(request):
    if request.method == 'POST':
        nome_convidado = request.POST.get('nome_convidado')
        whatsapp = request.POST.get('whatsapp')
        maximo_acompanhantes = request.POST.get('maximo_acompanhantes')

        if not all([nome_convidado, whatsapp, maximo_acompanhantes]):
            messages.add_message(request, messages.WARNING, 'Preencha todos os campos.')
            return redirect(reverse('lista_convidados'))

        convidados = Convidado(
            nome_convidado=nome_convidado,
            whatsapp=whatsapp,
            maximo_acompanhantes=int(maximo_acompanhantes)
        )

        try:
            convidados.save()
            messages.add_message(request, messages.SUCCESS, 'Convidado cadastrado com sucesso.')
        except Exception as e:
            messages.add_message(request, messages.ERROR, f'Erro: {e}')

        return redirect(reverse('lista_convidados'))
    
    else:
        convidados = Convidado.objects.all()
        return render(request, 'lista_convidados.html', {'convidados': convidados})