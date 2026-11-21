cmake_minimum_required(VERSION 3.20)
project(numkit_bundle CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

option(NUMKIT_WITH_SIMD "Enable Highway SIMD acceleration" ON)
option(NUMKIT_BUILD_CLI "Build numkit CLI executable" ON)
option(NUMKIT_BUILD_CODEGEN "Build numkit_codegen AOT transpiler CLI" ON)
option(NUMKIT_BUILD_TESTS "Build GoogleTest suites for core and all toolboxes" ON)

# Unified output directory for executables and shared libraries
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib")

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/../ops/build/_deps/highway-src/CMakeLists.txt")
    set(FETCHCONTENT_SOURCE_DIR_HIGHWAY
        "${CMAKE_CURRENT_SOURCE_DIR}/../ops/build/_deps/highway-src"
        CACHE PATH "" FORCE)
endif()

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/../numkit/build/_deps/googletest-src/CMakeLists.txt")
    set(FETCHCONTENT_SOURCE_DIR_GOOGLETEST
        "${CMAKE_CURRENT_SOURCE_DIR}/../numkit/build/_deps/googletest-src"
        CACHE PATH "" FORCE)
endif()

# Local sibling keelcpp checkouts (offline / developer fast-path)
foreach(_keel_pair
    "KEEL:keel"
    "KEEL_COMPRESS:compress"
    "KEEL_IMAGE:image"
    "KEEL_AUDIO:audio"
    "KEEL_FFT:fft"
    "KEEL_RANDOM:random"
    "KEEL_LINALG:linalg"
    "KEEL_MAT:mat"
    "KEEL_BIGNUM:bignum"
    "KEEL_SPECFUN:specfun"
    "KEEL_GEOM:geom"
    "KEEL_INTERP:interp"
    "KEEL_ODE:ode"
    "KEEL_QUAD:quad"
    "KEEL_OPTIM:optim"
    "KEEL_POLY:poly"
    "KEEL_WAVELET:wavelet"
    "KEEL_STATS:stats"
)
    string(REPLACE ":" ";" _keel_parts "${_keel_pair}")
    list(GET _keel_parts 0 _keel_var)
    list(GET _keel_parts 1 _keel_dir)
    if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/../../keelcpp/${_keel_dir}/CMakeLists.txt"
       AND NOT DEFINED FETCHCONTENT_SOURCE_DIR_${_keel_var})
        set(FETCHCONTENT_SOURCE_DIR_${_keel_var}
            "${CMAKE_CURRENT_SOURCE_DIR}/../../keelcpp/${_keel_dir}"
            CACHE PATH "" FORCE)
    endif()
endforeach()

# ---------------------------------------------------------------------------
# 1. Foundation layers (compiled once for the entire ecosystem)
# ---------------------------------------------------------------------------
add_subdirectory(modules/value)
add_subdirectory(modules/sys)
add_subdirectory(modules/ops)

# ---------------------------------------------------------------------------
# 2. Core runtime & CLI (numkit, numkit_cli, numkit_gtest)
# ---------------------------------------------------------------------------
add_subdirectory(modules/numkit)

