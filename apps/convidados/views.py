from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from noivos.models import Convidado, Presente, Acompanhante


def convidados(request):
    token = request.GET.get('token')
    convidado = Convidado.objects.get(token=token)
    if convidado.status == 'R':
        messages.add_message(request, messages.INFO, f'{convidado.nome_convidado} recusou o convite.')
        return redirect(reverse('lista_convidados'))
    
    presentes = Presente.objects.filter(reservado=False).order_by('-importancia')
    acompanhantes = Acompanhante.objects.filter(convidado=convidado)
    context = {
        'convidado': convidado,
        'presentes': presentes,
        'token': token,
        'acompanhantes': acompanhantes
    }

    return render(request, 'convidados.html', context)

def definir_presenca(request):
    resposta = request.GET.get('resposta')
    token = request.GET.get('token')
    convidado = Convidado.objects.get(token=token)
    if resposta not in ['C', 'R']:
        messages.add_message(request, messages.WARNING, 'Resposta inválida, você deve confirmar ou recusar')
        return redirect(f'{reverse('convidados')}?token={token}')
    
    try:
        convidado.status = resposta
        convidado.save()
        if resposta == 'R':
            messages.add_message(request, messages.INFO, f'{convidado.nome_convidado} recusou o convite.')
            return redirect(reverse('lista_convidados'))
        
    except Exception as e:
        messages.add_message(request, messages.ERROR, f'Erro: {e}')

    return redirect(f'{reverse('convidados')}?token={token}')

def reservar_presente(request, id):
    token = request.GET.get('token')

    convidado = Convidado.objects.get(token=token)
    presente = Presente.objects.get(id=id)

    try:
        presente.reservado=True
        presente.reservado_por = convidado
        presente.save()
        messages.add_message(request, messages.SUCCESS, 'Presente reservado com sucesso.')

    except Exception as e:
        messages.add_message(request, messages.ERROR, f'Erro: {e}')

    return redirect(f'{reverse('convidados')}?token={token}')


def adicionar_acompanhante(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        token = request.POST.get('token-convidado')
        convidado = Convidado.objects.get(token=token)

        if len(nome.strip()) == 0:
            messages.add_message(request, messages.WARNING, 'Nome do acompanhante não informado !')
            return redirect(f'{reverse('convidados')}?token={token}')
        
        if Acompanhante.objects.filter(convidado=convidado).count() < convidado.maximo_acompanhantes:
            acompanhante = Acompanhante(nome=nome.strip(), convidado=convidado)
            try:
                acompanhante.save()
                messages.add_message(request, messages.SUCCESS, 'Acompanhante cadastro com sucesso.')
            except Exception as e:
                messages.add_message(request, messages.ERROR, f'Erro: {e}')

        else:
            messages.add_message(request, messages.WARNING, 'Seu limite de acompanhantes foi atingido !')

        return redirect(f'{reverse('convidados')}?token={token}')
