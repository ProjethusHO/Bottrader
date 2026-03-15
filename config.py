import os

# Configurações da Binance (Lendo de variáveis de ambiente por segurança)
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', 'YOUR_BINANCE_API_KEY')
BINANCE_SECRET = os.getenv('BINANCE_SECRET', 'YOUR_BINANCE_SECRET')

# Configurações de Mercado
TIMEFRAME = '1h'
SYMBOLS = ['BTC/BRL', 'ETH/BRL', 'SOL/BRL']

# Configurações de Trading
TRADING_ENABLED = False  # Alterar para True para habilitar ordens reais
BINANCE_TESTNET = True   # Habilitar o modo TestNet (Sandbox) da Binance
BASE_CURRENCY = 'BRL'    # Moeda base para as operações
BRL_PER_TRADE = 100.0    # Valor em Reais para cada operação de compra

# Estratégia de Saída
STOP_LOSS_PCT = 0.10     # 10% de stop loss
TAKE_PROFIT_PCT = 0.20   # 20% de take profit
