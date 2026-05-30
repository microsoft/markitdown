const RUNTIME_PUBLIC_PATH = "server/chunks/ssr/[turbopack]_runtime.js";
const RELATIVE_ROOT_PATH = "../..";
const ASSET_PREFIX = "/_next/";
const WORKER_FORWARDED_GLOBALS = ["NEXT_DEPLOYMENT_ID","NEXT_CLIENT_ASSET_SUFFIX"];
// Apply forwarded globals from workerData if running in a worker thread
if (typeof require !== 'undefined') {
    try {
        const { workerData } = require('worker_threads');
        if (workerData?.__turbopack_globals__) {
            Object.assign(globalThis, workerData.__turbopack_globals__);
            // Remove internal data so it's not visible to user code
            delete workerData.__turbopack_globals__;
        }
    } catch (_) {
        // Not in a worker thread context, ignore
    }
}
/**
 * This file contains runtime types and functions that are shared between all
 * TurboPack ECMAScript runtimes.
 *
 * It will be prepended to the runtime code of each runtime.
 */ /* eslint-disable @typescript-eslint/no-unused-vars */ /// <reference path="./runtime-types.d.ts" />
/**
 * Describes why a module was instantiated.
 * Shared between browser and Node.js runtimes.
 */ var SourceType = /*#__PURE__*/ function(SourceType) {
    /**
   * The module was instantiated because it was included in an evaluated chunk's
   * runtime.
   * SourceData is a ChunkPath.
   */ SourceType[SourceType["Runtime"] = 0] = "Runtime";
    /**
   * The module was instantiated because a parent module imported it.
   * SourceData is a ModuleId.
   */ SourceType[SourceType["Parent"] = 1] = "Parent";
    /**
   * The module was instantiated because it was included in a chunk's hot module
   * update.
   * SourceData is an array of ModuleIds or undefined.
   */ SourceType[SourceType["Update"] = 2] = "Update";
    return SourceType;
}(SourceType || {});
/**
 * Flag indicating which module object type to create when a module is merged. Set to `true`
 * by each runtime that uses ModuleWithDirection (browser dev-base.ts, nodejs dev-base.ts,
 * nodejs build-base.ts). Browser production (build-base.ts) leaves it as `false` since it
 * uses plain Module objects.
 */ let createModuleWithDirectionFlag = false;
const REEXPORTED_OBJECTS = new WeakMap();
/**
 * Constructs the `__turbopack_context__` object for a module.
 */ function Context(module, exports) {
    this.m = module;
    // We need to store this here instead of accessing it from the module object to:
    // 1. Make it available to factories directly, since we rewrite `this` to
    //    `__turbopack_context__.e` in CJS modules.
    // 2. Support async modules which rewrite `module.exports` to a promise, so we
    //    can still access the original exports object from functions like
    //    `esmExport`
    // Ideally we could find a new approach for async modules and drop this property altogether.
    this.e = exports;
}
const contextPrototype = Context.prototype;
const hasOwnProperty = Object.prototype.hasOwnProperty;
const toStringTag = typeof Symbol !== 'undefined' && Symbol.toStringTag;
function defineProp(obj, name, options) {
    if (!hasOwnProperty.call(obj, name)) Object.defineProperty(obj, name, options);
}
function getOverwrittenModule(moduleCache, id) {
    let module = moduleCache[id];
    if (!module) {
        if (createModuleWithDirectionFlag) {
            // set in development modes for hmr support
            module = createModuleWithDirection(id);
        } else {
            module = createModuleObject(id);
        }
        moduleCache[id] = module;
    }
    return module;
}
/**
 * Creates the module object. Only done here to ensure all module objects have the same shape.
 */ function createModuleObject(id) {
    return {
        exports: {},
        error: undefined,
        id,
        namespaceObject: undefined
    };
}
function createModuleWithDirection(id) {
    return {
        exports: {},
        error: undefined,
        id,
        namespaceObject: undefined,
        parents: [],
        children: []
    };
}
const BindingTag_Value = 0;
/**
 * Adds the getters to the exports object.
 */ function esm(exports, bindings) {
    defineProp(exports, '__esModule', {
        value: true
    });
    if (toStringTag) defineProp(exports, toStringTag, {
        value: 'Module'
    });
    let i = 0;
    while(i < bindings.length){
        const propName = bindings[i++];
        const tagOrFunction = bindings[i++];
        if (typeof tagOrFunction === 'number') {
            if (tagOrFunction === BindingTag_Value) {
                defineProp(exports, propName, {
                    value: bindings[i++],
                    enumerable: true,
                    writable: false
                });
            } else {
                throw new Error(`unexpected tag: ${tagOrFunction}`);
            }
        } else {
            const getterFn = tagOrFunction;
            if (typeof bindings[i] === 'function') {
                const setterFn = bindings[i++];
                defineProp(exports, propName, {
                    get: getterFn,
                    set: setterFn,
                    enumerable: true
                });
            } else {
                defineProp(exports, propName, {
                    get: getterFn,
                    enumerable: true
                });
            }
        }
    }
    Object.seal(exports);
}
/**
 * Makes the module an ESM with exports
 */ function esmExport(bindings, id) {
    let module;
    let exports;
    if (id != null) {
        module = getOverwrittenModule(this.c, id);
        exports = module.exports;
    } else {
        module = this.m;
        exports = this.e;
    }
    module.namespaceObject = exports;
    esm(exports, bindings);
}
contextPrototype.s = esmExport;
function ensureDynamicExports(module, exports) {
    let reexportedObjects = REEXPORTED_OBJECTS.get(module);
    if (!reexportedObjects) {
        REEXPORTED_OBJECTS.set(module, reexportedObjects = []);
        module.exports = module.namespaceObject = new Proxy(exports, {
            get (target, prop) {
                if (hasOwnProperty.call(target, prop) || prop === 'default' || prop === '__esModule') {
                    return Reflect.get(target, prop);
                }
                for (const obj of reexportedObjects){
                    const value = Reflect.get(obj, prop);
                    if (value !== undefined) return value;
                }
                return undefined;
            },
            ownKeys (target) {
                const keys = Reflect.ownKeys(target);
                for (const obj of reexportedObjects){
                    for (const key of Reflect.ownKeys(obj)){
                        if (key !== 'default' && !keys.includes(key)) keys.push(key);
                    }
                }
                return keys;
            }
        });
    }
    return reexportedObjects;
}
/**
 * Dynamically exports properties from an object
 */ function dynamicExport(object, id) {
    let module;
    let exports;
    if (id != null) {
        module = getOverwrittenModule(this.c, id);
        exports = module.exports;
    } else {
        module = this.m;
        exports = this.e;
    }
    const reexportedObjects = ensureDynamicExports(module, exports);
    if (typeof object === 'object' && object !== null) {
        reexportedObjects.push(object);
    }
}
contextPrototype.j = dynamicExport;
function exportValue(value, id) {
    let module;
    if (id != null) {
        module = getOverwrittenModule(this.c, id);
    } else {
        module = this.m;
    }
    module.exports = value;
}
contextPrototype.v = exportValue;
function exportNamespace(namespace, id) {
    let module;
    if (id != null) {
        module = getOverwrittenModule(this.c, id);
    } else {
        module = this.m;
    }
    module.exports = module.namespaceObject = namespace;
}
contextPrototype.n = exportNamespace;
function createGetter(obj, key) {
    return ()=>obj[key];
}
/**
 * @returns prototype of the object
 */ const getProto = Object.getPrototypeOf ? (obj)=>Object.getPrototypeOf(obj) : (obj)=>obj.__proto__;
