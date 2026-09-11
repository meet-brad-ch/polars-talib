# Architecture

This document describes how polars-talib is built and why. It uses one name for each
thing. A *function* is one of the 161 indicators that TA-Lib provides. An *expression* is
a Polars `Expr`. The *plugin* is the compiled module `polars_talib._polars_talib`.

## 1. The idea

TA-Lib describes each of its functions at run time. This description is the *abstract
interface* in `ta_abstract.h`. For a function name, it gives:

- the inputs, as single series or as price bundles (open, high, low, close, volume),
- the parameters, with their type (integer or real) and their default value,
- the outputs, with their type (integer or real),
- the group and a one-line hint.

polars-talib reads this description and lets it drive everything. One Rust expression runs
any function by name. Python builds the public API from the same description at import
time. No function is written by hand. A new TA-Lib release adds its new functions without
a code change.

## 2. The parts

```
ta-lib/                        git submodule, TA-Lib C source at a release tag
build.rs                       compiles the submodule into a static library
src/ffi.rs                     C declarations of the abstract interface (22 functions)
src/talib.rs                   safe layer: Function (metadata) and Function::call
src/plugin.rs                  the one expression, `call`
src/extra.rs                   expressions for indicators TA-Lib does not have
src/lib.rs                     the Python module: version(), functions()
python/polars_talib/_build.py  builds a Python function from each description
python/polars_talib/<group>.py ten modules, one per TA-Lib group
python/polars_talib/<group>.pyi generated type stubs for the same modules
python/polars_talib/_stubs.py  the stub generator
python/polars_talib/__init__.py exports, get_functions, hma, supersmoother
tests/                         pytest, oracle is ta-lib-python on the same TA-Lib
```

### 2.1 TA-Lib as a dependency

The C source is not copied into this repository. The `ta-lib` submodule points at a
release tag of `TA-Lib/ta-lib`. `build.rs` compiles the five source directories that
TA-Lib's own CMake build puts into its static library. It uses the `cc` crate and the MSVC
compiler. Nothing is downloaded at build time.

To move to a new TA-Lib release:

1. Check out the new tag inside `ta-lib`.
2. Run `uv sync`. This rebuilds the plugin.
3. Run `uv run python -m polars_talib._stubs`. This regenerates the stubs.
4. Run `uv run pytest`. The coverage test lists the functions the new release added.

### 2.2 The C boundary (`src/ffi.rs`)

`ffi.rs` declares only the abstract interface: 22 C functions and 7 structs. It does not
declare the 161 indicator functions, so the crate does not need bindgen or libclang. The
declarations follow the headers of the pinned submodule. If TA-Lib changes the abstract
interface, this is the one file to update.

### 2.3 The safe layer (`src/talib.rs`)

`Function::lookup(name)` asks TA-Lib for the description of one function and stores it in
plain Rust values. This happens once per function: the first use builds a table of every
function, and `Function::get(name)` serves every later call from it without allocating.
The description holds:

- `inputs`: a list of `Input::Real(name)` or `Input::Price(parts)`,
- `params`: name, integer flag, default value, hint,
- `outputs`: name, integer flag.

Names are spelled the way ta-lib-python spells them. `optInFastPeriod` becomes
`fastperiod`. `outRealUpperBand` becomes `upperband`. The function `plain` does this.

`Function::all()` lists every function, group by group, in TA-Lib's order.

`Function::call(columns, values, offset)` runs the function:

1. Allocate a TA-Lib parameter holder.
2. Bind each input series in declaration order. A price input takes one series per
   component.
3. Set each parameter. An integer parameter refuses a fractional value.
4. Ask TA-Lib for the lookback. A negative lookback means the parameters are invalid.
5. If the lookback is not shorter than the data, return outputs of NaN (real) or 0
   (integer), `offset` rows longer than the input. This is not an error.
6. Otherwise allocate each output at that full length, fill only the first `offset` plus
   lookback rows, and let TA-Lib write the rest into the reserved capacity. This is the
   column the caller returns; nothing copies or fills it again.
8. For MAXINDEX, MININDEX and MINMAXINDEX, add `offset` to each position. These are the
   only functions whose output is a position in the input.

