//! The slice of TA-Lib's C API this crate uses: the abstract interface (`ta_abstract.h`),
//! which describes and calls every TA function by name, plus initialisation and version
//! (`ta_common.h`). Declarations follow the headers of the pinned `ta-lib` submodule.

#![allow(non_camel_case_types, non_snake_case)]

use std::os::raw::{c_char, c_double, c_int, c_uint, c_void};

pub type TA_Real = c_double;
pub type TA_Integer = c_int;
pub type TA_RetCode = c_int;
pub type TA_FuncHandle = c_uint;

pub const TA_SUCCESS: TA_RetCode = 0;

/// `TA_InputParameterType`
pub const TA_INPUT_PRICE: c_int = 0;
pub const TA_INPUT_REAL: c_int = 1;
/// `TA_OptInputParameterType`: real range, real list, integer range, integer list.
pub const TA_OPTINPUT_INTEGER_RANGE: c_int = 2;
pub const TA_OPTINPUT_INTEGER_LIST: c_int = 3;
/// `TA_OutputParameterType`
pub const TA_OUTPUT_INTEGER: c_int = 1;
/// `TA_InputFlags` price components, in the order `TA_SetInputParamPricePtr` takes them.
pub const TA_IN_PRICE: [(c_int, &str); 6] = [
    (0x01, "open"),
    (0x02, "high"),
    (0x04, "low"),
    (0x08, "close"),
    (0x10, "volume"),
    (0x20, "openinterest"),
];

#[repr(C)]
pub struct TA_ParamHolder {
    _hidden_data: *mut c_void,
}

#[repr(C)]
pub struct TA_FuncInfo {
    pub name: *const c_char,
    pub group: *const c_char,
    pub hint: *const c_char,
    pub camel_case_name: *const c_char,
    pub flags: c_int,
    pub nb_input: c_uint,
    pub nb_opt_input: c_uint,
    pub nb_output: c_uint,
    pub handle: *const TA_FuncHandle,
}

#[repr(C)]
pub struct TA_InputParameterInfo {
    pub kind: c_int,
    pub param_name: *const c_char,
    pub flags: c_int,
}

#[repr(C)]
pub struct TA_OptInputParameterInfo {
    pub kind: c_int,
    pub param_name: *const c_char,
    pub flags: c_int,
    pub display_name: *const c_char,
    pub data_set: *const c_void,
    pub default_value: TA_Real,
    pub hint: *const c_char,
    pub help_file: *const c_char,
}

#[repr(C)]
pub struct TA_OutputParameterInfo {
    pub kind: c_int,
    pub param_name: *const c_char,
    pub flags: c_int,
}

#[repr(C)]
pub struct TA_RetCodeInfo {
    pub enum_str: *const c_char,
    pub info_str: *const c_char,
}

#[repr(C)]
pub struct TA_StringTable {
    pub size: c_uint,
    pub string: *const *const c_char,
    _hidden_data: *const c_void,
}

extern "C" {
    pub fn TA_Initialize() -> TA_RetCode;
    pub fn TA_GetVersionString() -> *const c_char;
    pub fn TA_SetRetCodeInfo(code: TA_RetCode, info: *mut TA_RetCodeInfo);

    pub fn TA_GroupTableAlloc(table: *mut *mut TA_StringTable) -> TA_RetCode;
    pub fn TA_GroupTableFree(table: *mut TA_StringTable) -> TA_RetCode;
    pub fn TA_FuncTableAlloc(group: *const c_char, table: *mut *mut TA_StringTable) -> TA_RetCode;
    pub fn TA_FuncTableFree(table: *mut TA_StringTable) -> TA_RetCode;
    pub fn TA_GetFuncHandle(name: *const c_char, handle: *mut *const TA_FuncHandle) -> TA_RetCode;
    pub fn TA_GetFuncInfo(handle: *const TA_FuncHandle, info: *mut *const TA_FuncInfo) -> TA_RetCode;
    pub fn TA_GetInputParameterInfo(
        handle: *const TA_FuncHandle,
        index: c_uint,
        info: *mut *const TA_InputParameterInfo,
    ) -> TA_RetCode;
    pub fn TA_GetOptInputParameterInfo(
        handle: *const TA_FuncHandle,
        index: c_uint,
        info: *mut *const TA_OptInputParameterInfo,
    ) -> TA_RetCode;
    pub fn TA_GetOutputParameterInfo(
        handle: *const TA_FuncHandle,
        index: c_uint,
        info: *mut *const TA_OutputParameterInfo,
    ) -> TA_RetCode;

    pub fn TA_ParamHolderAlloc(handle: *const TA_FuncHandle, params: *mut *mut TA_ParamHolder) -> TA_RetCode;
    pub fn TA_ParamHolderFree(params: *mut TA_ParamHolder) -> TA_RetCode;
    pub fn TA_SetInputParamRealPtr(params: *mut TA_ParamHolder, index: c_uint, value: *const TA_Real) -> TA_RetCode;
    pub fn TA_SetInputParamPricePtr(
        params: *mut TA_ParamHolder,
        index: c_uint,
        open: *const TA_Real,
        high: *const TA_Real,
        low: *const TA_Real,
        close: *const TA_Real,
        volume: *const TA_Real,
        open_interest: *const TA_Real,
    ) -> TA_RetCode;
    pub fn TA_SetOptInputParamInteger(params: *mut TA_ParamHolder, index: c_uint, value: TA_Integer) -> TA_RetCode;
    pub fn TA_SetOptInputParamReal(params: *mut TA_ParamHolder, index: c_uint, value: TA_Real) -> TA_RetCode;
    pub fn TA_SetOutputParamIntegerPtr(params: *mut TA_ParamHolder, index: c_uint, out: *mut TA_Integer) -> TA_RetCode;
    pub fn TA_SetOutputParamRealPtr(params: *mut TA_ParamHolder, index: c_uint, out: *mut TA_Real) -> TA_RetCode;
    pub fn TA_GetLookback(params: *const TA_ParamHolder, lookback: *mut TA_Integer) -> TA_RetCode;
    pub fn TA_CallFunc(
        params: *const TA_ParamHolder,
        start_idx: TA_Integer,
        end_idx: TA_Integer,
        out_beg_idx: *mut TA_Integer,
        out_nb_element: *mut TA_Integer,
    ) -> TA_RetCode;
}
