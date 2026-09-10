from polars import Expr
from polars._typing import IntoExpr

def adx(high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Average Directional Movement Index (Momentum Indicators), TA-Lib ADX.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def adxr(high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Average Directional Movement Index Rating (Momentum Indicators), TA-Lib ADXR.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def apo(real: IntoExpr = ..., fastperiod: int = 12, slowperiod: int = 26, matype: int = 0) -> Expr:
    """Absolute Price Oscillator (Momentum Indicators), TA-Lib APO.
    
    fastperiod: Number of period for the fast MA (default 12)
    slowperiod: Number of period for the slow MA (default 26)
    matype: Type of Moving Average (default 0)
    Output: real"""

def aroon(high: IntoExpr = ..., low: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Aroon (Momentum Indicators), TA-Lib AROON.
    
    timeperiod: Number of period (default 14)
    Output struct: aroondown, aroonup"""

def aroonosc(high: IntoExpr = ..., low: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Aroon Oscillator (Momentum Indicators), TA-Lib AROONOSC.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def bop(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Balance Of Power (Momentum Indicators), TA-Lib BOP.
    
    Output: real"""

def cci(high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Commodity Channel Index (Momentum Indicators), TA-Lib CCI.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def cmo(real: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Chande Momentum Oscillator (Momentum Indicators), TA-Lib CMO.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def dx(high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Directional Movement Index (Momentum Indicators), TA-Lib DX.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def imi(open: IntoExpr = ..., close: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Intraday Momentum Index (Momentum Indicators), TA-Lib IMI.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def macd(real: IntoExpr = ..., fastperiod: int = 12, slowperiod: int = 26, signalperiod: int = 9) -> Expr:
    """Moving Average Convergence/Divergence (Momentum Indicators), TA-Lib MACD.
    
    fastperiod: Number of period for the fast MA (default 12)
    slowperiod: Number of period for the slow MA (default 26)
    signalperiod: Smoothing for the signal line (nb of period) (default 9)
    Output struct: macd, macdsignal, macdhist"""

def macdext(real: IntoExpr = ..., fastperiod: int = 12, fastmatype: int = 0, slowperiod: int = 26, slowmatype: int = 0, signalperiod: int = 9, signalmatype: int = 0) -> Expr:
    """MACD with controllable MA type (Momentum Indicators), TA-Lib MACDEXT.
    
    fastperiod: Number of period for the fast MA (default 12)
    fastmatype: Type of Moving Average for fast MA (default 0)
    slowperiod: Number of period for the slow MA (default 26)
    slowmatype: Type of Moving Average for slow MA (default 0)
    signalperiod: Smoothing for the signal line (nb of period) (default 9)
    signalmatype: Type of Moving Average for signal line (default 0)
    Output struct: macd, macdsignal, macdhist"""

def macdfix(real: IntoExpr = ..., signalperiod: int = 9) -> Expr:
    """Moving Average Convergence/Divergence Fix 12/26 (Momentum Indicators), TA-Lib MACDFIX.
    
    signalperiod: Smoothing for the signal line (nb of period) (default 9)
    Output struct: macd, macdsignal, macdhist"""

def mfi(high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., volume: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Money Flow Index (Momentum Indicators), TA-Lib MFI.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def minus_di(high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Minus Directional Indicator (Momentum Indicators), TA-Lib MINUS_DI.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def minus_dm(high: IntoExpr = ..., low: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Minus Directional Movement (Momentum Indicators), TA-Lib MINUS_DM.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def mom(real: IntoExpr = ..., timeperiod: int = 10) -> Expr:
    """Momentum (Momentum Indicators), TA-Lib MOM.
    
    timeperiod: Number of period (default 10)
    Output: real"""

def plus_di(high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Plus Directional Indicator (Momentum Indicators), TA-Lib PLUS_DI.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def plus_dm(high: IntoExpr = ..., low: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Plus Directional Movement (Momentum Indicators), TA-Lib PLUS_DM.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def ppo(real: IntoExpr = ..., fastperiod: int = 12, slowperiod: int = 26, matype: int = 0) -> Expr:
    """Percentage Price Oscillator (Momentum Indicators), TA-Lib PPO.
    
    fastperiod: Number of period for the fast MA (default 12)
    slowperiod: Number of period for the slow MA (default 26)
    matype: Type of Moving Average (default 0)
    Output: real"""

def roc(real: IntoExpr = ..., timeperiod: int = 10) -> Expr:
    """Rate of change : ((price/prevPrice)-1)*100 (Momentum Indicators), TA-Lib ROC.
    
    timeperiod: Number of period (default 10)
    Output: real"""

def rocp(real: IntoExpr = ..., timeperiod: int = 10) -> Expr:
    """Rate of change Percentage: (price-prevPrice)/prevPrice (Momentum Indicators), TA-Lib ROCP.
    
    timeperiod: Number of period (default 10)
    Output: real"""

def rocr(real: IntoExpr = ..., timeperiod: int = 10) -> Expr:
    """Rate of change ratio: (price/prevPrice) (Momentum Indicators), TA-Lib ROCR.
    
    timeperiod: Number of period (default 10)
    Output: real"""

def rocr100(real: IntoExpr = ..., timeperiod: int = 10) -> Expr:
    """Rate of change ratio 100 scale: (price/prevPrice)*100 (Momentum Indicators), TA-Lib ROCR100.
    
    timeperiod: Number of period (default 10)
    Output: real"""

def rsi(real: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Relative Strength Index (Momentum Indicators), TA-Lib RSI.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def stoch(high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., fastk_period: int = 5, slowk_period: int = 3, slowk_matype: int = 0, slowd_period: int = 3, slowd_matype: int = 0) -> Expr:
    """Stochastic (Momentum Indicators), TA-Lib STOCH.
    
    fastk_period: Time period for building the Fast-K line (default 5)
    slowk_period: Smoothing for making the Slow-K line. Usually set to 3 (default 3)
    slowk_matype: Type of Moving Average for Slow-K (default 0)
    slowd_period: Smoothing for making the Slow-D line (default 3)
    slowd_matype: Type of Moving Average for Slow-D (default 0)
    Output struct: slowk, slowd"""

def stochf(high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., fastk_period: int = 5, fastd_period: int = 3, fastd_matype: int = 0) -> Expr:
    """Stochastic Fast (Momentum Indicators), TA-Lib STOCHF.
    
    fastk_period: Time period for building the Fast-K line (default 5)
    fastd_period: Smoothing for making the Fast-D line. Usually set to 3 (default 3)
    fastd_matype: Type of Moving Average for Fast-D (default 0)
    Output struct: fastk, fastd"""

def stochrsi(real: IntoExpr = ..., timeperiod: int = 14, fastk_period: int = 5, fastd_period: int = 3, fastd_matype: int = 0) -> Expr:
    """Stochastic Relative Strength Index (Momentum Indicators), TA-Lib STOCHRSI.
    
    timeperiod: Number of period (default 14)
    fastk_period: Time period for building the Fast-K line (default 5)
    fastd_period: Smoothing for making the Fast-D line. Usually set to 3 (default 3)
    fastd_matype: Type of Moving Average for Fast-D (default 0)
    Output struct: fastk, fastd"""

def trix(real: IntoExpr = ..., timeperiod: int = 30) -> Expr:
    """1-day Rate-Of-Change (ROC) of a Triple Smooth EMA (Momentum Indicators), TA-Lib TRIX.
    
    timeperiod: Number of period (default 30)
    Output: real"""

def ultosc(high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., timeperiod1: int = 7, timeperiod2: int = 14, timeperiod3: int = 28) -> Expr:
    """Ultimate Oscillator (Momentum Indicators), TA-Lib ULTOSC.
    
    timeperiod1: Number of bars for 1st period. (default 7)
    timeperiod2: Number of bars fro 2nd period (default 14)
    timeperiod3: Number of bars for 3rd period (default 28)
    Output: real"""

def willr(high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Williams' %R (Momentum Indicators), TA-Lib WILLR.
    
    timeperiod: Number of period (default 14)
    Output: real"""
