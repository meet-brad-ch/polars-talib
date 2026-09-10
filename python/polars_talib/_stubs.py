"""Renders one ``.pyi`` per group module, so editors and type checkers see the signatures
that ``_build`` creates at import time.

Run ``python -m polars_talib._stubs`` after moving the ``ta-lib`` submodule; a test fails
while the committed stubs are stale.
"""

from __future__ import annotations

from ._build import MODULES, PLUGIN, Spec, specs

HEADER = "from polars import Expr\nfrom polars._typing import IntoExpr\n"


def _function(spec: Spec) -> str:
    columns = [f"{c}: IntoExpr = ..." for c in spec.columns]
    params = [f"{p.name}: {'int' if p.integer else 'float'} = {p.value!r}" for p in spec.params]
    doc = spec.doc.replace("\n", "\n    ")
    return f'def {spec.python_name}({", ".join(columns + params)}) -> Expr:\n    """{doc}"""\n'


def render(group: str) -> str:
    return "\n".join([HEADER] + [_function(s) for s in specs() if s.group == group])


def main() -> None:
    for group, module in MODULES.items():
        (PLUGIN / f"{module}.pyi").write_text(render(group), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
