from polars import Expr
from polars._typing import IntoExpr

def ht_dcperiod(real: IntoExpr = ...) -> Expr:
    """Hilbert Transform - Dominant Cycle Period (Cycle Indicators), TA-Lib HT_DCPERIOD.
    
    Output: real"""

def ht_dcphase(real: IntoExpr = ...) -> Expr:
    """Hilbert Transform - Dominant Cycle Phase (Cycle Indicators), TA-Lib HT_DCPHASE.
    
    Output: real"""

def ht_phasor(real: IntoExpr = ...) -> Expr:
    """Hilbert Transform - Phasor Components (Cycle Indicators), TA-Lib HT_PHASOR.
    
    Output struct: inphase, quadrature"""

def ht_sine(real: IntoExpr = ...) -> Expr:
    """Hilbert Transform - SineWave (Cycle Indicators), TA-Lib HT_SINE.
    
    Output struct: sine, leadsine"""

def ht_trendmode(real: IntoExpr = ...) -> Expr:
    """Hilbert Transform - Trend vs Cycle Mode (Cycle Indicators), TA-Lib HT_TRENDMODE.
    
    Output: integer"""
