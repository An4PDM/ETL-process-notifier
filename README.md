# Notificador de processos ETL com Airflow

## Descrição
Este projeto tem como objetivo realizar um processo ETL (Extract, Transform, Load) utilizando o Apache Airflow. O fluxo consiste em extrair dados de um arquivo CSV, realizar transformações nos dados e, em seguida, carregar as informações em um banco de dados MySQL. Além disso, o sistema envia notificações para o Slack e E-mail informando se houve sucesso ou falha no processo.

## Funcionalidades
- Monitoramento de processos ETL.
- Notificação de falhas e sucesso no processo ETL.
- Suporte para múltiplos canais de notificação (Slack, email, etc.).
- Fácil integração com outras ferramentas de monitoramento e notificação.

## Tecnologias Usadas
- **Python:** Linguagem principal utilizada para o desenvolvimento.
- **Apache Airflow:** Usado para orquestrar os processos ETL.
- **Slack API:** Envio de notificações para o canal de Slack.
- **MySQL:** Banco de dados para armazenar os dados transformados.

## Pré-requisitos
- Python 3.7 ou superior.
- Acesso à API de notificações (exemplo: Slack, Email, etc.), caso deseje configurá-las.
- Apache Airflow: O Airflow deve estar instalado e funcionando. Se ainda não o fez, você pode seguir a documentação oficial do Airflow para instalar.
- MySQL Database: Certifique-se de ter um banco de dados MySQL configurado. Altere as credenciais do banco de dados no arquivo config.py.

## Instalação
1. Clone este repositório
```bash
git clone https://github.com/An4PDM/ETL-process-notifier.git
```

2. Instale as dependências
```bash
cd ETL-process-notifier
pip install -r requirements.txt
```

3. Configuração

Configure as variáveis de ambiente no arquivo config.py:

- DB_HOST, DB_NAME, DB_USER, DB_PASSWORD: Credenciais do banco de dados MySQL.
- SLACK_TOKEN: Token de autenticação do Slack.
- SLACK_CHANNEL: ID do canal no Slack onde as mensagens serão enviadas. 

4. Execute o monitoramento
   
Com o código configurado, você pode iniciar o processo de monitoramento e notificação:

```bash
python notifier.py
```

O script irá monitorar os logs do processo ETL e enviará notificações sempre que um evento relevante ocorrer (falha ou sucesso).

### Exemplos de Uso
Envio de Notificação de Falha: Quando o processo ETL falhar, o sistema enviará uma notificação de erro através do canal configurado (Slack, por exemplo).


Envio de Notificação de Sucesso: Quando o processo ETL for concluído com sucesso, uma mensagem de sucesso será enviada para o canal configurado.

![Texto Alternativo](URL_da_Imagem)

## Contribuindo

Se você quiser contribuir para este projeto, sinta-se à vontade para fazer um fork, enviar um pull request ou abrir uma issue. Ficarei feliz em melhorar o código com a ajuda de vocês!

## Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.



