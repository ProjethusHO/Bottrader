import ccxt
import pandas as pd
import time
from datetime import datetime
from .config import *
from .patterns import is_rbr
from .bos import detect_bos
from .telegram_alert import send_telegram_alert
from .trading import create_market_order, get_balance, calculate_amount, get_current_price

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

# Estado das posições: symbol -> { 'active': bool, 'entry_price': float, 'amount': float }
positions = {symbol: {'active': False, 'entry_price': 0.0, 'amount': 0.0} for symbol in SYMBOLS}

print(f"--- Bottrader Iniciado (Modo {BASE_CURRENCY}) ---")
print(f"Modo Trading Habilitado: {TRADING_ENABLED}")
print(f"Símbolos: {SYMBOLS}")
print(f"Stop Loss: {STOP_LOSS_PCT * 100}% | Take Profit: {TAKE_PROFIT_PCT * 100}%")

while True:
    for symbol in SYMBOLS:
        try:
            # 1. Lógica de Compra (Se não houver posição aberta para este símbolo)
            if not positions[symbol]['active']:
                df = get_ohlcv(symbol)
                if is_rbr(df) or detect_bos(df):
                    msg = f"🔍 Sinal de COMPRA detectado em {symbol} ({TIMEFRAME}) - {datetime.now()}"
                    print(msg)
                    send_telegram_alert(msg)
                    
                    if TRADING_ENABLED:
                        # Verificar saldo na moeda base (BRL)
                        base_balance = get_balance(binance, BASE_CURRENCY)
                        if base_balance >= BRL_PER_TRADE:
                            amount_to_buy = calculate_amount(binance, symbol, BRL_PER_TRADE)
                            order = create_market_order(binance, symbol, 'buy', amount_to_buy)
                            if order:
                                positions[symbol]['active'] = True
                                positions[symbol]['entry_price'] = order['price'] if 'price' in order else get_current_price(binance, symbol)
                                positions[symbol]['amount'] = order['filled'] if 'filled' in order else amount_to_buy
                                msg_buy = f"✅ Posição aberta em {symbol} a R$ {positions[symbol]['entry_price']:.2f}"
                                print(msg_buy)
                                send_telegram_alert(msg_buy)
                        else:
                            msg_error = f"⚠️ Saldo insuficiente para comprar {symbol}. Saldo: R$ {base_balance:.2f}"
                            print(msg_error)
                            send_telegram_alert(msg_error)
            
            # 2. Lógica de Monitoramento e Saída (Stop Loss e Take Profit)
            elif positions[symbol]['active']:
                current_price = get_current_price(binance, symbol)
                if current_price is None:
                    continue
                
                entry_price = positions[symbol]['entry_price']
                profit_pct = (current_price - entry_price) / entry_price
                
                # Verificar Stop Loss
                if profit_pct <= -STOP_LOSS_PCT:
                    msg_sl = f"🛑 STOP LOSS atingido em {symbol}! Perda: {profit_pct*100:.2f}%"
                    print(msg_sl)
                    send_telegram_alert(msg_sl)
                    if TRADING_ENABLED:
                        create_market_order(binance, symbol, 'sell', positions[symbol]['amount'])
                    positions[symbol]['active'] = False
                
                # Verificar Take Profit
                elif profit_pct >= TAKE_PROFIT_PCT:
                    msg_tp = f"🎯 TAKE PROFIT atingido em {symbol}! Lucro: {profit_pct*100:.2f}%"
                    print(msg_tp)
                    send_telegram_alert(msg_tp)
                    if TRADING_ENABLED:
                        create_market_order(binance, symbol, 'sell', positions[symbol]['amount'])
                    positions[symbol]['active'] = False
                
                # Log de monitoramento opcional
                # print(f"Monitorando {symbol}: Lucro Atual: {profit_pct*100:.2f}%")

        except Exception as e:
            print(f"Erro com {symbol}: {e}")
            
    time.sleep(60)
