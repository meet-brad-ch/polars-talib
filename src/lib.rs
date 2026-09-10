//! `polars_talib._polars_talib`: the plugin binary (see `plugin.rs`) plus the two things the
//! Python side needs from TA-Lib itself, its version and the description of every function.

mod ffi;
mod plugin;
mod talib;

use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use pyo3::types::PyDict;

use talib::{Function, Input};

fn runtime_error(e: talib::Error) -> PyErr {
    PyRuntimeError::new_err(e.0)
}

#[pyfunction]
fn version() -> String {
    talib::version()
}

/// Every TA-Lib function as a dict: `name`, `group`, `hint`, `inputs` (name, price parts),
/// `params` (name, integer, default, hint) and `outputs` (name, integer).
#[pyfunction]
fn functions(py: Python<'_>) -> PyResult<Vec<Bound<'_, PyDict>>> {
    Function::all()
        .map_err(runtime_error)?
        .iter()
        .map(|f| {
            let d = PyDict::new(py);
            d.set_item("name", &f.name)?;
            d.set_item("group", &f.group)?;
            d.set_item("hint", &f.hint)?;
            let inputs: Vec<(&str, &[&str])> = f
                .inputs
                .iter()
                .map(|i| match i {
                    Input::Real(name) => (name.as_str(), &[][..]),
                    Input::Price(parts) => ("price", parts.as_slice()),
                })
                .collect();
            d.set_item("inputs", inputs)?;
            let params: Vec<(&str, bool, f64, &str)> =
                f.params.iter().map(|p| (p.name.as_str(), p.integer, p.default, p.hint.as_str())).collect();
            d.set_item("params", params)?;
            let outputs: Vec<(&str, bool)> = f.outputs.iter().map(|o| (o.name.as_str(), o.integer)).collect();
            d.set_item("outputs", outputs)?;
            Ok(d)
        })
        .collect()
}

#[pymodule]
fn _polars_talib(m: &Bound<'_, PyModule>) -> PyResult<()> {
    talib::initialize().map_err(runtime_error)?;
    m.add_function(wrap_pyfunction!(version, m)?)?;
    m.add_function(wrap_pyfunction!(functions, m)?)?;
    Ok(())
}
