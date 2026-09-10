//! Safe layer over the abstract interface: a `Function` is TA-Lib's own description of one
//! TA function (inputs, parameters, outputs), and `call` runs it on plain `f64` columns.
//! Nothing here knows any function by name.

use std::ffi::{CStr, CString};
use std::fmt;
use std::os::raw::{c_char, c_uint};

use crate::ffi::*;

#[derive(Debug)]
pub struct Error(pub String);

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&self.0)
    }
}

fn check(code: TA_RetCode, what: &str) -> Result<(), Error> {
    if code == TA_SUCCESS {
        return Ok(());
    }
    let mut info = TA_RetCodeInfo { enum_str: std::ptr::null(), info_str: std::ptr::null() };
    // SAFETY: TA_SetRetCodeInfo fills both pointers with static strings for any code.
    unsafe { TA_SetRetCodeInfo(code, &mut info) };
    Err(Error(format!("{what}: {} ({})", text(info.enum_str), text(info.info_str))))
}

/// A NUL-terminated static string owned by TA-Lib.
fn text(ptr: *const c_char) -> String {
    // SAFETY: TA-Lib hands out pointers to static, NUL-terminated ASCII.
    unsafe { CStr::from_ptr(ptr) }.to_string_lossy().into_owned()
}

/// TA-Lib names the way ta-lib-python spells them: the Hungarian prefix goes and the rest
/// is lower-cased (`optInFastPeriod` → `fastperiod`, `inReal0` → `real0`, `outMACD` →
/// `macd`). Outputs also drop a leading `Real` when something follows it
/// (`outRealUpperBand` → `upperband`, `outReal` → `real`).
fn plain(raw: &str, prefix: &str) -> String {
    let name = raw.strip_prefix(prefix).unwrap_or(raw);
    let name = match (prefix, name.strip_prefix("Real")) {
        ("out", Some(rest)) if !rest.is_empty() => rest,
        _ => name,
    };
    name.to_ascii_lowercase()
}

pub fn initialize() -> Result<(), Error> {
    check(unsafe { TA_Initialize() }, "TA_Initialize")
}

pub fn version() -> String {
    text(unsafe { TA_GetVersionString() })
}

/// One declared input: a single real series, or a price bundle of the named components.
#[derive(Debug, Clone)]
pub enum Input {
    Real(String),
    Price(Vec<&'static str>),
}

impl Input {
    /// How many series this input consumes from the plugin's argument list.
    pub fn width(&self) -> usize {
        match self {
            Input::Real(_) => 1,
            Input::Price(parts) => parts.len(),
        }
    }
}

#[derive(Debug, Clone)]
pub struct Param {
    pub name: String,
    pub integer: bool,
    pub default: f64,
    pub hint: String,
}

#[derive(Debug, Clone)]
pub struct Output {
    pub name: String,
    pub integer: bool,
}

/// A parameter value as supplied by the caller; integers stay integers so an integer
/// parameter given a fraction is an error, not a silent truncation.
#[derive(Debug, Clone, Copy)]
pub enum Number {
    Int(i64),
    Float(f64),
}

/// Result columns, one per declared output, each as long as the input.
pub enum Column {
    Real(Vec<f64>),
    Integer(Vec<i32>),
}

/// The functions whose integer output is a position in the input.
const POSITIONAL: [&str; 3] = ["MAXINDEX", "MININDEX", "MINMAXINDEX"];

#[derive(Debug, Clone)]
pub struct Function {
    handle: *const TA_FuncHandle,
    pub name: String,
    pub group: String,
    pub hint: String,
    pub inputs: Vec<Input>,
    pub params: Vec<Param>,
    pub outputs: Vec<Output>,
    /// Integer outputs are positions in the input (see `call`'s `offset`).
    positional: bool,
}

impl Function {
    pub fn lookup(name: &str) -> Result<Function, Error> {
        let c_name = CString::new(name).map_err(|e| Error(e.to_string()))?;
        let mut handle = std::ptr::null();
        check(unsafe { TA_GetFuncHandle(c_name.as_ptr(), &mut handle) }, &format!("TA_GetFuncHandle({name})"))?;
        let mut info = std::ptr::null();
        check(unsafe { TA_GetFuncInfo(handle, &mut info) }, "TA_GetFuncInfo")?;
        // SAFETY: TA-Lib returned a valid pointer into its static function table.
        let info = unsafe { &*info };
        Ok(Function {
            handle,
            positional: POSITIONAL.contains(&name),
            name: text(info.name),
            group: text(info.group),
            hint: text(info.hint),
            inputs: (0..info.nb_input).map(|i| Self::input(handle, i)).collect::<Result<_, _>>()?,
            params: (0..info.nb_opt_input).map(|i| Self::param(handle, i)).collect::<Result<_, _>>()?,
            outputs: (0..info.nb_output).map(|i| Self::output(handle, i)).collect::<Result<_, _>>()?,
        })
    }

