//! Safe, ergonomic Rust bindings to the NumKit ecosystem (`bindings/c_api/include/numkit_c.h`).
//!
//! Features:
//! - **Lite mode (`Context::new_lite`)**: Engine-free `PluginContext` that loads toolbox shared
//!   libraries (`signal`, `stats`, `image`, `control`, `comm`, `wavelet`, `audio`, `cas`) directly
//!   without the `.m` interpreter.
//! - **Full mode (`Context::new_full`)**: Full `StandardEngine` runtime with `ctx.eval("...")`.
//! - **Lifetime-safe Zero-Copy Views (`ValueView<'a>`)**: Wraps a Rust slice `&'a [f64]` via
//!   `numkit_val_view` with zero heap copy; implements `Deref<Target = Value>` so it passes directly
//!   into any toolbox function while enforcing borrow-checker lifetime `'a`.
//! - **Two-tier API**: Strongly-typed functions generated from C++ headers (`tb::<toolbox>::*`)
//!   plus dynamic `ctx.call(ns, name, args, nargout)` for MATLAB vararg/Name-Value overloads.

pub mod convert;
pub mod tb;

pub use convert::{FromValue, IntoValue};
pub use numkit_sys::numkit_dtype as DType;
pub use tb::*;

use numkit_sys as ffi;
use std::ffi::{CStr, CString};
use std::fmt;
use std::marker::PhantomData;
use std::ops::Deref;
use std::os::raw::{c_char, c_int, c_void};
use std::ptr::{self, NonNull};
use std::slice;

/// Error returned by NumKit operations.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Error {
    pub code: i32,
    pub message: String,
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "NumKit error ({}): {}", self.code, self.message)
    }
}

impl std::error::Error for Error {}

fn check_ffi_err(err: &ffi::numkit_error) -> Result<(), Error> {
    if err.code == 0 {
        return Ok(());
    }
    let msg = unsafe { CStr::from_ptr(err.message.as_ptr()) }
        .to_string_lossy()
        .into_owned();
    Err(Error {
        code: err.code,
        message: msg,
    })
}

/// Owned handle to a `numkit::Value` (`numkit_val*`).
///
/// Cloning is $O(1)$ shallow Copy-on-Write for heap arrays.
pub struct Value {
    raw: NonNull<ffi::numkit_val>,
}

impl Drop for Value {
    fn drop(&mut self) {
        unsafe { ffi::numkit_val_release(self.raw.as_ptr()) };
    }
}

impl Clone for Value {
    fn clone(&self) -> Self {
        let cloned = unsafe { ffi::numkit_val_clone(self.raw.as_ptr()) };
        Self {
            raw: NonNull::new(cloned).expect("numkit_val_clone returned null"),
        }
    }
}

impl fmt::Debug for Value {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "Value(dtype={:?}, dims={:?}, text={:?})",
            self.dtype(),
            self.dims(),
            self.to_string_lossy()
        )
    }
}

impl Value {
    /// Wrap an owned raw `numkit_val*` pointer.
    ///
    /// # Safety
    /// `ptr` must be a valid owned handle returned by the C-ABI.
    pub unsafe fn from_raw(ptr: *mut ffi::numkit_val) -> Result<Self, Error> {
        NonNull::new(ptr).map(|raw| Self { raw }).ok_or_else(|| Error {
            code: 1,
            message: "Null numkit_val pointer".to_string(),
        })
    }

    pub fn as_raw(&self) -> *const ffi::numkit_val {
        self.raw.as_ptr()
    }

    pub fn empty() -> Result<Self, Error> {
        unsafe { Self::from_raw(ffi::numkit_val_empty()) }
    }

    pub fn scalar(v: f64) -> Result<Self, Error> {
        unsafe { Self::from_raw(ffi::numkit_val_scalar(v)) }
    }

    pub fn logical(b: bool) -> Result<Self, Error> {
        unsafe { Self::from_raw(ffi::numkit_val_logical(i32::from(b))) }
    }

    pub fn complex_scalar(re: f64, im: f64) -> Result<Self, Error> {
        unsafe { Self::from_raw(ffi::numkit_val_complex_scalar(re, im)) }
    }

    pub fn from_char(s: &str) -> Result<Self, Error> {
        let cs = CString::new(s).map_err(|_| Error {
            code: 1,
            message: "Interior NUL byte in char string".to_string(),
        })?;
        unsafe { Self::from_raw(ffi::numkit_val_char(cs.as_ptr())) }
    }

    pub fn from_string(s: &str) -> Result<Self, Error> {
        let cs = CString::new(s).map_err(|_| Error {
            code: 1,
            message: "Interior NUL byte in string".to_string(),
        })?;
        unsafe { Self::from_raw(ffi::numkit_val_string(cs.as_ptr())) }
    }

