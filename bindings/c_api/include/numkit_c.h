/* bindings/c_api/include/numkit_c.h
 *
 * Canonical C-ABI for NumKit multi-language bindings (Python, Rust, Go, C#, JS/WASM).
 *
 * Supports two runtime modes behind a single ABI:
 *   1. Lite mode (`numkit_ctx_create_lite`):
 *      Engine-free `PluginContext` backed only by L0/L1 (`value`, `sys`, `ops`).
 *      Loads toolbox shared libraries (`signal`, `stats`, `image`, `control`,
 *      `comm`, `wavelet`, `audio`, `cas`) and invokes their functions directly
 *      with zero interpreter/parser/VM dependency.
 *   2. Full mode (`numkit_ctx_create_full`):
 *      Full `StandardEngine` runtime supporting all built-in functions, toolbox
 *      plugins, and `.m` script/expression evaluation via `numkit_eval`.
 *
 * Memory & Exception Safety:
 *   - No C++ types or headers leak through this file (pure C99/C11).
 *   - No C++ exception ever crosses the `extern "C"` boundary; all errors are
 *     caught and reported via `numkit_error`.
 *   - `numkit_val*` handles returned by creation functions or `numkit_call`/`numkit_eval`
 *     are OWNED by the caller and must be freed via `numkit_val_release`.
 *   - Zero-copy input arrays are supported via `numkit_val_view` (backed by
 *     `numkit::Value::view` with automatic Copy-on-Write on mutation), and
 *     zero-copy output reads via `numkit_val_raw_data`.
 */
#ifndef NUMKIT_C_H
#define NUMKIT_C_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#if defined(_WIN32) || defined(__CYGWIN__)
#  if defined(NUMKIT_C_BUILDING_DLL)
#    define NUMKIT_API __declspec(dllexport)
#  elif defined(NUMKIT_C_USE_DLL)
#    define NUMKIT_API __declspec(dllimport)
#  else
#    define NUMKIT_API
#  endif
#else
#  if defined(__GNUC__) && __GNUC__ >= 4
#    define NUMKIT_API __attribute__((visibility("default")))
#  else
#    define NUMKIT_API
#  endif
#endif

#define NUMKIT_C_ABI_VERSION 1

/* Opaque handles */
typedef struct numkit_ctx_s numkit_ctx;
typedef struct numkit_val_s numkit_val;

/* Element / value type tag (mirrors numkit::ValueType) */
typedef enum numkit_dtype {
    NUMKIT_DTYPE_DOUBLE      = 0,
    NUMKIT_DTYPE_SINGLE      = 1,
    NUMKIT_DTYPE_COMPLEX     = 2,  /* interleaved double (re, im) pairs */
    NUMKIT_DTYPE_LOGICAL     = 3,  /* uint8_t (0 or 1) */
    NUMKIT_DTYPE_CHAR        = 4,  /* char matrix */
    NUMKIT_DTYPE_STRING      = 5,  /* string array */
    NUMKIT_DTYPE_INT8        = 6,
    NUMKIT_DTYPE_INT16       = 7,
    NUMKIT_DTYPE_INT32       = 8,
    NUMKIT_DTYPE_INT64       = 9,
    NUMKIT_DTYPE_UINT8       = 10,
    NUMKIT_DTYPE_UINT16      = 11,
    NUMKIT_DTYPE_UINT32      = 12,
    NUMKIT_DTYPE_UINT64      = 13,
    NUMKIT_DTYPE_CELL        = 14,
    NUMKIT_DTYPE_STRUCT      = 15,
    NUMKIT_DTYPE_FUNC_HANDLE = 16,
    NUMKIT_DTYPE_OBJECT      = 17,
    NUMKIT_DTYPE_UNKNOWN     = 255
} numkit_dtype;

/* Error reporting structure. code == 0 indicates success. */
typedef struct numkit_error {
    int  code;
    char message[512];
} numkit_error;

/* Host-defined callback function signature for numkit_register_fn */
typedef int (*numkit_host_fn)(void *user_data,
                          const numkit_val *const *args,
                          size_t nargs,
                          size_t nargout,
                          numkit_val **outs,
                          numkit_error *err);

/* =========================================================================
 * 1. Context Lifecycle & Plugin Loading
 * ========================================================================= */

/* Return the C-ABI version number (NUMKIT_C_ABI_VERSION). */
NUMKIT_API uint32_t numkit_abi_version(void);

/* Create a lightweight toolbox-only context (no interpreter/parser/VM). */
NUMKIT_API numkit_ctx *numkit_ctx_create_lite(numkit_error *err);

/* Create a full engine context (with StandardEngine, builtins, and numkit_eval).
 * In `libnumkit_c_lite` builds, returns NULL and sets `err`. */
NUMKIT_API numkit_ctx *numkit_ctx_create_full(numkit_error *err);