/** Prototypes that are not expanded for exports */ const LEAF_PROTOTYPES = [
    null,
    getProto({}),
    getProto([]),
    getProto(getProto)
];
/**
 * @param raw
 * @param ns
 * @param allowExportDefault
 *   * `false`: will have the raw module as default export
 *   * `true`: will have the default property as default export
 */ function interopEsm(raw, ns, allowExportDefault) {
    const bindings = [];
    let defaultLocation = -1;
    for(let current = raw; (typeof current === 'object' || typeof current === 'function') && !LEAF_PROTOTYPES.includes(current); current = getProto(current)){
        for (const key of Object.getOwnPropertyNames(current)){
            bindings.push(key, createGetter(raw, key));
            if (defaultLocation === -1 && key === 'default') {
                defaultLocation = bindings.length - 1;
            }
        }
    }
    // this is not really correct
    // we should set the `default` getter if the imported module is a `.cjs file`
    if (!(allowExportDefault && defaultLocation >= 0)) {
        // Replace the binding with one for the namespace itself in order to preserve iteration order.
        if (defaultLocation >= 0) {
            // Replace the getter with the value
            bindings.splice(defaultLocation, 1, BindingTag_Value, raw);
        } else {
            bindings.push('default', BindingTag_Value, raw);
        }
    }
    esm(ns, bindings);
    return ns;
}
function createNS(raw) {
    if (typeof raw === 'function') {
        return function(...args) {
            return raw.apply(this, args);
        };
    } else {
        return Object.create(null);
    }
}
function esmImport(id) {
    const module = getOrInstantiateModuleFromParent(id, this.m);
    // any ES module has to have `module.namespaceObject` defined.
    if (module.namespaceObject) return module.namespaceObject;
    // only ESM can be an async module, so we don't need to worry about exports being a promise here.
    const raw = module.exports;
    return module.namespaceObject = interopEsm(raw, createNS(raw), raw && raw.__esModule);
}
contextPrototype.i = esmImport;
function asyncLoader(moduleId) {
    const loader = this.r(moduleId);
    return loader(esmImport.bind(this));
}
contextPrototype.A = asyncLoader;
// Add a simple runtime require so that environments without one can still pass
// `typeof require` CommonJS checks so that exports are correctly registered.
const runtimeRequire = // @ts-ignore
typeof require === 'function' ? require : function require1() {
    throw new Error('Unexpected use of runtime require');
};
contextPrototype.t = runtimeRequire;
function commonJsRequire(id) {
    return getOrInstantiateModuleFromParent(id, this.m).exports;
}
contextPrototype.r = commonJsRequire;
/**
 * Remove fragments and query parameters since they are never part of the context map keys
 *
 * This matches how we parse patterns at resolving time.  Arguably we should only do this for
 * strings passed to `import` but the resolve does it for `import` and `require` and so we do
 * here as well.
 */ function parseRequest(request) {
    // Per the URI spec fragments can contain `?` characters, so we should trim it off first
    // https://datatracker.ietf.org/doc/html/rfc3986#section-3.5
    const hashIndex = request.indexOf('#');
    if (hashIndex !== -1) {
        request = request.substring(0, hashIndex);
    }
    const queryIndex = request.indexOf('?');
    if (queryIndex !== -1) {
        request = request.substring(0, queryIndex);
    }
    return request;
}
/**
 * `require.context` and require/import expression runtime.
 */ function moduleContext(map) {
    function moduleContext(id) {
        id = parseRequest(id);
        if (hasOwnProperty.call(map, id)) {
            return map[id].module();
        }
        const e = new Error(`Cannot find module '${id}'`);
        e.code = 'MODULE_NOT_FOUND';
        throw e;
    }
    moduleContext.keys = ()=>{
        return Object.keys(map);
    };
    moduleContext.resolve = (id)=>{
        id = parseRequest(id);
        if (hasOwnProperty.call(map, id)) {
            return map[id].id();
        }
        const e = new Error(`Cannot find module '${id}'`);
        e.code = 'MODULE_NOT_FOUND';
        throw e;
    };
    moduleContext.import = async (id)=>{
        return await moduleContext(id);
    };
    return moduleContext;
}
contextPrototype.f = moduleContext;
/**
 * Returns the path of a chunk defined by its data.
 */ function getChunkPath(chunkData) {
    return typeof chunkData === 'string' ? chunkData : chunkData.path;
}
function isPromise(maybePromise) {
    return maybePromise != null && typeof maybePromise === 'object' && 'then' in maybePromise && typeof maybePromise.then === 'function';
}
function isAsyncModuleExt(obj) {
    return turbopackQueues in obj;
}
function createPromise() {
    let resolve;
    let reject;
    const promise = new Promise((res, rej)=>{
        reject = rej;
        resolve = res;
    });
    return {
        promise,
        resolve: resolve,
        reject: reject
    };
}
// Load the CompressedmoduleFactories of a chunk into the `moduleFactories` Map.
// The CompressedModuleFactories format is
// - 1 or more module ids
// - a module factory function
// So walking this is a little complex but the flat structure is also fast to
// traverse, we can use `typeof` operators to distinguish the two cases.
function installCompressedModuleFactories(chunkModules, offset, moduleFactories, newModuleId) {
    let i = offset;
    while(i < chunkModules.length){
        let end = i + 1;
        // Find our factory function
        while(end < chunkModules.length && typeof chunkModules[end] !== 'function'){
            end++;
        }
        if (end === chunkModules.length) {
            throw new Error('malformed chunk format, expected a factory function');
        }
        // Install the factory for each module ID that doesn't already have one.
        // When some IDs in this group already have a factory, reuse that existing
        // group factory for the missing IDs to keep all IDs in the group consistent.
        // Otherwise, install the factory from this chunk.
        const moduleFactoryFn = chunkModules[end];
        let existingGroupFactory = undefined;
        for(let j = i; j < end; j++){
            const id = chunkModules[j];
            const existingFactory = moduleFactories.get(id);
            if (existingFactory) {
                existingGroupFactory = existingFactory;
                break;
            }
        }
        const factoryToInstall = existingGroupFactory ?? moduleFactoryFn;
        let didInstallFactory = false;
        for(let j = i; j < end; j++){
            const id = chunkModules[j];
            if (!moduleFactories.has(id)) {
                if (!didInstallFactory) {
                    if (factoryToInstall === moduleFactoryFn) {
                        applyModuleFactoryName(moduleFactoryFn);
                    }
                    didInstallFactory = true;
                }
                moduleFactories.set(id, factoryToInstall);
                newModuleId?.(id);
            }
        }
        i = end + 1; // end is pointing at the last factory advance to the next id or the end of the array.
    }
}
// everything below is adapted from webpack
// https://github.com/webpack/webpack/blob/6be4065ade1e252c1d8dcba4af0f43e32af1bdc1/lib/runtime/AsyncModuleRuntimeModule.js#L13
const turbopackQueues = Symbol('turbopack queues');
const turbopackExports = Symbol('turbopack exports');
const turbopackError = Symbol('turbopack error');
function resolveQueue(queue) {
    if (queue && queue.status !== 1) {
        queue.status = 1;
        queue.forEach((fn)=>fn.queueCount--);
        queue.forEach((fn)=>fn.queueCount-- ? fn.queueCount++ : fn());
    }
}
function wrapDeps(deps) {
    return deps.map((dep)=>{
        if (dep !== null && typeof dep === 'object') {
            if (isAsyncModuleExt(dep)) return dep;
            if (isPromise(dep)) {
                const queue = Object.assign([], {
                    status: 0
                });
                const obj = {
                    [turbopackExports]: {},
                    [turbopackQueues]: (fn)=>fn(queue)
                };
                dep.then((res)=>{
                    obj[turbopackExports] = res;
                    resolveQueue(queue);
                }, (err)=>{
                    obj[turbopackError] = err;
                    resolveQueue(queue);
                });
                return obj;
            }
        }
        return {
            [turbopackExports]: dep,
            [turbopackQueues]: ()=>{}
        };
    });
}
function asyncModule(body, hasAwait) {
    const module = this.m;
    const queue = hasAwait ? Object.assign([], {
        status: -1
    }) : undefined;
    const depQueues = new Set();
    const { resolve, reject, promise: rawPromise } = createPromise();
    const promise = Object.assign(rawPromise, {
        [turbopackExports]: module.exports,
        [turbopackQueues]: (fn)=>{
            queue && fn(queue);
            depQueues.forEach(fn);
            promise['catch'](()=>{});
        }
    });
    const attributes = {
        get () {
            return promise;
        },
        set (v) {
            // Calling `esmExport` leads to this.
            if (v !== promise) {
                promise[turbopackExports] = v;
            }
        }
    };
    Object.defineProperty(module, 'exports', attributes);
    Object.defineProperty(module, 'namespaceObject', attributes);
    function handleAsyncDependencies(deps) {
        const currentDeps = wrapDeps(deps);
        const getResult = ()=>currentDeps.map((d)=>{
                if (d[turbopackError]) throw d[turbopackError];
                return d[turbopackExports];
            });
        const { promise, resolve } = createPromise();
        const fn = Object.assign(()=>resolve(getResult), {
            queueCount: 0
        });
        function fnQueue(q) {
            if (q !== queue && !depQueues.has(q)) {
                depQueues.add(q);
                if (q && q.status === 0) {
                    fn.queueCount++;
                    q.push(fn);
                }
            }
        }
        currentDeps.map((dep)=>dep[turbopackQueues](fnQueue));
        return fn.queueCount ? promise : getResult();
    }
    function asyncResult(err) {
        if (err) {
            reject(promise[turbopackError] = err);
        } else {
            resolve(promise[turbopackExports]);
        }
        resolveQueue(queue);
    }
    body(handleAsyncDependencies, asyncResult);
    if (queue && queue.status === -1) {
        queue.status = 0;
    }
}
contextPrototype.a = asyncModule;
/**
 * A pseudo "fake" URL object to resolve to its relative path.
 *
 * When UrlRewriteBehavior is set to relative, calls to the `new URL()` will construct url without base using this
 * runtime function to generate context-agnostic urls between different rendering context, i.e ssr / client to avoid
 * hydration mismatch.
 *
 * This is based on webpack's existing implementation:
 * https://github.com/webpack/webpack/blob/87660921808566ef3b8796f8df61bd79fc026108/lib/runtime/RelativeUrlRuntimeModule.js
 */ const relativeURL = function relativeURL(inputUrl) {
    const realUrl = new URL(inputUrl, 'x:/');
    const values = {};
    for(const key in realUrl)values[key] = realUrl[key];
    values.href = inputUrl;
    values.pathname = inputUrl.replace(/[?#].*/, '');
    values.origin = values.protocol = '';
    values.toString = values.toJSON = (..._args)=>inputUrl;
    for(const key in values)Object.defineProperty(this, key, {
        enumerable: true,
        configurable: true,
        value: values[key]
    });
};
relativeURL.prototype = URL.prototype;
contextPrototype.U = relativeURL;
/**
 * Utility function to ensure all variants of an enum are handled.
 */ function invariant(never, computeMessage) {
    throw new Error(`Invariant: ${computeMessage(never)}`);
}
/**
 * Constructs an error message for when a module factory is not available.
 */ function factoryNotAvailableMessage(moduleId, sourceType, sourceData) {
    let instantiationReason;
    switch(sourceType){
        case 0:
            instantiationReason = `as a runtime entry of chunk ${sourceData}`;
            break;
        case 1:
            instantiationReason = `because it was required from module ${sourceData}`;
            break;
        case 2:
            instantiationReason = 'because of an HMR update';
            break;
        default:
            invariant(sourceType, (sourceType)=>`Unknown source type: ${sourceType}`);
    }
    return `Module ${moduleId} was instantiated ${instantiationReason}, but the module factory is not available.`;
}
/**
 * A stub function to make `require` available but non-functional in ESM.
 */ function requireStub(_moduleId) {
    throw new Error('dynamic usage of require is not supported');
}
contextPrototype.z = requireStub;
// Make `globalThis` available to the module in a way that cannot be shadowed by a local variable.
contextPrototype.g = globalThis;
function applyModuleFactoryName(factory) {
    // Give the module factory a nice name to improve stack traces.
    Object.defineProperty(factory, 'name', {
        value: 'module evaluation'
    });
}
/// <reference path="../shared/runtime/runtime-utils.ts" />
/// A 'base' utilities to support runtime can have externals.
/// Currently this is for node.js / edge runtime both.
/// If a fn requires node.js specific behavior, it should be placed in `node-external-utils` instead.
async function externalImport(id) {
    let raw;
    try {
        raw = await import(id);
    } catch (err) {
        // TODO(alexkirsz) This can happen when a client-side module tries to load
        // an external module we don't provide a shim for (e.g. querystring, url).
        // For now, we fail semi-silently, but in the future this should be a
        // compilation error.
        throw new Error(`Failed to load external module ${id}: ${err}`);
    }
    if (raw && raw.__esModule && raw.default && 'default' in raw.default) {
        return interopEsm(raw.default, createNS(raw), true);
    }
    return raw;
}
contextPrototype.y = externalImport;
function externalRequire(id, thunk, esm = false) {
    let raw;
    try {
        raw = thunk();
    } catch (err) {
        // TODO(alexkirsz) This can happen when a client-side module tries to load
        // an external module we don't provide a shim for (e.g. querystring, url).
        // For now, we fail semi-silently, but in the future this should be a
        // compilation error.
        throw new Error(`Failed to load external module ${id}: ${err}`);
    }
    if (!esm || raw.__esModule) {
        return raw;
    }
    return interopEsm(raw, createNS(raw), true);
}
externalRequire.resolve = (id, options)=>{
    return require.resolve(id, options);
};
contextPrototype.x = externalRequire;
/* eslint-disable @typescript-eslint/no-unused-vars */ const path = require('path');
const relativePathToRuntimeRoot = path.relative(RUNTIME_PUBLIC_PATH, '.');
// Compute the relative path to the `distDir`.
const relativePathToDistRoot = path.join(relativePathToRuntimeRoot, RELATIVE_ROOT_PATH);
const RUNTIME_ROOT = path.resolve(__filename, relativePathToRuntimeRoot);
// Compute the absolute path to the root, by stripping distDir from the absolute path to this file.
const ABSOLUTE_ROOT = path.resolve(__filename, relativePathToDistRoot);
/**
 * Returns an absolute path to the given module path.
 * Module path should be relative, either path to a file or a directory.
 *
 * This fn allows to calculate an absolute path for some global static values, such as
 * `__dirname` or `import.meta.url` that Turbopack will not embeds in compile time.
 * See ImportMetaBinding::code_generation for the usage.
 */ function resolveAbsolutePath(modulePath) {
    if (modulePath) {
        return path.join(ABSOLUTE_ROOT, modulePath);
    }
    return ABSOLUTE_ROOT;
}
Context.prototype.P = resolveAbsolutePath;
/* eslint-disable @typescript-eslint/no-unused-vars */ /// <reference path="../shared/runtime/runtime-utils.ts" />
function readWebAssemblyAsResponse(path) {
    const { createReadStream } = require('fs');
    const { Readable } = require('stream');
    const stream = createReadStream(path);
    // @ts-ignore unfortunately there's a slight type mismatch with the stream.
    return new Response(Readable.toWeb(stream), {
        headers: {
            'content-type': 'application/wasm'
        }
    });
}
async function compileWebAssemblyFromPath(path) {
    const response = readWebAssemblyAsResponse(path);
    return await WebAssembly.compileStreaming(response);
}
async function instantiateWebAssemblyFromPath(path, importsObj) {
    const response = readWebAssemblyAsResponse(path);
    const { instance } = await WebAssembly.instantiateStreaming(response, importsObj);
    return instance.exports;
}
/* eslint-disable @typescript-eslint/no-unused-vars */ /// <reference path="../../shared/runtime/runtime-utils.ts" />
/// <reference path="../../shared-node/base-externals-utils.ts" />
/// <reference path="../../shared-node/node-externals-utils.ts" />
/// <reference path="../../shared-node/node-wasm-utils.ts" />
/// <reference path="./nodejs-globals.d.ts" />
/**
 * Base Node.js runtime shared between production and development.
 * Contains chunk loading, module caching, and other non-HMR functionality.
 */ process.env.TURBOPACK = '1';
const url = require('url');
const moduleFactories = new Map();
const moduleCache = Object.create(null);
/**
 * Returns an absolute path to the given module's id.
 */ function resolvePathFromModule(moduleId) {
    const exported = this.r(moduleId);
    const exportedPath = exported?.default ?? exported;
    if (typeof exportedPath !== 'string') {
        return exported;
    }
    const strippedAssetPrefix = exportedPath.slice(ASSET_PREFIX.length);
    const resolved = path.resolve(RUNTIME_ROOT, strippedAssetPrefix);
    return url.pathToFileURL(resolved).href;
}
/**
 * Exports a URL value. No suffix is added in Node.js runtime.
 */ function exportUrl(urlValue, id) {
    exportValue.call(this, urlValue, id);
}
function loadRuntimeChunk(sourcePath, chunkData) {
    if (typeof chunkData === 'string') {
        loadRuntimeChunkPath(sourcePath, chunkData);
    } else {
        loadRuntimeChunkPath(sourcePath, chunkData.path);
    }
}
const loadedChunks = new Set();
const unsupportedLoadChunk = Promise.resolve(undefined);
const loadedChunk = Promise.resolve(undefined);
const chunkCache = new Map();
function clearChunkCache() {
    chunkCache.clear();
    loadedChunks.clear();
}
function loadRuntimeChunkPath(sourcePath, chunkPath) {
    if (!isJs(chunkPath)) {
        // We only support loading JS chunks in Node.js.
        // This branch can be hit when trying to load a CSS chunk.
        return;
    }
    if (loadedChunks.has(chunkPath)) {
        return;
    }
    try {
        const resolved = path.resolve(RUNTIME_ROOT, chunkPath);
        const chunkModules = require(resolved);
        installCompressedModuleFactories(chunkModules, 0, moduleFactories);
        loadedChunks.add(chunkPath);
    } catch (cause) {
        let errorMessage = `Failed to load chunk ${chunkPath}`;
        if (sourcePath) {
            errorMessage += ` from runtime for chunk ${sourcePath}`;
        }
        const error = new Error(errorMessage, {
            cause
        });
        error.name = 'ChunkLoadError';
        throw error;
    }
}
function loadChunkAsync(chunkData) {
    const chunkPath = typeof chunkData === 'string' ? chunkData : chunkData.path;
    if (!isJs(chunkPath)) {
        // We only support loading JS chunks in Node.js.
        // This branch can be hit when trying to load a CSS chunk.
        return unsupportedLoadChunk;
    }
    let entry = chunkCache.get(chunkPath);
    if (entry === undefined) {
        try {
            // resolve to an absolute path to simplify `require` handling
            const resolved = path.resolve(RUNTIME_ROOT, chunkPath);
            // TODO: consider switching to `import()` to enable concurrent chunk loading and async file io
            // However this is incompatible with hot reloading (since `import` doesn't use the require cache)
            const chunkModules = require(resolved);
            installCompressedModuleFactories(chunkModules, 0, moduleFactories);
            entry = loadedChunk;
        } catch (cause) {
            const errorMessage = `Failed to load chunk ${chunkPath} from module ${this.m.id}`;
            const error = new Error(errorMessage, {
                cause
            });
            error.name = 'ChunkLoadError';
            // Cache the failure promise, future requests will also get this same rejection
            entry = Promise.reject(error);
        }
        chunkCache.set(chunkPath, entry);
    }
    // TODO: Return an instrumented Promise that React can use instead of relying on referential equality.
    return entry;
}
contextPrototype.l = loadChunkAsync;
function loadChunkAsyncByUrl(chunkUrl) {
    const path1 = url.fileURLToPath(new URL(chunkUrl, RUNTIME_ROOT));
    return loadChunkAsync.call(this, path1);
}
contextPrototype.L = loadChunkAsyncByUrl;
function loadWebAssembly(chunkPath, _edgeModule, imports) {
    const resolved = path.resolve(RUNTIME_ROOT, chunkPath);
    return instantiateWebAssemblyFromPath(resolved, imports);
}
contextPrototype.w = loadWebAssembly;
function loadWebAssemblyModule(chunkPath, _edgeModule) {
    const resolved = path.resolve(RUNTIME_ROOT, chunkPath);
    return compileWebAssemblyFromPath(resolved);
}
contextPrototype.u = loadWebAssemblyModule;
/**
 * Creates a Node.js worker thread by instantiating the given WorkerConstructor
 * with the appropriate path and options, including forwarded globals.
 *
 * @param WorkerConstructor The Worker constructor from worker_threads
 * @param workerPath Path to the worker entry chunk
 * @param workerOptions options to pass to the Worker constructor (optional)
 */ function createWorker(WorkerConstructor, workerPath, workerOptions) {
    // Build the forwarded globals object
    const forwardedGlobals = {};
    for (const name of WORKER_FORWARDED_GLOBALS){
        forwardedGlobals[name] = globalThis[name];
    }
    // Merge workerData with forwarded globals
    const existingWorkerData = workerOptions?.workerData || {};
    const options = {
        ...workerOptions,
        workerData: {
            ...typeof existingWorkerData === 'object' ? existingWorkerData : {},
            __turbopack_globals__: forwardedGlobals
        }
    };
    return new WorkerConstructor(workerPath, options);
}
const regexJsUrl = /\.js(?:\?[^#]*)?(?:#.*)?$/;
/**
 * Checks if a given path/URL ends with .js, optionally followed by ?query or #fragment.
 */ function isJs(chunkUrlOrPath) {
    return regexJsUrl.test(chunkUrlOrPath);
}
/// <reference path="./runtime-utils.ts" />
/// <reference path="./runtime-types.d.ts" />
/// <reference path="./dev-extensions.ts" />
/// <reference path="./dev-protocol.d.ts" />
/**
 * Shared HMR (Hot Module Replacement) implementation.
 *
 * This file contains the complete HMR implementation that's shared between
 * browser and Node.js runtimes. It manages module hot state, dependency
 * tracking, the module.hot API, and the full HMR update flow.
 */ /**
 * The development module cache shared across the runtime.
 * Browser runtime declares this directly.
 * Node.js runtime assigns globalThis.__turbopack_module_cache__ to this.
 */ let devModuleCache;
/**
 * Module IDs that are instantiated as part of the runtime of a chunk.
 */ let runtimeModules;
/**
 * Maps module IDs to persisted data between executions of their hot module
 * implementation (`hot.data`).
 */ const moduleHotData = new Map();
/**
 * Maps module instances to their hot module state.
 * Uses WeakMap so it works with both HotModule and ModuleWithDirection.
 */ const moduleHotState = new WeakMap();
/**
 * Modules that call `module.hot.invalidate()` (while being updated).
 */ const queuedInvalidatedModules = new Set();
class UpdateApplyError extends Error {
    name = 'UpdateApplyError';
    dependencyChain;
    constructor(message, dependencyChain){
        super(message);
        this.dependencyChain = dependencyChain;
    }
}
/**
 * Records parent-child relationship when a module imports another.
 * Should be called during module instantiation.
 */ // eslint-disable-next-line @typescript-eslint/no-unused-vars
function trackModuleImport(parentModule, childModuleId, childModule) {
    // Record that parent imports child
    if (parentModule.children.indexOf(childModuleId) === -1) {
        parentModule.children.push(childModuleId);
    }
    // Record that child is imported by parent
    if (childModule && childModule.parents.indexOf(parentModule.id) === -1) {
        childModule.parents.push(parentModule.id);
    }
}
function formatDependencyChain(dependencyChain) {
    return `Dependency chain: ${dependencyChain.join(' -> ')}`;
}
/**
 * Walks the dependency tree to find all modules affected by a change.
 * Returns information about whether the update can be accepted and which
 * modules need to be invalidated.
 *
 * @param moduleId - The module that changed
 * @param autoAcceptRootModules - If true, root modules auto-accept updates without explicit module.hot.accept().
 *                           This is used for server-side HMR where pages auto-accept at the top level.
 */ function getAffectedModuleEffects(moduleId, autoAcceptRootModules) {
    const outdatedModules = new Set();
    const outdatedDependencies = new Map();
    const queue = [
        {
            moduleId,
            dependencyChain: []
        }
    ];
    let nextItem;
    while(nextItem = queue.shift()){
        const { moduleId, dependencyChain } = nextItem;
        if (moduleId != null) {
            if (outdatedModules.has(moduleId)) {
                continue;
            }
            outdatedModules.add(moduleId);
        }
        // We've arrived at the runtime of the chunk, which means that nothing
        // else above can accept this update.
        if (moduleId === undefined) {
            if (autoAcceptRootModules) {
                return {
                    type: 'accepted',
                    moduleId,
                    outdatedModules,
                    outdatedDependencies
                };
            }
            return {
                type: 'unaccepted',
                dependencyChain
            };
        }
        const module = devModuleCache[moduleId];
        const hotState = moduleHotState.get(module);
        if (// The module is not in the cache. Since this is a "modified" update,
        // it means that the module was never instantiated before.
        !module || hotState.selfAccepted && !hotState.selfInvalidated) {
            continue;
        }
        if (hotState.selfDeclined) {
            return {
                type: 'self-declined',
                dependencyChain,
                moduleId
            };
        }
        if (runtimeModules.has(moduleId)) {
            if (autoAcceptRootModules) {
                continue;
            }
            queue.push({
                moduleId: undefined,
                dependencyChain: [
                    ...dependencyChain,
                    moduleId
                ]
            });
            continue;
        }
        for (const parentId of module.parents){
            const parent = devModuleCache[parentId];
            if (!parent) {
                continue;
            }
            const parentHotState = moduleHotState.get(parent);
            // Check if parent declined this dependency
            if (parentHotState?.declinedDependencies[moduleId]) {
                return {
                    type: 'declined',
                    dependencyChain: [
                        ...dependencyChain,
                        moduleId
                    ],
                    moduleId,
                    parentId
                };
            }
            // Skip if parent is already outdated
            if (outdatedModules.has(parentId)) {
                continue;
            }
            // Check if parent accepts this dependency
            if (parentHotState?.acceptedDependencies[moduleId]) {
                if (!outdatedDependencies.has(parentId)) {
                    outdatedDependencies.set(parentId, new Set());
                }
                outdatedDependencies.get(parentId).add(moduleId);
                continue;
            }
            // Neither accepted nor declined — propagate to parent
            queue.push({
                moduleId: parentId,
                dependencyChain: [
                    ...dependencyChain,
                    moduleId
                ]
            });
        }
        // If no parents and we're at a root module, auto-accept if configured
        if (module.parents.length === 0 && autoAcceptRootModules) {
            continue;
        }
    }
    return {
        type: 'accepted',
        moduleId,
        outdatedModules,
        outdatedDependencies
    };
}
/**
 * Merges source dependency map into target dependency map.
 */ function mergeDependencies(target, source) {
    for (const [parentId, deps] of source){
        const existing = target.get(parentId);
        if (existing) {
            for (const dep of deps){
                existing.add(dep);
            }
        } else {
            target.set(parentId, new Set(deps));
        }
    }
}
/**
 * Computes all modules that need to be invalidated based on which modules changed.
 *
 * @param invalidated - The modules that have been invalidated
 * @param autoAcceptRootModules - If true, root modules auto-accept updates without explicit module.hot.accept()
 */ function computedInvalidatedModules(invalidated, autoAcceptRootModules) {
    const outdatedModules = new Set();
    const outdatedDependencies = new Map();
    for (const moduleId of invalidated){
        const effect = getAffectedModuleEffects(moduleId, autoAcceptRootModules);
        switch(effect.type){
            case 'unaccepted':
                throw new UpdateApplyError(`cannot apply update: unaccepted module. ${formatDependencyChain(effect.dependencyChain)}.`, effect.dependencyChain);
            case 'self-declined':
                throw new UpdateApplyError(`cannot apply update: self-declined module. ${formatDependencyChain(effect.dependencyChain)}.`, effect.dependencyChain);
            case 'declined':
                throw new UpdateApplyError(`cannot apply update: declined dependency. ${formatDependencyChain(effect.dependencyChain)}. Declined by ${effect.parentId}.`, effect.dependencyChain);
            case 'accepted':
                for (const outdatedModuleId of effect.outdatedModules){
                    outdatedModules.add(outdatedModuleId);
                }
                mergeDependencies(outdatedDependencies, effect.outdatedDependencies);
                break;
            default:
                invariant(effect, (effect)=>`Unknown effect type: ${effect?.type}`);
        }
    }
    return {
        outdatedModules,
        outdatedDependencies
    };
}
/**
 * Creates the module.hot API object and its internal state.
 * This provides the HMR API that user code calls (module.hot.accept(), etc.)
 */ function createModuleHot(moduleId, hotData) {
    const hotState = {
        selfAccepted: false,
        selfDeclined: false,
        selfInvalidated: false,
        disposeHandlers: [],
        acceptedDependencies: {},
        acceptedErrorHandlers: {},
        declinedDependencies: {}
    };
    const hot = {
        // TODO(alexkirsz) This is not defined in the HMR API. It was used to
        // decide whether to warn whenever an HMR-disposed module required other
        // modules. We might want to remove it.
        active: true,
        data: hotData ?? {},
        accept: (modules, callback, errorHandler)=>{
            if (modules === undefined) {
                hotState.selfAccepted = true;
            } else if (typeof modules === 'function') {
                hotState.selfAccepted = modules;
            } else if (typeof modules === 'object' && modules !== null) {
                for(let i = 0; i < modules.length; i++){
                    hotState.acceptedDependencies[modules[i]] = callback || function() {};
                    hotState.acceptedErrorHandlers[modules[i]] = errorHandler;
                }
            } else {
                hotState.acceptedDependencies[modules] = callback || function() {};
                hotState.acceptedErrorHandlers[modules] = errorHandler;
            }
        },
        decline: (dep)=>{
            if (dep === undefined) {
                hotState.selfDeclined = true;
            } else if (typeof dep === 'object' && dep !== null) {
                for(let i = 0; i < dep.length; i++){
                    hotState.declinedDependencies[dep[i]] = true;
                }
            } else {
                hotState.declinedDependencies[dep] = true;
            }
        },
        dispose: (callback)=>{
            hotState.disposeHandlers.push(callback);
        },
        addDisposeHandler: (callback)=>{
            hotState.disposeHandlers.push(callback);
        },
        removeDisposeHandler: (callback)=>{
            const idx = hotState.disposeHandlers.indexOf(callback);
            if (idx >= 0) {
                hotState.disposeHandlers.splice(idx, 1);
            }
        },
        invalidate: ()=>{
            hotState.selfInvalidated = true;
            queuedInvalidatedModules.add(moduleId);
        },
        // NOTE(alexkirsz) This is part of the management API, which we don't
        // implement, but the Next.js React Refresh runtime uses this to decide
        // whether to schedule an update.
        status: ()=>'idle',
        // NOTE(alexkirsz) Since we always return "idle" for now, these are no-ops.
        addStatusHandler: (_handler)=>{},
        removeStatusHandler: (_handler)=>{},
        // NOTE(jridgewell) Check returns the list of updated modules, but we don't
        // want the webpack code paths to ever update (the turbopack paths handle
        // this already).
        check: ()=>Promise.resolve(null)
    };
    return {
        hot,
        hotState
    };
}
/**
 * Processes queued invalidated modules and adds them to the outdated modules set.
 * Modules that call module.hot.invalidate() are queued and processed here.
 *
 * @param outdatedModules - The current set of outdated modules
 * @param autoAcceptRootModules - If true, root modules auto-accept updates without explicit module.hot.accept()
 */ function applyInvalidatedModules(outdatedModules, outdatedDependencies, autoAcceptRootModules) {
    if (queuedInvalidatedModules.size > 0) {
        const result = computedInvalidatedModules(queuedInvalidatedModules, autoAcceptRootModules);
        for (const moduleId of result.outdatedModules){
            outdatedModules.add(moduleId);
        }
        mergeDependencies(outdatedDependencies, result.outdatedDependencies);
        queuedInvalidatedModules.clear();
    }
    return {
        outdatedModules,
        outdatedDependencies
    };
}
/**
 * Computes which outdated modules have self-accepted and can be hot reloaded.
 */ function computeOutdatedSelfAcceptedModules(outdatedModules) {
    const outdatedSelfAcceptedModules = [];
    for (const moduleId of outdatedModules){
        const module = devModuleCache[moduleId];
        const hotState = moduleHotState.get(module);
        if (module && hotState?.selfAccepted && !hotState.selfInvalidated) {
            outdatedSelfAcceptedModules.push({
                moduleId,
                errorHandler: hotState.selfAccepted
            });
        }
    }
    return outdatedSelfAcceptedModules;
}
/**
 * Disposes of an instance of a module.
 * Runs hot.dispose handlers and manages persistent hot data.
 *
 * NOTE: mode = "replace" will not remove modules from devModuleCache.
 * This must be done in a separate step afterwards.
 */ function disposeModule(moduleId, mode) {
    const module = devModuleCache[moduleId];
    if (!module) {
        return;
    }
    const hotState = moduleHotState.get(module);
    if (!hotState) {
        return;
    }
    const data = {};
    // Run the `hot.dispose` handler, if any, passing in the persistent
    // `hot.data` object.
    for (const disposeHandler of hotState.disposeHandlers){
        disposeHandler(data);
    }
    // This used to warn in `getOrInstantiateModuleFromParent` when a disposed
    // module is still importing other modules.
    if (module.hot) {
        module.hot.active = false;
    }
    moduleHotState.delete(module);
    // Remove the disposed module from its children's parent list.
    // It will be added back once the module re-instantiates and imports its
    // children again.
    for (const childId of module.children){
        const child = devModuleCache[childId];
        if (!child) {
            continue;
        }
        const idx = child.parents.indexOf(module.id);
        if (idx >= 0) {
            child.parents.splice(idx, 1);
        }
    }
    switch(mode){
        case 'clear':
            delete devModuleCache[module.id];
            moduleHotData.delete(module.id);
            break;
        case 'replace':
            moduleHotData.set(module.id, data);
            break;
        default:
            invariant(mode, (mode)=>`invalid mode: ${mode}`);
    }
}
/**
 * Dispose phase: runs dispose handlers and cleans up outdated/disposed modules.
 * Returns the parent modules of outdated modules for use in the apply phase.
 */ function disposePhase(outdatedModules, disposedModules, outdatedDependencies) {
    for (const moduleId of outdatedModules){
        disposeModule(moduleId, 'replace');
    }
    for (const moduleId of disposedModules){
        disposeModule(moduleId, 'clear');
    }
    // Removing modules from the module cache is a separate step.
    // We also want to keep track of previous parents of the outdated modules.
    const outdatedModuleParents = new Map();
    for (const moduleId of outdatedModules){
        const oldModule = devModuleCache[moduleId];
        outdatedModuleParents.set(moduleId, oldModule?.parents);
        delete devModuleCache[moduleId];
    }
    // Remove outdated dependencies from parent module's children list.
    // When a parent accepts a child's update, the child is re-instantiated
    // but the parent stays alive. We remove the old child reference so it
    // gets re-added when the child re-imports.
    for (const [parentId, deps] of outdatedDependencies){
        const module = devModuleCache[parentId];
        if (module) {
            for (const dep of deps){
                const idx = module.children.indexOf(dep);
                if (idx >= 0) {
                    module.children.splice(idx, 1);
                }
            }
        }
    }
    return {
        outdatedModuleParents
    };
}
/* eslint-disable @typescript-eslint/no-unused-vars */ /**
 * Shared module instantiation logic.
 * This handles the full module instantiation flow for both browser and Node.js.
 * Only React Refresh hooks differ between platforms (passed as callback).
 */ function instantiateModuleShared(moduleId, sourceType, sourceData, moduleFactories, devModuleCache, runtimeModules, createModuleObjectFn, createContextFn, runModuleExecutionHooksFn) {
    // 1. Factory validation (same in both browser and Node.js)
    const id = moduleId;
    const moduleFactory = moduleFactories.get(id);
    if (typeof moduleFactory !== 'function') {
        throw new Error(factoryNotAvailableMessage(moduleId, sourceType, sourceData) + `\nThis is often caused by a stale browser cache, misconfigured Cache-Control headers, or a service worker serving outdated responses.` + `\nTo fix this, make sure your Cache-Control headers allow revalidation of chunks and review your service worker configuration. ` + `As an immediate workaround, try hard-reloading the page, clearing the browser cache, or unregistering any service workers.`);
    }
    // 2. Hot API setup (same in both - works for browser, included for Node.js)
    const hotData = moduleHotData.get(id);
    const { hot, hotState } = createModuleHot(id, hotData);
    // 3. Parent assignment logic (same in both)
    let parents;
    switch(sourceType){
        case SourceType.Runtime:
            runtimeModules.add(id);
            parents = [];
            break;
        case SourceType.Parent:
            parents = [
                sourceData
            ];
            break;
        case SourceType.Update:
            parents = sourceData || [];
            break;
        default:
            throw new Error(`Unknown source type: ${sourceType}`);
    }
    // 4. Module creation (platform creates base module object)
    const module = createModuleObjectFn(id);
    const exports = module.exports;
    module.parents = parents;
    module.children = [];
    module.hot = hot;
    devModuleCache[id] = module;
    moduleHotState.set(module, hotState);
    // 5. Module execution (React Refresh hooks are platform-specific)
    try {
        runModuleExecutionHooksFn(module, (refresh)=>{
            const context = createContextFn(module, exports, refresh);
            moduleFactory.call(exports, context, module, exports);
        });
    } catch (error) {
        module.error = error;
        throw error;
    }
    // 6. ESM interop (same in both)
    if (module.namespaceObject && module.exports !== module.namespaceObject) {
        // in case of a circular dependency: cjs1 -> esm2 -> cjs1
        interopEsm(module.exports, module.namespaceObject);
    }
    return module;
}
/**
 * Analyzes update entries and chunks to determine which modules were added, modified, or deleted.
 * This is pure logic that doesn't depend on the runtime environment.
 */ function computeChangedModules(entries, updates, chunkModulesMap) {
    const chunksAdded = new Map();
    const chunksDeleted = new Map();
    const added = new Map();
    const modified = new Map();
    const deleted = new Set();
    for (const [chunkPath, mergedChunkUpdate] of Object.entries(updates)){
        switch(mergedChunkUpdate.type){
            case 'added':
                {
                    const updateAdded = new Set(mergedChunkUpdate.modules);
                    for (const moduleId of updateAdded){
                        added.set(moduleId, entries[moduleId]);
                    }
                    chunksAdded.set(chunkPath, updateAdded);
                    break;
                }
            case 'deleted':
                {
                    const updateDeleted = chunkModulesMap ? new Set(chunkModulesMap.get(chunkPath)) : new Set();
                    for (const moduleId of updateDeleted){
                        deleted.add(moduleId);
                    }
                    chunksDeleted.set(chunkPath, updateDeleted);
                    break;
                }
            case 'partial':
                {
                    const updateAdded = new Set(mergedChunkUpdate.added);
                    const updateDeleted = new Set(mergedChunkUpdate.deleted);
                    for (const moduleId of updateAdded){
                        added.set(moduleId, entries[moduleId]);
                    }
                    for (const moduleId of updateDeleted){
                        deleted.add(moduleId);
                    }
                    chunksAdded.set(chunkPath, updateAdded);
                    chunksDeleted.set(chunkPath, updateDeleted);
                    break;
                }
            default:
                throw new Error('Unknown merged chunk update type');
        }
    }
    // If a module was added from one chunk and deleted from another in the same update,
    // consider it to be modified, as it means the module was moved from one chunk to another
    // AND has new code in a single update.
    for (const moduleId of added.keys()){
        if (deleted.has(moduleId)) {
            added.delete(moduleId);
            deleted.delete(moduleId);
        }
    }
    for (const [moduleId, entry] of Object.entries(entries)){
        // Modules that haven't been added to any chunk but have new code are considered
        // to be modified.
        // This needs to be under the previous loop, as we need it to get rid of modules
        // that were added and deleted in the same update.
        if (!added.has(moduleId)) {
            modified.set(moduleId, entry);
        }
    }
    return {
        added,
        deleted,
        modified,
        chunksAdded,
        chunksDeleted
    };
}
/**
 * Compiles new module code and walks the dependency tree to find all outdated modules.
 * Uses the evalModuleEntry function to compile code (platform-specific).
 *
 * @param added - Map of added modules
 * @param modified - Map of modified modules
 * @param evalModuleEntry - Function to compile module code
 * @param autoAcceptRootModules - If true, root modules auto-accept updates without explicit module.hot.accept()
 */ function computeOutdatedModules(added, modified, evalModuleEntry, autoAcceptRootModules) {
    const newModuleFactories = new Map();
    // Compile added modules
    for (const [moduleId, entry] of added){
        if (entry != null) {
            newModuleFactories.set(moduleId, evalModuleEntry(entry));
        }
    }
    // Walk dependency tree to find all modules affected by modifications
    const { outdatedModules, outdatedDependencies } = computedInvalidatedModules(modified.keys(), autoAcceptRootModules);
    // Compile modified modules
    for (const [moduleId, entry] of modified){
        newModuleFactories.set(moduleId, evalModuleEntry(entry));
    }
    return {
        outdatedModules,
        outdatedDependencies,
        newModuleFactories
    };
}
/**
 * Updates module factories and re-instantiates self-accepted modules.
 * Uses the instantiateModule function (platform-specific via callback).
 */ function applyPhase(outdatedSelfAcceptedModules, newModuleFactories, outdatedModuleParents, outdatedDependencies, moduleFactories, devModuleCache, instantiateModuleFn, applyModuleFactoryNameFn, reportError) {
    // Update module factories
    for (const [moduleId, factory] of newModuleFactories.entries()){
        applyModuleFactoryNameFn(factory);
        moduleFactories.set(moduleId, factory);
    }
    // TODO(alexkirsz) Run new runtime entries here.
    // Call accept handlers for outdated dependencies.
    // This runs BEFORE re-instantiating self-accepted modules, matching
    // webpack's behavior.
    for (const [parentId, deps] of outdatedDependencies){
        const module = devModuleCache[parentId];
        if (!module) continue;
        const hotState = moduleHotState.get(module);
        if (!hotState) continue;
        // Group deps by callback, deduplicating callbacks that handle multiple deps.
        // Each callback receives only the deps it was registered for.
        const callbackDeps = new Map();
        const callbackErrorHandlers = new Map();
        for (const dep of deps){
            const acceptCallback = hotState.acceptedDependencies[dep];
            if (acceptCallback) {
                let depList = callbackDeps.get(acceptCallback);
                if (!depList) {
                    depList = [];
                    callbackDeps.set(acceptCallback, depList);
                    callbackErrorHandlers.set(acceptCallback, hotState.acceptedErrorHandlers[dep]);
                }
                depList.push(dep);
            }
        }
        for (const [callback, cbDeps] of callbackDeps){
            try {
                callback.call(null, cbDeps);
            } catch (err) {
                const errorHandler = callbackErrorHandlers.get(callback);
                if (typeof errorHandler === 'function') {
                    try {
                        errorHandler(err, {
                            moduleId: parentId,
                            dependencyId: cbDeps[0]
                        });
                    } catch (err2) {
                        reportError(err2);
                        reportError(err);
                    }
                } else {
                    reportError(err);
                }
            }
        }
    }
    // Re-instantiate all outdated self-accepted modules
    for (const { moduleId, errorHandler } of outdatedSelfAcceptedModules){
        try {
            instantiateModuleFn(moduleId, SourceType.Update, outdatedModuleParents.get(moduleId));
        } catch (err) {
            if (typeof errorHandler === 'function') {
                try {
                    errorHandler(err, {
                        moduleId,
                        module: devModuleCache[moduleId]
                    });
                } catch (err2) {
                    reportError(err2);
                    reportError(err);
                }
            } else {
                reportError(err);
            }
        }
    }
}
/**
 * Internal implementation that orchestrates the full HMR update flow:
 * invalidation, disposal, and application of new modules.
 *
 * @param autoAcceptRootModules - If true, root modules auto-accept updates without explicit module.hot.accept()
 */ function applyInternal(outdatedModules, outdatedDependencies, disposedModules, newModuleFactories, moduleFactories, devModuleCache, instantiateModuleFn, applyModuleFactoryNameFn, autoAcceptRootModules) {
    ;
    ({ outdatedModules, outdatedDependencies } = applyInvalidatedModules(outdatedModules, outdatedDependencies, autoAcceptRootModules));
    // Find self-accepted modules to re-instantiate
    const outdatedSelfAcceptedModules = computeOutdatedSelfAcceptedModules(outdatedModules);
    // Run dispose handlers, save hot.data, clear caches
    const { outdatedModuleParents } = disposePhase(outdatedModules, disposedModules, outdatedDependencies);
    let error;
    function reportError(err) {
        if (!error) error = err; // Keep first error
    }
    applyPhase(outdatedSelfAcceptedModules, newModuleFactories, outdatedModuleParents, outdatedDependencies, moduleFactories, devModuleCache, instantiateModuleFn, applyModuleFactoryNameFn, reportError);
    if (error) {
        throw error;
    }
    // Recursively apply any queued invalidations from new module execution
    if (queuedInvalidatedModules.size > 0) {
        applyInternal(new Set(), new Map(), [], new Map(), moduleFactories, devModuleCache, instantiateModuleFn, applyModuleFactoryNameFn, autoAcceptRootModules);
    }
}
/**
 * Main entry point for applying an ECMAScript merged update.
 * This is called by both browser and Node.js runtimes with platform-specific callbacks.
 *
 * @param options.autoAcceptRootModules - If true, root modules auto-accept updates without explicit
 *                                   module.hot.accept(). Used for server-side HMR where pages
 *                                   auto-accept at the top level.
 */ function applyEcmascriptMergedUpdateShared(options) {
    const { added, modified, disposedModules, evalModuleEntry, instantiateModule, applyModuleFactoryName, moduleFactories, devModuleCache, autoAcceptRootModules } = options;
    const { outdatedModules, outdatedDependencies, newModuleFactories } = computeOutdatedModules(added, modified, evalModuleEntry, autoAcceptRootModules);
    applyInternal(outdatedModules, outdatedDependencies, disposedModules, newModuleFactories, moduleFactories, devModuleCache, instantiateModule, applyModuleFactoryName, autoAcceptRootModules);
}
/* eslint-disable @typescript-eslint/no-unused-vars */ /// <reference path="./runtime-base.ts" />
/// <reference path="../../shared/runtime/dev-extensions.ts" />
/// <reference path="../../shared/runtime/hmr-runtime.ts" />
/**
 * Development Node.js runtime.
 * Uses HotModule and shared HMR logic for hot module replacement support.
 */ // Cast the module cache to HotModule for development mode
// (hmr-runtime.ts declares devModuleCache as `let` variable expecting assignment)
// This is safe because HotModule extends Module
devModuleCache = moduleCache;
// this is read in runtime-utils.ts so it creates a module with direction for hmr
createModuleWithDirectionFlag = true;
if (!globalThis.__turbopack_runtime_modules__) {
    globalThis.__turbopack_runtime_modules__ = new Set();
}
runtimeModules = globalThis.__turbopack_runtime_modules__;
const nodeDevContextPrototype = Context.prototype;
nodeDevContextPrototype.q = exportUrl;
nodeDevContextPrototype.M = moduleFactories;
nodeDevContextPrototype.c = devModuleCache;
nodeDevContextPrototype.R = resolvePathFromModule;
nodeDevContextPrototype.b = createWorker;
nodeDevContextPrototype.C = clearChunkCache;
/**
 * Instantiates a module in development mode using shared HMR logic.
 */ function instantiateModule(id, sourceType, sourceData) {
    // Node.js: creates base module object (hot API added by shared code)
    const createModuleObjectFn = (moduleId)=>{
        return createModuleWithDirection(moduleId);
    };
    // Node.js: creates Context (no refresh parameter)
    const createContext = (module1, exports, _refresh)=>{
        return new Context(module1, exports);
    };
    // Node.js: no hooks wrapper, just execute directly
    const runWithHooks = (module1, exec)=>{
        exec(undefined); // no refresh context
    };
    // Use shared instantiation logic (includes hot API setup)
    const newModule = instantiateModuleShared(id, sourceType, sourceData, moduleFactories, devModuleCache, runtimeModules, createModuleObjectFn, createContext, runWithHooks);
    newModule.loaded = true;
    return newModule;
}
/**
 * Instantiates a runtime module in development mode.
 */ function instantiateRuntimeModule(chunkPath, moduleId) {
    return instantiateModule(moduleId, SourceType.Runtime, chunkPath);
}
/**
 * Retrieves a module from the cache, or instantiate it as a runtime module if it is not cached.
 */ // @ts-ignore TypeScript doesn't separate this module space from the browser runtime
function getOrInstantiateRuntimeModule(chunkPath, moduleId) {
    const module1 = devModuleCache[moduleId];
    if (module1) {
        if (module1.error) {
            throw module1.error;
        }
        return module1;
    }
    return instantiateRuntimeModule(chunkPath, moduleId);
}
/**
 * Retrieves a module from the cache, or instantiate it if it is not cached.
 * Also tracks parent-child relationships for HMR dependency tracking.
 */ // @ts-ignore
function getOrInstantiateModuleFromParent(id, sourceModule) {
    // Track parent-child relationship
    trackModuleImport(sourceModule, id, devModuleCache[id]);
    const module1 = devModuleCache[id];
    if (module1) {
        if (module1.error) {
            throw module1.error;
        }
        return module1;
    }
    const newModule = instantiateModule(id, SourceType.Parent, sourceModule.id);
    // Track again after instantiation to ensure the relationship is recorded
    trackModuleImport(sourceModule, id, newModule);
    return newModule;
}
module.exports = (sourcePath)=>({
        m: (id)=>getOrInstantiateRuntimeModule(sourcePath, id),
        c: (chunkData)=>loadRuntimeChunk(sourcePath, chunkData)
    });
/// <reference path="../../shared/runtime/dev-protocol.d.ts" />
/// <reference path="../../shared/runtime/hmr-runtime.ts" />
/* eslint-disable @typescript-eslint/no-unused-vars */ /**
 * Appends the module code with //# sourceURL and //# sourceMappingURL so
 * that Node.js can resolve stack frames from `eval`ed server HMR modules back to
 * their original source files. Mirrors the browser's _eval in dev-backend-dom.ts.
 */ function inlineSourcemaps(entry) {
    const [chunkPath, moduleId] = entry.url.split('?', 2);
    const absolutePath = path.resolve(RUNTIME_ROOT, chunkPath);
    const fileHref = url.pathToFileURL(absolutePath).href;
    const sourceURL = moduleId ? `${fileHref}?${moduleId}` : fileHref;
    let code = entry.code + '\n\n//# sourceURL=' + sourceURL;
    if (entry.map) {
        code += '\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,' + Buffer.from(entry.map).toString('base64');
    }
    return code;
}
let serverHmrUpdateHandler = null;
function initializeServerHmr(moduleFactories, devModuleCache) {
    if (serverHmrUpdateHandler != null) {
        throw new Error('[Server HMR] Server HMR client is already initialized');
    }
    // Register the update handler for the server runtime
    serverHmrUpdateHandler = (msg)=>{
        handleNodejsUpdate(msg, moduleFactories, devModuleCache);
    };
}
/**
 * Emits an HMR message to the registered update handler.
 * Node uses a simpler listener pattern than the browser's websocket connection.
 *
 * Note: This is only called via __turbopack_server_hmr_apply__ which ensures
 * the handler is initialized first via ensureHmrClientInitialized().
 */ function emitMessage(msg) {
    if (serverHmrUpdateHandler == null) {
        console.warn('[Server HMR] No update handler registered to receive message:', msg);
        return false;
    }
    try {
        serverHmrUpdateHandler(msg.data);
        return true;
    } catch (err) {
        console.error('[Server HMR] Listener error:', err);
        return false;
    }
}
/**
 * Handles server message updates and applies them to the Node.js runtime.
 * Uses shared HMR update logic from hmr-runtime.ts.
 */ function handleNodejsUpdate(msg, moduleFactories, devModuleCache) {
    if (msg.type !== 'partial') {
        return;
    }
    const instruction = msg.instruction;
    if (instruction.type !== 'EcmascriptMergedUpdate') {
        return;
    }
    try {
        const { entries = {}, chunks = {} } = instruction;
        const evalModuleEntry = (entry)=>{
            // eslint-disable-next-line no-eval
            return (0, eval)(entry.map ? inlineSourcemaps(entry) : entry.code);
        };
        const { added, modified } = computeChangedModules(entries, chunks, undefined // no chunkModulesMap for Node.js
        );
        // Use shared HMR update implementation
        applyEcmascriptMergedUpdateShared({
            added,
            modified,
            disposedModules: [],
            evalModuleEntry,
            instantiateModule,
            applyModuleFactoryName: ()=>{},
            moduleFactories,
            devModuleCache,
            autoAcceptRootModules: true
        });
    } catch (e) {
        console.error('[Server HMR] Update failed, full reload needed:', e);
        throw e;
    }
}
/// <reference path="../../shared/runtime/dev-protocol.d.ts" />
/// <reference path="./hmr-client.ts" />
/**
 * Note: hmr-runtime.ts is embedded before this file, so its functions
 * (initializeServerHmr, emitMessage) are available in the same scope.
 */ // Initialize server HMR client (connects to shared HMR infrastructure)
let hmrClientInitialized = false;
function ensureHmrClientInitialized() {
    if (hmrClientInitialized) return;
    hmrClientInitialized = true;
    // initializeServerHmr is from hmr-client.ts (embedded before this file)
    // moduleFactories is from dev-runtime.ts
    // devModuleCache is the HotModule-typed cache from dev-runtime.ts
    initializeServerHmr(moduleFactories, devModuleCache);
}
function __turbopack_server_hmr_apply__(update) {
    try {
        ensureHmrClientInitialized();
        // emitMessage returns false if any listener failed to apply the update
        return emitMessage({
            type: 'turbopack-message',
            data: update
        });
    } catch (err) {
        console.error('[Server HMR] Failed to apply update:', err);
        return false;
    }
}
const handlers = globalThis.__turbopack_server_hmr_handlers__ ?? new Map();
const chunkPrefix = path.relative(RUNTIME_ROOT, path.dirname(__filename));
if (handlers.size === 0) {
    // First registration in this generation: install the routing dispatcher.
    globalThis.__turbopack_server_hmr_apply__ = (update)=>{
        const registry = globalThis.__turbopack_server_hmr_handlers__ ?? new Map();
        const updateChunkPaths = Object.keys(update.instruction?.chunks ?? {});
        const toCall = [];
        if (updateChunkPaths.length === 0) {
            for (const entry of registry.values())toCall.push(entry);
        } else {
            const seen = new Set();
            for (const chunkPath of updateChunkPaths){
                const dir = path.dirname(chunkPath);
                for (const [key, entry] of registry){
                    if (dir === entry.chunkPrefix && !seen.has(key)) {
                        seen.add(key);
                        toCall.push(entry);
                    }
                }
            }
        }
        let applied = false;
        for (const { handler } of toCall){
            try {
                if (handler(update)) applied = true;
            } catch (err) {
                console.error('[Server HMR] Handler error:', err);
            }
        }
        return applied;
    };
}
globalThis.__turbopack_server_hmr_handlers__ = handlers;
handlers.set(__filename, {
    handler: __turbopack_server_hmr_apply__,
    chunkPrefix
});


//# sourceMappingURL=%5Bturbopack%5D_runtime.js.map