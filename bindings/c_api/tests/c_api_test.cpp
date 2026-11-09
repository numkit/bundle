// bindings/c_api/tests/c_api_test.cpp
//
// Comprehensive GoogleTest suite for the NumKit C-ABI (`numkit_c.h`).
// Verifies Lite (engine-free toolbox-only) mode, Full Engine mode,
// zero-copy array views, structs/cells, host callbacks, and handle leak freedom.

#include "numkit_c.h"

#include <gtest/gtest.h>

#include <cmath>
#include <string>
#include <vector>

namespace {

struct ScopedLiveCheck {
    int64_t baseline;
    ScopedLiveCheck() : baseline(numkit_debug_live_values()) {}
    ~ScopedLiveCheck()
    {
        EXPECT_EQ(numkit_debug_live_values(), baseline) << "Leaked numkit_val* handles detected!";
    }
};

} // namespace

TEST(NumkitCApiTest, AbiVersionAndScalarPrimitives)
{
    ScopedLiveCheck leakGuard;
    EXPECT_EQ(numkit_abi_version(), static_cast<uint32_t>(NUMKIT_C_ABI_VERSION));

    numkit_error err{};
    numkit_val *s = numkit_val_scalar(42.5);
    ASSERT_NE(s, nullptr);
    EXPECT_EQ(numkit_val_type(s), NUMKIT_DTYPE_DOUBLE);
    EXPECT_EQ(numkit_val_numel(s), 1u);
    EXPECT_EQ(numkit_val_is_scalar(s), 1);
    EXPECT_DOUBLE_EQ(numkit_val_as_double(s, &err), 42.5);
    EXPECT_EQ(err.code, 0);
    numkit_val_release(s);

    numkit_val *b = numkit_val_logical(1);
    ASSERT_NE(b, nullptr);
    EXPECT_EQ(numkit_val_type(b), NUMKIT_DTYPE_LOGICAL);
    EXPECT_EQ(numkit_val_as_bool(b, &err), 1);
    numkit_val_release(b);

    numkit_val *z = numkit_val_complex_scalar(3.0, -4.0);
    ASSERT_NE(z, nullptr);
    EXPECT_EQ(numkit_val_type(z), NUMKIT_DTYPE_COMPLEX);
    double re = 0.0, im = 0.0;
    EXPECT_EQ(numkit_val_as_complex(z, &re, &im, &err), 0);
    EXPECT_DOUBLE_EQ(re, 3.0);
    EXPECT_DOUBLE_EQ(im, -4.0);
    numkit_val_release(z);
}

TEST(NumkitCApiTest, ZeroCopyViewAndAllocArray)
{
    ScopedLiveCheck leakGuard;
    numkit_error err{};

    // External column-major 2x3 matrix
    const double externalBuf[6] = {1.0, 2.0, 3.0, 4.0, 5.0, 6.0};
    const size_t dims[2] = {2, 3};

    numkit_val *view = numkit_val_view(externalBuf, NUMKIT_DTYPE_DOUBLE, dims, 2, &err);
    ASSERT_NE(view, nullptr) << err.message;
    EXPECT_EQ(err.code, 0);
    EXPECT_EQ(numkit_val_numel(view), 6u);
    EXPECT_EQ(numkit_val_ndims(view), 2u);

    size_t outDims[2] = {0, 0};
    EXPECT_EQ(numkit_val_dims(view, outDims, 2), 2u);
    EXPECT_EQ(outDims[0], 2u);
    EXPECT_EQ(outDims[1], 3u);

    // Zero-copy guarantee: raw_data pointer must equal externalBuf
    EXPECT_EQ(numkit_val_raw_data(view), static_cast<const void *>(externalBuf));
    EXPECT_EQ(numkit_val_raw_bytes(view), 6 * sizeof(double));
    numkit_val_release(view);

    // Direct in-place allocation
    void *mutPtr = nullptr;
    numkit_val *owned = numkit_val_alloc_array(NUMKIT_DTYPE_INT32, dims, 2, &mutPtr, &err);
    ASSERT_NE(owned, nullptr);
    ASSERT_NE(mutPtr, nullptr);
    auto *i32 = static_cast<int32_t *>(mutPtr);
    for (int i = 0; i < 6; ++i) i32[i] = (i + 1) * 10;

    const auto *readBack = static_cast<const int32_t *>(numkit_val_raw_data(owned));
    ASSERT_NE(readBack, nullptr);
    EXPECT_EQ(readBack[0], 10);
    EXPECT_EQ(readBack[5], 60);
    numkit_val_release(owned);
}

