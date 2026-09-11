//! Safe layer over the abstract interface: a `Function` is TA-Lib's own description of one
//! TA function (inputs, parameters, outputs), and `call` runs it on plain `f64` columns.
//! Nothing here knows any function by name.

use std::collections::HashMap;
use std::ffi::{CStr, CString};
use std::fmt;
use std::os::raw::{c_char, c_uint};
use std::sync::OnceLock;

use serde::Deserialize;

use crate::ffi::*;

#[derive(Debug, Clone)]
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
/// (`outRealUpperBand` → `upperband`, `outReal` → `real`). A name without the prefix is
/// an error: it would collide with or misname a Python parameter.
fn plain(raw: &str, prefix: &str) -> Result<String, Error> {
    let Some(name) = raw.strip_prefix(prefix) else {
        return Err(Error(format!("unexpected TA-Lib name {raw}, expected prefix {prefix}")));
    };
    let name = match (prefix, name.strip_prefix("Real")) {
        ("out", Some(rest)) if !rest.is_empty() => rest,
        _ => name,
    };
    Ok(name.to_ascii_lowercase())
}

pub fn initialize() -> Result<(), Error> {
    check(unsafe { TA_Initialize() }, "TA_Initialize")
}

pub fn version() -> String {
    text(unsafe { TA_GetVersionString() })
}

/// One declared input: a single real series, or a price bundle of the named components.
#[derive(Debug)]
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

    /// The name of each series this input consumes, in order.
    fn names(&self) -> Vec<&str> {
        match self {
            Input::Real(name) => vec![name.as_str()],
            Input::Price(parts) => parts.clone(),
        }
    }
}

#[derive(Debug)]
pub struct Param {
    pub name: String,
    pub integer: bool,
    pub default: f64,
    pub hint: String,
}

#[derive(Debug)]
pub struct Output {
    pub name: String,
    pub integer: bool,
}

/// A parameter value as supplied by the caller; integers stay integers so an integer
/// parameter given a fraction is an error, not a silent truncation.
#[derive(Debug, Clone, Copy, Deserialize)]
#[serde(untagged)]
pub enum Number {
    Int(i64),
    Float(f64),
}

impl fmt::Display for Number {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Number::Int(v) => write!(f, "{v}"),
            Number::Float(v) => write!(f, "{v:?}"),
        }
    }
}

/// Result columns, one per declared output, each `offset` rows longer than the input.
pub enum Column {
    Real(Vec<f64>),
    Integer(Vec<i32>),
}

impl Column {
    /// `len` rows of the value a row without a result holds (NaN, or 0 for integers), in
    /// one allocation with room for `capacity` rows.
    fn new(integer: bool, len: usize, capacity: usize) -> Column {
        if integer {
            let mut v = Vec::with_capacity(capacity);
            v.resize(len, 0);
            Column::Integer(v)
        } else {
            let mut v = Vec::with_capacity(capacity);
            v.resize(len, f64::NAN);
            Column::Real(v)
        }
    }
}

/// The functions whose integer output is a position in the input.
const POSITIONAL: [&str; 3] = ["MAXINDEX", "MININDEX", "MINMAXINDEX"];

#[derive(Debug)]
pub struct Function {
    /// One of TA-Lib's static function definitions.
    handle: &'static TA_FuncHandle,
    pub name: String,
    pub group: String,
    pub hint: String,
    pub inputs: Vec<Input>,
    pub params: Vec<Param>,
    pub outputs: Vec<Output>,
    /// Integer outputs are positions in the input (see `call`'s `offset`).
    positional: bool,
}

/// Every function, described once: the first use asks TA-Lib, every call after that is a
/// map lookup with no allocation. A failure to describe them is cached too.
struct Table {
    functions: Vec<Function>,
    index: HashMap<String, usize>,
}

static TABLE: OnceLock<Result<Table, Error>> = OnceLock::new();

impl Table {
    fn get() -> Result<&'static Table, Error> {
        TABLE.get_or_init(Table::build).as_ref().map_err(Error::clone)
    }

    /// Every function TA-Lib knows, group by group in TA-Lib's own order (the order
    /// ta-lib-python lists them in too).
    fn build() -> Result<Table, Error> {
        let mut functions = Vec::new();
        for group in strings(|t| unsafe { TA_GroupTableAlloc(t) }, TA_GroupTableFree)? {
            let c_group = CString::new(group).map_err(|e| Error(e.to_string()))?;
            for name in strings(|t| unsafe { TA_FuncTableAlloc(c_group.as_ptr(), t) }, TA_FuncTableFree)? {
                functions.push(Function::lookup(&name)?);
            }
        }
        let index = functions.iter().enumerate().map(|(i, f)| (f.name.clone(), i)).collect();
        Ok(Table { functions, index })
    }
}

