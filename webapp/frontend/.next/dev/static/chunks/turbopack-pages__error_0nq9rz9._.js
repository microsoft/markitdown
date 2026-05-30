(globalThis["TURBOPACK"] || (globalThis["TURBOPACK"] = [])).push([
    typeof document === "object" ? document.currentScript : undefined,
    {"otherChunks":["static/chunks/08c5_next_dist_compiled_10o-w6b._.js","static/chunks/08c5_next_dist_shared_lib_0iea6re._.js","static/chunks/08c5_next_dist_client_0yl.0ti._.js","static/chunks/08c5_next_dist_0hskx5n._.js","static/chunks/[next]_entry_page-loader_ts_0mgynyz._.js","static/chunks/0a8t_react-dom_07.400g._.js","static/chunks/node_modules__pnpm_0mcpr3x._.js","static/chunks/[root-of-the-server]__01mw43t._.js"],"runtimeModuleIds":["[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/@next/react-refresh-utils/dist/runtime.js [client] (ecmascript)","[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/next-dev-turbopack.js [client] (ecmascript)","[hmr-entry]/hmr-entry.js { ENTRY => \"[project]/pages/_error\" }"]}
]);
(() => {
if (!Array.isArray(globalThis["TURBOPACK"])) {
    return;
}

const CHUNK_BASE_PATH = "/_next/";
const RELATIVE_ROOT_PATH = "/ROOT";
const RUNTIME_PUBLIC_PATH = "/_next/";
const ASSET_SUFFIX = getAssetSuffixFromScriptSrc();
const WORKER_FORWARDED_GLOBALS = ["NEXT_DEPLOYMENT_ID","NEXT_CLIENT_ASSET_SUFFIX"];
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
/**
 * This file contains runtime types and functions that are shared between all
 * Turbopack *browser* ECMAScript runtimes.
 *
 * It will be appended to the runtime code of each runtime right after the
 * shared runtime utils.
 */ /* eslint-disable @typescript-eslint/no-unused-vars */ /// <reference path="../base/globals.d.ts" />
/// <reference path="../../../shared/runtime/runtime-utils.ts" />
// Used in WebWorkers to tell the runtime about the chunk suffix
const browserContextPrototype = Context.prototype;
const moduleFactories = new Map();
contextPrototype.M = moduleFactories;
const availableModules = new Map();
const availableModuleChunks = new Map();
function loadChunk(chunkData) {
    return loadChunkInternal(SourceType.Parent, this.m.id, chunkData);
}
browserContextPrototype.l = loadChunk;
function loadInitialChunk(chunkPath, chunkData) {
    return loadChunkInternal(SourceType.Runtime, chunkPath, chunkData);
}
async function loadChunkInternal(sourceType, sourceData, chunkData) {
    if (typeof chunkData === 'string') {
        return loadChunkPath(sourceType, sourceData, chunkData);
    }
    const includedList = chunkData.included || [];
    const modulesPromises = includedList.map((included)=>{
        if (moduleFactories.has(included)) return true;
        return availableModules.get(included);
    });
    if (modulesPromises.length > 0 && modulesPromises.every((p)=>p)) {
        // When all included items are already loaded or loading, we can skip loading ourselves
        await Promise.all(modulesPromises);
        return;
    }
    const includedModuleChunksList = chunkData.moduleChunks || [];
    const moduleChunksPromises = includedModuleChunksList.map((included)=>{
        // TODO(alexkirsz) Do we need this check?
        // if (moduleFactories[included]) return true;
        return availableModuleChunks.get(included);
    }).filter((p)=>p);
    let promise;
    if (moduleChunksPromises.length > 0) {
        // Some module chunks are already loaded or loading.
        if (moduleChunksPromises.length === includedModuleChunksList.length) {
            // When all included module chunks are already loaded or loading, we can skip loading ourselves
            await Promise.all(moduleChunksPromises);
            return;
        }
        const moduleChunksToLoad = new Set();
        for (const moduleChunk of includedModuleChunksList){
            if (!availableModuleChunks.has(moduleChunk)) {
                moduleChunksToLoad.add(moduleChunk);
            }
        }
        for (const moduleChunkToLoad of moduleChunksToLoad){
            const promise = loadChunkPath(sourceType, sourceData, moduleChunkToLoad);
            availableModuleChunks.set(moduleChunkToLoad, promise);
            moduleChunksPromises.push(promise);
        }
        promise = Promise.all(moduleChunksPromises);
    } else {
        promise = loadChunkPath(sourceType, sourceData, chunkData.path);
        // Mark all included module chunks as loading if they are not already loaded or loading.
        for (const includedModuleChunk of includedModuleChunksList){
            if (!availableModuleChunks.has(includedModuleChunk)) {
                availableModuleChunks.set(includedModuleChunk, promise);
            }
        }
    }
    for (const included of includedList){
        if (!availableModules.has(included)) {
            // It might be better to race old and new promises, but it's rare that the new promise will be faster than a request started earlier.
            // In production it's even more rare, because the chunk optimization tries to deduplicate modules anyway.
            availableModules.set(included, promise);
        }
    }
    await promise;
}
const loadedChunk = Promise.resolve(undefined);
const instrumentedBackendLoadChunks = new WeakMap();
// Do not make this async. React relies on referential equality of the returned Promise.
function loadChunkByUrl(chunkUrl) {
    return loadChunkByUrlInternal(SourceType.Parent, this.m.id, chunkUrl);
}
browserContextPrototype.L = loadChunkByUrl;
// Do not make this async. React relies on referential equality of the returned Promise.
function loadChunkByUrlInternal(sourceType, sourceData, chunkUrl) {
    const thenable = BACKEND.loadChunkCached(sourceType, chunkUrl);
    let entry = instrumentedBackendLoadChunks.get(thenable);
    if (entry === undefined) {
        const resolve = instrumentedBackendLoadChunks.set.bind(instrumentedBackendLoadChunks, thenable, loadedChunk);
        entry = thenable.then(resolve).catch((cause)=>{
            let loadReason;
            switch(sourceType){
                case SourceType.Runtime:
                    loadReason = `as a runtime dependency of chunk ${sourceData}`;
                    break;
                case SourceType.Parent:
                    loadReason = `from module ${sourceData}`;
                    break;
                case SourceType.Update:
                    loadReason = 'from an HMR update';
                    break;
                default:
                    invariant(sourceType, (sourceType)=>`Unknown source type: ${sourceType}`);
            }
            let error = new Error(`Failed to load chunk ${chunkUrl} ${loadReason}${cause ? `: ${cause}` : ''}`, cause ? {
                cause
            } : undefined);
            error.name = 'ChunkLoadError';
            throw error;
        });
        instrumentedBackendLoadChunks.set(thenable, entry);
    }
    return entry;
}
// Do not make this async. React relies on referential equality of the returned Promise.
function loadChunkPath(sourceType, sourceData, chunkPath) {
    const url = getChunkRelativeUrl(chunkPath);
    return loadChunkByUrlInternal(sourceType, sourceData, url);
}
/**
 * Returns an absolute url to an asset.
 */ function resolvePathFromModule(moduleId) {
    const exported = this.r(moduleId);
    return exported?.default ?? exported;
}
browserContextPrototype.R = resolvePathFromModule;
/**
 * no-op for browser
 * @param modulePath
 */ function resolveAbsolutePath(modulePath) {
    return `/ROOT/${modulePath ?? ''}`;
}
browserContextPrototype.P = resolveAbsolutePath;
/**
 * Exports a URL with the static suffix appended.
 */ function exportUrl(url, id) {
    exportValue.call(this, `${url}${ASSET_SUFFIX}`, id);
}
browserContextPrototype.q = exportUrl;
/**
 * Creates a worker by instantiating the given WorkerConstructor with the
 * appropriate URL and options.
 *
 * The entrypoint is a pre-compiled worker runtime file. The params configure
 * which module chunks to load and which module to run as the entry point.
 *
 * The params are a JSON array of the following structure:
 * `[TURBOPACK_NEXT_CHUNK_URLS, ASSET_SUFFIX, ...WORKER_FORWARDED_GLOBALS values]`
 *
 * @param WorkerConstructor The Worker or SharedWorker constructor
 * @param entrypoint URL path to the worker entrypoint chunk
 * @param moduleChunks list of module chunk paths to load
 * @param workerOptions options to pass to the Worker constructor (optional)
 */ function createWorker(WorkerConstructor, entrypoint, moduleChunks, workerOptions) {
    const isSharedWorker = WorkerConstructor.name === 'SharedWorker';
    const chunkUrls = moduleChunks.map((chunk)=>getChunkRelativeUrl(chunk)).reverse();
    const params = [
        chunkUrls,
        ASSET_SUFFIX
    ];
    for (const globalName of WORKER_FORWARDED_GLOBALS){
        params.push(globalThis[globalName]);
    }
    const url = new URL(getChunkRelativeUrl(entrypoint), location.origin);
    const paramsJson = JSON.stringify(params);
    if (isSharedWorker) {
        url.searchParams.set('params', paramsJson);
    } else {
        url.hash = '#params=' + encodeURIComponent(paramsJson);
    }
    // Remove type: "module" from options since our worker entrypoint is not a module
    const options = workerOptions ? {
        ...workerOptions,
        type: undefined
    } : undefined;
    return new WorkerConstructor(url, options);
}
browserContextPrototype.b = createWorker;
/**
 * Instantiates a runtime module.
 */ function instantiateRuntimeModule(moduleId, chunkPath) {
    return instantiateModule(moduleId, SourceType.Runtime, chunkPath);
}
/**
 * Returns the URL relative to the origin where a chunk can be fetched from.
 */ function getChunkRelativeUrl(chunkPath) {
    return `${CHUNK_BASE_PATH}${chunkPath.split('/').map((p)=>encodeURIComponent(p)).join('/')}${ASSET_SUFFIX}`;
}
function getPathFromScript(chunkScript) {
    if (typeof chunkScript === 'string') {
        return chunkScript;
    }
    const chunkUrl = chunkScript.src;
    const src = decodeURIComponent(chunkUrl.replace(/[?#].*$/, ''));
    const path = src.startsWith(CHUNK_BASE_PATH) ? src.slice(CHUNK_BASE_PATH.length) : src;
    return path;
}
/**
 * Return the ChunkUrl from a ChunkScript.
 */ function getUrlFromScript(chunk) {
    if (typeof chunk === 'string') {
        return getChunkRelativeUrl(chunk);
    } else {
        // This is already exactly what we want
        return chunk.src;
    }
}
/**
 * Determine the chunk to register. Note that this function has side-effects!
 */ function getChunkFromRegistration(chunk) {
    if (typeof chunk === 'string') {
        return chunk;
    } else if (!chunk) {
        if (typeof TURBOPACK_NEXT_CHUNK_URLS !== 'undefined') {
            return {
                src: TURBOPACK_NEXT_CHUNK_URLS.pop()
            };
        } else {
            throw new Error('chunk path empty but not in a worker');
        }
    } else {
        return {
            src: chunk.getAttribute('src')
        };
    }
}
const regexJsUrl = /\.js(?:\?[^#]*)?(?:#.*)?$/;
/**
 * Checks if a given path/URL ends with .js, optionally followed by ?query or #fragment.
 */ function isJs(chunkUrlOrPath) {
    return regexJsUrl.test(chunkUrlOrPath);
}
const regexCssUrl = /\.css(?:\?[^#]*)?(?:#.*)?$/;
/**
 * Checks if a given path/URL ends with .css, optionally followed by ?query or #fragment.
 */ function isCss(chunkUrl) {
    return regexCssUrl.test(chunkUrl);
}
function loadWebAssembly(chunkPath, edgeModule, importsObj) {
    return BACKEND.loadWebAssembly(SourceType.Parent, this.m.id, chunkPath, edgeModule, importsObj);
}
contextPrototype.w = loadWebAssembly;
function loadWebAssemblyModule(chunkPath, edgeModule) {
    return BACKEND.loadWebAssemblyModule(SourceType.Parent, this.m.id, chunkPath, edgeModule);
}
contextPrototype.u = loadWebAssemblyModule;
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
/// <reference path="../../../shared/runtime/dev-globals.d.ts" />
/// <reference path="../../../shared/runtime/dev-protocol.d.ts" />
const devContextPrototype = Context.prototype;
/**
 * This file contains runtime types and functions that are shared between all
 * Turbopack *development* ECMAScript runtimes.
 *
 * It will be appended to the runtime code of each runtime right after the
 * shared runtime utils.
 */ /* eslint-disable @typescript-eslint/no-unused-vars */ // Assign browser's module cache and runtime modules to shared HMR state
devModuleCache = Object.create(null);
devContextPrototype.c = devModuleCache;
runtimeModules = new Set();
// Set flag to indicate we use ModuleWithDirection
createModuleWithDirectionFlag = true;
/**
 * Map from module ID to the chunks that contain this module.
 *
 * In HMR, we need to keep track of which modules are contained in which so
 * chunks. This is so we don't eagerly dispose of a module when it is removed
 * from chunk A, but still exists in chunk B.
 */ const moduleChunksMap = new Map();
/**
 * Map from a chunk path to all modules it contains.
 */ const chunkModulesMap = new Map();
/**
 * Chunk lists that contain a runtime. When these chunk lists receive an update
 * that can't be reconciled with the current state of the page, we need to
 * reload the runtime entirely.
 */ const runtimeChunkLists = new Set();
/**
 * Map from a chunk list to the chunk paths it contains.
 */ const chunkListChunksMap = new Map();
/**
 * Map from a chunk path to the chunk lists it belongs to.
 */ const chunkChunkListsMap = new Map();
/**
 * Gets or instantiates a runtime module.
 */ // @ts-ignore
function getOrInstantiateRuntimeModule(chunkPath, moduleId) {
    const module = devModuleCache[moduleId];
    if (module) {
        if (module.error) {
            throw module.error;
        }
        return module;
    }
    // @ts-ignore
    return instantiateModule(moduleId, SourceType.Runtime, chunkPath);
}
/**
 * Retrieves a module from the cache, or instantiate it if it is not cached.
 */ // @ts-ignore Defined in `runtime-utils.ts`
const getOrInstantiateModuleFromParent = (id, sourceModule)=>{
    if (!sourceModule.hot.active) {
        console.warn(`Unexpected import of module ${id} from module ${sourceModule.id}, which was deleted by an HMR update`);
    }
    const module = devModuleCache[id];
    if (sourceModule.children.indexOf(id) === -1) {
        sourceModule.children.push(id);
    }
    if (module) {
        if (module.error) {
            throw module.error;
        }
        if (module.parents.indexOf(sourceModule.id) === -1) {
            module.parents.push(sourceModule.id);
        }
        return module;
    }
    return instantiateModule(id, SourceType.Parent, sourceModule.id);
};
function DevContext(module, exports, refresh) {
    Context.call(this, module, exports);
    this.k = refresh;
}
DevContext.prototype = Context.prototype;
function instantiateModule(moduleId, sourceType, sourceData) {
    // Browser: creates base HotModule object (hot API added by shared code)
    const createModuleObjectFn = (id)=>{
        return createModuleObject(id);
    };
    // Browser: creates DevContext with refresh
    const createContext = (module, exports, refresh)=>{
        return new DevContext(module, exports, refresh);
    };
    // Use shared instantiation logic (includes hot API setup)
    return instantiateModuleShared(moduleId, sourceType, sourceData, moduleFactories, devModuleCache, runtimeModules, createModuleObjectFn, createContext, runModuleExecutionHooks);
}
const DUMMY_REFRESH_CONTEXT = {
    register: (_type, _id)=>{},
    signature: ()=>(_type)=>{},
    registerExports: (_module, _helpers)=>{}
};
/**
 * NOTE(alexkirsz) Webpack has a "module execution" interception hook that
 * Next.js' React Refresh runtime hooks into to add module context to the
 * refresh registry.
 */ function runModuleExecutionHooks(module, executeModule) {
    if (typeof globalThis.$RefreshInterceptModuleExecution$ === 'function') {
        const cleanupReactRefreshIntercept = globalThis.$RefreshInterceptModuleExecution$(module.id);
        try {
            executeModule({
                register: globalThis.$RefreshReg$,
                signature: globalThis.$RefreshSig$,
                registerExports: registerExportsAndSetupBoundaryForReactRefresh
            });
        } finally{
            // Always cleanup the intercept, even if module execution failed.
            cleanupReactRefreshIntercept();
        }
    } else {
        // If the react refresh hooks are not installed we need to bind dummy functions.
        // This is expected when running in a Web Worker.  It is also common in some of
        // our test environments.
        executeModule(DUMMY_REFRESH_CONTEXT);
    }
}
/**
 * This is adapted from https://github.com/vercel/next.js/blob/3466862d9dc9c8bb3131712134d38757b918d1c0/packages/react-refresh-utils/internal/ReactRefreshModule.runtime.ts
 */ function registerExportsAndSetupBoundaryForReactRefresh(module, helpers) {
    const currentExports = module.exports;
    const prevExports = module.hot.data.prevExports ?? null;
    helpers.registerExportsForReactRefresh(currentExports, module.id);
    // A module can be accepted automatically based on its exports, e.g. when
    // it is a Refresh Boundary.
    if (helpers.isReactRefreshBoundary(currentExports)) {
        // Save the previous exports on update, so we can compare the boundary
        // signatures.
        module.hot.dispose((data)=>{
            data.prevExports = currentExports;
        });
        // Unconditionally accept an update to this module, we'll check if it's
        // still a Refresh Boundary later.
        module.hot.accept();
        // This field is set when the previous version of this module was a
        // Refresh Boundary, letting us know we need to check for invalidation or
        // enqueue an update.
        if (prevExports !== null) {
            // A boundary can become ineligible if its exports are incompatible
            // with the previous exports.
            //
            // For example, if you add/remove/change exports, we'll want to
            // re-execute the importing modules, and force those components to
            // re-render. Similarly, if you convert a class component to a
            // function, we want to invalidate the boundary.
            if (helpers.shouldInvalidateReactRefreshBoundary(helpers.getRefreshBoundarySignature(prevExports), helpers.getRefreshBoundarySignature(currentExports))) {
                module.hot.invalidate();
            } else {
                helpers.scheduleUpdate();
            }
        }
    } else {
        // Since we just executed the code for the module, it's possible that the
        // new exports made it ineligible for being a boundary.
        // We only care about the case when we were _previously_ a boundary,
        // because we already accepted this update (accidental side effect).
        const isNoLongerABoundary = prevExports !== null;
        if (isNoLongerABoundary) {
            module.hot.invalidate();
        }
    }
}
/**
 * Adds, deletes, and moves modules between chunks. This must happen before the
 * dispose phase as it needs to know which modules were removed from all chunks,
 * which we can only compute *after* taking care of added and moved modules.
 */ function updateChunksPhase(chunksAddedModules, chunksDeletedModules) {
    for (const [chunkPath, addedModuleIds] of chunksAddedModules){
        for (const moduleId of addedModuleIds){
            addModuleToChunk(moduleId, chunkPath);
        }
    }
    const disposedModules = new Set();
    for (const [chunkPath, addedModuleIds] of chunksDeletedModules){
        for (const moduleId of addedModuleIds){
            if (removeModuleFromChunk(moduleId, chunkPath)) {
                disposedModules.add(moduleId);
            }
        }
    }
    return {
        disposedModules
    };
}
function applyUpdate(update) {
    switch(update.type){
        case 'ChunkListUpdate':
            applyChunkListUpdate(update);
            break;
        default:
            invariant(update, (update)=>`Unknown update type: ${update.type}`);
    }
}
function applyChunkListUpdate(update) {
    if (update.merged != null) {
        for (const merged of update.merged){
            switch(merged.type){
                case 'EcmascriptMergedUpdate':
                    applyEcmascriptMergedUpdate(merged);
                    break;
                default:
                    invariant(merged, (merged)=>`Unknown merged type: ${merged.type}`);
            }
        }
    }
    if (update.chunks != null) {
        for (const [chunkPath, chunkUpdate] of Object.entries(update.chunks)){
            const chunkUrl = getChunkRelativeUrl(chunkPath);
            switch(chunkUpdate.type){
                case 'added':
                    BACKEND.loadChunkCached(SourceType.Update, chunkUrl);
                    break;
                case 'total':
                    DEV_BACKEND.reloadChunk?.(chunkUrl);
                    break;
                case 'deleted':
                    DEV_BACKEND.unloadChunk?.(chunkUrl);
                    break;
                case 'partial':
                    invariant(chunkUpdate.instruction, (instruction)=>`Unknown partial instruction: ${JSON.stringify(instruction)}.`);
                    break;
                default:
                    invariant(chunkUpdate, (chunkUpdate)=>`Unknown chunk update type: ${chunkUpdate.type}`);
            }
        }
    }
}
function applyEcmascriptMergedUpdate(update) {
    // Browser-specific chunk management phase
    const { entries = {}, chunks = {} } = update;
    const { added, modified, chunksAdded, chunksDeleted } = computeChangedModules(entries, chunks, chunkModulesMap);
    const { disposedModules } = updateChunksPhase(chunksAdded, chunksDeleted);
    // Use shared HMR update implementation
    applyEcmascriptMergedUpdateShared({
        added,
        modified,
        disposedModules,
        evalModuleEntry: _eval,
        instantiateModule,
        applyModuleFactoryName,
        moduleFactories,
        devModuleCache,
        autoAcceptRootModules: false
    });
}
function handleApply(chunkListPath, update) {
    switch(update.type){
        case 'partial':
            {
                // This indicates that the update is can be applied to the current state of the application.
                applyUpdate(update.instruction);
                break;
            }
        case 'restart':
            {
                // This indicates that there is no way to apply the update to the
                // current state of the application, and that the application must be
                // restarted.
                DEV_BACKEND.restart();
                break;
            }
        case 'notFound':
            {
                // This indicates that the chunk list no longer exists: either the dynamic import which created it was removed,
                // or the page itself was deleted.
                // If it is a dynamic import, we simply discard all modules that the chunk has exclusive access to.
                // If it is a runtime chunk list, we restart the application.
                if (runtimeChunkLists.has(chunkListPath)) {
                    DEV_BACKEND.restart();
                } else {
                    disposeChunkList(chunkListPath);
                }
                break;
            }
        default:
            throw new Error(`Unknown update type: ${update.type}`);
    }
}
/**
 * Removes a module from a chunk.
 * Returns `true` if there are no remaining chunks including this module.
 */ function removeModuleFromChunk(moduleId, chunkPath) {
    const moduleChunks = moduleChunksMap.get(moduleId);
    moduleChunks.delete(chunkPath);
    const chunkModules = chunkModulesMap.get(chunkPath);
    chunkModules.delete(moduleId);
    const noRemainingModules = chunkModules.size === 0;
    if (noRemainingModules) {
        chunkModulesMap.delete(chunkPath);
    }
    const noRemainingChunks = moduleChunks.size === 0;
    if (noRemainingChunks) {
        moduleChunksMap.delete(moduleId);
    }
    return noRemainingChunks;
}
/**
 * Disposes of a chunk list and its corresponding exclusive chunks.
 */ function disposeChunkList(chunkListPath) {
    const chunkPaths = chunkListChunksMap.get(chunkListPath);
    if (chunkPaths == null) {
        return false;
    }
    chunkListChunksMap.delete(chunkListPath);
    for (const chunkPath of chunkPaths){
        const chunkChunkLists = chunkChunkListsMap.get(chunkPath);
        chunkChunkLists.delete(chunkListPath);
        if (chunkChunkLists.size === 0) {
            chunkChunkListsMap.delete(chunkPath);
            disposeChunk(chunkPath);
        }
    }
    // We must also dispose of the chunk list's chunk itself to ensure it may
    // be reloaded properly in the future.
    const chunkListUrl = getChunkRelativeUrl(chunkListPath);
    DEV_BACKEND.unloadChunk?.(chunkListUrl);
    return true;
}
/**
 * Disposes of a chunk and its corresponding exclusive modules.
 *
 * @returns Whether the chunk was disposed of.
 */ function disposeChunk(chunkPath) {
    const chunkUrl = getChunkRelativeUrl(chunkPath);
    // This should happen whether the chunk has any modules in it or not.
    // For instance, CSS chunks have no modules in them, but they still need to be unloaded.
    DEV_BACKEND.unloadChunk?.(chunkUrl);
    const chunkModules = chunkModulesMap.get(chunkPath);
    if (chunkModules == null) {
        return false;
    }
    chunkModules.delete(chunkPath);
    for (const moduleId of chunkModules){
        const moduleChunks = moduleChunksMap.get(moduleId);
        moduleChunks.delete(chunkPath);
        const noRemainingChunks = moduleChunks.size === 0;
        if (noRemainingChunks) {
            moduleChunksMap.delete(moduleId);
            disposeModule(moduleId, 'clear');
            availableModules.delete(moduleId);
        }
    }
    return true;
}
/**
 * Adds a module to a chunk.
 */ function addModuleToChunk(moduleId, chunkPath) {
    let moduleChunks = moduleChunksMap.get(moduleId);
    if (!moduleChunks) {
        moduleChunks = new Set([
            chunkPath
        ]);
        moduleChunksMap.set(moduleId, moduleChunks);
    } else {
        moduleChunks.add(chunkPath);
    }
    let chunkModules = chunkModulesMap.get(chunkPath);
    if (!chunkModules) {
        chunkModules = new Set([
            moduleId
        ]);
        chunkModulesMap.set(chunkPath, chunkModules);
    } else {
        chunkModules.add(moduleId);
    }
}
/**
 * Marks a chunk list as a runtime chunk list. There can be more than one
 * runtime chunk list. For instance, integration tests can have multiple chunk
 * groups loaded at runtime, each with its own chunk list.
 */ function markChunkListAsRuntime(chunkListPath) {
    runtimeChunkLists.add(chunkListPath);
}
function registerChunk(registration) {
    const chunk = getChunkFromRegistration(registration[0]);
    let runtimeParams;
    // When bootstrapping we are passed a single runtimeParams object so we can distinguish purely based on length
    if (registration.length === 2) {
        runtimeParams = registration[1];
    } else {
        let chunkPath = getPathFromScript(chunk);
        runtimeParams = undefined;
        installCompressedModuleFactories(registration, /* offset= */ 1, moduleFactories, (id)=>addModuleToChunk(id, chunkPath));
    }
    return BACKEND.registerChunk(chunk, runtimeParams);
}
/**
 * Subscribes to chunk list updates from the update server and applies them.
 */ function registerChunkList(chunkList) {
    const chunkListScript = getChunkFromRegistration(chunkList.script);
    const chunkListPath = getPathFromScript(chunkListScript);
    // The "chunk" is also registered to finish the loading in the backend
    BACKEND.registerChunk(chunkListPath);
    globalThis.TURBOPACK_CHUNK_UPDATE_LISTENERS.push([
        chunkListPath,
        handleApply.bind(null, chunkListPath)
    ]);
    // Adding chunks to chunk lists and vice versa.
    const chunkPaths = new Set(chunkList.chunks.map(getChunkPath));
    chunkListChunksMap.set(chunkListPath, chunkPaths);
    for (const chunkPath of chunkPaths){
        let chunkChunkLists = chunkChunkListsMap.get(chunkPath);
        if (!chunkChunkLists) {
            chunkChunkLists = new Set([
                chunkListPath
            ]);
            chunkChunkListsMap.set(chunkPath, chunkChunkLists);
        } else {
            chunkChunkLists.add(chunkListPath);
        }
    }
    if (chunkList.source === 'entry') {
        markChunkListAsRuntime(chunkListPath);
    }
}
globalThis.TURBOPACK_CHUNK_UPDATE_LISTENERS ??= [];
/**
 * This file contains the runtime code specific to the Turbopack ECMAScript DOM runtime.
 *
 * It will be appended to the base runtime code.
 */ /* eslint-disable @typescript-eslint/no-unused-vars */ /// <reference path="../../../browser/runtime/base/runtime-base.ts" />
/// <reference path="../../../shared/runtime/runtime-types.d.ts" />
function getAssetSuffixFromScriptSrc() {
    // TURBOPACK_ASSET_SUFFIX is set in web workers
    if (self.TURBOPACK_ASSET_SUFFIX != null) return self.TURBOPACK_ASSET_SUFFIX;
    const src = document?.currentScript?.getAttribute?.('src') ?? '';
    const qi = src.indexOf('?');
    return qi >= 0 ? src.slice(qi) : '';
}
let BACKEND;
/**
 * Maps chunk paths to the corresponding resolver.
 */ const chunkResolvers = new Map();
(()=>{
    BACKEND = {
        async registerChunk (chunk, params) {
            let chunkPath = getPathFromScript(chunk);
            let chunkUrl = getUrlFromScript(chunk);
            const resolver = getOrCreateResolver(chunkUrl);
            resolver.resolve();
            if (params == null) {
                return;
            }
            for (const otherChunkData of params.otherChunks){
                const otherChunkPath = getChunkPath(otherChunkData);
                const otherChunkUrl = getChunkRelativeUrl(otherChunkPath);
                // Chunk might have started loading, so we want to avoid triggering another load.
                getOrCreateResolver(otherChunkUrl);
            }
            // This waits for chunks to be loaded, but also marks included items as available.
            await Promise.all(params.otherChunks.map((otherChunkData)=>loadInitialChunk(chunkPath, otherChunkData)));
            if (params.runtimeModuleIds.length > 0) {
                for (const moduleId of params.runtimeModuleIds){
                    getOrInstantiateRuntimeModule(chunkPath, moduleId);
                }
            }
        },
        /**
     * Loads the given chunk, and returns a promise that resolves once the chunk
     * has been loaded.
     */ loadChunkCached (sourceType, chunkUrl) {
            return doLoadChunk(sourceType, chunkUrl);
        },
        async loadWebAssembly (_sourceType, _sourceData, wasmChunkPath, _edgeModule, importsObj) {
            const req = fetchWebAssembly(wasmChunkPath);
            const { instance } = await WebAssembly.instantiateStreaming(req, importsObj);
            return instance.exports;
        },
        async loadWebAssemblyModule (_sourceType, _sourceData, wasmChunkPath, _edgeModule) {
            const req = fetchWebAssembly(wasmChunkPath);
            return await WebAssembly.compileStreaming(req);
        }
    };
    function getOrCreateResolver(chunkUrl) {
        let resolver = chunkResolvers.get(chunkUrl);
        if (!resolver) {
            let resolve;
            let reject;
            const promise = new Promise((innerResolve, innerReject)=>{
                resolve = innerResolve;
                reject = innerReject;
            });
            resolver = {
                resolved: false,
                loadingStarted: false,
                promise,
                resolve: ()=>{
                    resolver.resolved = true;
                    resolve();
                },
                reject: reject
            };
            chunkResolvers.set(chunkUrl, resolver);
        }
        return resolver;
    }
    /**
   * Loads the given chunk, and returns a promise that resolves once the chunk
   * has been loaded.
   */ function doLoadChunk(sourceType, chunkUrl) {
        const resolver = getOrCreateResolver(chunkUrl);
        if (resolver.loadingStarted) {
            return resolver.promise;
        }
        if (sourceType === SourceType.Runtime) {
            // We don't need to load chunks references from runtime code, as they're already
            // present in the DOM.
            resolver.loadingStarted = true;
            if (isCss(chunkUrl)) {
                // CSS chunks do not register themselves, and as such must be marked as
                // loaded instantly.
                resolver.resolve();
            }
            // We need to wait for JS chunks to register themselves within `registerChunk`
            // before we can start instantiating runtime modules, hence the absence of
            // `resolver.resolve()` in this branch.
            return resolver.promise;
        }
        if (typeof importScripts === 'function') {
            // We're in a web worker
            if (isCss(chunkUrl)) {
            // ignore
            } else if (isJs(chunkUrl)) {
                self.TURBOPACK_NEXT_CHUNK_URLS.push(chunkUrl);
                importScripts(chunkUrl);
            } else {
                throw new Error(`can't infer type of chunk from URL ${chunkUrl} in worker`);
            }
        } else {
            // TODO(PACK-2140): remove this once all filenames are guaranteed to be escaped.
            const decodedChunkUrl = decodeURI(chunkUrl);
            if (isCss(chunkUrl)) {
                const previousLinks = document.querySelectorAll(`link[rel=stylesheet][href="${chunkUrl}"],link[rel=stylesheet][href^="${chunkUrl}?"],link[rel=stylesheet][href="${decodedChunkUrl}"],link[rel=stylesheet][href^="${decodedChunkUrl}?"]`);
                if (previousLinks.length > 0) {
                    // CSS chunks do not register themselves, and as such must be marked as
                    // loaded instantly.
                    resolver.resolve();
                } else {
                    const link = document.createElement('link');
                    link.rel = 'stylesheet';
                    link.href = chunkUrl;
                    link.onerror = ()=>{
                        resolver.reject();
                    };
                    link.onload = ()=>{
                        // CSS chunks do not register themselves, and as such must be marked as
                        // loaded instantly.
                        resolver.resolve();
                    };
                    // Append to the `head` for webpack compatibility.
                    document.head.appendChild(link);
                }
            } else if (isJs(chunkUrl)) {
                const previousScripts = document.querySelectorAll(`script[src="${chunkUrl}"],script[src^="${chunkUrl}?"],script[src="${decodedChunkUrl}"],script[src^="${decodedChunkUrl}?"]`);
                if (previousScripts.length > 0) {
                    // There is this edge where the script already failed loading, but we
                    // can't detect that. The Promise will never resolve in this case.
                    for (const script of Array.from(previousScripts)){
                        script.addEventListener('error', ()=>{
                            resolver.reject();
                        });
                    }
                } else {
                    const script = document.createElement('script');
                    script.src = chunkUrl;
                    // We'll only mark the chunk as loaded once the script has been executed,
                    // which happens in `registerChunk`. Hence the absence of `resolve()` in
                    // this branch.
                    script.onerror = ()=>{
                        resolver.reject();
                    };
                    // Append to the `head` for webpack compatibility.
                    document.head.appendChild(script);
                }
            } else {
                throw new Error(`can't infer type of chunk from URL ${chunkUrl}`);
            }
        }
        resolver.loadingStarted = true;
        return resolver.promise;
    }
    function fetchWebAssembly(wasmChunkPath) {
        return fetch(getChunkRelativeUrl(wasmChunkPath));
    }
})();
/**
 * This file contains the runtime code specific to the Turbopack development
 * ECMAScript DOM runtime.
 *
 * It will be appended to the base development runtime code.
 */ /* eslint-disable @typescript-eslint/no-unused-vars */ /// <reference path="../base/runtime-base.ts" />
/// <reference path="../base/dev-base.ts" />
/// <reference path="./runtime-backend-dom.ts" />
/// <reference path="../../../shared/require-type.d.ts" />
let DEV_BACKEND;
(()=>{
    DEV_BACKEND = {
        unloadChunk (chunkUrl) {
            deleteResolver(chunkUrl);
            // Strip query string so we match links regardless of cache-busting
            // params (e.g. ?ts=) that may differ between HMR updates.
            const baseChunkUrl = chunkUrl.split('?')[0];
            // TODO(PACK-2140): remove this once all filenames are guaranteed to be escaped.
            const decodedBaseChunkUrl = decodeURI(baseChunkUrl);
            if (isCss(chunkUrl)) {
                const links = document.querySelectorAll(`link[href="${baseChunkUrl}"],link[href^="${baseChunkUrl}?"],link[href="${decodedBaseChunkUrl}"],link[href^="${decodedBaseChunkUrl}?"]`);
                for (const link of Array.from(links)){
                    link.remove();
                }
            } else if (isJs(chunkUrl)) {
                // Unloading a JS chunk would have no effect, as it lives in the JS
                // runtime once evaluated.
                // However, we still want to remove the script tag from the DOM to keep
                // the HTML somewhat consistent from the user's perspective.
                const scripts = document.querySelectorAll(`script[src="${baseChunkUrl}"],script[src^="${baseChunkUrl}?"],script[src="${decodedBaseChunkUrl}"],script[src^="${decodedBaseChunkUrl}?"]`);
                for (const script of Array.from(scripts)){
                    script.remove();
                }
            } else {
                throw new Error(`can't infer type of chunk from URL ${chunkUrl}`);
            }
        },
        reloadChunk (chunkUrl) {
            return new Promise((resolve, reject)=>{
                if (!isCss(chunkUrl)) {
                    reject(new Error('The DOM backend can only reload CSS chunks'));
                    return;
                }
                // Strip query string so we match links regardless of cache-busting
                // params (e.g. ?ts=) that may differ between HMR updates.
                const baseChunkUrl = chunkUrl.split('?')[0];
                const decodedBaseChunkUrl = decodeURI(baseChunkUrl);
                const previousLinks = document.querySelectorAll(`link[rel=stylesheet][href="${baseChunkUrl}"],link[rel=stylesheet][href^="${baseChunkUrl}?"],link[rel=stylesheet][href="${decodedBaseChunkUrl}"],link[rel=stylesheet][href^="${decodedBaseChunkUrl}?"]`);
                if (previousLinks.length === 0) {
                    reject(new Error(`No link element found for chunk ${chunkUrl}`));
                    return;
                }
                const link = document.createElement('link');
                link.rel = 'stylesheet';
                if (navigator.userAgent.includes('Firefox') || navigator.userAgent.includes('Safari') && !navigator.userAgent.includes('Chrome') && !navigator.userAgent.includes('Chromium')) {
                    // Firefox won't reload CSS files that were previously loaded on the
                    // current page: https://bugzilla.mozilla.org/show_bug.cgi?id=1037506
                    //
                    // Safari serves cached CSS when a <link rel=preload> exists for the
                    // same URL: https://bugs.webkit.org/show_bug.cgi?id=187726
                    //
                    // Replace or add a fresh `ts` cache-busting param without
                    // discarding other query parameters that may already be present.
                    const url = new URL(chunkUrl, location.origin);
                    url.searchParams.set('ts', String(Date.now()));
                    // Reduced timer precision in some browers could lead to an update getting dropped
                    // in firefox if it happens fast enough (in firefox precision is sometimes 100ms!).
                    // So trust that the server is only updating us when it is important and use a
                    // random number to bust the cache.
                    url.searchParams.set('_next_rand', String(Math.random()));
                    link.href = url.pathname + url.search;
                } else {
                    link.href = chunkUrl;
                }
                link.onerror = ()=>{
                    reject();
                };
                link.onload = ()=>{
                    // First load the new CSS, then remove the old ones. This prevents visible
                    // flickering that would happen in-between removing the previous CSS and
                    // loading the new one.
                    for (const previousLink of Array.from(previousLinks))previousLink.remove();
                    // CSS chunks do not register themselves, and as such must be marked as
                    // loaded instantly.
                    resolve();
                };
                // Make sure to insert the new CSS right after the previous one, so that
                // its precedence is higher.
                previousLinks[0].parentElement.insertBefore(link, previousLinks[0].nextSibling);
            });
        },
        restart: ()=>self.location.reload()
    };
    function deleteResolver(chunkUrl) {
        chunkResolvers.delete(chunkUrl);
    }
})();
function _eval({ code, url, map }) {
    code += `\n\n//# sourceURL=${encodeURI(location.origin + CHUNK_BASE_PATH + url + ASSET_SUFFIX)}`;
    if (map) {
        code += `\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,${btoa(// btoa doesn't handle nonlatin characters, so escape them as \x sequences
        // See https://stackoverflow.com/a/26603875
        unescape(encodeURIComponent(map)))}`;
    }
    // eslint-disable-next-line no-eval
    return eval(code);
}
const chunksToRegister = globalThis["TURBOPACK"];
globalThis["TURBOPACK"] = { push: registerChunk };
chunksToRegister.forEach(registerChunk);
const chunkListsToRegister = globalThis["TURBOPACK_CHUNK_LISTS"] || [];
globalThis["TURBOPACK_CHUNK_LISTS"] = { push: registerChunkList };
chunkListsToRegister.forEach(registerChunkList);
})();


//# sourceMappingURL=pages__error_0nq9rz9._.js.map