Every TA-Lib return code other than success becomes an `Error` that carries TA-Lib's own
enum name, for example `TA_BAD_PARAM`.

### 2.4 The expression (`src/plugin.rs`)

The plugin exports one expression, `call`. Its kwargs carry the function name and the
parameters by name. The input series arrive in declaration order.

At plan time, Polars asks for the output type. `output_type` looks the function up and
answers: `Float64` for one real output, `Int32` for one integer output, and a `Struct` for
several outputs. The struct fields carry TA-Lib's output names.

At run time, `call` does the following:

1. Take the function from the table and check the number of input series.
2. Take each input as `f64` values. A `Float64` column in one chunk without nulls is
   borrowed as it is, without a copy. Anything else is cast to `Float64` and copied chunk
   by chunk; nulls become NaN.
3. Find the first row where no input is NaN. Rows before it are skipped. This is what
   ta-lib-python does. TA-Lib itself does not understand NaN.
4. Run `Function::call` on the remaining rows, with the number of skipped rows as `offset`.
   The outputs come back full length, the skipped rows already NaN or 0.
5. Return one series, or a struct of series.

The expression is not elementwise. Polars therefore evaluates it once per group under
`.over()` and once per frame otherwise.

### 2.5 Indicators beyond TA-Lib (`src/extra.rs`)

An indicator that TA-Lib does not have takes one of two routes:

- If it is a composition of TA-Lib functions, it is a Python function in `__init__.py`.
  `hma` is three `wma` expressions. It contains no arithmetic of its own, and TA-Lib's
  `wma` is its oracle.
- If it is new arithmetic, it is a Rust expression in `src/extra.rs` with a Python wrapper
  in `__init__.py`. `supersmoother` is Ehlers' 2-pole filter. Its test is a numpy version
  of the same recursion.

The TA-Lib layer is never changed for either route. TA-Lib's C source is never changed.

### 2.6 The Python module (`src/lib.rs`)

`lib.rs` initializes TA-Lib when Python imports the plugin. It exports two functions:
`version()` returns TA-Lib's version string, and `functions()` returns the description of
every function as a list of dicts.

### 2.7 The Python API (`python/polars_talib/_build.py`)

`_build.py` turns each description into a Python function with a real signature:

1. `specs()` reads `functions()` once and keeps the result as `Spec` records. It orders
   the groups as ta-lib-python orders them.
2. `signature(spec)` builds an `inspect.Signature`. The input series come first, one
   parameter per series. A single series defaults to `pl.col("close")`, the two series of
   a pair default to `high` and `low`, and price components default to the column of their
   own name. The parameters come next with TA-Lib's defaults.
3. `function(spec)` returns a callable with that signature and a docstring built from the
   hint, the group, the parameter hints and the output names.
4. `group(name)` returns the functions of one TA-Lib group.

Each group module is three lines. It asks `_build` for its group and puts the functions
in its namespace. `__init__.py` re-exports the ten modules.

`expression(name, inputs, kwargs)` is the one call into Polars' plugin registry. Both the
generated functions and the wrappers in `__init__.py` use it.

### 2.8 Type stubs (`_stubs.py`)

Editors and type checkers cannot see functions that are built at import time. `_stubs.py`
renders one `.pyi` file per group module from the same `Spec` records. The stubs are
committed. A test fails while a committed stub differs from a fresh render.

## 3. Rules the code keeps

- Inputs are `Float64` inside the plugin. Integer and `Float32` columns are cast.
- A window longer than the data gives NaN or 0 rows, never an error. This keeps `.over()`
  groups that are shorter than the window from failing the whole query.
- Invalid parameters raise `ComputeError` with TA-Lib's enum name in the message.
- A fractional value for an integer parameter raises. It is not truncated.
- Output names, parameter names and defaults are TA-Lib's. Nothing is renamed by hand.
- There are no fallbacks. A missing function, a wrong number of inputs or an unknown
  parameter is an error.

## 4. Tests

The oracle is ta-lib-python built on the same TA-Lib release. It reads the same
description through its own abstract layer, so it is a second, independent path to the
same C code. Every test is parametrized over the descriptions. No test names a function
by hand, except the tests for `hma` and `supersmoother`.

