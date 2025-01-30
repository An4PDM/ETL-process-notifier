# Notificador de processos ETL com Airflow

## Descrição
O ETL Process Notifier é uma ferramenta desenvolvida para monitorar o andamento de processos ETL (Extract, Transform, Load) e enviar notificações sobre o status de cada etapa do processo. O objetivo é permitir que equipes de dados saibam imediatamente quando ocorrem falhas ou quando o processo de ETL for concluído com sucesso.

## Funcionalidades
- Monitoramento de processos ETL.
- Notificação de falhas e sucesso no processo ETL.
- Suporte para múltiplos canais de notificação (Slack, email, etc.).
- Fácil integração com outras ferramentas de monitoramento e notificação.

## Tecnologias Usadas
- **Python:** Linguagem principal utilizada para o desenvolvimento.
- **Slack API (opcional):** Para envio de notificações no Slack.
- **Bibliotecas de monitoramento de logs:** Para observar e capturar eventos de falhas ou sucessos nos processos ETL.

## Pré-requisitos
- Python 3.7 ou superior.
- Acesso à API de notificações (exemplo: Slack, Email, etc.), caso deseje configurar notificações.

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
O sistema de notificações pode ser configurado através de variáveis de ambiente ou diretamente no código, dependendo da sua escolha de canal de notificação. Veja os detalhes de configuração no arquivo config.py.

Exemplo de configuração com Slack:

```python
# config.py

SLACK_TOKEN = "seu_token_do_slack"
SLACK_CHANNEL = "#canal-de-notificacao"
```

4. Execute o monitoramento
Com o código configurado, você pode iniciar o processo de monitoramento e notificação:

```bash
python notifier.py
```

O script irá monitorar os logs do processo ETL e enviará notificações sempre que um evento relevante ocorrer (falha ou sucesso).

Exemplos de Uso
Envio de Notificação de Falha
Quando o processo ETL falhar, o sistema enviará uma notificação de erro através do canal configurado (Slack, por exemplo).

Envio de Notificação de Sucesso
Quando o processo ETL for concluído com sucesso, uma mensagem de sucesso será enviada para o canal configurado.

## Contribuindo
Contribuições são bem-vindas! Para contribuir, siga os passos abaixo:

- Fork o repositório.
- Crie uma nova branch (git checkout -b feature/feature-name).
- Faça suas alterações e commit (git commit -am 'Adicionando nova feature').
- Envie para a branch principal (git push origin feature/feature-name).
- Abra um Pull Request.

## Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.



