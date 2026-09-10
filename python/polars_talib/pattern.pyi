from polars import Expr
from polars._typing import IntoExpr

def cdl2crows(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Two Crows (Pattern Recognition), TA-Lib CDL2CROWS.
    
    Output: integer"""

def cdl3blackcrows(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Three Black Crows (Pattern Recognition), TA-Lib CDL3BLACKCROWS.
    
    Output: integer"""

def cdl3inside(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Three Inside Up/Down (Pattern Recognition), TA-Lib CDL3INSIDE.
    
    Output: integer"""

def cdl3linestrike(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Three-Line Strike  (Pattern Recognition), TA-Lib CDL3LINESTRIKE.
    
    Output: integer"""

def cdl3outside(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Three Outside Up/Down (Pattern Recognition), TA-Lib CDL3OUTSIDE.
    
    Output: integer"""

def cdl3starsinsouth(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Three Stars In The South (Pattern Recognition), TA-Lib CDL3STARSINSOUTH.
    
    Output: integer"""

def cdl3whitesoldiers(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Three Advancing White Soldiers (Pattern Recognition), TA-Lib CDL3WHITESOLDIERS.
    
    Output: integer"""

def cdlabandonedbaby(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., penetration: float = 0.3) -> Expr:
    """Abandoned Baby (Pattern Recognition), TA-Lib CDLABANDONEDBABY.
    
    penetration: Percentage of penetration of a candle within another candle (default 0.3)
    Output: integer"""

def cdladvanceblock(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Advance Block (Pattern Recognition), TA-Lib CDLADVANCEBLOCK.
    
    Output: integer"""

def cdlbelthold(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Belt-hold (Pattern Recognition), TA-Lib CDLBELTHOLD.
    
    Output: integer"""

def cdlbreakaway(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Breakaway (Pattern Recognition), TA-Lib CDLBREAKAWAY.
    
    Output: integer"""

def cdlclosingmarubozu(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Closing Marubozu (Pattern Recognition), TA-Lib CDLCLOSINGMARUBOZU.
    
    Output: integer"""

def cdlconcealbabyswall(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Concealing Baby Swallow (Pattern Recognition), TA-Lib CDLCONCEALBABYSWALL.
    
    Output: integer"""

def cdlcounterattack(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Counterattack (Pattern Recognition), TA-Lib CDLCOUNTERATTACK.
    
    Output: integer"""

def cdldarkcloudcover(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., penetration: float = 0.5) -> Expr:
    """Dark Cloud Cover (Pattern Recognition), TA-Lib CDLDARKCLOUDCOVER.
    
    penetration: Percentage of penetration of a candle within another candle (default 0.5)
    Output: integer"""

def cdldoji(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Doji (Pattern Recognition), TA-Lib CDLDOJI.
    
    Output: integer"""

def cdldojistar(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Doji Star (Pattern Recognition), TA-Lib CDLDOJISTAR.
    
    Output: integer"""

def cdldragonflydoji(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Dragonfly Doji (Pattern Recognition), TA-Lib CDLDRAGONFLYDOJI.
    
    Output: integer"""

def cdlengulfing(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Engulfing Pattern (Pattern Recognition), TA-Lib CDLENGULFING.
    
    Output: integer"""

def cdleveningdojistar(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., penetration: float = 0.3) -> Expr:
    """Evening Doji Star (Pattern Recognition), TA-Lib CDLEVENINGDOJISTAR.
    
    penetration: Percentage of penetration of a candle within another candle (default 0.3)
    Output: integer"""

def cdleveningstar(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., penetration: float = 0.3) -> Expr:
    """Evening Star (Pattern Recognition), TA-Lib CDLEVENINGSTAR.
    
    penetration: Percentage of penetration of a candle within another candle (default 0.3)
    Output: integer"""

def cdlgapsidesidewhite(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Up/Down-gap side-by-side white lines (Pattern Recognition), TA-Lib CDLGAPSIDESIDEWHITE.
    
    Output: integer"""

def cdlgravestonedoji(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Gravestone Doji (Pattern Recognition), TA-Lib CDLGRAVESTONEDOJI.
    
    Output: integer"""

def cdlhammer(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Hammer (Pattern Recognition), TA-Lib CDLHAMMER.
    
    Output: integer"""

def cdlhangingman(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Hanging Man (Pattern Recognition), TA-Lib CDLHANGINGMAN.
    
    Output: integer"""

def cdlharami(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Harami Pattern (Pattern Recognition), TA-Lib CDLHARAMI.
    
    Output: integer"""

def cdlharamicross(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Harami Cross Pattern (Pattern Recognition), TA-Lib CDLHARAMICROSS.
    
    Output: integer"""

def cdlhighwave(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """High-Wave Candle (Pattern Recognition), TA-Lib CDLHIGHWAVE.
    
    Output: integer"""

def cdlhikkake(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Hikkake Pattern (Pattern Recognition), TA-Lib CDLHIKKAKE.
    
    Output: integer"""

def cdlhikkakemod(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Modified Hikkake Pattern (Pattern Recognition), TA-Lib CDLHIKKAKEMOD.
    
    Output: integer"""

def cdlhomingpigeon(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Homing Pigeon (Pattern Recognition), TA-Lib CDLHOMINGPIGEON.
    
    Output: integer"""

def cdlidentical3crows(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Identical Three Crows (Pattern Recognition), TA-Lib CDLIDENTICAL3CROWS.
    
    Output: integer"""

def cdlinneck(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """In-Neck Pattern (Pattern Recognition), TA-Lib CDLINNECK.
    
    Output: integer"""

def cdlinvertedhammer(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Inverted Hammer (Pattern Recognition), TA-Lib CDLINVERTEDHAMMER.
    
    Output: integer"""

def cdlkicking(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Kicking (Pattern Recognition), TA-Lib CDLKICKING.
    
    Output: integer"""

def cdlkickingbylength(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Kicking - bull/bear determined by the longer marubozu (Pattern Recognition), TA-Lib CDLKICKINGBYLENGTH.
    
    Output: integer"""

def cdlladderbottom(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Ladder Bottom (Pattern Recognition), TA-Lib CDLLADDERBOTTOM.
    
    Output: integer"""

def cdllongleggeddoji(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Long Legged Doji (Pattern Recognition), TA-Lib CDLLONGLEGGEDDOJI.
    
    Output: integer"""

def cdllongline(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Long Line Candle (Pattern Recognition), TA-Lib CDLLONGLINE.
    
    Output: integer"""

def cdlmarubozu(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Marubozu (Pattern Recognition), TA-Lib CDLMARUBOZU.
    
    Output: integer"""

def cdlmatchinglow(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Matching Low (Pattern Recognition), TA-Lib CDLMATCHINGLOW.
    
    Output: integer"""

def cdlmathold(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., penetration: float = 0.5) -> Expr:
    """Mat Hold (Pattern Recognition), TA-Lib CDLMATHOLD.
    
    penetration: Percentage of penetration of a candle within another candle (default 0.5)
    Output: integer"""

def cdlmorningdojistar(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., penetration: float = 0.3) -> Expr:
    """Morning Doji Star (Pattern Recognition), TA-Lib CDLMORNINGDOJISTAR.
    
    penetration: Percentage of penetration of a candle within another candle (default 0.3)
    Output: integer"""

def cdlmorningstar(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ..., penetration: float = 0.3) -> Expr:
    """Morning Star (Pattern Recognition), TA-Lib CDLMORNINGSTAR.
    
    penetration: Percentage of penetration of a candle within another candle (default 0.3)
    Output: integer"""

def cdlonneck(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """On-Neck Pattern (Pattern Recognition), TA-Lib CDLONNECK.
    
    Output: integer"""

def cdlpiercing(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Piercing Pattern (Pattern Recognition), TA-Lib CDLPIERCING.
    
    Output: integer"""

def cdlrickshawman(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Rickshaw Man (Pattern Recognition), TA-Lib CDLRICKSHAWMAN.
    
    Output: integer"""

def cdlrisefall3methods(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Rising/Falling Three Methods (Pattern Recognition), TA-Lib CDLRISEFALL3METHODS.
    
    Output: integer"""

def cdlseparatinglines(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Separating Lines (Pattern Recognition), TA-Lib CDLSEPARATINGLINES.
    
    Output: integer"""

def cdlshootingstar(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Shooting Star (Pattern Recognition), TA-Lib CDLSHOOTINGSTAR.
    
    Output: integer"""

def cdlshortline(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Short Line Candle (Pattern Recognition), TA-Lib CDLSHORTLINE.
    
    Output: integer"""

def cdlspinningtop(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Spinning Top (Pattern Recognition), TA-Lib CDLSPINNINGTOP.
    
    Output: integer"""

def cdlstalledpattern(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Stalled Pattern (Pattern Recognition), TA-Lib CDLSTALLEDPATTERN.
    
    Output: integer"""

def cdlsticksandwich(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Stick Sandwich (Pattern Recognition), TA-Lib CDLSTICKSANDWICH.
    
    Output: integer"""

def cdltakuri(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Takuri (Dragonfly Doji with very long lower shadow) (Pattern Recognition), TA-Lib CDLTAKURI.
    
    Output: integer"""

def cdltasukigap(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Tasuki Gap (Pattern Recognition), TA-Lib CDLTASUKIGAP.
    
    Output: integer"""

def cdlthrusting(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Thrusting Pattern (Pattern Recognition), TA-Lib CDLTHRUSTING.
    
    Output: integer"""

def cdltristar(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Tristar Pattern (Pattern Recognition), TA-Lib CDLTRISTAR.
    
    Output: integer"""

def cdlunique3river(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Unique 3 River (Pattern Recognition), TA-Lib CDLUNIQUE3RIVER.
    
    Output: integer"""

def cdlupsidegap2crows(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Upside Gap Two Crows (Pattern Recognition), TA-Lib CDLUPSIDEGAP2CROWS.
    
    Output: integer"""

def cdlxsidegap3methods(open: IntoExpr = ..., high: IntoExpr = ..., low: IntoExpr = ..., close: IntoExpr = ...) -> Expr:
    """Upside/Downside Gap Three Methods (Pattern Recognition), TA-Lib CDLXSIDEGAP3METHODS.
    
    Output: integer"""
