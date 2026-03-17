# Bottrader

Este repositório contém o código-fonte de um robô de trading automatizado, desenvolvido para monitorar o mercado de criptomoedas e enviar alertas com base em padrões técnicos específicos. O Bottrader utiliza a biblioteca `ccxt` para interagir com a exchange Binance e `pandas` para análise de dados.

## Funcionalidades

*   **Conexão com Binance**: Utiliza a API da Binance para obter dados de mercado.
*   **Detecção de Padrões**: Implementa a detecção de padrões como Rally-Base-Rally (RBR) e Break of Structure (BoS).
*   **Alertas via Telegram**: Envia notificações em tempo real para um chat do Telegram quando padrões são detectados.
*   **Configurável**: Parâmetros como chaves de API, símbolos de trading e timeframe são facilmente configuráveis.

## Estrutura do Projeto

```
Bottrader/
├── main.py
├── config.py
├── patterns.py
├── bos.py
├── telegram_alert.py
└── requirements.txt
```

*   `main.py`: O script principal que orquestra a coleta de dados, detecção de padrões e envio de alertas.
*   `config.py`: Contém as chaves de API da Binance, símbolos de trading e o timeframe.
*   `patterns.py`: Módulo com a lógica para detecção de padrões técnicos (RBR).
*   `bos.py`: Módulo com a lógica para detecção de Break of Structure (BoS).
*   `telegram_alert.py`: Módulo responsável por enviar mensagens para o Telegram.
*   `requirements.txt`: Lista de dependências Python necessárias para o projeto.

## Configuração Segura (GitHub Secrets)

Por motivos de segurança, o **Bottrader** está configurado para ler suas chaves da Binance de **variáveis de ambiente**. 

### No Ambiente Local (Desenvolvimento)
Você pode exportar as chaves no seu terminal antes de rodar o bot:
```bash
export BINANCE_API_KEY='sua_chave_aqui'
export BINANCE_SECRET='seu_secret_aqui'
```

### No GitHub (Produção/CI)
Vá em **Settings > Secrets and variables > Actions** e adicione:
- `BINANCE_API_KEY`
- `BINANCE_SECRET`

## Modo TestNet (Sandbox)
O bot está configurado por padrão para rodar no modo **TestNet (Sandbox)** da Binance. Isso permite testar a estratégia sem usar dinheiro real.
Para desativar o TestNet e operar na conta real, altere no `config.py`:
```python
BINANCE_TESTNET = False
```

## Configuração Básica

1.  **Clonar o repositório**:
    ```bash
    git clone https://github.com/ProjethusHO/Bottrader.git
    cd Bottrader
    ```

2.  **Instalar dependências**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurar Símbolos e Moeda**:
    No `config.py`, você pode ajustar a moeda base e os pares de trading.
    ```python
    BASE_CURRENCY = 'BRL'
    SYMBOLS = ['BTC/BRL', 'ETH/BRL']
    ```

4.  **Configurar `telegram_alert.py`**:
    Abra o arquivo `telegram_alert.py` e preencha o token do seu bot do Telegram e o ID do chat.
    ```python
    TELEGRAM_BOT_TOKEN = 'SEU_BOT_TOKEN_TELEGRAM'
    TELEGRAM_CHAT_ID = 'SEU_CHAT_ID_TELEGRAM'
    ```
    Para obter o `TELEGRAM_BOT_TOKEN`, você pode conversar com o BotFather no Telegram. Para obter o `TELEGRAM_CHAT_ID`, você pode usar o bot `@get_id_bot`.

## Execução no Windows (Recomendado)

Para facilitar o uso no Windows, utilize o arquivo `iniciar_bot.bat`. Ele configura as chaves de API do TestNet automaticamente e inicia o robô.

1.  Dê um clique duplo em `iniciar_bot.bat`.
2.  O navegador abrirá uma tirinha do Python (via `antigravity`) e o robô começará a monitorar o mercado no terminal.

## Execução Manual

Para iniciar o Bottrader manualmente, execute o script `main.py`:

```bash
python main.py
```

O robô irá rodar em um loop contínuo, verificando os padrões a cada 60 segundos e enviando alertas para o Telegram quando um padrão for detectado.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues para sugestões ou reportar bugs, e enviar pull requests com melhorias ou novas funcionalidades.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes. (Nota: O arquivo LICENSE não está incluído neste repositório, mas pode ser adicionado se desejado.)