# ---------------------------------------------------------------------------
# 2b. AOT C++ Transpiler & Static Type Inference (numkit/codegen)
# ---------------------------------------------------------------------------
if(NUMKIT_BUILD_CODEGEN AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/modules/codegen/CMakeLists.txt")
    add_subdirectory(modules/codegen)
endif()

# ---------------------------------------------------------------------------
# 3. Domain plugin toolboxes
# ---------------------------------------------------------------------------
set(NUMKIT_TOOLBOXES
    signal
    control
    stats
    wavelet
    audio
    comm
    image
    cas
)

set(STAGE_COMMANDS "")
set(STAGE_DEPENDS "")

foreach(tb IN LISTS NUMKIT_TOOLBOXES)
    add_subdirectory("modules/${tb}")
    if(TARGET numkit_${tb} AND TARGET numkit_cli)
        list(APPEND STAGE_DEPENDS numkit_${tb} numkit_cli)
        list(APPEND STAGE_COMMANDS
            COMMAND ${CMAKE_COMMAND} -E make_directory "$<TARGET_FILE_DIR:numkit_cli>/modules/${tb}"
            COMMAND ${CMAKE_COMMAND} -E copy_if_different
                "$<TARGET_FILE:numkit_${tb}>"
                "$<TARGET_FILE_DIR:numkit_cli>/modules/${tb}/"
            COMMAND ${CMAKE_COMMAND} -E copy_if_different
                "${CMAKE_CURRENT_SOURCE_DIR}/modules/${tb}/manifest.json"
                "$<TARGET_FILE_DIR:numkit_cli>/modules/${tb}/manifest.json"
        )
    endif()
endforeach()

if(STAGE_COMMANDS)
    add_custom_target(numkit_stage_plugins ALL
        ${STAGE_COMMANDS}
        DEPENDS ${STAGE_DEPENDS}
        COMMENT "Staging all NumKit plugin libraries and manifests into <exe_dir>/modules/*"
    )
endif()

# ---------------------------------------------------------------------------
# 3b. Build-time Keel Guidelines enforcement across non-foundation modules
#     (numkit_value and numkit_sys enforce strict BAN_RAW_INTS ALL directly)
# ---------------------------------------------------------------------------
if(COMMAND keel_enforce_guidelines)
    set(_NUMKIT_ALLOW_TRANSITIONAL_HEADERS
        algorithm atomic cerrno charconv climits cstddef cstdint
        cstdio cstdlib deque iterator limits mutex numeric regex tuple
        type_traits utility
    )
    set(_NUMKIT_GUIDELINE_TARGETS
        "numkit_ops:modules/ops/include"
        "numkit:modules/numkit/include"
        "numkit_codegen_lib:modules/codegen/include"
    )
    foreach(tb IN LISTS NUMKIT_TOOLBOXES)
        list(APPEND _NUMKIT_GUIDELINE_TARGETS "numkit_${tb}_core:modules/${tb}/include")
    endforeach()
    foreach(_gt_pair IN LISTS _NUMKIT_GUIDELINE_TARGETS)
        string(REPLACE ":" ";" _gt_parts "${_gt_pair}")
        list(GET _gt_parts 0 _gt_target)
        list(GET _gt_parts 1 _gt_inc)
        if(TARGET "${_gt_target}")
            keel_enforce_guidelines("${_gt_target}"
                SCOPE ALL
                BAN_STL ON
                BAN_RAW_INTS OFF
                ALLOW_STDEXCEPT ON
                ALLOW_STDEXCEPT_IN_HEADERS ON
                HEADERS_DIR "${CMAKE_CURRENT_SOURCE_DIR}/${_gt_inc}"
                ALLOWED_ANGLE_PREFIXES "numkit/" "hwy/"
                ALLOW_HEADERS ${_NUMKIT_ALLOW_TRANSITIONAL_HEADERS}
                EXCLUDE_FILES "c_api\\.h$" "c_api\\.cpp$"
                WARNINGS OFF
            )
        endif()
    endforeach()
endif()

# ---------------------------------------------------------------------------
# 4. Unified GoogleTest suite & architectural checks (core + all toolboxes)
# ---------------------------------------------------------------------------
if(NUMKIT_BUILD_TESTS)
    enable_testing()

    find_package(Python3 COMPONENTS Interpreter QUIET)
    if(Python3_Interpreter_FOUND)
        add_test(
            NAME numkit_check_layering
            COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/scripts/check_layering.py"
        )
        add_test(
            NAME numkit_check_api
            COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/scripts/check_api.py"
        )
    endif()

    # Per-toolbox GoogleTest executables
    foreach(tb IN LISTS NUMKIT_TOOLBOXES)
        if(NOT TARGET numkit_${tb}_test)
            file(GLOB TB_TEST_SOURCES "modules/${tb}/tests/*_test.cpp")
            if(TB_TEST_SOURCES)
                add_executable(numkit_${tb}_test ${TB_TEST_SOURCES})
                target_include_directories(numkit_${tb}_test PRIVATE
                    "${CMAKE_CURRENT_SOURCE_DIR}/modules/${tb}"
                    "${CMAKE_CURRENT_SOURCE_DIR}/modules/${tb}/src"
                    "${CMAKE_CURRENT_SOURCE_DIR}/modules/${tb}/tests"
                    "${CMAKE_CURRENT_SOURCE_DIR}/modules/ops/src"
                    "${CMAKE_CURRENT_SOURCE_DIR}/modules/ops/src/image_io"
                )
                target_link_libraries(numkit_${tb}_test PRIVATE
                    numkit_${tb}_core
                    numkit
                    GTest::gtest_main
                )
                if(NUMKIT_WITH_SIMD)
                    target_link_libraries(numkit_${tb}_test PRIVATE hwy hwy_contrib)
                endif()
                add_dependencies(numkit_${tb}_test numkit_${tb})
                if(TARGET numkit_stage_plugins)
                    add_dependencies(numkit_${tb}_test numkit_stage_plugins)
                endif()
                if(MSVC)
                    target_compile_options(numkit_${tb}_test PRIVATE /W3 /MP /bigobj)
                endif()
                add_test(NAME numkit_${tb}_test COMMAND numkit_${tb}_test)
            endif()
        elseif(TARGET numkit_stage_plugins)
            add_dependencies(numkit_${tb}_test numkit_stage_plugins)
        endif()
    endforeach()
endif()
