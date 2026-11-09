// bindings/c_api/src/full_context.hpp
//
// Full Engine context wrapper for C-ABI Full mode (`numkit_ctx_create_full`).
// Compiled ONLY when NUMKIT_C_ENABLE_FULL_ENGINE == 1.
#pragma once

#if defined(NUMKIT_C_ENABLE_FULL_ENGINE) && NUMKIT_C_ENABLE_FULL_ENGINE

#include "lite_context.hpp"

#include <numkit/core/engine.hpp>
#include <numkit/core/plugin_loader.hpp>
#include <numkit/core/standard_engine.hpp>

#include <filesystem>
#include <stdexcept>
#include <string>
#include <vector>

namespace numkit::c_api {

class FullEngineContext
{
public:
    FullEngineContext()
    {
        auto libDir = detail::currentLibraryDir();
        if (!libDir.empty()) {
            engine_.pluginLoader().addSearchPath(libDir.string());
            engine_.pluginLoader().addSearchPath((libDir / "modules").string());
            if (libDir.has_parent_path()) {
                engine_.pluginLoader().addSearchPath((libDir.parent_path() / "bin").string());
                engine_.pluginLoader().addSearchPath((libDir.parent_path() / "bin" / "modules").string());
                engine_.pluginLoader().addSearchPath((libDir.parent_path() / "lib").string());
            }
        }
    }

    StandardEngine &engine() noexcept { return engine_; }
    const StandardEngine &engine() const noexcept { return engine_; }

    void addSearchDir(const std::string &dir)
    {
        if (!dir.empty()) {
            engine_.pluginLoader().addSearchPath(dir);
            extraDirs_.emplace_back(dir);
        }
    }

    void loadPlugin(const std::string &nameOrPath)
    {
        if (nameOrPath.empty()) {
            throw std::runtime_error("Empty plugin name or path");
        }
        std::error_code ec;
        if (std::filesystem::is_regular_file(nameOrPath, ec)) {
            if (!engine_.pluginLoader().loadModule(nameOrPath)) {
                throw std::runtime_error("Failed to load plugin from '" + nameOrPath + "'");
            }
            return;
        }
        std::string pkgPath = engine_.pluginLoader().findPackageLibrary(nameOrPath);
        if (!pkgPath.empty()) {
            if (!engine_.pluginLoader().loadModule(pkgPath)) {
                throw std::runtime_error("Failed to load plugin package '" + nameOrPath + "'");
            }
            return;
        }
        // Fallback: check extraDirs_ and currentLibraryDir()
        auto candidates = detail::candidateFilenames(nameOrPath);
        std::vector<std::filesystem::path> dirs = extraDirs_;
        auto libDir = detail::currentLibraryDir();
        if (!libDir.empty()) {
            dirs.push_back(libDir);
            dirs.push_back(libDir / "modules");
            if (libDir.has_parent_path()) {
                dirs.push_back(libDir.parent_path() / "bin" / "modules");
                dirs.push_back(libDir.parent_path() / "lib");
            }
        }
        for (const auto &d : dirs) {
            for (const auto &fname : candidates) {
                for (const auto &p : {d / fname, d / nameOrPath / fname, d / "modules" / nameOrPath / fname}) {
                    if (std::filesystem::is_regular_file(p, ec)) {
                        if (!engine_.pluginLoader().loadModule(p.string())) {
                            throw std::runtime_error("Failed to load plugin '" + p.string() + "'");
                        }
                        return;
                    }
                }
            }
        }
        throw std::runtime_error("Could not find plugin '" + nameOrPath + "'");
    }

    bool hasFunction(const std::string &ns, const std::string &name)
    {
        if (!ns.empty() && engine_.findExternal(ns + "." + name, &engine_.workspaceEnv())) {
            return true;
        }
        if (engine_.hasFunction(name) || engine_.isKnownLeafName(name)) {
            return true;
        }
        return !engine_.pluginLoader().moduleProvidingFunction(name).empty();
    }

    void invoke(const std::string &ns,
                const std::string &name,
                Span<const Value> args,
                size_t nargout,
                Span<Value> outs)
    {
        // Auto-load toolbox if needed
        if (!ns.empty() && !engine_.isPluginNamespace(ns)) {
            try {
                loadPlugin(ns);
            } catch (...) {}
        }
        engine_.pluginLoader().tryAutoLoadForFunction(name);

        // 1. Object method dispatch when first arg is OBJECT
        if (!args.empty() && args[0].isObject()) {
            const BuiltinClass *cls = engine_.findClass(args[0].objectClassName());
            if (cls) {
                auto mIt = cls->methods.find(name);
                if (mIt != cls->methods.end() && mIt->second) {
                    Value selfCopy = args[0];
                    Span<const Value> rest(args.data() + 1, args.size() - 1);
                    CallContext ctx{&engine_, &engine_.workspaceEnv()};
                    mIt->second(selfCopy, rest, nargout, outs, ctx);
                    return;
                }
            }
        }

        // 2. Direct ExternalFunc lookup (fast path, avoids parsing "@name")
        const ExternalFunc *ext = nullptr;
        if (!ns.empty()) {
            ext = engine_.findExternal(ns + "." + name, &engine_.workspaceEnv());
        }
        if (!ext) {
            ext = engine_.findExternal(name, &engine_.workspaceEnv());
        }
        if (ext) {
            CallContext ctx{&engine_, &engine_.workspaceEnv()};
            (*ext)(args, nargout, outs, ctx);
            return;
        }

        // 3. Fallback through callFunctionHandleMulti (supports user .m functions & class constructors)
        Value handle = Value::funcHandle(name, engine_.resource());
        auto res = engine_.callFunctionHandleMulti(handle, args, nargout == 0 ? 1 : nargout, &engine_.workspaceEnv());
        for (size_t i = 0; i < outs.size() && i < res.size(); ++i) {
            outs[i] = std::move(res[i]);
        }
    }

private:
    StandardEngine engine_;
    std::vector<std::filesystem::path> extraDirs_;
};

} // namespace numkit::c_api

#endif // NUMKIT_C_ENABLE_FULL_ENGINE