/* Destroy a context and release its resources. */
NUMKIT_API void numkit_ctx_destroy(numkit_ctx *ctx);

/* Return 1 if `ctx` is a Full Engine context, 0 if Lite. */
NUMKIT_API int numkit_ctx_is_full(const numkit_ctx *ctx);

/* Load a toolbox plugin either by short name (e.g. "signal", "stats", "cas")
 * or by explicit filesystem path to the shared library (.so / .dll / .dylib).
 * Returns 0 on success, non-zero on error (filling `err`). Idempotent. */
NUMKIT_API int numkit_ctx_load_plugin(numkit_ctx *ctx, const char *name_or_path, numkit_error *err);

/* Add a directory to search when resolving toolbox names in numkit_ctx_load_plugin. */
NUMKIT_API void numkit_ctx_add_plugin_search_dir(numkit_ctx *ctx, const char *dir_path);

/* Check whether function `name` (optionally in namespace `ns`, or NULL/"" for any)
 * is registered in `ctx`. Returns 1 if found, 0 otherwise. */
NUMKIT_API int numkit_ctx_has_function(const numkit_ctx *ctx, const char *ns, const char *name);

/* Seed the context's random number generator (MATLAB `rng(seed)` semantics). */
NUMKIT_API void numkit_ctx_seed_rng(numkit_ctx *ctx, uint64_t seed);

/* Register a host callback (e.g. from Python or Rust) into `ctx`. */
NUMKIT_API int numkit_ctx_register_fn(numkit_ctx *ctx,
                              const char *ns,
                              const char *name,
                              numkit_host_fn fn,
                              void *user_data,
                              numkit_error *err);

/* =========================================================================
 * 2. Value Creation, Zero-Copy Views & Lifecycle
 * ========================================================================= */

/* Construct an empty 0x0 double matrix `[]`. */
NUMKIT_API numkit_val *numkit_val_empty(void);

/* Construct a 1x1 double scalar (inline representation, no heap allocation). */
NUMKIT_API numkit_val *numkit_val_scalar(double v);

/* Construct a 1x1 logical scalar (0 -> false, non-zero -> true). */
NUMKIT_API numkit_val *numkit_val_logical(int b);

/* Construct a 1x1 complex double scalar (re + i*im). */
NUMKIT_API numkit_val *numkit_val_complex_scalar(double re, double im);

/* Construct a 1x1 string scalar (MATLAB double-quoted "string"). */
NUMKIT_API numkit_val *numkit_val_string(const char *utf8);

/* Construct a 1xN char row vector (MATLAB single-quoted 'char'). */
NUMKIT_API numkit_val *numkit_val_char(const char *utf8);

/* Construct a function handle `@name`. */
NUMKIT_API numkit_val *numkit_val_func_handle(const char *name);

/* Construct an owning N-D array by copying `data` (column-major / Fortran order).
 * `dims` has length `ndims` (e.g. dims={rows, cols}, ndims=2).
 * Valid `dtype`: DOUBLE, SINGLE, COMPLEX, LOGICAL, CHAR, INT8..UINT64. */
NUMKIT_API numkit_val *numkit_val_array_copy(const void *data,
                                 numkit_dtype dtype,
                                 const size_t *dims,
                                 int ndims,
                                 numkit_error *err);

/* Construct a ZERO-COPY non-owning view over externally owned column-major memory.
 * Caller MUST keep `data` alive while this `numkit_val` is used. Any internal
 * mutation automatically detaches into a fresh owning buffer (Copy-on-Write). */
NUMKIT_API numkit_val *numkit_val_view(const void *data,
                           numkit_dtype dtype,
                           const size_t *dims,
                           int ndims,
                           numkit_error *err);

/* Allocate an owning N-D array and return its mutable data pointer in `*out_data_ptr`
 * so the host language can fill it directly without an intermediate copy. */
NUMKIT_API numkit_val *numkit_val_alloc_array(numkit_dtype dtype,
                                  const size_t *dims,
                                  int ndims,
                                  void **out_data_ptr,
                                  numkit_error *err);

/* Clone a value handle (O(1) shallow Copy-on-Write for heap arrays). */
NUMKIT_API numkit_val *numkit_val_clone(const numkit_val *v);

/* Release an owned value handle. Safe to call with NULL. */
NUMKIT_API void numkit_val_release(numkit_val *v);

/* Return the number of currently live `numkit_val*` handles (for leak tests). */
NUMKIT_API int64_t numkit_debug_live_values(void);

/* =========================================================================
 * 3. Value Introspection & Zero-Copy Data Access
 * ========================================================================= */

NUMKIT_API numkit_dtype numkit_val_type(const numkit_val *v);
NUMKIT_API size_t   numkit_val_numel(const numkit_val *v);
NUMKIT_API size_t   numkit_val_ndims(const numkit_val *v);

