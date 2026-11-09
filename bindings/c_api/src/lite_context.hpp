// bindings/c_api/src/lite_context.hpp
//
// Engine-free PluginContext implementation for Lite C-ABI mode.
// Depends ONLY on L0/L1 (`numkit/value`, `numkit/sys`, `numkit/ops`).
// Zero dependency on `numkit/core` (no parser, AST, TreeWalker, or VM).
#pragma once

#include <numkit/ops/rng_context.hpp>
#include <numkit/sys/fs_context.hpp>
#include <numkit/sys/plugin.hpp>
#include <numkit/value/error.hpp>
#include <numkit/value/object.hpp>
#include <numkit/value/span.hpp>
#include <numkit/value/value.hpp>

#include <cstdlib>
#include <filesystem>
#include <memory>
#include <memory_resource>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#if defined(_WIN32)
#  define WIN32_LEAN_AND_MEAN
#  ifndef NOMINMAX
#    define NOMINMAX
#  endif
#  include <windows.h>
#else
#  include <dlfcn.h>
#endif

namespace numkit::c_api {

namespace detail {

inline void *osLoadSharedLib(const char *path)
{
#if defined(_WIN32)
    return static_cast<void *>(LoadLibraryA(path));
#else
    return dlopen(path, RTLD_NOW | RTLD_LOCAL);
#endif
}

inline void *osGetSymbol(void *handle, const char *symbol)
{
#if defined(_WIN32)
    return reinterpret_cast<void *>(GetProcAddress(static_cast<HMODULE>(handle), symbol));
#else
    return dlsym(handle, symbol);
#endif
}

inline std::string osLastDlError()
{
#if defined(_WIN32)
    DWORD err = GetLastError();
    char  buf[256];
    DWORD len = FormatMessageA(FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
                               nullptr, err, MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
                               buf, sizeof(buf), nullptr);
    return len > 0 ? std::string(buf, len) : ("Win32 error " + std::to_string(err));
#else
    const char *e = dlerror();
    return e ? std::string(e) : "dlopen error";
#endif
}

inline std::filesystem::path currentLibraryDir()
{
#if defined(_WIN32)
    HMODULE hm = nullptr;
    if (GetModuleHandleExA(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS |
                               GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
                           reinterpret_cast<LPCSTR>(&currentLibraryDir), &hm)) {
        char path[MAX_PATH];
        DWORD len = GetModuleFileNameA(hm, path, MAX_PATH);
        if (len > 0) {
            return std::filesystem::path(std::string(path, len)).parent_path();
        }
    }
#else
    Dl_info info{};
    if (dladdr(reinterpret_cast<const void *>(&currentLibraryDir), &info) && info.dli_fname) {
        std::error_code ec;
        auto p = std::filesystem::canonical(info.dli_fname, ec);
        if (!ec) return p.parent_path();
        return std::filesystem::path(info.dli_fname).parent_path();
    }
#endif
    std::error_code ec;
    return std::filesystem::current_path(ec);
}

inline std::vector<std::string> candidateFilenames(const std::string &tb)
{
#if defined(_WIN32)
    return {"numkit_" + tb + ".dll", "libnumkit_" + tb + ".dll"};
#elif defined(__APPLE__)
    return {"libnumkit_" + tb + ".dylib", "libnumkit_" + tb + ".so", "numkit_" + tb + ".dylib"};
#else
    return {"libnumkit_" + tb + ".so", "numkit_" + tb + ".so"};
#endif
}

} // namespace detail

class LitePluginContext final : public PluginContext
{
public:
    explicit LitePluginContext(std::pmr::memory_resource *mr = std::pmr::get_default_resource())
        : mr_(mr ? mr : std::pmr::get_default_resource())
    {
        auto libDir = detail::currentLibraryDir();
        if (!libDir.empty()) {
            searchDirs_.push_back(libDir);
            searchDirs_.push_back(libDir / "modules");
            if (libDir.has_parent_path()) {
                searchDirs_.push_back(libDir.parent_path() / "bin");
                searchDirs_.push_back(libDir.parent_path() / "bin" / "modules");
                searchDirs_.push_back(libDir.parent_path() / "lib");
            }
        }
        if (const char *envPath = std::getenv("NUMKIT_MODULE_PATH")) {
            if (*envPath) {
                searchDirs_.emplace_back(envPath);
            }
        }
    }

    ~LitePluginContext() override = default;

    std::pmr::memory_resource *resource() const noexcept override { return mr_; }

