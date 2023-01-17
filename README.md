# Cliente de email
 **Trabalho de redes, com utilização de socket. Cliente IMAP e cliente SMTP** 

O script começa pedindo que o usuário entre com seu e-mail e senha e tenta fazer login tanto na conta IMAP quanto SMTP. Caso o login não seja bem-sucedido, ele continua pedindo as credenciais até que sejam válidas.

#
**Uma vez logado, o usuário é apresentado com as seguintes opções:**

* Ver E-mails: permite visualizar e gerenciar as mensagens na caixa de entrada
* Ver Lixeira: permite visualizar e gerenciar as mensagens na lixeira
* Enviar E-mail: permite enviar novos e-mails
* Fazer Logout: permite fazer logout da conta de e-mail

#
As funcionalidades de visualização de e-mails (inbox e lixeira) permitem ao usuário escolher uma mensagem para abrir, visualizar seu conteúdo e ter as opções de responder ou excluir a mensagem. A funcionalidade de envio de e-mails pede destinatário, assunto e corpo do e-mail.

Além disso, o código também inclui funções auxiliares para listagem de cabeçalhos, visualização de e-mails, exclusão de e-mails e resposta de e-mails.