    /// Every function TA-Lib knows, group by group in TA-Lib's own order (the order
    /// ta-lib-python lists them in too).
    pub fn all() -> Result<Vec<Function>, Error> {
        let mut functions = Vec::new();
        for group in strings(|t| unsafe { TA_GroupTableAlloc(t) }, TA_GroupTableFree)? {
            let c_group = CString::new(group).map_err(|e| Error(e.to_string()))?;
            for name in strings(|t| unsafe { TA_FuncTableAlloc(c_group.as_ptr(), t) }, TA_FuncTableFree)? {
                functions.push(Function::lookup(&name)?);
            }
        }
        Ok(functions)
    }

    fn input(handle: *const TA_FuncHandle, i: c_uint) -> Result<Input, Error> {
        let mut info = std::ptr::null();
        check(unsafe { TA_GetInputParameterInfo(handle, i, &mut info) }, "TA_GetInputParameterInfo")?;
        let info = unsafe { &*info };
        Ok(match info.kind {
            TA_INPUT_PRICE => Input::Price(
                TA_IN_PRICE.iter().filter(|(bit, _)| info.flags & bit != 0).map(|(_, part)| *part).collect(),
            ),
            TA_INPUT_REAL => Input::Real(plain(&text(info.param_name), "in")),
            kind => return Err(Error(format!("unsupported input kind {kind}"))),
        })
    }

    fn param(handle: *const TA_FuncHandle, i: c_uint) -> Result<Param, Error> {
        let mut info = std::ptr::null();
        check(unsafe { TA_GetOptInputParameterInfo(handle, i, &mut info) }, "TA_GetOptInputParameterInfo")?;
        let info = unsafe { &*info };
        Ok(Param {
            name: plain(&text(info.param_name), "optIn"),
            integer: matches!(info.kind, TA_OPTINPUT_INTEGER_RANGE | TA_OPTINPUT_INTEGER_LIST),
            default: info.default_value,
            hint: text(info.hint),
        })
    }

    fn output(handle: *const TA_FuncHandle, i: c_uint) -> Result<Output, Error> {
        let mut info = std::ptr::null();
        check(unsafe { TA_GetOutputParameterInfo(handle, i, &mut info) }, "TA_GetOutputParameterInfo")?;
        let info = unsafe { &*info };
        Ok(Output { name: plain(&text(info.param_name), "out"), integer: info.kind == TA_OUTPUT_INTEGER })
    }

    /// Number of series the caller must pass, in declaration order.
    pub fn width(&self) -> usize {
        self.inputs.iter().map(Input::width).sum()
    }

