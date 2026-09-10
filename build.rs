//! Compiles TA-Lib (the `ta-lib` git submodule) into a static library linked into the plugin.
//! The source directories are the ones TA-Lib's own CMakeLists.txt puts into `ta-lib-static`.

use std::fs;
use std::path::Path;

const TA_LIB: &str = "ta-lib";
const SOURCE_DIRS: [&str; 5] = [
    "src/ta_common",
    "src/ta_abstract",
    "src/ta_abstract/tables",
    "src/ta_abstract/frames",
    "src/ta_func",
];

fn main() {
    let root = Path::new(TA_LIB);
    let mut build = cc::Build::new();
    for dir in SOURCE_DIRS {
        let dir = root.join(dir);
        let entries = fs::read_dir(&dir).unwrap_or_else(|e| {
            panic!("{}: {e} (run `git submodule update --init`)", dir.display())
        });
        for entry in entries {
            let path = entry.unwrap().path();
            if path.extension().is_some_and(|ext| ext == "c") {
                build.file(path);
            }
        }
        build.include(&dir);
    }
    build.include(root.join("include")).warnings(false).compile("ta-lib");
    println!("cargo:rerun-if-changed={TA_LIB}/VERSION");
}
