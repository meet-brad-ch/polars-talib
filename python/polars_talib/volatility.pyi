from polars import Expr
from polars._typing import IntoExpr

def atr(high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Average True Range (Volatility Indicators), TA-Lib ATR.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def natr(high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Normalized Average True Range (Volatility Indicators), TA-Lib NATR.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def trange(high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """True Range (Volatility Indicators), TA-Lib TRANGE.
    
    Output: real"""
