from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from contact.models import Contact
import re

class ContactForm(forms.ModelForm):

    picture = forms.ImageField(
        label='Imagem',
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
            }     
        ),
        required=False,
    )

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone', 'category','picture' ]
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'phone': 'Telefone',
            'category': 'Categoria',
            'picture': 'Imagem',
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


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3,
        max_length=30,
    )    
    last_name = forms.CharField(
        required=True,
        min_length=3,
        max_length=30,
    )
    email = forms.CharField(
        required=True,
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email','username', 'password1', 'password2']
        labels = {
             'username': 'Usuário',
             'first_name': 'Nome',
             'last_name': 'Sobrenome',
             'email': 'E-mail',}
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Este e-mail já está cadastrado.', code='invalid')
            ) 
        return email
    
class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=3,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Por favor, insira mais de 2 letras'
        }
    )
    last_name = forms.CharField(
        min_length=3,
        max_length=30,
        required=True,
        help_text='Required.'
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Password 2",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use the same password as before.',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username',
        )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Senhas não batem')
                )

        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError('Já existe este e-mail', code='invalid')
                )

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )

        return password1