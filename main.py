import ccxt
import pandas as pd
import time
from datetime import datetime
from .config import *
from .patterns import is_rbr
from .bos import detect_bos
from .telegram_alert import send_telegram_alert
from .trading import create_market_order, get_balance, calculate_amount

# Inicialização da Binance
binance = ccxt.binance({
    'apiKey': BINANCE_API_KEY,
    'secret': BINANCE_SECRET,
    'enableRateLimit': True
})

def get_ohlcv(symbol):
    """
    Busca as velas de preço da Binance.
    """
    candles = binance.fetch_ohlcv(symbol, timeframe=TIMEFRAME, limit=50)
    df = pd.DataFrame(candles, columns=['timestamp','open','high','low','close','volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Estado simples para rastrear se já estamos em uma posição
# Em um sistema real, isso deveria ser salvo em um banco de dados ou arquivo
active_positions = {symbol: False for symbol in SYMBOLS}

print(f"--- Bottrader Iniciado ---")
print(f"Modo Trading Habilitado: {TRADING_ENABLED}")
print(f"Símbolos: {SYMBOLS}")

while True:
    for symbol in SYMBOLS:
        try:
            df = get_ohlcv(symbol)
            
            # 1. Lógica de Compra
            if not active_positions[symbol]:
                if is_rbr(df) or detect_bos(df):
                    msg = f"🔍 Sinal de COMPRA detectado em {symbol} ({TIMEFRAME}) - {datetime.now()}"
                    print(msg)
                    send_telegram_alert(msg)
                    
                    if TRADING_ENABLED:
                        # Verificar saldo em USDT
                        usdt_balance = get_balance(binance, 'USDT')
                        if usdt_balance >= USDT_PER_TRADE:
                            amount_to_buy = calculate_amount(binance, symbol, USDT_PER_TRADE)
                            order = create_market_order(binance, symbol, 'buy', amount_to_buy)
                            if order:
                                active_positions[symbol] = True
                        else:
                            msg_error = f"⚠️ Saldo insuficiente para comprar {symbol}. Saldo: {usdt_balance} USDT"
                            print(msg_error)
                            send_telegram_alert(msg_error)
            
            # 2. Lógica de Venda (Exemplo Simples)
            elif active_positions[symbol]:
                # Aqui você implementaria sua lógica de saída (Stop Loss, Take Profit ou sinal contrário)
                # Por enquanto, vamos apenas monitorar um sinal de venda fictício ou lucro/prejuízo
                # Exemplo: Vender se o preço subir 2% ou cair 1% (Placeholder simplificado)
                current_price = df['close'].iloc[-1]
                # Nota: Em um bot real, você deve salvar o preço de entrada da ordem
                
                # Placeholder para demonstrar a chamada de venda
                # if logic_to_sell:
                #     amount_to_sell = get_balance(binance, symbol.split('/')[0])
                #     create_market_order(binance, symbol, 'sell', amount_to_sell)
                #     active_positions[symbol] = False
                pass

        except Exception as e:
            print(f"Erro com {symbol}: {e}")
            
    time.sleep(60)
