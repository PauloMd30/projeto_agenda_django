from django.shortcuts import render, redirect, get_object_or_404
from contact.forms import ContactForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from contact.models import Contact





@login_required(login_url='contact:login')
def create(request):
    form_action = reverse('contact:create')
    
    if request.method == 'POST' :
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            return redirect('contact:index') #contact_id=contact.id)

    else:
        form = ContactForm()
        
    context = {
        'form': form,
        'form_action': form_action,
        'site_title': 'Crie seu Contato - ',
        
    }
    return render(request, 'contact/create.html', context)

@login_required(login_url='contact:login')
def update(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, show=True, owner=request.user)
    form_action = reverse('contact:update', args=[contact_id])

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            contact = form.save()
            return redirect('contact:update', contact_id=contact.id)
    else:
        form = ContactForm(instance=contact)

    context = {
        'form': form,
        'form_action': form_action,
        'site_title': 'Atualize seu Contato - ',
    }

    return render(request, 'contact/create.html', context)

@login_required(login_url='contact:login')
def delete(request, contact_id):
    contact = get_object_or_404(
        Contact, id=contact_id, show=True, owner=request.user
    )
    confirmation = request.POST.get('confirmation', 'no')

    if confirmation == 'yes':
        contact.delete()
        return redirect('contact:index')

    return render(
        request,
        'contact/contact.html',
        {
            'contact': contact,
            'confirmation': confirmation,
        }
    )