    pub fn from_f64_slice(data: &[f64], dims: &[usize]) -> Result<Self, Error> {
        let mut err = ffi::numkit_error::default();
        let ptr = unsafe {
            ffi::numkit_val_array_copy(
                data.as_ptr() as *const c_void,
                DType::NUMKIT_DTYPE_DOUBLE,
                dims.as_ptr(),
                dims.len() as c_int,
                &mut err,
            )
        };
        check_ffi_err(&err)?;
        unsafe { Self::from_raw(ptr) }
    }

    /// Create a zero-copy non-owning view over `data` tied to lifetime `'a`.
    pub fn view_f64<'a>(data: &'a [f64], dims: &[usize]) -> Result<ValueView<'a>, Error> {
        ValueView::new_f64(data, dims)
    }

    pub fn dtype(&self) -> DType {
        unsafe { ffi::numkit_val_type(self.raw.as_ptr()) }
    }

    pub fn numel(&self) -> usize {
        unsafe { ffi::numkit_val_numel(self.raw.as_ptr()) }
    }

    pub fn ndims(&self) -> usize {
        unsafe { ffi::numkit_val_ndims(self.raw.as_ptr()) }
    }

    pub fn dims(&self) -> Vec<usize> {
        let nd = self.ndims();
        let mut out = vec![0usize; nd];
        unsafe { ffi::numkit_val_dims(self.raw.as_ptr(), out.as_mut_ptr(), nd) };
        out
    }

    pub fn is_empty(&self) -> bool {
        unsafe { ffi::numkit_val_is_empty(self.raw.as_ptr()) != 0 }
    }

    pub fn is_scalar(&self) -> bool {
        unsafe { ffi::numkit_val_is_scalar(self.raw.as_ptr()) != 0 }
    }

    pub fn as_f64(&self) -> Result<f64, Error> {
        let mut err = ffi::numkit_error::default();
        let v = unsafe { ffi::numkit_val_as_double(self.raw.as_ptr(), &mut err) };
        check_ffi_err(&err)?;
        Ok(v)
    }

    pub fn as_bool(&self) -> Result<bool, Error> {
        let mut err = ffi::numkit_error::default();
        let v = unsafe { ffi::numkit_val_as_bool(self.raw.as_ptr(), &mut err) };
        check_ffi_err(&err)?;
        Ok(v != 0)
    }

    pub fn as_complex(&self) -> Result<(f64, f64), Error> {
        let mut err = ffi::numkit_error::default();
        let mut re = 0.0;
        let mut im = 0.0;
        unsafe { ffi::numkit_val_as_complex(self.raw.as_ptr(), &mut re, &mut im, &mut err) };
        check_ffi_err(&err)?;
        Ok((re, im))
    }

    /// Zero-copy slice borrow of the underlying column-major `f64` buffer.
    pub fn as_f64_slice(&self) -> Result<&[f64], Error> {
        if self.dtype() != DType::NUMKIT_DTYPE_DOUBLE {
            return Err(Error {
                code: 1,
                message: format!("Expected DOUBLE array, got {:?}", self.dtype()),
            });
        }
        let n = self.numel();
        if n == 0 {
            return Ok(&[]);
        }
        let ptr = unsafe { ffi::numkit_val_raw_data(self.raw.as_ptr()) as *const f64 };
        if ptr.is_null() {
            return Err(Error {
                code: 1,
                message: "Null raw data buffer".to_string(),
            });
        }
        Ok(unsafe { slice::from_raw_parts(ptr, n) })
    }

    pub fn to_string_lossy(&self) -> String {
        let n = unsafe { ffi::numkit_val_string_bytes(self.raw.as_ptr()) };
        let mut buf = vec![0u8; n + 1];
        unsafe {
            ffi::numkit_val_write_string(
                self.raw.as_ptr(),
                buf.as_mut_ptr() as *mut c_char,
                buf.len(),
            );
        }
        buf.truncate(n);
        String::from_utf8_lossy(&buf).into_owned()
    }
}

/// Lifetime-bound zero-copy view over a host slice `&'a [f64]`.
///
/// Derefs to [`Value`], so `&view` can be passed anywhere `&Value` is expected.
pub struct ValueView<'a> {
    inner: Value,
    _borrow: PhantomData<&'a [f64]>,
}

impl<'a> ValueView<'a> {
    pub fn new_f64(data: &'a [f64], dims: &[usize]) -> Result<Self, Error> {
        let expected: usize = dims.iter().copied().product();
        if expected != data.len() {
            return Err(Error {
                code: 1,
                message: format!(
                    "Slice length {} does not match dims product {}",
                    data.len(),
                    expected
                ),
            });
        }
        let mut err = ffi::numkit_error::default();
        let ptr = unsafe {
            ffi::numkit_val_view(
                data.as_ptr() as *const c_void,
                DType::NUMKIT_DTYPE_DOUBLE,
                dims.as_ptr(),
                dims.len() as c_int,
                &mut err,
            )
        };
        check_ffi_err(&err)?;
        let inner = unsafe { Value::from_raw(ptr)? };
        Ok(Self {
            inner,
            _borrow: PhantomData,
        })
    }
}

