# bindings/CMakeLists.txt
#
# Builds the canonical C-ABI libraries:
#   - numkit_c_lite : Engine-free toolbox-only C-ABI (links only value + sys + ops)
#   - numkit_c      : Full C-ABI supporting both Lite and Full Engine modes

set(NUMKIT_C_API_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/c_api/include")
set(NUMKIT_C_API_SOURCES     "${CMAKE_CURRENT_SOURCE_DIR}/c_api/src/numkit_c.cpp")

# ---------------------------------------------------------------------------
# 1. Engine-free Lite C-ABI library (libnumkit_c_lite)
# ---------------------------------------------------------------------------
add_library(numkit_c_lite SHARED ${NUMKIT_C_API_SOURCES})
add_library(numkit::c_lite ALIAS numkit_c_lite)

target_include_directories(numkit_c_lite
    PUBLIC
        $<BUILD_INTERFACE:${NUMKIT_C_API_INCLUDE_DIR}>
        $<INSTALL_INTERFACE:include>
    PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}/c_api/src"
)

target_compile_definitions(numkit_c_lite
    PRIVATE
        NUMKIT_C_BUILDING_DLL=1
        NUMKIT_C_ENABLE_FULL_ENGINE=0
)

target_link_libraries(numkit_c_lite
    PRIVATE
        numkit_value
        numkit_sys
        numkit_ops
        ${CMAKE_DL_LIBS}
)

if(NUMKIT_WITH_SIMD AND TARGET hwy)
    target_link_libraries(numkit_c_lite PRIVATE hwy hwy_contrib)
endif()

if(MSVC)
    target_compile_options(numkit_c_lite PRIVATE /W4 /MP /bigobj)
else()
    target_compile_options(numkit_c_lite PRIVATE -Wall -Wextra -fPIC)
endif()

# ---------------------------------------------------------------------------
# 2. Unified Full + Lite C-ABI library (libnumkit_c)
# ---------------------------------------------------------------------------
if(TARGET numkit)
    add_library(numkit_c SHARED ${NUMKIT_C_API_SOURCES})
    add_library(numkit::c ALIAS numkit_c)

    target_include_directories(numkit_c
        PUBLIC
            $<BUILD_INTERFACE:${NUMKIT_C_API_INCLUDE_DIR}>
            $<INSTALL_INTERFACE:include>
        PRIVATE
            "${CMAKE_CURRENT_SOURCE_DIR}/c_api/src"
    )

    target_compile_definitions(numkit_c
        PRIVATE
            NUMKIT_C_BUILDING_DLL=1
            NUMKIT_C_ENABLE_FULL_ENGINE=1
            NUMKIT_CORE_BUILD=1
    )

    target_link_libraries(numkit_c
        PRIVATE
            numkit
            numkit_value
            numkit_sys
            numkit_ops
            ${CMAKE_DL_LIBS}
    )

    if(NUMKIT_WITH_SIMD AND TARGET hwy)
        target_link_libraries(numkit_c PRIVATE hwy hwy_contrib)
    endif()

    if(MSVC)
        target_compile_options(numkit_c PRIVATE /W4 /MP /bigobj)
    else()
        target_compile_options(numkit_c PRIVATE -Wall -Wextra -fPIC)
    endif()
endif()

# ---------------------------------------------------------------------------
# 3. C-ABI GoogleTest Suite
# ---------------------------------------------------------------------------
if(NUMKIT_BUILD_TESTS AND TARGET GTest::gtest_main)
    add_executable(numkit_c_api_test c_api/tests/c_api_test.cpp)
    target_include_directories(numkit_c_api_test PRIVATE ${NUMKIT_C_API_INCLUDE_DIR})

    if(TARGET numkit_c)
        target_link_libraries(numkit_c_api_test PRIVATE numkit_c GTest::gtest_main)
    else()
        target_link_libraries(numkit_c_api_test PRIVATE numkit_c_lite GTest::gtest_main)
    endif()

    if(TARGET numkit_stage_plugins)
        add_dependencies(numkit_c_api_test numkit_stage_plugins)
    endif()

    add_test(NAME numkit_c_api_test COMMAND numkit_c_api_test)
endif()
