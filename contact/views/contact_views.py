from django.http import Http404
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect



from contact.models import Contact

# Create your views here.
def index(request):
    contacts = Contact.objects.filter(show=True).order_by('-created_date')

    context = {
        'contacts': contacts,
        'site_title': 'Lista de Contatos - ',
    }

    return render(request, 'contact/index.html', context)

def search(request):
    search_query = request.GET.get('q', '').strip()

    if search_query == '':
        return redirect('contact:index')

    contacts = Contact.objects \
        .filter(show=True)\
        .filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )\
        .order_by('-created_date')

    context = {
        'contacts': contacts,
        'site_title': 'Pesquisar - ',
    }

    return render(request, 'contact/index.html', context)


def contact(request, contact_id):
    
    single_contact = get_object_or_404(Contact, id=contact_id, show=True)

    contact_name = f'{single_contact.first_name} {single_contact.last_name} - ' 

    context = {
        'contact': single_contact,
        'site_title': contact_name,
    }

    return render(request, 'contact/contact.html', context)