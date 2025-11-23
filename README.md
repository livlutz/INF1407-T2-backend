# Receitinhas da Vovó
## Segundo trabalho de Programação para a Web (INF1407) - 2025.2
## BACKEND

![Contributors](https://img.shields.io/github/contributors/livlutz/INF1407-T1)
![Python](https://img.shields.io/badge/python-3670A0?style=plastic&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=plastic&logo=django&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=plastic&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/css-%231572B6.svg?style=plastic&logo=css3&logoColor=white)
![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=plastic&logo=gnu-bash&logoColor=white)

## 👥 Membros da Dupla

| Nome | Matrícula |
|------|-----------|
| **Lívia Lutz dos Santos** | 2211055 |
| **Luiza Marcondes Paes Leme** | 2210275 |

---

## Escopo do Projeto

Receitinhas da Vovó é uma plataforma web completa para compartilhamento de receitas culinárias, desenvolvida com Django, TypeScript/JavaScript e Swagger. O projeto implementa um sistema de gerenciamento de usuários e receitas. Para esse trabalho, o frontend e o backend estão em repositórios separados.

## Frontend

Disponível no repositório: https://github.com/livlutz/INF1407-T2-frontend

### 🌟 O que funcionou

#### Sistema de Usuários
- ✅ Cadastro de usuários 
- ✅ Sistema de login e logout
- ✅ Perfil personalizado com foto de perfil
- ✅ Edição de dados pessoais
- ✅ Exclusão de conta com confirmação

#### Gerenciamento de Receitas
- ✅ Criação de receitas
- ✅ Controle de visibilidade (público/privado)
- ✅ Edição de receitas
- ✅ Exclusão de receitas com confirmação
- ✅ Visualização detalhada de receitas

#### Interface e Experiência
- ✅ Navegação intuitiva entre páginas (Nav-bar com autenticação)
- ✅ Formulários com validação
- ✅ Feedback visual para ações do usuário

---

## O que não funcionou

- Conforme as especificações do trabalho no enunciado, não houve nenhuma funcionalidade que testamos e não funcionou


## 🚀 Instalação e Configuração Local

### Instalação Automática

```bash
./run.sh
```
### Conexão com front

Após abrir a porta do backend, ir na aba Portas e mudar a visibilidade para pública. 

Incluir endereço do frontend no CORS_ORIGIN_WHITELIST do settings.py se for rodar em um codespace próprio.

Para abrir o site, vá para o repositório do frontend.

## 📚 Manual do Usuário

### 🏠 Página Inicial
A página inicial apresenta todas as receitas públicas disponíveis e botões de homepage, login e cadastro.

### 👤 Sistema de Usuários

#### Cadastro de Novo Usuário
1. Clique em **"Cadastrar"** no menu superior
2. Preencha os campos obrigatórios
3. Opcionalmente, adicione uma foto de perfil
4. Clique em **"Cadastrar"** para criar a conta

#### Login
1. Clique em **"Login"** no menu superior
2. Insira seu email e senha
3. Clique em **"Login"** para acessar sua conta
4. Caso tenha esquecido sua senha ou errado sua senha, clique em **Esqueceu a senha?** (ainda não implementado)
5. Caso não tenha uma conta, clique em **Cadastre-se!** 

#### Gerenciamento de Perfil
- **Perfil**: Acesse através do menu superior após fazer login
- **Editar Dados**: Clique em "Atualizar Perfil" no seu perfil para modificar informações
- **Deletar Conta**: Clique em "Deletar Conta" para deletar sua conta com confirmação
- **Trocar senha**: Clique em "Trocar Senha" para trocar a senha da sua conta
- **Ver receitas**: Clique em "Minhas Receitas" para ver as receitas criadas pelo seu usuário, incluindo as privadas - Você pode clicar em cada receita para vê-la, editar ou excluir
- **Criar receitas**: Clique em "Criar Receita" para criar uma receita

### 🍳 Gerenciamento de Receitas

#### Criar Nova Receita
1. Faça login na sua conta
2. Clique em **"Criar Receita"**
3. Preencha todos os campos obrigatórios
4. Defina a visibilidade (Pública ou Privada)
5. Opcionalmente, adicione uma foto da receita
6. Clique em **"Salvar"** para publicar

#### Visualizar Receitas
- **Receitas Próprias**: Acesse através do seu perfil
- **Receitas Públicas**: Disponíveis na página inicial (incluindo as suas públicas)
- **Detalhes**: Clique em qualquer receita para ver informações completas

#### Editar Receitas
1. Acesse sua receita através do perfil ou a partir da homepage clicando em receitas cujo autor é o seu usuário
2. Clique no botão **"Editar"**
3. Modifique os campos desejados
4. Salve as alterações

#### Excluir Receitas
1. Acesse sua receita
2. Clique no botão **"Excluir"**
3. Confirme a exclusão (ação irreversível)

### 🔒 Controle de Privacidade
- **Receitas Públicas**: Visíveis para todos os usuários
- **Receitas Privadas**: Visíveis apenas para o autor