| File | What it proves |
|---|---|
| `test_coverage.py` | Every ta-lib-python function exists here, with the same parameters, defaults, types, output names and groups. |
| `test_values.py` | Every function gives bit-identical values, on `Float64` and `Float32`, for the defaults and a short window, on two frames. Grouped evaluation equals per-group evaluation. |
| `test_edges.py` | Short windows, invalid parameters, fractional integers, integer columns, lazy and streaming evaluation. |
| `test_api.py` | `hma` and `supersmoother` against their definitions. Stubs are current. Each function lives in its group module. |

The two frames are in `tests/data.py`: a synthetic frame with seven leading NaN rows, a
null in the middle and a `periods` column, and TA-Lib's own 252-bar daily reference series
from its regression tool, parsed from the submodule.

## 5. Build and CI

- Rust stable with the MSVC target, the Visual Studio C++ build tools, and `uv`.
- `uv sync` builds the plugin through maturin. `[tool.uv] cache-keys` lists the Rust
  sources, so a `.rs` change triggers a rebuild.
- The wheel is `abi3` for Python 3.10 and newer, `win_amd64` only.
- CI runs on `windows-latest`: `uv sync`, ruff, ruff format, mypy strict, pytest, then
  `maturin build`. A `v*` tag attaches the wheel to a GitHub release.

## 6. Limits

- Windows x64 only. The `cc` build would likely work elsewhere, but nothing tests it.
- TA-Lib is single-threaded per call. Polars runs independent expressions in parallel.
- A column with nulls, in several chunks, or not `Float64` is copied once per call. A
  dense single-chunk `Float64` column is not.

### 6.1 Would rewriting the functions in Rust be faster?

No. Measured once with a throwaway Rust EMA, bit-identical to `TA_EMA`, on one machine
(24 threads, polars 1.44, TA-Lib 0.7.1, period 30, minimum of 15 runs). Both paths went
through the same `call` machinery, before the output fill and the function table were
trimmed; both have become about 10 % faster since, in step.

| rows | `ema` through TA-Lib | the same loop in Rust | `ewm_mean` (Polars, seeds differently) |
|---|---:|---:|---:|
| 100 000 | 0.20 ms | 0.19 ms | 0.42 ms |
| 1 000 000 | 2.9 ms | 2.9 ms | 4.0 ms |
| 10 000 000 | 29 ms | 30 ms | 42 ms |
| 2 000 groups × 500 rows, `.over()` | 8.5 ms | 8.2 ms | 6.2 ms |

The C loop behind the abstract interface and the Rust loop cost the same. A rewrite of the
161 functions would gain nothing and give up the property that no function is written by
hand.

The measurement first looked different. Before `column` borrowed dense columns and
`Function::call` wrote into the final buffer, the C path took 6.9 ms and the Rust path
5.8 ms on one million rows, both behind `ewm_mean`. The copies around the loop, shared by
both paths, cost more than the loop itself. Removing them halved every call; the C
boundary was never the cost.

Under `.over()` with many small groups, both paths sit about 3.5 ms above the cost of a
plain arithmetic expression over the same groups. That is Polars' per-call plugin
dispatch (the kwargs are deserialized on every call) plus TA-Lib's parameter holder,
about 1.7 µs per group in total.

### 6.2 Against ta-lib-python

ta-lib-python runs the same C code on numpy arrays, and `to_numpy()` is zero-copy for a
dense float column, so one indicator on one series costs the same on either route. The
plugin wins where Polars does the work around the call: independent expressions run in
parallel, and `.over()` runs the function per group without a Python call. Median of 10
runs, same machine:

| scenario | plugin | ta-lib-python on `to_numpy` | ta-lib-python in `map_batches` |
|---|---:|---:|---:|
| 1 indicator, 1M rows | 2.7 ms | 2.6 ms | 2.6 ms |
| 8 indicators in one select, 1M rows | 13.5 ms | 32.6 ms | 33.4 ms |
| 8 indicators, 10M rows | 128 ms | 334 ms | 339 ms |
| 1 indicator over 2 000 symbols | 10.5 ms | 8.9 ms, hand-written loop | 32.4 ms |
| 1 indicator over 20 000 symbols | 69 ms | 51 ms, hand-written loop | 291 ms |
