def is_rbr(df):
    # Lógica para detectar Rally-Base-Rally (RBR)
    # Esta é uma implementação de exemplo e pode precisar ser ajustada
    # para a sua estratégia específica.
    # Por exemplo, um RBR pode ser definido como 3 velas: alta, baixa, alta
    if len(df) < 3:
        return False
    
    # Exemplo simplificado: vela de alta, seguida de uma vela menor (base), seguida de outra vela de alta
    # Isso é apenas um placeholder. A lógica real de RBR é mais complexa.
    if df["close"].iloc[-3] < df["open"].iloc[-3] and \
       df["close"].iloc[-2] > df["open"].iloc[-2] and \
       df["close"].iloc[-1] < df["open"].iloc[-1]:
        return True
    return False
