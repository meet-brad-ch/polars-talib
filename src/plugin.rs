//! The one Polars expression: `call` runs any TA-Lib function, named in its kwargs, on the
//! input series it is given.

use std::borrow::Cow;
use std::collections::BTreeMap;

use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use serde::Deserialize;

use crate::talib::{Column, Function, Number, Output};

/// Kwargs of `call`: which TA-Lib function, and its parameters by name.
#[derive(Deserialize)]
struct Call {
    name: String,
    params: BTreeMap<String, Number>,
}

impl Call {
    fn function(&self) -> PolarsResult<&'static Function> {
        Function::get(&self.name).map_err(|e| polars_err!(ComputeError: "{e}"))
    }

    /// Parameter values in TA-Lib's declaration order. Every declared parameter must be
    /// given, and nothing else.
    fn values(&self, function: &Function) -> PolarsResult<Vec<Number>> {
        let values = function
            .params
            .iter()
            .map(|p| {
                self.params
                    .get(&p.name)
                    .copied()
                    .ok_or_else(|| polars_err!(ComputeError: "{}: missing parameter {}", self.name, p.name))
            })
            .collect::<PolarsResult<Vec<_>>>()?;
        if self.params.len() != values.len() {
            let unknown: Vec<&str> = self
                .params
                .keys()
                .filter(|k| !function.params.iter().any(|p| &p.name == *k))
                .map(String::as_str)
                .collect();
            polars_bail!(ComputeError: "{}: unknown parameter {}", self.name, unknown.join(", "));
        }
        Ok(values)
    }
}

fn dtype(output: &Output) -> DataType {
    if output.integer {
        DataType::Int32
    } else {
        DataType::Float64
    }
}

fn output_type(fields: &[Field], kwargs: Call) -> PolarsResult<Field> {
    let function = kwargs.function()?;
    let name = fields[0].name().clone();
    Ok(match function.outputs.as_slice() {
        [single] => Field::new(name, dtype(single)),
        many => Field::new(name, DataType::Struct(many.iter().map(|o| Field::new(o.name.as_str().into(), dtype(o))).collect())),
    })
}

/// An input series as the `f64` values TA-Lib reads: nulls become NaN. A `Float64` column
/// in one chunk without nulls is borrowed as it is; anything else is cast and copied chunk
/// by chunk, the null rows set to NaN afterwards.
pub(crate) fn column(series: &Series) -> PolarsResult<Cow<'_, [f64]>> {
    if let Ok(ca) = series.f64() {
        if let Ok(slice) = ca.cont_slice() {
            return Ok(Cow::Borrowed(slice));
        }
    }
    let cast = series.cast(&DataType::Float64)?;
    let mut values = Vec::with_capacity(cast.len());
    for array in cast.f64()?.downcast_iter() {
        let start = values.len();
        values.extend_from_slice(array.values().as_slice());
        if let Some(validity) = array.validity() {
            for (i, valid) in validity.iter().enumerate() {
                if !valid {
                    values[start + i] = f64::NAN;
                }
            }
        }
    }
    Ok(Cow::Owned(values))
}

fn series(name: PlSmallStr, output: Column) -> Series {
    match output {
        Column::Real(v) => Float64Chunked::from_vec(name, v).into_series(),
        Column::Integer(v) => Int32Chunked::from_vec(name, v).into_series(),
    }
}

#[polars_expr(output_type_func_with_kwargs = output_type)]
fn call(inputs: &[Series], kwargs: Call) -> PolarsResult<Series> {
    let function = kwargs.function()?;
    let values = kwargs.values(function)?;
    let columns = inputs.iter().map(column).collect::<PolarsResult<Vec<_>>>()?;
    let n = function.rows(columns.iter().map(|c| c.len())).map_err(|e| polars_err!(ComputeError: "{e}"))?;
    // TA-Lib does not understand NaN: skip the leading rows where any input is NaN, as
    // ta-lib-python does, and leave those rows at NaN / 0 in the output.
    let begin = (0..n).find(|&i| columns.iter().all(|c| !c[i].is_nan())).unwrap_or(n);
    let slices: Vec<&[f64]> = columns.iter().map(|c| &c[begin..]).collect();
    let outputs = function.call(&slices, &values, begin).map_err(|e| polars_err!(ComputeError: "{e}"))?;
    let name = inputs[0].name().clone();
    if function.outputs.len() == 1 {
        return Ok(series(name, outputs.into_iter().next().unwrap()));
    }
    let fields: Vec<Series> = function
        .outputs
        .iter()
        .zip(outputs)
        .map(|(o, out)| series(o.name.as_str().into(), out))
        .collect();
    Ok(StructChunked::from_series(name, n, fields.iter())?.into_series())
}
