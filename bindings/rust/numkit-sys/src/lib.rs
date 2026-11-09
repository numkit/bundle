//! Raw FFI declarations for `bindings/c_api/include/numkit_c.h`.
#![allow(non_camel_case_types)]

use std::os::raw::{c_char, c_int, c_void};

pub const NUMKIT_C_ABI_VERSION: u32 = 1;

#[repr(C)]
pub struct numkit_ctx_s {
    _private: [u8; 0],
}
pub type numkit_ctx = numkit_ctx_s;

#[repr(C)]
pub struct numkit_val_s {
    _private: [u8; 0],
}
pub type numkit_val = numkit_val_s;

#[repr(C)]
#[derive(Debug, Copy, Clone, PartialEq, Eq)]
pub enum numkit_dtype {
    NUMKIT_DTYPE_DOUBLE = 0,
    NUMKIT_DTYPE_SINGLE = 1,
    NUMKIT_DTYPE_COMPLEX = 2,
    NUMKIT_DTYPE_LOGICAL = 3,
    NUMKIT_DTYPE_CHAR = 4,
    NUMKIT_DTYPE_STRING = 5,
    NUMKIT_DTYPE_INT8 = 6,
    NUMKIT_DTYPE_INT16 = 7,
    NUMKIT_DTYPE_INT32 = 8,
    NUMKIT_DTYPE_INT64 = 9,
    NUMKIT_DTYPE_UINT8 = 10,
    NUMKIT_DTYPE_UINT16 = 11,
    NUMKIT_DTYPE_UINT32 = 12,
    NUMKIT_DTYPE_UINT64 = 13,
    NUMKIT_DTYPE_CELL = 14,
    NUMKIT_DTYPE_STRUCT = 15,
    NUMKIT_DTYPE_FUNC_HANDLE = 16,
    NUMKIT_DTYPE_OBJECT = 17,
    NUMKIT_DTYPE_UNKNOWN = 255,
}

#[repr(C)]
#[derive(Copy, Clone)]
pub struct numkit_error {
    pub code: c_int,
    pub message: [c_char; 512],
}

impl Default for numkit_error {
    fn default() -> Self {
        Self {
            code: 0,
            message: [0; 512],
        }
    }
}

pub type numkit_host_fn = Option<
    unsafe extern "C" fn(
        user_data: *mut c_void,
        args: *const *const numkit_val,
        nargs: usize,
        nargout: usize,
        outs: *mut *mut numkit_val,
        err: *mut numkit_error,
    ) -> c_int,
>;