TEST(NumkitCApiTest, StructAndCellContainers)
{
    ScopedLiveCheck leakGuard;
    numkit_error err{};

    numkit_val *st = numkit_struct_create(1, 1, &err);
    ASSERT_NE(st, nullptr);
    numkit_val *f1 = numkit_val_scalar(3.14);
    numkit_val *f2 = numkit_val_string("lowpass");
    EXPECT_EQ(numkit_struct_set(st, 0, "order", f1, &err), 0);
    EXPECT_EQ(numkit_struct_set(st, 0, "mode", f2, &err), 0);
    numkit_val_release(f1);
    numkit_val_release(f2);

    EXPECT_EQ(numkit_struct_num_fields(st), 2u);
    char fname[64];
    numkit_struct_field_name(st, 0, fname, sizeof(fname));
    EXPECT_STREQ(fname, "order");

    numkit_val *got = numkit_struct_get(st, 0, "mode", &err);
    ASSERT_NE(got, nullptr);
    char sbuf[64];
    numkit_val_write_string(got, sbuf, sizeof(sbuf));
    EXPECT_STREQ(sbuf, "lowpass");
    numkit_val_release(got);
    numkit_val_release(st);
}

TEST(NumkitCApiTest, LiteContextSignalAndStatsToolboxes)
{
    ScopedLiveCheck leakGuard;
    numkit_error err{};

    numkit_ctx *ctx = numkit_ctx_create_lite(&err);
    ASSERT_NE(ctx, nullptr) << err.message;
    EXPECT_EQ(numkit_ctx_is_full(ctx), 0);

    // Load signal and stats plugins into the engine-free Lite context
    ASSERT_EQ(numkit_ctx_load_plugin(ctx, "signal", &err), 0) << err.message;
    ASSERT_EQ(numkit_ctx_load_plugin(ctx, "stats", &err), 0) << err.message;
    EXPECT_EQ(numkit_ctx_has_function(ctx, "signal", "butter"), 1);
    EXPECT_EQ(numkit_ctx_has_function(ctx, "stats", "normpdf"), 1);

    // [b, a] = butter(4, 0.25, 'low')
    numkit_val *argN = numkit_val_scalar(4.0);
    numkit_val *argWn = numkit_val_scalar(0.25);
    numkit_val *argType = numkit_val_char("low");
    const numkit_val *butterArgs[3] = {argN, argWn, argType};
    numkit_val *butterOuts[2] = {nullptr, nullptr};

    ASSERT_EQ(numkit_call(ctx, "signal", "butter", butterArgs, 3, 2, butterOuts, &err), 0)
        << err.message;
    ASSERT_NE(butterOuts[0], nullptr);
    ASSERT_NE(butterOuts[1], nullptr);
    EXPECT_EQ(numkit_val_numel(butterOuts[0]), 5u);
    EXPECT_EQ(numkit_val_numel(butterOuts[1]), 5u);

    const auto *aCoeffs = static_cast<const double *>(numkit_val_raw_data(butterOuts[1]));
    ASSERT_NE(aCoeffs, nullptr);
    EXPECT_NEAR(aCoeffs[0], 1.0, 1e-12);

    // Zero-copy filtfilt(b, a, x)
    std::vector<double> sig(64, 1.0);
    size_t sigDims[2] = {1, sig.size()};
    numkit_val *xView = numkit_val_view(sig.data(), NUMKIT_DTYPE_DOUBLE, sigDims, 2, &err);
    const numkit_val *ffArgs[3] = {butterOuts[0], butterOuts[1], xView};
    numkit_val *yOut = nullptr;
    ASSERT_EQ(numkit_call(ctx, "signal", "filtfilt", ffArgs, 3, 1, &yOut, &err), 0) << err.message;
    ASSERT_NE(yOut, nullptr);
    EXPECT_EQ(numkit_val_numel(yOut), sig.size());
    const auto *yData = static_cast<const double *>(numkit_val_raw_data(yOut));
    // DC gain of a lowpass Butterworth filter is 1.0, so constant 1.0 signal stays 1.0
    EXPECT_NEAR(yData[32], 1.0, 1e-9);

    numkit_val_release(yOut);
    numkit_val_release(xView);
    numkit_val_release(butterOuts[0]);
    numkit_val_release(butterOuts[1]);
    numkit_val_release(argN);
    numkit_val_release(argWn);
    numkit_val_release(argType);

    // stats.normpdf(0, 0, 1) == 1 / sqrt(2*pi)
    numkit_val *z0 = numkit_val_scalar(0.0);
    numkit_val *mu = numkit_val_scalar(0.0);
    numkit_val *sigma = numkit_val_scalar(1.0);
    const numkit_val *pdfArgs[3] = {z0, mu, sigma};
    numkit_val *pdfOut = nullptr;
    ASSERT_EQ(numkit_call(ctx, "stats", "normpdf", pdfArgs, 3, 1, &pdfOut, &err), 0) << err.message;
    EXPECT_NEAR(numkit_val_as_double(pdfOut, &err), 0.3989422804014327, 1e-12);
    numkit_val_release(pdfOut);
    numkit_val_release(z0);
    numkit_val_release(mu);
    numkit_val_release(sigma);

    numkit_ctx_destroy(ctx);
}

