from django import forms
from django.core.exceptions import ValidationError
from contact.models import Contact
import re

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone', 'category' ]
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'phone': 'Telefone',
            'category': 'Categoria',
        }
        error_messages = {
            'email': {
                'invalid': 'Digite um e-mail válido.',
            },
        }


    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name and last_name and first_name.strip().lower() == last_name.strip().lower():
            self.add_error('last_name', 'O sobrenome não pode ser igual ao primeiro nome.')

        return cleaned_data


    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Remove espaços e formatação antes de validar (opcional)
        phone_cleaned = re.sub(r'\D', '', phone)  # apenas os dígitos
        pattern = r'^(\d{2})9\d{8}$'  # DDD (2) + 9 + 8 dígitos
        
        if not re.match(pattern, phone_cleaned):
            raise ValidationError('Digite um número de telefone válido. Ex: (11) 91234-5678')

        return phone_cleaned