/* Copy up to `max_dims` dimension sizes into `out_dims`. Returns total rank. */
NUMKIT_API size_t   numkit_val_dims(const numkit_val *v, size_t *out_dims, size_t max_dims);

NUMKIT_API int      numkit_val_is_empty(const numkit_val *v);
NUMKIT_API int      numkit_val_is_scalar(const numkit_val *v);

/* Return a const pointer to the contiguous column-major buffer of `v`
 * (or NULL if `v` is an inline scalar, empty, cell, struct, string, or object).
 * Note: for a 1x1 inline double scalar, `numkit_val_as_double` or `numkit_val_copy_data`
 * works uniformly; `numkit_val_raw_data` also returns a valid pointer for inline
 * double scalars (pointing to the internal `scalar_` field). */
NUMKIT_API const void *numkit_val_raw_data(const numkit_val *v);
NUMKIT_API size_t      numkit_val_raw_bytes(const numkit_val *v);

/* Copy the flat byte representation of `v` into `dst` (up to `max_bytes`).
 * Works uniformly for both inline scalars and heap arrays. Returns bytes copied. */
NUMKIT_API size_t numkit_val_copy_bytes(const numkit_val *v, void *dst, size_t max_bytes);

/* Extract a scalar value as double / bool / complex. */
NUMKIT_API double numkit_val_as_double(const numkit_val *v, numkit_error *err);
NUMKIT_API int    numkit_val_as_bool(const numkit_val *v, numkit_error *err);
NUMKIT_API int    numkit_val_as_complex(const numkit_val *v, double *out_re, double *out_im, numkit_error *err);

/* String / Char / Object display extraction:
 * `numkit_val_string_bytes` returns the UTF-8 byte length (excluding NUL).
 * `numkit_val_write_string` writes UTF-8 + NUL into `buf` (up to `buf_cap`). */
NUMKIT_API size_t numkit_val_string_bytes(const numkit_val *v);
NUMKIT_API size_t numkit_val_write_string(const numkit_val *v, char *buf, size_t buf_cap);

/* Return the class name of an `NUMKIT_DTYPE_OBJECT` value (e.g. "sym", "tf"), or "". */
NUMKIT_API size_t numkit_val_object_class(const numkit_val *v, char *buf, size_t buf_cap);

/* =========================================================================
 * 4. Cell & Struct Containers
 * ========================================================================= */

NUMKIT_API numkit_val *numkit_cell_create(const size_t *dims, int ndims, numkit_error *err);
NUMKIT_API numkit_val *numkit_cell_get(const numkit_val *cell, size_t linear_idx, numkit_error *err);
NUMKIT_API int     numkit_cell_set(numkit_val *cell, size_t linear_idx, const numkit_val *elem, numkit_error *err);

NUMKIT_API numkit_val *numkit_struct_create(size_t rows, size_t cols, numkit_error *err);
NUMKIT_API size_t  numkit_struct_num_fields(const numkit_val *s);
NUMKIT_API size_t  numkit_struct_field_name(const numkit_val *s, size_t field_idx, char *buf, size_t buf_cap);
NUMKIT_API numkit_val *numkit_struct_get(const numkit_val *s, size_t linear_idx, const char *field, numkit_error *err);
NUMKIT_API int     numkit_struct_set(numkit_val *s, size_t linear_idx, const char *field, const numkit_val *val, numkit_error *err);

/* =========================================================================
 * 5. Function Dispatch & Evaluation
 * ========================================================================= */

/* Invoke function `name` (optionally scoped to toolbox namespace `ns`, e.g. "signal")
 * with `nargs` borrowed input handles `args[0..nargs)`.
 * Produces `nargout` owned output handles in `outs[0..nargout)` (when `nargout == 0`,
 * 1 slot may still be computed and discarded unless `outs` is non-null).
 * Returns 0 on success, non-zero on error (populating `err`). */
NUMKIT_API int numkit_call(numkit_ctx *ctx,
                   const char *ns,
                   const char *name,
                   const numkit_val *const *args,
                   size_t nargs,
                   size_t nargout,
                   numkit_val **outs,
                   numkit_error *err);

/* Evaluate MATLAB-compatible source `code` in Full Engine mode and return the
 * result of the last expression as an owned `numkit_val*` (or empty `numkit_val*` for
 * statements). Returns NULL on error and populates `err`. */
NUMKIT_API numkit_val *numkit_eval(numkit_ctx *ctx, const char *code, numkit_error *err);

/* Get or set a variable in the Full Engine workspace. */
NUMKIT_API numkit_val *numkit_workspace_get(numkit_ctx *ctx, const char *name, numkit_error *err);
NUMKIT_API int     numkit_workspace_set(numkit_ctx *ctx, const char *name, const numkit_val *val, numkit_error *err);

#ifdef __cplusplus
}
#endif

#endif /* NUMKIT_C_H */