TEST(NumkitCApiTest, LiteContextCasSymbolicIntegration)
{
    ScopedLiveCheck leakGuard;
    numkit_error err{};

    numkit_ctx *ctx = numkit_ctx_create_lite(&err);
    ASSERT_NE(ctx, nullptr);
    ASSERT_EQ(numkit_ctx_load_plugin(ctx, "cas", &err), 0) << err.message;

    numkit_val *exprStr = numkit_val_char("2*x + 3");
    numkit_val *varStr = numkit_val_char("x");
    const numkit_val *symArgs[1] = {exprStr};
    numkit_val *symF = nullptr;
    ASSERT_EQ(numkit_call(ctx, "cas", "sym", symArgs, 1, 1, &symF, &err), 0) << err.message;

    const numkit_val *varArgs[1] = {varStr};
    numkit_val *symX = nullptr;
    ASSERT_EQ(numkit_call(ctx, "cas", "sym", varArgs, 1, 1, &symX, &err), 0) << err.message;

    const numkit_val *intArgs[2] = {symF, symX};
    numkit_val *symInt = nullptr;
    ASSERT_EQ(numkit_call(ctx, "cas", "int", intArgs, 2, 1, &symInt, &err), 0) << err.message;

    const numkit_val *charArgs[1] = {symInt};
    numkit_val *charOut = nullptr;
    ASSERT_EQ(numkit_call(ctx, "cas", "char", charArgs, 1, 1, &charOut, &err), 0) << err.message;

    char buf[128];
    numkit_val_write_string(charOut, buf, sizeof(buf));
    std::string result(buf);
    EXPECT_NE(result.find("x"), std::string::npos);

    numkit_val_release(charOut);
    numkit_val_release(symInt);
    numkit_val_release(symX);
    numkit_val_release(symF);
    numkit_val_release(varStr);
    numkit_val_release(exprStr);
    numkit_ctx_destroy(ctx);
}

static int hostScaleCallback(void *user_data,
                             const numkit_val *const *args,
                             size_t nargs,
                             size_t /*nargout*/,
                             numkit_val **outs,
                             numkit_error *err)
{
    if (nargs < 1) return 1;
    double factor = *static_cast<const double *>(user_data);
    double x = numkit_val_as_double(args[0], err);
    if (err->code != 0) return 1;
    outs[0] = numkit_val_scalar(x * factor);
    return 0;
}

TEST(NumkitCApiTest, HostCallbackRegistration)
{
    ScopedLiveCheck leakGuard;
    numkit_error err{};

    numkit_ctx *ctx = numkit_ctx_create_lite(&err);
    ASSERT_NE(ctx, nullptr);

    double factor = 7.0;
    ASSERT_EQ(numkit_ctx_register_fn(ctx, "host", "scale7", &hostScaleCallback, &factor, &err), 0)
        << err.message;

    numkit_val *in = numkit_val_scalar(6.0);
    const numkit_val *args[1] = {in};
    numkit_val *out = nullptr;
    ASSERT_EQ(numkit_call(ctx, "host", "scale7", args, 1, 1, &out, &err), 0) << err.message;
    EXPECT_DOUBLE_EQ(numkit_val_as_double(out, &err), 42.0);

    numkit_val_release(out);
    numkit_val_release(in);
    numkit_ctx_destroy(ctx);
}

TEST(NumkitCApiTest, FullEngineEvalAndWorkspace)
{
    ScopedLiveCheck leakGuard;
    numkit_error err{};

    numkit_ctx *ctx = numkit_ctx_create_full(&err);
    if (!ctx && err.code == 2) {
        GTEST_SKIP() << "Full Engine not linked in this test configuration";
    }
    ASSERT_NE(ctx, nullptr) << err.message;
    EXPECT_EQ(numkit_ctx_is_full(ctx), 1);

    numkit_val *res = numkit_eval(ctx, "M = magic(3); sum(diag(M))", &err);
    ASSERT_NE(res, nullptr) << err.message;
    EXPECT_DOUBLE_EQ(numkit_val_as_double(res, &err), 15.0);
    numkit_val_release(res);

    numkit_val *mVar = numkit_workspace_get(ctx, "M", &err);
    ASSERT_NE(mVar, nullptr) << err.message;
    EXPECT_EQ(numkit_val_numel(mVar), 9u);
    numkit_val_release(mVar);

    numkit_ctx_destroy(ctx);
}