    /// Run the function. `columns` are the input series in declaration order, all of equal
    /// length; `values` are the parameters in declaration order. Rows before the function's
    /// lookback hold NaN (real) or 0 (integer). A window longer than the data is not an
    /// error: every row is then NaN / 0. `offset` is the number of rows the caller cut off
    /// the front of its data; positions reported by the MAXINDEX family count from the
    /// caller's first row, as ta-lib-python's do.
    pub fn call(&self, columns: &[&[f64]], values: &[Number], offset: usize) -> Result<Vec<Column>, Error> {
        let n = columns.first().map_or(0, |c| c.len());
        assert!(columns.len() == self.width() && columns.iter().all(|c| c.len() == n));
        let holder = Holder::new(self.handle)?;
        let mut next = 0;
        for (i, input) in self.inputs.iter().enumerate() {
            let series = &columns[next..next + input.width()];
            next += input.width();
            let code = match input {
                Input::Real(_) => unsafe { TA_SetInputParamRealPtr(holder.0, i as c_uint, series[0].as_ptr()) },
                Input::Price(parts) => {
                    let mut ptr = [std::ptr::null(); 6];
                    for (slot, (_, part)) in ptr.iter_mut().zip(TA_IN_PRICE.iter()) {
                        if let Some(k) = parts.iter().position(|p| p == part) {
                            *slot = series[k].as_ptr();
                        }
                    }
                    unsafe { TA_SetInputParamPricePtr(holder.0, i as c_uint, ptr[0], ptr[1], ptr[2], ptr[3], ptr[4], ptr[5]) }
                }
            };
            check(code, "TA_SetInputParam")?;
        }
        if values.len() != self.params.len() {
            return Err(Error(format!("{} takes {} parameters, {} given", self.name, self.params.len(), values.len())));
        }
        for (i, (param, value)) in self.params.iter().zip(values).enumerate() {
            let code = match (param.integer, value) {
                (true, Number::Int(v)) => unsafe { TA_SetOptInputParamInteger(holder.0, i as c_uint, *v as TA_Integer) },
                (true, Number::Float(v)) => return Err(Error(format!("{}: {} must be an integer, got {v}", self.name, param.name))),
                (false, Number::Int(v)) => unsafe { TA_SetOptInputParamReal(holder.0, i as c_uint, *v as f64) },
                (false, Number::Float(v)) => unsafe { TA_SetOptInputParamReal(holder.0, i as c_uint, *v) },
            };
            check(code, &format!("{}: {}", self.name, param.name))?;
        }
        let mut lookback: TA_Integer = 0;
        check(unsafe { TA_GetLookback(holder.0, &mut lookback) }, "TA_GetLookback")?;
        let mut outputs: Vec<Column> = self
            .outputs
            .iter()
            .map(|o| if o.integer { Column::Integer(vec![0; n]) } else { Column::Real(vec![f64::NAN; n]) })
            .collect();
        // A negative lookback means the parameters are invalid; the call below then returns
        // TA-Lib's own error for them.
        if lookback >= n as TA_Integer {
            return Ok(outputs);
        }
        let lookback = lookback.max(0) as usize;
        for (i, out) in outputs.iter_mut().enumerate() {
            let code = match out {
                Column::Real(v) => unsafe { TA_SetOutputParamRealPtr(holder.0, i as c_uint, v[lookback..].as_mut_ptr()) },
                Column::Integer(v) => unsafe { TA_SetOutputParamIntegerPtr(holder.0, i as c_uint, v[lookback..].as_mut_ptr()) },
            };
            check(code, "TA_SetOutputParam")?;
        }
        let (mut beg, mut count) = (0, 0);
        check(unsafe { TA_CallFunc(holder.0, 0, n as TA_Integer - 1, &mut beg, &mut count) }, &self.name)?;
        assert!(beg as usize == lookback && lookback + count as usize == n, "{}: unexpected output range", self.name);
        if self.positional {
            for out in outputs.iter_mut() {
                if let Column::Integer(v) = out {
                    v[lookback..].iter_mut().for_each(|i| *i += offset as i32);
                }
            }
        }
        Ok(outputs)
    }
}

/// The strings of a TA-Lib table (groups, or the functions of one group), freed again
/// before returning.
fn strings(
    alloc: impl FnOnce(*mut *mut TA_StringTable) -> TA_RetCode,
    free: unsafe extern "C" fn(*mut TA_StringTable) -> TA_RetCode,
) -> Result<Vec<String>, Error> {
    let mut table = std::ptr::null_mut();
    check(alloc(&mut table), "TA_*TableAlloc")?;
    // SAFETY: TA-Lib filled `table` with `size` valid C strings; freed right after reading.
    let names = unsafe {
        let t = &*table;
        (0..t.size as usize).map(|i| text(*t.string.add(i))).collect()
    };
    check(unsafe { free(table) }, "TA_*TableFree")?;
    Ok(names)
}

/// Owns a `TA_ParamHolder` for the duration of one call.
struct Holder(*mut TA_ParamHolder);

impl Holder {
    fn new(handle: *const TA_FuncHandle) -> Result<Holder, Error> {
        let mut params = std::ptr::null_mut();
        check(unsafe { TA_ParamHolderAlloc(handle, &mut params) }, "TA_ParamHolderAlloc")?;
        Ok(Holder(params))
    }
}

impl Drop for Holder {
    fn drop(&mut self) {
        unsafe { TA_ParamHolderFree(self.0) };
    }
}
