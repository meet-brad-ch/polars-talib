//! The one Polars expression: `call` runs any TA-Lib function, named in its kwargs, on the
//! input series it is given.

use std::collections::BTreeMap;

use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use serde::Deserialize;

use crate::talib::{Column, Function, Number, Output};

#[derive(Deserialize)]
#[serde(untagged)]
enum Value {
    Int(i64),
    Float(f64),
}

/// Kwargs of `call`: which TA-Lib function, and its parameters by name.
#[derive(Deserialize)]
struct Call {
    name: String,
    params: BTreeMap<String, Value>,
}

impl Call {
    fn function(&self) -> PolarsResult<Function> {
        Function::lookup(&self.name).map_err(|e| polars_err!(ComputeError: "{e}"))
    }

    /// Parameter values in TA-Lib's declaration order.
    fn values(&self, function: &Function) -> PolarsResult<Vec<Number>> {
        function
            .params
            .iter()
            .map(|p| match self.params.get(&p.name) {
                Some(Value::Int(v)) => Ok(Number::Int(*v)),
                Some(Value::Float(v)) => Ok(Number::Float(*v)),
                None => polars_bail!(ComputeError: "{}: missing parameter {}", self.name, p.name),
            })
            .collect()
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

/// An input series as the `f64` values TA-Lib reads: nulls become NaN.
fn column(series: &Series) -> PolarsResult<Vec<f64>> {
    Ok(series.cast(&DataType::Float64)?.f64()?.iter().map(|v| v.unwrap_or(f64::NAN)).collect())
}

fn series(name: PlSmallStr, leading: usize, output: Column) -> Series {
    match output {
        Column::Real(v) => {
            let mut full = vec![f64::NAN; leading];
            full.extend(v);
            Float64Chunked::from_vec(name, full).into_series()
        }
        Column::Integer(v) => {
            let mut full = vec![0i32; leading];
            full.extend(v);
            Int32Chunked::from_vec(name, full).into_series()
        }
    }
}

#[polars_expr(output_type_func_with_kwargs = output_type)]
fn call(inputs: &[Series], kwargs: Call) -> PolarsResult<Series> {
    let function = kwargs.function()?;
    if inputs.len() != function.width() {
        polars_bail!(ComputeError: "{}: expects {} input series, got {}", function.name, function.width(), inputs.len());
    }
    let values = kwargs.values(&function)?;
    let columns = inputs.iter().map(column).collect::<PolarsResult<Vec<_>>>()?;
    let n = columns[0].len();
    // TA-Lib does not understand NaN: skip the leading rows where any input is NaN, as
    // ta-lib-python does, and leave those rows at NaN / 0 in the output.
    let begin = (0..n).find(|&i| columns.iter().all(|c| !c[i].is_nan())).unwrap_or(n);
    let slices: Vec<&[f64]> = columns.iter().map(|c| &c[begin..]).collect();
    let outputs = function.call(&slices, &values, begin).map_err(|e| polars_err!(ComputeError: "{e}"))?;
    let name = inputs[0].name().clone();
    if function.outputs.len() == 1 {
        return Ok(series(name, begin, outputs.into_iter().next().unwrap()));
    }
    let fields: Vec<Series> = function
        .outputs
        .iter()
        .zip(outputs)
        .map(|(o, out)| series(o.name.as_str().into(), begin, out))
        .collect();
    Ok(StructChunked::from_series(name, n, fields.iter())?.into_series())
}
