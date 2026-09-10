from polars import Expr
from polars._typing import IntoExpr

def ad(high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., volume: IntoExpr = ...) -> Expr:
    """Chaikin A/D Line (Volume Indicators), TA-Lib AD.
    
    Output: real"""

def adosc(high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., volume: IntoExpr = ..., fastperiod: int = 3, slowperiod: int = 10) -> Expr:
    """Chaikin A/D Oscillator (Volume Indicators), TA-Lib ADOSC.
    
    fastperiod: Number of period for the fast MA (default 3)
    slowperiod: Number of period for the slow MA (default 10)
    Output: real"""

def obv(real: IntoExpr = ..., volume: IntoExpr = ...) -> Expr:
    """On Balance Volume (Volume Indicators), TA-Lib OBV.
    
    Output: real"""
