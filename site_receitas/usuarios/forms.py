from django import forms
from usuarios.models import Usuario
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django.contrib.auth import authenticate

class UsuarioLoginForm(forms.Form):
    """Formulário de login para o modelo Usuario.

    Args:
        forms (forms.Form): Classe base para todos os formulários Django.

    Raises:
        forms.ValidationError: Se as credenciais de login forem inválidas.
        forms.ValidationError: Se as credenciais de login forem inválidas.

    Returns:
        _type_: _user: Retorna o usuário autenticado se as credenciais forem válidas.
    """

    # Campos do formulário

    email = forms.EmailField(label='Email') # Campo de email
    password = forms.CharField(widget=forms.PasswordInput, label='Senha') # Campo de senha

    def clean(self):
        """Valida o formulário de login e verifica as credenciais do usuário para autenticação.

        Raises:
            forms.ValidationError: Se as credenciais de login forem inválidas.
            forms.ValidationError: Se as credenciais de login forem inválidas.

        Returns:
            _type_: _user: Retorna o usuário autenticado se as credenciais forem válidas.
        """
        # Obtém os dados de email e senha limpos do formulário
        cleaned_data = super().clean()

        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        # Verifica se ambos os campos foram preenchidos
        if email and password:
            # Tenta obter o usuário pelo email
            try:
                user = Usuario.objects.get(email=email)

            # Se o usuário não for encontrado, lança um erro de validação
            except Usuario.DoesNotExist:
                raise forms.ValidationError("Email ou senha inválidos")

            # Autentica o usuário com o nome de usuário e senha
            user = authenticate(username=user.username, password=password)

            # Se a autenticação falhar, lança um erro de validação
            if not user:
                raise forms.ValidationError("Email ou senha inválidos")

            # Atualiza o usuário autenticado no formulário
            self.user = user

        # Retorna os dados limpos do formulário
        return cleaned_data


class CustomUserCreationForm(UserCreationForm):
    """Formulário de criação de usuário personalizado.

    Args:
        UserCreationForm (UserCreationForm): Classe base para formulários de criação de usuário do Django.
    """
    class Meta(UserCreationForm.Meta):
        """Define os campos e textos de ajuda para o formulário de criação de usuário.

        Args:
            UserCreationForm (UserCreationForm): Classe base para formulários de criação de usuário do Django.
        """

        model = Usuario

        # Define os campos a serem incluídos no formulário
        fields = ("username", "email", "password1", "password2")

        # Define textos de ajuda personalizados para os campos do formulário
        help_texts = {
            'username': "Escolha um nome único (letras, números e @/./+/-/_).",
            'email': "Usado para recuperação de senha e notificações.",
            'password1': "Sua senha deve ter pelo menos 8 caracteres e não pode ser muito comum.",
            'password2': "Digite a mesma senha para verificação.",
        }

class UsuarioUpdateForm(forms.ModelForm):
    """Formulário de atualização de usuário.

    Args:
        forms (ModelForm): Classe base para formulários de modelo do Django.
    """
    class Meta:
        """Define os campos e widgets para o formulário de atualização de usuário.
        """
        model = Usuario
        # Define os campos a serem incluídos no formulário
        fields = ("username", "email", "foto_de_perfil")

        # Define widgets para estilizar os campos do formulário
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'foto_de_perfil': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

        #define textos de ajuda personalizados para os campos do formulário
        help_texts = {
            'username': "Atualize seu nome de usuário (letras, números e @/./+/-/_).",
            'email': "Atualize seu email para recuperação de senha e notificações.",
            'foto_de_perfil': "Atualize sua foto de perfil.",
        }

