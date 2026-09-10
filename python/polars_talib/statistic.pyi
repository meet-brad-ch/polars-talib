from polars import Expr
from polars._typing import IntoExpr

def beta(real0: IntoExpr = ..., real1: IntoExpr = ..., timeperiod: int = 5) -> Expr:
    """Beta (Statistic Functions), TA-Lib BETA.
    
    timeperiod: Number of period (default 5)
    Output: real"""

def correl(real0: IntoExpr = ..., real1: IntoExpr = ..., timeperiod: int = 30) -> Expr:
    """Pearson's Correlation Coefficient (r) (Statistic Functions), TA-Lib CORREL.
    
    timeperiod: Number of period (default 30)
    Output: real"""

def linearreg(real: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Linear Regression (Statistic Functions), TA-Lib LINEARREG.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def linearreg_angle(real: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Linear Regression Angle (Statistic Functions), TA-Lib LINEARREG_ANGLE.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def linearreg_intercept(real: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Linear Regression Intercept (Statistic Functions), TA-Lib LINEARREG_INTERCEPT.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def linearreg_slope(real: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Linear Regression Slope (Statistic Functions), TA-Lib LINEARREG_SLOPE.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def stddev(real: IntoExpr = ..., timeperiod: int = 5, nbdev: float = 1.0) -> Expr:
    """Standard Deviation (Statistic Functions), TA-Lib STDDEV.
    
    timeperiod: Number of period (default 5)
    nbdev: Nb of deviations (default 1.0)
    Output: real"""

def tsf(real: IntoExpr = ..., timeperiod: int = 14) -> Expr:
    """Time Series Forecast (Statistic Functions), TA-Lib TSF.
    
    timeperiod: Number of period (default 14)
    Output: real"""

def var(real: IntoExpr = ..., timeperiod: int = 5, nbdev: float = 1.0) -> Expr:
    """Variance (Statistic Functions), TA-Lib VAR.
    
    timeperiod: Number of period (default 5)
    nbdev: Nb of deviations (default 1.0)
    Output: real"""
