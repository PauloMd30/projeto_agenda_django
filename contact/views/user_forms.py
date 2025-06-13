from contact.forms import RegisterForm, RegisterUpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm




def register(request):
    form = RegisterForm()

    if request.method == 'POST' :
        form = RegisterForm(request.POST)
        if form.is_valid():
            form = form.save()
            messages.success(
                request,
                'Usuário registrado com sucesso!'
            )
            return redirect('contact:login')

    return render(
        request,
        'contact/register.html',
        {
            'form': form,
            'site_title': 'Registrar Usuário - ',
        })

@login_required(login_url='contact:login')
def user_update(request):
    form = RegisterUpdateForm(instance=request.user)
    if request.method == 'POST':
        form = RegisterUpdateForm(
            request.POST,
            instance=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Usuário atualizado com sucesso!'
            )
            return redirect('contact:index')
        else:
            messages.error(
                request,
                'Erro ao atualizar usuário.'
            )
    return render(
        request,
        'contact/user_update.html',
        {
            'form': form,
            'site_title': 'Atualizar Perfil - ',
        })

def login_view(request):
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(
                request,
                'Login realizado com sucesso!'
            )
            return redirect('contact:index')
        else:
            messages.error(
                request,
                'Usuário ou senha inválidos.'
            )
                

    return render(
        request,
        'contact/login.html',
        {
            'form': form,
            'site_title': 'Registrar Usuário - ',
        })

@login_required(login_url='contact:login')
def logout_view(request):
    auth.logout(request)
    messages.success(
        request,
        'Saída realizado com sucesso!'
    )
    return redirect('contact:login')