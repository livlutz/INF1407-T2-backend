# INF1407-T2-backend

## 📖 Sobre o Projeto

Sistema de gerenciamento de receitas culinárias desenvolvido com Django REST Framework. O backend fornece uma API completa para criação, edição, visualização e exclusão de receitas, além de um sistema robusto de autenticação e gerenciamento de usuários.

## ✨ Funcionalidades

### Gerenciamento de Receitas
- ✅ Criar novas receitas com detalhes completos
- ✅ Listar receitas públicas
- ✅ Visualizar detalhes de receitas específicas
- ✅ Editar receitas (apenas o autor)
- ✅ Excluir receitas (apenas o autor)
- ✅ Upload de fotos das receitas
- ✅ Controle de visibilidade (pública/privada)
- ✅ Categorização de receitas

### Gerenciamento de Usuários
- ✅ Cadastro de novos usuários
- ✅ Login e logout
- ✅ Visualização de perfil
- ✅ Atualização de perfil
- ✅ Upload de foto de perfil
- ✅ Listagem de receitas do usuário
- ✅ Alteração de senha
- ✅ Recuperação de senha via email
- ✅ Exclusão de conta

### API e Documentação
- ✅ API RESTful completa
- ✅ Documentação Swagger/OpenAPI
- ✅ Suporte a CORS para integração com frontend
- ✅ Autenticação por token

## 🛠️ Tecnologias Utilizadas

- **Django 5.2.6** - Framework web Python
- **Django REST Framework** - Toolkit para construção de APIs REST
- **drf-yasg** - Geração de documentação Swagger/OpenAPI
- **Pillow** - Processamento de imagens
- **django-cors-headers** - Suporte a CORS
- **djangorestframework-authtoken** - Autenticação por token

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Virtualenv (recomendado)

## 🚀 Instalação e Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/livlutz/INF1407-T2-backend.git
cd INF1407-T2-backend
```

### 2. Crie e ative um ambiente virtual

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

```bash
cd site_receitas
python manage.py makemigrations
python manage.py migrate
```

### 5. (Opcional) Crie um superusuário para acessar o admin

```bash
python manage.py createsuperuser
```

### 6. Execute o servidor de desenvolvimento

```bash
python manage.py runserver
```

O servidor estará disponível em `http://localhost:8000`

### Execução Rápida (Script Automatizado)

Alternativamente, você pode usar o script `run.sh` (Linux/macOS):

```bash
chmod +x run.sh
./run.sh
```

## 📚 Estrutura do Projeto

```
INF1407-T2-backend/
├── site_receitas/           # Diretório principal do Django
│   ├── receitas/            # App de receitas
│   │   ├── models.py        # Modelo Receita
│   │   ├── views.py         # Views da API de receitas
│   │   ├── serializers.py   # Serializers para API
│   │   └── urls.py          # URLs de receitas
│   ├── usuarios/            # App de usuários
│   │   ├── models.py        # Modelo Usuario personalizado
│   │   ├── views.py         # Views da API de usuários
│   │   ├── serializers.py   # Serializers para API
│   │   └── urls.py          # URLs de usuários
│   ├── site_receitas/       # Configurações do projeto
│   │   ├── settings.py      # Configurações do Django
│   │   ├── urls.py          # URLs principais
│   │   └── wsgi.py          # WSGI config
│   └── manage.py            # Gerenciador do Django
├── requirements.txt         # Dependências do projeto
└── run.sh                   # Script de execução rápida
```

## 🔌 Endpoints da API

### Receitas

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| GET | `/` | Lista todas as receitas públicas | Não |
| GET | `/receita/<id>/` | Visualiza uma receita específica | Não |
| POST | `/criar_receita/` | Cria uma nova receita | Sim |
| PUT | `/editar_receita/<id>/` | Edita uma receita | Sim (apenas autor) |
| DELETE | `/deletar_receita/<id>/` | Exclui uma receita | Sim (apenas autor) |

### Usuários

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| POST | `/login/` | Realiza login | Não |
| POST | `/logout/` | Realiza logout | Sim |
| POST | `/cadastro/` | Cadastra novo usuário | Não |
| GET | `/perfil/<id>/` | Visualiza perfil de usuário | Sim |
| PUT | `/perfil/atualizar/<id>/` | Atualiza perfil | Sim (próprio usuário) |
| DELETE | `/perfil/deletar/<id>/` | Exclui conta | Sim (próprio usuário) |
| GET | `/perfil/receitas/<id>/` | Lista receitas do usuário | Sim |
| POST | `/password_change/` | Altera senha | Sim |

### Documentação

| Endpoint | Descrição |
|----------|-----------|
| `/swagger/` | Documentação Swagger da API de Receitas |
| `/docs/` | Documentação interativa da API |
| `/admin/` | Painel administrativo do Django |

## 📝 Modelo de Dados

### Receita

```python
- id: Identificador único (autoincremental)
- titulo: Título da receita (máx. 200 caracteres)
- ingredientes: Lista de ingredientes (texto)
- modo_de_preparo: Instruções de preparo (texto)
- tempo_de_preparo: Tempo em minutos (inteiro)
- porcoes: Número de porções (inteiro)
- categoria: Categoria da receita (máx. 100 caracteres)
- foto_da_receita: Imagem da receita (opcional)
- visibilidade: 'pub' (pública) ou 'priv' (privada)
- autor: Referência ao usuário criador (ForeignKey)
```

### Usuário

```python
- id: Identificador único (autoincremental)
- username: Nome de usuário (único)
- email: Email do usuário (único)
- password: Senha (hash)
- foto_de_perfil: Foto de perfil (opcional)
- first_name: Primeiro nome (opcional)
- last_name: Sobrenome (opcional)
```

## 🔐 Autenticação

O sistema utiliza autenticação por token do Django REST Framework. Para acessar endpoints protegidos:

1. Faça login através do endpoint `/login/`
2. Inclua o token recebido no header das requisições:
   ```
   Authorization: Token <seu-token-aqui>
   ```

## 🌐 Configuração de CORS

O projeto está configurado para aceitar requisições de origens específicas. Para adicionar novas origens permitidas, edite o arquivo `site_receitas/site_receitas/settings.py`:

```python
CSRF_TRUSTED_ORIGINS = [
    'https://seu-dominio.com',
    'http://localhost:8080',
]
```

## 📦 Arquivos de Media

As imagens enviadas (fotos de receitas e perfis) são armazenadas no diretório `media/`:
- Fotos de receitas: `media/receitas/img/`
- Fotos de perfil: `media/usuarios/img/`

## 🧪 Testes

Para executar os testes do projeto:

```bash
cd site_receitas
python manage.py test
```

## 🚀 Deploy

### Configurações de Produção

Antes de fazer deploy em produção, certifique-se de:

1. Definir `DEBUG = False` em `settings.py`
2. Configurar `ALLOWED_HOSTS` com seu domínio
3. Gerar uma nova `SECRET_KEY` segura
4. Configurar um banco de dados de produção (PostgreSQL recomendado)
5. Configurar servidor de arquivos estáticos e de media
6. Configurar HTTPS

### Variáveis de Ambiente Recomendadas

```bash
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos como parte da disciplina INF1407.

## 👥 Autores

- Desenvolvido por estudantes da disciplina INF1407

## 📞 Contato

Para dúvidas ou sugestões, entre em contato através do email: contato@receitas.com

---

**Nota:** Este é um projeto acadêmico desenvolvido para aprendizado de desenvolvimento web com Django e APIs REST.