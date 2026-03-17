@echo off
TITLE Bottrader - @traderskybot
echo ==========================================
echo    INICIANDO BOTTRADER (TESTNET)
echo ==========================================

:: Configurando as chaves de API (Ambiente de Teste)
set BINANCE_API_KEY=TUHS2uC4AJAifVt57csTNhb7StM8Akp94vYOggTlKAAR8fZ1TQllRx1i1OM5YT2N
set BINANCE_SECRET=c7mmMs9YUdYNZymHbzf0ngLQXGbLvfP1y42EbrlAcbMR4BrFuUHnHUixSait1L93

:: Verificando se as dependências estão instaladas
echo Verificando dependencias...
pip install -r requirements.txt

:: Iniciando o robô
echo.
echo O robo sera iniciado agora. Fique atento ao Telegram!
python main.py

pause
