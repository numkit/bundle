//! Value conversion traits (`IntoValue` / `FromValue`) for ergonomic Rust calls.

use crate::{Error, Value};

pub trait IntoValue {
    fn into_numkit_value(self) -> Result<Value, Error>;
}

impl IntoValue for Value {
    fn into_numkit_value(self) -> Result<Value, Error> {
        Ok(self)
    }
}

impl IntoValue for &Value {
    fn into_numkit_value(self) -> Result<Value, Error> {
        Ok(self.clone())
    }
}

impl IntoValue for f64 {
    fn into_numkit_value(self) -> Result<Value, Error> {
        Value::scalar(self)
    }
}

impl IntoValue for i32 {
    fn into_numkit_value(self) -> Result<Value, Error> {
        Value::scalar(f64::from(self))
    }
}

impl IntoValue for usize {
    fn into_numkit_value(self) -> Result<Value, Error> {
        Value::scalar(self as f64)
    }
}

impl IntoValue for bool {
    fn into_numkit_value(self) -> Result<Value, Error> {
        Value::logical(self)
    }
}

impl IntoValue for &str {
    fn into_numkit_value(self) -> Result<Value, Error> {
        Value::from_char(self)
    }
}

impl IntoValue for String {
    fn into_numkit_value(self) -> Result<Value, Error> {
        Value::from_char(&self)
    }
}

impl IntoValue for &[f64] {
    fn into_numkit_value(self) -> Result<Value, Error> {
        Value::from_f64_slice(self, &[1, self.len()])
    }
}

impl IntoValue for Vec<f64> {
    fn into_numkit_value(self) -> Result<Value, Error> {
        Value::from_f64_slice(&self, &[1, self.len()])
    }
}

pub trait FromValue: Sized {
    fn from_numkit_value(v: Value) -> Result<Self, Error>;
}

impl FromValue for Value {
    fn from_numkit_value(v: Value) -> Result<Self, Error> {
        Ok(v)
    }
}

impl FromValue for f64 {
    fn from_numkit_value(v: Value) -> Result<Self, Error> {
        v.as_f64()
    }
}

impl FromValue for bool {
    fn from_numkit_value(v: Value) -> Result<Self, Error> {
        v.as_bool()
    }
}

impl FromValue for String {
    fn from_numkit_value(v: Value) -> Result<Self, Error> {
        Ok(v.to_string_lossy())
    }
}

impl FromValue for Vec<f64> {
    fn from_numkit_value(v: Value) -> Result<Self, Error> {
        Ok(v.as_f64_slice()?.to_vec())
    }
}
