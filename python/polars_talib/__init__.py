"""TA-Lib for Polars expressions.

Every TA-Lib function is a module-level function returning a ``pl.Expr``; multi-output
functions return a struct with TA-Lib's output names. Signatures, defaults and docstrings
come from TA-Lib itself (see ``_build``), grouped into one module per TA-Lib group.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

import polars as pl

from . import _polars_talib
from ._build import MODULES, specs
from .cycle import *  # noqa: F403
from .math_operators import *  # noqa: F403
from .math_transform import *  # noqa: F403
from .momentum import *  # noqa: F403
from .overlap import *  # noqa: F403
from .overlap import wma
from .pattern import *  # noqa: F403
from .price_transform import *  # noqa: F403
from .statistic import *  # noqa: F403
from .volatility import *  # noqa: F403
from .volume import *  # noqa: F403

if TYPE_CHECKING:
    from polars._typing import IntoExpr

__talib_version__ = _polars_talib.version().split(" ")[0]


def get_functions() -> list[str]:
    return [s.python_name for s in specs()]


def get_function_groups() -> dict[str, list[str]]:
    return {group: [s.python_name for s in specs() if s.group == group] for group in MODULES}


def hma(real: IntoExpr = "close", period: int = 16) -> pl.Expr:
    """Hull Moving Average: WMA(2 * WMA(n / 2) - WMA(n), isqrt(n)). Not a TA-Lib function."""
    return wma(2 * wma(real, period // 2) - wma(real, period), math.isqrt(period))
