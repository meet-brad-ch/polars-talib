from polars import Expr
from polars._typing import IntoExpr

def add(real0: IntoExpr = ..., real1: IntoExpr = ...) -> Expr:
    """Vector Arithmetic Add (Math Operators), TA-Lib ADD.
    
    Output: real"""

def div(real0: IntoExpr = ..., real1: IntoExpr = ...) -> Expr:
    """Vector Arithmetic Div (Math Operators), TA-Lib DIV.
    
    Output: real"""

def max(real: IntoExpr = ..., timeperiod: int = 30) -> Expr:
    """Highest value over a specified period (Math Operators), TA-Lib MAX.
    
    timeperiod: Number of period (default 30)
    Output: real"""

def maxindex(real: IntoExpr = ..., timeperiod: int = 30) -> Expr:
    """Index of highest value over a specified period (Math Operators), TA-Lib MAXINDEX.
    
    timeperiod: Number of period (default 30)
    Output: integer"""

def min(real: IntoExpr = ..., timeperiod: int = 30) -> Expr:
    """Lowest value over a specified period (Math Operators), TA-Lib MIN.
    
    timeperiod: Number of period (default 30)
    Output: real"""

def minindex(real: IntoExpr = ..., timeperiod: int = 30) -> Expr:
    """Index of lowest value over a specified period (Math Operators), TA-Lib MININDEX.
    
    timeperiod: Number of period (default 30)
    Output: integer"""

def minmax(real: IntoExpr = ..., timeperiod: int = 30) -> Expr:
    """Lowest and highest values over a specified period (Math Operators), TA-Lib MINMAX.
    
    timeperiod: Number of period (default 30)
    Output struct: min, max"""

def minmaxindex(real: IntoExpr = ..., timeperiod: int = 30) -> Expr:
    """Indexes of lowest and highest values over a specified period (Math Operators), TA-Lib MINMAXINDEX.
    
    timeperiod: Number of period (default 30)
    Output struct: minidx, maxidx"""

def mult(real0: IntoExpr = ..., real1: IntoExpr = ...) -> Expr:
    """Vector Arithmetic Mult (Math Operators), TA-Lib MULT.
    
    Output: real"""

def sub(real0: IntoExpr = ..., real1: IntoExpr = ...) -> Expr:
    """Vector Arithmetic Subtraction (Math Operators), TA-Lib SUB.
    
    Output: real"""

def sum(real: IntoExpr = ..., timeperiod: int = 30) -> Expr:
    """Summation (Math Operators), TA-Lib SUM.
    
    timeperiod: Number of period (default 30)
    Output: real"""
