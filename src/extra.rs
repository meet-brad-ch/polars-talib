//! Indicators TA-Lib does not have, each its own expression. They share the input
//! conventions of the TA-Lib functions: nulls are NaN, leading NaN rows are skipped and
//! stay NaN in the output.

use std::f64::consts::PI;

use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use serde::Deserialize;

use crate::plugin::column;

/// sqrt(2) as AmiBroker's IIR() documentation writes it, so results agree with AFL.
const SQRT2: f64 = 1.41421;

#[derive(Deserialize)]
struct Period {
    period: f64,
}

/// John Ehlers' 2-pole SuperSmoother, a low-pass IIR filter: each output is the average
/// of the current and previous input weighted by `b0`, plus the two previous outputs
/// weighted by `a1` and `a2`. Seeded with the first two inputs, as AmiBroker's IIR() is.
#[polars_expr(output_type = Float64)]
fn supersmoother(inputs: &[Series], kwargs: Period) -> PolarsResult<Series> {
    let period = kwargs.period;
    if !(period > 0.0) {
        polars_bail!(ComputeError: "supersmoother: period must be positive, got {period}");
    }
    let c1 = SQRT2 * PI / period;
    let c2 = (-c1).exp();
    let a1 = 2.0 * c2 * c1.cos();
    let a2 = -c2 * c2;
    let b0 = (1.0 - a1 - a2) / 2.0;

    let x = column(&inputs[0])?;
    let begin = x.iter().position(|v| !v.is_nan()).unwrap_or(x.len());
    let mut y = x.clone();
    for i in begin + 2..x.len() {
        y[i] = b0 * x[i] + b0 * x[i - 1] + a1 * y[i - 1] + a2 * y[i - 2];
    }
    Ok(Float64Chunked::from_vec(inputs[0].name().clone(), y).into_series())
}
