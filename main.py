
import ccxt
import pandas as pd
import time
from datetime import datetime
from .config import *
from .patterns import is_rbr
from .bos import detect_bos
from .telegram_alert import send_telegram_alert

binance = ccxt.binance({
    'apiKey': BINANCE_API_KEY,
    'secret': BINANCE_SECRET,
    'enableRateLimit': True
})

def get_ohlcv(symbol):
    candles = binance.fetch_ohlcv(symbol, timeframe=TIMEFRAME, limit=50)
    df = pd.DataFrame(candles, columns=['timestamp','open','high','low','close','volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

while True:
    for symbol in SYMBOLS:
        try:
            df = get_ohlcv(symbol)
            if is_rbr(df):
                msg = f"🟢 RBR detectado em {symbol} ({TIMEFRAME}) - {datetime.now()}"
                send_telegram_alert(msg)
            if detect_bos(df):
                msg = f"📈 BoS detectado em {symbol} ({TIMEFRAME}) - {datetime.now()}"
                send_telegram_alert(msg)
        except Exception as e:
            print(f"Erro com {symbol}: {e}")
    time.sleep(60)