    void registerFunction(const std::string &ns, const std::string &name, ExternalFunc func) override
    {
        if (name.empty() || !func) return;
        ExternalFunc wrapped = wrapWithSelf(std::move(func));
        if (!ns.empty()) {
            qualifiedFuncs_[ns + "." + name] = wrapped;
            auto dot = ns.find('.');
            if (dot != std::string::npos) {
                std::string topNs = ns.substr(0, dot);
                if (!topNs.empty()) {
                    qualifiedFuncs_[topNs + "." + name] = wrapped;
                }
            }
        }
        bareFuncs_[name] = std::move(wrapped);
    }

    void registerFunction(const std::string &name, ExternalFunc func) override
    {
        if (name.empty() || !func) return;
        bareFuncs_[name] = wrapWithSelf(std::move(func));
    }

    Value callFunctionHandle(const Value &handle, Span<const Value> args, void * /*env*/) override
    {
        auto res = callFunctionHandleMulti(handle, args, 1, nullptr);
        return res.empty() ? Value() : std::move(res[0]);
    }

    std::vector<Value> callFunctionHandleMulti(const Value &handle,
                                               Span<const Value> args,
                                               size_t nargout,
                                               void * /*env*/) override
    {
        std::string fnName;
        if (handle.isFuncHandle()) {
            fnName = handle.funcHandleName();
        } else if (handle.isChar() || handle.isString()) {
            fnName = handle.toString();
        }
        if (fnName.empty() || fnName[0] == '@') {
            throw std::runtime_error(
                "Anonymous MATLAB source closures require Full Engine context (numkit_ctx_create_full)");
        }
        const ExternalFunc *fn = findExternal(fnName, nullptr);
        if (!fn) {
            throw std::runtime_error("Undefined function handle '" + fnName + "' in Lite context");
        }
        size_t actualOut = nargout == 0 ? 1 : nargout;
        std::vector<Value> outs(actualOut);
        CallContext ctx{reinterpret_cast<Engine *>(static_cast<PluginContext *>(this)), nullptr};
        (*fn)(args, nargout, Span<Value>(outs.data(), outs.size()), ctx);
        return outs;
    }

    ops::RngContext &rng() override { return rng_; }

    FsContext::ResolvedPath resolvePath(const std::string &userPath) const override
    {
        return fs_.resolvePath(userPath);
    }

    FigureManager &figureManager() override
    {
        throw std::runtime_error("FigureManager is not available in Lite context");
    }

    const ExternalFunc *findExternal(const std::string &name, const Environment * /*env*/) const override
    {
        auto qIt = qualifiedFuncs_.find(name);
        if (qIt != qualifiedFuncs_.end()) return &qIt->second;
        auto bIt = bareFuncs_.find(name);
        if (bIt != bareFuncs_.end()) return &bIt->second;
        return nullptr;
    }

    void registerClass(BuiltinClass cls) override
    {
        std::string className = cls.name;
        if (cls.construct && bareFuncs_.find(className) == bareFuncs_.end()) {
            auto ctor = cls.construct;
            registerFunction(className, [ctor](Span<const Value> args,
                                               size_t /*nargout*/,
                                               Span<Value> outs,
                                               CallContext &ctx) {
                if (!outs.empty()) {
                    outs[0] = ctor(args, ctx);
                }
            });
        }
        classes_[className] = std::move(cls);
    }

    const BuiltinClass *findClass(const std::string &name) const override
    {
        auto it = classes_.find(name);
        return it != classes_.end() ? &it->second : nullptr;
    }

    void assignToCaller(int /*n*/, const std::string &name, Value val) override
    {
        callerVars_[name] = std::move(val);
    }

    void addSearchDir(const std::string &dir)
    {
        if (!dir.empty()) {
            searchDirs_.emplace_back(dir);
        }
    }

    bool hasFunction(const std::string &ns, const std::string &name) const
    {
        if (!ns.empty()) {
            if (qualifiedFuncs_.count(ns + "." + name) > 0) return true;
        }
        return bareFuncs_.count(name) > 0;
    }

    void invoke(const std::string &ns,
                const std::string &name,
                Span<const Value> args,
                size_t nargout,
                Span<Value> outs)
    {
        CallContext ctx{reinterpret_cast<Engine *>(static_cast<PluginContext *>(this)), nullptr};

        // 1. Check object method dispatch if first argument is an OBJECT
        if (!args.empty() && args[0].isObject()) {
            const BuiltinClass *cls = findClass(args[0].objectClassName());
            if (cls) {
                auto mIt = cls->methods.find(name);
                if (mIt != cls->methods.end() && mIt->second) {
                    Value selfCopy = args[0];
                    Span<const Value> rest(args.data() + 1, args.size() - 1);
                    mIt->second(selfCopy, rest, nargout, outs, ctx);
                    return;
                }
                auto opIt = cls->ops.find(name);
                if (opIt != cls->ops.end() && opIt->second) {
                    Value selfCopy = args[0];
                    opIt->second(selfCopy, args, nargout, outs, ctx);
                    return;
                }
            }
        }

        // 2. Qualified lookup (`ns.name`), then bare lookup (`name`)
        const ExternalFunc *fn = nullptr;
        if (!ns.empty()) {
            fn = findExternal(ns + "." + name, nullptr);
        }
        if (!fn) {
            fn = findExternal(name, nullptr);
        }
        if (!fn) {
            std::string full = ns.empty() ? name : (ns + "." + name);
            throw std::runtime_error("Undefined function '" + full + "'");
        }
        (*fn)(args, nargout, outs, ctx);
    }

