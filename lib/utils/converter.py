from decimal import Decimal, getcontext, ROUND_HALF_UP

def get_decimal(valor, casas_decimais = 2, rounding = ROUND_HALF_UP):
    """
    Recebe um número e o converte para Decimal com precisão de duas casas decimais por padrão
    """

    valor_convertido = Decimal(str(valor)).quantize(Decimal("0." + "0" * casas_decimais), rounding=rounding)

    return valor_convertido