extern "C" {
    pub fn numkit_abi_version() -> u32;
    pub fn numkit_ctx_create_lite(err: *mut numkit_error) -> *mut numkit_ctx;
    pub fn numkit_ctx_create_full(err: *mut numkit_error) -> *mut numkit_ctx;
    pub fn numkit_ctx_destroy(ctx: *mut numkit_ctx);
    pub fn numkit_ctx_is_full(ctx: *const numkit_ctx) -> c_int;
    pub fn numkit_ctx_load_plugin(
        ctx: *mut numkit_ctx,
        name_or_path: *const c_char,
        err: *mut numkit_error,
    ) -> c_int;
    pub fn numkit_ctx_add_plugin_search_dir(ctx: *mut numkit_ctx, dir_path: *const c_char);
    pub fn numkit_ctx_has_function(
        ctx: *const numkit_ctx,
        ns: *const c_char,
        name: *const c_char,
    ) -> c_int;
    pub fn numkit_ctx_seed_rng(ctx: *mut numkit_ctx, seed: u64);
    pub fn numkit_ctx_register_fn(
        ctx: *mut numkit_ctx,
        ns: *const c_char,
        name: *const c_char,
        func: numkit_host_fn,
        user_data: *mut c_void,
        err: *mut numkit_error,
    ) -> c_int;

    pub fn numkit_val_empty() -> *mut numkit_val;
    pub fn numkit_val_scalar(v: f64) -> *mut numkit_val;
    pub fn numkit_val_logical(b: c_int) -> *mut numkit_val;
    pub fn numkit_val_complex_scalar(re: f64, im: f64) -> *mut numkit_val;
    pub fn numkit_val_string(utf8: *const c_char) -> *mut numkit_val;
    pub fn numkit_val_char(utf8: *const c_char) -> *mut numkit_val;
    pub fn numkit_val_func_handle(name: *const c_char) -> *mut numkit_val;
    pub fn numkit_val_array_copy(
        data: *const c_void,
        dtype: numkit_dtype,
        dims: *const usize,
        ndims: c_int,
        err: *mut numkit_error,
    ) -> *mut numkit_val;
    pub fn numkit_val_view(
        data: *const c_void,
        dtype: numkit_dtype,
        dims: *const usize,
        ndims: c_int,
        err: *mut numkit_error,
    ) -> *mut numkit_val;
    pub fn numkit_val_alloc_array(
        dtype: numkit_dtype,
        dims: *const usize,
        ndims: c_int,
        out_data_ptr: *mut *mut c_void,
        err: *mut numkit_error,
    ) -> *mut numkit_val;
    pub fn numkit_val_clone(v: *const numkit_val) -> *mut numkit_val;
    pub fn numkit_val_release(v: *mut numkit_val);
    pub fn numkit_debug_live_values() -> i64;

    pub fn numkit_val_type(v: *const numkit_val) -> numkit_dtype;
    pub fn numkit_val_numel(v: *const numkit_val) -> usize;
    pub fn numkit_val_ndims(v: *const numkit_val) -> usize;
    pub fn numkit_val_dims(v: *const numkit_val, out_dims: *mut usize, max_dims: usize) -> usize;
    pub fn numkit_val_is_empty(v: *const numkit_val) -> c_int;
    pub fn numkit_val_is_scalar(v: *const numkit_val) -> c_int;
    pub fn numkit_val_raw_data(v: *const numkit_val) -> *const c_void;
    pub fn numkit_val_raw_bytes(v: *const numkit_val) -> usize;
    pub fn numkit_val_copy_bytes(v: *const numkit_val, dst: *mut c_void, max_bytes: usize) -> usize;
    pub fn numkit_val_as_double(v: *const numkit_val, err: *mut numkit_error) -> f64;
    pub fn numkit_val_as_bool(v: *const numkit_val, err: *mut numkit_error) -> c_int;
    pub fn numkit_val_as_complex(
        v: *const numkit_val,
        out_re: *mut f64,
        out_im: *mut f64,
        err: *mut numkit_error,
    ) -> c_int;
    pub fn numkit_val_string_bytes(v: *const numkit_val) -> usize;
    pub fn numkit_val_write_string(v: *const numkit_val, buf: *mut c_char, buf_cap: usize) -> usize;
    pub fn numkit_val_object_class(v: *const numkit_val, buf: *mut c_char, buf_cap: usize) -> usize;

    pub fn numkit_cell_create(
        dims: *const usize,
        ndims: c_int,
        err: *mut numkit_error,
    ) -> *mut numkit_val;
    pub fn numkit_cell_get(
        cell: *const numkit_val,
        linear_idx: usize,
        err: *mut numkit_error,
    ) -> *mut numkit_val;
    pub fn numkit_cell_set(
        cell: *mut numkit_val,
        linear_idx: usize,
        elem: *const numkit_val,
        err: *mut numkit_error,
    ) -> c_int;

    pub fn numkit_struct_create(rows: usize, cols: usize, err: *mut numkit_error) -> *mut numkit_val;
    pub fn numkit_struct_num_fields(s: *const numkit_val) -> usize;
    pub fn numkit_struct_field_name(
        s: *const numkit_val,
        field_idx: usize,
        buf: *mut c_char,
        buf_cap: usize,
    ) -> usize;
    pub fn numkit_struct_get(
        s: *const numkit_val,
        linear_idx: usize,
        field: *const c_char,
        err: *mut numkit_error,
    ) -> *mut numkit_val;
    pub fn numkit_struct_set(
        s: *mut numkit_val,
        linear_idx: usize,
        field: *const c_char,
        val: *const numkit_val,
        err: *mut numkit_error,
    ) -> c_int;

    pub fn numkit_call(
        ctx: *mut numkit_ctx,
        ns: *const c_char,
        name: *const c_char,
        args: *const *const numkit_val,
        nargs: usize,
        nargout: usize,
        outs: *mut *mut numkit_val,
        err: *mut numkit_error,
    ) -> c_int;
    pub fn numkit_eval(ctx: *mut numkit_ctx, code: *const c_char, err: *mut numkit_error) -> *mut numkit_val;
    pub fn numkit_workspace_get(
        ctx: *mut numkit_ctx,
        name: *const c_char,
        err: *mut numkit_error,
    ) -> *mut numkit_val;
    pub fn numkit_workspace_set(
        ctx: *mut numkit_ctx,
        name: *const c_char,
        val: *const numkit_val,
        err: *mut numkit_error,
    ) -> c_int;
}
