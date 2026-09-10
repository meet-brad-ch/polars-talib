# polars-talib

[![CI](https://github.com/meet-brad-ch/polars-talib/actions/workflows/ci.yml/badge.svg)](https://github.com/meet-brad-ch/polars-talib/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/meet-brad-ch/polars-talib?label=release)](https://github.com/meet-brad-ch/polars-talib/releases/latest)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-windows%20x64-lightgrey)
![TA-Lib](https://img.shields.io/badge/TA--Lib-0.7.1-blue)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Every [TA-Lib](https://ta-lib.org) function as a [Polars](https://pola.rs) expression.

```python
import polars as pl
import polars_talib as plta

df.with_columns(
    plta.sma(timeperiod=20).alias("sma20"),
    plta.macd().over("symbol").alias("macd"),  # struct: macd, macdsignal, macdhist
    plta.atr(pl.col("high"), pl.col("low"), pl.col("close"), timeperiod=14).alias("atr"),
    plta.cdlengulfing().alias("engulfing"),  # Int32, as TA-Lib reports patterns
)
```

Inputs default to the columns TA-Lib's own conventions name (`close` for a single series,
`open`/`high`/`low`/`close`/`volume` for price functions), parameters default to TA-Lib's
values, and multi-output functions return a struct with TA-Lib's output names. Nulls and
leading NaN rows are handled as ta-lib-python does: the output is NaN (or 0 for integer
outputs) until the function has enough data.

## How it works

The design is described in [ARCHITECTURE.md](ARCHITECTURE.md). In short: TA-Lib
describes its own functions through its *abstract interface*: inputs, parameters
with defaults, outputs, group, hint. This library has **one** Rust expression that runs
any TA-Lib function by name through that interface, and builds the Python API from the
same metadata at import time. No function is written by hand, so a new TA-Lib release is
a submodule bump:

```
cd ta-lib && git checkout v0.7.1 && cd ..
uv sync                                  # builds the extension
uv run python -m polars_talib._stubs     # regenerate the .pyi stubs
uv run pytest
```

TA-Lib is compiled from the `ta-lib` submodule by `build.rs`; nothing is downloaded at
build time.

## Install

Windows x64, Python 3.10 or newer, from the wheel attached to a
[release](https://github.com/meet-brad-ch/polars-talib/releases):

```
pip install https://github.com/meet-brad-ch/polars-talib/releases/download/v0.1.0/polars_talib-0.1.0-cp310-abi3-win_amd64.whl
```

## Tests

The oracle is ta-lib-python built on the same TA-Lib version. Every function is checked
for the exact signature TA-Lib declares and for bit-identical values on float64 and float32
input, on a synthetic frame with leading NaN rows and a null, and on TA-Lib's own 252-bar
reference data. The two functions TA-Lib does not have are checked against their
definitions: `hma` against the WMA composition, `supersmoother` against the recursion.

## Beyond TA-Lib

`hma` (Hull Moving Average) is a composition of `wma` calls in Python. `supersmoother`
(Ehlers' 2-pole low-pass filter, with AmiBroker's IIR() coefficients) is a Rust expression
of its own in `src/extra.rs`. New indicators follow the same two routes; the TA-Lib layer
is never touched.

```
git clone --recurse-submodules https://github.com/meet-brad-ch/polars-talib
uv sync                                  # builds the extension
uv run pytest
```

Needs a Rust toolchain and the Visual Studio C++ build tools.

The idea of exposing TA-Lib as Polars expressions comes from
[Yvictor/polars_ta_extension](https://github.com/Yvictor/polars_ta_extension).
