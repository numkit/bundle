cmake_minimum_required(VERSION 3.20)
project(numkit_bundle CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

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

# ---------------------------------------------------------------------------
# 1. Foundation layers (compiled once for the entire ecosystem)
# ---------------------------------------------------------------------------
add_subdirectory(modules/value)
add_subdirectory(modules/sys)
add_subdirectory(modules/ops)

# ---------------------------------------------------------------------------
# 2. Core runtime & CLI (numkit, numkit_cli, numkit_codegen, numkit_gtest)
# ---------------------------------------------------------------------------
add_subdirectory(modules/numkit)

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
# 4. Unified GoogleTest suite (core + all toolboxes)
# ---------------------------------------------------------------------------
if(NUMKIT_BUILD_TESTS)
    enable_testing()

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
        endif()
    endforeach()
endif()