    void loadPlugin(const std::string &nameOrPath)
    {
        if (nameOrPath.empty()) {
            throw std::runtime_error("Empty plugin name or path");
        }
        if (loadedNames_.count(nameOrPath) > 0) {
            return;
        }

        std::filesystem::path resolved = resolvePluginLibraryPath(nameOrPath);
        std::string canonicalStr = resolved.lexically_normal().string();
        if (loadedPaths_.count(canonicalStr) > 0) {
            loadedNames_.insert(nameOrPath);
            return;
        }

        void *handle = detail::osLoadSharedLib(resolved.string().c_str());
        if (!handle) {
            throw std::runtime_error("Failed to load plugin '" + resolved.string() +
                                     "': " + detail::osLastDlError());
        }

        auto initFn = reinterpret_cast<NumkitPluginInitFn>(
            detail::osGetSymbol(handle, "numkit_plugin_init"));
        if (!initFn) {
            throw std::runtime_error("Plugin '" + resolved.string() +
                                     "' does not export numkit_plugin_init");
        }

        if (!initFn(*this)) {
            throw std::runtime_error("Plugin '" + resolved.string() +
                                     "' failed ABI version check or initialization");
        }

        loadedPaths_.insert(canonicalStr);
        loadedNames_.insert(nameOrPath);
    }

    std::string formatObject(const Value &v) const
    {
        if (!v.isObject()) return v.toString();
        const BuiltinClass *cls = findClass(v.objectClassName());
        if (cls) {
            auto charIt = cls->methods.find("char");
            if (charIt != cls->methods.end() && charIt->second) {
                Value selfCopy = v;
                Value out;
                CallContext ctx{
                    reinterpret_cast<Engine *>(const_cast<LitePluginContext *>(this)), nullptr};
                charIt->second(selfCopy, Span<const Value>(), 1, Span<Value>(&out, 1), ctx);
                if (out.isChar() || out.isString()) {
                    return out.toString();
                }
            }
            if (cls->dispText) {
                std::string s = cls->dispText(v);
                while (!s.empty() && (s.front() == ' ' || s.front() == '\n')) s.erase(s.begin());
                while (!s.empty() && (s.back() == ' ' || s.back() == '\n')) s.pop_back();
                return s;
            }
        }
        return "<" + v.objectClassName() + " object>";
    }

private:
    ExternalFunc wrapWithSelf(ExternalFunc func)
    {
        return [this, fn = std::move(func)](Span<const Value> args,
                                            size_t nargout,
                                            Span<Value> outs,
                                            CallContext &ctx) {
            CallContext localCtx = ctx;
            localCtx.engine = reinterpret_cast<Engine *>(static_cast<PluginContext *>(this));
            fn(args, nargout, outs, localCtx);
        };
    }

    std::filesystem::path resolvePluginLibraryPath(const std::string &nameOrPath) const
    {
        std::error_code ec;
        std::filesystem::path direct(nameOrPath);
        if (std::filesystem::is_regular_file(direct, ec)) {
            return direct;
        }

        auto filenames = detail::candidateFilenames(nameOrPath);
        for (const auto &dir : searchDirs_) {
            for (const auto &fname : filenames) {
                auto p1 = dir / fname;
                if (std::filesystem::is_regular_file(p1, ec)) return p1;
                auto p2 = dir / nameOrPath / fname;
                if (std::filesystem::is_regular_file(p2, ec)) return p2;
                auto p3 = dir / "modules" / nameOrPath / fname;
                if (std::filesystem::is_regular_file(p3, ec)) return p3;
            }
        }

        throw std::runtime_error("Could not locate plugin library for '" + nameOrPath + "'");
    }

    std::pmr::memory_resource *mr_;
    ops::RngContext rng_;
    FsContext fs_;
    std::unordered_map<std::string, ExternalFunc> qualifiedFuncs_;
    std::unordered_map<std::string, ExternalFunc> bareFuncs_;
    std::unordered_map<std::string, BuiltinClass> classes_;
    std::unordered_map<std::string, Value> callerVars_;
    std::vector<std::filesystem::path> searchDirs_;
    std::unordered_set<std::string> loadedPaths_;
    std::unordered_set<std::string> loadedNames_;
};

} // namespace numkit::c_api
