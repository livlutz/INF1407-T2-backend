from django import forms
from receitas.models import Receita

class ReceitaModel2Form(forms.ModelForm):
    """Formulário para atualização de receitas.

    Args:
        forms (model): cria um formulario baseado no modelo Receita
    """

    # Escolha de visibilidade
    VISIBILIDADE_CHOICES = [
        ('pub', 'Pública'),
        ('priv', 'Privada'),
    ]

    # Campo de escolha de visibilidade
    visibilidade = forms.ChoiceField(
        choices=VISIBILIDADE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Visibilidade da Receita'
    )

    class Meta:
        """Classe de geração de formulário para atualização de receitas.
        """
        model = Receita
        fields = ['titulo', 'foto_da_receita', 'ingredientes', 'modo_de_preparo',
                    'tempo_de_preparo', 'porcoes', 'categoria', 'visibilidade']

        """define widgets para estilizar os campos do formuláro
        """
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título da receita'
            }),
            'ingredientes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Liste os ingredientes da receita'
            }),
            'modo_de_preparo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Descreva o modo de preparo'
            }),
            'tempo_de_preparo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Tempo em minutos'
            }),
            'porcoes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Número de porções'
            }),
            'categoria': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: sobremesa, prato principal'
            }),
            'foto_da_receita': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            })
        }