impl<'a> Deref for ValueView<'a> {
    type Target = Value;
    fn deref(&self) -> &Self::Target {
        &self.inner
    }
}

/// Execution context (Lite toolbox-only or Full Engine).
pub struct Context {
    raw: NonNull<ffi::numkit_ctx>,
}

impl Drop for Context {
    fn drop(&mut self) {
        unsafe { ffi::numkit_ctx_destroy(self.raw.as_ptr()) };
    }
}

impl Context {
    /// Create a lightweight engine-free context (for loading and invoking toolbox plugins).
    pub fn new_lite() -> Result<Self, Error> {
        let mut err = ffi::numkit_error::default();
        let ptr = unsafe { ffi::numkit_ctx_create_lite(&mut err) };
        check_ffi_err(&err)?;
        NonNull::new(ptr).map(|raw| Self { raw }).ok_or_else(|| Error {
            code: 1,
            message: "Failed to allocate Lite context".to_string(),
        })
    }

    /// Create a Full Engine context (supports `.m` evaluation via [`Context::eval`]).
    pub fn new_full() -> Result<Self, Error> {
        let mut err = ffi::numkit_error::default();
        let ptr = unsafe { ffi::numkit_ctx_create_full(&mut err) };
        check_ffi_err(&err)?;
        NonNull::new(ptr).map(|raw| Self { raw }).ok_or_else(|| Error {
            code: 1,
            message: "Failed to allocate Full context".to_string(),
        })
    }

    pub fn is_full(&self) -> bool {
        unsafe { ffi::numkit_ctx_is_full(self.raw.as_ptr()) != 0 }
    }

    pub fn load_plugin(&self, name_or_path: &str) -> Result<(), Error> {
        let cs = CString::new(name_or_path).map_err(|_| Error {
            code: 1,
            message: "Invalid plugin name".to_string(),
        })?;
        let mut err = ffi::numkit_error::default();
        unsafe { ffi::numkit_ctx_load_plugin(self.raw.as_ptr(), cs.as_ptr(), &mut err) };
        check_ffi_err(&err)
    }

    pub fn seed_rng(&self, seed: u64) {
        unsafe { ffi::numkit_ctx_seed_rng(self.raw.as_ptr(), seed) };
    }

    /// Invoke any function `name` (in optional toolbox namespace `ns`) with `args`,
    /// returning `nargout` owned [`Value`] handles.
    pub fn call(
        &self,
        ns: &str,
        name: &str,
        args: &[&Value],
        nargout: usize,
    ) -> Result<Vec<Value>, Error> {
        if !ns.is_empty() {
            let _ = self.load_plugin(ns);
        }
        let c_ns = CString::new(ns).map_err(|_| Error {
            code: 1,
            message: "Invalid namespace".to_string(),
        })?;
        let c_name = CString::new(name).map_err(|_| Error {
            code: 1,
            message: "Invalid function name".to_string(),
        })?;

        let raw_args: Vec<*const ffi::numkit_val> = args.iter().map(|v| v.as_raw()).collect();
        let actual_out = nargout.max(1);
        let mut raw_outs: Vec<*mut ffi::numkit_val> = vec![ptr::null_mut(); actual_out];
        let mut err = ffi::numkit_error::default();

        unsafe {
            ffi::numkit_call(
                self.raw.as_ptr(),
                if ns.is_empty() {
                    ptr::null()
                } else {
                    c_ns.as_ptr()
                },
                c_name.as_ptr(),
                if raw_args.is_empty() {
                    ptr::null()
                } else {
                    raw_args.as_ptr()
                },
                raw_args.len(),
                actual_out,
                raw_outs.as_mut_ptr(),
                &mut err,
            );
        }
        check_ffi_err(&err)?;

        let mut results = Vec::with_capacity(nargout);
        for (i, ptr) in raw_outs.into_iter().enumerate() {
            if i < nargout {
                results.push(unsafe { Value::from_raw(ptr)? });
            } else if !ptr.is_null() {
                unsafe { ffi::numkit_val_release(ptr) };
            }
        }
        Ok(results)
    }

    /// Evaluate MATLAB-compatible source `code` in Full Engine mode.
    pub fn eval(&self, code: &str) -> Result<Value, Error> {
        let c_code = CString::new(code).map_err(|_| Error {
            code: 1,
            message: "Interior NUL byte in code".to_string(),
        })?;
        let mut err = ffi::numkit_error::default();
        let ptr = unsafe { ffi::numkit_eval(self.raw.as_ptr(), c_code.as_ptr(), &mut err) };
        check_ffi_err(&err)?;
        unsafe { Value::from_raw(ptr) }
    }
}

/// Return the number of currently live `numkit_val*` handles (for leak assertions in tests).
pub fn live_values_count() -> i64 {
    unsafe { ffi::numkit_debug_live_values() }
}
