# Projeto---PSI
Plataforma para armazenar projetos acadêmicos

1. Cadastro e Autenticação
RF01: Usuário poderá criar conta com e-mail e senha.
RF02: Usuário poderá fazer login e logout.
RF03: Senhas deverão ser armazenadas com hash seguro.
RF04: Validação dos dados no formulário (e-mail válido, senha com no mínimo 6 caracteres). (Recomendado)
RF05: Redirecionamento automático para o login após o cadastro ser realizado com sucesso. (Opcional)

2. Gerenciamento de Projetos (Recurso)
RF06: Usuário autenticado poderá criar projetos.
RF07: Usuário autenticado poderá listar projetos.
RF08: Usuário autenticado poderá editar seus próprios projetos.
RF09: Usuário autenticado poderá excluir seus próprios projetos.
RF10: Acesso restrito às funcionalidades para usuário logado.

3. Banco de Dados
RF11: Utilizar SQLite para armazenar usuários e dados dos projetos.

4. Templates
RF12: Utilizar extends/includes para estruturação do layout.
RF13: Criar páginas de erro personalizadas (ex: 404, 500).
RF14: Utilizar blocos ({% block %}) para separar conteúdo, títulos e scripts.
RF15: Inserir mensagens visuais com flash() para feedback ao usuário.
RF16: Uso de ícones (ex: Font Awesome) para interface amigável.
RF17: Templates acessíveis: uso de atributos alt em imagens, bom contraste e legibilidade.
RF18: Aplicar tema com cores e logo do IFRN – Campus Caicó. (Opcional)

5. Requisitos Técnicos
RF19: Utilizar sessões (session) para manter usuário autenticado.
RF20: Utilizar cookies para salvar preferências do usuário. (Opcional)
RF21: Utilizar funções request, redirect, url_for e make_response do framework web.
RF22: Código versionado no GitHub com entregas semanais.
RF23: Documentar o projeto com README contendo instruções de uso.
RF24: Realizar testes manuais das funcionalidades principais. (Recomendado)
