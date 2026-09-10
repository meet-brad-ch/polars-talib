from polars import Expr
from polars._typing import IntoExpr

def accbands(high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., timeperiod: int = 20) -> Expr:
    """Acceleration Bands (Overlap Studies), TA-Lib ACCBANDS.
    
    timeperiod: Number of period (default 20)
    Output struct: upperband, middleband, lowerband"""

def bbands(real: IntoExpr = ..., timeperiod: int = 5, nbdevup: float = 2.0, nbdevdn: float = 2.0, matype: int = 0) -> Expr:
    """Bollinger Bands (Overlap Studies), TA-Lib BBANDS.
    
    timeperiod: Number of period (default 5)
    nbdevup: Deviation multiplier for upper band (default 2.0)
    nbdevdn: Deviation multiplier for lower band (default 2.0)
    matype: Type of Moving Average (default 0)
    Output struct: upperband, middleband, lowerband"""

def dema(real: IntoExpr = ..., timeperiod: int = 30) -> Expr:
    """Double Exponential Moving Average (Overlap Studies), TA-Lib DEMA.
    
    timeperiod: Number of period (default 30)
    Output: real"""

def ema(real: IntoExpr = ..., timeperiod: int = 30) -> Expr:
    """Exponential Moving Average (Overlap Studies), TA-Lib EMA.
    
    timeperiod: Number of period (default 30)
    Output: real"""

def ht_trendline(real: IntoExpr = ...) -> Expr:
    """Hilbert Transform - Instantaneous Trendline (Overlap Studies), TA-Lib HT_TRENDLINE.
    
    Output: real"""

def kama(real: IntoExpr = ..., timeperiod: int = 30) -> Expr:
    """Kaufman Adaptive Moving Average (Overlap Studies), TA-Lib KAMA.
    
    timeperiod: Number of period (default 30)
    Output: real"""

def ma(real: IntoExpr = ..., timeperiod: int = 30, matype: int = 0) -> Expr:
    """Moving average (Overlap Studies), TA-Lib MA.
    
    timeperiod: Number of period (default 30)
    matype: Type of Moving Average (default 0)
    Output: real"""

def mama(real: IntoExpr = ..., fastlimit: float = 0.5, slowlimit: float = 0.05) -> Expr:
    """MESA Adaptive Moving Average (Overlap Studies), TA-Lib MAMA.
    
    fastlimit: Upper limit use in the adaptive algorithm (default 0.5)
    slowlimit: Lower limit use in the adaptive algorithm (default 0.05)
    Output struct: mama, fama"""

def mavp(real: IntoExpr = ..., periods: IntoExpr = ..., minperiod: int = 2, maxperiod: int = 30, matype: int = 0) -> Expr:
    """Moving average with variable period (Overlap Studies), TA-Lib MAVP.
    
    minperiod: Value less than minimum will be changed to Minimum period (default 2)
    maxperiod: Value higher than maximum will be changed to Maximum period (default 30)
    matype: Type of Moving Average (default 0)
    Output: real"""

def midpoint(real: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """MidPoint over period (Overlap Studies), TA-Lib MIDPOINT.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def midprice(high: IntoExpr = ..., low: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Midpoint Price over period (Overlap Studies), TA-Lib MIDPRICE.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def sar(high: IntoExpr = ..., low: IntoExpr = ..., acceleration: float = 0.02, maximum: float = 0.2) -> Expr:
    """Parabolic SAR (Overlap Studies), TA-Lib SAR.
    
    acceleration: Acceleration Factor used up to the Maximum value (default 0.02)
    maximum: Acceleration Factor Maximum value (default 0.2)
    Output: real"""

def sarext(high: IntoExpr = ..., low: IntoExpr = ..., startvalue: float = 0.0, offsetonreverse: float = 0.0, accelerationinitlong: float = 0.02, accelerationlong: float = 0.02, accelerationmaxlong: float = 0.2, accelerationinitshort: float = 0.02, accelerationshort: float = 0.02, accelerationmaxshort: float = 0.2) -> Expr:
    """Parabolic SAR - Extended (Overlap Studies), TA-Lib SAREXT.
    
    startvalue: Start value and direction. 0 for Auto, >0 for Long, <0 for Short (default 0.0)
    offsetonreverse: Percent offset added/removed to initial stop on short/long reversal (default 0.0)
    accelerationinitlong: Acceleration Factor initial value for the Long direction (default 0.02)
    accelerationlong: Acceleration Factor for the Long direction (default 0.02)
    accelerationmaxlong: Acceleration Factor maximum value for the Long direction (default 0.2)
    accelerationinitshort: Acceleration Factor initial value for the Short direction (default 0.02)
    accelerationshort: Acceleration Factor for the Short direction (default 0.02)
    accelerationmaxshort: Acceleration Factor maximum value for the Short direction (default 0.2)
    Output: real"""

def sma(real: IntoExpr = ..., timeperiod: int = 30) -> Expr:
    """Simple Moving Average (Overlap Studies), TA-Lib SMA.
    
    timeperiod: Number of period (default 30)
    Output: real"""

def t3(real: IntoExpr = ..., timeperiod: int = 5, vfactor: float = 0.7) -> Expr:
    """Triple Exponential Moving Average (T3) (Overlap Studies), TA-Lib T3.
    
    timeperiod: Number of period (default 5)
    vfactor: Volume Factor (default 0.7)
    Output: real"""

def tema(real: IntoExpr = ..., timeperiod: int = 30) -> Expr:
    """Triple Exponential Moving Average (Overlap Studies), TA-Lib TEMA.
    
    timeperiod: Number of period (default 30)
    Output: real"""

def trima(real: IntoExpr = ..., timeperiod: int = 30) -> Expr:
    """Triangular Moving Average (Overlap Studies), TA-Lib TRIMA.
    
    timeperiod: Number of period (default 30)
    Output: real"""

def wma(real: IntoExpr = ..., timeperiod: int = 30) -> Expr:
    """Weighted Moving Average (Overlap Studies), TA-Lib WMA.
    
    timeperiod: Number of period (default 30)
    Output: real"""
