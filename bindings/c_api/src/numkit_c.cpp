// bindings/c_api/src/numkit_c.cpp
//
// Implementation of the canonical NumKit C-ABI (`numkit_c.h`).
// Supports both Lite (engine-free toolbox-only) and Full (StandardEngine) modes.

#include "numkit_c.h"

#include "lite_context.hpp"
#include "full_context.hpp"

#include <numkit/value/dims.hpp>
#include <numkit/value/error.hpp>
#include <numkit/value/object.hpp>
#include <numkit/value/span.hpp>
#include <numkit/value/value.hpp>
#include <numkit/value/value_type.hpp>

#include <algorithm>
#include <atomic>
#include <cstdio>
#include <cstring>
#include <exception>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

struct numkit_val_s {
    numkit::Value val;
    explicit numkit_val_s(numkit::Value v) : val(std::move(v)) {}
};

struct numkit_ctx_s {
    bool is_full{false};
    std::unique_ptr<numkit::c_api::LitePluginContext> lite;
#if defined(NUMKIT_C_ENABLE_FULL_ENGINE) && NUMKIT_C_ENABLE_FULL_ENGINE
    std::unique_ptr<numkit::c_api::FullEngineContext> full;
#endif
};

namespace {

using numkit::Dims;
using numkit::Span;
using numkit::Value;
using numkit::ValueType;

std::atomic<int64_t> &liveValuesCounter() noexcept
{
    static std::atomic<int64_t> count{0};
    return count;
}

numkit_val *makeHandle(Value v)
{
    auto *h = new numkit_val_s(std::move(v));
    liveValuesCounter().fetch_add(1, std::memory_order_relaxed);
    return h;
}

void destroyHandle(numkit_val *h) noexcept
{
    if (!h) return;
    liveValuesCounter().fetch_sub(1, std::memory_order_relaxed);
    delete h;
}

void clearErr(numkit_error *err) noexcept
{
    if (!err) return;
    err->code = 0;
    err->message[0] = '\0';
}

void setErr(numkit_error *err, int code, const char *msg) noexcept
{
    if (!err) return;
    err->code = code ? code : 1;
    std::snprintf(err->message, sizeof(err->message), "%s", msg ? msg : "unknown error");
}

bool toCppValueType(numkit_dtype dt, ValueType &out) noexcept
{
    switch (dt) {
    case NUMKIT_DTYPE_DOUBLE:      out = ValueType::DOUBLE; return true;
    case NUMKIT_DTYPE_SINGLE:      out = ValueType::SINGLE; return true;
    case NUMKIT_DTYPE_COMPLEX:     out = ValueType::COMPLEX; return true;
    case NUMKIT_DTYPE_LOGICAL:     out = ValueType::LOGICAL; return true;
    case NUMKIT_DTYPE_CHAR:        out = ValueType::CHAR; return true;
    case NUMKIT_DTYPE_STRING:      out = ValueType::STRING; return true;
    case NUMKIT_DTYPE_INT8:        out = ValueType::INT8; return true;
    case NUMKIT_DTYPE_INT16:       out = ValueType::INT16; return true;
    case NUMKIT_DTYPE_INT32:       out = ValueType::INT32; return true;
    case NUMKIT_DTYPE_INT64:       out = ValueType::INT64; return true;
    case NUMKIT_DTYPE_UINT8:       out = ValueType::UINT8; return true;
    case NUMKIT_DTYPE_UINT16:      out = ValueType::UINT16; return true;
    case NUMKIT_DTYPE_UINT32:      out = ValueType::UINT32; return true;
    case NUMKIT_DTYPE_UINT64:      out = ValueType::UINT64; return true;
    case NUMKIT_DTYPE_CELL:        out = ValueType::CELL; return true;
    case NUMKIT_DTYPE_STRUCT:      out = ValueType::STRUCT; return true;
    case NUMKIT_DTYPE_FUNC_HANDLE: out = ValueType::FUNC_HANDLE; return true;
    case NUMKIT_DTYPE_OBJECT:      out = ValueType::OBJECT; return true;
    default:                   return false;
    }
}

numkit_dtype fromCppValueType(ValueType vt) noexcept
{
    switch (vt) {
    case ValueType::DOUBLE:      return NUMKIT_DTYPE_DOUBLE;
    case ValueType::SINGLE:      return NUMKIT_DTYPE_SINGLE;
    case ValueType::COMPLEX:     return NUMKIT_DTYPE_COMPLEX;
    case ValueType::LOGICAL:     return NUMKIT_DTYPE_LOGICAL;
    case ValueType::CHAR:        return NUMKIT_DTYPE_CHAR;
    case ValueType::STRING:      return NUMKIT_DTYPE_STRING;
    case ValueType::INT8:        return NUMKIT_DTYPE_INT8;
    case ValueType::INT16:       return NUMKIT_DTYPE_INT16;
    case ValueType::INT32:       return NUMKIT_DTYPE_INT32;
    case ValueType::INT64:       return NUMKIT_DTYPE_INT64;
    case ValueType::UINT8:       return NUMKIT_DTYPE_UINT8;
    case ValueType::UINT16:      return NUMKIT_DTYPE_UINT16;
    case ValueType::UINT32:      return NUMKIT_DTYPE_UINT32;
    case ValueType::UINT64:      return NUMKIT_DTYPE_UINT64;
    case ValueType::CELL:        return NUMKIT_DTYPE_CELL;
    case ValueType::STRUCT:      return NUMKIT_DTYPE_STRUCT;
    case ValueType::FUNC_HANDLE: return NUMKIT_DTYPE_FUNC_HANDLE;
    case ValueType::OBJECT:      return NUMKIT_DTYPE_OBJECT;
    default:                     return NUMKIT_DTYPE_UNKNOWN;
    }
}

std::string valueToStringRep(const Value &v)
{
    if (v.isString()) {
        if (v.numel() == 0) return "";
        return v.stringElem(0);
    }
    if (v.isChar()) {
        return v.toString();
    }
    if (v.isObject()) {
        // Check if object has a readable char/display representation via debugString or formatDisplay
        std::string disp = v.formatDisplay("");
        // Strip leading/trailing whitespace and newlines
        size_t a = 0, b = disp.size();
        while (a < b && (disp[a] == ' ' || disp[a] == '\n' || disp[a] == '\r')) ++a;
        while (b > a && (disp[b - 1] == ' ' || disp[b - 1] == '\n' || disp[b - 1] == '\r')) --b;
        if (b > a) return disp.substr(a, b - a);
        return "<" + v.objectClassName() + " object>";
    }
    return v.debugString();
}

} // namespace