impl Function {
    /// The description of one function, by TA-Lib's name.
    pub fn get(name: &str) -> Result<&'static Function, Error> {
        let table = Table::get()?;
        match table.index.get(name) {
            Some(&i) => Ok(&table.functions[i]),
            None => Err(Error(format!("unknown TA-Lib function {name}"))),
        }
    }

    /// Every function TA-Lib knows, in TA-Lib's order.
    pub fn table() -> Result<&'static [Function], Error> {
        Ok(&Table::get()?.functions)
    }

    fn lookup(name: &str) -> Result<Function, Error> {
        let c_name = CString::new(name).map_err(|e| Error(e.to_string()))?;
        let mut handle = std::ptr::null();
        check(unsafe { TA_GetFuncHandle(c_name.as_ptr(), &mut handle) }, &format!("TA_GetFuncHandle({name})"))?;
        // SAFETY: on success TA-Lib set `handle` to one of its static, read-only function
        // definitions, which live as long as the program.
        let handle: &'static TA_FuncHandle = unsafe { &*handle };
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

    fn input(handle: &TA_FuncHandle, i: c_uint) -> Result<Input, Error> {
        let mut info = std::ptr::null();
        check(unsafe { TA_GetInputParameterInfo(handle, i, &mut info) }, "TA_GetInputParameterInfo")?;
        let info = unsafe { &*info };
        Ok(match info.kind {
            TA_INPUT_PRICE => Input::Price(
                TA_IN_PRICE.iter().filter(|(bit, _)| info.flags & bit != 0).map(|(_, part)| *part).collect(),
            ),
            TA_INPUT_REAL => Input::Real(plain(&text(info.param_name), "in")?),
            kind => return Err(Error(format!("unsupported input kind {kind}"))),
        })
    }

    fn param(handle: &TA_FuncHandle, i: c_uint) -> Result<Param, Error> {
        let mut info = std::ptr::null();
        check(unsafe { TA_GetOptInputParameterInfo(handle, i, &mut info) }, "TA_GetOptInputParameterInfo")?;
        let info = unsafe { &*info };
        Ok(Param {
            name: plain(&text(info.param_name), "optIn")?,
            integer: matches!(info.kind, TA_OPTINPUT_INTEGER_RANGE | TA_OPTINPUT_INTEGER_LIST),
            default: info.default_value,
            hint: text(info.hint),
        })
    }

    fn output(handle: &TA_FuncHandle, i: c_uint) -> Result<Output, Error> {
        let mut info = std::ptr::null();
        check(unsafe { TA_GetOutputParameterInfo(handle, i, &mut info) }, "TA_GetOutputParameterInfo")?;
        let info = unsafe { &*info };
        Ok(Output { name: plain(&text(info.param_name), "out")?, integer: info.kind == TA_OUTPUT_INTEGER })
    }

    /// The common length of the input series given by `lengths`, or why there is none:
    /// the wrong number of series, or series of different lengths. Allocates only for
    /// the error message.
    pub fn rows(&self, lengths: impl ExactSizeIterator<Item = usize> + Clone) -> Result<usize, Error> {
        let width: usize = self.inputs.iter().map(Input::width).sum();
        if lengths.len() != width {
            let names: Vec<&str> = self.inputs.iter().flat_map(Input::names).collect();
            return Err(Error(format!(
                "{}: expects {width} input series ({}), got {}",
                self.name,
                names.join(", "),
                lengths.len()
            )));
        }
        let mut rest = lengths.clone();
        let n = rest.next().unwrap_or(0);
        if rest.any(|len| len != n) {
            let names = self.inputs.iter().flat_map(Input::names);
            let each: Vec<String> = names.zip(lengths).map(|(name, len)| format!("{name}={len}")).collect();
            return Err(Error(format!("{}: input series differ in length: {}", self.name, each.join(", "))));
        }
        Ok(n)
    }

    /// The call as TA-Lib sees it, for error messages: "SMA: timeperiod=0".
    fn describe(&self, values: &[Number]) -> String {
        let given: Vec<String> = self.params.iter().zip(values).map(|(p, v)| format!("{}={v}", p.name)).collect();
        if given.is_empty() {
            self.name.clone()
        } else {
            format!("{}: {}", self.name, given.join(", "))
        }
    }

    /// Run the function. `columns` are the input series in declaration order, all of equal
    /// length; `values` are the parameters in declaration order. `offset` is the number of
    /// rows the caller cut off the front of its data: each output column is `offset` rows
    /// longer than the input, and those rows, like the rows before the function's lookback,
    /// hold NaN (real) or 0 (integer). Positions reported by the MAXINDEX family count from
    /// the caller's first row, as ta-lib-python's do. A window longer than the data is not
    /// an error: every row is then NaN / 0.
    pub fn call(&self, columns: &[&[f64]], values: &[Number], offset: usize) -> Result<Vec<Column>, Error> {
        let n = self.rows(columns.iter().map(|c| c.len()))?;
        let full = offset + n;
        // TA-Lib indexes rows with a C int.
        let rows = i32::try_from(full)
            .map_err(|_| Error(format!("{}: {full} rows, TA-Lib handles at most {}", self.name, i32::MAX)))?;
        let skipped = offset as i32; // fits: offset <= full
        let n_rows = rows - skipped;
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
                (true, Number::Int(v)) => {
                    let v = i32::try_from(*v)
                        .map_err(|_| Error(format!("{}: {} must fit a 32-bit integer, got {v}", self.name, param.name)))?;
                    unsafe { TA_SetOptInputParamInteger(holder.0, i as c_uint, v) }
                }
                (true, Number::Float(v)) => return Err(Error(format!("{}: {} must be an integer, got {v:?}", self.name, param.name))),
                (false, Number::Int(v)) => unsafe { TA_SetOptInputParamReal(holder.0, i as c_uint, *v as f64) },
                (false, Number::Float(v)) => unsafe { TA_SetOptInputParamReal(holder.0, i as c_uint, *v) },
            };
            check(code, &format!("{}: {}", self.name, param.name))?;
        }
        let mut lookback: TA_Integer = 0;
        check(unsafe { TA_GetLookback(holder.0, &mut lookback) }, "TA_GetLookback")?;
        // A negative lookback is how TA-Lib's lookback functions report a parameter out of
        // range; TA_CallFunc would report the same, or an index error first on no rows.
        if lookback < 0 {
            return Err(Error(format!("{}: TA_BAD_PARAM (a parameter is out of range)", self.describe(values))));
        }
        if lookback >= n_rows {
            return Ok(self.outputs.iter().map(|o| Column::new(o.integer, full, full)).collect());
        }
        let lookback = lookback as usize;
        let first = offset + lookback;
        // Rows before `first` hold the no-result value. TA-Lib writes into the capacity
        // after them, at most `n` values (its contract: `endIdx - startIdx + 1`), and the
        // length is set once it has reported the range it produced.
        let mut outputs: Vec<Column> = self.outputs.iter().map(|o| Column::new(o.integer, first, first + n)).collect();
        for (i, out) in outputs.iter_mut().enumerate() {
            let code = match out {
                Column::Real(v) => unsafe {
                    TA_SetOutputParamRealPtr(holder.0, i as c_uint, v.spare_capacity_mut().as_mut_ptr().cast())
                },
                Column::Integer(v) => unsafe {
                    TA_SetOutputParamIntegerPtr(holder.0, i as c_uint, v.spare_capacity_mut().as_mut_ptr().cast())
                },
            };
            check(code, "TA_SetOutputParam")?;
        }
        let (mut beg, mut count) = (0, 0);
        let code = unsafe { TA_CallFunc(holder.0, 0, n_rows - 1, &mut beg, &mut count) };
        if code != TA_SUCCESS {
            check(code, &self.describe(values))?;
        }
        if i64::from(beg) != lookback as i64 || i64::from(count) != (n - lookback) as i64 {
            return Err(Error(format!(
                "{}: TA-Lib produced rows {beg}..{}, expected {lookback}..{n}",
                self.name,
                i64::from(beg) + i64::from(count)
            )));
        }
        for out in outputs.iter_mut() {
            // SAFETY: TA-Lib reported success and `count == n - lookback` values written
            // from the start of the spare capacity, which holds `n` rows; so the elements
            // up to `first + count == full` are initialized.
            match out {
                Column::Real(v) => unsafe { v.set_len(full) },
                Column::Integer(v) => unsafe { v.set_len(full) },
            }
        }
        if self.positional {
            for out in outputs.iter_mut() {
                if let Column::Integer(v) = out {
                    v[first..].iter_mut().for_each(|i| *i += skipped);
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
    fn new(handle: &TA_FuncHandle) -> Result<Holder, Error> {
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
