use std::env;
use std::path::PathBuf;

fn main() {
    let manifest_dir = PathBuf::from(env::var("CARGO_MANIFEST_DIR").unwrap());
    let bundle_root = manifest_dir
        .parent()
        .and_then(|p| p.parent())
        .expect("Failed to locate bundle root");

    if let Ok(lib_dir) = env::var("NUMKIT_LIB_DIR") {
        println!("cargo:rustc-link-search=native={lib_dir}");
    } else {
        let build_lib = bundle_root.join("build").join("lib");
        let build_bin = bundle_root.join("build").join("bin");
        println!("cargo:rustc-link-search=native={}", build_lib.display());
        println!("cargo:rustc-link-search=native={}", build_bin.display());
        println!(
            "cargo:rustc-link-search=native={}",
            build_lib.join("Release").display()
        );
    }

    let link_lite_only = env::var("NUMKIT_LITE_ONLY").map(|v| v == "1").unwrap_or(false);
    if link_lite_only {
        println!("cargo:rustc-link-lib=dylib=numkit_c_lite");
    } else {
        println!("cargo:rustc-link-lib=dylib=numkit_c");
    }
    println!(
        "cargo:rerun-if-changed={}",
        bundle_root
            .join("bindings/c_api/include/numkit_c.h")
            .display()
    );
}