extern "C" {

uint32_t numkit_abi_version(void)
{
    return NUMKIT_C_ABI_VERSION;
}

numkit_ctx *numkit_ctx_create_lite(numkit_error *err)
{
    clearErr(err);
    try {
        auto *ctx = new numkit_ctx_s();
        ctx->is_full = false;
        ctx->lite = std::make_unique<numkit::c_api::LitePluginContext>();
        return ctx;
    } catch (const std::exception &e) {
        setErr(err, 1, e.what());
        return nullptr;
    } catch (...) {
        setErr(err, 1, "Failed to create Lite context");
        return nullptr;
    }
}

numkit_ctx *numkit_ctx_create_full(numkit_error *err)
{
    clearErr(err);
#if defined(NUMKIT_C_ENABLE_FULL_ENGINE) && NUMKIT_C_ENABLE_FULL_ENGINE
    try {
        auto *ctx = new numkit_ctx_s();
        ctx->is_full = true;
        ctx->full = std::make_unique<numkit::c_api::FullEngineContext>();
        return ctx;
    } catch (const std::exception &e) {
        setErr(err, 1, e.what());
        return nullptr;
    } catch (...) {
        setErr(err, 1, "Failed to create Full Engine context");
        return nullptr;
    }
#else
    setErr(err, 2, "Full Engine mode is not linked in libnumkit_c_lite; link libnumkit_c_full instead");
    return nullptr;
#endif
}

void numkit_ctx_destroy(numkit_ctx *ctx)
{
    delete ctx;
}

int numkit_ctx_is_full(const numkit_ctx *ctx)
{
    return (ctx && ctx->is_full) ? 1 : 0;
}

int numkit_ctx_load_plugin(numkit_ctx *ctx, const char *name_or_path, numkit_error *err)
{
    clearErr(err);
    if (!ctx || !name_or_path) {
        setErr(err, 1, "numkit_ctx_load_plugin: null context or plugin name");
        return 1;
    }
    try {
        if (!ctx->is_full && ctx->lite) {
            ctx->lite->loadPlugin(name_or_path);
            return 0;
        }
#if defined(NUMKIT_C_ENABLE_FULL_ENGINE) && NUMKIT_C_ENABLE_FULL_ENGINE
        if (ctx->is_full && ctx->full) {
            ctx->full->loadPlugin(name_or_path);
            return 0;
        }
#endif
        setErr(err, 1, "Invalid context state");
        return 1;
    } catch (const std::exception &e) {
        setErr(err, 1, e.what());
        return 1;
    } catch (...) {
        setErr(err, 1, "Unknown error loading plugin");
        return 1;
    }
}

void numkit_ctx_add_plugin_search_dir(numkit_ctx *ctx, const char *dir_path)
{
    if (!ctx || !dir_path) return;
    try {
        if (!ctx->is_full && ctx->lite) {
            ctx->lite->addSearchDir(dir_path);
        }
#if defined(NUMKIT_C_ENABLE_FULL_ENGINE) && NUMKIT_C_ENABLE_FULL_ENGINE
        if (ctx->is_full && ctx->full) {
            ctx->full->addSearchDir(dir_path);
        }
#endif
    } catch (...) {}
}

int numkit_ctx_has_function(const numkit_ctx *ctx, const char *ns, const char *name)
{
    if (!ctx || !name) return 0;
    try {
        std::string nsStr = ns ? ns : "";
        if (!ctx->is_full && ctx->lite) {
            return ctx->lite->hasFunction(nsStr, name) ? 1 : 0;
        }
#if defined(NUMKIT_C_ENABLE_FULL_ENGINE) && NUMKIT_C_ENABLE_FULL_ENGINE
        if (ctx->is_full && ctx->full) {
            return ctx->full->hasFunction(nsStr, name) ? 1 : 0;
        }
#endif
    } catch (...) {}
    return 0;
}

void numkit_ctx_seed_rng(numkit_ctx *ctx, uint64_t seed)
{
    if (!ctx) return;
    try {
        if (!ctx->is_full && ctx->lite) {
            ctx->lite->rng().seed(seed);
        }
#if defined(NUMKIT_C_ENABLE_FULL_ENGINE) && NUMKIT_C_ENABLE_FULL_ENGINE
        if (ctx->is_full && ctx->full) {
            ctx->full->engine().rng().seed(seed);
        }
#endif
    } catch (...) {}
}

int numkit_ctx_register_fn(numkit_ctx *ctx,
                       const char *ns,
                       const char *name,
                       numkit_host_fn fn,
                       void *user_data,
                       numkit_error *err)
{
    clearErr(err);
    if (!ctx || !name || !fn) {
        setErr(err, 1, "numkit_ctx_register_fn: null argument");
        return 1;
    }
    try {
        auto wrapper = [fn, user_data](Span<const Value> args,
                                       size_t nargout,
                                       Span<Value> outs,
                                       numkit::CallContext & /*cctx*/) {
            std::vector<numkit_val_s> argWrappers;
            argWrappers.reserve(args.size());
            std::vector<const numkit_val *> argPtrs(args.size());
            for (size_t i = 0; i < args.size(); ++i) {
                argWrappers.emplace_back(args[i]);
                argPtrs[i] = &argWrappers[i];
            }
            size_t actualOut = outs.size();
            std::vector<numkit_val *> outHandles(actualOut, nullptr);
            numkit_error hostErr{};
            int rc = fn(user_data,
                        argPtrs.empty() ? nullptr : argPtrs.data(),
                        argPtrs.size(),
                        nargout,
                        outHandles.empty() ? nullptr : outHandles.data(),
                        &hostErr);
            if (rc != 0 || hostErr.code != 0) {
                for (numkit_val *h : outHandles) destroyHandle(h);
                throw std::runtime_error(hostErr.message[0] ? hostErr.message : "Host callback failed");
            }
            for (size_t i = 0; i < actualOut; ++i) {
                if (outHandles[i]) {
                    outs[i] = std::move(outHandles[i]->val);
                    destroyHandle(outHandles[i]);
                }
            }
        };

        std::string nsStr = ns ? ns : "";
        if (!ctx->is_full && ctx->lite) {
            if (nsStr.empty()) {
                ctx->lite->registerFunction(name, std::move(wrapper));
            } else {
                ctx->lite->registerFunction(nsStr, name, std::move(wrapper));
            }
            return 0;
        }
#if defined(NUMKIT_C_ENABLE_FULL_ENGINE) && NUMKIT_C_ENABLE_FULL_ENGINE
        if (ctx->is_full && ctx->full) {
            if (nsStr.empty()) {
                ctx->full->engine().registerFunction(name, std::move(wrapper));
            } else {
                ctx->full->engine().registerFunction(nsStr, name, std::move(wrapper));
            }
            return 0;
        }
#endif
        setErr(err, 1, "Invalid context");
        return 1;
    } catch (const std::exception &e) {
        setErr(err, 1, e.what());
        return 1;
    } catch (...) {
        setErr(err, 1, "Failed to register host function");
        return 1;
    }
}

/* =========================================================================
 * 2. Value Creation, Zero-Copy Views & Lifecycle
 * ========================================================================= */

numkit_val *numkit_val_empty(void)
{
    try {
        return makeHandle(Value::Empty);
    } catch (...) {
        return nullptr;
    }
}

numkit_val *numkit_val_scalar(double v)
{
    try {
        return makeHandle(Value::scalar(v));
    } catch (...) {
        return nullptr;
    }
}

numkit_val *numkit_val_logical(int b)
{
    try {
        return makeHandle(Value::logicalScalar(b != 0));
    } catch (...) {
        return nullptr;
    }
}

numkit_val *numkit_val_complex_scalar(double re, double im)
{
    try {
        return makeHandle(Value::complexScalar(re, im));
    } catch (...) {
        return nullptr;
    }
}

numkit_val *numkit_val_string(const char *utf8)
{
    try {
        return makeHandle(Value::stringScalar(utf8 ? utf8 : ""));
    } catch (...) {
        return nullptr;
    }
}

numkit_val *numkit_val_char(const char *utf8)
{
    try {
        return makeHandle(Value::fromString(utf8 ? utf8 : ""));
    } catch (...) {
        return nullptr;
    }
}

numkit_val *numkit_val_func_handle(const char *name)
{
    try {
        return makeHandle(Value::funcHandle(name ? name : ""));
    } catch (...) {
        return nullptr;
    }
}

numkit_val *numkit_val_array_copy(const void *data,
                          numkit_dtype dtype,
                          const size_t *dims,
                          int ndims,
                          numkit_error *err)
{
    clearErr(err);
    if (!dims || ndims <= 0) {
        setErr(err, 1, "numkit_val_array_copy: invalid dimensions");
        return nullptr;
    }
    ValueType vt;
    if (!toCppValueType(dtype, vt)) {
        setErr(err, 1, "numkit_val_array_copy: unsupported dtype");
        return nullptr;
    }
    try {
        size_t normDims[2] = {1, 1};
        const size_t *dPtr = dims;
        int actualNd = ndims;
        if (ndims == 1) {
            normDims[0] = 1;
            normDims[1] = dims[0];
            dPtr = normDims;
            actualNd = 2;
        }
        Value arr = Value::matrixND(dPtr, actualNd, vt, nullptr);
        size_t bytes = arr.rawBytes();
        if (bytes > 0) {
            if (!data) {
                setErr(err, 1, "numkit_val_array_copy: null data pointer for non-empty array");
                return nullptr;
            }
            std::memcpy(arr.rawDataMut(), data, bytes);
        }
        return makeHandle(std::move(arr));
    } catch (const std::exception &e) {
        setErr(err, 1, e.what());
        return nullptr;
    }
}

numkit_val *numkit_val_view(const void *data,
                    numkit_dtype dtype,
                    const size_t *dims,
                    int ndims,
                    numkit_error *err)
{
    clearErr(err);
    if (!dims || ndims <= 0) {
        setErr(err, 1, "numkit_val_view: invalid dimensions");
        return nullptr;
    }
    ValueType vt;
    if (!toCppValueType(dtype, vt)) {
        setErr(err, 1, "numkit_val_view: unsupported dtype");
        return nullptr;
    }
    try {
        size_t normDims[2] = {1, 1};
        const size_t *dPtr = dims;
        int actualNd = ndims;
        if (ndims == 1) {
            normDims[0] = 1;
            normDims[1] = dims[0];
            dPtr = normDims;
            actualNd = 2;
        }
        Dims d(dPtr, actualNd);
        if (d.numel() > 0 && !data) {
            setErr(err, 1, "numkit_val_view: null data pointer for non-empty view");
            return nullptr;
        }
        return makeHandle(Value::view(data, vt, d));
    } catch (const std::exception &e) {
        setErr(err, 1, e.what());
        return nullptr;
    }
}

numkit_val *numkit_val_alloc_array(numkit_dtype dtype,
                           const size_t *dims,
                           int ndims,
                           void **out_data_ptr,
                           numkit_error *err)
{
    clearErr(err);
    if (out_data_ptr) *out_data_ptr = nullptr;
    if (!dims || ndims <= 0) {
        setErr(err, 1, "numkit_val_alloc_array: invalid dimensions");
        return nullptr;
    }
    ValueType vt;
    if (!toCppValueType(dtype, vt)) {
        setErr(err, 1, "numkit_val_alloc_array: unsupported dtype");
        return nullptr;
    }
    try {
        size_t normDims[2] = {1, 1};
        const size_t *dPtr = dims;
        int actualNd = ndims;
        if (ndims == 1) {
            normDims[0] = 1;
            normDims[1] = dims[0];
            dPtr = normDims;
            actualNd = 2;
        }
        Value arr = Value::matrixND(dPtr, actualNd, vt, nullptr);
        numkit_val *h = makeHandle(std::move(arr));
        if (out_data_ptr) {
            *out_data_ptr = h->val.rawDataMut();
        }
        return h;
    } catch (const std::exception &e) {
        setErr(err, 1, e.what());
        return nullptr;
    }
}

numkit_val *numkit_val_clone(const numkit_val *v)
{
    if (!v) return nullptr;
    try {
        return makeHandle(v->val);
    } catch (...) {
        return nullptr;
    }
}

void numkit_val_release(numkit_val *v)
{
    destroyHandle(v);
}

int64_t numkit_debug_live_values(void)
{
    return liveValuesCounter().load(std::memory_order_relaxed);
}

/* =========================================================================
 * 3. Value Introspection & Zero-Copy Data Access
 * ========================================================================= */

numkit_dtype numkit_val_type(const numkit_val *v)
{
    if (!v) return NUMKIT_DTYPE_UNKNOWN;
    return fromCppValueType(v->val.type());
}

size_t numkit_val_numel(const numkit_val *v)
{
    if (!v) return 0;
    return v->val.numel();
}

size_t numkit_val_ndims(const numkit_val *v)
{
    if (!v) return 0;
    return static_cast<size_t>(v->val.dims().ndim());
}

size_t numkit_val_dims(const numkit_val *v, size_t *out_dims, size_t max_dims)
{
    if (!v) return 0;
    const Dims &d = v->val.dims();
    size_t nd = static_cast<size_t>(d.ndim());
    if (out_dims && max_dims > 0) {
        size_t n = std::min(nd, max_dims);
        for (size_t i = 0; i < n; ++i) {
            out_dims[i] = d.dim(static_cast<int>(i));
        }
    }
    return nd;
}

int numkit_val_is_empty(const numkit_val *v)
{
    if (!v) return 1;
    return v->val.isEmpty() ? 1 : 0;
}

int numkit_val_is_scalar(const numkit_val *v)
{
    if (!v) return 0;
    return v->val.isScalar() ? 1 : 0;
}

const void *numkit_val_raw_data(const numkit_val *v)
{
    if (!v) return nullptr;
    try {
        return v->val.rawData();
    } catch (...) {
        return nullptr;
    }
}

size_t numkit_val_raw_bytes(const numkit_val *v)
{
    if (!v) return 0;
    try {
        return v->val.rawBytes();
    } catch (...) {
        return 0;
    }
}

size_t numkit_val_copy_bytes(const numkit_val *v, void *dst, size_t max_bytes)
{
    if (!v || !dst || max_bytes == 0) return 0;
    try {
        const void *src = v->val.rawData();
        size_t avail = v->val.rawBytes();
        if (!src || avail == 0) return 0;
        size_t n = std::min(avail, max_bytes);
        std::memcpy(dst, src, n);
        return n;
    } catch (...) {
        return 0;
    }
}

double numkit_val_as_double(const numkit_val *v, numkit_error *err)
{
    clearErr(err);
    if (!v) {
        setErr(err, 1, "numkit_val_as_double: null handle");
        return 0.0;
    }
    try {
        return v->val.toScalar();
    } catch (const std::exception &e) {
        setErr(err, 1, e.what());
        return 0.0;
    }
}

int numkit_val_as_bool(const numkit_val *v, numkit_error *err)
{
    clearErr(err);
    if (!v) {
        setErr(err, 1, "numkit_val_as_bool: null handle");
        return 0;
    }
    try {
        return v->val.toBool() ? 1 : 0;
    } catch (const std::exception &e) {
        setErr(err, 1, e.what());
        return 0;
    }
}

int numkit_val_as_complex(const numkit_val *v, double *out_re, double *out_im, numkit_error *err)
{
    clearErr(err);
    if (!v) {
        setErr(err, 1, "numkit_val_as_complex: null handle");
        return 1;
    }
    try {
        numkit::Complex c = v->val.toComplex();
        if (out_re) *out_re = c.real();
        if (out_im) *out_im = c.imag();
        return 0;
    } catch (const std::exception &e) {
        setErr(err, 1, e.what());
        return 1;
    }
}

size_t numkit_val_string_bytes(const numkit_val *v)
{
    if (!v) return 0;
    try {
        return valueToStringRep(v->val).size();
    } catch (...) {
        return 0;
    }
}

size_t numkit_val_write_string(const numkit_val *v, char *buf, size_t buf_cap)
{
    if (!v) return 0;
    try {
        std::string s = valueToStringRep(v->val);
        if (buf && buf_cap > 0) {
            size_t n = std::min(s.size(), buf_cap - 1);
            std::memcpy(buf, s.data(), n);
            buf[n] = '\0';
        }
        return s.size();
    } catch (...) {
        if (buf && buf_cap > 0) buf[0] = '\0';
        return 0;
    }
}

size_t numkit_val_object_class(const numkit_val *v, char *buf, size_t buf_cap)
{
    if (!v || !v->val.isObject()) {
        if (buf && buf_cap > 0) buf[0] = '\0';
        return 0;
    }
    try {
        std::string cls = v->val.objectClassName();
        if (buf && buf_cap > 0) {
            size_t n = std::min(cls.size(), buf_cap - 1);
            std::memcpy(buf, cls.data(), n);
            buf[n] = '\0';
        }
        return cls.size();
    } catch (...) {
        if (buf && buf_cap > 0) buf[0] = '\0';
        return 0;
    }
}

/* =========================================================================
 * 4. Cell & Struct Containers
 * ========================================================================= */

numkit_val *numkit_cell_create(const size_t *dims, int ndims, numkit_error *err)
{
    clearErr(err);
    if (!dims || ndims <= 0) {
        setErr(err, 1, "numkit_cell_create: invalid dimensions");
        return nullptr;
    }
    try {
        size_t normDims[2] = {1, 1};
        const size_t *dPtr = dims;
        int actualNd = ndims;
        if (ndims == 1) {
            normDims[0] = 1;
            normDims[1] = dims[0];
            dPtr = normDims;
            actualNd = 2;
        }
        return makeHandle(Value::cellND(dPtr, actualNd, nullptr));
    } catch (const std::exception &e) {
        setErr(err, 1, e.what());
        return nullptr;
    }
}

numkit_val *numkit_cell_get(const numkit_val *cell, size_t linear_idx, numkit_error *err)
{
    clearErr(err);
    if (!cell || !cell->val.isCell()) {
        setErr(err, 1, "numkit_cell_get: receiver is not a cell array");
        return nullptr;
    }
    try {
        if (linear_idx >= cell->val.numel()) {
            setErr(err, 1, "numkit_cell_get: index out of bounds");
            return nullptr;
        }
        return makeHandle(cell->val.cellAt(linear_idx));
    } catch (const std::exception &e) {
        setErr(err, 1, e.what());
        return nullptr;
    }
}

int numkit_cell_set(numkit_val *cell, size_t linear_idx, const numkit_val *elem, numkit_error *err)
{
    clearErr(err);
    if (!cell || !cell->val.isCell() || !elem) {
        setErr(err, 1, "numkit_cell_set: invalid cell or element handle");
        return 1;
    }
    try {
        if (linear_idx >= cell->val.numel()) {
            setErr(err, 1, "numkit_cell_set: index out of bounds");
            return 1;
        }
        cell->val.cellAt(linear_idx) = elem->val;
        return 0;
    } catch (const std::exception &e) {
        setErr(err, 1, e.what());
        return 1;
    }
}

numkit_val *numkit_struct_create(size_t rows, size_t cols, numkit_error *err)
{
    clearErr(err);
    try {
        if (rows == 1 && cols == 1) {
            return makeHandle(Value::structure(nullptr));
        }
        return makeHandle(Value::structArray(rows, cols, nullptr));
    } catch (const std::exception &e) {
        setErr(err, 1, e.what());
        return nullptr;
    }
}

size_t numkit_struct_num_fields(const numkit_val *s)
{
    if (!s || !s->val.isStruct()) return 0;
    try {
        return s->val.fieldNamesInOrder().size();
    } catch (...) {
        return 0;
    }
}

size_t numkit_struct_field_name(const numkit_val *s, size_t field_idx, char *buf, size_t buf_cap)
{
    if (!s || !s->val.isStruct()) {
        if (buf && buf_cap > 0) buf[0] = '\0';
        return 0;
    }
    try {
        auto fields = s->val.fieldNamesInOrder();
        if (field_idx >= fields.size()) {
            if (buf && buf_cap > 0) buf[0] = '\0';
            return 0;
        }
        const std::string &name = fields[field_idx];
        if (buf && buf_cap > 0) {
            size_t n = std::min(name.size(), buf_cap - 1);
            std::memcpy(buf, name.data(), n);
            buf[n] = '\0';
        }
        return name.size();
    } catch (...) {
        if (buf && buf_cap > 0) buf[0] = '\0';
        return 0;
    }
}

numkit_val *numkit_struct_get(const numkit_val *s, size_t linear_idx, const char *field, numkit_error *err)
{
    clearErr(err);
    if (!s || !s->val.isStruct() || !field) {
        setErr(err, 1, "numkit_struct_get: invalid struct or field name");
        return nullptr;
    }
    try {
        if (s->val.isStructArray()) {
            if (linear_idx >= s->val.numel()) {
                setErr(err, 1, "numkit_struct_get: struct array index out of bounds");
                return nullptr;
            }
            const auto &elemMap = s->val.structArrayElem(linear_idx);
            auto it = elemMap.find(field);
            if (it == elemMap.end()) {
                setErr(err, 1, "numkit_struct_get: field not found");
                return nullptr;
            }
            return makeHandle(it->second);
        }
        if (linear_idx != 0) {
            setErr(err, 1, "numkit_struct_get: scalar struct index must be 0");
            return nullptr;
        }
        if (!s->val.hasField(field)) {
            setErr(err, 1, "numkit_struct_get: field not found");
            return nullptr;
        }
        return makeHandle(s->val.field(field));
    } catch (const std::exception &e) {
        setErr(err, 1, e.what());
        return nullptr;
    }
}

int numkit_struct_set(numkit_val *s, size_t linear_idx, const char *field, const numkit_val *val, numkit_error *err)
{
    clearErr(err);
    if (!s || !s->val.isStruct() || !field || !val) {
        setErr(err, 1, "numkit_struct_set: invalid argument");
        return 1;
    }
    try {
        s->val.setField(linear_idx, field, val->val);
        return 0;
    } catch (const std::exception &e) {
        setErr(err, 1, e.what());
        return 1;
    }
}

/* =========================================================================
 * 5. Function Dispatch & Evaluation
 * ========================================================================= */

int numkit_call(numkit_ctx *ctx,
            const char *ns,
            const char *name,
            const numkit_val *const *args,
            size_t nargs,
            size_t nargout,
            numkit_val **outs,
            numkit_error *err)
{
    clearErr(err);
    if (!ctx || !name || !*name) {
        setErr(err, 1, "numkit_call: null context or function name");
        return 1;
    }
    if (nargs > 0 && !args) {
        setErr(err, 1, "numkit_call: null args array with nargs > 0");
        return 1;
    }
    if (nargout > 0 && !outs) {
        setErr(err, 1, "numkit_call: null outs array with nargout > 0");
        return 1;
    }
    try {
        std::vector<Value> inVals;
        inVals.reserve(nargs);
        for (size_t i = 0; i < nargs; ++i) {
            if (!args[i]) {
                setErr(err, 1, "numkit_call: null input argument handle");
                return 1;
            }
            inVals.push_back(args[i]->val);
        }

        size_t allocSlots = nargout == 0 ? 1 : nargout;
        std::vector<Value> outVals(allocSlots);
        std::string nsStr = ns ? ns : "";

        if (!ctx->is_full && ctx->lite) {
            ctx->lite->invoke(nsStr,
                              name,
                              Span<const Value>(inVals.data(), inVals.size()),
                              nargout,
                              Span<Value>(outVals.data(), outVals.size()));
        }
#if defined(NUMKIT_C_ENABLE_FULL_ENGINE) && NUMKIT_C_ENABLE_FULL_ENGINE
        else if (ctx->is_full && ctx->full) {
            ctx->full->invoke(nsStr,
                              name,
                              Span<const Value>(inVals.data(), inVals.size()),
                              nargout,
                              Span<Value>(outVals.data(), outVals.size()));
        }
#endif
        else {
            setErr(err, 1, "numkit_call: invalid context state");
            return 1;
        }

        if (outs && nargout > 0) {
            for (size_t i = 0; i < nargout; ++i) {
                outs[i] = makeHandle(std::move(outVals[i]));
            }
        }
        return 0;
    } catch (const std::exception &e) {
        setErr(err, 1, e.what());
        return 1;
    } catch (...) {
        setErr(err, 1, "numkit_call: unknown exception");
        return 1;
    }
}

numkit_val *numkit_eval(numkit_ctx *ctx, const char *code, numkit_error *err)
{
    clearErr(err);
    if (!ctx || !code) {
        setErr(err, 1, "numkit_eval: null context or code");
        return nullptr;
    }
    if (!ctx->is_full) {
        setErr(err, 2, "numkit_eval requires a Full Engine context (numkit_ctx_create_full)");
        return nullptr;
    }
#if defined(NUMKIT_C_ENABLE_FULL_ENGINE) && NUMKIT_C_ENABLE_FULL_ENGINE
    try {
        Value res = ctx->full->engine().eval(code, /*suppressTopLevelDisplay=*/true);
        return makeHandle(std::move(res));
    } catch (const std::exception &e) {
        setErr(err, 1, e.what());
        return nullptr;
    } catch (...) {
        setErr(err, 1, "numkit_eval: unknown error");
        return nullptr;
    }
#else
    setErr(err, 2, "Full Engine not available in this build");
    return nullptr;
#endif
}

numkit_val *numkit_workspace_get(numkit_ctx *ctx, const char *name, numkit_error *err)
{
    clearErr(err);
    if (!ctx || !name) {
        setErr(err, 1, "numkit_workspace_get: null context or variable name");
        return nullptr;
    }
    if (!ctx->is_full) {
        setErr(err, 2, "numkit_workspace_get requires Full Engine context");
        return nullptr;
    }
#if defined(NUMKIT_C_ENABLE_FULL_ENGINE) && NUMKIT_C_ENABLE_FULL_ENGINE
    try {
        Value *v = ctx->full->engine().getVariable(name);
        if (!v) {
            setErr(err, 1, ("Undefined variable '" + std::string(name) + "'").c_str());
            return nullptr;
        }
        return makeHandle(*v);
    } catch (const std::exception &e) {
        setErr(err, 1, e.what());
        return nullptr;
    }
#else
    setErr(err, 2, "Full Engine not available");
    return nullptr;
#endif
}

int numkit_workspace_set(numkit_ctx *ctx, const char *name, const numkit_val *val, numkit_error *err)
{
    clearErr(err);
    if (!ctx || !name || !val) {
        setErr(err, 1, "numkit_workspace_set: null argument");
        return 1;
    }
    if (!ctx->is_full) {
        setErr(err, 2, "numkit_workspace_set requires Full Engine context");
        return 1;
    }
#if defined(NUMKIT_C_ENABLE_FULL_ENGINE) && NUMKIT_C_ENABLE_FULL_ENGINE
    try {
        ctx->full->engine().setVariable(name, val->val);
        return 0;
    } catch (const std::exception &e) {
        setErr(err, 1, e.what());
        return 1;
    }
#else
    setErr(err, 2, "Full Engine not available");
    return 1;
#endif
}

} // extern "C"
