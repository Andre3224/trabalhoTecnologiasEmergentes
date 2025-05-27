# Sistema de Login e Registro com Flask e SQLite
## Toledo Prudente Centro Universitário - Disciplina de Tecnologias Emergentes ##
**André Junior S Santos**

Este é um sistema simples de login e registro de usuários desenvolvido em Flask e utilizando um banco de dados SQLite. O sistema permite que os usuários se registrem, façam login e façam logout. Utlizado para entrega de trabalho final da disciplina, no curso de Análise e Desenvolvimento de Sistemas.

### Tecnologias Utilizadas ###
+ Flask: Framework para desenvolvimento de aplicações web em Python.
+ SQLite: Banco de dados leve e simples, utilizado para armazenar as informações dos usuários.

### Funcionalidades ###
+ Registro de Usuário: O usuário pode se cadastrar com um nome de usuário e uma senha.

+ Login: O usuário pode acessar o sistema inserindo o nome de usuário e a senha.

+ Logout: O usuário pode sair da conta a qualquer momento.

+ Validação de Dados: Validação de formulários para garantir que o nome de usuário seja único e a senha esteja segura.

## Pré-requisitos ##
Para rodar esse projeto, você precisa ter o Python e o pip instalados no seu ambiente. Além disso, é necessário instalar as dependências, no linux (Debian) utilize os seguintes comandos no terminal:

sudo apt update 

sudo apt install python3 python3-pip  

No windows e outros sistemas, acesse o site oficial ou o link abaixo:
* https://python.org.br/instalacao-windows/

### Instale o Flask ###
* Terminal: pip install flask werkzeug

## Como Funciona ##

Página de Registro:
- O usuário entra com um nome de usuário e uma senha.
- O sistema valida se o nome de usuário já está registrado. Se não, ele cria um novo usuário e registra a senha de forma segura (com hash).
- Após o registro bem-sucedido, o usuário é redirecionado para a página de login.

Página de Login:
- O usuário entra com seu nome de usuário e senha.
- O sistema valida as credenciais e, se estiverem corretas, cria uma sessão para o usuário.
- Se a autenticação falhar, uma mensagem de erro será exibida.

Página de Logout:
- O usuário pode sair a qualquer momento, e a sessão será limpa.

Para Instalar, clone o repositório ou realize o download dos arquivos, crie uma virtualização (Debian) e rode com o comando:
 - python3 main.py

## Ambiente de Desenvolvimento

### Versões Utilizadas
- **Python:** 3.11.2 (versão mínima suportada: 3.8)
- **Dependências principais:**
  - Flask==2.2.3
