import ccxt
from .config import *
from .telegram_alert import send_telegram_alert

def create_market_order(exchange, symbol, side, amount):
    """
    Cria uma ordem a mercado na Binance.
    :param exchange: Instância do ccxt.binance
    :param symbol: Símbolo do par (ex: 'BTC/USDT')
    :param side: 'buy' ou 'sell'
    :param amount: Quantidade a ser comprada ou vendida
    """
    try:
        order = exchange.create_market_order(symbol, side, amount)
        msg = f"🚀 Ordem de {side.upper()} executada para {symbol}: {amount} unidades."
        print(msg)
        send_telegram_alert(msg)
        return order
    except Exception as e:
        msg = f"❌ Erro ao executar ordem de {side.upper()} para {symbol}: {e}"
        print(msg)
        send_telegram_alert(msg)
        return None

def get_balance(exchange, currency):
    """
    Verifica o saldo disponível para uma moeda específica.
    :param exchange: Instância do ccxt.binance
    :param currency: Moeda (ex: 'USDT', 'BTC')
    """
    try:
        balance = exchange.fetch_balance()
        return balance['free'][currency]
    except Exception as e:
        print(f"Erro ao buscar saldo de {currency}: {e}")
        return 0.0

def calculate_amount(exchange, symbol, usdt_amount):
    """
    Calcula a quantidade de ativos a comprar com base em um valor em USDT.
    """
    try:
        ticker = exchange.fetch_ticker(symbol)
        price = ticker['last']
        return usdt_amount / price
    except Exception as e:
        print(f"Erro ao calcular quantidade para {symbol}: {e}")
        return 0.0
