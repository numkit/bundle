//! Integration tests for the safe Rust SDK (`numkit`).

use numkit::{cas, live_values_count, signal, stats, Context, Value};

#[test]
fn test_lite_signal_butter_and_zero_copy_view() {
    let baseline = live_values_count();
    {
        let ctx = Context::new_lite().expect("create_lite failed");
        assert!(!ctx.is_full());

        // Level 1: Strongly-typed C++ signature wrapper
        let (b, a) = signal::butter_typed(&ctx, 4, 0.25, "low").expect("butter_typed failed");
        assert_eq!(b.numel(), 5);
        assert_eq!(a.numel(), 5);
        assert!((a.as_f64_slice().unwrap()[0] - 1.0).abs() < 1e-12);

        // Zero-copy slice view via Value::view_f64
        let input_signal = vec![1.0_f64; 64];
        let x_view = Value::view_f64(&input_signal, &[1, input_signal.len()])
            .expect("view_f64 failed");

        // Level 2: Dynamic / overload call
        let y = signal::filtfilt(&ctx, &[&b, &a, &x_view]).expect("filtfilt failed");
        let y_slice = y.as_f64_slice().expect("as_f64_slice failed");
        assert_eq!(y_slice.len(), 64);
        assert!((y_slice[32] - 1.0).abs() < 1e-9);
    }
    assert_eq!(
        live_values_count(),
        baseline,
        "All numkit_val handles must be dropped when leaving scope"
    );
}

#[test]
fn test_lite_stats_and_cas() {
    let baseline = live_values_count();
    {
        let ctx = Context::new_lite().expect("create_lite failed");

        let z0 = Value::scalar(0.0).unwrap();
        let mu = Value::scalar(0.0).unwrap();
        let sigma = Value::scalar(1.0).unwrap();
        let pdf = stats::normpdf_typed(&ctx, &z0, &mu, &sigma).expect("normpdf_typed failed");
        assert!((pdf.as_f64().unwrap() - 0.3989422804014327).abs() < 1e-12);

        let expr_str = Value::from_char("2*x + 3").unwrap();
        let var_str = Value::from_char("x").unwrap();
        let sym_f = cas::sym(&ctx, &[&expr_str]).expect("cas::sym failed");
        let sym_x = cas::sym(&ctx, &[&var_str]).expect("cas::sym failed");
        let sym_int = cas::int(&ctx, &[&sym_f, &sym_x]).expect("cas::int failed");
        let char_out = cas::char(&ctx, &[&sym_int]).expect("cas::char failed");
        assert!(char_out.to_string_lossy().contains('x'));
    }
    assert_eq!(live_values_count(), baseline);
}

#[test]
fn test_full_engine_eval() {
    let baseline = live_values_count();
    {
        if let Ok(ctx) = Context::new_full() {
            assert!(ctx.is_full());
            let v = ctx
                .eval("M = magic(3); sum(diag(M))")
                .expect("eval failed");
            assert!((v.as_f64().unwrap() - 15.0).abs() < 1e-12);
        }
    }
    assert_eq!(live_values_count(), baseline);
}
