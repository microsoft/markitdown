(globalThis["TURBOPACK"] || (globalThis["TURBOPACK"] = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/process/browser.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {

(function() {
    var e = {
        229: function(e) {
            var t = e.exports = {};
            var r;
            var n;
            function defaultSetTimout() {
                throw new Error("setTimeout has not been defined");
            }
            function defaultClearTimeout() {
                throw new Error("clearTimeout has not been defined");
            }
            (function() {
                try {
                    if (typeof setTimeout === "function") {
                        r = setTimeout;
                    } else {
                        r = defaultSetTimout;
                    }
                } catch (e) {
                    r = defaultSetTimout;
                }
                try {
                    if (typeof clearTimeout === "function") {
                        n = clearTimeout;
                    } else {
                        n = defaultClearTimeout;
                    }
                } catch (e) {
                    n = defaultClearTimeout;
                }
            })();
            function runTimeout(e) {
                if (r === setTimeout) {
                    return setTimeout(e, 0);
                }
                if ((r === defaultSetTimout || !r) && setTimeout) {
                    r = setTimeout;
                    return setTimeout(e, 0);
                }
                try {
                    return r(e, 0);
                } catch (t) {
                    try {
                        return r.call(null, e, 0);
                    } catch (t) {
                        return r.call(this, e, 0);
                    }
                }
            }
            function runClearTimeout(e) {
                if (n === clearTimeout) {
                    return clearTimeout(e);
                }
                if ((n === defaultClearTimeout || !n) && clearTimeout) {
                    n = clearTimeout;
                    return clearTimeout(e);
                }
                try {
                    return n(e);
                } catch (t) {
                    try {
                        return n.call(null, e);
                    } catch (t) {
                        return n.call(this, e);
                    }
                }
            }
            var i = [];
            var o = false;
            var u;
            var a = -1;
            function cleanUpNextTick() {
                if (!o || !u) {
                    return;
                }
                o = false;
                if (u.length) {
                    i = u.concat(i);
                } else {
                    a = -1;
                }
                if (i.length) {
                    drainQueue();
                }
            }
            function drainQueue() {
                if (o) {
                    return;
                }
                var e = runTimeout(cleanUpNextTick);
                o = true;
                var t = i.length;
                while(t){
                    u = i;
                    i = [];
                    while(++a < t){
                        if (u) {
                            u[a].run();
                        }
                    }
                    a = -1;
                    t = i.length;
                }
                u = null;
                o = false;
                runClearTimeout(e);
            }
            t.nextTick = function(e) {
                var t = new Array(arguments.length - 1);
                if (arguments.length > 1) {
                    for(var r = 1; r < arguments.length; r++){
                        t[r - 1] = arguments[r];
                    }
                }
                i.push(new Item(e, t));
                if (i.length === 1 && !o) {
                    runTimeout(drainQueue);
                }
            };
            function Item(e, t) {
                this.fun = e;
                this.array = t;
            }
            Item.prototype.run = function() {
                this.fun.apply(null, this.array);
            };
            t.title = "browser";
            t.browser = true;
            t.env = {};
            t.argv = [];
            t.version = "";
            t.versions = {};
            function noop() {}
            t.on = noop;
            t.addListener = noop;
            t.once = noop;
            t.off = noop;
            t.removeListener = noop;
            t.removeAllListeners = noop;
            t.emit = noop;
            t.prependListener = noop;
            t.prependOnceListener = noop;
            t.listeners = function(e) {
                return [];
            };
            t.binding = function(e) {
                throw new Error("process.binding is not supported");
            };
            t.cwd = function() {
                return "/";
            };
            t.chdir = function(e) {
                throw new Error("process.chdir is not supported");
            };
            t.umask = function() {
                return 0;
            };
        }
    };
    var t = {};
    function __nccwpck_require__(r) {
        var n = t[r];
        if (n !== undefined) {
            return n.exports;
        }
        var i = t[r] = {
            exports: {}
        };
        var o = true;
        try {
            e[r](i, i.exports, __nccwpck_require__);
            o = false;
        } finally{
            if (o) delete t[r];
        }
        return i.exports;
    }
    if (typeof __nccwpck_require__ !== "undefined") __nccwpck_require__.ab = ("TURBOPACK compile-time value", "/ROOT/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/process") + "/";
    var r = __nccwpck_require__(229);
    module.exports = r;
})();
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-refresh/cjs/react-refresh-runtime.development.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
/**
 * @license React
 * react-refresh-runtime.development.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */ 'use strict';
if ("TURBOPACK compile-time truthy", 1) {
    (function() {
        'use strict';
        // ATTENTION
        var REACT_FORWARD_REF_TYPE = Symbol.for('react.forward_ref');
        var REACT_MEMO_TYPE = Symbol.for('react.memo');
        var PossiblyWeakMap = typeof WeakMap === 'function' ? WeakMap : Map; // We never remove these associations.
        // It's OK to reference families, but use WeakMap/Set for types.
        var allFamiliesByID = new Map();
        var allFamiliesByType = new PossiblyWeakMap();
        var allSignaturesByType = new PossiblyWeakMap(); // This WeakMap is read by React, so we only put families
        // that have actually been edited here. This keeps checks fast.
        // $FlowIssue
        var updatedFamiliesByType = new PossiblyWeakMap(); // This is cleared on every performReactRefresh() call.
        // It is an array of [Family, NextType] tuples.
        var pendingUpdates = []; // This is injected by the renderer via DevTools global hook.
        var helpersByRendererID = new Map();
        var helpersByRoot = new Map(); // We keep track of mounted roots so we can schedule updates.
        var mountedRoots = new Set(); // If a root captures an error, we remember it so we can retry on edit.
        var failedRoots = new Set(); // In environments that support WeakMap, we also remember the last element for every root.
        // It needs to be weak because we do this even for roots that failed to mount.
        // If there is no WeakMap, we won't attempt to do retrying.
        // $FlowIssue
        var rootElements = typeof WeakMap === 'function' ? new WeakMap() : null;
        var isPerformingRefresh = false;
        function computeFullKey(signature) {
            if (signature.fullKey !== null) {
                return signature.fullKey;
            }
            var fullKey = signature.ownKey;
            var hooks;
            try {
                hooks = signature.getCustomHooks();
            } catch (err) {
                // This can happen in an edge case, e.g. if expression like Foo.useSomething
                // depends on Foo which is lazily initialized during rendering.
                // In that case just assume we'll have to remount.
                signature.forceReset = true;
                signature.fullKey = fullKey;
                return fullKey;
            }
            for(var i = 0; i < hooks.length; i++){
                var hook = hooks[i];
                if (typeof hook !== 'function') {
                    // Something's wrong. Assume we need to remount.
                    signature.forceReset = true;
                    signature.fullKey = fullKey;
                    return fullKey;
                }
                var nestedHookSignature = allSignaturesByType.get(hook);
                if (nestedHookSignature === undefined) {
                    continue;
                }
                var nestedHookKey = computeFullKey(nestedHookSignature);
                if (nestedHookSignature.forceReset) {
                    signature.forceReset = true;
                }
                fullKey += '\n---\n' + nestedHookKey;
            }
            signature.fullKey = fullKey;
            return fullKey;
        }
        function haveEqualSignatures(prevType, nextType) {
            var prevSignature = allSignaturesByType.get(prevType);
            var nextSignature = allSignaturesByType.get(nextType);
            if (prevSignature === undefined && nextSignature === undefined) {
                return true;
            }
            if (prevSignature === undefined || nextSignature === undefined) {
                return false;
            }
            if (computeFullKey(prevSignature) !== computeFullKey(nextSignature)) {
                return false;
            }
            if (nextSignature.forceReset) {
                return false;
            }
            return true;
        }
        function isReactClass(type) {
            return type.prototype && type.prototype.isReactComponent;
        }
        function canPreserveStateBetween(prevType, nextType) {
            if (isReactClass(prevType) || isReactClass(nextType)) {
                return false;
            }
            if (haveEqualSignatures(prevType, nextType)) {
                return true;
            }
            return false;
        }
        function resolveFamily(type) {
            // Only check updated types to keep lookups fast.
            return updatedFamiliesByType.get(type);
        } // If we didn't care about IE11, we could use new Map/Set(iterable).
        function cloneMap(map) {
            var clone = new Map();
            map.forEach(function(value, key) {
                clone.set(key, value);
            });
            return clone;
        }
        function cloneSet(set) {
            var clone = new Set();
            set.forEach(function(value) {
                clone.add(value);
            });
            return clone;
        } // This is a safety mechanism to protect against rogue getters and Proxies.
        function getProperty(object, property) {
            try {
                return object[property];
            } catch (err) {
                // Intentionally ignore.
                return undefined;
            }
        }
        function performReactRefresh() {
            if (pendingUpdates.length === 0) {
                return null;
            }
            if (isPerformingRefresh) {
                return null;
            }
            isPerformingRefresh = true;
            try {
                var staleFamilies = new Set();
                var updatedFamilies = new Set();
                var updates = pendingUpdates;
                pendingUpdates = [];
                updates.forEach(function(_ref) {
                    var family = _ref[0], nextType = _ref[1];
                    // Now that we got a real edit, we can create associations
                    // that will be read by the React reconciler.
                    var prevType = family.current;
                    updatedFamiliesByType.set(prevType, family);
                    updatedFamiliesByType.set(nextType, family);
                    family.current = nextType; // Determine whether this should be a re-render or a re-mount.
                    if (canPreserveStateBetween(prevType, nextType)) {
                        updatedFamilies.add(family);
                    } else {
                        staleFamilies.add(family);
                    }
                }); // TODO: rename these fields to something more meaningful.
                var update = {
                    updatedFamilies: updatedFamilies,
                    // Families that will re-render preserving state
                    staleFamilies: staleFamilies // Families that will be remounted
                };
                helpersByRendererID.forEach(function(helpers) {
                    // Even if there are no roots, set the handler on first update.
                    // This ensures that if *new* roots are mounted, they'll use the resolve handler.
                    helpers.setRefreshHandler(resolveFamily);
                });
                var didError = false;
                var firstError = null; // We snapshot maps and sets that are mutated during commits.
                // If we don't do this, there is a risk they will be mutated while
                // we iterate over them. For example, trying to recover a failed root
                // may cause another root to be added to the failed list -- an infinite loop.
                var failedRootsSnapshot = cloneSet(failedRoots);
                var mountedRootsSnapshot = cloneSet(mountedRoots);
                var helpersByRootSnapshot = cloneMap(helpersByRoot);
                failedRootsSnapshot.forEach(function(root) {
                    var helpers = helpersByRootSnapshot.get(root);
                    if (helpers === undefined) {
                        throw new Error('Could not find helpers for a root. This is a bug in React Refresh.');
                    }
                    if (!failedRoots.has(root)) {}
                    if (rootElements === null) {
                        return;
                    }
                    if (!rootElements.has(root)) {
                        return;
                    }
                    var element = rootElements.get(root);
                    try {
                        helpers.scheduleRoot(root, element);
                    } catch (err) {
                        if (!didError) {
                            didError = true;
                            firstError = err;
                        } // Keep trying other roots.
                    }
                });
                mountedRootsSnapshot.forEach(function(root) {
                    var helpers = helpersByRootSnapshot.get(root);
                    if (helpers === undefined) {
                        throw new Error('Could not find helpers for a root. This is a bug in React Refresh.');
                    }
                    if (!mountedRoots.has(root)) {}
                    try {
                        helpers.scheduleRefresh(root, update);
                    } catch (err) {
                        if (!didError) {
                            didError = true;
                            firstError = err;
                        } // Keep trying other roots.
                    }
                });
                if (didError) {
                    throw firstError;
                }
                return update;
            } finally{
                isPerformingRefresh = false;
            }
        }
        function register(type, id) {
            {
                if (type === null) {
                    return;
                }
                if (typeof type !== 'function' && typeof type !== 'object') {
                    return;
                } // This can happen in an edge case, e.g. if we register
                // return value of a HOC but it returns a cached component.
                // Ignore anything but the first registration for each type.
                if (allFamiliesByType.has(type)) {
                    return;
                } // Create family or remember to update it.
                // None of this bookkeeping affects reconciliation
                // until the first performReactRefresh() call above.
                var family = allFamiliesByID.get(id);
                if (family === undefined) {
                    family = {
                        current: type
                    };
                    allFamiliesByID.set(id, family);
                } else {
                    pendingUpdates.push([
                        family,
                        type
                    ]);
                }
                allFamiliesByType.set(type, family); // Visit inner types because we might not have registered them.
                if (typeof type === 'object' && type !== null) {
                    switch(getProperty(type, '$$typeof')){
                        case REACT_FORWARD_REF_TYPE:
                            register(type.render, id + '$render');
                            break;
                        case REACT_MEMO_TYPE:
                            register(type.type, id + '$type');
                            break;
                    }
                }
            }
        }
        function setSignature(type, key) {
            var forceReset = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
            var getCustomHooks = arguments.length > 3 ? arguments[3] : undefined;
            {
                if (!allSignaturesByType.has(type)) {
                    allSignaturesByType.set(type, {
                        forceReset: forceReset,
                        ownKey: key,
                        fullKey: null,
                        getCustomHooks: getCustomHooks || function() {
                            return [];
                        }
                    });
                } // Visit inner types because we might not have signed them.
                if (typeof type === 'object' && type !== null) {
                    switch(getProperty(type, '$$typeof')){
                        case REACT_FORWARD_REF_TYPE:
                            setSignature(type.render, key, forceReset, getCustomHooks);
                            break;
                        case REACT_MEMO_TYPE:
                            setSignature(type.type, key, forceReset, getCustomHooks);
                            break;
                    }
                }
            }
        } // This is lazily called during first render for a type.
        // It captures Hook list at that time so inline requires don't break comparisons.
        function collectCustomHooksForSignature(type) {
            {
                var signature = allSignaturesByType.get(type);
                if (signature !== undefined) {
                    computeFullKey(signature);
                }
            }
        }
        function getFamilyByID(id) {
            {
                return allFamiliesByID.get(id);
            }
        }
        function getFamilyByType(type) {
            {
                return allFamiliesByType.get(type);
            }
        }
        function findAffectedHostInstances(families) {
            {
                var affectedInstances = new Set();
                mountedRoots.forEach(function(root) {
                    var helpers = helpersByRoot.get(root);
                    if (helpers === undefined) {
                        throw new Error('Could not find helpers for a root. This is a bug in React Refresh.');
                    }
                    var instancesForRoot = helpers.findHostInstancesForRefresh(root, families);
                    instancesForRoot.forEach(function(inst) {
                        affectedInstances.add(inst);
                    });
                });
                return affectedInstances;
            }
        }
        function injectIntoGlobalHook(globalObject) {
            {
                // For React Native, the global hook will be set up by require('react-devtools-core').
                // That code will run before us. So we need to monkeypatch functions on existing hook.
                // For React Web, the global hook will be set up by the extension.
                // This will also run before us.
                var hook = globalObject.__REACT_DEVTOOLS_GLOBAL_HOOK__;
                if (hook === undefined) {
                    // However, if there is no DevTools extension, we'll need to set up the global hook ourselves.
                    // Note that in this case it's important that renderer code runs *after* this method call.
                    // Otherwise, the renderer will think that there is no global hook, and won't do the injection.
                    var nextID = 0;
                    globalObject.__REACT_DEVTOOLS_GLOBAL_HOOK__ = hook = {
                        renderers: new Map(),
                        supportsFiber: true,
                        inject: function(injected) {
                            return nextID++;
                        },
                        onScheduleFiberRoot: function(id, root, children) {},
                        onCommitFiberRoot: function(id, root, maybePriorityLevel, didError) {},
                        onCommitFiberUnmount: function() {}
                    };
                }
                if (hook.isDisabled) {
                    // This isn't a real property on the hook, but it can be set to opt out
                    // of DevTools integration and associated warnings and logs.
                    // Using console['warn'] to evade Babel and ESLint
                    console['warn']('Something has shimmed the React DevTools global hook (__REACT_DEVTOOLS_GLOBAL_HOOK__). ' + 'Fast Refresh is not compatible with this shim and will be disabled.');
                    return;
                } // Here, we just want to get a reference to scheduleRefresh.
                var oldInject = hook.inject;
                hook.inject = function(injected) {
                    var id = oldInject.apply(this, arguments);
                    if (typeof injected.scheduleRefresh === 'function' && typeof injected.setRefreshHandler === 'function') {
                        // This version supports React Refresh.
                        helpersByRendererID.set(id, injected);
                    }
                    return id;
                }; // Do the same for any already injected roots.
                // This is useful if ReactDOM has already been initialized.
                // https://github.com/facebook/react/issues/17626
                hook.renderers.forEach(function(injected, id) {
                    if (typeof injected.scheduleRefresh === 'function' && typeof injected.setRefreshHandler === 'function') {
                        // This version supports React Refresh.
                        helpersByRendererID.set(id, injected);
                    }
                }); // We also want to track currently mounted roots.
                var oldOnCommitFiberRoot = hook.onCommitFiberRoot;
                var oldOnScheduleFiberRoot = hook.onScheduleFiberRoot || function() {};
                hook.onScheduleFiberRoot = function(id, root, children) {
                    if (!isPerformingRefresh) {
                        // If it was intentionally scheduled, don't attempt to restore.
                        // This includes intentionally scheduled unmounts.
                        failedRoots.delete(root);
                        if (rootElements !== null) {
                            rootElements.set(root, children);
                        }
                    }
                    return oldOnScheduleFiberRoot.apply(this, arguments);
                };
                hook.onCommitFiberRoot = function(id, root, maybePriorityLevel, didError) {
                    var helpers = helpersByRendererID.get(id);
                    if (helpers !== undefined) {
                        helpersByRoot.set(root, helpers);
                        var current = root.current;
                        var alternate = current.alternate; // We need to determine whether this root has just (un)mounted.
                        // This logic is copy-pasted from similar logic in the DevTools backend.
                        // If this breaks with some refactoring, you'll want to update DevTools too.
                        if (alternate !== null) {
                            var wasMounted = alternate.memoizedState != null && alternate.memoizedState.element != null && mountedRoots.has(root);
                            var isMounted = current.memoizedState != null && current.memoizedState.element != null;
                            if (!wasMounted && isMounted) {
                                // Mount a new root.
                                mountedRoots.add(root);
                                failedRoots.delete(root);
                            } else if (wasMounted && isMounted) ;
                            else if (wasMounted && !isMounted) {
                                // Unmount an existing root.
                                mountedRoots.delete(root);
                                if (didError) {
                                    // We'll remount it on future edits.
                                    failedRoots.add(root);
                                } else {
                                    helpersByRoot.delete(root);
                                }
                            } else if (!wasMounted && !isMounted) {
                                if (didError) {
                                    // We'll remount it on future edits.
                                    failedRoots.add(root);
                                }
                            }
                        } else {
                            // Mount a new root.
                            mountedRoots.add(root);
                        }
                    } // Always call the decorated DevTools hook.
                    return oldOnCommitFiberRoot.apply(this, arguments);
                };
            }
        }
        function hasUnrecoverableErrors() {
            // TODO: delete this after removing dependency in RN.
            return false;
        } // Exposed for testing.
        function _getMountedRootCount() {
            {
                return mountedRoots.size;
            }
        } // This is a wrapper over more primitive functions for setting signature.
        // Signatures let us decide whether the Hook order has changed on refresh.
        //
        // This function is intended to be used as a transform target, e.g.:
        // var _s = createSignatureFunctionForTransform()
        //
        // function Hello() {
        //   const [foo, setFoo] = useState(0);
        //   const value = useCustomHook();
        //   _s(); /* Call without arguments triggers collecting the custom Hook list.
        //          * This doesn't happen during the module evaluation because we
        //          * don't want to change the module order with inline requires.
        //          * Next calls are noops. */
        //   return <h1>Hi</h1>;
        // }
        //
        // /* Call with arguments attaches the signature to the type: */
        // _s(
        //   Hello,
        //   'useState{[foo, setFoo]}(0)',
        //   () => [useCustomHook], /* Lazy to avoid triggering inline requires */
        // );
        function createSignatureFunctionForTransform() {
            {
                var savedType;
                var hasCustomHooks;
                var didCollectHooks = false;
                return function(type, key, forceReset, getCustomHooks) {
                    if (typeof key === 'string') {
                        // We're in the initial phase that associates signatures
                        // with the functions. Note this may be called multiple times
                        // in HOC chains like _s(hoc1(_s(hoc2(_s(actualFunction))))).
                        if (!savedType) {
                            // We're in the innermost call, so this is the actual type.
                            savedType = type;
                            hasCustomHooks = typeof getCustomHooks === 'function';
                        } // Set the signature for all types (even wrappers!) in case
                        // they have no signatures of their own. This is to prevent
                        // problems like https://github.com/facebook/react/issues/20417.
                        if (type != null && (typeof type === 'function' || typeof type === 'object')) {
                            setSignature(type, key, forceReset, getCustomHooks);
                        }
                        return type;
                    } else {
                        // We're in the _s() call without arguments, which means
                        // this is the time to collect custom Hook signatures.
                        // Only do this once. This path is hot and runs *inside* every render!
                        if (!didCollectHooks && hasCustomHooks) {
                            didCollectHooks = true;
                            collectCustomHooksForSignature(savedType);
                        }
                    }
                };
            }
        }
        function isLikelyComponentType(type) {
            {
                switch(typeof type){
                    case 'function':
                        {
                            // First, deal with classes.
                            if (type.prototype != null) {
                                if (type.prototype.isReactComponent) {
                                    // React class.
                                    return true;
                                }
                                var ownNames = Object.getOwnPropertyNames(type.prototype);
                                if (ownNames.length > 1 || ownNames[0] !== 'constructor') {
                                    // This looks like a class.
                                    return false;
                                } // eslint-disable-next-line no-proto
                                if (type.prototype.__proto__ !== Object.prototype) {
                                    // It has a superclass.
                                    return false;
                                } // Pass through.
                            // This looks like a regular function with empty prototype.
                            } // For plain functions and arrows, use name as a heuristic.
                            var name = type.name || type.displayName;
                            return typeof name === 'string' && /^[A-Z]/.test(name);
                        }
                    case 'object':
                        {
                            if (type != null) {
                                switch(getProperty(type, '$$typeof')){
                                    case REACT_FORWARD_REF_TYPE:
                                    case REACT_MEMO_TYPE:
                                        // Definitely React components.
                                        return true;
                                    default:
                                        return false;
                                }
                            }
                            return false;
                        }
                    default:
                        {
                            return false;
                        }
                }
            }
        }
        exports._getMountedRootCount = _getMountedRootCount;
        exports.collectCustomHooksForSignature = collectCustomHooksForSignature;
        exports.createSignatureFunctionForTransform = createSignatureFunctionForTransform;
        exports.findAffectedHostInstances = findAffectedHostInstances;
        exports.getFamilyByID = getFamilyByID;
        exports.getFamilyByType = getFamilyByType;
        exports.hasUnrecoverableErrors = hasUnrecoverableErrors;
        exports.injectIntoGlobalHook = injectIntoGlobalHook;
        exports.isLikelyComponentType = isLikelyComponentType;
        exports.performReactRefresh = performReactRefresh;
        exports.register = register;
        exports.setSignature = setSignature;
    })();
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-refresh/runtime.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
'use strict';
if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
;
else {
    module.exports = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-refresh/cjs/react-refresh-runtime.development.js [client] (ecmascript)");
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/@next/react-refresh-utils/dist/internal/helpers.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

/**
 * MIT License
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */ var __importDefault = /*TURBOPACK member replacement*/ __turbopack_context__.e && /*TURBOPACK member replacement*/ __turbopack_context__.e.__importDefault || function(mod) {
    return mod && mod.__esModule ? mod : {
        "default": mod
    };
};
Object.defineProperty(exports, "__esModule", {
    value: true
});
// This file is copied from the Metro JavaScript bundler, with minor tweaks for
// webpack 4 compatibility.
//
// https://github.com/facebook/metro/blob/d6b9685c730d0d63577db40f41369157f28dfa3a/packages/metro/src/lib/polyfills/require.js
const runtime_1 = __importDefault(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-refresh/runtime.js [client] (ecmascript)"));
function isSafeExport(key) {
    return key === '__esModule' || key === '__N_SSG' || key === '__N_SSP' || // TODO: remove this key from page config instead of allow listing it
    key === 'config';
}
function registerExportsForReactRefresh(moduleExports, moduleID) {
    runtime_1.default.register(moduleExports, moduleID + ' %exports%');
    if (moduleExports == null || typeof moduleExports !== 'object') {
        // Exit if we can't iterate over exports.
        // (This is important for legacy environments.)
        return;
    }
    for(var key in moduleExports){
        if (isSafeExport(key)) {
            continue;
        }
        try {
            var exportValue = moduleExports[key];
        } catch (_a) {
            continue;
        }
        var typeID = moduleID + ' %exports% ' + key;
        runtime_1.default.register(exportValue, typeID);
    }
}
function getRefreshBoundarySignature(moduleExports) {
    var signature = [];
    signature.push(runtime_1.default.getFamilyByType(moduleExports));
    if (moduleExports == null || typeof moduleExports !== 'object') {
        // Exit if we can't iterate over exports.
        // (This is important for legacy environments.)
        return signature;
    }
    for(var key in moduleExports){
        if (isSafeExport(key)) {
            continue;
        }
        try {
            var exportValue = moduleExports[key];
        } catch (_a) {
            continue;
        }
        signature.push(key);
        signature.push(runtime_1.default.getFamilyByType(exportValue));
    }
    return signature;
}
function isReactRefreshBoundary(moduleExports) {
    if (runtime_1.default.isLikelyComponentType(moduleExports)) {
        return true;
    }
    if (moduleExports == null || typeof moduleExports !== 'object') {
        // Exit if we can't iterate over exports.
        return false;
    }
    var hasExports = false;
    var areAllExportsComponents = true;
    for(var key in moduleExports){
        hasExports = true;
        if (isSafeExport(key)) {
            continue;
        }
        try {
            var exportValue = moduleExports[key];
        } catch (_a) {
            // This might fail due to circular dependencies
            return false;
        }
        if (!runtime_1.default.isLikelyComponentType(exportValue)) {
            areAllExportsComponents = false;
        }
    }
    return hasExports && areAllExportsComponents;
}
function shouldInvalidateReactRefreshBoundary(prevSignature, nextSignature) {
    if (prevSignature.length !== nextSignature.length) {
        return true;
    }
    for(var i = 0; i < nextSignature.length; i++){
        if (prevSignature[i] !== nextSignature[i]) {
            return true;
        }
    }
    return false;
}
var isUpdateScheduled = false;
// This function aggregates updates from multiple modules into a single React Refresh call.
function scheduleUpdate() {
    if (isUpdateScheduled) {
        return;
    }
    isUpdateScheduled = true;
    function canApplyUpdate(status) {
        return status === 'idle';
    }
    function applyUpdate() {
        isUpdateScheduled = false;
        try {
            runtime_1.default.performReactRefresh();
        } catch (err) {
            console.warn('Warning: Failed to re-render. We will retry on the next Fast Refresh event.\n' + err);
        }
    }
    if (canApplyUpdate(module.hot.status())) {
        // Apply update on the next tick.
        Promise.resolve().then(()=>{
            applyUpdate();
        });
        return;
    }
    const statusHandler = (status)=>{
        if (canApplyUpdate(status)) {
            module.hot.removeStatusHandler(statusHandler);
            applyUpdate();
        }
    };
    // Apply update once the HMR runtime's status is idle.
    module.hot.addStatusHandler(statusHandler);
}
// Needs to be compatible with IE11
exports.default = {
    registerExportsForReactRefresh: registerExportsForReactRefresh,
    isReactRefreshBoundary: isReactRefreshBoundary,
    shouldInvalidateReactRefreshBoundary: shouldInvalidateReactRefreshBoundary,
    getRefreshBoundarySignature: getRefreshBoundarySignature,
    scheduleUpdate: scheduleUpdate
};
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/@next/react-refresh-utils/dist/runtime.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __importDefault = /*TURBOPACK member replacement*/ __turbopack_context__.e && /*TURBOPACK member replacement*/ __turbopack_context__.e.__importDefault || function(mod) {
    return mod && mod.__esModule ? mod : {
        "default": mod
    };
};
Object.defineProperty(exports, "__esModule", {
    value: true
});
const runtime_1 = __importDefault(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-refresh/runtime.js [client] (ecmascript)"));
const helpers_1 = __importDefault(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/@next/react-refresh-utils/dist/internal/helpers.js [client] (ecmascript)"));
// Hook into ReactDOM initialization
runtime_1.default.injectIntoGlobalHook(self);
// Register global helpers
self.$RefreshHelpers$ = helpers_1.default;
// Register a helper for module execution interception
self.$RefreshInterceptModuleExecution$ = function(webpackModuleId) {
    var prevRefreshReg = self.$RefreshReg$;
    var prevRefreshSig = self.$RefreshSig$;
    self.$RefreshReg$ = function(type, id) {
        runtime_1.default.register(type, webpackModuleId + ' ' + id);
    };
    self.$RefreshSig$ = runtime_1.default.createSignatureFunctionForTransform;
    // Modeled after `useEffect` cleanup pattern:
    // https://react.dev/learn/synchronizing-with-effects#step-3-add-cleanup-if-needed
    return function() {
        self.$RefreshReg$ = prevRefreshReg;
        self.$RefreshSig$ = prevRefreshSig;
    };
};
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/path-to-regexp/index.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {

(()=>{
    "use strict";
    if (typeof __nccwpck_require__ !== "undefined") __nccwpck_require__.ab = ("TURBOPACK compile-time value", "/ROOT/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/path-to-regexp") + "/";
    var e = {};
    (()=>{
        var n = e;
        Object.defineProperty(n, "__esModule", {
            value: true
        });
        n.pathToRegexp = n.tokensToRegexp = n.regexpToFunction = n.match = n.tokensToFunction = n.compile = n.parse = void 0;
        function lexer(e) {
            var n = [];
            var r = 0;
            while(r < e.length){
                var t = e[r];
                if (t === "*" || t === "+" || t === "?") {
                    n.push({
                        type: "MODIFIER",
                        index: r,
                        value: e[r++]
                    });
                    continue;
                }
                if (t === "\\") {
                    n.push({
                        type: "ESCAPED_CHAR",
                        index: r++,
                        value: e[r++]
                    });
                    continue;
                }
                if (t === "{") {
                    n.push({
                        type: "OPEN",
                        index: r,
                        value: e[r++]
                    });
                    continue;
                }
                if (t === "}") {
                    n.push({
                        type: "CLOSE",
                        index: r,
                        value: e[r++]
                    });
                    continue;
                }
                if (t === ":") {
                    var a = "";
                    var i = r + 1;
                    while(i < e.length){
                        var o = e.charCodeAt(i);
                        if (o >= 48 && o <= 57 || o >= 65 && o <= 90 || o >= 97 && o <= 122 || o === 95) {
                            a += e[i++];
                            continue;
                        }
                        break;
                    }
                    if (!a) throw new TypeError("Missing parameter name at ".concat(r));
                    n.push({
                        type: "NAME",
                        index: r,
                        value: a
                    });
                    r = i;
                    continue;
                }
                if (t === "(") {
                    var c = 1;
                    var f = "";
                    var i = r + 1;
                    if (e[i] === "?") {
                        throw new TypeError('Pattern cannot start with "?" at '.concat(i));
                    }
                    while(i < e.length){
                        if (e[i] === "\\") {
                            f += e[i++] + e[i++];
                            continue;
                        }
                        if (e[i] === ")") {
                            c--;
                            if (c === 0) {
                                i++;
                                break;
                            }
                        } else if (e[i] === "(") {
                            c++;
                            if (e[i + 1] !== "?") {
                                throw new TypeError("Capturing groups are not allowed at ".concat(i));
                            }
                        }
                        f += e[i++];
                    }
                    if (c) throw new TypeError("Unbalanced pattern at ".concat(r));
                    if (!f) throw new TypeError("Missing pattern at ".concat(r));
                    n.push({
                        type: "PATTERN",
                        index: r,
                        value: f
                    });
                    r = i;
                    continue;
                }
                n.push({
                    type: "CHAR",
                    index: r,
                    value: e[r++]
                });
            }
            n.push({
                type: "END",
                index: r,
                value: ""
            });
            return n;
        }
        function parse(e, n) {
            if (n === void 0) {
                n = {};
            }
            var r = lexer(e);
            var t = n.prefixes, a = t === void 0 ? "./" : t, i = n.delimiter, o = i === void 0 ? "/#?" : i;
            var c = [];
            var f = 0;
            var u = 0;
            var p = "";
            var tryConsume = function(e) {
                if (u < r.length && r[u].type === e) return r[u++].value;
            };
            var mustConsume = function(e) {
                var n = tryConsume(e);
                if (n !== undefined) return n;
                var t = r[u], a = t.type, i = t.index;
                throw new TypeError("Unexpected ".concat(a, " at ").concat(i, ", expected ").concat(e));
            };
            var consumeText = function() {
                var e = "";
                var n;
                while(n = tryConsume("CHAR") || tryConsume("ESCAPED_CHAR")){
                    e += n;
                }
                return e;
            };
            var isSafe = function(e) {
                for(var n = 0, r = o; n < r.length; n++){
                    var t = r[n];
                    if (e.indexOf(t) > -1) return true;
                }
                return false;
            };
            var safePattern = function(e) {
                var n = c[c.length - 1];
                var r = e || (n && typeof n === "string" ? n : "");
                if (n && !r) {
                    throw new TypeError('Must have text between two parameters, missing text after "'.concat(n.name, '"'));
                }
                if (!r || isSafe(r)) return "[^".concat(escapeString(o), "]+?");
                return "(?:(?!".concat(escapeString(r), ")[^").concat(escapeString(o), "])+?");
            };
            while(u < r.length){
                var v = tryConsume("CHAR");
                var s = tryConsume("NAME");
                var d = tryConsume("PATTERN");
                if (s || d) {
                    var g = v || "";
                    if (a.indexOf(g) === -1) {
                        p += g;
                        g = "";
                    }
                    if (p) {
                        c.push(p);
                        p = "";
                    }
                    c.push({
                        name: s || f++,
                        prefix: g,
                        suffix: "",
                        pattern: d || safePattern(g),
                        modifier: tryConsume("MODIFIER") || ""
                    });
                    continue;
                }
                var x = v || tryConsume("ESCAPED_CHAR");
                if (x) {
                    p += x;
                    continue;
                }
                if (p) {
                    c.push(p);
                    p = "";
                }
                var h = tryConsume("OPEN");
                if (h) {
                    var g = consumeText();
                    var l = tryConsume("NAME") || "";
                    var m = tryConsume("PATTERN") || "";
                    var T = consumeText();
                    mustConsume("CLOSE");
                    c.push({
                        name: l || (m ? f++ : ""),
                        pattern: l && !m ? safePattern(g) : m,
                        prefix: g,
                        suffix: T,
                        modifier: tryConsume("MODIFIER") || ""
                    });
                    continue;
                }
                mustConsume("END");
            }
            return c;
        }
        n.parse = parse;
        function compile(e, n) {
            return tokensToFunction(parse(e, n), n);
        }
        n.compile = compile;
        function tokensToFunction(e, n) {
            if (n === void 0) {
                n = {};
            }
            var r = flags(n);
            var t = n.encode, a = t === void 0 ? function(e) {
                return e;
            } : t, i = n.validate, o = i === void 0 ? true : i;
            var c = e.map(function(e) {
                if (typeof e === "object") {
                    return new RegExp("^(?:".concat(e.pattern, ")$"), r);
                }
            });
            return function(n) {
                var r = "";
                for(var t = 0; t < e.length; t++){
                    var i = e[t];
                    if (typeof i === "string") {
                        r += i;
                        continue;
                    }
                    var f = n ? n[i.name] : undefined;
                    var u = i.modifier === "?" || i.modifier === "*";
                    var p = i.modifier === "*" || i.modifier === "+";
                    if (Array.isArray(f)) {
                        if (!p) {
                            throw new TypeError('Expected "'.concat(i.name, '" to not repeat, but got an array'));
                        }
                        if (f.length === 0) {
                            if (u) continue;
                            throw new TypeError('Expected "'.concat(i.name, '" to not be empty'));
                        }
                        for(var v = 0; v < f.length; v++){
                            var s = a(f[v], i);
                            if (o && !c[t].test(s)) {
                                throw new TypeError('Expected all "'.concat(i.name, '" to match "').concat(i.pattern, '", but got "').concat(s, '"'));
                            }
                            r += i.prefix + s + i.suffix;
                        }
                        continue;
                    }
                    if (typeof f === "string" || typeof f === "number") {
                        var s = a(String(f), i);
                        if (o && !c[t].test(s)) {
                            throw new TypeError('Expected "'.concat(i.name, '" to match "').concat(i.pattern, '", but got "').concat(s, '"'));
                        }
                        r += i.prefix + s + i.suffix;
                        continue;
                    }
                    if (u) continue;
                    var d = p ? "an array" : "a string";
                    throw new TypeError('Expected "'.concat(i.name, '" to be ').concat(d));
                }
                return r;
            };
        }
        n.tokensToFunction = tokensToFunction;
        function match(e, n) {
            var r = [];
            var t = pathToRegexp(e, r, n);
            return regexpToFunction(t, r, n);
        }
        n.match = match;
        function regexpToFunction(e, n, r) {
            if (r === void 0) {
                r = {};
            }
            var t = r.decode, a = t === void 0 ? function(e) {
                return e;
            } : t;
            return function(r) {
                var t = e.exec(r);
                if (!t) return false;
                var i = t[0], o = t.index;
                var c = Object.create(null);
                var _loop_1 = function(e) {
                    if (t[e] === undefined) return "continue";
                    var r = n[e - 1];
                    if (r.modifier === "*" || r.modifier === "+") {
                        c[r.name] = t[e].split(r.prefix + r.suffix).map(function(e) {
                            return a(e, r);
                        });
                    } else {
                        c[r.name] = a(t[e], r);
                    }
                };
                for(var f = 1; f < t.length; f++){
                    _loop_1(f);
                }
                return {
                    path: i,
                    index: o,
                    params: c
                };
            };
        }
        n.regexpToFunction = regexpToFunction;
        function escapeString(e) {
            return e.replace(/([.+*?=^!:${}()[\]|/\\])/g, "\\$1");
        }
        function flags(e) {
            return e && e.sensitive ? "" : "i";
        }
        function regexpToRegexp(e, n) {
            if (!n) return e;
            var r = /\((?:\?<(.*?)>)?(?!\?)/g;
            var t = 0;
            var a = r.exec(e.source);
            while(a){
                n.push({
                    name: a[1] || t++,
                    prefix: "",
                    suffix: "",
                    modifier: "",
                    pattern: ""
                });
                a = r.exec(e.source);
            }
            return e;
        }
        function arrayToRegexp(e, n, r) {
            var t = e.map(function(e) {
                return pathToRegexp(e, n, r).source;
            });
            return new RegExp("(?:".concat(t.join("|"), ")"), flags(r));
        }
        function stringToRegexp(e, n, r) {
            return tokensToRegexp(parse(e, r), n, r);
        }
        function tokensToRegexp(e, n, r) {
            if (r === void 0) {
                r = {};
            }
            var t = r.strict, a = t === void 0 ? false : t, i = r.start, o = i === void 0 ? true : i, c = r.end, f = c === void 0 ? true : c, u = r.encode, p = u === void 0 ? function(e) {
                return e;
            } : u, v = r.delimiter, s = v === void 0 ? "/#?" : v, d = r.endsWith, g = d === void 0 ? "" : d;
            var x = "[".concat(escapeString(g), "]|$");
            var h = "[".concat(escapeString(s), "]");
            var l = o ? "^" : "";
            for(var m = 0, T = e; m < T.length; m++){
                var E = T[m];
                if (typeof E === "string") {
                    l += escapeString(p(E));
                } else {
                    var w = escapeString(p(E.prefix));
                    var y = escapeString(p(E.suffix));
                    if (E.pattern) {
                        if (n) n.push(E);
                        if (w || y) {
                            if (E.modifier === "+" || E.modifier === "*") {
                                var R = E.modifier === "*" ? "?" : "";
                                l += "(?:".concat(w, "((?:").concat(E.pattern, ")(?:").concat(y).concat(w, "(?:").concat(E.pattern, "))*)").concat(y, ")").concat(R);
                            } else {
                                l += "(?:".concat(w, "(").concat(E.pattern, ")").concat(y, ")").concat(E.modifier);
                            }
                        } else {
                            if (E.modifier === "+" || E.modifier === "*") {
                                throw new TypeError('Can not repeat "'.concat(E.name, '" without a prefix and suffix'));
                            }
                            l += "(".concat(E.pattern, ")").concat(E.modifier);
                        }
                    } else {
                        l += "(?:".concat(w).concat(y, ")").concat(E.modifier);
                    }
                }
            }
            if (f) {
                if (!a) l += "".concat(h, "?");
                l += !r.endsWith ? "$" : "(?=".concat(x, ")");
            } else {
                var A = e[e.length - 1];
                var _ = typeof A === "string" ? h.indexOf(A[A.length - 1]) > -1 : A === undefined;
                if (!a) {
                    l += "(?:".concat(h, "(?=").concat(x, "))?");
                }
                if (!_) {
                    l += "(?=".concat(h, "|").concat(x, ")");
                }
            }
            return new RegExp(l, flags(r));
        }
        n.tokensToRegexp = tokensToRegexp;
        function pathToRegexp(e, n, r) {
            if (e instanceof RegExp) return regexpToRegexp(e, n);
            if (Array.isArray(e)) return arrayToRegexp(e, n, r);
            return stringToRegexp(e, n, r);
        }
        n.pathToRegexp = pathToRegexp;
    })();
    module.exports = e;
})();
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-is/cjs/react-is.development.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
/**
 * @license React
 * react-is.development.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */ "use strict";
"production" !== ("TURBOPACK compile-time value", "development") && function() {
    function typeOf(object) {
        if ("object" === typeof object && null !== object) {
            var $$typeof = object.$$typeof;
            switch($$typeof){
                case REACT_ELEMENT_TYPE:
                    switch(object = object.type, object){
                        case REACT_FRAGMENT_TYPE:
                        case REACT_PROFILER_TYPE:
                        case REACT_STRICT_MODE_TYPE:
                        case REACT_SUSPENSE_TYPE:
                        case REACT_SUSPENSE_LIST_TYPE:
                        case REACT_VIEW_TRANSITION_TYPE:
                            return object;
                        default:
                            switch(object = object && object.$$typeof, object){
                                case REACT_CONTEXT_TYPE:
                                case REACT_FORWARD_REF_TYPE:
                                case REACT_LAZY_TYPE:
                                case REACT_MEMO_TYPE:
                                    return object;
                                case REACT_CONSUMER_TYPE:
                                    return object;
                                default:
                                    return $$typeof;
                            }
                    }
                case REACT_PORTAL_TYPE:
                    return $$typeof;
            }
        }
    }
    var REACT_ELEMENT_TYPE = Symbol.for("react.transitional.element"), REACT_PORTAL_TYPE = Symbol.for("react.portal"), REACT_FRAGMENT_TYPE = Symbol.for("react.fragment"), REACT_STRICT_MODE_TYPE = Symbol.for("react.strict_mode"), REACT_PROFILER_TYPE = Symbol.for("react.profiler"), REACT_CONSUMER_TYPE = Symbol.for("react.consumer"), REACT_CONTEXT_TYPE = Symbol.for("react.context"), REACT_FORWARD_REF_TYPE = Symbol.for("react.forward_ref"), REACT_SUSPENSE_TYPE = Symbol.for("react.suspense"), REACT_SUSPENSE_LIST_TYPE = Symbol.for("react.suspense_list"), REACT_MEMO_TYPE = Symbol.for("react.memo"), REACT_LAZY_TYPE = Symbol.for("react.lazy"), REACT_VIEW_TRANSITION_TYPE = Symbol.for("react.view_transition"), REACT_CLIENT_REFERENCE = Symbol.for("react.client.reference");
    exports.ContextConsumer = REACT_CONSUMER_TYPE;
    exports.ContextProvider = REACT_CONTEXT_TYPE;
    exports.Element = REACT_ELEMENT_TYPE;
    exports.ForwardRef = REACT_FORWARD_REF_TYPE;
    exports.Fragment = REACT_FRAGMENT_TYPE;
    exports.Lazy = REACT_LAZY_TYPE;
    exports.Memo = REACT_MEMO_TYPE;
    exports.Portal = REACT_PORTAL_TYPE;
    exports.Profiler = REACT_PROFILER_TYPE;
    exports.StrictMode = REACT_STRICT_MODE_TYPE;
    exports.Suspense = REACT_SUSPENSE_TYPE;
    exports.SuspenseList = REACT_SUSPENSE_LIST_TYPE;
    exports.isContextConsumer = function(object) {
        return typeOf(object) === REACT_CONSUMER_TYPE;
    };
    exports.isContextProvider = function(object) {
        return typeOf(object) === REACT_CONTEXT_TYPE;
    };
    exports.isElement = function(object) {
        return "object" === typeof object && null !== object && object.$$typeof === REACT_ELEMENT_TYPE;
    };
    exports.isForwardRef = function(object) {
        return typeOf(object) === REACT_FORWARD_REF_TYPE;
    };
    exports.isFragment = function(object) {
        return typeOf(object) === REACT_FRAGMENT_TYPE;
    };
    exports.isLazy = function(object) {
        return typeOf(object) === REACT_LAZY_TYPE;
    };
    exports.isMemo = function(object) {
        return typeOf(object) === REACT_MEMO_TYPE;
    };
    exports.isPortal = function(object) {
        return typeOf(object) === REACT_PORTAL_TYPE;
    };
    exports.isProfiler = function(object) {
        return typeOf(object) === REACT_PROFILER_TYPE;
    };
    exports.isStrictMode = function(object) {
        return typeOf(object) === REACT_STRICT_MODE_TYPE;
    };
    exports.isSuspense = function(object) {
        return typeOf(object) === REACT_SUSPENSE_TYPE;
    };
    exports.isSuspenseList = function(object) {
        return typeOf(object) === REACT_SUSPENSE_LIST_TYPE;
    };
    exports.isValidElementType = function(type) {
        return "string" === typeof type || "function" === typeof type || type === REACT_FRAGMENT_TYPE || type === REACT_PROFILER_TYPE || type === REACT_STRICT_MODE_TYPE || type === REACT_SUSPENSE_TYPE || type === REACT_SUSPENSE_LIST_TYPE || type === REACT_VIEW_TRANSITION_TYPE || "object" === typeof type && null !== type && (type.$$typeof === REACT_LAZY_TYPE || type.$$typeof === REACT_MEMO_TYPE || type.$$typeof === REACT_CONTEXT_TYPE || type.$$typeof === REACT_CONSUMER_TYPE || type.$$typeof === REACT_FORWARD_REF_TYPE || type.$$typeof === REACT_CLIENT_REFERENCE || void 0 !== type.getModuleId) ? !0 : !1;
    };
    exports.typeOf = typeOf;
}();
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-is/index.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
'use strict';
if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
;
else {
    module.exports = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-is/cjs/react-is.development.js [client] (ecmascript)");
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/next-devtools/index.js (raw)", ((__turbopack_context__, module, exports) => {

var process = {env:
{"__NEXT_DIST_DIR":"/Users/mac/Desktop/markitdown/webapp/frontend/.next/dev","__NEXT_DEV_INDICATOR":true,"__NEXT_DEV_INDICATOR_POSITION":"bottom-left","__NEXT_INSTANT_NAV_TOGGLE":false,"__NEXT_ROUTER_BASEPATH":"","__NEXT_TELEMETRY_DISABLED":false,"__NEXT_BUNDLER":"Turbopack","__NEXT_BUNDLER_HAS_PERSISTENT_CACHE":true,"TURBOPACK":true,"__NEXT_CACHE_COMPONENTS":false}
};
(function(){
var __webpack_modules__={"../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/components/devtools-indicator/devtools-indicator.css"(e,t,r){"use strict";r.d(t,{A:()=>l});var n=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/noSourceMaps.js"),o=r.n(n),a=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/api.js"),i=r.n(a)()(o());i.push([e.id,`[data-nextjs-toast] {
  &[data-hidden='true'] {
    display: none;
  }
}

.dev-tools-indicator-menu {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  background: var(--color-background-100);
  border: 1px solid var(--color-gray-alpha-400);
  background-clip: padding-box;
  box-shadow: var(--shadow-menu);
  border-radius: var(--rounded-xl);
  position: absolute;
  font-family: var(--font-stack-sans);
  z-index: 3;
  overflow: hidden;
  opacity: 0;
  outline: 0;
  min-width: 248px;
  transition: opacity var(--animate-out-duration-ms)
    var(--animate-out-timing-function);

  &[data-rendered='true'] {
    opacity: 1;
    scale: 1;
  }
}

.dev-tools-indicator-inner {
  padding: 6px;
  width: 100%;
}

.dev-tools-indicator-item {
  display: flex;
  align-items: center;
  padding: 8px 6px;
  height: var(--size-36);
  border-radius: 6px;
  text-decoration: none !important;
  user-select: none;
  white-space: nowrap;

  svg {
    width: var(--size-16);
    height: var(--size-16);
  }

  &:focus-visible {
    outline: 0;
  }
}

.dev-tools-indicator-footer {
  background: var(--color-background-200);
  padding: 6px;
  border-top: 1px solid var(--color-gray-400);
  width: 100%;
}

.dev-tools-indicator-item[data-selected='true'] {
  cursor: pointer;
  background-color: var(--color-gray-200);
}

.dev-tools-indicator-label {
  font-size: var(--size-14);
  line-height: var(--size-20);
  color: var(--color-gray-1000);
}

.dev-tools-indicator-value {
  font-size: var(--size-14);
  line-height: var(--size-20);
  color: var(--color-gray-900);
  margin-left: auto;
}

.dev-tools-indicator-issue-count {
  --color-primary: var(--color-gray-800);
  --color-secondary: var(--color-gray-100);
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-width: var(--size-40);
  height: var(--size-24);
  background: var(--color-background-100);
  border: 1px solid var(--color-gray-alpha-400);
  background-clip: padding-box;
  box-shadow: var(--shadow-small);
  padding: 2px;
  color: var(--color-gray-1000);
  border-radius: 128px;
  font-weight: 500;
  font-size: var(--size-13);
  font-variant-numeric: tabular-nums;

  &[data-has-issues='true'] {
    --color-primary: var(--color-red-800);
    --color-secondary: var(--color-red-100);
  }

  .dev-tools-indicator-issue-count-indicator {
    width: var(--size-8);
    height: var(--size-8);
    background: var(--color-primary);
    box-shadow: 0 0 0 2px var(--color-secondary);
    border-radius: 50%;
  }
}

.dev-tools-indicator-shortcut {
  display: flex;
  gap: 4px;

  kbd {
    width: var(--size-20);
    height: var(--size-20);
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: var(--rounded-md);
    border: 1px solid var(--color-gray-400);
    font-family: var(--font-stack-sans);
    background: var(--color-background-100);
    color: var(--color-gray-1000);
    text-align: center;
    font-size: var(--size-12);
    line-height: var(--size-16);
  }
}

.dev-tools-grabbing {
  cursor: grabbing;

  > * {
    pointer-events: none;
  }
}
`,""]);let l=i},"../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/components/devtools-panel/resize/resize-handle.css"(e,t,r){"use strict";r.d(t,{A:()=>l});var n=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/noSourceMaps.js"),o=r.n(n),a=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/api.js"),i=r.n(a)()(o());i.push([e.id,`.resize-container {
  position: absolute;
  /* todo: better z index */
  z-index: 10;
  /* todo: is this needed */
  background: transparent;
}

.resize-line {
  position: absolute;
  /* todo smarter z index */
  z-index: -1;
  pointer-events: none;
  /* a normal exit animation curve- at this point the exit animation is */
  /* immediately responsive so we don't need a bespoke curve */
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  /* todo: better var? */
  border: 1px solid var(--color-gray-400);
}

/* start really fast because we start super hidden initially behind the panel, otherwise feels like an unintended animation delay */
.resize-container:hover ~ .resize-line {
  transition: transform 0.25s cubic-bezier(0.23, 1, 0.32, 0.9);
}

.resize-container.right,
.resize-container.left {
  top: 0;
  height: 100%;
  width: 22px;
  cursor: ew-resize;
}

/* todo: don't hard code all these values/use vars */

.resize-container.bottom,
.resize-container.top {
  left: 0;
  width: 100%;
  height: 22px;
  cursor: ns-resize;
}

.resize-container.top {
  top: -7px;
}
.resize-container.bottom {
  bottom: -7px;
}
.resize-container.left {
  left: -7px;
}
.resize-container.right {
  right: -7px;
}

.resize-container.top-left,
.resize-container.top-right,
.resize-container.bottom-left,
.resize-container.bottom-right {
  width: 26px;
  height: 26px;
  z-index: 15;
}

.resize-container.top-left {
  top: -5px;
  left: -5px;
  cursor: nwse-resize;
}
.resize-container.top-right {
  top: -5px;
  right: -5px;
  cursor: nesw-resize;
}
.resize-container.bottom-left {
  bottom: -5px;
  left: -5px;
  cursor: nesw-resize;
}
.resize-container.bottom-right {
  bottom: -5px;
  right: -5px;
  cursor: nwse-resize;
}

.resize-line.top,
.resize-line.bottom {
  height: 18px;
  width: 100%;
  background-color: var(--color-background-200);
}

.resize-line.left,
.resize-line.right {
  width: 18px;
  height: 100%;
  background-color: var(--color-background-200);
}

.resize-line.top {
  top: -7px;
  left: calc(-1 * var(--border-left, 2px));
  width: calc(100% + var(--border-horizontal, 4px));
  border-radius: var(--rounded-lg) var(--rounded-lg) 0 0;
  transform: translateY(18px);
}

.resize-line.bottom {
  bottom: -7px;
  left: calc(-1 * var(--border-left, 2px));
  width: calc(100% + var(--border-horizontal, 4px));
  border-radius: 0 0 var(--rounded-lg) var(--rounded-lg);
  transform: translateY(-18px);
}

.resize-line.left {
  top: calc(-1 * var(--border-top, 2px));
  left: -7px;
  height: calc(100% + var(--border-vertical, 4px));
  border-radius: var(--rounded-lg) 0 0 var(--rounded-lg);
  transform: translateX(18px);
}

.resize-line.right {
  top: calc(-1 * var(--border-top, 2px));
  right: -7px;
  height: calc(100% + var(--border-vertical, 4px));
  border-radius: 0 var(--rounded-lg) var(--rounded-lg) 0;
  transform: translateX(-18px);
}

.resize-container.right:hover ~ .resize-line.right,
.resize-container.left:hover ~ .resize-line.left,
.resize-line.right.dragging,
.resize-line.left.dragging {
  transform: translateX(0);
}

.resize-container.bottom:hover ~ .resize-line.bottom,
.resize-container.top:hover ~ .resize-line.top,
.resize-line.bottom.dragging,
.resize-line.top.dragging {
  transform: translateY(0);
}

/* make sure that we don't show multiple handles at once
 * we should only ever show the currently resizing handle
 * regardless of hover state 
 */
.resize-container.no-hover.right:hover ~ .resize-line.right {
  transform: translateX(-20px);
}
.resize-container.no-hover.left:hover ~ .resize-line.left {
  transform: translateX(20px);
}
.resize-container.no-hover.bottom:hover ~ .resize-line.bottom {
  transform: translateY(-20px);
}
.resize-container.no-hover.top:hover ~ .resize-line.top {
  transform: translateY(20px);
}
`,""]);let l=i},"../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/components/instant-navs/instant-navs-panel.css"(e,t,r){"use strict";r.d(t,{A:()=>l});var n=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/noSourceMaps.js"),o=r.n(n),a=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/api.js"),i=r.n(a)()(o());i.push([e.id,`.instant-nav-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.instant-nav-content {
  flex: 1;
  padding: 12px 20px 0;
}

/* Waiting state: preference-style sections */
.instant-nav-section {
  padding: 12px 20px;
  border-bottom: 1px solid var(--color-gray-400);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
}

.instant-nav-section:last-child {
  border-bottom: none;
}

.instant-nav-section-header {
  flex: 1;
}

.instant-nav-section-header label {
  font-size: var(--size-14);
  font-weight: 500;
  color: var(--color-gray-1000);
  margin: 0;
}

.instant-nav-section-description {
  color: var(--color-gray-900);
  font-size: var(--size-14);
  margin: 0;
}

.instant-nav-section-control {
  flex-shrink: 0;
}

.instant-nav-section-control .action-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--color-background-100);
  border: 1px solid var(--color-gray-400);
  border-radius: var(--rounded-lg);
  font-weight: 400;
  font-size: var(--size-14);
  color: var(--color-gray-1000);
  padding: 6px 8px;
  cursor: pointer;
  transition: border-color 150ms var(--timing-swift);
}

.instant-nav-section-control .action-button:hover {
  border-color: var(--color-gray-500);
}

.instant-nav-section-control .action-button svg {
  width: 14px;
  height: 14px;
  overflow: visible;
}

.instant-nav-helper-text {
  font-size: var(--size-14);
  color: var(--color-gray-900);
  font-style: italic;
  white-space: nowrap;
}

/* Result states (client-nav, initial-load) */
.instant-nav-status-title {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-gray-900);
}

.instant-nav-urls {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: 4px;
}

.instant-nav-url-row {
  display: flex;
  gap: 8px;
  font-size: 13px;
}

.instant-nav-url-label {
  color: var(--color-gray-700);
  flex-shrink: 0;
}

.instant-nav-url-value {
  color: var(--color-gray-900);
  word-break: break-all;
  font-family: var(--font-mono);
}

.instant-nav-actions {
  margin-top: 8px;
  display: flex;
}

.instant-nav-share-button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 16px;
  border-radius: 6px;
  border: 1px solid var(--color-gray-alpha-400);
  background: var(--color-background-200);
  color: var(--color-gray-900);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: background 150ms ease;
}

.instant-nav-share-button:hover {
  background: var(--color-gray-alpha-200);
}

.instant-nav-helper-description {
  color: var(--color-gray-900);
  font-size: var(--size-14);
  margin: 8px 0 0;
}

/* Footer (pinned to bottom, matching segment-explorer-footer) */
.instant-nav-footer {
  display: flex;
  gap: 8px;
  padding: 8px;
  border-top: 1px solid var(--color-gray-400);
  user-select: none;
}

.instant-nav-footer-button {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
  gap: 8px;
  padding: 6px;
  background: var(--color-background-100);
  border: 1px solid var(--color-gray-400);
  border-radius: 6px;
  color: var(--color-gray-1000);
  font-size: var(--size-14);
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.instant-nav-footer-button:hover {
  background: var(--color-gray-200);
}

/* Shimmer skeleton for pending "to" route */
@keyframes instant-nav-shimmer {
  0% {
    background-position: -400px 0;
  }
  100% {
    background-position: 400px 0;
  }
}

.instant-nav-skeleton {
  display: inline-block;
  width: 120px;
  height: 1em;
  vertical-align: middle;
  border-radius: 4px;
  background: linear-gradient(
    90deg,
    var(--color-gray-300) 25%,
    var(--color-blue-300) 50%,
    var(--color-gray-300) 75%
  );
  background-size: 800px 100%;
  animation: instant-nav-shimmer 1.5s ease-in-out infinite;
}
`,""]);let l=i},"../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/components/overview/segment-boundary-trigger.css"(e,t,r){"use strict";r.d(t,{A:()=>l});var n=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/noSourceMaps.js"),o=r.n(n),a=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/api.js"),i=r.n(a)()(o());i.push([e.id,`.segment-boundary-trigger {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 6px;
  line-height: 16px;
  font-weight: 500;
  color: var(--color-gray-1000);
  border-radius: 999px;
  border: none;
  font-size: var(--size-12);
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.segment-boundary-trigger-text {
  font-size: var(--size-12);
  font-weight: 500;
  user-select: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.segment-boundary-trigger-text .plus-icon {
  transition: transform 0.25s ease;
}

.segment-boundary-trigger-text:hover .plus-icon {
  color: var(--color-gray-800);
}

.segment-boundary-trigger svg {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
  vertical-align: middle;
}

.segment-boundary-trigger:hover svg {
  color: var(--color-gray-700);
}

.segment-boundary-trigger[disabled] svg,
.segment-boundary-trigger[disabled]:hover svg {
  color: var(--color-gray-400);
  cursor: not-allowed;
}

.segment-boundary-dropdown {
  padding: 8px;
  background: var(--color-background-100);
  border: 1px solid var(--color-gray-400);
  border-radius: 16px;
  min-width: 120px;
  user-select: none;
  cursor: default;
  box-shadow: 0px 4px 8px -4px
    color-mix(in srgb, var(--color-gray-900) 4%, transparent);
}

.segment-boundary-dropdown-positioner {
  z-index: var(--top-z-index);
}

.segment-boundary-dropdown-item {
  display: flex;
  align-items: center;
  padding: 8px;
  line-height: 20px;
  font-size: 14px;
  border-radius: 6px;
  color: var(--color-gray-1000);
  cursor: pointer;
  min-width: 220px;
  border: none;
  background: none;
  width: 100%;
}

.segment-boundary-dropdown-item[data-disabled] {
  color: var(--color-gray-400);
  cursor: not-allowed;
}

.segment-boundary-dropdown-item svg {
  margin-right: 12px;
  color: currentColor;
}

.segment-boundary-dropdown-item:hover {
  background: var(--color-gray-200);
}

.segment-boundary-dropdown-item:first-child {
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}

.segment-boundary-dropdown-item:last-child {
  border-bottom-left-radius: 4px;
  border-bottom-right-radius: 4px;
}

.segment-boundary-group-label {
  padding: 8px;
  font-size: 13px;
  line-height: 16px;
  font-weight: 400;
  color: var(--color-gray-900);
}
`,""]);let l=i},"../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/components/overview/segment-explorer.css"(e,t,r){"use strict";r.d(t,{A:()=>l});var n=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/noSourceMaps.js"),o=r.n(n),a=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/api.js"),i=r.n(a)()(o());i.push([e.id,`.segment-explorer-content {
  font-size: var(--size-14);
  padding: 0 8px;
  width: 100%;
  height: 100%;
}

.segment-explorer-page-route-bar {
  display: flex;
  align-items: center;
  padding: 14px 16px;
  background-color: var(--color-background-200);
  gap: 12px;
}

.segment-explorer-page-route-bar-path {
  font-size: var(--size-14);
  font-weight: 500;
  color: var(--color-gray-1000);
  font-family: var(--font-mono);
  white-space: nowrap;
  line-height: 20px;
}

.segment-explorer-item {
  margin: 4px 0;
  border-radius: 6px;
}

.segment-explorer-item:nth-child(even) {
  background-color: var(--color-background-200);
}
.segment-explorer-item-row {
  display: flex;
  flex-direction: column;
  padding-top: 10px;
  padding-bottom: 10px;
  padding-right: 4px;
}
.segment-explorer-item-row-main {
  display: flex;
  align-items: center;
  white-space: pre;
  color: var(--color-gray-1000);
}

.segment-explorer-children--intended {
  padding-left: 16px;
}

.segment-explorer-filename {
  display: inline-flex;
  width: 100%;
  align-items: center;
}

.segment-explorer-filename select {
  margin-left: auto;
}
.segment-explorer-filename--path {
  margin-right: 8px;
}
.segment-explorer-filename--path small {
  display: inline-block;
  width: 0;
  opacity: 0;
}
.segment-explorer-filename--name {
  color: var(--color-gray-800);
}

.segment-explorer-files {
  display: inline-flex;
  gap: 8px;
  margin-left: auto;
}

.segment-explorer-files + .segment-boundary-trigger {
  margin-left: 8px;
}

.segment-explorer-file-label {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0 6px;
  height: 20px;
  border-radius: 16px;
  line-height: 16px;
  font-size: var(--size-12);
  font-weight: 500;
  background-color: var(--color-gray-300);
  color: var(--color-gray-1000);
}
.segment-explorer-file-label-text {
  display: inline-flex;
  align-items: center;
}

.segment-explorer-file-label--overridden {
  background-color: var(--color-amber-300);
  color: var(--color-amber-900);
}

.segment-explorer-file-label .code-icon {
  opacity: 0;
  margin-left: 0;
  width: 0;
  transition: all 0.15s ease-in-out;
}
.segment-explorer-file-label:hover .code-icon {
  opacity: 1;
  width: 12px;
  margin-left: 4px;
}

.segment-explorer-file-label:hover {
  filter: brightness(0.95);
}

.segment-explorer-file-label--builtin {
  background-color: transparent;
  color: var(--color-gray-900);
  border: 1px dashed var(--color-gray-500);
  height: 24px;
  cursor: default;
}
.segment-explorer-file-label--builtin svg {
  margin-left: 4px;
  margin-right: -4px;
}

/* Footer styles */
.segment-explorer-footer {
  padding: 8px;
  border-top: 1px solid var(--color-gray-400);
  user-select: none;
}

.segment-explorer-footer-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 6px;
  background: var(--color-background-100);
  border: 1px solid var(--color-gray-400);
  border-radius: 6px;
  color: var(--color-gray-1000);
  font-size: var(--size-14);
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.segment-explorer-footer-button:hover:not(:disabled) {
  background: var(--color-gray-200);
}

.segment-explorer-footer-button--disabled {
  cursor: not-allowed;
}

.segment-explorer-footer-text {
  text-align: center;
}

.segment-explorer-footer-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  background: var(--color-amber-300);
  color: var(--color-amber-900);
  border-radius: 10px;
  font-size: var(--size-12);
  font-weight: 600;
  line-height: 1;
}

.segment-explorer-file-label-tooltip--sm {
  white-space: nowrap;
}

.segment-explorer-file-label-tooltip--lg {
  min-width: 200px;
}

.segment-explorer-suggestions {
  display: inline-flex;
  gap: 8px;
}

.segment-explorer-suggestions-tooltip {
  width: 200px;
}
`,""]);let l=i},"../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/components/toast/style.css"(e,t,r){"use strict";r.d(t,{A:()=>l});var n=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/noSourceMaps.js"),o=r.n(n),a=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/api.js"),i=r.n(a)()(o());i.push([e.id,`.nextjs-toast {
  position: fixed;
  z-index: var(--top-z-index);
  max-width: 420px;
  box-shadow: 0px 16px 32px rgba(0, 0, 0, 0.25);
}

.nextjs-toast-errors-parent {
  padding: 16px;
  border-radius: var(--rounded-4xl);
  font-weight: 500;
  color: var(--color-ansi-bright-white);
  background-color: var(--color-ansi-red);
}
`,""]);let l=i},"../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/components/tooltip/tooltip.css"(e,t,r){"use strict";r.d(t,{A:()=>l});var n=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/noSourceMaps.js"),o=r.n(n),a=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/api.js"),i=r.n(a)()(o());i.push([e.id,`.tooltip-wrapper {
  position: relative;
  display: inline-block;
  line-height: 1;
}

.tooltip {
  position: relative;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.4;
  pointer-events: none;
  color: var(--color-gray-100);
  background-color: var(--color-gray-1000);
}

.tooltip-arrow {
  position: absolute;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: var(--arrow-size, 6px);
  border-color: transparent;
}

.tooltip-arrow--top {
  border-width: var(--arrow-size, 6px) var(--arrow-size, 6px) 0
    var(--arrow-size, 6px);
  border-top-color: var(--color-gray-1000);
  bottom: 0;
  transform: translateY(100%);
}

.tooltip-arrow--bottom {
  border-width: 0 var(--arrow-size, 6px) var(--arrow-size, 6px)
    var(--arrow-size, 6px);
  border-bottom-color: var(--color-gray-1000);
  top: 0;
  transform: translateY(-100%);
}

.tooltip-arrow--left {
  border-width: var(--arrow-size, 6px) 0 var(--arrow-size, 6px)
    var(--arrow-size, 6px);
  border-left-color: var(--color-gray-1000);
  right: 0;
  transform: translateX(100%);
}

.tooltip-arrow--right {
  border-width: var(--arrow-size, 6px) var(--arrow-size, 6px)
    var(--arrow-size, 6px) 0;
  border-right-color: var(--color-gray-1000);
  left: 0;
  transform: translateX(-100%);
}

.tooltip-positioner {
  z-index: var(--top-z-index);
}
`,""]);let l=i},"../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/global.css"(e,t,r){"use strict";r.d(t,{A:()=>f});var n=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/noSourceMaps.js"),o=r.n(n),a=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/api.js"),i=r.n(a),l=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/normalize.css"),s=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/styles/default-theme.css"),c=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/styles/dark-theme.css"),u=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/styles/colors.css"),d=i()(o());d.i(l.A),d.i(s.A),d.i(c.A),d.i(u.A),d.push([e.id,`/* devtool global css variables */
:host {
  /* variables */
  --top-z-index: 2147483647;
}

/* global styles */
* {
  -webkit-font-smoothing: antialiased;
}

/* global reset for draggable content scrollbar styles */
[data-nextjs-scrollable-content],
[data-nextjs-scrollable-content] * {
  &::-webkit-scrollbar {
    width: 6px;
    height: 6px;
    border-radius: 0 0 1rem 1rem;
    margin-bottom: 1rem;
  }

  &::-webkit-scrollbar-button {
    display: none;
  }

  &::-webkit-scrollbar-track {
    border-radius: 0 0 1rem 1rem;
    background-color: var(--color-background-100);
  }

  &::-webkit-scrollbar-thumb {
    border-radius: 1rem;
    background-color: var(--color-gray-500);
  }
}

/* Place overflow: hidden on this so we can break out from [data-nextjs-dialog] */
[data-nextjs-scrollable-content] {
  overflow: hidden;
  border-radius: inherit;
}
`,""]);let f=d},"../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/menu/panel-router.css"(e,t,r){"use strict";r.d(t,{A:()=>l});var n=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/noSourceMaps.js"),o=r.n(n),a=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/api.js"),i=r.n(a)()(o());i.push([e.id,`/* Panel content padding styles */
.panel-content {
  padding: 16px;
  padding-top: 8px;
  overflow: hidden;
}

/* User preferences wrapper styles */
.user-preferences-wrapper {
  padding: 20px;
  padding-top: 8px;
  overflow: hidden;
}

/* Panel route base styles */
.panel-route {
  opacity: var(--panel-opacity);
  transition: var(--panel-transition);
}

.turbopack-upgrade-link {
  text-decoration: underline;
  font-weight: 500;
}
`,""]);let l=i},"../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/normalize.css"(e,t,r){"use strict";r.d(t,{A:()=>l});var n=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/noSourceMaps.js"),o=r.n(n),a=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/api.js"),i=r.n(a)()(o());i.push([e.id,`:host {
  all: initial;

  /* the direction property is not reset by 'all' */
  direction: ltr;
}

/*!
 * Bootstrap Reboot v4.4.1 (https://getbootstrap.com/)
 * Copyright 2011-2019 The Bootstrap Authors
 * Copyright 2011-2019 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * Forked from Normalize.css, licensed MIT (https://github.com/necolas/normalize.css/blob/master/LICENSE.md)
 */
*,
*::before,
*::after {
  box-sizing: border-box;
}

:host {
  font-family: sans-serif;
  line-height: 1.15;
  -webkit-text-size-adjust: 100%;
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
}

article,
aside,
figcaption,
figure,
footer,
header,
hgroup,
main,
nav,
section {
  display: block;
}

:host {
  margin: 0;
  font-family:
    -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue',
    Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji',
    'Segoe UI Symbol', 'Noto Color Emoji';
  font-size: 16px;
  font-weight: 400;
  line-height: 1.5;
  color: var(--color-font);
  text-align: left;
}

:host:not(button) {
  background-color: #fff;
}

[tabindex='-1']:focus:not(:focus-visible) {
  outline: 0 !important;
}

hr {
  box-sizing: content-box;
  height: 0;
  overflow: visible;
}

h1,
h2,
h3,
h4,
h5,
h6 {
  margin-top: 0;
  margin-bottom: 8px;
}

p {
  margin-top: 0;
  margin-bottom: 16px;
}

abbr[title],
abbr[data-original-title] {
  text-decoration: underline;
  -webkit-text-decoration: underline dotted;
  text-decoration: underline dotted;
  cursor: help;
  border-bottom: 0;
  -webkit-text-decoration-skip-ink: none;
  text-decoration-skip-ink: none;
}

address {
  margin-bottom: 16px;
  font-style: normal;
  line-height: inherit;
}

ol,
ul,
dl {
  margin-top: 0;
  margin-bottom: 16px;
}

ol ol,
ul ul,
ol ul,
ul ol {
  margin-bottom: 0;
}

dt {
  font-weight: 700;
}

dd {
  margin-bottom: 8px;
  margin-left: 0;
}

blockquote {
  margin: 0 0 16px;
}

b,
strong {
  font-weight: bolder;
}

small {
  font-size: 80%;
}

sub,
sup {
  position: relative;
  font-size: 75%;
  line-height: 0;
  vertical-align: baseline;
}

sub {
  bottom: -0.25em;
}

sup {
  top: -0.5em;
}

a {
  color: #007bff;
  text-decoration: none;
  background-color: transparent;
}

a:hover {
  color: #0056b3;
  text-decoration: underline;
}

a:not([href]) {
  color: inherit;
  text-decoration: none;
}

a:not([href]):hover {
  color: inherit;
  text-decoration: none;
}

pre,
code,
kbd,
samp {
  font-family:
    SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New',
    monospace;
  font-size: 1em;
}

pre {
  margin-top: 0;
  margin-bottom: 16px;
  overflow: auto;
}

figure {
  margin: 0 0 16px;
}

img {
  vertical-align: middle;
  border-style: none;
}

svg {
  overflow: hidden;
  vertical-align: middle;
}

table {
  border-collapse: collapse;
}

caption {
  padding-top: 12px;
  padding-bottom: 12px;
  color: #6c757d;
  text-align: left;
  caption-side: bottom;
}

th {
  text-align: inherit;
}

label {
  display: inline-block;
  margin-bottom: 8px;
}

button {
  border-radius: 0;
  border: 0;
  padding: 0;
  margin: 0;
  background: none;
  appearance: none;
  -webkit-appearance: none;
}

button:focus {
  outline: 1px dotted;
  outline: 5px auto -webkit-focus-ring-color;
}

button:focus:not(:focus-visible) {
  outline: none;
}

input,
button,
select,
optgroup,
textarea {
  margin: 0;
  font-family: inherit;
  font-size: inherit;
  line-height: inherit;
}

button,
input {
  overflow: visible;
}

button,
select {
  text-transform: none;
}

select {
  word-wrap: normal;
}

button,
[type='button'],
[type='reset'],
[type='submit'] {
  -webkit-appearance: button;
}

button:not(:disabled),
[type='button']:not(:disabled),
[type='reset']:not(:disabled),
[type='submit']:not(:disabled) {
  cursor: pointer;
}

button::-moz-focus-inner,
[type='button']::-moz-focus-inner,
[type='reset']::-moz-focus-inner,
[type='submit']::-moz-focus-inner {
  padding: 0;
  border-style: none;
}

input[type='radio'],
input[type='checkbox'] {
  box-sizing: border-box;
  padding: 0;
}

input[type='date'],
input[type='time'],
input[type='datetime-local'],
input[type='month'] {
  -webkit-appearance: listbox;
}

textarea {
  overflow: auto;
  resize: vertical;
}

fieldset {
  min-width: 0;
  padding: 0;
  margin: 0;
  border: 0;
}

legend {
  display: block;
  width: 100%;
  max-width: 100%;
  padding: 0;
  margin-bottom: 8px;
  font-size: 24px;
  line-height: inherit;
  color: inherit;
  white-space: normal;
}

progress {
  vertical-align: baseline;
}

[type='number']::-webkit-inner-spin-button,
[type='number']::-webkit-outer-spin-button {
  height: auto;
}

[type='search'] {
  outline-offset: -2px;
  -webkit-appearance: none;
}

[type='search']::-webkit-search-decoration {
  -webkit-appearance: none;
}

::-webkit-file-upload-button {
  font: inherit;
  -webkit-appearance: button;
}

output {
  display: inline-block;
}

summary {
  display: list-item;
  cursor: pointer;
}

template {
  display: none;
}

[hidden] {
  display: none !important;
}
`,""]);let l=i},"../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/panel/dynamic-panel.css"(e,t,r){"use strict";r.d(t,{A:()=>l});var n=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/noSourceMaps.js"),o=r.n(n),a=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/api.js"),i=r.n(a)()(o());i.push([e.id,`/* Panel container base styles with dynamic positioning and sizing */
.dynamic-panel-container {
  position: fixed;
  z-index: 2147483646;
  outline: none;
  top: var(--panel-top, auto);
  bottom: var(--panel-bottom, auto);
  left: var(--panel-left, auto);
  right: var(--panel-right, auto);
  width: var(--panel-width);
  height: var(--panel-height);
  min-width: var(--panel-min-width);
  min-height: var(--panel-min-height);
  max-width: var(--panel-max-width);
  max-height: var(--panel-max-height);
}

/* Panel content container styles */
.panel-content-container {
  position: relative;
  width: 100%;
  height: 100%;
  border: 1px solid var(--color-gray-alpha-400);
  border-radius: var(--rounded-xl);
  background: var(--color-background-100);
  display: flex;
  flex-direction: column;
}

/* Draggable content area styles */
.draggable-content {
  flex: 1;
  overflow: auto;
}
`,""]);let l=i},"../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/styles/colors.css"(e,t,r){"use strict";r.d(t,{A:()=>l});var n=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/noSourceMaps.js"),o=r.n(n),a=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/api.js"),i=r.n(a)()(o());i.push([e.id,`:host {
  /*
   * CAUTION: THIS IS A WORKAROUND!
   * The code frame renderer (next-code-frame) uses hardcoded ANSI colors that don't match
   * our theme colors. We do a workaround mapping to change the ANSI color matching the theme.
   *
   * next-code-frame color scheme:
   *   cyan (36m):    keywords (const, function, return, etc.)
   *   yellow (33m):  capitalized identifiers (Component names, types)
   *   magenta (35m): numbers, regex literals
   *   green (32m):   strings
   *   gray (90m):    comments, gutter
   */
  /* cyan: keyword */
  --color-ansi-cyan: var(--color-syntax-keyword);
  /* yellow: capitalized identifiers */
  --color-ansi-yellow: var(--color-syntax-function);
  /* magenta: number, regex */
  --color-ansi-magenta: var(--color-syntax-keyword);
  /* green: string */
  --color-ansi-green: var(--color-syntax-string);
  /* gray (bright black): comment, gutter */
  --color-ansi-bright-black: var(--color-syntax-comment);

  /* Ansi - Temporary */
  --color-ansi-selection: var(--color-gray-alpha-300);
  --color-ansi-bg: var(--color-background-200);
  --color-ansi-fg: var(--color-gray-1000);

  --color-ansi-white: var(--color-gray-700);
  --color-ansi-black: var(--color-gray-200);
  --color-ansi-blue: var(--color-blue-700);
  --color-ansi-red: var(--color-red-700);
  --color-ansi-bright-white: var(--color-gray-1000);
  --color-ansi-bright-blue: var(--color-blue-800);
  --color-ansi-bright-cyan: var(--color-blue-800);
  --color-ansi-bright-green: var(--color-green-800);
  --color-ansi-bright-magenta: var(--color-blue-800);
  --color-ansi-bright-red: var(--color-red-800);
  --color-ansi-bright-yellow: var(--color-amber-900);

  /* Background Light */
  --color-background-100: #ffffff;
  --color-background-200: #fafafa;

  /* Syntax Light */
  --color-syntax-comment: #545454;
  --color-syntax-constant: #171717;
  --color-syntax-function: #0054ad;
  --color-syntax-keyword: #a51850;
  --color-syntax-link: #066056;
  --color-syntax-parameter: #8f3e00;
  --color-syntax-punctuation: #171717;
  --color-syntax-string: #036157;
  --color-syntax-string-expression: #066056;

  /* Gray Scale Light */
  --color-gray-100: #f2f2f2;
  --color-gray-200: #ebebeb;
  --color-gray-300: #e6e6e6;
  --color-gray-400: #eaeaea;
  --color-gray-500: #c9c9c9;
  --color-gray-600: #a8a8a8;
  --color-gray-700: #8f8f8f;
  --color-gray-800: #7d7d7d;
  --color-gray-900: #666666;
  --color-gray-1000: #171717;

  /* Gray Alpha Scale Light */
  --color-gray-alpha-100: rgba(0, 0, 0, 0.05);
  --color-gray-alpha-200: rgba(0, 0, 0, 0.081);
  --color-gray-alpha-300: rgba(0, 0, 0, 0.1);
  --color-gray-alpha-400: rgba(0, 0, 0, 0.08);
  --color-gray-alpha-500: rgba(0, 0, 0, 0.21);
  --color-gray-alpha-600: rgba(0, 0, 0, 0.34);
  --color-gray-alpha-700: rgba(0, 0, 0, 0.44);
  --color-gray-alpha-800: rgba(0, 0, 0, 0.51);
  --color-gray-alpha-900: rgba(0, 0, 0, 0.605);
  --color-gray-alpha-1000: rgba(0, 0, 0, 0.91);

  /* Blue Scale Light */
  --color-blue-100: #f0f7ff;
  --color-blue-200: #edf6ff;
  --color-blue-300: #e1f0ff;
  --color-blue-400: #cde7ff;
  --color-blue-500: #99ceff;
  --color-blue-600: #52aeff;
  --color-blue-700: #0070f3;
  --color-blue-800: #0060d1;
  --color-blue-900: #0067d6;
  --color-blue-1000: #0025ad;

  /* Red Scale Light */
  --color-red-100: #fff0f0;
  --color-red-200: #ffebeb;
  --color-red-300: #ffe5e5;
  --color-red-400: #fdd8d8;
  --color-red-500: #f8baba;
  --color-red-600: #f87274;
  --color-red-700: #e5484d;
  --color-red-800: #da3036;
  --color-red-900: #ca2a30;
  --color-red-1000: #381316;

  /* Amber Scale Light */
  --color-amber-100: #fff6e5;
  --color-amber-200: #fff4d5;
  --color-amber-300: #fef0cd;
  --color-amber-400: #ffddbf;
  --color-amber-500: #ffc96b;
  --color-amber-600: #f5b047;
  --color-amber-700: #ffb224;
  --color-amber-800: #ff990a;
  --color-amber-900: #a35200;
  --color-amber-1000: #4e2009;

  /* Green Scale Light */
  --color-green-100: #effbef;
  --color-green-200: #eafaea;
  --color-green-300: #dcf6dc;
  --color-green-400: #c8f1c9;
  --color-green-500: #99e59f;
  --color-green-600: #6cda76;
  --color-green-700: #46a758;
  --color-green-800: #388e4a;
  --color-green-900: #297c3b;
  --color-green-1000: #18311e;

  /* Turbopack Light - Temporary */
  --color-turbopack-text-red: #ff1e56;
  --color-turbopack-text-blue: #0096ff;
  --color-turbopack-border-red: #f0adbe;
  --color-turbopack-border-blue: #adccea;
  --color-turbopack-background-red: #fff7f9;
  --color-turbopack-background-blue: #f6fbff;
}
`,""]);let l=i},"../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/styles/dark-theme.css"(e,t,r){"use strict";r.d(t,{A:()=>l});var n=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/noSourceMaps.js"),o=r.n(n),a=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/api.js"),i=r.n(a)()(o());i.push([e.id,`:host(.dark) {
  --color-font: white;
  --color-backdrop: rgba(0, 0, 0, 0.8);
  --color-border-shadow: rgba(255, 255, 255, 0.145);

  --color-title-color: #fafafa;
  --color-stack-notes: #a9a9a9;

  /* Background Dark */
  --color-background-100: #0a0a0a;
  --color-background-200: #000000;

  /* Syntax Dark */
  --color-syntax-comment: #a0a0a0;
  --color-syntax-constant: #ededed;
  --color-syntax-function: #52a9ff;
  --color-syntax-keyword: #f76e99;
  --color-syntax-link: #0ac5b2;
  --color-syntax-parameter: #f1a10d;
  --color-syntax-punctuation: #ededed;
  --color-syntax-string: #0ac5b2;
  --color-syntax-string-expression: #0ac5b2;

  /* Gray Scale Dark */
  --color-gray-100: #1a1a1a;
  --color-gray-200: #1f1f1f;
  --color-gray-300: #292929;
  --color-gray-400: #2e2e2e;
  --color-gray-500: #454545;
  --color-gray-600: #878787;
  --color-gray-700: #8f8f8f;
  --color-gray-800: #7d7d7d;
  --color-gray-900: #a0a0a0;
  --color-gray-1000: #ededed;

  /* Gray Alpha Scale Dark */
  --color-gray-alpha-100: rgba(255, 255, 255, 0.066);
  --color-gray-alpha-200: rgba(255, 255, 255, 0.087);
  --color-gray-alpha-300: rgba(255, 255, 255, 0.125);
  --color-gray-alpha-400: rgba(255, 255, 255, 0.145);
  --color-gray-alpha-500: rgba(255, 255, 255, 0.239);
  --color-gray-alpha-600: rgba(255, 255, 255, 0.506);
  --color-gray-alpha-700: rgba(255, 255, 255, 0.54);
  --color-gray-alpha-800: rgba(255, 255, 255, 0.47);
  --color-gray-alpha-900: rgba(255, 255, 255, 0.61);
  --color-gray-alpha-1000: rgba(255, 255, 255, 0.923);

  /* Blue Scale Dark */
  --color-blue-100: #0f1b2d;
  --color-blue-200: #10243e;
  --color-blue-300: #0f3058;
  --color-blue-400: #0d3868;
  --color-blue-500: #0a4481;
  --color-blue-600: #0091ff;
  --color-blue-700: #0070f3;
  --color-blue-800: #0060d1;
  --color-blue-900: #52a9ff;
  --color-blue-1000: #eaf6ff;

  /* Red Scale Dark */
  --color-red-100: #2a1314;
  --color-red-200: #3d1719;
  --color-red-300: #551a1e;
  --color-red-400: #671e22;
  --color-red-500: #822025;
  --color-red-600: #e5484d;
  --color-red-700: #e5484d;
  --color-red-800: #da3036;
  --color-red-900: #ff6369;
  --color-red-1000: #ffecee;

  /* Amber Scale Dark */
  --color-amber-100: #271700;
  --color-amber-200: #341c00;
  --color-amber-300: #4a2900;
  --color-amber-400: #573300;
  --color-amber-500: #693f05;
  --color-amber-600: #e79c13;
  --color-amber-700: #ffb224;
  --color-amber-800: #ff990a;
  --color-amber-900: #f1a10d;
  --color-amber-1000: #fef3dd;

  /* Green Scale Dark */
  --color-green-100: #0b2211;
  --color-green-200: #0f2c17;
  --color-green-300: #11351b;
  --color-green-400: #0c461b;
  --color-green-500: #126427;
  --color-green-600: #1a9338;
  --color-green-700: #46a758;
  --color-green-800: #388e4a;
  --color-green-900: #63c174;
  --color-green-1000: #e5fbeb;

  /* Turbopack Dark - Temporary */
  --color-turbopack-text-red: #ff6d92;
  --color-turbopack-text-blue: #45b2ff;
  --color-turbopack-border-red: #6e293b;
  --color-turbopack-border-blue: #284f80;
  --color-turbopack-background-red: #250d12;
  --color-turbopack-background-blue: #0a1723;
}

@media (prefers-color-scheme: dark) {
  :host(:not(.light)) {
    --color-font: white;
    --color-backdrop: rgba(0, 0, 0, 0.8);
    --color-border-shadow: rgba(255, 255, 255, 0.145);

    --color-title-color: #fafafa;
    --color-stack-notes: #a9a9a9;

    /* Background Dark */
    --color-background-100: #0a0a0a;
    --color-background-200: #000000;

    /* Syntax Dark */
    --color-syntax-comment: #a0a0a0;
    --color-syntax-constant: #ededed;
    --color-syntax-function: #52a9ff;
    --color-syntax-keyword: #f76e99;
    --color-syntax-link: #0ac5b2;
    --color-syntax-parameter: #f1a10d;
    --color-syntax-punctuation: #ededed;
    --color-syntax-string: #0ac5b2;
    --color-syntax-string-expression: #0ac5b2;

    /* Gray Scale Dark */
    --color-gray-100: #1a1a1a;
    --color-gray-200: #1f1f1f;
    --color-gray-300: #292929;
    --color-gray-400: #2e2e2e;
    --color-gray-500: #454545;
    --color-gray-600: #878787;
    --color-gray-700: #8f8f8f;
    --color-gray-800: #7d7d7d;
    --color-gray-900: #a0a0a0;
    --color-gray-1000: #ededed;

    /* Gray Alpha Scale Dark */
    --color-gray-alpha-100: rgba(255, 255, 255, 0.066);
    --color-gray-alpha-200: rgba(255, 255, 255, 0.087);
    --color-gray-alpha-300: rgba(255, 255, 255, 0.125);
    --color-gray-alpha-400: rgba(255, 255, 255, 0.145);
    --color-gray-alpha-500: rgba(255, 255, 255, 0.239);
    --color-gray-alpha-600: rgba(255, 255, 255, 0.506);
    --color-gray-alpha-700: rgba(255, 255, 255, 0.54);
    --color-gray-alpha-800: rgba(255, 255, 255, 0.47);
    --color-gray-alpha-900: rgba(255, 255, 255, 0.61);
    --color-gray-alpha-1000: rgba(255, 255, 255, 0.923);

    /* Blue Scale Dark */
    --color-blue-100: #0f1b2d;
    --color-blue-200: #10243e;
    --color-blue-300: #0f3058;
    --color-blue-400: #0d3868;
    --color-blue-500: #0a4481;
    --color-blue-600: #0091ff;
    --color-blue-700: #0070f3;
    --color-blue-800: #0060d1;
    --color-blue-900: #52a9ff;
    --color-blue-1000: #eaf6ff;

    /* Red Scale Dark */
    --color-red-100: #2a1314;
    --color-red-200: #3d1719;
    --color-red-300: #551a1e;
    --color-red-400: #671e22;
    --color-red-500: #822025;
    --color-red-600: #e5484d;
    --color-red-700: #e5484d;
    --color-red-800: #da3036;
    --color-red-900: #ff6369;
    --color-red-1000: #ffecee;

    /* Amber Scale Dark */
    --color-amber-100: #271700;
    --color-amber-200: #341c00;
    --color-amber-300: #4a2900;
    --color-amber-400: #573300;
    --color-amber-500: #693f05;
    --color-amber-600: #e79c13;
    --color-amber-700: #ffb224;
    --color-amber-800: #ff990a;
    --color-amber-900: #f1a10d;
    --color-amber-1000: #fef3dd;

    /* Green Scale Dark */
    --color-green-100: #0b2211;
    --color-green-200: #0f2c17;
    --color-green-300: #11351b;
    --color-green-400: #0c461b;
    --color-green-500: #126427;
    --color-green-600: #1a9338;
    --color-green-700: #46a758;
    --color-green-800: #388e4a;
    --color-green-900: #63c174;
    --color-green-1000: #e5fbeb;

    /* Turbopack Dark - Temporary */
    --color-turbopack-text-red: #ff6d92;
    --color-turbopack-text-blue: #45b2ff;
    --color-turbopack-border-red: #6e293b;
    --color-turbopack-border-blue: #284f80;
    --color-turbopack-background-red: #250d12;
    --color-turbopack-background-blue: #0a1723;
  }
}
`,""]);let l=i},"../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/styles/default-theme.css"(e,t,r){"use strict";r.d(t,{A:()=>l});var n=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/noSourceMaps.js"),o=r.n(n),a=r("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/api.js"),i=r.n(a)()(o());i.push([e.id,`:host {
  /* 
   * Although the style applied to the shadow host is isolated,
   * the element that attached the shadow host (i.e. "nextjs-portal")
   * is still affected by the parent's style (e.g. "body"). This may
   * occur style conflicts like "display: flex", with other children
   * elements therefore give the shadow host an absolute position.
   */
  position: absolute;

  --color-font: #757575;
  --color-backdrop: rgba(250, 250, 250, 0.8);
  --color-border-shadow: rgba(0, 0, 0, 0.145);

  --color-title-color: #1f1f1f;
  --color-stack-notes: #777;

  --color-accents-1: #808080;
  --color-accents-2: #222222;
  --color-accents-3: #404040;

  --font-stack-monospace:
    '__nextjs-Geist Mono', 'Geist Mono', 'SFMono-Regular', Consolas,
    'Liberation Mono', Menlo, Courier, monospace;
  --font-stack-sans:
    '__nextjs-Geist', 'Geist', -apple-system, 'Source Sans Pro', sans-serif;

  font-family: var(--font-stack-sans);
  font-variant-ligatures: none;

  /* TODO: Remove replaced ones. */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg:
    0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-xl:
    0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  --shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);
  --shadow-inner: inset 0 2px 4px 0 rgb(0 0 0 / 0.05);
  --shadow-none: 0 0 #0000;

  --shadow-small: 0px 2px 2px rgba(0, 0, 0, 0.04);
  --shadow-menu:
    0px 1px 1px rgba(0, 0, 0, 0.02), 0px 4px 8px -4px rgba(0, 0, 0, 0.04),
    0px 16px 24px -8px rgba(0, 0, 0, 0.06);

  --focus-color: var(--color-blue-800);
  --focus-ring: 2px solid var(--focus-color);

  --timing-swift: cubic-bezier(0.23, 0.88, 0.26, 0.92);
  --timing-overlay: cubic-bezier(0.175, 0.885, 0.32, 1.1);
  /* prettier-ignore */
  --timing-bounce: linear(0 0%, 0.005871 1%, 0.022058 2%, 0.046612 3%, 0.077823 4%, 0.114199 5%, 0.154441 6%, 0.197431 7.000000000000001%, 0.242208 8%, 0.287959 9%, 0.333995 10%, 0.379743 11%, 0.424732 12%, 0.46858 13%, 0.510982 14.000000000000002%, 0.551702 15%, 0.590564 16%, 0.627445 17%, 0.662261 18%, 0.694971 19%, 0.725561 20%, 0.754047 21%, 0.780462 22%, 0.804861 23%, 0.82731 24%, 0.847888 25%, 0.866679 26%, 0.883775 27%, 0.899272 28.000000000000004%, 0.913267 28.999999999999996%, 0.925856 30%, 0.937137 31%, 0.947205 32%, 0.956153 33%, 0.96407 34%, 0.971043 35%, 0.977153 36%, 0.982479 37%, 0.987094 38%, 0.991066 39%, 0.994462 40%, 0.997339 41%, 0.999755 42%, 1.001761 43%, 1.003404 44%, 1.004727 45%, 1.00577 46%, 1.006569 47%, 1.007157 48%, 1.007563 49%, 1.007813 50%, 1.007931 51%, 1.007939 52%, 1.007855 53%, 1.007697 54%, 1.007477 55.00000000000001%, 1.00721 56.00000000000001%, 1.006907 56.99999999999999%, 1.006576 57.99999999999999%, 1.006228 59%, 1.005868 60%, 1.005503 61%, 1.005137 62%, 1.004776 63%, 1.004422 64%, 1.004078 65%, 1.003746 66%, 1.003429 67%, 1.003127 68%, 1.00284 69%, 1.002571 70%, 1.002318 71%, 1.002082 72%, 1.001863 73%, 1.00166 74%, 1.001473 75%, 1.001301 76%, 1.001143 77%, 1.001 78%, 1.000869 79%, 1.000752 80%, 1.000645 81%, 1.00055 82%, 1.000464 83%, 1.000388 84%, 1.000321 85%, 1.000261 86%, 1.000209 87%, 1.000163 88%, 1.000123 89%, 1.000088 90%);

  --rounded-none: 0px;
  --rounded-sm: 2px;
  --rounded-md: 4px;
  --rounded-md-2: 6px;
  --rounded-lg: 8px;
  --rounded-xl: 12px;
  --rounded-2xl: 16px;
  --rounded-3xl: 24px;
  --rounded-4xl: 32px;
  --rounded-full: 9999px;

  /* 
    This value gets set from the Dev Tools preferences,
    and we use the following --size-* variables to 
    scale the relevant elements.

    The reason why we don't rely on rem values is because
    if an app sets their root font size to something tiny, 
    it feels unexpected to have the app root size leak 
    into a Next.js surface.

    https://github.com/vercel/next.js/discussions/76812
  */
  --nextjs-dev-tools-scale: 1;
  --size-1: calc(1px / var(--nextjs-dev-tools-scale));
  --size-2: calc(2px / var(--nextjs-dev-tools-scale));
  --size-3: calc(3px / var(--nextjs-dev-tools-scale));
  --size-4: calc(4px / var(--nextjs-dev-tools-scale));
  --size-5: calc(5px / var(--nextjs-dev-tools-scale));
  --size-6: calc(6px / var(--nextjs-dev-tools-scale));
  --size-7: calc(7px / var(--nextjs-dev-tools-scale));
  --size-8: calc(8px / var(--nextjs-dev-tools-scale));
  --size-9: calc(9px / var(--nextjs-dev-tools-scale));
  --size-10: calc(10px / var(--nextjs-dev-tools-scale));
  --size-11: calc(11px / var(--nextjs-dev-tools-scale));
  --size-12: calc(12px / var(--nextjs-dev-tools-scale));
  --size-13: calc(13px / var(--nextjs-dev-tools-scale));
  --size-14: calc(14px / var(--nextjs-dev-tools-scale));
  --size-15: calc(15px / var(--nextjs-dev-tools-scale));
  --size-16: calc(16px / var(--nextjs-dev-tools-scale));
  --size-17: calc(17px / var(--nextjs-dev-tools-scale));
  --size-18: calc(18px / var(--nextjs-dev-tools-scale));
  --size-20: calc(20px / var(--nextjs-dev-tools-scale));
  --size-22: calc(22px / var(--nextjs-dev-tools-scale));
  --size-24: calc(24px / var(--nextjs-dev-tools-scale));
  --size-26: calc(26px / var(--nextjs-dev-tools-scale));
  --size-28: calc(28px / var(--nextjs-dev-tools-scale));
  --size-30: calc(30px / var(--nextjs-dev-tools-scale));
  --size-32: calc(32px / var(--nextjs-dev-tools-scale));
  --size-34: calc(34px / var(--nextjs-dev-tools-scale));
  --size-36: calc(36px / var(--nextjs-dev-tools-scale));
  --size-38: calc(38px / var(--nextjs-dev-tools-scale));
  --size-40: calc(40px / var(--nextjs-dev-tools-scale));
  --size-42: calc(42px / var(--nextjs-dev-tools-scale));
  --size-44: calc(44px / var(--nextjs-dev-tools-scale));
  --size-46: calc(46px / var(--nextjs-dev-tools-scale));
  --size-48: calc(48px / var(--nextjs-dev-tools-scale));

  @media print {
    display: none;
  }
}

h1,
h2,
h3,
h4,
h5,
h6 {
  margin-bottom: 8px;
  font-weight: 500;
  line-height: 1.5;
}

a {
  color: var(--color-blue-900);
  &:hover {
    color: var(--color-blue-900);
  }
  &:focus-visible {
    outline: var(--focus-ring);
  }
}
`,""]);let l=i},"../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/api.js"(e){"use strict";e.exports=function(e){var t=[];return t.toString=function(){return this.map(function(t){var r="",n=void 0!==t[5];return t[4]&&(r+="@supports (".concat(t[4],") {")),t[2]&&(r+="@media ".concat(t[2]," {")),n&&(r+="@layer".concat(t[5].length>0?" ".concat(t[5]):""," {")),r+=e(t),n&&(r+="}"),t[2]&&(r+="}"),t[4]&&(r+="}"),r}).join("")},t.i=function(e,r,n,o,a){"string"==typeof e&&(e=[[null,e,void 0]]);var i={};if(n)for(var l=0;l<this.length;l++){var s=this[l][0];null!=s&&(i[s]=!0)}for(var c=0;c<e.length;c++){var u=[].concat(e[c]);n&&i[u[0]]||(void 0!==a&&(void 0===u[5]||(u[1]="@layer".concat(u[5].length>0?" ".concat(u[5]):""," {").concat(u[1],"}")),u[5]=a),r&&(u[2]&&(u[1]="@media ".concat(u[2]," {").concat(u[1],"}")),u[2]=r),o&&(u[4]?(u[1]="@supports (".concat(u[4],") {").concat(u[1],"}"),u[4]=o):u[4]="".concat(o)),t.push(u))}},t}},"../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/runtime/noSourceMaps.js"(e){"use strict";e.exports=function(e){return e[1]}},"../../node_modules/.pnpm/style-loader@4.0.0_webpack@5.98.0_@swc+core@1.11.24_@swc+helpers@0.5.15__esbuild@0.25.9_/node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js"(e){"use strict";var t=[];function r(e){for(var r=-1,n=0;n<t.length;n++)if(t[n].identifier===e){r=n;break}return r}function n(e,n){for(var o={},a=[],i=0;i<e.length;i++){var l=e[i],s=n.base?l[0]+n.base:l[0],c=o[s]||0,u="".concat(s," ").concat(c);o[s]=c+1;var d=r(u),f={css:l[1],media:l[2],sourceMap:l[3],supports:l[4],layer:l[5]};if(-1!==d)t[d].references++,t[d].updater(f);else{var p=function(e,t){var r=t.domAPI(t);return r.update(e),function(t){t?(t.css!==e.css||t.media!==e.media||t.sourceMap!==e.sourceMap||t.supports!==e.supports||t.layer!==e.layer)&&r.update(e=t):r.remove()}}(f,n);n.byIndex=i,t.splice(i,0,{identifier:u,updater:p,references:1})}a.push(u)}return a}e.exports=function(e,o){var a=n(e=e||[],o=o||{});return function(e){e=e||[];for(var i=0;i<a.length;i++){var l=r(a[i]);t[l].references--}for(var s=n(e,o),c=0;c<a.length;c++){var u=r(a[c]);0===t[u].references&&(t[u].updater(),t.splice(u,1))}a=s}}},"../../node_modules/.pnpm/style-loader@4.0.0_webpack@5.98.0_@swc+core@1.11.24_@swc+helpers@0.5.15__esbuild@0.25.9_/node_modules/style-loader/dist/runtime/insertStyleElement.js"(e){"use strict";e.exports=function(e){var t=document.createElement("style");return e.setAttributes(t,e.attributes),e.insert(t,e.options),t}},"../../node_modules/.pnpm/style-loader@4.0.0_webpack@5.98.0_@swc+core@1.11.24_@swc+helpers@0.5.15__esbuild@0.25.9_/node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js"(e,t,r){"use strict";e.exports=function(e){var t=r.nc;t&&e.setAttribute("nonce",t)}},"../../node_modules/.pnpm/style-loader@4.0.0_webpack@5.98.0_@swc+core@1.11.24_@swc+helpers@0.5.15__esbuild@0.25.9_/node_modules/style-loader/dist/runtime/styleDomAPI.js"(e){"use strict";e.exports=function(e){if("undefined"==typeof document)return{update:function(){},remove:function(){}};var t=e.insertStyleElement(e);return{update:function(r){var n,o,a;n="",r.supports&&(n+="@supports (".concat(r.supports,") {")),r.media&&(n+="@media ".concat(r.media," {")),(o=void 0!==r.layer)&&(n+="@layer".concat(r.layer.length>0?" ".concat(r.layer):""," {")),n+=r.css,o&&(n+="}"),r.media&&(n+="}"),r.supports&&(n+="}"),(a=r.sourceMap)&&"undefined"!=typeof btoa&&(n+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(a))))," */")),e.styleTagTransform(n,t,e.options)},remove:function(){var e;null===(e=t).parentNode||e.parentNode.removeChild(e)}}}},"../../node_modules/.pnpm/style-loader@4.0.0_webpack@5.98.0_@swc+core@1.11.24_@swc+helpers@0.5.15__esbuild@0.25.9_/node_modules/style-loader/dist/runtime/styleTagTransform.js"(e){"use strict";e.exports=function(e,t){if(t.styleSheet)t.styleSheet.cssText=e;else{for(;t.firstChild;)t.removeChild(t.firstChild);t.appendChild(document.createTextNode(e))}}},"./dist/compiled/anser/index.js"(e){(()=>{"use strict";var t={211:e=>{var t=function(){function e(e,t){for(var r=0;r<t.length;r++){var n=t[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}return function(t,r,n){return r&&e(t.prototype,r),n&&e(t,n),t}}(),r=[[{color:"0, 0, 0",class:"ansi-black"},{color:"187, 0, 0",class:"ansi-red"},{color:"0, 187, 0",class:"ansi-green"},{color:"187, 187, 0",class:"ansi-yellow"},{color:"0, 0, 187",class:"ansi-blue"},{color:"187, 0, 187",class:"ansi-magenta"},{color:"0, 187, 187",class:"ansi-cyan"},{color:"255,255,255",class:"ansi-white"}],[{color:"85, 85, 85",class:"ansi-bright-black"},{color:"255, 85, 85",class:"ansi-bright-red"},{color:"0, 255, 0",class:"ansi-bright-green"},{color:"255, 255, 85",class:"ansi-bright-yellow"},{color:"85, 85, 255",class:"ansi-bright-blue"},{color:"255, 85, 255",class:"ansi-bright-magenta"},{color:"85, 255, 255",class:"ansi-bright-cyan"},{color:"255, 255, 255",class:"ansi-bright-white"}]];e.exports=function(){function e(){if(!(this instanceof e))throw TypeError("Cannot call a class as a function");this.fg=this.bg=this.fg_truecolor=this.bg_truecolor=null,this.bright=0}return t(e,null,[{key:"escapeForHtml",value:function(t){return(new e).escapeForHtml(t)}},{key:"linkify",value:function(t){return(new e).linkify(t)}},{key:"ansiToHtml",value:function(t,r){return(new e).ansiToHtml(t,r)}},{key:"ansiToJson",value:function(t,r){return(new e).ansiToJson(t,r)}},{key:"ansiToText",value:function(t){return(new e).ansiToText(t)}}]),t(e,[{key:"setupPalette",value:function(){this.PALETTE_COLORS=[];for(var e=0;e<2;++e)for(var t=0;t<8;++t)this.PALETTE_COLORS.push(r[e][t].color);for(var n=[0,95,135,175,215,255],o=function(e,t,r){return n[e]+", "+n[t]+", "+n[r]},a=0;a<6;++a)for(var i=0;i<6;++i)for(var l=0;l<6;++l)this.PALETTE_COLORS.push(o(a,i,l));for(var s=8,c=0;c<24;++c,s+=10)this.PALETTE_COLORS.push(o(s,s,s))}},{key:"escapeForHtml",value:function(e){return e.replace(/[&<>]/gm,function(e){return"&"==e?"&amp;":"<"==e?"&lt;":">"==e?"&gt;":""})}},{key:"linkify",value:function(e){return e.replace(/(https?:\/\/[^\s]+)/gm,function(e){return'<a href="'+e+'">'+e+"</a>"})}},{key:"ansiToHtml",value:function(e,t){return this.process(e,t,!0)}},{key:"ansiToJson",value:function(e,t){return(t=t||{}).json=!0,t.clearLine=!1,this.process(e,t,!0)}},{key:"ansiToText",value:function(e){return this.process(e,{},!1)}},{key:"process",value:function(e,t,r){var n=this,o=e.split(/\033\[/),a=o.shift();null==t&&(t={}),t.clearLine=/\r/.test(e);var i=o.map(function(e){return n.processChunk(e,t,r)});if(t&&t.json){var l=this.processChunkJson("");return l.content=a,l.clearLine=t.clearLine,i.unshift(l),t.remove_empty&&(i=i.filter(function(e){return!e.isEmpty()})),i}return i.unshift(a),i.join("")}},{key:"processChunkJson",value:function(e,t,n){var o=(t=void 0===t?{}:t).use_classes=void 0!==t.use_classes&&t.use_classes,a=t.key=o?"class":"color",i={content:e,fg:null,bg:null,fg_truecolor:null,bg_truecolor:null,clearLine:t.clearLine,decoration:null,was_processed:!1,isEmpty:function(){return!i.content}},l=e.match(/^([!\x3c-\x3f]*)([\d;]*)([\x20-\x2c]*[\x40-\x7e])([\s\S]*)/m);if(!l)return i;i.content=l[4];var s=l[2].split(";");if(""!==l[1]||"m"!==l[3]||!n)return i;for(this.decoration=null;s.length>0;){var c=parseInt(s.shift());if(isNaN(c)||0===c)this.fg=this.bg=this.decoration=null;else if(1===c)this.decoration="bold";else if(2===c)this.decoration="dim";else if(3==c)this.decoration="italic";else if(4==c)this.decoration="underline";else if(5==c)this.decoration="blink";else if(7===c)this.decoration="reverse";else if(8===c)this.decoration="hidden";else if(9===c)this.decoration="strikethrough";else if(39==c)this.fg=null;else if(49==c)this.bg=null;else if(c>=30&&c<38)this.fg=r[0][c%10][a];else if(c>=90&&c<98)this.fg=r[1][c%10][a];else if(c>=40&&c<48)this.bg=r[0][c%10][a];else if(c>=100&&c<108)this.bg=r[1][c%10][a];else if(38===c||48===c){var u=38===c;if(s.length>=1){var d=s.shift();if("5"===d&&s.length>=1){var f=parseInt(s.shift());if(f>=0&&f<=255)if(o){var p=f>=16?"ansi-palette-"+f:r[+(f>7)][f%8].class;u?this.fg=p:this.bg=p}else this.PALETTE_COLORS||this.setupPalette(),u?this.fg=this.PALETTE_COLORS[f]:this.bg=this.PALETTE_COLORS[f]}else if("2"===d&&s.length>=3){var h=parseInt(s.shift()),m=parseInt(s.shift()),g=parseInt(s.shift());if(h>=0&&h<=255&&m>=0&&m<=255&&g>=0&&g<=255){var v=h+", "+m+", "+g;o?u?(this.fg="ansi-truecolor",this.fg_truecolor=v):(this.bg="ansi-truecolor",this.bg_truecolor=v):u?this.fg=v:this.bg=v}}}}}return null===this.fg&&null===this.bg&&null===this.decoration||(i.fg=this.fg,i.bg=this.bg,i.fg_truecolor=this.fg_truecolor,i.bg_truecolor=this.bg_truecolor,i.decoration=this.decoration,i.was_processed=!0),i}},{key:"processChunk",value:function(e,t,r){var n=this;t=t||{};var o=this.processChunkJson(e,t,r);if(t.json)return o;if(o.isEmpty())return"";if(!o.was_processed)return o.content;var a=t.use_classes,i=[],l=[],s={},c=function(e){var t=[],r=void 0;for(r in e)e.hasOwnProperty(r)&&t.push("data-"+r+'="'+n.escapeForHtml(e[r])+'"');return t.length>0?" "+t.join(" "):""};return(o.fg&&(a?(l.push(o.fg+"-fg"),null!==o.fg_truecolor&&(s["ansi-truecolor-fg"]=o.fg_truecolor,o.fg_truecolor=null)):i.push("color:rgb("+o.fg+")")),o.bg&&(a?(l.push(o.bg+"-bg"),null!==o.bg_truecolor&&(s["ansi-truecolor-bg"]=o.bg_truecolor,o.bg_truecolor=null)):i.push("background-color:rgb("+o.bg+")")),o.decoration&&(a?l.push("ansi-"+o.decoration):"bold"===o.decoration?i.push("font-weight:bold"):"dim"===o.decoration?i.push("opacity:0.5"):"italic"===o.decoration?i.push("font-style:italic"):"reverse"===o.decoration?i.push("filter:invert(100%)"):"hidden"===o.decoration?i.push("visibility:hidden"):"strikethrough"===o.decoration?i.push("text-decoration:line-through"):i.push("text-decoration:"+o.decoration)),a)?'<span class="'+l.join(" ")+'"'+c(s)+">"+o.content+"</span>":'<span style="'+i.join(";")+'"'+c(s)+">"+o.content+"</span>"}}]),e}()}},r={};function n(e){var o=r[e];if(void 0!==o)return o.exports;var a=r[e]={exports:{}},i=!0;try{t[e](a,a.exports,n),i=!1}finally{i&&delete r[e]}return a.exports}n.ab="//",e.exports=n(211)})()},"./dist/compiled/react-dom/cjs/react-dom-client.production.js"(e,t,r){"use strict";var n,o=r("./dist/compiled/scheduler/index.js"),a=r("./dist/compiled/react/index.js"),i=r("./dist/compiled/react-dom/index.js");function l(e){var t="https://react.dev/errors/"+e;if(1<arguments.length){t+="?args[]="+encodeURIComponent(arguments[1]);for(var r=2;r<arguments.length;r++)t+="&args[]="+encodeURIComponent(arguments[r])}return"Minified React error #"+e+"; visit "+t+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}function s(e){for(var t=e,r=t;r&&!r.alternate;)0!=(4098&(t=r).flags)&&(e=t.return),r=t.return;for(;t.return;)t=t.return;return 3===t.tag?e:null}function c(e){if(13===e.tag){var t=e.memoizedState;if(null===t&&null!==(e=e.alternate)&&(t=e.memoizedState),null!==t)return t.dehydrated}return null}function u(e){if(31===e.tag){var t=e.memoizedState;if(null===t&&null!==(e=e.alternate)&&(t=e.memoizedState),null!==t)return t.dehydrated}return null}function d(e){if(s(e)!==e)throw Error(l(188))}function f(e,t,r,n,o,a){for(;null!==e;){if((5===e.tag||6===e.tag)&&r(e,n,o,a)||(22!==e.tag||null===e.memoizedState)&&(t||5!==e.tag)&&f(e.child,t,r,n,o,a))return!0;e=e.sibling}return!1}function p(e){for(e=e.return;null!==e;){if(3===e.tag||5===e.tag)return e;e=e.return}return null}function h(e){switch(e.tag){case 5:case 6:return e.stateNode;case 3:return e.stateNode.containerInfo;default:throw Error(l(559))}}var m=null,g=null;function v(e){return m=e,!0}function y(e,t,r){return e===r||e===t&&(m=e,!0)}function b(e,t,r){return e===r?(g=e,!1):e===t&&(null!==g&&(m=e),!0)}function x(e){if(null===e)return null;do e=null===e?null:e.return;while(e&&5!==e.tag&&27!==e.tag&&3!==e.tag);return e||null}function _(e,t,r){for(var n=0,o=e;o;o=r(o))n++;o=0;for(var a=t;a;a=r(a))o++;for(;0<n-o;)e=r(e),n--;for(;0<o-n;)t=r(t),o--;for(;n--;){if(e===t||null!==t&&e===t.alternate)return e;e=r(e),t=r(t)}return null}var w=Object.assign,k=Symbol.for("react.element"),j=Symbol.for("react.transitional.element"),S=Symbol.for("react.portal"),C=Symbol.for("react.fragment"),E=Symbol.for("react.strict_mode"),T=Symbol.for("react.profiler"),N=Symbol.for("react.consumer"),L=Symbol.for("react.context"),I=Symbol.for("react.forward_ref"),P=Symbol.for("react.suspense"),z=Symbol.for("react.suspense_list"),R=Symbol.for("react.memo"),O=Symbol.for("react.lazy");Symbol.for("react.scope");var M=Symbol.for("react.activity"),A=Symbol.for("react.legacy_hidden");Symbol.for("react.tracing_marker");var D=Symbol.for("react.memo_cache_sentinel"),Z=Symbol.for("react.view_transition"),F=Symbol.iterator;function U(e){return null===e||"object"!=typeof e?null:"function"==typeof(e=F&&e[F]||e["@@iterator"])?e:null}var $=Symbol.for("react.client.reference"),H=Array.isArray,V=a.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE,B=i.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE,q={pending:!1,data:null,method:null,action:null},W=[],K=-1;function Y(e){return{current:e}}function X(e){0>K||(e.current=W[K],W[K]=null,K--)}function G(e,t){W[++K]=e.current,e.current=t}var Q=Y(null),J=Y(null),ee=Y(null),et=Y(null);function er(e,t){switch(G(ee,t),G(J,e),G(Q,null),t.nodeType){case 9:case 11:e=(e=t.documentElement)&&(e=e.namespaceURI)?ud(e):0;break;default:if(e=t.tagName,t=t.namespaceURI)e=uf(t=ud(t),e);else switch(e){case"svg":e=1;break;case"math":e=2;break;default:e=0}}X(Q),G(Q,e)}function en(){X(Q),X(J),X(ee)}function eo(e){var t=e.memoizedState;null!==t&&(dw._currentValue=t.memoizedState,G(et,e));var r=uf(t=Q.current,e.type);t!==r&&(G(J,e),G(Q,r))}function ea(e){J.current===e&&(X(Q),X(J)),et.current===e&&(X(et),dw._currentValue=q)}function ei(e){if(void 0===tX)try{throw Error()}catch(e){var t=e.stack.trim().match(/\n( *(at )?)/);tX=t&&t[1]||"",tG=-1<e.stack.indexOf("\n    at")?" (<anonymous>)":-1<e.stack.indexOf("@")?"@unknown:0:0":""}return"\n"+tX+e+tG}var el=!1;function es(e,t){if(!e||el)return"";el=!0;var r=Error.prepareStackTrace;Error.prepareStackTrace=void 0;try{var n={DetermineComponentFrameRoot:function(){try{if(t){var r=function(){throw Error()};if(Object.defineProperty(r.prototype,"props",{set:function(){throw Error()}}),"object"==typeof Reflect&&Reflect.construct){try{Reflect.construct(r,[])}catch(e){var n=e}Reflect.construct(e,[],r)}else{try{r.call()}catch(e){n=e}e.call(r.prototype)}}else{try{throw Error()}catch(e){n=e}(r=e())&&"function"==typeof r.catch&&r.catch(function(){})}}catch(e){if(e&&n&&"string"==typeof e.stack)return[e.stack,n.stack]}return[null,null]}};n.DetermineComponentFrameRoot.displayName="DetermineComponentFrameRoot";var o=Object.getOwnPropertyDescriptor(n.DetermineComponentFrameRoot,"name");o&&o.configurable&&Object.defineProperty(n.DetermineComponentFrameRoot,"name",{value:"DetermineComponentFrameRoot"});var a=n.DetermineComponentFrameRoot(),i=a[0],l=a[1];if(i&&l){var s=i.split("\n"),c=l.split("\n");for(o=n=0;n<s.length&&!s[n].includes("DetermineComponentFrameRoot");)n++;for(;o<c.length&&!c[o].includes("DetermineComponentFrameRoot");)o++;if(n===s.length||o===c.length)for(n=s.length-1,o=c.length-1;1<=n&&0<=o&&s[n]!==c[o];)o--;for(;1<=n&&0<=o;n--,o--)if(s[n]!==c[o]){if(1!==n||1!==o)do if(n--,o--,0>o||s[n]!==c[o]){var u="\n"+s[n].replace(" at new "," at ");return e.displayName&&u.includes("<anonymous>")&&(u=u.replace("<anonymous>",e.displayName)),u}while(1<=n&&0<=o);break}}}finally{el=!1,Error.prepareStackTrace=r}return(r=e?e.displayName||e.name:"")?ei(r):""}function ec(e){try{var t="",r=null;do t+=function(e,t){switch(e.tag){case 26:case 27:case 5:return ei(e.type);case 16:return ei("Lazy");case 13:return e.child!==t&&null!==t?ei("Suspense Fallback"):ei("Suspense");case 19:return ei("SuspenseList");case 0:case 15:return es(e.type,!1);case 11:return es(e.type.render,!1);case 1:return es(e.type,!0);case 31:return ei("Activity");case 30:return ei("ViewTransition");default:return""}}(e,r),r=e,e=e.return;while(e);return t}catch(e){return"\nError generating stack: "+e.message+"\n"+e.stack}}var eu=Object.prototype.hasOwnProperty,ed=o.unstable_scheduleCallback,ef=o.unstable_cancelCallback,ep=o.unstable_shouldYield,eh=o.unstable_requestPaint,em=o.unstable_now,eg=o.unstable_getCurrentPriorityLevel,ev=o.unstable_ImmediatePriority,ey=o.unstable_UserBlockingPriority,eb=o.unstable_NormalPriority,ex=o.unstable_LowPriority,e_=o.unstable_IdlePriority,ew=o.log,ek=o.unstable_setDisableYieldValue,ej=null,eS=null;function eC(e){if("function"==typeof ew&&ek(e),eS&&"function"==typeof eS.setStrictMode)try{eS.setStrictMode(ej,e)}catch(e){}}var eE=Math.clz32?Math.clz32:function(e){return 0==(e>>>=0)?32:31-(eT(e)/eN|0)|0},eT=Math.log,eN=Math.LN2,eL=256,eI=262144,eP=4194304;function ez(e){var t=42&e;if(0!==t)return t;switch(e&-e){case 1:return 1;case 2:return 2;case 4:return 4;case 8:return 8;case 16:return 16;case 32:return 32;case 64:return 64;case 128:return 128;case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:return 261888&e;case 262144:case 524288:case 1048576:case 2097152:return 3932160&e;case 4194304:case 8388608:case 0x1000000:case 0x2000000:return 0x3c00000&e;case 0x4000000:return 0x4000000;case 0x8000000:return 0x8000000;case 0x10000000:return 0x10000000;case 0x20000000:return 0x20000000;case 0x40000000:return 0;default:return e}}function eR(e,t,r){var n=e.pendingLanes;if(0===n)return 0;var o=0,a=e.suspendedLanes,i=e.pingedLanes;e=e.warmLanes;var l=0x7ffffff&n;return 0!==l?0!=(n=l&~a)?o=ez(n):0!=(i&=l)?o=ez(i):r||0!=(r=l&~e)&&(o=ez(r)):0!=(l=n&~a)?o=ez(l):0!==i?o=ez(i):r||0!=(r=n&~e)&&(o=ez(r)),0===o?0:0!==t&&t!==o&&0==(t&a)&&((a=o&-o)>=(r=t&-t)||32===a&&0!=(4194048&r))?t:o}function eO(e,t){return 0==(e.pendingLanes&~(e.suspendedLanes&~e.pingedLanes)&t)}function eM(){var e=eP;return 0==(0x3c00000&(eP<<=1))&&(eP=4194304),e}function eA(e){for(var t=[],r=0;31>r;r++)t.push(e);return t}function eD(e,t){e.pendingLanes|=t,0x10000000!==t&&(e.suspendedLanes=0,e.pingedLanes=0,e.warmLanes=0)}function eZ(e,t,r){e.pendingLanes|=t,e.suspendedLanes&=~t;var n=31-eE(t);e.entangledLanes|=t,e.entanglements[n]=0x40000000|e.entanglements[n]|261930&r}function eF(e,t){var r=e.entangledLanes|=t;for(e=e.entanglements;r;){var n=31-eE(r),o=1<<n;o&t|e[n]&t&&(e[n]|=t),r&=~o}}function eU(e,t){var r=t&-t;return 0!=((r=0!=(42&r)?1:e$(r))&(e.suspendedLanes|t))?0:r}function e$(e){switch(e){case 2:e=1;break;case 8:e=4;break;case 32:e=16;break;case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:case 4194304:case 8388608:case 0x1000000:case 0x2000000:e=128;break;case 0x10000000:e=0x8000000;break;default:e=0}return e}function eH(e){return 2<(e&=-e)?8<e?0!=(0x7ffffff&e)?32:0x10000000:8:2}function eV(){var e=B.p;return 0!==e?e:void 0===(e=window.event)?32:dM(e.type)}function eB(e,t){var r=B.p;try{return B.p=e,t()}finally{B.p=r}}var eq=Math.random().toString(36).slice(2),eW="__reactFiber$"+eq,eK="__reactProps$"+eq,eY="__reactContainer$"+eq,eX="__reactEvents$"+eq,eG="__reactListeners$"+eq,eQ="__reactHandles$"+eq,eJ="__reactResources$"+eq,e0="__reactMarker$"+eq;function e1(e){delete e[eW],delete e[eK],delete e[eX],delete e[eG],delete e[eQ]}function e2(e){var t;if(t=e[eW])return t;for(var r=e.parentNode;r;){if(t=r[eY]||r[eW]){if(r=t.alternate,null!==t.child||null!==r&&null!==r.child)for(e=uQ(e);null!==e;){if(r=e[eW])return r;e=uQ(e)}return t}r=(e=r).parentNode}return null}function e3(e){if(e=e[eW]||e[eY]){var t=e.tag;if(5===t||6===t||13===t||31===t||26===t||27===t||3===t)return e}return null}function e4(e){var t=e.tag;if(5===t||26===t||27===t||6===t)return e.stateNode;throw Error(l(33))}function e5(e){var t=e[eJ];return t||(t=e[eJ]={hoistableStyles:new Map,hoistableScripts:new Map}),t}function e6(e){e[e0]=!0}var e9=new Set,e8={};function e7(e,t){te(e,t),te(e+"Capture",t)}function te(e,t){for(e8[e]=t,e=0;e<t.length;e++)e9.add(t[e])}var tt=RegExp("^[:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD][:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD\\-.0-9\\u00B7\\u0300-\\u036F\\u203F-\\u2040]*$"),tr={},tn={},to=!1;function ta(){var e=to;return to=!1,e}function ti(e,t,r){if(eu.call(tn,t)||!eu.call(tr,t)&&(tt.test(t)?tn[t]=!0:(tr[t]=!0,!1)))if(null===r)e.removeAttribute(t);else{switch(typeof r){case"undefined":case"function":case"symbol":e.removeAttribute(t);return;case"boolean":var n=t.toLowerCase().slice(0,5);if("data-"!==n&&"aria-"!==n)return void e.removeAttribute(t)}e.setAttribute(t,r)}}function tl(e,t,r){if(null===r)e.removeAttribute(t);else{switch(typeof r){case"undefined":case"function":case"symbol":case"boolean":e.removeAttribute(t);return}e.setAttribute(t,r)}}function ts(e,t,r,n){if(null===n)e.removeAttribute(r);else{switch(typeof n){case"undefined":case"function":case"symbol":case"boolean":e.removeAttribute(r);return}e.setAttributeNS(t,r,n)}}function tc(e){switch(typeof e){case"bigint":case"boolean":case"number":case"string":case"undefined":case"object":return e;default:return""}}function tu(e){var t=e.type;return(e=e.nodeName)&&"input"===e.toLowerCase()&&("checkbox"===t||"radio"===t)}function td(e){if(!e._valueTracker){var t=tu(e)?"checked":"value";e._valueTracker=function(e,t,r){var n=Object.getOwnPropertyDescriptor(e.constructor.prototype,t);if(!e.hasOwnProperty(t)&&void 0!==n&&"function"==typeof n.get&&"function"==typeof n.set){var o=n.get,a=n.set;return Object.defineProperty(e,t,{configurable:!0,get:function(){return o.call(this)},set:function(e){r=""+e,a.call(this,e)}}),Object.defineProperty(e,t,{enumerable:n.enumerable}),{getValue:function(){return r},setValue:function(e){r=""+e},stopTracking:function(){e._valueTracker=null,delete e[t]}}}}(e,t,""+e[t])}}function tf(e){if(!e)return!1;var t=e._valueTracker;if(!t)return!0;var r=t.getValue(),n="";return e&&(n=tu(e)?e.checked?"true":"false":e.value),(e=n)!==r&&(t.setValue(e),!0)}function tp(e){if(void 0===(e=e||("undefined"!=typeof document?document:void 0)))return null;try{return e.activeElement||e.body}catch(t){return e.body}}var th=/[\n"\\]/g;function tm(e){return e.replace(th,function(e){return"\\"+e.charCodeAt(0).toString(16)+" "})}function tg(e,t,r,n,o,a,i,l){e.name="",null!=i&&"function"!=typeof i&&"symbol"!=typeof i&&"boolean"!=typeof i?e.type=i:e.removeAttribute("type"),null!=t?"number"===i?(0===t&&""===e.value||e.value!=t)&&(e.value=""+tc(t)):e.value!==""+tc(t)&&(e.value=""+tc(t)):"submit"!==i&&"reset"!==i||e.removeAttribute("value"),null!=t?ty(e,i,tc(t)):null!=r?ty(e,i,tc(r)):null!=n&&e.removeAttribute("value"),null==o&&null!=a&&(e.defaultChecked=!!a),null!=o&&(e.checked=o&&"function"!=typeof o&&"symbol"!=typeof o),null!=l&&"function"!=typeof l&&"symbol"!=typeof l&&"boolean"!=typeof l?e.name=""+tc(l):e.removeAttribute("name")}function tv(e,t,r,n,o,a,i,l){if(null!=a&&"function"!=typeof a&&"symbol"!=typeof a&&"boolean"!=typeof a&&(e.type=a),null!=t||null!=r){if(("submit"===a||"reset"===a)&&null==t)return void td(e);r=null!=r?""+tc(r):"",t=null!=t?""+tc(t):r,l||t===e.value||(e.value=t),e.defaultValue=t}n="function"!=typeof(n=null!=n?n:o)&&"symbol"!=typeof n&&!!n,e.checked=l?e.checked:!!n,e.defaultChecked=!!n,null!=i&&"function"!=typeof i&&"symbol"!=typeof i&&"boolean"!=typeof i&&(e.name=i),td(e)}function ty(e,t,r){"number"===t&&tp(e.ownerDocument)===e||e.defaultValue===""+r||(e.defaultValue=""+r)}function tb(e,t,r,n){if(e=e.options,t){t={};for(var o=0;o<r.length;o++)t["$"+r[o]]=!0;for(r=0;r<e.length;r++)o=t.hasOwnProperty("$"+e[r].value),e[r].selected!==o&&(e[r].selected=o),o&&n&&(e[r].defaultSelected=!0)}else{for(o=0,r=""+tc(r),t=null;o<e.length;o++){if(e[o].value===r){e[o].selected=!0,n&&(e[o].defaultSelected=!0);return}null!==t||e[o].disabled||(t=e[o])}null!==t&&(t.selected=!0)}}function tx(e,t,r){if(null!=t&&((t=""+tc(t))!==e.value&&(e.value=t),null==r)){e.defaultValue!==t&&(e.defaultValue=t);return}e.defaultValue=null!=r?""+tc(r):""}function t_(e,t,r,n){if(null==t){if(null!=n){if(null!=r)throw Error(l(92));if(H(n)){if(1<n.length)throw Error(l(93));n=n[0]}r=n}null==r&&(r=""),t=r}e.defaultValue=r=tc(t),(n=e.textContent)===r&&""!==n&&null!==n&&(e.value=n),td(e)}function tw(e,t){if(t){var r=e.firstChild;if(r&&r===e.lastChild&&3===r.nodeType){r.nodeValue=t;return}}e.textContent=t}var tk=new Set("animationIterationCount aspectRatio borderImageOutset borderImageSlice borderImageWidth boxFlex boxFlexGroup boxOrdinalGroup columnCount columns flex flexGrow flexPositive flexShrink flexNegative flexOrder gridArea gridRow gridRowEnd gridRowSpan gridRowStart gridColumn gridColumnEnd gridColumnSpan gridColumnStart fontWeight lineClamp lineHeight opacity order orphans scale tabSize widows zIndex zoom fillOpacity floodOpacity stopOpacity strokeDasharray strokeDashoffset strokeMiterlimit strokeOpacity strokeWidth MozAnimationIterationCount MozBoxFlex MozBoxFlexGroup MozLineClamp msAnimationIterationCount msFlex msZoom msFlexGrow msFlexNegative msFlexOrder msFlexPositive msFlexShrink msGridColumn msGridColumnSpan msGridRow msGridRowSpan WebkitAnimationIterationCount WebkitBoxFlex WebKitBoxFlexGroup WebkitBoxOrdinalGroup WebkitColumnCount WebkitColumns WebkitFlex WebkitFlexGrow WebkitFlexPositive WebkitFlexShrink WebkitLineClamp".split(" "));function tj(e,t,r){var n=0===t.indexOf("--");null==r||"boolean"==typeof r||""===r?n?e.setProperty(t,""):"float"===t?e.cssFloat="":e[t]="":n?e.setProperty(t,r):"number"!=typeof r||0===r||tk.has(t)?"float"===t?e.cssFloat=r:e[t]=(""+r).trim():e[t]=r+"px"}function tS(e,t,r){if(null!=t&&"object"!=typeof t)throw Error(l(62));if(e=e.style,null!=r){for(var n in r)!r.hasOwnProperty(n)||null!=t&&t.hasOwnProperty(n)||(0===n.indexOf("--")?e.setProperty(n,""):"float"===n?e.cssFloat="":e[n]="",to=!0);for(var o in t)n=t[o],t.hasOwnProperty(o)&&r[o]!==n&&(tj(e,o,n),to=!0)}else for(var a in t)t.hasOwnProperty(a)&&tj(e,a,t[a])}function tC(e){if(-1===e.indexOf("-"))return!1;switch(e){case"annotation-xml":case"color-profile":case"font-face":case"font-face-src":case"font-face-uri":case"font-face-format":case"font-face-name":case"missing-glyph":return!1;default:return!0}}var tE=new Map([["acceptCharset","accept-charset"],["htmlFor","for"],["httpEquiv","http-equiv"],["crossOrigin","crossorigin"],["accentHeight","accent-height"],["alignmentBaseline","alignment-baseline"],["arabicForm","arabic-form"],["baselineShift","baseline-shift"],["capHeight","cap-height"],["clipPath","clip-path"],["clipRule","clip-rule"],["colorInterpolation","color-interpolation"],["colorInterpolationFilters","color-interpolation-filters"],["colorProfile","color-profile"],["colorRendering","color-rendering"],["dominantBaseline","dominant-baseline"],["enableBackground","enable-background"],["fillOpacity","fill-opacity"],["fillRule","fill-rule"],["floodColor","flood-color"],["floodOpacity","flood-opacity"],["fontFamily","font-family"],["fontSize","font-size"],["fontSizeAdjust","font-size-adjust"],["fontStretch","font-stretch"],["fontStyle","font-style"],["fontVariant","font-variant"],["fontWeight","font-weight"],["glyphName","glyph-name"],["glyphOrientationHorizontal","glyph-orientation-horizontal"],["glyphOrientationVertical","glyph-orientation-vertical"],["horizAdvX","horiz-adv-x"],["horizOriginX","horiz-origin-x"],["imageRendering","image-rendering"],["letterSpacing","letter-spacing"],["lightingColor","lighting-color"],["markerEnd","marker-end"],["markerMid","marker-mid"],["markerStart","marker-start"],["maskType","mask-type"],["overlinePosition","overline-position"],["overlineThickness","overline-thickness"],["paintOrder","paint-order"],["panose-1","panose-1"],["pointerEvents","pointer-events"],["renderingIntent","rendering-intent"],["shapeRendering","shape-rendering"],["stopColor","stop-color"],["stopOpacity","stop-opacity"],["strikethroughPosition","strikethrough-position"],["strikethroughThickness","strikethrough-thickness"],["strokeDasharray","stroke-dasharray"],["strokeDashoffset","stroke-dashoffset"],["strokeLinecap","stroke-linecap"],["strokeLinejoin","stroke-linejoin"],["strokeMiterlimit","stroke-miterlimit"],["strokeOpacity","stroke-opacity"],["strokeWidth","stroke-width"],["textAnchor","text-anchor"],["textDecoration","text-decoration"],["textRendering","text-rendering"],["transformOrigin","transform-origin"],["underlinePosition","underline-position"],["underlineThickness","underline-thickness"],["unicodeBidi","unicode-bidi"],["unicodeRange","unicode-range"],["unitsPerEm","units-per-em"],["vAlphabetic","v-alphabetic"],["vHanging","v-hanging"],["vIdeographic","v-ideographic"],["vMathematical","v-mathematical"],["vectorEffect","vector-effect"],["vertAdvY","vert-adv-y"],["vertOriginX","vert-origin-x"],["vertOriginY","vert-origin-y"],["wordSpacing","word-spacing"],["writingMode","writing-mode"],["xmlnsXlink","xmlns:xlink"],["xHeight","x-height"]]),tT=/^[\u0000-\u001F ]*j[\r\n\t]*a[\r\n\t]*v[\r\n\t]*a[\r\n\t]*s[\r\n\t]*c[\r\n\t]*r[\r\n\t]*i[\r\n\t]*p[\r\n\t]*t[\r\n\t]*:/i;function tN(e){return tT.test(""+e)?"javascript:throw new Error('React has blocked a javascript: URL as a security precaution.')":e}function tL(){}var tI=null;function tP(e){return(e=e.target||e.srcElement||window).correspondingUseElement&&(e=e.correspondingUseElement),3===e.nodeType?e.parentNode:e}var tz=null,tR=null;function tO(e){var t=e3(e);if(t&&(e=t.stateNode)){var r=e[eK]||null;switch(e=t.stateNode,t.type){case"input":if(tg(e,r.value,r.defaultValue,r.defaultValue,r.checked,r.defaultChecked,r.type,r.name),t=r.name,"radio"===r.type&&null!=t){for(r=e;r.parentNode;)r=r.parentNode;for(r=r.querySelectorAll('input[name="'+tm(""+t)+'"][type="radio"]'),t=0;t<r.length;t++){var n=r[t];if(n!==e&&n.form===e.form){var o=n[eK]||null;if(!o)throw Error(l(90));tg(n,o.value,o.defaultValue,o.defaultValue,o.checked,o.defaultChecked,o.type,o.name)}}for(t=0;t<r.length;t++)(n=r[t]).form===e.form&&tf(n)}break;case"textarea":tx(e,r.value,r.defaultValue);break;case"select":null!=(t=r.value)&&tb(e,!!r.multiple,t,!1)}}}var tM=!1;function tA(e,t,r){if(tM)return e(t,r);tM=!0;try{return e(t)}finally{if(tM=!1,(null!==tz||null!==tR)&&(co(),tz&&(t=tz,e=tR,tR=tz=null,tO(t),e)))for(t=0;t<e.length;t++)tO(e[t])}}function tD(e,t){var r=e.stateNode;if(null===r)return null;var n=r[eK]||null;if(null===n)return null;switch(r=n[t],t){case"onClick":case"onClickCapture":case"onDoubleClick":case"onDoubleClickCapture":case"onMouseDown":case"onMouseDownCapture":case"onMouseMove":case"onMouseMoveCapture":case"onMouseUp":case"onMouseUpCapture":case"onMouseEnter":(n=!n.disabled)||(n="button"!==(e=e.type)&&"input"!==e&&"select"!==e&&"textarea"!==e),e=!n;break;default:e=!1}if(e)return null;if(r&&"function"!=typeof r)throw Error(l(231,t,typeof r));return r}var tZ="undefined"!=typeof window&&void 0!==window.document&&void 0!==window.document.createElement,tF=!1;if(tZ)try{var tU={};Object.defineProperty(tU,"passive",{get:function(){tF=!0}}),window.addEventListener("test",tU,tU),window.removeEventListener("test",tU,tU)}catch(e){tF=!1}var t$=null,tH=null,tV=null;function tB(){if(tV)return tV;var e,t,r=tH,n=r.length,o="value"in t$?t$.value:t$.textContent,a=o.length;for(e=0;e<n&&r[e]===o[e];e++);var i=n-e;for(t=1;t<=i&&r[n-t]===o[a-t];t++);return tV=o.slice(e,1<t?1-t:void 0)}function tq(e){var t=e.keyCode;return"charCode"in e?0===(e=e.charCode)&&13===t&&(e=13):e=t,10===e&&(e=13),32<=e||13===e?e:0}function tW(){return!0}function tK(){return!1}function tY(e){function t(t,r,n,o,a){for(var i in this._reactName=t,this._targetInst=n,this.type=r,this.nativeEvent=o,this.target=a,this.currentTarget=null,e)e.hasOwnProperty(i)&&(t=e[i],this[i]=t?t(o):o[i]);return this.isDefaultPrevented=(null!=o.defaultPrevented?o.defaultPrevented:!1===o.returnValue)?tW:tK,this.isPropagationStopped=tK,this}return w(t.prototype,{preventDefault:function(){this.defaultPrevented=!0;var e=this.nativeEvent;e&&(e.preventDefault?e.preventDefault():"unknown"!=typeof e.returnValue&&(e.returnValue=!1),this.isDefaultPrevented=tW)},stopPropagation:function(){var e=this.nativeEvent;e&&(e.stopPropagation?e.stopPropagation():"unknown"!=typeof e.cancelBubble&&(e.cancelBubble=!0),this.isPropagationStopped=tW)},persist:function(){},isPersistent:tW}),t}var tX,tG,tQ,tJ,t0,t1={eventPhase:0,bubbles:0,cancelable:0,timeStamp:function(e){return e.timeStamp||Date.now()},defaultPrevented:0,isTrusted:0},t2=tY(t1),t3=w({},t1,{view:0,detail:0}),t4=tY(t3),t5=w({},t3,{screenX:0,screenY:0,clientX:0,clientY:0,pageX:0,pageY:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,getModifierState:ri,button:0,buttons:0,relatedTarget:function(e){return void 0===e.relatedTarget?e.fromElement===e.srcElement?e.toElement:e.fromElement:e.relatedTarget},movementX:function(e){return"movementX"in e?e.movementX:(e!==t0&&(t0&&"mousemove"===e.type?(tQ=e.screenX-t0.screenX,tJ=e.screenY-t0.screenY):tJ=tQ=0,t0=e),tQ)},movementY:function(e){return"movementY"in e?e.movementY:tJ}}),t6=tY(t5),t9=tY(w({},t5,{dataTransfer:0})),t8=tY(w({},t3,{relatedTarget:0})),t7=tY(w({},t1,{animationName:0,elapsedTime:0,pseudoElement:0})),re=tY(w({},t1,{clipboardData:function(e){return"clipboardData"in e?e.clipboardData:window.clipboardData}})),rt=tY(w({},t1,{data:0})),rr={Esc:"Escape",Spacebar:" ",Left:"ArrowLeft",Up:"ArrowUp",Right:"ArrowRight",Down:"ArrowDown",Del:"Delete",Win:"OS",Menu:"ContextMenu",Apps:"ContextMenu",Scroll:"ScrollLock",MozPrintableKey:"Unidentified"},rn={8:"Backspace",9:"Tab",12:"Clear",13:"Enter",16:"Shift",17:"Control",18:"Alt",19:"Pause",20:"CapsLock",27:"Escape",32:" ",33:"PageUp",34:"PageDown",35:"End",36:"Home",37:"ArrowLeft",38:"ArrowUp",39:"ArrowRight",40:"ArrowDown",45:"Insert",46:"Delete",112:"F1",113:"F2",114:"F3",115:"F4",116:"F5",117:"F6",118:"F7",119:"F8",120:"F9",121:"F10",122:"F11",123:"F12",144:"NumLock",145:"ScrollLock",224:"Meta"},ro={Alt:"altKey",Control:"ctrlKey",Meta:"metaKey",Shift:"shiftKey"};function ra(e){var t=this.nativeEvent;return t.getModifierState?t.getModifierState(e):!!(e=ro[e])&&!!t[e]}function ri(){return ra}var rl=tY(w({},t3,{key:function(e){if(e.key){var t=rr[e.key]||e.key;if("Unidentified"!==t)return t}return"keypress"===e.type?13===(e=tq(e))?"Enter":String.fromCharCode(e):"keydown"===e.type||"keyup"===e.type?rn[e.keyCode]||"Unidentified":""},code:0,location:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,repeat:0,locale:0,getModifierState:ri,charCode:function(e){return"keypress"===e.type?tq(e):0},keyCode:function(e){return"keydown"===e.type||"keyup"===e.type?e.keyCode:0},which:function(e){return"keypress"===e.type?tq(e):"keydown"===e.type||"keyup"===e.type?e.keyCode:0}})),rs=tY(w({},t5,{pointerId:0,width:0,height:0,pressure:0,tangentialPressure:0,tiltX:0,tiltY:0,twist:0,pointerType:0,isPrimary:0})),rc=tY(w({},t1,{submitter:0})),ru=tY(w({},t3,{touches:0,targetTouches:0,changedTouches:0,altKey:0,metaKey:0,ctrlKey:0,shiftKey:0,getModifierState:ri})),rd=tY(w({},t1,{propertyName:0,elapsedTime:0,pseudoElement:0})),rf=tY(w({},t5,{deltaX:function(e){return"deltaX"in e?e.deltaX:"wheelDeltaX"in e?-e.wheelDeltaX:0},deltaY:function(e){return"deltaY"in e?e.deltaY:"wheelDeltaY"in e?-e.wheelDeltaY:"wheelDelta"in e?-e.wheelDelta:0},deltaZ:0,deltaMode:0})),rp=tY(w({},t1,{newState:0,oldState:0})),rh=[9,13,27,32],rm=tZ&&"CompositionEvent"in window,rg=null;tZ&&"documentMode"in document&&(rg=document.documentMode);var rv=tZ&&"TextEvent"in window&&!rg,ry=tZ&&(!rm||rg&&8<rg&&11>=rg),rb=!1;function rx(e,t){switch(e){case"keyup":return -1!==rh.indexOf(t.keyCode);case"keydown":return 229!==t.keyCode;case"keypress":case"mousedown":case"focusout":return!0;default:return!1}}function r_(e){return"object"==typeof(e=e.detail)&&"data"in e?e.data:null}var rw=!1,rk={color:!0,date:!0,datetime:!0,"datetime-local":!0,email:!0,month:!0,number:!0,password:!0,range:!0,search:!0,tel:!0,text:!0,time:!0,url:!0,week:!0};function rj(e){var t=e&&e.nodeName&&e.nodeName.toLowerCase();return"input"===t?!!rk[e.type]:"textarea"===t}function rS(e,t,r,n){tz?tR?tR.push(n):tR=[n]:tz=n,0<(t=c9(t,"onChange")).length&&(r=new t2("onChange","change",null,r,n),e.push({event:r,listeners:t}))}var rC=null,rE=null;function rT(e){cJ(e,0)}function rN(e){if(tf(e4(e)))return e}function rL(e,t){if("change"===e)return t}var rI=!1;if(tZ){if(tZ){var rP="oninput"in document;if(!rP){var rz=document.createElement("div");rz.setAttribute("oninput","return;"),rP="function"==typeof rz.oninput}n=rP}else n=!1;rI=n&&(!document.documentMode||9<document.documentMode)}function rR(){rC&&(rC.detachEvent("onpropertychange",rO),rE=rC=null)}function rO(e){if("value"===e.propertyName&&rN(rE)){var t=[];rS(t,rE,e,tP(e)),tA(rT,t)}}function rM(e,t,r){"focusin"===e?(rR(),rC=t,rE=r,rC.attachEvent("onpropertychange",rO)):"focusout"===e&&rR()}function rA(e){if("selectionchange"===e||"keyup"===e||"keydown"===e)return rN(rE)}function rD(e,t){if("click"===e)return rN(t)}function rZ(e,t){if("input"===e||"change"===e)return rN(t)}var rF="function"==typeof Object.is?Object.is:function(e,t){return e===t&&(0!==e||1/e==1/t)||e!=e&&t!=t};function rU(e,t){if(rF(e,t))return!0;if("object"!=typeof e||null===e||"object"!=typeof t||null===t)return!1;var r=Object.keys(e),n=Object.keys(t);if(r.length!==n.length)return!1;for(n=0;n<r.length;n++){var o=r[n];if(!eu.call(t,o)||!rF(e[o],t[o]))return!1}return!0}function r$(e){for(;e&&e.firstChild;)e=e.firstChild;return e}function rH(e,t){var r,n=r$(e);for(e=0;n;){if(3===n.nodeType){if(r=e+n.textContent.length,e<=t&&r>=t)return{node:n,offset:t-e};e=r}e:{for(;n;){if(n.nextSibling){n=n.nextSibling;break e}n=n.parentNode}n=void 0}n=r$(n)}}function rV(e){e=null!=e&&null!=e.ownerDocument&&null!=e.ownerDocument.defaultView?e.ownerDocument.defaultView:window;for(var t=tp(e.document);t instanceof e.HTMLIFrameElement;){try{var r="string"==typeof t.contentWindow.location.href}catch(e){r=!1}if(r)e=t.contentWindow;else break;t=tp(e.document)}return t}function rB(e){var t=e&&e.nodeName&&e.nodeName.toLowerCase();return t&&("input"===t&&("text"===e.type||"search"===e.type||"tel"===e.type||"url"===e.type||"password"===e.type)||"textarea"===t||"true"===e.contentEditable)}var rq=tZ&&"documentMode"in document&&11>=document.documentMode,rW=null,rK=null,rY=null,rX=!1;function rG(e,t,r){var n=r.window===r?r.document:9===r.nodeType?r:r.ownerDocument;rX||null==rW||rW!==tp(n)||(n="selectionStart"in(n=rW)&&rB(n)?{start:n.selectionStart,end:n.selectionEnd}:{anchorNode:(n=(n.ownerDocument&&n.ownerDocument.defaultView||window).getSelection()).anchorNode,anchorOffset:n.anchorOffset,focusNode:n.focusNode,focusOffset:n.focusOffset},rY&&rU(rY,n)||(rY=n,0<(n=c9(rK,"onSelect")).length&&(t=new t2("onSelect","select",null,t,r),e.push({event:t,listeners:n}),t.target=rW)))}function rQ(e,t){var r={};return r[e.toLowerCase()]=t.toLowerCase(),r["Webkit"+e]="webkit"+t,r["Moz"+e]="moz"+t,r}var rJ={animationend:rQ("Animation","AnimationEnd"),animationiteration:rQ("Animation","AnimationIteration"),animationstart:rQ("Animation","AnimationStart"),transitionrun:rQ("Transition","TransitionRun"),transitionstart:rQ("Transition","TransitionStart"),transitioncancel:rQ("Transition","TransitionCancel"),transitionend:rQ("Transition","TransitionEnd")},r0={},r1={};function r2(e){if(r0[e])return r0[e];if(!rJ[e])return e;var t,r=rJ[e];for(t in r)if(r.hasOwnProperty(t)&&t in r1)return r0[e]=r[t];return e}tZ&&(r1=document.createElement("div").style,"AnimationEvent"in window||(delete rJ.animationend.animation,delete rJ.animationiteration.animation,delete rJ.animationstart.animation),"TransitionEvent"in window||delete rJ.transitionend.transition);var r3=r2("animationend"),r4=r2("animationiteration"),r5=r2("animationstart"),r6=r2("transitionrun"),r9=r2("transitionstart"),r8=r2("transitioncancel"),r7=r2("transitionend"),ne=new Map,nt="abort auxClick beforeToggle cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error fullscreenChange fullscreenError gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");function nr(e,t){ne.set(e,t),e7(t,[e])}nt.push("scrollEnd");var nn=0;function no(e,t){return null!=e.name&&"auto"!==e.name?e.name:null!==t.autoName?t.autoName:t.autoName=e="_"+(e=sX.identifierPrefix)+"t_"+(nn++).toString(32)+"_"}function na(e){if(null==e||"string"==typeof e)return e;var t=null,r=s4;if(null!==r)for(var n=0;n<r.length;n++){var o=e[r[n]];if(null!=o){if("none"===o)return"none";t=null==t?o:t+" "+o}}return null==t?e.default:t}function ni(e,t){return e=na(e),null==(t=na(t))?"auto"===e?null:e:"auto"===t?null:t}var nl="function"==typeof reportError?reportError:function(e){if("object"==typeof window&&"function"==typeof window.ErrorEvent){var t=new window.ErrorEvent("error",{bubbles:!0,cancelable:!0,message:"object"==typeof e&&null!==e&&"string"==typeof e.message?String(e.message):String(e),error:e});if(!window.dispatchEvent(t))return}else if("object"==typeof process&&"function"==typeof process.emit)return void process.emit("uncaughtException",e);console.error(e)},ns=[],nc=0,nu=0;function nd(){for(var e=nc,t=nu=nc=0;t<e;){var r=ns[t];ns[t++]=null;var n=ns[t];ns[t++]=null;var o=ns[t];ns[t++]=null;var a=ns[t];if(ns[t++]=null,null!==n&&null!==o){var i=n.pending;null===i?o.next=o:(o.next=i.next,i.next=o),n.pending=o}0!==a&&nm(r,o,a)}}function nf(e,t,r,n){ns[nc++]=e,ns[nc++]=t,ns[nc++]=r,ns[nc++]=n,nu|=n,e.lanes|=n,null!==(e=e.alternate)&&(e.lanes|=n)}function np(e,t,r,n){return nf(e,t,r,n),ng(e)}function nh(e,t){return nf(e,null,null,t),ng(e)}function nm(e,t,r){e.lanes|=r;var n=e.alternate;null!==n&&(n.lanes|=r);for(var o=!1,a=e.return;null!==a;)a.childLanes|=r,null!==(n=a.alternate)&&(n.childLanes|=r),22===a.tag&&(null===(e=a.stateNode)||1&e._visibility||(o=!0)),e=a,a=a.return;return 3===e.tag?(a=e.stateNode,o&&null!==t&&(o=31-eE(r),null===(n=(e=a.hiddenUpdates)[o])?e[o]=[t]:n.push(t),t.lane=0x20000000|r),a):null}function ng(e){if(50<s5)throw s5=0,s6=null,Error(l(185));for(var t=e.return;null!==t;)t=(e=t).return;return 3===e.tag?e.stateNode:null}var nv={};function ny(e,t,r,n){this.tag=e,this.key=r,this.sibling=this.child=this.return=this.stateNode=this.type=this.elementType=null,this.index=0,this.refCleanup=this.ref=null,this.pendingProps=t,this.dependencies=this.memoizedState=this.updateQueue=this.memoizedProps=null,this.mode=n,this.subtreeFlags=this.flags=0,this.deletions=null,this.childLanes=this.lanes=0,this.alternate=null}function nb(e,t,r,n){return new ny(e,t,r,n)}function nx(e){return!(!(e=e.prototype)||!e.isReactComponent)}function n_(e,t){var r=e.alternate;return null===r?((r=nb(e.tag,t,e.key,e.mode)).elementType=e.elementType,r.type=e.type,r.stateNode=e.stateNode,r.alternate=e,e.alternate=r):(r.pendingProps=t,r.type=e.type,r.flags=0,r.subtreeFlags=0,r.deletions=null),r.flags=0x7f00000&e.flags,r.childLanes=e.childLanes,r.lanes=e.lanes,r.child=e.child,r.memoizedProps=e.memoizedProps,r.memoizedState=e.memoizedState,r.updateQueue=e.updateQueue,t=e.dependencies,r.dependencies=null===t?null:{lanes:t.lanes,firstContext:t.firstContext},r.sibling=e.sibling,r.index=e.index,r.ref=e.ref,r.refCleanup=e.refCleanup,r}function nw(e,t){e.flags&=0x7f00002;var r=e.alternate;return null===r?(e.childLanes=0,e.lanes=t,e.child=null,e.subtreeFlags=0,e.memoizedProps=null,e.memoizedState=null,e.updateQueue=null,e.dependencies=null,e.stateNode=null):(e.childLanes=r.childLanes,e.lanes=r.lanes,e.child=r.child,e.subtreeFlags=0,e.deletions=null,e.memoizedProps=r.memoizedProps,e.memoizedState=r.memoizedState,e.updateQueue=r.updateQueue,e.type=r.type,e.dependencies=null===(t=r.dependencies)?null:{lanes:t.lanes,firstContext:t.firstContext}),e}function nk(e,t,r,n,o,a){var i=0;if(n=e,"function"==typeof e)nx(e)&&(i=1);else if("string"==typeof e)i=!function(e,t,r){if(1===r||null!=t.itemProp)return!1;switch(e){case"meta":case"title":return!0;case"style":if("string"!=typeof t.precedence||"string"!=typeof t.href||""===t.href)break;return!0;case"link":if("string"!=typeof t.rel||"string"!=typeof t.href||""===t.href||t.onLoad||t.onError)break;if("stylesheet"===t.rel)return e=t.disabled,"string"==typeof t.precedence&&null==e;return!0;case"script":if(t.async&&"function"!=typeof t.async&&"symbol"!=typeof t.async&&!t.onLoad&&!t.onError&&t.src&&"string"==typeof t.src)return!0}return!1}(e,r,Q.current)?"html"===e||"head"===e||"body"===e?27:5:26;else e:switch(e){case M:return(e=nb(31,r,t,o)).elementType=M,e.lanes=a,e;case C:return nj(r.children,o,a,t);case E:i=8,o|=24;break;case T:return(e=nb(12,r,t,2|o)).elementType=T,e.lanes=a,e;case P:return(e=nb(13,r,t,o)).elementType=P,e.lanes=a,e;case z:return(e=nb(19,r,t,o)).elementType=z,e.lanes=a,e;case A:case Z:return(e=nb(30,r,t,e=32|o)).elementType=Z,e.lanes=a,e.stateNode={autoName:null,paired:null,clones:null,ref:null},e;default:if("object"==typeof e&&null!==e)switch(e.$$typeof){case L:i=10;break e;case N:i=9;break e;case I:i=11;break e;case R:i=14;break e;case O:i=16,n=null;break e}i=29,r=Error(l(130,null===e?"null":typeof e,"")),n=null}return(t=nb(i,r,t,o)).elementType=e,t.type=n,t.lanes=a,t}function nj(e,t,r,n){return(e=nb(7,e,n,t)).lanes=r,e}function nS(e,t,r){return(e=nb(6,e,null,t)).lanes=r,e}function nC(e){var t=nb(18,null,null,0);return t.stateNode=e,t}function nE(e,t,r){return(t=nb(4,null!==e.children?e.children:[],e.key,t)).lanes=r,t.stateNode={containerInfo:e.containerInfo,pendingChildren:null,implementation:e.implementation},t}var nT=new WeakMap;function nN(e,t){if("object"==typeof e&&null!==e){var r=nT.get(e);return void 0!==r?r:(t={value:e,source:t,stack:ec(t)},nT.set(e,t),t)}return{value:e,source:t,stack:ec(t)}}var nL=[],nI=0,nP=null,nz=0,nR=[],nO=0,nM=null,nA=1,nD="";function nZ(e,t){nL[nI++]=nz,nL[nI++]=nP,nP=e,nz=t}function nF(e,t,r){nR[nO++]=nA,nR[nO++]=nD,nR[nO++]=nM,nM=e;var n=nA;e=nD;var o=32-eE(n)-1;n&=~(1<<o),r+=1;var a=32-eE(t)+o;if(30<a){var i=o-o%5;a=(n&(1<<i)-1).toString(32),n>>=i,o-=i,nA=1<<32-eE(t)+o|r<<o|n,nD=a+e}else nA=1<<a|r<<o|n,nD=e}function nU(e){null!==e.return&&(nZ(e,1),nF(e,1,0))}function n$(e){for(;e===nP;)nP=nL[--nI],nL[nI]=null,nz=nL[--nI],nL[nI]=null;for(;e===nM;)nM=nR[--nO],nR[nO]=null,nD=nR[--nO],nR[nO]=null,nA=nR[--nO],nR[nO]=null}function nH(e,t){nR[nO++]=nA,nR[nO++]=nD,nR[nO++]=nM,nA=t.id,nD=t.overflow,nM=e}var nV=null,nB=null,nq=!1,nW=null,nK=!1,nY=Error(l(519));function nX(e){var t=Error(l(418,1<arguments.length&&void 0!==arguments[1]&&arguments[1]?"text":"HTML",""));throw n2(nN(t,e)),nY}function nG(e){var t=e.stateNode,r=e.type,n=e.memoizedProps;switch(t[eW]=e,t[eK]=n,r){case"dialog":c0("cancel",t),c0("close",t);break;case"iframe":case"object":case"embed":c0("load",t);break;case"video":case"audio":for(r=0;r<cG.length;r++)c0(cG[r],t);break;case"source":c0("error",t);break;case"img":case"image":case"link":c0("error",t),c0("load",t);break;case"details":c0("toggle",t);break;case"input":c0("invalid",t),tv(t,n.value,n.defaultValue,n.checked,n.defaultChecked,n.type,n.name,!0);break;case"select":c0("invalid",t);break;case"textarea":c0("invalid",t),t_(t,n.value,n.defaultValue,n.children)}"string"!=typeof(r=n.children)&&"number"!=typeof r&&"bigint"!=typeof r||t.textContent===""+r||!0===n.suppressHydrationWarning||un(t.textContent,r)?(null!=n.popover&&(c0("beforetoggle",t),c0("toggle",t)),null!=n.onScroll&&c0("scroll",t),null!=n.onScrollEnd&&c0("scrollend",t),null!=n.onClick&&(t.onclick=tL),t=!0):t=!1,t||nX(e,!0)}function nQ(e){for(nV=e.return;nV;)switch(nV.tag){case 5:case 31:case 13:nK=!1;return;case 27:case 3:nK=!0;return;default:nV=nV.return}}function nJ(e){if(e!==nV)return!1;if(!nq)return nQ(e),nq=!0,!1;var t,r=e.tag;if((t=3!==r&&27!==r)&&((t=5===r)&&(t="form"===(t=e.type)||"button"===t||up(e.type,e.memoizedProps)),t=!t),t&&nB&&nX(e),nQ(e),13===r){if(!(e=null!==(e=e.memoizedState)?e.dehydrated:null))throw Error(l(317));nB=uG(e)}else if(31===r){if(!(e=null!==(e=e.memoizedState)?e.dehydrated:null))throw Error(l(317));nB=uG(e)}else 27===r?(r=nB,ux(e.type)?(e=uX,uX=null,nB=e):nB=r):nB=nV?uY(e.stateNode.nextSibling):null;return!0}function n0(){nB=nV=null,nq=!1}function n1(){var e=nW;return null!==e&&(null===s$?s$=e:s$.push.apply(s$,e),nW=null),e}function n2(e){null===nW?nW=[e]:nW.push(e)}var n3=Y(null),n4=null,n5=null;function n6(e,t,r){G(n3,t._currentValue),t._currentValue=r}function n9(e){e._currentValue=n3.current,X(n3)}function n8(e,t,r){for(;null!==e;){var n=e.alternate;if((e.childLanes&t)!==t?(e.childLanes|=t,null!==n&&(n.childLanes|=t)):null!==n&&(n.childLanes&t)!==t&&(n.childLanes|=t),e===r)break;e=e.return}}function n7(e,t,r,n){var o=e.child;for(null!==o&&(o.return=e);null!==o;){var a=o.dependencies;if(null!==a){var i=o.child;a=a.firstContext;e:for(;null!==a;){var s=a;a=o;for(var c=0;c<t.length;c++)if(s.context===t[c]){a.lanes|=r,null!==(s=a.alternate)&&(s.lanes|=r),n8(a.return,r,e),n||(i=null);break e}a=s.next}}else if(18===o.tag){if(null===(i=o.return))throw Error(l(341));i.lanes|=r,null!==(a=i.alternate)&&(a.lanes|=r),n8(i,r,e),i=null}else 13===o.tag&&null!==o.memoizedState&&null===o.memoizedState.dehydrated?(o.lanes|=r,null!==(i=o.alternate)&&(i.lanes|=r),n8(o.return,r,e),i=n?o.child:null):i=o.child;if(null!==i)i.return=o;else for(i=o;null!==i;){if(i===e){i=null;break}if(null!==(o=i.sibling)){o.return=i.return,i=o;break}i=i.return}o=i}}function oe(e,t,r,n){e=null;for(var o=t,a=!1;null!==o;){if(!a){if(0!=(524288&o.flags))a=!0;else if(0!=(262144&o.flags))break}if(10===o.tag){var i=o.alternate;if(null===i)throw Error(l(387));if(null!==(i=i.memoizedProps)){var s=o.type;rF(o.pendingProps.value,i.value)||(null!==e?e.push(s):e=[s])}}else if(o===et.current){if(null===(i=o.alternate))throw Error(l(387));i.memoizedState.memoizedState!==o.memoizedState.memoizedState&&(null!==e?e.push(dw):e=[dw])}o=o.return}return null!==e&&n7(t,e,r,n),t.flags|=262144,null!==e}function ot(e){for(e=e.firstContext;null!==e;){if(!rF(e.context._currentValue,e.memoizedValue))return!0;e=e.next}return!1}function or(e){n4=e,n5=null,null!==(e=e.dependencies)&&(e.firstContext=null)}function on(e){return oa(n4,e)}function oo(e,t){return null===n4&&or(e),oa(e,t)}function oa(e,t){var r=t._currentValue;if(t={context:t,memoizedValue:r,next:null},null===n5){if(null===e)throw Error(l(308));n5=t,e.dependencies={lanes:0,firstContext:t},e.flags|=524288}else n5=n5.next=t;return r}var oi="undefined"!=typeof AbortController?AbortController:function(){var e=[],t=this.signal={aborted:!1,addEventListener:function(t,r){e.push(r)}};this.abort=function(){t.aborted=!0,e.forEach(function(e){return e()})}},ol=o.unstable_scheduleCallback,os=o.unstable_NormalPriority,oc={$$typeof:L,Consumer:null,Provider:null,_currentValue:null,_currentValue2:null,_threadCount:0};function ou(){return{controller:new oi,data:new Map,refCount:0}}function od(e){e.refCount--,0===e.refCount&&ol(os,function(){e.controller.abort()})}function of(e,t){if(0!=(4194048&e.pendingLanes)){var r=e.transitionTypes;for(null===r&&(r=e.transitionTypes=[]),e=0;e<t.length;e++){var n=t[e];-1===r.indexOf(n)&&r.push(n)}}}var op=null,oh=null,om=0,og=0,ov=null;function oy(){if(0==--om&&(op=null,null!==oh)){null!==ov&&(ov.status="fulfilled");var e=oh;oh=null,og=0,ov=null;for(var t=0;t<e.length;t++)(0,e[t])()}}var ob=V.S;V.S=function(e,t){if(sB=em(),"object"==typeof t&&null!==t&&"function"==typeof t.then&&function(e,t){if(null===oh){var r=oh=[];om=0,og=cW(),ov={status:"pending",value:void 0,then:function(e){r.push(e)}}}om++,t.then(oy,oy)}(0,t),null!==op)for(var r=cR;null!==r;)of(r,op),r=r.next;if(null!==(r=e.types)){for(var n=cR;null!==n;)of(n,r),n=n.next;if(0!==og){null===(n=op)&&(n=op=[]);for(var o=0;o<r.length;o++){var a=r[o];-1===n.indexOf(a)&&n.push(a)}}}null!==ob&&ob(e,t)};var ox=Y(null);function o_(){var e=ox.current;return null!==e?e:sC.pooledCache}function ow(e,t){null===t?G(ox,ox.current):G(ox,t.pool)}function ok(){var e=o_();return null===e?null:{parent:oc._currentValue,pool:e}}var oj=Error(l(460)),oS=Error(l(474)),oC=Error(l(542)),oE={then:function(){}};function oT(e){return"fulfilled"===(e=e.status)||"rejected"===e}function oN(e,t,r){switch(void 0===(r=e[r])?e.push(t):r!==t&&(t.then(tL,tL),t=r),t.status){case"fulfilled":return t.value;case"rejected":throw oz(e=t.reason),e;default:if("string"==typeof t.status)t.then(tL,tL);else{if(null!==(e=sC)&&100<e.shellSuspendCounter)throw Error(l(482));(e=t).status="pending",e.then(function(e){if("pending"===t.status){var r=t;r.status="fulfilled",r.value=e}},function(e){if("pending"===t.status){var r=t;r.status="rejected",r.reason=e}})}switch(t.status){case"fulfilled":return t.value;case"rejected":throw oz(e=t.reason),e}throw oI=t,oj}}function oL(e){try{return(0,e._init)(e._payload)}catch(e){if(null!==e&&"object"==typeof e&&"function"==typeof e.then)throw oI=e,oj;throw e}}var oI=null;function oP(){if(null===oI)throw Error(l(459));var e=oI;return oI=null,e}function oz(e){if(e===oj||e===oC)throw Error(l(483))}var oR=null,oO=0;function oM(e){var t=oO;return oO+=1,null===oR&&(oR=[]),oN(oR,e,t)}function oA(e,t){e.ref=void 0!==(t=t.props.ref)?t:null}function oD(e,t){if(t.$$typeof===k)throw Error(l(525));throw Error(l(31,"[object Object]"===(e=Object.prototype.toString.call(t))?"object with keys {"+Object.keys(t).join(", ")+"}":e))}function oZ(e){function t(t,r){if(e){var n=t.deletions;null===n?(t.deletions=[r],t.flags|=16):n.push(r)}}function r(r,n){if(!e)return null;for(;null!==n;)t(r,n),n=n.sibling;return null}function n(e){for(var t=new Map;null!==e;)null===e.key?t.set(e.index,e):t.set(e.key,e),e=e.sibling;return t}function o(e,t){return(e=n_(e,t)).index=0,e.sibling=null,e}function a(t,r,n){return(t.index=n,e)?null!==(n=t.alternate)?(n=n.index)<r?(t.flags|=0x8000002,r):n:(t.flags|=0x8000002,r):(t.flags|=1048576,r)}function i(t){return e&&null===t.alternate&&(t.flags|=0x8000002),t}function s(e,t,r,n){return null===t||6!==t.tag?(t=nS(r,e.mode,n)).return=e:(t=o(t,r)).return=e,t}function c(e,t,r,n){var a=r.type;return a===C?(oA(e=d(e,t,r.props.children,n,r.key),r),e):(null!==t&&(t.elementType===a||"object"==typeof a&&null!==a&&a.$$typeof===O&&oL(a)===t.type)?oA(t=o(t,r.props),r):oA(t=nk(r.type,r.key,r.props,null,e.mode,n),r),t.return=e,t)}function u(e,t,r,n){return null===t||4!==t.tag||t.stateNode.containerInfo!==r.containerInfo||t.stateNode.implementation!==r.implementation?(t=nE(r,e.mode,n)).return=e:(t=o(t,r.children||[])).return=e,t}function d(e,t,r,n,a){return null===t||7!==t.tag?(t=nj(r,e.mode,n,a)).return=e:(t=o(t,r)).return=e,t}function f(e,t,r){if("string"==typeof t&&""!==t||"number"==typeof t||"bigint"==typeof t)return(t=nS(""+t,e.mode,r)).return=e,t;if("object"==typeof t&&null!==t){switch(t.$$typeof){case j:return oA(r=nk(t.type,t.key,t.props,null,e.mode,r),t),r.return=e,r;case S:return(t=nE(t,e.mode,r)).return=e,t;case O:return f(e,t=oL(t),r)}if(H(t)||U(t))return(t=nj(t,e.mode,r,null)).return=e,t;if("function"==typeof t.then)return f(e,oM(t),r);if(t.$$typeof===L)return f(e,oo(e,t),r);oD(e,t)}return null}function p(e,t,r,n){var o=null!==t?t.key:null;if("string"==typeof r&&""!==r||"number"==typeof r||"bigint"==typeof r)return null!==o?null:s(e,t,""+r,n);if("object"==typeof r&&null!==r){switch(r.$$typeof){case j:return r.key===o?c(e,t,r,n):null;case S:return r.key===o?u(e,t,r,n):null;case O:return p(e,t,r=oL(r),n)}if(H(r)||U(r))return null!==o?null:d(e,t,r,n,null);if("function"==typeof r.then)return p(e,t,oM(r),n);if(r.$$typeof===L)return p(e,t,oo(e,r),n);oD(e,r)}return null}function h(e,t,r,n,o){if("string"==typeof n&&""!==n||"number"==typeof n||"bigint"==typeof n)return s(t,e=e.get(r)||null,""+n,o);if("object"==typeof n&&null!==n){switch(n.$$typeof){case j:return c(t,e=e.get(null===n.key?r:n.key)||null,n,o);case S:return u(t,e=e.get(null===n.key?r:n.key)||null,n,o);case O:return h(e,t,r,n=oL(n),o)}if(H(n)||U(n))return d(t,e=e.get(r)||null,n,o,null);if("function"==typeof n.then)return h(e,t,r,oM(n),o);if(n.$$typeof===L)return h(e,t,r,oo(t,n),o);oD(t,n)}return null}return function(s,c,u,d){try{oO=0;var m=function s(c,u,d,m){if("object"==typeof d&&null!==d&&d.type===C&&null===d.key&&void 0===d.props.ref&&(d=d.props.children),"object"==typeof d&&null!==d){switch(d.$$typeof){case j:e:{for(var g=d.key;null!==u;){if(u.key===g){if((g=d.type)===C){if(7===u.tag){r(c,u.sibling),oA(m=o(u,d.props.children),d),m.return=c,c=m;break e}}else if(u.elementType===g||"object"==typeof g&&null!==g&&g.$$typeof===O&&oL(g)===u.type){r(c,u.sibling),oA(m=o(u,d.props),d),m.return=c,c=m;break e}r(c,u);break}t(c,u),u=u.sibling}d.type===C?oA(m=nj(d.props.children,c.mode,m,d.key),d):oA(m=nk(d.type,d.key,d.props,null,c.mode,m),d),m.return=c,c=m}return i(c);case S:e:{for(g=d.key;null!==u;){if(u.key===g)if(4===u.tag&&u.stateNode.containerInfo===d.containerInfo&&u.stateNode.implementation===d.implementation){r(c,u.sibling),(m=o(u,d.children||[])).return=c,c=m;break e}else{r(c,u);break}t(c,u),u=u.sibling}(m=nE(d,c.mode,m)).return=c,c=m}return i(c);case O:return s(c,u,d=oL(d),m)}if(H(d))return function(o,i,l,s){for(var c=null,u=null,d=i,m=i=0,g=null;null!==d&&m<l.length;m++){d.index>m?(g=d,d=null):g=d.sibling;var v=p(o,d,l[m],s);if(null===v){null===d&&(d=g);break}e&&d&&null===v.alternate&&t(o,d),i=a(v,i,m),null===u?c=v:u.sibling=v,u=v,d=g}if(m===l.length)return r(o,d),nq&&nZ(o,m),c;if(null===d){for(;m<l.length;m++)null!==(d=f(o,l[m],s))&&(i=a(d,i,m),null===u?c=d:u.sibling=d,u=d);return nq&&nZ(o,m),c}for(d=n(d);m<l.length;m++)null!==(g=h(d,o,m,l[m],s))&&(e&&null!==(v=g.alternate)&&d.delete(null===v.key?m:v.key),i=a(g,i,m),null===u?c=g:u.sibling=g,u=g);return e&&d.forEach(function(e){return t(o,e)}),nq&&nZ(o,m),c}(c,u,d,m);if(U(d)){if("function"!=typeof(g=U(d)))throw Error(l(150));return function(o,i,s,c){if(null==s)throw Error(l(151));for(var u=null,d=null,m=i,g=i=0,v=null,y=s.next();null!==m&&!y.done;g++,y=s.next()){m.index>g?(v=m,m=null):v=m.sibling;var b=p(o,m,y.value,c);if(null===b){null===m&&(m=v);break}e&&m&&null===b.alternate&&t(o,m),i=a(b,i,g),null===d?u=b:d.sibling=b,d=b,m=v}if(y.done)return r(o,m),nq&&nZ(o,g),u;if(null===m){for(;!y.done;g++,y=s.next())null!==(y=f(o,y.value,c))&&(i=a(y,i,g),null===d?u=y:d.sibling=y,d=y);return nq&&nZ(o,g),u}for(m=n(m);!y.done;g++,y=s.next())null!==(y=h(m,o,g,y.value,c))&&(e&&null!==(v=y.alternate)&&m.delete(null===v.key?g:v.key),i=a(y,i,g),null===d?u=y:d.sibling=y,d=y);return e&&m.forEach(function(e){return t(o,e)}),nq&&nZ(o,g),u}(c,u,d=g.call(d),m)}if("function"==typeof d.then)return s(c,u,oM(d),m);if(d.$$typeof===L)return s(c,u,oo(c,d),m);oD(c,d)}return"string"==typeof d&&""!==d||"number"==typeof d||"bigint"==typeof d?(d=""+d,null!==u&&6===u.tag?(r(c,u.sibling),(m=o(u,d)).return=c):(r(c,u),(m=nS(d,c.mode,m)).return=c),i(c=m)):r(c,u)}(s,c,u,d);return oR=null,m}catch(e){if(e===oj||e===oC)throw e;var g=nb(29,e,null,s.mode);return g.lanes=d,g.return=s,g}finally{}}}var oF=oZ(!0),oU=oZ(!1),o$=!1;function oH(e){e.updateQueue={baseState:e.memoizedState,firstBaseUpdate:null,lastBaseUpdate:null,shared:{pending:null,lanes:0,hiddenCallbacks:null},callbacks:null}}function oV(e,t){e=e.updateQueue,t.updateQueue===e&&(t.updateQueue={baseState:e.baseState,firstBaseUpdate:e.firstBaseUpdate,lastBaseUpdate:e.lastBaseUpdate,shared:e.shared,callbacks:null})}function oB(e){return{lane:e,tag:0,payload:null,callback:null,next:null}}function oq(e,t,r){var n=e.updateQueue;if(null===n)return null;if(n=n.shared,0!=(2&sS)){var o=n.pending;return null===o?t.next=t:(t.next=o.next,o.next=t),n.pending=t,t=ng(e),nm(e,null,r),t}return nf(e,n,t,r),ng(e)}function oW(e,t,r){if(null!==(t=t.updateQueue)&&(t=t.shared,0!=(4194048&r))){var n=t.lanes;n&=e.pendingLanes,r|=n,t.lanes=r,eF(e,r)}}function oK(e,t){var r=e.updateQueue,n=e.alternate;if(null!==n&&r===(n=n.updateQueue)){var o=null,a=null;if(null!==(r=r.firstBaseUpdate)){do{var i={lane:r.lane,tag:r.tag,payload:r.payload,callback:null,next:null};null===a?o=a=i:a=a.next=i,r=r.next}while(null!==r);null===a?o=a=t:a=a.next=t}else o=a=t;r={baseState:n.baseState,firstBaseUpdate:o,lastBaseUpdate:a,shared:n.shared,callbacks:n.callbacks},e.updateQueue=r;return}null===(e=r.lastBaseUpdate)?r.firstBaseUpdate=t:e.next=t,r.lastBaseUpdate=t}var oY=!1;function oX(){if(oY){var e=ov;if(null!==e)throw e}}function oG(e,t,r,n){oY=!1;var o=e.updateQueue;o$=!1;var a=o.firstBaseUpdate,i=o.lastBaseUpdate,l=o.shared.pending;if(null!==l){o.shared.pending=null;var s=l,c=s.next;s.next=null,null===i?a=c:i.next=c,i=s;var u=e.alternate;null!==u&&(l=(u=u.updateQueue).lastBaseUpdate)!==i&&(null===l?u.firstBaseUpdate=c:l.next=c,u.lastBaseUpdate=s)}if(null!==a){var d=o.baseState;for(i=0,u=c=s=null,l=a;;){var f=-0x20000001&l.lane,p=f!==l.lane;if(p?(sT&f)===f:(n&f)===f){0!==f&&f===og&&(oY=!0),null!==u&&(u=u.next={lane:0,tag:l.tag,payload:l.payload,callback:null,next:null});e:{var h=e,m=l;switch(f=t,m.tag){case 1:if("function"==typeof(h=m.payload)){d=h.call(r,d,f);break e}d=h;break e;case 3:h.flags=-65537&h.flags|128;case 0:if(null==(f="function"==typeof(h=m.payload)?h.call(r,d,f):h))break e;d=w({},d,f);break e;case 2:o$=!0}}null!==(f=l.callback)&&(e.flags|=64,p&&(e.flags|=8192),null===(p=o.callbacks)?o.callbacks=[f]:p.push(f))}else p={lane:f,tag:l.tag,payload:l.payload,callback:l.callback,next:null},null===u?(c=u=p,s=d):u=u.next=p,i|=f;if(null===(l=l.next))if(null===(l=o.shared.pending))break;else l=(p=l).next,p.next=null,o.lastBaseUpdate=p,o.shared.pending=null}null===u&&(s=d),o.baseState=s,o.firstBaseUpdate=c,o.lastBaseUpdate=u,null===a&&(o.shared.lanes=0),sM|=i,e.lanes=i,e.memoizedState=d}}function oQ(e,t){if("function"!=typeof e)throw Error(l(191,e));e.call(t)}function oJ(e,t){var r=e.callbacks;if(null!==r)for(e.callbacks=null,e=0;e<r.length;e++)oQ(r[e],t)}var o0=Y(null),o1=Y(0);function o2(e,t){G(o1,e=sR),G(o0,t),sR=e|t.baseLanes}function o3(){G(o1,sR),G(o0,o0.current)}function o4(){sR=o1.current,X(o0),X(o1)}var o5=Y(null),o6=null;function o9(e){var t=e.alternate;G(ar,1&ar.current),G(o5,e),null===o6&&(null===t||null!==o0.current?o6=e:null!==t.memoizedState&&(o6=e))}function o8(e){G(ar,ar.current),G(o5,e),null===o6&&(o6=e)}function o7(e){22===e.tag?(G(ar,ar.current),G(o5,e),null===o6&&(o6=e)):ae()}function ae(){G(ar,ar.current),G(o5,o5.current)}function at(e){X(o5),o6===e&&(o6=null),X(ar)}var ar=Y(0);function an(e,t){G(o5,o5.current),G(ar,t)}function ao(e){X(ar),X(o5),o6===e&&(o6=null)}function aa(e){for(var t=e;null!==t;){if(13===t.tag){var r=t.memoizedState;if(null!==r&&(null===(r=r.dehydrated)||uW(r)||uK(r)))return t}else if(19===t.tag&&"independent"!==t.memoizedProps.revealOrder){if(0!=(128&t.flags))return t}else if(null!==t.child){t.child.return=t,t=t.child;continue}if(t===e)break;for(;null===t.sibling;){if(null===t.return||t.return===e)return null;t=t.return}t.sibling.return=t.return,t=t.sibling}return null}var ai=0,al=null,as=null,ac=null,au=!1,ad=!1,af=!1,ap=0,ah=0,am=null,ag=0;function av(){throw Error(l(321))}function ay(e,t){if(null===t)return!1;for(var r=0;r<t.length&&r<e.length;r++)if(!rF(e[r],t[r]))return!1;return!0}function ab(e,t,r,n,o,a){return ai=a,al=t,t.memoizedState=null,t.updateQueue=null,t.lanes=0,V.H=null===e||null===e.memoizedState?iE:iT,af=!1,a=r(n,o),af=!1,ad&&(a=a_(t,r,n,o)),ax(e),a}function ax(e){V.H=iC;var t=null!==as&&null!==as.next;if(ai=0,ac=as=al=null,au=!1,ah=0,am=null,t)throw Error(l(300));null===e||iV||null!==(e=e.dependencies)&&ot(e)&&(iV=!0)}function a_(e,t,r,n){al=e;var o=0;do{if(ad&&(am=null),ah=0,ad=!1,25<=o)throw Error(l(301));if(o+=1,ac=as=null,null!=e.updateQueue){var a=e.updateQueue;a.lastEffect=null,a.events=null,a.stores=null,null!=a.memoCache&&(a.memoCache.index=0)}V.H=iN,a=t(r,n)}while(ad);return a}function aw(){var e=V.H,t=e.useState()[0];return t="function"==typeof t.then?aN(t):t,e=e.useState()[0],(null!==as?as.memoizedState:null)!==e&&(al.flags|=1024),t}function ak(){var e=0!==ap;return ap=0,e}function aj(e,t,r){t.updateQueue=e.updateQueue,t.flags&=-2053,e.lanes&=~r}function aS(e){if(au){for(e=e.memoizedState;null!==e;){var t=e.queue;null!==t&&(t.pending=null),e=e.next}au=!1}ai=0,ac=as=al=null,ad=!1,ah=ap=0,am=null}function aC(){var e={memoizedState:null,baseState:null,baseQueue:null,queue:null,next:null};return null===ac?al.memoizedState=ac=e:ac=ac.next=e,ac}function aE(){if(null===as){var e=al.alternate;e=null!==e?e.memoizedState:null}else e=as.next;var t=null===ac?al.memoizedState:ac.next;if(null!==t)ac=t,as=e;else{if(null===e){if(null===al.alternate)throw Error(l(467));throw Error(l(310))}e={memoizedState:(as=e).memoizedState,baseState:as.baseState,baseQueue:as.baseQueue,queue:as.queue,next:null},null===ac?al.memoizedState=ac=e:ac=ac.next=e}return ac}function aT(){return{lastEffect:null,events:null,stores:null,memoCache:null}}function aN(e){var t=ah;return ah+=1,null===am&&(am=[]),e=oN(am,e,t),t=al,null===(null===ac?t.memoizedState:ac.next)&&(V.H=null===(t=t.alternate)||null===t.memoizedState?iE:iT),e}function aL(e){if(null!==e&&"object"==typeof e){if("function"==typeof e.then)return aN(e);if(e.$$typeof===L)return on(e)}throw Error(l(438,String(e)))}function aI(e){var t=null,r=al.updateQueue;if(null!==r&&(t=r.memoCache),null==t){var n=al.alternate;null!==n&&null!==(n=n.updateQueue)&&null!=(n=n.memoCache)&&(t={data:n.data.map(function(e){return e.slice()}),index:0})}if(null==t&&(t={data:[],index:0}),null===r&&(r=aT(),al.updateQueue=r),r.memoCache=t,void 0===(r=t.data[t.index]))for(r=t.data[t.index]=Array(e),n=0;n<e;n++)r[n]=D;return t.index++,r}function aP(e,t){return"function"==typeof t?t(e):t}function az(e){return aR(aE(),as,e)}function aR(e,t,r){var n=e.queue;if(null===n)throw Error(l(311));n.lastRenderedReducer=r;var o=e.baseQueue,a=n.pending;if(null!==a){if(null!==o){var i=o.next;o.next=a.next,a.next=i}t.baseQueue=o=a,n.pending=null}if(a=e.baseState,null===o)e.memoizedState=a;else{t=o.next;var s=i=null,c=null,u=t,d=!1;do{var f=-0x20000001&u.lane;if(f!==u.lane?(sT&f)===f:(ai&f)===f){var p=u.revertLane;if(0===p)null!==c&&(c=c.next={lane:0,revertLane:0,gesture:null,action:u.action,hasEagerState:u.hasEagerState,eagerState:u.eagerState,next:null}),f===og&&(d=!0);else if((ai&p)===p){u=u.next,p===og&&(d=!0);continue}else f={lane:0,revertLane:u.revertLane,gesture:null,action:u.action,hasEagerState:u.hasEagerState,eagerState:u.eagerState,next:null},null===c?(s=c=f,i=a):c=c.next=f,al.lanes|=p,sM|=p;f=u.action,af&&r(a,f),a=u.hasEagerState?u.eagerState:r(a,f)}else p={lane:f,revertLane:u.revertLane,gesture:u.gesture,action:u.action,hasEagerState:u.hasEagerState,eagerState:u.eagerState,next:null},null===c?(s=c=p,i=a):c=c.next=p,al.lanes|=f,sM|=f;u=u.next}while(null!==u&&u!==t);if(null===c?i=a:c.next=s,!rF(a,e.memoizedState)&&(iV=!0,d&&null!==(r=ov)))throw r;e.memoizedState=a,e.baseState=i,e.baseQueue=c,n.lastRenderedState=a}return null===o&&(n.lanes=0),[e.memoizedState,n.dispatch]}function aO(e){var t=aE(),r=t.queue;if(null===r)throw Error(l(311));r.lastRenderedReducer=e;var n=r.dispatch,o=r.pending,a=t.memoizedState;if(null!==o){r.pending=null;var i=o=o.next;do a=e(a,i.action),i=i.next;while(i!==o);rF(a,t.memoizedState)||(iV=!0),t.memoizedState=a,null===t.baseQueue&&(t.baseState=a),r.lastRenderedState=a}return[a,n]}function aM(e,t,r){var n=al,o=aE(),a=nq;if(a){if(void 0===r)throw Error(l(407));r=r()}else r=t();var i=!rF((as||o).memoizedState,r);if(i&&(o.memoizedState=r,iV=!0),o=o.queue,a9(aZ.bind(null,n,o,e),[e]),o.getSnapshot!==t||i||null!==ac&&1&ac.memoizedState.tag){if(n.flags|=2048,a2(9,{destroy:void 0},aD.bind(null,n,o,r,t),null),null===sC)throw Error(l(349));a||0!=(127&ai)||aA(n,t,r)}return r}function aA(e,t,r){e.flags|=16384,e={getSnapshot:t,value:r},null===(t=al.updateQueue)?(t=aT(),al.updateQueue=t,t.stores=[e]):null===(r=t.stores)?t.stores=[e]:r.push(e)}function aD(e,t,r,n){t.value=r,t.getSnapshot=n,aF(t)&&aU(e)}function aZ(e,t,r){return r(function(){aF(t)&&aU(e)})}function aF(e){var t=e.getSnapshot;e=e.value;try{var r=t();return!rF(e,r)}catch(e){return!0}}function aU(e){var t=nh(e,2);null!==t&&ce(t,e,2)}function a$(e){var t=aC();if("function"==typeof e){var r=e;if(e=r(),af){eC(!0);try{r()}finally{eC(!1)}}}return t.memoizedState=t.baseState=e,t.queue={pending:null,lanes:0,dispatch:null,lastRenderedReducer:aP,lastRenderedState:e},t}function aH(e,t,r,n){return e.baseState=r,aR(e,as,"function"==typeof n?n:aP)}function aV(e,t,r,n,o){if(ik(e))throw Error(l(485));if(null!==(e=t.action)){var a={payload:o,action:e,next:null,isTransition:!0,status:"pending",value:null,reason:null,listeners:[],then:function(e){a.listeners.push(e)}};null!==V.T?r(!0):a.isTransition=!1,n(a),null===(r=t.pending)?(a.next=t.pending=a,aB(t,a)):(a.next=r.next,t.pending=r.next=a)}}function aB(e,t){var r=t.action,n=t.payload,o=e.state;if(t.isTransition){var a=V.T,i={};i.types=null!==a?a.types:null,V.T=i;try{var l=r(o,n),s=V.S;null!==s&&s(i,l),aq(e,t,l)}catch(r){aK(e,t,r)}finally{null!==a&&null!==i.types&&(a.types=i.types),V.T=a}}else try{a=r(o,n),aq(e,t,a)}catch(r){aK(e,t,r)}}function aq(e,t,r){null!==r&&"object"==typeof r&&"function"==typeof r.then?r.then(function(r){aW(e,t,r)},function(r){return aK(e,t,r)}):aW(e,t,r)}function aW(e,t,r){t.status="fulfilled",t.value=r,aY(t),e.state=r,null!==(t=e.pending)&&((r=t.next)===t?e.pending=null:(r=r.next,t.next=r,aB(e,r)))}function aK(e,t,r){var n=e.pending;if(e.pending=null,null!==n){n=n.next;do t.status="rejected",t.reason=r,aY(t),t=t.next;while(t!==n)}e.action=null}function aY(e){e=e.listeners;for(var t=0;t<e.length;t++)(0,e[t])()}function aX(e,t){return t}function aG(e,t){if(nq){var r=sC.formState;if(null!==r){e:{var n=al;if(nq){if(nB){t:{for(var o=nB,a=nK;8!==o.nodeType;)if(!a||null===(o=uY(o.nextSibling))){o=null;break t}o="F!"===(a=o.data)||"F"===a?o:null}if(o){nB=uY(o.nextSibling),n="F!"===o.data;break e}}nX(n)}n=!1}n&&(t=r[0])}}return(r=aC()).memoizedState=r.baseState=t,n={pending:null,lanes:0,dispatch:null,lastRenderedReducer:aX,lastRenderedState:t},r.queue=n,r=ix.bind(null,al,n),n.dispatch=r,n=a$(!1),a=iw.bind(null,al,!1,n.queue),n=aC(),o={state:t,dispatch:null,action:e,pending:null},n.queue=o,r=aV.bind(null,al,o,a,r),o.dispatch=r,n.memoizedState=e,[t,r,!1]}function aQ(e){return aJ(aE(),as,e)}function aJ(e,t,r){if(t=aR(e,t,aX)[0],e=az(aP)[0],"object"==typeof t&&null!==t&&"function"==typeof t.then)try{var n=aN(t)}catch(e){if(e===oj)throw oC;throw e}else n=t;var o=(t=aE()).queue,a=o.dispatch;return r!==t.memoizedState&&(al.flags|=2048,a2(9,{destroy:void 0},a0.bind(null,o,r),null)),[n,a,e]}function a0(e,t){e.action=t}function a1(e){var t=aE(),r=as;if(null!==r)return aJ(t,r,e);aE(),t=t.memoizedState;var n=(r=aE()).queue.dispatch;return r.memoizedState=e,[t,n,!1]}function a2(e,t,r,n){return e={tag:e,create:r,deps:n,inst:t,next:null},null===(t=al.updateQueue)&&(t=aT(),al.updateQueue=t),null===(r=t.lastEffect)?t.lastEffect=e.next=e:(n=r.next,r.next=e,e.next=n,t.lastEffect=e),e}function a3(){return aE().memoizedState}function a4(e,t,r,n){var o=aC();al.flags|=e,o.memoizedState=a2(1|t,{destroy:void 0},r,void 0===n?null:n)}function a5(e,t,r,n){var o=aE();n=void 0===n?null:n;var a=o.memoizedState.inst;null!==as&&null!==n&&ay(n,as.memoizedState.deps)?o.memoizedState=a2(t,a,r,n):(al.flags|=e,o.memoizedState=a2(1|t,a,r,n))}function a6(e,t){a4(8390656,8,e,t)}function a9(e,t){a5(2048,8,e,t)}function a8(e){var t=aE().memoizedState,r={ref:t,nextImpl:e};al.flags|=4;var n=al.updateQueue;if(null===n)n=aT(),al.updateQueue=n,n.events=[r];else{var o=n.events;null===o?n.events=[r]:o.push(r)}return function(){if(0!=(2&sS))throw Error(l(440));return t.impl.apply(void 0,arguments)}}function a7(e,t){return a5(4,2,e,t)}function ie(e,t){return a5(4,4,e,t)}function it(e,t){if("function"==typeof t){var r=t(e=e());return function(){"function"==typeof r?r():t(null)}}if(null!=t)return t.current=e=e(),function(){t.current=null}}function ir(e,t,r){r=null!=r?r.concat([e]):null,a5(4,4,it.bind(null,t,e),r)}function io(){}function ia(e,t){var r=aE();t=void 0===t?null:t;var n=r.memoizedState;return null!==t&&ay(t,n[1])?n[0]:(r.memoizedState=[e,t],e)}function ii(e,t){var r=aE();t=void 0===t?null:t;var n=r.memoizedState;if(null!==t&&ay(t,n[1]))return n[0];if(n=e(),af){eC(!0);try{e()}finally{eC(!1)}}return r.memoizedState=[n,t],n}function il(e,t,r){return void 0===r||0!=(0x40000000&ai)&&0==(261930&sT)?e.memoizedState=t:(e.memoizedState=r,e=s8(),al.lanes|=e,sM|=e,r)}function is(e,t,r,n){return rF(r,t)?r:null!==o0.current?(rF(e=il(e,r,n),t)||(iV=!0),e):0==(106&ai)||0!=(0x40000000&ai)&&0==(261930&sT)?(iV=!0,e.memoizedState=r):(e=s8(),al.lanes|=e,sM|=e,t)}function ic(e,t,r,n,o){var a=B.p;B.p=0!==a&&8>a?a:8;var i=V.T,l={};l.types=null!==i?i.types:null,V.T=l,iw(e,!1,t,r);try{var s=o(),c=V.S;if(null!==c&&c(l,s),null!==s&&"object"==typeof s&&"function"==typeof s.then){var u,d,f=(u=[],d={status:"pending",value:null,reason:null,then:function(e){u.push(e)}},s.then(function(){d.status="fulfilled",d.value=n;for(var e=0;e<u.length;e++)(0,u[e])(n)},function(e){for(d.status="rejected",d.reason=e,e=0;e<u.length;e++)(0,u[e])(void 0)}),d);i_(e,t,f,s9(e))}else i_(e,t,n,s9(e))}catch(r){i_(e,t,{then:function(){},status:"rejected",reason:r},s9())}finally{B.p=a,null!==i&&null!==l.types&&(i.types=l.types),V.T=i}}function iu(){}function id(e,t,r,n){if(5!==e.tag)throw Error(l(476));var o=ip(e).queue;ic(e,o,t,q,null===r?iu:function(){return ih(e),r(n)})}function ip(e){var t=e.memoizedState;if(null!==t)return t;var r={};return(t={memoizedState:q,baseState:q,baseQueue:null,queue:{pending:null,lanes:0,dispatch:null,lastRenderedReducer:aP,lastRenderedState:q},next:null}).next={memoizedState:r,baseState:r,baseQueue:null,queue:{pending:null,lanes:0,dispatch:null,lastRenderedReducer:aP,lastRenderedState:r},next:null},e.memoizedState=t,null!==(e=e.alternate)&&(e.memoizedState=t),t}function ih(e){var t=ip(e);null===t.next&&(t=e.alternate.memoizedState),i_(e,t.next.queue,{},s9())}function im(){return on(dw)}function ig(){return aE().memoizedState}function iv(){return aE().memoizedState}function iy(e){for(var t=e.return;null!==t;){switch(t.tag){case 24:case 3:var r=s9(),n=oq(t,e=oB(r),r);null!==n&&(ce(n,t,r),oW(n,t,r)),t={cache:ou()},e.payload=t;return}t=t.return}}function ib(e,t,r){var n=s9();r={lane:n,revertLane:0,gesture:null,action:r,hasEagerState:!1,eagerState:null,next:null},ik(e)?ij(t,r):null!==(r=np(e,t,r,n))&&(ce(r,e,n),iS(r,t,n))}function ix(e,t,r){i_(e,t,r,s9())}function i_(e,t,r,n){var o={lane:n,revertLane:0,gesture:null,action:r,hasEagerState:!1,eagerState:null,next:null};if(ik(e))ij(t,o);else{var a=e.alternate;if(0===e.lanes&&(null===a||0===a.lanes)&&null!==(a=t.lastRenderedReducer))try{var i=t.lastRenderedState,l=a(i,r);if(o.hasEagerState=!0,o.eagerState=l,rF(l,i))return nf(e,t,o,0),null===sC&&nd(),!1}catch(e){}finally{}if(null!==(r=np(e,t,o,n)))return ce(r,e,n),iS(r,t,n),!0}return!1}function iw(e,t,r,n){if(n={lane:2,revertLane:cW(),gesture:null,action:n,hasEagerState:!1,eagerState:null,next:null},ik(e)){if(t)throw Error(l(479))}else null!==(t=np(e,r,n,2))&&ce(t,e,2)}function ik(e){var t=e.alternate;return e===al||null!==t&&t===al}function ij(e,t){ad=au=!0;var r=e.pending;null===r?t.next=t:(t.next=r.next,r.next=t),e.pending=t}function iS(e,t,r){if(0!=(4194048&r)){var n=t.lanes;n&=e.pendingLanes,t.lanes=r|=n,eF(e,r)}}var iC={readContext:on,use:aL,useCallback:av,useContext:av,useEffect:av,useImperativeHandle:av,useLayoutEffect:av,useInsertionEffect:av,useMemo:av,useReducer:av,useRef:av,useState:av,useDebugValue:av,useDeferredValue:av,useTransition:av,useSyncExternalStore:av,useId:av,useHostTransitionStatus:av,useFormState:av,useActionState:av,useOptimistic:av,useMemoCache:av,useCacheRefresh:av,useEffectEvent:av},iE={readContext:on,use:aL,useCallback:function(e,t){return aC().memoizedState=[e,void 0===t?null:t],e},useContext:on,useEffect:a6,useImperativeHandle:function(e,t,r){r=null!=r?r.concat([e]):null,a4(4194308,4,it.bind(null,t,e),r)},useLayoutEffect:function(e,t){return a4(4194308,4,e,t)},useInsertionEffect:function(e,t){a4(4,2,e,t)},useMemo:function(e,t){var r=aC();t=void 0===t?null:t;var n=e();if(af){eC(!0);try{e()}finally{eC(!1)}}return r.memoizedState=[n,t],n},useReducer:function(e,t,r){var n=aC();if(void 0!==r){var o=r(t);if(af){eC(!0);try{r(t)}finally{eC(!1)}}}else o=t;return n.memoizedState=n.baseState=o,n.queue=e={pending:null,lanes:0,dispatch:null,lastRenderedReducer:e,lastRenderedState:o},e=e.dispatch=ib.bind(null,al,e),[n.memoizedState,e]},useRef:function(e){return aC().memoizedState={current:e}},useState:function(e){var t=(e=a$(e)).queue,r=ix.bind(null,al,t);return t.dispatch=r,[e.memoizedState,r]},useDebugValue:io,useDeferredValue:function(e,t){return il(aC(),e,t)},useTransition:function(){var e=a$(!1);return e=ic.bind(null,al,e.queue,!0,!1),aC().memoizedState=e,[!1,e]},useSyncExternalStore:function(e,t,r){var n=al,o=aC();if(nq){if(void 0===r)throw Error(l(407));r=r()}else{if(r=t(),null===sC)throw Error(l(349));0!=(127&sT)||aA(n,t,r)}o.memoizedState=r;var a={value:r,getSnapshot:t};return o.queue=a,a6(aZ.bind(null,n,a,e),[e]),n.flags|=2048,a2(9,{destroy:void 0},aD.bind(null,n,a,r,t),null),r},useId:function(){var e=aC(),t=sC.identifierPrefix;if(nq){var r=nD,n=nA;t="_"+t+"R_"+(r=(n&~(1<<32-eE(n)-1)).toString(32)+r),0<(r=ap++)&&(t+="H"+r.toString(32)),t+="_"}else t="_"+t+"r_"+(r=ag++).toString(32)+"_";return e.memoizedState=t},useHostTransitionStatus:im,useFormState:aG,useActionState:aG,useOptimistic:function(e){var t=aC();t.memoizedState=t.baseState=e;var r={pending:null,lanes:0,dispatch:null,lastRenderedReducer:null,lastRenderedState:null};return t.queue=r,t=iw.bind(null,al,!0,r),r.dispatch=t,[e,t]},useMemoCache:aI,useCacheRefresh:function(){return aC().memoizedState=iy.bind(null,al)},useEffectEvent:function(e){var t=aC(),r={impl:e};return t.memoizedState=r,function(){if(0!=(2&sS))throw Error(l(440));return r.impl.apply(void 0,arguments)}}},iT={readContext:on,use:aL,useCallback:ia,useContext:on,useEffect:a9,useImperativeHandle:ir,useInsertionEffect:a7,useLayoutEffect:ie,useMemo:ii,useReducer:az,useRef:a3,useState:function(){return az(aP)},useDebugValue:io,useDeferredValue:function(e,t){return is(aE(),as.memoizedState,e,t)},useTransition:function(){var e=az(aP)[0],t=aE().memoizedState;return["boolean"==typeof e?e:aN(e),t]},useSyncExternalStore:aM,useId:ig,useHostTransitionStatus:im,useFormState:aQ,useActionState:aQ,useOptimistic:function(e,t){return aH(aE(),as,e,t)},useMemoCache:aI,useCacheRefresh:iv,useEffectEvent:a8},iN={readContext:on,use:aL,useCallback:ia,useContext:on,useEffect:a9,useImperativeHandle:ir,useInsertionEffect:a7,useLayoutEffect:ie,useMemo:ii,useReducer:aO,useRef:a3,useState:function(){return aO(aP)},useDebugValue:io,useDeferredValue:function(e,t){var r=aE();return null===as?il(r,e,t):is(r,as.memoizedState,e,t)},useTransition:function(){var e=aO(aP)[0],t=aE().memoizedState;return["boolean"==typeof e?e:aN(e),t]},useSyncExternalStore:aM,useId:ig,useHostTransitionStatus:im,useFormState:a1,useActionState:a1,useOptimistic:function(e,t){var r=aE();return null!==as?aH(r,as,e,t):(r.baseState=e,[e,r.queue.dispatch])},useMemoCache:aI,useCacheRefresh:iv,useEffectEvent:a8};function iL(e,t,r,n){r=null==(r=r(n,t=e.memoizedState))?t:w({},t,r),e.memoizedState=r,0===e.lanes&&(e.updateQueue.baseState=r)}var iI={enqueueSetState:function(e,t,r){e=e._reactInternals;var n=s9(),o=oB(n);o.payload=t,null!=r&&(o.callback=r),null!==(t=oq(e,o,n))&&(ce(t,e,n),oW(t,e,n))},enqueueReplaceState:function(e,t,r){e=e._reactInternals;var n=s9(),o=oB(n);o.tag=1,o.payload=t,null!=r&&(o.callback=r),null!==(t=oq(e,o,n))&&(ce(t,e,n),oW(t,e,n))},enqueueForceUpdate:function(e,t){e=e._reactInternals;var r=s9(),n=oB(r);n.tag=2,null!=t&&(n.callback=t),null!==(t=oq(e,n,r))&&(ce(t,e,r),oW(t,e,r))}};function iP(e,t,r,n,o,a,i){return"function"==typeof(e=e.stateNode).shouldComponentUpdate?e.shouldComponentUpdate(n,a,i):!t.prototype||!t.prototype.isPureReactComponent||!rU(r,n)||!rU(o,a)}function iz(e,t,r,n){e=t.state,"function"==typeof t.componentWillReceiveProps&&t.componentWillReceiveProps(r,n),"function"==typeof t.UNSAFE_componentWillReceiveProps&&t.UNSAFE_componentWillReceiveProps(r,n),t.state!==e&&iI.enqueueReplaceState(t,t.state,null)}function iR(e,t){var r=t;if("ref"in t)for(var n in r={},t)"ref"!==n&&(r[n]=t[n]);if(e=e.defaultProps)for(var o in r===t&&(r=w({},r)),e)void 0===r[o]&&(r[o]=e[o]);return r}function iO(e){nl(e)}function iM(e){console.error(e)}function iA(e){nl(e)}function iD(e,t){try{(0,e.onUncaughtError)(t.value,{componentStack:t.stack})}catch(e){setTimeout(function(){throw e})}}function iZ(e,t,r){try{(0,e.onCaughtError)(r.value,{componentStack:r.stack,errorBoundary:1===t.tag?t.stateNode:null})}catch(e){setTimeout(function(){throw e})}}function iF(e,t,r){return(r=oB(r)).tag=3,r.payload={element:null},r.callback=function(){iD(e,t)},r}function iU(e){return(e=oB(e)).tag=3,e}function i$(e,t,r,n){var o=r.type.getDerivedStateFromError;if("function"==typeof o){var a=n.value;e.payload=function(){return o(a)},e.callback=function(){iZ(t,r,n)}}var i=r.stateNode;null!==i&&"function"==typeof i.componentDidCatch&&(e.callback=function(){iZ(t,r,n),"function"!=typeof o&&(null===sK?sK=new Set([this]):sK.add(this));var e=n.stack;this.componentDidCatch(n.value,{componentStack:null!==e?e:""})})}var iH=Error(l(461)),iV=!1;function iB(e,t,r,n){t.child=null===e?oU(t,null,r,n):oF(t,e.child,r,n)}function iq(e,t,r,n,o){r=r.render;var a=t.ref;if("ref"in n){var i={};for(var l in n)"ref"!==l&&(i[l]=n[l])}else i=n;return(or(t),n=ab(e,t,r,i,a,o),l=ak(),null===e||iV)?(nq&&l&&nU(t),t.flags|=1,iB(e,t,n,o),t.child):(aj(e,t,o),ls(e,t,o))}function iW(e,t,r,n,o){if(null===e){var a=r.type;return"function"!=typeof a||nx(a)||void 0!==a.defaultProps||null!==r.compare?((e=nk(r.type,null,n,t,t.mode,o)).ref=t.ref,e.return=t,t.child=e):(t.tag=15,t.type=a,iK(e,t,a,n,o))}if(a=e.child,!lc(e,o)){var i=a.memoizedProps;if((r=null!==(r=r.compare)?r:rU)(i,n)&&e.ref===t.ref)return ls(e,t,o)}return t.flags|=1,(e=n_(a,n)).ref=t.ref,e.return=t,t.child=e}function iK(e,t,r,n,o){if(null!==e){var a=e.memoizedProps;if(rU(a,n)&&e.ref===t.ref)if(iV=!1,t.pendingProps=n=a,!lc(e,o))return t.lanes=e.lanes,ls(e,t,o);else 0!=(131072&e.flags)&&(iV=!0)}return i1(e,t,r,n,o)}function iY(e,t,r,n){var o=n.children,a=null!==e?e.memoizedState:null;if(null===e&&null===t.stateNode&&(t.stateNode={_visibility:1,_pendingMarkers:null,_retryCache:null,_transitions:null}),"hidden"===n.mode){if(0!=(128&t.flags)){if(a=null!==a?a.baseLanes|r:r,null!==e){for(o=0,n=t.child=e.child;null!==n;)o=o|n.lanes|n.childLanes,n=n.sibling;n=o&~a}else n=0,t.child=null;return iG(e,t,a,r,n)}if(0==(0x20000000&r))return n=t.lanes=0x20000000,iG(e,t,null!==a?a.baseLanes|r:r,r,n);t.memoizedState={baseLanes:0,cachePool:null},null!==e&&ow(t,null!==a?a.cachePool:null),null!==a?o2(t,a):o3(),o7(t)}else null!==a?(ow(t,a.cachePool),o2(t,a),ae(),t.memoizedState=null):(null!==e&&ow(t,null),o3(),ae());return iB(e,t,o,r),t.child}function iX(e,t){return null!==e&&22===e.tag||null!==t.stateNode||(t.stateNode={_visibility:1,_pendingMarkers:null,_retryCache:null,_transitions:null}),t.sibling}function iG(e,t,r,n,o){var a=o_();return t.memoizedState={baseLanes:r,cachePool:a=null===a?null:{parent:oc._currentValue,pool:a}},null!==e&&ow(t,null),o3(),o7(t),null!==e&&oe(e,t,n,!0),t.childLanes=o,null}function iQ(e,t){return(t=le({mode:t.mode,children:t.children},e.mode)).ref=e.ref,e.child=t,t.return=e,t}function iJ(e,t,r){return oF(t,e.child,null,r),e=iQ(t,t.pendingProps),e.flags|=2,at(t),t.memoizedState=null,e}function i0(e,t){var r=t.ref;if(null===r)null!==e&&null!==e.ref&&(t.flags|=4194816);else{if("function"!=typeof r&&"object"!=typeof r)throw Error(l(284));(null===e||e.ref!==r)&&(t.flags|=4194816)}}function i1(e,t,r,n,o){return(or(t),r=ab(e,t,r,n,void 0,o),n=ak(),null===e||iV)?(nq&&n&&nU(t),t.flags|=1,iB(e,t,r,o),t.child):(aj(e,t,o),ls(e,t,o))}function i2(e,t,r,n,o,a){return(or(t),t.updateQueue=null,r=a_(t,n,r,o),ax(e),n=ak(),null===e||iV)?(nq&&n&&nU(t),t.flags|=1,iB(e,t,r,a),t.child):(aj(e,t,a),ls(e,t,a))}function i3(e,t,r,n,o){if(or(t),null===t.stateNode){var a=nv,i=r.contextType;"object"==typeof i&&null!==i&&(a=on(i)),t.memoizedState=null!==(a=new r(n,a)).state&&void 0!==a.state?a.state:null,a.updater=iI,t.stateNode=a,a._reactInternals=t,(a=t.stateNode).props=n,a.state=t.memoizedState,a.refs={},oH(t),i=r.contextType,a.context="object"==typeof i&&null!==i?on(i):nv,a.state=t.memoizedState,"function"==typeof(i=r.getDerivedStateFromProps)&&(iL(t,r,i,n),a.state=t.memoizedState),"function"==typeof r.getDerivedStateFromProps||"function"==typeof a.getSnapshotBeforeUpdate||"function"!=typeof a.UNSAFE_componentWillMount&&"function"!=typeof a.componentWillMount||(i=a.state,"function"==typeof a.componentWillMount&&a.componentWillMount(),"function"==typeof a.UNSAFE_componentWillMount&&a.UNSAFE_componentWillMount(),i!==a.state&&iI.enqueueReplaceState(a,a.state,null),oG(t,n,a,o),oX(),a.state=t.memoizedState),"function"==typeof a.componentDidMount&&(t.flags|=4194308),n=!0}else if(null===e){a=t.stateNode;var l=t.memoizedProps,s=iR(r,l);a.props=s;var c=a.context,u=r.contextType;i=nv,"object"==typeof u&&null!==u&&(i=on(u));var d=r.getDerivedStateFromProps;u="function"==typeof d||"function"==typeof a.getSnapshotBeforeUpdate,l=t.pendingProps!==l,u||"function"!=typeof a.UNSAFE_componentWillReceiveProps&&"function"!=typeof a.componentWillReceiveProps||(l||c!==i)&&iz(t,a,n,i),o$=!1;var f=t.memoizedState;a.state=f,oG(t,n,a,o),oX(),c=t.memoizedState,l||f!==c||o$?("function"==typeof d&&(iL(t,r,d,n),c=t.memoizedState),(s=o$||iP(t,r,s,n,f,c,i))?(u||"function"!=typeof a.UNSAFE_componentWillMount&&"function"!=typeof a.componentWillMount||("function"==typeof a.componentWillMount&&a.componentWillMount(),"function"==typeof a.UNSAFE_componentWillMount&&a.UNSAFE_componentWillMount()),"function"==typeof a.componentDidMount&&(t.flags|=4194308)):("function"==typeof a.componentDidMount&&(t.flags|=4194308),t.memoizedProps=n,t.memoizedState=c),a.props=n,a.state=c,a.context=i,n=s):("function"==typeof a.componentDidMount&&(t.flags|=4194308),n=!1)}else{a=t.stateNode,oV(e,t),u=iR(r,i=t.memoizedProps),a.props=u,d=t.pendingProps,f=a.context,c=r.contextType,s=nv,"object"==typeof c&&null!==c&&(s=on(c)),(c="function"==typeof(l=r.getDerivedStateFromProps)||"function"==typeof a.getSnapshotBeforeUpdate)||"function"!=typeof a.UNSAFE_componentWillReceiveProps&&"function"!=typeof a.componentWillReceiveProps||(i!==d||f!==s)&&iz(t,a,n,s),o$=!1,f=t.memoizedState,a.state=f,oG(t,n,a,o),oX();var p=t.memoizedState;i!==d||f!==p||o$||null!==e&&null!==e.dependencies&&ot(e.dependencies)?("function"==typeof l&&(iL(t,r,l,n),p=t.memoizedState),(u=o$||iP(t,r,u,n,f,p,s)||null!==e&&null!==e.dependencies&&ot(e.dependencies))?(c||"function"!=typeof a.UNSAFE_componentWillUpdate&&"function"!=typeof a.componentWillUpdate||("function"==typeof a.componentWillUpdate&&a.componentWillUpdate(n,p,s),"function"==typeof a.UNSAFE_componentWillUpdate&&a.UNSAFE_componentWillUpdate(n,p,s)),"function"==typeof a.componentDidUpdate&&(t.flags|=4),"function"==typeof a.getSnapshotBeforeUpdate&&(t.flags|=1024)):("function"!=typeof a.componentDidUpdate||i===e.memoizedProps&&f===e.memoizedState||(t.flags|=4),"function"!=typeof a.getSnapshotBeforeUpdate||i===e.memoizedProps&&f===e.memoizedState||(t.flags|=1024),t.memoizedProps=n,t.memoizedState=p),a.props=n,a.state=p,a.context=s,n=u):("function"!=typeof a.componentDidUpdate||i===e.memoizedProps&&f===e.memoizedState||(t.flags|=4),"function"!=typeof a.getSnapshotBeforeUpdate||i===e.memoizedProps&&f===e.memoizedState||(t.flags|=1024),n=!1)}return a=n,i0(e,t),n=0!=(128&t.flags),a||n?(a=t.stateNode,r=n&&"function"!=typeof r.getDerivedStateFromError?null:a.render(),t.flags|=1,null!==e&&n?(t.child=oF(t,e.child,null,o),t.child=oF(t,null,r,o)):iB(e,t,r,o),t.memoizedState=a.state,e=t.child):e=ls(e,t,o),e}function i4(e,t,r,n){return n0(),t.flags|=256,iB(e,t,r,n),t.child}var i5={dehydrated:null,treeContext:null,retryLane:0,hydrationErrors:null};function i6(e){return{baseLanes:e,cachePool:ok()}}function i9(e,t,r){return e=null!==e?e.childLanes&~r:0,t&&(e|=sZ),e}function i8(e,t,r){var n,o=t.pendingProps,a=!1,i=0!=(128&t.flags);if((n=i)||(n=(null===e||null!==e.memoizedState)&&0!=(2&ar.current)),n&&(a=!0,t.flags&=-129),n=0!=(32&t.flags),t.flags&=-33,null===e){if(nq){if(a?o9(t):ae(),(e=nB)?null!==(e=null!==(e=uq(e,nK))&&"&"!==e.data?e:null)&&(t.memoizedState={dehydrated:e,treeContext:null!==nM?{id:nA,overflow:nD}:null,retryLane:0x20000000,hydrationErrors:null},(r=nC(e)).return=t,t.child=r,nV=t,nB=null):e=null,null===e)throw nX(t);return uK(e)?t.lanes=32:t.lanes=0x20000000,null}var s=o.children;return(o=o.fallback,a)?(ae(),s=le({mode:"hidden",children:s},a=t.mode),o=nj(o,a,r,null),s.return=t,o.return=t,s.sibling=o,t.child=s,(o=t.child).memoizedState=i6(r),o.childLanes=i9(e,n,r),t.memoizedState=i5,iX(null,o)):(o9(t),i7(t,s))}var c=e.memoizedState;if(null!==c&&null!==(s=c.dehydrated)){if(i)256&t.flags?(o9(t),t.flags&=-257,t=lt(e,t,r)):null!==t.memoizedState?(ae(),t.child=e.child,t.flags|=128,t=null):(ae(),s=o.fallback,a=t.mode,o=le({mode:"visible",children:o.children},a),s=nj(s,a,r,null),s.flags|=2,o.return=t,s.return=t,o.sibling=s,t.child=o,oF(t,e.child,null,r),(o=t.child).memoizedState=i6(r),o.childLanes=i9(e,n,r),t.memoizedState=i5,t=iX(null,o));else if(o9(t),uK(s)){if(n=s.nextSibling&&s.nextSibling.dataset)var u=n.dgst;n=u,(o=Error(l(419))).stack="",o.digest=n,n2({value:o,source:null,stack:null}),t=lt(e,t,r)}else if(iV||oe(e,t,r,!1),n=0!=(r&e.childLanes),iV||n){if(null!==(n=sC)&&0!==(o=eU(n,r))&&o!==c.retryLane)throw c.retryLane=o,nh(e,o),ce(n,e,o),iH;uW(s)||cd(),t=lt(e,t,r)}else uW(s)?(t.flags|=192,t.child=e.child,t=null):(e=c.treeContext,nB=uY(s.nextSibling),nV=t,nq=!0,nW=null,nK=!1,null!==e&&nH(t,e),t=i7(t,o.children),t.flags|=4096);return t}return a?(ae(),s=o.fallback,a=t.mode,u=(c=e.child).sibling,(o=n_(c,{mode:"hidden",children:o.children})).subtreeFlags=0x7f00000&c.subtreeFlags,null!==u?s=n_(u,s):(s=nj(s,a,r,null),s.flags|=2),s.return=t,o.return=t,o.sibling=s,t.child=o,iX(null,o),o=t.child,null===(s=e.child.memoizedState)?s=i6(r):(null!==(a=s.cachePool)?(c=oc._currentValue,a=a.parent!==c?{parent:c,pool:c}:a):a=ok(),s={baseLanes:s.baseLanes|r,cachePool:a}),o.memoizedState=s,o.childLanes=i9(e,n,r),t.memoizedState=i5,iX(e.child,o)):(o9(t),e=(r=e.child).sibling,(r=n_(r,{mode:"visible",children:o.children})).return=t,r.sibling=null,null!==e&&(null===(n=t.deletions)?(t.deletions=[e],t.flags|=16):n.push(e)),t.child=r,t.memoizedState=null,r)}function i7(e,t){return(t=le({mode:"visible",children:t},e.mode)).return=e,e.child=t}function le(e,t){return(e=nb(22,e,null,t)).lanes=0,e}function lt(e,t,r){return oF(t,e.child,null,r),e=i7(t,t.pendingProps.children),e.flags|=2,t.memoizedState=null,e}function lr(e,t,r){e.lanes|=t;var n=e.alternate;null!==n&&(n.lanes|=t),n8(e.return,t,r)}function ln(e){for(var t=null;null!==e;){var r=e.alternate;null!==r&&null===aa(r)&&(t=e),e=e.sibling}return t}function lo(e,t,r,n,o,a){var i=e.memoizedState;null===i?e.memoizedState={isBackwards:t,rendering:null,renderingStartTime:0,last:n,tail:r,tailMode:o,treeForkCount:a}:(i.isBackwards=t,i.rendering=null,i.renderingStartTime=0,i.last=n,i.tail=r,i.tailMode=o,i.treeForkCount=a)}function la(e){var t=e.child;for(e.child=null;null!==t;){var r=t.sibling;t.sibling=e.child,e.child=t,t=r}}function li(e,t,r){var n=t.pendingProps,o=n.revealOrder,a=n.tail;n=n.children;var i=ar.current;if(128&t.flags)return an(t,i),null;var l=0!=(2&i);if(l?(i=1&i|2,t.flags|=128):i&=1,an(t,i),"backwards"===o&&null!==e?(la(e),iB(e,t,n,r),la(e)):iB(e,t,n,r),n=nq?nz:0,!l&&null!==e&&0!=(128&e.flags))e:for(e=t.child;null!==e;){if(13===e.tag)null!==e.memoizedState&&lr(e,r,t);else if(19===e.tag)lr(e,r,t);else if(null!==e.child){e.child.return=e,e=e.child;continue}if(e===t)break;for(;null===e.sibling;){if(null===e.return||e.return===t)break e;e=e.return}e.sibling.return=e.return,e=e.sibling}switch(o){case"backwards":null===(r=ln(t.child))?(o=t.child,t.child=null):(o=r.sibling,r.sibling=null,la(t)),lo(t,!0,o,null,a,n);break;case"unstable_legacy-backwards":for(r=null,o=t.child,t.child=null;null!==o;){if(null!==(e=o.alternate)&&null===aa(e)){t.child=o;break}e=o.sibling,o.sibling=r,r=o,o=e}lo(t,!0,r,null,a,n);break;case"together":lo(t,!1,null,null,void 0,n);break;case"independent":t.memoizedState=null;break;default:null===(r=ln(t.child))?(o=t.child,t.child=null):(o=r.sibling,r.sibling=null),lo(t,!1,o,r,a,n)}return t.child}function ll(e,t,r){var n=t.pendingProps;return n6(t,t.type,n.value),iB(e,t,n.children,r),t.child}function ls(e,t,r){if(null!==e&&(t.dependencies=e.dependencies),sM|=t.lanes,0==(r&t.childLanes)){if(null===e)return null;else if(oe(e,t,r,!1),0==(r&t.childLanes))return null}if(null!==e&&t.child!==e.child)throw Error(l(153));if(null!==t.child){for(r=n_(e=t.child,e.pendingProps),t.child=r,r.return=t;null!==e.sibling;)e=e.sibling,(r=r.sibling=n_(e,e.pendingProps)).return=t;r.sibling=null}return t.child}function lc(e,t){return 0!=(e.lanes&t)||!!(null!==(e=e.dependencies)&&ot(e))}function lu(e,t,r){if(null!==e)if(e.memoizedProps!==t.pendingProps)iV=!0;else{if(!lc(e,r)&&0==(128&t.flags))return iV=!1,function(e,t,r){switch(t.tag){case 3:er(t,t.stateNode.containerInfo),n6(t,oc,e.memoizedState.cache),n0();break;case 27:case 5:eo(t);break;case 4:er(t,t.stateNode.containerInfo);break;case 10:n6(t,t.type,t.memoizedProps.value);break;case 31:if(null!==t.memoizedState)return t.flags|=128,o8(t),null;break;case 13:var n=t.memoizedState;if(null!==n){if(null!==n.dehydrated)return o9(t),t.flags|=128,null;n=oe(e,t,r,!1);var o=t.child.childLanes;if(n||0!=(r&o))return i8(e,t,r);return o9(t),null!==(e=ls(e,t,r))?e.sibling:null}o9(t);break;case 19:if(128&t.flags)return li(e,t,r);if(o=0!=(128&e.flags),(n=0!=(r&t.childLanes))||(oe(e,t,r,!1),n=0!=(r&t.childLanes)),o){if(n)return li(e,t,r);t.flags|=128}if(null!==(o=t.memoizedState)&&(o.rendering=null,o.tail=null,o.lastEffect=null),an(t,ar.current),!n)return null;break;case 22:return t.lanes=0,iY(e,t,r,t.pendingProps);case 24:n6(t,oc,e.memoizedState.cache)}return ls(e,t,r)}(e,t,r);iV=0!=(131072&e.flags)}else iV=!1,nq&&0!=(1048576&t.flags)&&nF(t,nz,t.index);switch(t.lanes=0,t.tag){case 16:e:{var n=t.pendingProps;if(e=oL(t.elementType),t.type=e,"function"==typeof e)nx(e)?(n=iR(e,n),t.tag=1,t=i3(null,t,e,n,r)):(t.tag=0,t=i1(null,t,e,n,r));else{if(null!=e){var o=e.$$typeof;if(o===I){t.tag=11,t=iq(null,t,e,n,r);break e}if(o===R){t.tag=14,t=iW(null,t,e,n,r);break e}if(o===L){t.tag=10,t.type=e,t=ll(null,t,r);break e}}throw Error(l(306,t=function e(t){if(null==t)return null;if("function"==typeof t)return t.$$typeof===$?null:t.displayName||t.name||null;if("string"==typeof t)return t;switch(t){case C:return"Fragment";case T:return"Profiler";case E:return"StrictMode";case P:return"Suspense";case z:return"SuspenseList";case M:return"Activity";case Z:return"ViewTransition"}if("object"==typeof t)switch(t.$$typeof){case S:return"Portal";case L:return t.displayName||"Context";case N:return(t._context.displayName||"Context")+".Consumer";case I:var r=t.render;return(t=t.displayName)||(t=""!==(t=r.displayName||r.name||"")?"ForwardRef("+t+")":"ForwardRef"),t;case R:return null!==(r=t.displayName||null)?r:e(t.type)||"Memo";case O:r=t._payload,t=t._init;try{return e(t(r))}catch(e){}}return null}(e)||e,""))}}return t;case 0:return i1(e,t,t.type,t.pendingProps,r);case 1:return o=iR(n=t.type,t.pendingProps),i3(e,t,n,o,r);case 3:e:{if(er(t,t.stateNode.containerInfo),null===e)throw Error(l(387));n=t.pendingProps;var a=t.memoizedState;o=a.element,oV(e,t),oG(t,n,null,r);var i=t.memoizedState;if(n6(t,oc,n=i.cache),n!==a.cache&&n7(t,[oc],r,!0),oX(),n=i.element,a.isDehydrated)if(a={element:n,isDehydrated:!1,cache:i.cache},t.updateQueue.baseState=a,t.memoizedState=a,256&t.flags){t=i4(e,t,n,r);break e}else if(n!==o){n2(o=nN(Error(l(424)),t)),t=i4(e,t,n,r);break e}else for(nB=uY((e=9===(e=t.stateNode.containerInfo).nodeType?e.body:"HTML"===e.nodeName?e.ownerDocument.body:e).firstChild),nV=t,nq=!0,nW=null,nK=!0,r=oU(t,null,n,r),t.child=r;r;)r.flags=-3&r.flags|4096,r=r.sibling;else{if(n0(),n===o){t=ls(e,t,r);break e}iB(e,t,n,r)}t=t.child}return t;case 26:return i0(e,t),null===e?(r=u9(t.type,null,t.pendingProps,null))?t.memoizedState=r:nq||(r=t.type,e=t.pendingProps,(n=uu(ee.current).createElement(r))[eW]=t,n[eK]=e,ui(n,r,e),e6(n),t.stateNode=n):t.memoizedState=u9(t.type,e.memoizedProps,t.pendingProps,e.memoizedState),null;case 27:return eo(t),null===e&&nq&&(n=t.stateNode=uJ(t.type,t.pendingProps,ee.current),nV=t,nK=!0,o=nB,ux(t.type)?(uX=o,nB=uY(n.firstChild)):nB=o),iB(e,t,t.pendingProps.children,r),i0(e,t),null===e&&(t.flags|=4194304),t.child;case 5:return null===e&&nq&&((o=n=nB)&&(null!==(n=function(e,t,r,n){for(;1===e.nodeType;){if(e.nodeName.toLowerCase()!==t.toLowerCase()){if(!n&&("INPUT"!==e.nodeName||"hidden"!==e.type))break}else if(n){if(!e[e0])switch(t){case"meta":if(!e.hasAttribute("itemprop"))break;return e;case"link":if("stylesheet"===(o=e.getAttribute("rel"))&&e.hasAttribute("data-precedence")||o!==r.rel||e.getAttribute("href")!==(null==r.href||""===r.href?null:r.href)||e.getAttribute("crossorigin")!==(null==r.crossOrigin?null:r.crossOrigin)||e.getAttribute("title")!==(null==r.title?null:r.title))break;return e;case"style":if(e.hasAttribute("data-precedence"))break;return e;case"script":if(((o=e.getAttribute("src"))!==(null==r.src?null:r.src)||e.getAttribute("type")!==(null==r.type?null:r.type)||e.getAttribute("crossorigin")!==(null==r.crossOrigin?null:r.crossOrigin))&&o&&e.hasAttribute("async")&&!e.hasAttribute("itemprop"))break;return e;default:return e}}else{if("input"!==t||"hidden"!==e.type)return e;var o=null==r.name?null:""+r.name;if("hidden"===r.type&&e.getAttribute("name")===o)return e}if(null===(e=uY(e.nextSibling)))break}return null}(n,t.type,t.pendingProps,nK))?(t.stateNode=n,nV=t,nB=uY(n.firstChild),nK=!1,o=!0):o=!1),o||nX(t)),eo(t),o=t.type,a=t.pendingProps,i=null!==e?e.memoizedProps:null,n=a.children,up(o,a)?n=null:null!==i&&up(o,i)&&(t.flags|=32),null!==t.memoizedState&&(dw._currentValue=o=ab(e,t,aw,null,null,r)),i0(e,t),iB(e,t,n,r),t.child;case 6:return null===e&&nq&&((e=r=nB)&&(null!==(r=function(e,t,r){if(""===t)return null;for(;3!==e.nodeType;)if((1!==e.nodeType||"INPUT"!==e.nodeName||"hidden"!==e.type)&&!r||null===(e=uY(e.nextSibling)))return null;return e}(r,t.pendingProps,nK))?(t.stateNode=r,nV=t,nB=null,e=!0):e=!1),e||nX(t)),null;case 13:return i8(e,t,r);case 4:return er(t,t.stateNode.containerInfo),n=t.pendingProps,null===e?t.child=oF(t,null,n,r):iB(e,t,n,r),t.child;case 11:return iq(e,t,t.type,t.pendingProps,r);case 7:return n=t.pendingProps,i0(e,t),iB(e,t,n,r),t.child;case 8:case 12:return iB(e,t,t.pendingProps.children,r),t.child;case 10:return ll(e,t,r);case 9:return o=t.type._context,n=t.pendingProps.children,or(t),n=n(o=on(o)),t.flags|=1,iB(e,t,n,r),t.child;case 14:return iW(e,t,t.type,t.pendingProps,r);case 15:return iK(e,t,t.type,t.pendingProps,r);case 19:return li(e,t,r);case 31:var s=e,c=t,u=r,d=c.pendingProps,f=0!=(128&c.flags);if(c.flags&=-129,null===s){if(nq){if("hidden"===d.mode)return s=iQ(c,d),c.lanes=0x20000000,iX(null,s);if(o8(c),(s=nB)?null!==(s=null!==(s=uq(s,nK))&&"&"===s.data?s:null)&&(c.memoizedState={dehydrated:s,treeContext:null!==nM?{id:nA,overflow:nD}:null,retryLane:0x20000000,hydrationErrors:null},(u=nC(s)).return=c,c.child=u,nV=c,nB=null):s=null,null===s)throw nX(c);return c.lanes=0x20000000,null}return iQ(c,d)}var p=s.memoizedState;if(null!==p){var h=p.dehydrated;if(o8(c),f)if(256&c.flags)c.flags&=-257,c=iJ(s,c,u);else if(null!==c.memoizedState)c.child=s.child,c.flags|=128,c=null;else throw Error(l(558));else if(iV||oe(s,c,u,!1),f=0!=(u&s.childLanes),iV||f){if(null!==(d=sC)&&0!==(h=eU(d,u))&&h!==p.retryLane)throw p.retryLane=h,nh(s,h),ce(d,s,h),iH;cd(),c=iJ(s,c,u)}else s=p.treeContext,nB=uY(h.nextSibling),nV=c,nq=!0,nW=null,nK=!1,null!==s&&nH(c,s),c=iQ(c,d),c.flags|=4096;return c}return(s=n_(s.child,{mode:d.mode,children:d.children})).ref=c.ref,c.child=s,s.return=c,s;case 22:return iY(e,t,r,t.pendingProps);case 24:return or(t),n=on(oc),null===e?(null===(o=o_())&&(o=sC,a=ou(),o.pooledCache=a,a.refCount++,null!==a&&(o.pooledCacheLanes|=r),o=a),t.memoizedState={parent:n,cache:o},oH(t),n6(t,oc,o)):(0!=(e.lanes&r)&&(oV(e,t),oG(t,null,null,r),oX()),o=e.memoizedState,a=t.memoizedState,o.parent!==n?(o={parent:n,cache:n},t.memoizedState=o,0===t.lanes&&(t.memoizedState=t.updateQueue.baseState=o),n6(t,oc,n)):(n6(t,oc,n=a.cache),n!==o.cache&&n7(t,[oc],r,!0))),iB(e,t,t.pendingProps.children,r),t.child;case 30:return null===t.stateNode&&(t.stateNode={autoName:null,paired:null,clones:null,ref:null}),null!=(n=t.pendingProps).name&&"auto"!==n.name?t.flags|=null===e?0x1202000:0x1200000:nq&&nU(t),null!==e&&e.memoizedProps.name!==n.name?t.flags|=4194816:i0(e,t),iB(e,t,n.children,r),t.child;case 29:throw t.pendingProps}throw Error(l(156,t.tag))}function ld(e){e.flags|=4}function lf(e,t,r,n,o){var a;if((a=0!=(32&e.mode))&&(a=null===r?dd(t,n):dd(t,n)&&(n.src!==r.src||n.srcSet!==r.srcSet)),a){if(e.flags|=0x1000000,(0x13ffff40&o)===o)if(e.stateNode.complete)e.flags|=8192;else if(cs())e.flags|=8192;else throw oI=oE,oS}else e.flags&=-0x1000001}function lp(e,t){if("stylesheet"!==t.type||0!=(4&t.state.loading))e.flags&=-0x1000001;else if(e.flags|=0x1000000,!df(t))if(cs())e.flags|=8192;else throw oI=oE,oS}function lh(e,t){null!==t&&(e.flags|=4),16384&e.flags&&(t=22!==e.tag?eM():0x20000000,e.lanes|=t,sF|=t)}function lm(e,t){if(!nq)switch(e.tailMode){case"visible":break;case"collapsed":for(var r=e.tail,n=null;null!==r;)null!==r.alternate&&(n=r),r=r.sibling;null===n?t||null===e.tail?e.tail=null:e.tail.sibling=null:n.sibling=null;break;default:for(r=null,t=e.tail;null!==t;)null!==t.alternate&&(r=t),t=t.sibling;null===r?e.tail=null:r.sibling=null}}function lg(e){var t=null!==e.alternate&&e.alternate.child===e.child,r=0,n=0;if(t)for(var o=e.child;null!==o;)r|=o.lanes|o.childLanes,n|=0x7f00000&o.subtreeFlags,n|=0x7f00000&o.flags,o.return=e,o=o.sibling;else for(o=e.child;null!==o;)r|=o.lanes|o.childLanes,n|=o.subtreeFlags,n|=o.flags,o.return=e,o=o.sibling;return e.subtreeFlags|=n,e.childLanes=r,t}function lv(e,t){switch(n$(t),t.tag){case 3:n9(oc),en();break;case 26:case 27:case 5:ea(t);break;case 4:en();break;case 31:null!==t.memoizedState&&at(t);break;case 13:at(t);break;case 19:ao(t);break;case 10:n9(t.type);break;case 22:case 23:at(t),o4(),null!==e&&X(ox);break;case 24:n9(oc)}}function ly(e,t){try{var r=t.updateQueue,n=null!==r?r.lastEffect:null;if(null!==n){var o=n.next;r=o;do{if((r.tag&e)===e){n=void 0;var a=r.create;r.inst.destroy=n=a()}r=r.next}while(r!==o)}}catch(e){cT(t,t.return,e)}}function lb(e,t,r){try{var n=t.updateQueue,o=null!==n?n.lastEffect:null;if(null!==o){var a=o.next;n=a;do{if((n.tag&e)===e){var i=n.inst,l=i.destroy;if(void 0!==l){i.destroy=void 0,o=t;try{l()}catch(e){cT(o,r,e)}}}n=n.next}while(n!==a)}}catch(e){cT(t,t.return,e)}}function lx(e){var t=e.updateQueue;if(null!==t){var r=e.stateNode;try{oJ(t,r)}catch(t){cT(e,e.return,t)}}}function l_(e,t,r){r.props=iR(e.type,e.memoizedProps),r.state=e.memoizedState;try{r.componentWillUnmount()}catch(r){cT(e,t,r)}}function lw(e,t){try{var r=e.ref;if(null!==r){switch(e.tag){case 26:case 27:case 5:var n=e.stateNode;break;case 30:var o=e.stateNode,a=no(e.memoizedProps,o);(null===o.ref||o.ref.name!==a)&&(o.ref=uL(a)),n=o.ref;break;case 7:if(null===e.stateNode){var i=new uI(e);f(e.child,!1,u$,i,void 0,void 0),e.stateNode=i}n=e.stateNode;break;default:n=e.stateNode}"function"==typeof r?e.refCleanup=r(n):r.current=n}}catch(r){cT(e,t,r)}}function lk(e,t){var r=e.ref,n=e.refCleanup;if(null!==r)if("function"==typeof n)try{n()}catch(r){cT(e,t,r)}finally{e.refCleanup=null,null!=(e=e.alternate)&&(e.refCleanup=null)}else if("function"==typeof r)try{r(null)}catch(r){cT(e,t,r)}else r.current=null}function lj(e){var t=e.type,r=e.memoizedProps,n=e.stateNode;try{switch(t){case"button":case"input":case"select":case"textarea":r.autoFocus&&n.focus();break;case"img":r.src?n.src=r.src:r.srcSet&&(n.srcset=r.srcSet)}}catch(t){cT(e,e.return,t)}}function lS(e,t,r){try{var n=e.stateNode;(function(e,t,r,n){switch(t){case"div":case"span":case"svg":case"path":case"a":case"g":case"p":case"li":break;case"input":var o=null,a=null,i=null,s=null,c=null,u=null,d=null;for(h in r){var f=r[h];if(r.hasOwnProperty(h)&&null!=f)switch(h){case"checked":case"value":break;case"defaultValue":c=f;default:n.hasOwnProperty(h)||uo(e,t,h,null,n,f)}}for(var p in n){var h=n[p];if(f=r[p],n.hasOwnProperty(p)&&(null!=h||null!=f))switch(p){case"type":h!==f&&(to=!0),a=h;break;case"name":h!==f&&(to=!0),o=h;break;case"checked":h!==f&&(to=!0),u=h;break;case"defaultChecked":h!==f&&(to=!0),d=h;break;case"value":h!==f&&(to=!0),i=h;break;case"defaultValue":h!==f&&(to=!0),s=h;break;case"children":case"dangerouslySetInnerHTML":if(null!=h)throw Error(l(137,t));break;default:h!==f&&uo(e,t,p,h,n,f)}}tg(e,i,s,c,u,d,a,o);return;case"select":for(a in h=i=s=p=null,r)if(c=r[a],r.hasOwnProperty(a)&&null!=c)switch(a){case"value":break;case"multiple":h=c;default:n.hasOwnProperty(a)||uo(e,t,a,null,n,c)}for(o in n)if(a=n[o],c=r[o],n.hasOwnProperty(o)&&(null!=a||null!=c))switch(o){case"value":a!==c&&(to=!0),p=a;break;case"defaultValue":a!==c&&(to=!0),s=a;break;case"multiple":a!==c&&(to=!0),i=a;default:a!==c&&uo(e,t,o,a,n,c)}t=s,r=i,n=h,null!=p?tb(e,!!r,p,!1):!!n!=!!r&&(null!=t?tb(e,!!r,t,!0):tb(e,!!r,r?[]:"",!1));return;case"textarea":for(s in h=p=null,r)if(o=r[s],r.hasOwnProperty(s)&&null!=o&&!n.hasOwnProperty(s))switch(s){case"value":case"children":break;default:uo(e,t,s,null,n,o)}for(i in n)if(o=n[i],a=r[i],n.hasOwnProperty(i)&&(null!=o||null!=a))switch(i){case"value":o!==a&&(to=!0),p=o;break;case"defaultValue":o!==a&&(to=!0),h=o;break;case"children":break;case"dangerouslySetInnerHTML":if(null!=o)throw Error(l(91));break;default:o!==a&&uo(e,t,i,o,n,a)}tx(e,p,h);return;case"option":for(var m in r)p=r[m],r.hasOwnProperty(m)&&null!=p&&!n.hasOwnProperty(m)&&("selected"===m?e.selected=!1:uo(e,t,m,null,n,p));for(c in n)p=n[c],h=r[c],n.hasOwnProperty(c)&&p!==h&&(null!=p||null!=h)&&("selected"===c?(p!==h&&(to=!0),e.selected=p&&"function"!=typeof p&&"symbol"!=typeof p):uo(e,t,c,p,n,h));return;case"img":case"link":case"area":case"base":case"br":case"col":case"embed":case"hr":case"keygen":case"meta":case"param":case"source":case"track":case"wbr":case"menuitem":for(var g in r)p=r[g],r.hasOwnProperty(g)&&null!=p&&!n.hasOwnProperty(g)&&uo(e,t,g,null,n,p);for(u in n)if(p=n[u],h=r[u],n.hasOwnProperty(u)&&p!==h&&(null!=p||null!=h))switch(u){case"children":case"dangerouslySetInnerHTML":if(null!=p)throw Error(l(137,t));break;default:uo(e,t,u,p,n,h)}return;default:if(tC(t)){for(var v in r)p=r[v],r.hasOwnProperty(v)&&void 0!==p&&!n.hasOwnProperty(v)&&ua(e,t,v,void 0,n,p);for(d in n)p=n[d],h=r[d],n.hasOwnProperty(d)&&p!==h&&(void 0!==p||void 0!==h)&&ua(e,t,d,p,n,h);return}}for(var y in r)p=r[y],r.hasOwnProperty(y)&&null!=p&&!n.hasOwnProperty(y)&&uo(e,t,y,null,n,p);for(f in n)p=n[f],h=r[f],n.hasOwnProperty(f)&&p!==h&&(null!=p||null!=h)&&uo(e,t,f,p,n,h)})(n,e.type,r,t),n[eK]=t}catch(t){cT(e,e.return,t)}}function lC(e,t){if((5===e.tag||6===e.tag)&&null===e.alternate&&null!==t)for(var r=0;r<t.length;r++)uV(e.stateNode,t[r])}function lE(e){for(var t=e.return;null!==t;){if(lN(t)){var r=t.stateNode,n=e.stateNode;if(3!==n.nodeType){var o=r._eventListeners;if(null!==o)for(var a=0;a<o.length;a++){var i=o[a];n.removeEventListener(i.type,i.listener,i.optionsOrUseCapture)}null!=n.reactFragments&&n.reactFragments.delete(r)}}if(lT(t))break;t=t.return}}function lT(e){return 5===e.tag||3===e.tag||26===e.tag||27===e.tag&&ux(e.type)||4===e.tag}function lN(e){return e&&7===e.tag&&null!==e.stateNode}function lL(e){e:for(;;){for(;null===e.sibling;){if(null===e.return||lT(e.return))return null;e=e.return}for(e.sibling.return=e.return,e=e.sibling;5!==e.tag&&6!==e.tag&&18!==e.tag;){if(27===e.tag&&ux(e.type)||2&e.flags||null===e.child||4===e.tag)continue e;e.child.return=e,e=e.child}if(!(2&e.flags))return e.stateNode}}function lI(e,t,r,n){var o=e.tag;if(5===o||6===o)o=e.stateNode,t?r.insertBefore(o,t):r.appendChild(o),lC(e,n),to=!0;else if(4!==o&&(27===o&&ux(e.type)&&(r=e.stateNode),null!==(e=e.child)))for(lI(e,t,r,n),e=e.sibling;null!==e;)lI(e,t,r,n),e=e.sibling}function lP(e){var t=e.stateNode,r=e.memoizedProps;try{for(var n=e.type,o=t.attributes;o.length;)t.removeAttributeNode(o[0]);ui(t,n,r),t[eW]=e,t[eK]=r}catch(t){cT(e,e.return,t)}}var lz=!1,lR=null;function lO(e){(30===e.tag||0!=(0x2000000&e.subtreeFlags))&&(lz=!0)}var lM=null;function lA(){var e=lM;return lM=null,e}var lD=0;function lZ(e,t,r,n,o){return lD=0,function e(t,r,n,o,a){for(var i=!1;null!==t;){if(5===t.tag){var l=t.stateNode;if(null!==o){var s=uC(l);o.push(s),s.view&&(i=!0)}else i||uC(l).view&&(i=!0);lz=!0,uk(l,0===lD?r:r+"_"+lD,n),lD++}else(22!==t.tag||null===t.memoizedState)&&(30===t.tag&&a||e(t.child,r,n,o,a)&&(i=!0));t=t.sibling}return i}(e.child,t,r,n,o)}function lF(e,t){for(;null!==e;)5===e.tag?uj(e.stateNode,e.memoizedProps):(22!==e.tag||null===e.memoizedState)&&(30===e.tag&&t||lF(e.child,t)),e=e.sibling}function lU(e){if(0!=(0x1200000&e.subtreeFlags))for(e=e.child;null!==e;){if((22!==e.tag||null===e.memoizedState)&&(lU(e),30===e.tag&&0!=(0x1200000&e.flags)&&e.stateNode.paired)){var t=e.memoizedProps;if(null==t.name||"auto"===t.name)throw Error(l(544));var r=t.name;"none"!==(t=ni(t.default,t.share))&&(lZ(e,r,t,null,!1)||lF(e.child,!1))}e=e.sibling}}function l$(e,t){if(30===e.tag){var r=e.stateNode,n=e.memoizedProps,o=no(n,r),a=ni(n.default,r.paired?n.share:n.enter);"none"!==a?lZ(e,o,a,null,!1)?(lU(e),r.paired||t||s7(e,n.onEnter)):lF(e.child,!1):lU(e)}else if(0!=(0x2000000&e.subtreeFlags))for(e=e.child;null!==e;)l$(e,t),e=e.sibling;else lU(e)}function lH(e){if(null!==lR&&0!==lR.size){var t=lR;if(0!=(0x1200000&e.subtreeFlags))for(e=e.child;null!==e;){if(22!==e.tag||null===e.memoizedState){if(30===e.tag&&0!=(0x1200000&e.flags)){var r=e.memoizedProps,n=r.name;if(null!=n&&"auto"!==n){var o=t.get(n);if(void 0!==o){var a=ni(r.default,r.share);if("none"!==a&&(lZ(e,n,a,null,!1)?(o.paired=a=e.stateNode,a.paired=o,s7(e,r.onShare)):lF(e.child,!1)),t.delete(n),0===t.size)break}}}lH(e)}e=e.sibling}}}function lV(e){if(30===e.tag){var t=e.memoizedProps,r=no(t,e.stateNode),n=null!==lR?lR.get(r):void 0,o=ni(t.default,void 0!==n?t.share:t.exit);"none"!==o&&(lZ(e,r,o,null,!1)?void 0!==n?(n.paired=o=e.stateNode,o.paired=n,lR.delete(r),s7(e,t.onShare)):s7(e,t.onExit):lF(e.child,!1)),null!==lR&&lH(e)}else if(0!=(0x2000000&e.subtreeFlags))for(e=e.child;null!==e;)lV(e),e=e.sibling;else null!==lR&&lH(e)}function lB(e){if(0!=(0x1200000&e.subtreeFlags))for(e=e.child;null!==e;){if(22!==e.tag||null===e.memoizedState){if(30===e.tag&&0!=(0x1200000&e.flags)){var t=e.stateNode;null!==t.paired&&(t.paired=null,lF(e.child,!1))}lB(e)}e=e.sibling}}function lq(e){if(30===e.tag)e.stateNode.paired=null,lF(e.child,!1),lB(e);else if(0!=(0x2000000&e.subtreeFlags))for(e=e.child;null!==e;)lq(e),e=e.sibling;else lB(e)}function lW(e,t,r,n,o,a,i){for(var l=!1;null!==t;){if(5===t.tag){var s=t.stateNode;if(null!==a&&lD<a.length){var c,u=a[lD],d=uC(s);if((u.view||d.view)&&(l=!0),c=0==(4&e.flags))if(d.clip)c=!0;else{c=u.rect;var f=d.rect;c=c.y!==f.y||c.x!==f.x||c.height!==f.height||c.width!==f.width}c&&(e.flags|=4),d.abs?d=!u.abs:(u=u.rect,d=d.rect,d=u.height!==d.height||u.width!==d.width),d&&(e.flags|=32)}else e.flags|=32;0!=(4&e.flags)&&uk(s,0===lD?r:r+"_"+lD,o),l&&0!=(4&e.flags)||(null===lM&&(lM=[]),lM.push(s,0===lD?n:n+"_"+lD,t.memoizedProps)),lD++}else(22!==t.tag||null===t.memoizedState)&&(30===t.tag&&i?e.flags|=32&t.flags:lW(e,t.child,r,n,o,a,i)&&(l=!0));t=t.sibling}return l}var lK=!1,lY=!1,lX=!1,lG=!1,lQ="function"==typeof WeakSet?WeakSet:Set,lJ=null,l0=!1,l1=!1,l2=!1,l3=!1;function l4(e){for(;null!==lJ;){var t=lJ,r=e,n=t.alternate,o=t.flags;switch(t.tag){case 0:case 11:case 15:if(0!=(4&o)&&null!==(n=null!==(n=t.updateQueue)?n.events:null))for(r=0;r<n.length;r++)(o=n[r]).ref.impl=o.nextImpl;break;case 1:if(0!=(1024&o)&&null!==n){r=void 0,o=n.memoizedProps,n=n.memoizedState;var a=t.stateNode;try{var i=iR(t.type,o);r=a.getSnapshotBeforeUpdate(i,n),a.__reactInternalSnapshotBeforeUpdate=r}catch(e){cT(t,t.return,e)}}break;case 3:if(0!=(1024&o)){if(9===(r=(n=t.stateNode.containerInfo).nodeType))uB(n);else if(1===r)switch(n.nodeName){case"HEAD":case"HTML":case"BODY":uB(n);break;default:n.textContent=""}}break;case 5:case 26:case 27:case 6:case 4:case 17:break;case 30:r&&null!==n&&(r=no(n.memoizedProps,n.stateNode),"none"!==(o=ni((o=t.memoizedProps).default,o.update))&&lZ(n,r,o,n.memoizedState=[],!0));break;default:if(0!=(1024&o))throw Error(l(163))}if(null!==(n=t.sibling)){n.return=t.return,lJ=n;break}lJ=t.return}}function l5(e,t,r){var n=r.flags;switch(r.tag){case 0:case 11:case 15:su(e,r),4&n&&ly(5,r);break;case 1:if(su(e,r),4&n)if(e=r.stateNode,null===t)try{e.componentDidMount()}catch(e){cT(r,r.return,e)}else{var o=iR(r.type,t.memoizedProps);t=t.memoizedState;try{e.componentDidUpdate(o,t,e.__reactInternalSnapshotBeforeUpdate)}catch(e){cT(r,r.return,e)}}64&n&&lx(r),512&n&&lw(r,r.return);break;case 3:if(su(e,r),64&n&&null!==(e=r.updateQueue)){if(t=null,null!==r.child)switch(r.child.tag){case 27:case 5:case 1:t=r.child.stateNode}try{oJ(e,t)}catch(e){cT(r,r.return,e)}}break;case 27:null===t&&4&n&&lP(r);case 26:case 5:su(e,r),null===t&&4&n&&lj(r),512&n&&lw(r,r.return);break;case 12:su(e,r);break;case 31:su(e,r),4&n&&st(e,r);break;case 13:su(e,r),4&n&&sr(e,r),64&n&&null!==(e=r.memoizedState)&&null!==(e=e.dehydrated)&&function(e,t){var r=e.ownerDocument;if("$~"===e.data)e._reactRetry=t;else if("$?"!==e.data||"loading"!==r.readyState)t();else{var n=function(){t(),r.removeEventListener("DOMContentLoaded",n)};r.addEventListener("DOMContentLoaded",n),e._reactRetry=n}}(e,r=cP.bind(null,r));break;case 22:if(!(n=null!==r.memoizedState||lK)){t=null!==t&&null!==t.memoizedState||lY,o=lK;var a=lY;lK=n,(lY=t)&&!a?function e(t,r,n){for(n=n&&0!=(8772&r.subtreeFlags),r=r.child;null!==r;){var o=r.alternate,a=t,i=r,l=i.flags;switch(i.tag){case 0:case 11:case 15:e(a,i,n),ly(4,i);break;case 1:if(e(a,i,n),"function"==typeof(a=(o=i).stateNode).componentDidMount)try{a.componentDidMount()}catch(e){cT(o,o.return,e)}if(null!==(a=(o=i).updateQueue)){var s=o.stateNode;try{var c=a.shared.hiddenCallbacks;if(null!==c)for(a.shared.hiddenCallbacks=null,a=0;a<c.length;a++)oQ(c[a],s)}catch(e){cT(o,o.return,e)}}n&&64&l&&lx(i),lw(i,i.return);break;case 27:lP(i);case 26:case 5:if(5===i.tag){s=i;for(var u=s.return;null!==u&&(lN(u)&&uV(s.stateNode,u.stateNode),!lT(u));)u=u.return}e(a,i,n),n&&null===o&&4&l&&lj(i),lw(i,i.return);break;case 12:e(a,i,n);break;case 31:e(a,i,n),n&&4&l&&st(a,i);break;case 13:e(a,i,n),n&&4&l&&sr(a,i);break;case 22:null===i.memoizedState&&e(a,i,n),lw(i,i.return);break;case 30:e(a,i,n),lw(i,i.return);break;case 7:lw(i,i.return);default:e(a,i,n)}r=r.sibling}}(e,r,0!=(8772&r.subtreeFlags)):su(e,r),lK=o,lY=a}break;case 30:su(e,r),512&n&&lw(r,r.return);break;case 7:512&n&&lw(r,r.return);default:su(e,r)}}function l6(e,t){for(e=e.child;null!==e;)(function e(t,r){switch(t.tag){case 5:case 26:try{var n=t.stateNode;if(r){var o=n.style;"function"==typeof o.setProperty?o.setProperty("display","none","important"):o.display="none"}else{var a=t.stateNode,i=t.memoizedProps.style,l=null!=i&&i.hasOwnProperty("display")?i.display:null;a.style.display=null==l||"boolean"==typeof l?"":(""+l).trim()}}catch(e){cT(t,t.return,e)}!function t(r,n){if(0x4000000&r.subtreeFlags)for(r=r.child;null!==r;){e:{var o=r;switch(o.tag){case 4:e(o,n);break e;case 22:null===o.memoizedState&&t(o,n);break e;default:t(o,n)}}r=r.sibling}}(t,r);break;case 6:try{t.stateNode.nodeValue=r?"":t.memoizedProps,to=!0}catch(e){cT(t,t.return,e)}break;case 18:try{var s=t.stateNode;r?uw(s,!0):uw(t.stateNode,!1)}catch(e){cT(t,t.return,e)}break;case 22:case 23:null===t.memoizedState&&l6(t,r);break;default:l6(t,r)}})(e,t),e=e.sibling}var l9=null,l8=!1;function l7(e,t,r){for(r=r.child;null!==r;)se(e,t,r),r=r.sibling}function se(e,t,r){if(eS&&"function"==typeof eS.onCommitFiberUnmount)try{eS.onCommitFiberUnmount(ej,r)}catch(e){}switch(r.tag){case 26:lY||lk(r,t),l7(e,t,r),r.memoizedState?r.memoizedState.count--:r.stateNode&&(r=r.stateNode).parentNode.removeChild(r);break;case 27:lY||lk(r,t);var n=l9,o=l8;ux(r.type)&&(l9=r.stateNode,l8=!1),l7(e,t,r),u0(r.stateNode),l9=n,l8=o;break;case 5:lY||lk(r,t),5!==r.tag&&6!==r.tag||lE(r);case 6:if(n=l9,o=l8,l9=null,l7(e,t,r),l9=n,l8=o,null!==l9)if(l8)try{(9===l9.nodeType?l9.body:"HTML"===l9.nodeName?l9.ownerDocument.body:l9).removeChild(r.stateNode),to=!0}catch(e){cT(r,t,e)}else try{l9.removeChild(r.stateNode),to=!0}catch(e){cT(r,t,e)}break;case 18:null!==l9&&(l8?(u_(9===(e=l9).nodeType?e.body:"HTML"===e.nodeName?e.ownerDocument.body:e,r.stateNode),d0(e)):u_(l9,r.stateNode));break;case 4:n=l9,o=l8,l9=r.stateNode.containerInfo,l8=!0,l7(e,t,r),l9=n,l8=o;break;case 0:case 11:case 14:case 15:lb(2,r,t),lY||lb(4,r,t),l7(e,t,r);break;case 1:lY||(lk(r,t),"function"==typeof(n=r.stateNode).componentWillUnmount&&l_(r,t,n)),l7(e,t,r);break;case 21:default:l7(e,t,r);break;case 22:lY=(n=lY)||null!==r.memoizedState,l7(e,t,r),lY=n;break;case 30:lk(r,t),l7(e,t,r);break;case 7:lY||lk(r,t),l7(e,t,r)}}function st(e,t){if(null===t.memoizedState&&null!==(e=t.alternate)&&null!==(e=e.memoizedState)){e=e.dehydrated;try{d0(e)}catch(e){cT(t,t.return,e)}}}function sr(e,t){if(null===t.memoizedState&&null!==(e=t.alternate)&&null!==(e=e.memoizedState)&&null!==(e=e.dehydrated))try{d0(e)}catch(e){cT(t,t.return,e)}}function sn(e,t){var r=function(e){switch(e.tag){case 31:case 13:case 19:var t=e.stateNode;return null===t&&(t=e.stateNode=new lQ),t;case 22:return null===(t=(e=e.stateNode)._retryCache)&&(t=e._retryCache=new lQ),t;default:throw Error(l(435,e.tag))}}(e);t.forEach(function(t){if(!r.has(t)){r.add(t);var n=cz.bind(null,e,t);t.then(n,n)}})}function so(e,t,r){var n=t.deletions;if(null!==n)for(var o=0;o<n.length;o++){var a=n[o],i=e,s=t,c=s;e:for(;null!==c;){switch(c.tag){case 27:if(ux(c.type)){l9=c.stateNode,l8=!1;break e}break;case 5:l9=c.stateNode,l8=!1;break e;case 3:case 4:l9=c.stateNode.containerInfo,l8=!0;break e}c=c.return}if(null===l9)throw Error(l(160));se(i,s,a),l9=null,l8=!1,null!==(i=a.alternate)&&(i.return=null),a.return=null}if(13886&t.subtreeFlags)for(t=t.child;null!==t;)si(t,e,r),t=t.sibling}var sa=null;function si(e,t,r){var n=e.alternate,o=e.flags;switch(e.tag){case 0:case 11:case 14:case 15:so(t,e,r),sl(e),4&o&&(lb(3,e,e.return),ly(3,e),lb(5,e,e.return));break;case 1:so(t,e,r),sl(e),512&o&&(lY||null===n||lk(n,n.return)),64&o&&lK&&null!==(e=e.updateQueue)&&null!==(n=e.callbacks)&&(t=e.shared.hiddenCallbacks,e.shared.hiddenCallbacks=null===t?n:t.concat(n));break;case 26:var a=sa;if(so(t,e,r),sl(e),512&o&&(lY||null===n||lk(n,n.return)),4&o)if(r=null!==n?n.memoizedState:null,t=e.memoizedState,null===n)if(null===t)if(null===e.stateNode){e:{n=e.type,t=e.memoizedProps,r=a.ownerDocument||a;t:switch(n){case"title":(!(o=r.getElementsByTagName("title")[0])||o[e0]||o[eW]||"http://www.w3.org/2000/svg"===o.namespaceURI||o.hasAttribute("itemprop"))&&(o=r.createElement(n),r.head.insertBefore(o,r.querySelector("head > title"))),ui(o,n,t),o[eW]=e,e6(o),n=o;break e;case"link":if(a=dc("link","href",r).get(n+(t.href||""))){for(var i=0;i<a.length;i++)if((o=a[i]).getAttribute("href")===(null==t.href||""===t.href?null:t.href)&&o.getAttribute("rel")===(null==t.rel?null:t.rel)&&o.getAttribute("title")===(null==t.title?null:t.title)&&o.getAttribute("crossorigin")===(null==t.crossOrigin?null:t.crossOrigin)){a.splice(i,1);break t}}ui(o=r.createElement(n),n,t),r.head.appendChild(o);break;case"meta":if(a=dc("meta","content",r).get(n+(t.content||""))){for(i=0;i<a.length;i++)if((o=a[i]).getAttribute("content")===(null==t.content?null:""+t.content)&&o.getAttribute("name")===(null==t.name?null:t.name)&&o.getAttribute("property")===(null==t.property?null:t.property)&&o.getAttribute("http-equiv")===(null==t.httpEquiv?null:t.httpEquiv)&&o.getAttribute("charset")===(null==t.charSet?null:t.charSet)){a.splice(i,1);break t}}ui(o=r.createElement(n),n,t),r.head.appendChild(o);break;default:throw Error(l(468,n))}o[eW]=e,e6(o),n=o}e.stateNode=n}else du(a,e.type,e.stateNode);else e.stateNode=dn(a,t,e.memoizedProps);else r!==t?(null===r?null!==n.stateNode&&(n=n.stateNode).parentNode.removeChild(n):r.count--,null===t?du(a,e.type,e.stateNode):dn(a,t,e.memoizedProps)):null===t&&null!==e.stateNode&&lS(e,e.memoizedProps,n.memoizedProps);break;case 27:so(t,e,r),sl(e),512&o&&(lY||null===n||lk(n,n.return)),null!==n&&4&o&&lS(e,e.memoizedProps,n.memoizedProps);break;case 5:if(a=lX,lX=!1,so(t,e,r),lX=a,sl(e),512&o&&(lY||null===n||lk(n,n.return)),32&e.flags){t=e.stateNode;try{tw(t,""),to=!0}catch(t){cT(e,e.return,t)}}4&o&&null!=e.stateNode&&(t=e.memoizedProps,lS(e,t,null!==n?n.memoizedProps:t)),1024&o&&(lG=!0);break;case 6:if(so(t,e,r),sl(e),4&o){if(null===e.stateNode)throw Error(l(162));n=e.memoizedProps,t=e.stateNode;try{t.nodeValue=n,to=!0}catch(t){cT(e,e.return,t)}}break;case 3:if(to=!1,ds=null,a=sa,sa=u3(t.containerInfo),so(t,e,r),sa=a,sl(e),4&o&&null!==n&&n.memoizedState.isDehydrated)try{d0(t.containerInfo)}catch(t){cT(e,e.return,t)}lG&&(lG=!1,function e(t){if(1024&t.subtreeFlags)for(t=t.child;null!==t;){var r=t;e(r),5===r.tag&&1024&r.flags&&(r=r.stateNode,dN=!0,r.reset(),dN=!1),t=t.sibling}}(e)),to=!1;break;case 4:n=lX,lX=lK,o=ta(),a=sa,sa=u3(e.stateNode.containerInfo),so(t,e,r),sl(e),sa=a,to&&l1&&(l2=!0),to=o,lX=n;break;case 12:so(t,e,r),sl(e);break;case 31:case 19:so(t,e,r),sl(e),4&o&&null!==(n=e.updateQueue)&&(e.updateQueue=null,sn(e,n));break;case 13:so(t,e,r),sl(e),8192&e.child.flags&&null!==e.memoizedState!=(null!==n&&null!==n.memoizedState)&&(sV=em()),4&o&&null!==(n=e.updateQueue)&&(e.updateQueue=null,sn(e,n));break;case 22:a=null!==e.memoizedState,i=null!==n&&null!==n.memoizedState;var s=lK,c=lY,u=lX;lK=s||a,lX=u||a,lY=c||i,so(t,e,r),lY=c,lX=u,lK=s,sl(e),8192&o&&((t=e.stateNode)._visibility=a?-2&t._visibility:1|t._visibility,a&&(null===n||i||lK||lY||function e(t){for(t=t.child;null!==t;){var r=t;switch(r.tag){case 0:case 11:case 14:case 15:lb(4,r,r.return),e(r);break;case 1:lk(r,r.return);var n=r.stateNode;"function"==typeof n.componentWillUnmount&&l_(r,r.return,n),e(r);break;case 27:u0(r.stateNode);case 26:case 5:lk(r,r.return),5!==r.tag&&6!==r.tag||lE(r),e(r);break;case 22:null===r.memoizedState&&e(r);break;case 30:lk(r,r.return),e(r);break;case 7:lk(r,r.return);default:e(r)}t=t.sibling}}(e)),!a&&lX||l6(e,a)),4&o&&null!==(n=e.updateQueue)&&null!==(t=n.retryQueue)&&(n.retryQueue=null,sn(e,t));break;case 30:512&o&&(lY||null===n||lk(n,n.return)),o=ta(),a=l1,i=(0x13ffff00&r)===r,s=e.memoizedProps,l1=i&&"none"!==ni(s.default,s.update),so(t,e,r),sl(e),i&&null!==n&&to&&(e.flags|=4),l1=a,to=o;break;case 21:break;case 7:n&&null!==n.stateNode&&(n.stateNode._fragmentFiber=e);default:so(t,e,r),sl(e)}}function sl(e){var t=e.flags;if(2&t){try{for(var r,n=null,o=e.return;null!==o;){if(lN(o)){var a=o.stateNode;null===n?n=[a]:n.push(a)}if(lT(o)){r=o;break}o=o.return}if(null==r)throw Error(l(160));switch(r.tag){case 27:var i=r.stateNode,s=lL(e);lI(e,s,i,n);break;case 5:var c=r.stateNode;32&r.flags&&(tw(c,""),r.flags&=-33);var u=lL(e);lI(e,u,c,n);break;case 3:case 4:var d=r.stateNode.containerInfo,f=lL(e);!function e(t,r,n,o){var a=t.tag;if(5===a||6===a)a=t.stateNode,r?(9===n.nodeType?n.body:"HTML"===n.nodeName?n.ownerDocument.body:n).insertBefore(a,r):((r=9===n.nodeType?n.body:"HTML"===n.nodeName?n.ownerDocument.body:n).appendChild(a),null!=(n=n._reactRootContainer)||null!==r.onclick||(r.onclick=tL)),lC(t,o),to=!0;else if(4!==a&&(27===a&&ux(t.type)&&(n=t.stateNode,r=null),null!==(t=t.child)))for(e(t,r,n,o),t=t.sibling;null!==t;)e(t,r,n,o),t=t.sibling}(e,f,d,n);break;default:throw Error(l(161))}}catch(t){cT(e,e.return,t)}e.flags&=-3}4096&t&&(e.flags&=-4097)}function ss(e,t){if(9270&t.subtreeFlags)for(t=t.child;null!==t;)sc(t,e),t=t.sibling;else!function e(t,r){for(t=t.child;null!==t;){if(30===t.tag){var n=t.memoizedProps,o=t.stateNode,a=no(n,o),i=ni(n.default,n.update);if(r)var l=null===(o=o.clones)?null:o.map(uE);else l=t.memoizedState,t.memoizedState=null;o=t;var s=t.child;lD=0,a=lW(o,s,a,a,i,l,!1),0!=(4&t.flags)&&a&&(r||s7(t,n.onUpdate))}else 0!=(0x2000000&t.subtreeFlags)&&e(t,r);t=t.sibling}}(t,!1)}function sc(e,t){var r=e.alternate;if(null===r)l$(e,!1);else switch(e.tag){case 3:if(l3=l0=!1,lA(),ss(t,e),!l0&&!l2){if(null!==(e=lM))for(var n=0;n<e.length;n+=3){r=e[n];var o=e[n+1];uj(r,e[n+2]),null!==(r=r.ownerDocument.documentElement)&&r.animate({opacity:[0,0],pointerEvents:["none","none"]},{duration:0,fill:"forwards",pseudoElement:"::view-transition-group("+o+")"})}null!==(e=9===(e=t.containerInfo).nodeType?e.documentElement:e.ownerDocument.documentElement)&&""===e.style.viewTransitionName&&(e.style.viewTransitionName="none",e.animate({opacity:[0,0],pointerEvents:["none","none"]},{duration:0,fill:"forwards",pseudoElement:"::view-transition-group(root)"}),e.animate({width:[0,0],height:[0,0]},{duration:0,fill:"forwards",pseudoElement:"::view-transition"})),l3=!0}lM=null;break;case 5:default:ss(t,e);break;case 4:n=l0,l0=!1,ss(t,e),l0&&(l2=!0),l0=n;break;case 22:null===e.memoizedState&&(null!==r.memoizedState?l$(e,!1):ss(t,e));break;case 30:n=l0,o=lA(),l0=!1,ss(t,e),l0&&(e.flags|=4);var a=e.memoizedProps,i=e.stateNode;t=no(a,i),i=no(r.memoizedProps,i);var l=ni(a.default,a.update);"none"===l?t=!1:(a=r.memoizedState,r.memoizedState=null,r=e.child,lD=0,t=lW(e,r,t,i,l,a,!0),lD!==(null===a?0:a.length)&&(e.flags|=32)),0!=(4&e.flags)&&t?(s7(e,e.memoizedProps.onUpdate),lM=o):null!==o&&(o.push.apply(o,lM),lM=o),l0=0!=(32&e.flags)||n}}function su(e,t){if(8772&t.subtreeFlags)for(t=t.child;null!==t;)l5(e,t.alternate,t),t=t.sibling}function sd(e,t){var r=null;null!==e&&null!==e.memoizedState&&null!==e.memoizedState.cachePool&&(r=e.memoizedState.cachePool.pool),e=null,null!==t.memoizedState&&null!==t.memoizedState.cachePool&&(e=t.memoizedState.cachePool.pool),e!==r&&(null!=e&&e.refCount++,null!=r&&od(r))}function sf(e,t){e=null,null!==t.alternate&&(e=t.alternate.memoizedState.cache),(t=t.memoizedState.cache)!==e&&(t.refCount++,null!=e&&od(e))}function sp(e,t,r,n){var o=(0x13ffff00&r)===r;if(t.subtreeFlags&(o?10262:10256))for(t=t.child;null!==t;)sh(e,t,r,n),t=t.sibling;else o&&function e(t){for(t=t.child;null!==t;)30===t.tag?lF(t.child,!1):0!=(0x2000000&t.subtreeFlags)&&e(t),t=t.sibling}(t)}function sh(e,t,r,n){var o=(0x13ffff00&r)===r;o&&null===t.alternate&&null!==t.return&&null!==t.return.alternate&&lq(t);var a=t.flags;switch(t.tag){case 0:case 11:case 15:sp(e,t,r,n),2048&a&&ly(9,t);break;case 1:case 31:case 13:default:sp(e,t,r,n);break;case 3:sp(e,t,r,n),o&&l3&&("root"===(e=9===(e=e.containerInfo).nodeType?e.body:"HTML"===e.nodeName?e.ownerDocument.body:e).style.viewTransitionName&&(e.style.viewTransitionName=""),null!==(e=e.ownerDocument.documentElement)&&"none"===e.style.viewTransitionName&&(e.style.viewTransitionName="")),2048&a&&(a=null,null!==t.alternate&&(a=t.alternate.memoizedState.cache),(t=t.memoizedState.cache)!==a&&(t.refCount++,null!=a&&od(a)));break;case 12:if(2048&a){sp(e,t,r,n),a=t.stateNode;try{var i=t.memoizedProps,l=i.id,s=i.onPostCommit;"function"==typeof s&&s(l,null===t.alternate?"mount":"update",a.passiveEffectDuration,-0)}catch(e){cT(t,t.return,e)}}else sp(e,t,r,n);break;case 23:break;case 22:i=t.stateNode,l=t.alternate,null!==t.memoizedState?(o&&null!==l&&null===l.memoizedState&&lq(l),2&i._visibility?sp(e,t,r,n):sm(e,t)):(o&&null!==l&&null!==l.memoizedState&&lq(t),2&i._visibility?sp(e,t,r,n):(i._visibility|=2,function e(t,r,n,o,a){for(a=a&&0!=(10256&r.subtreeFlags),r=r.child;null!==r;){var i=r,l=i.flags;switch(i.tag){case 0:case 11:case 15:e(t,i,n,o,a),ly(8,i);break;case 23:break;case 22:var s=i.stateNode;null!==i.memoizedState?2&s._visibility?e(t,i,n,o,a):sm(t,i):(s._visibility|=2,e(t,i,n,o,a)),a&&2048&l&&sd(i.alternate,i);break;case 24:e(t,i,n,o,a),a&&2048&l&&sf(i.alternate,i);break;default:e(t,i,n,o,a)}r=r.sibling}}(e,t,r,n,0!=(10256&t.subtreeFlags)))),2048&a&&sd(l,t);break;case 24:sp(e,t,r,n),2048&a&&sf(t.alternate,t);break;case 30:o&&null!==(a=t.alternate)&&(lF(a.child,!0),lF(t.child,!0)),sp(e,t,r,n)}}function sm(e,t){if(10256&t.subtreeFlags)for(t=t.child;null!==t;){var r=t,n=r.flags;switch(r.tag){case 22:sm(e,r),2048&n&&sd(r.alternate,r);break;case 24:sm(e,r),2048&n&&sf(r.alternate,r);break;default:sm(e,r)}t=t.sibling}}var sg=8192;function sv(e,t,r){if(e.subtreeFlags&sg)for(e=e.child;null!==e;)sy(e,t,r),e=e.sibling}function sy(e,t,r){switch(e.tag){case 26:sv(e,t,r),e.flags&sg&&(null!==e.memoizedState?function(e,t,r,n){if("stylesheet"===r.type&&("string"!=typeof n.media||!1!==matchMedia(n.media).matches)&&0==(4&r.state.loading)){if(null===r.instance){var o=u8(n.href),a=t.querySelector(u7(o));if(a){null!==(t=a._p)&&"object"==typeof t&&"function"==typeof t.then&&(e.count++,e=dv.bind(e),t.then(e,e)),r.state.loading|=4,r.instance=a,e6(a);return}a=t.ownerDocument||t,n=de(n),(o=u1.get(o))&&di(n,o),e6(a=a.createElement("link"));var i=a;i._p=new Promise(function(e,t){i.onload=e,i.onerror=t}),ui(a,"link",n),r.instance=a}null===e.stylesheets&&(e.stylesheets=new Map),e.stylesheets.set(r,t),(t=r.state.preload)&&0==(3&r.state.loading)&&(e.count++,r=dv.bind(e),t.addEventListener("load",r),t.addEventListener("error",r))}}(r,sa,e.memoizedState,e.memoizedProps):(e=e.stateNode,(0x13ffff40&t)===t&&dh(r,e)));break;case 5:sv(e,t,r),e.flags&sg&&(e=e.stateNode,(0x13ffff40&t)===t&&dh(r,e));break;case 3:case 4:var n=sa;sa=u3(e.stateNode.containerInfo),sv(e,t,r),sa=n;break;case 22:null===e.memoizedState&&(null!==(n=e.alternate)&&null!==n.memoizedState?(n=sg,sg=0x1000000,sv(e,t,r),sg=n):sv(e,t,r));break;case 30:if(0!=(e.flags&sg)&&null!=(n=e.memoizedProps.name)&&"auto"!==n){var o=e.stateNode;o.paired=null,null===lR&&(lR=new Map),lR.set(n,o)}sv(e,t,r);break;default:sv(e,t,r)}}function sb(e){var t=e.alternate;if(null!==t&&null!==(e=t.child)){t.child=null;do t=e.sibling,e.sibling=null,e=t;while(null!==e)}}function sx(e){var t=e.deletions;if(0!=(16&e.flags)){if(null!==t)for(var r=0;r<t.length;r++){var n=t[r];lJ=n,sw(n,e)}sb(e)}if(10256&e.subtreeFlags)for(e=e.child;null!==e;)s_(e),e=e.sibling}function s_(e){switch(e.tag){case 0:case 11:case 15:sx(e),2048&e.flags&&lb(9,e,e.return);break;case 3:case 12:default:sx(e);break;case 22:var t=e.stateNode;null!==e.memoizedState&&2&t._visibility&&(null===e.return||13!==e.return.tag)?(t._visibility&=-3,function e(t){var r=t.deletions;if(0!=(16&t.flags)){if(null!==r)for(var n=0;n<r.length;n++){var o=r[n];lJ=o,sw(o,t)}sb(t)}for(t=t.child;null!==t;){switch((r=t).tag){case 0:case 11:case 15:lb(8,r,r.return),e(r);break;case 22:2&(n=r.stateNode)._visibility&&(n._visibility&=-3,e(r));break;default:e(r)}t=t.sibling}}(e)):sx(e)}}function sw(e,t){for(;null!==lJ;){var r=lJ;switch(r.tag){case 0:case 11:case 15:lb(8,r,t);break;case 23:case 22:if(null!==r.memoizedState&&null!==r.memoizedState.cachePool){var n=r.memoizedState.cachePool.pool;null!=n&&n.refCount++}break;case 24:od(r.memoizedState.cache)}if(null!==(n=r.child))n.return=r,lJ=n;else for(r=e;null!==lJ;){var o=(n=lJ).sibling,a=n.return;if(!function e(t){var r=t.alternate;null!==r&&(t.alternate=null,e(r)),t.child=null,t.deletions=null,t.sibling=null,5===t.tag&&null!==(r=t.stateNode)&&e1(r),t.stateNode=null,t.return=null,t.dependencies=null,t.memoizedProps=null,t.memoizedState=null,t.pendingProps=null,t.stateNode=null,t.updateQueue=null}(n),n===r){lJ=null;break}if(null!==o){o.return=a,lJ=o;break}lJ=a}}}var sk={getCacheForType:function(e){var t=on(oc),r=t.data.get(e);return void 0===r&&(r=e(),t.data.set(e,r)),r},cacheSignal:function(){return on(oc).controller.signal}},sj="function"==typeof WeakMap?WeakMap:Map,sS=0,sC=null,sE=null,sT=0,sN=0,sL=null,sI=!1,sP=!1,sz=!1,sR=0,sO=0,sM=0,sA=0,sD=0,sZ=0,sF=0,sU=null,s$=null,sH=!1,sV=0,sB=0,sq=1/0,sW=null,sK=null,sY=0,sX=null,sG=null,sQ=0,sJ=0,s0=null,s1=null,s2=null,s3=null,s4=null,s5=0,s6=null;function s9(){return 0!=(2&sS)&&0!==sT?sT&-sT:null!==V.T?cW():eV()}function s8(){if(0===sZ)if(0==(0x20000000&sT)||nq){var e=eI;0==(3932160&(eI<<=1))&&(eI=262144),sZ=e}else sZ=0x20000000;return null!==(e=o5.current)&&(e.flags|=32),sZ}function s7(e,t){if(null!=t){var r=e.stateNode,n=r.ref;null===n&&(n=r.ref=uL(no(e.memoizedProps,r))),null===s3&&(s3=[]),s3.push(t.bind(null,n))}}function ce(e,t,r){(e===sC&&(2===sN||9===sN)||null!==e.cancelPendingCommit)&&(ci(e,0),cn(e,sT,sZ,!1)),eD(e,r),(0==(2&sS)||e!==sC)&&(e===sC&&(0==(2&sS)&&(sA|=r),4===sO&&cn(e,sT,sZ,!1)),cF(e))}function ct(e,t,r){if(0!=(6&sS))throw Error(l(327));for(var n=!r&&0==(127&t)&&0==(t&e.expiredLanes)||eO(e,t),o=n?function(e,t){var r=sS;sS|=2;var n=cc(),o=cu();sC!==e||sT!==t?(sW=null,sq=em()+500,ci(e,t)):sP=eO(e,t);e:for(;;)try{if(0!==sN&&null!==sE){t=sE;var a=sL;t:switch(sN){case 1:sN=0,sL=null,cm(e,t,a,1);break;case 2:case 9:if(oT(a)){sN=0,sL=null,ch(t);break}t=function(){2!==sN&&9!==sN||sC!==e||(sN=7),cF(e)},a.then(t,t);break e;case 3:sN=7;break e;case 4:sN=5;break e;case 7:oT(a)?(sN=0,sL=null,ch(t)):(sN=0,sL=null,cm(e,t,a,7));break;case 5:var i=null;switch(sE.tag){case 26:i=sE.memoizedState;case 5:case 27:var s=sE;if(i?df(i):s.stateNode.complete){sN=0,sL=null;var c=s.sibling;if(null!==c)sE=c;else{var u=s.return;null!==u?(sE=u,cg(u)):sE=null}break t}}sN=0,sL=null,cm(e,t,a,5);break;case 6:sN=0,sL=null,cm(e,t,a,6);break;case 8:ca(),sO=6;break e;default:throw Error(l(462))}}for(;null!==sE&&!ep();)cp(sE);break}catch(t){cl(e,t)}return(n5=n4=null,V.H=n,V.A=o,sS=r,null!==sE)?0:(sC=null,sT=0,nd(),sO)}(e,t):cf(e,t,!0),a=n;;){if(0===o)sP&&!n&&cn(e,t,0,!1);else{if(r=e.current.alternate,a&&!function(e){for(var t=e;;){var r=t.tag;if((0===r||11===r||15===r)&&16384&t.flags&&null!==(r=t.updateQueue)&&null!==(r=r.stores))for(var n=0;n<r.length;n++){var o=r[n],a=o.getSnapshot;o=o.value;try{if(!rF(a(),o))return!1}catch(e){return!1}}if(r=t.child,16384&t.subtreeFlags&&null!==r)r.return=t,t=r;else{if(t===e)break;for(;null===t.sibling;){if(null===t.return||t.return===e)return!0;t=t.return}t.sibling.return=t.return,t=t.sibling}}return!0}(r)){o=cf(e,t,!1),a=!1;continue}if(2===o){if(a=t,e.errorRecoveryDisabledLanes&a)var i=0;else i=0!=(i=-0x20000001&e.pendingLanes)?i:0x20000000&i?0x20000000:0;if(0!==i){t=i;e:{o=sU;var s=e.current.memoizedState.isDehydrated;if(s&&(ci(e,i).flags|=256),2!==(i=cf(e,i,!1))){if(sz&&!s){e.errorRecoveryDisabledLanes|=a,sA|=a,o=4;break e}a=s$,s$=o,null!==a&&(null===s$?s$=a:s$.push.apply(s$,a))}o=i}if(a=!1,2!==o)continue}}if(1===o){ci(e,0),cn(e,t,0,!0);break}e:{switch(n=e,a=o){case 0:case 1:throw Error(l(345));case 4:if((4194048&t)!==t&&(0x3c00000&t)!==t)break;case 6:cn(n,t,sZ,!sI);break e;case 2:s$=null;break;case 3:case 5:break;default:throw Error(l(329))}if((0x3c00000&t)===t&&10<(o=sV+300-em())){if(cn(n,t,sZ,!sI),0!==eR(n,0,!0))break e;sQ=t,n.timeoutHandle=um(cr.bind(null,n,r,s$,sW,sH,t,sZ,sA,sF,sI,a,"Throttled",-0,0),o);break e}cr(n,r,s$,sW,sH,t,sZ,sA,sF,sI,a,null,-0,0)}}break}cF(e)}function cr(e,t,r,n,o,a,i,l,s,c,u,d,f,p){e.timeoutHandle=-1;var h,m,g=t.subtreeFlags,v=(0x13ffff00&a)===a;if(d=null,(v||8192&g||0x1002000==(0x1002000&g))&&(lR=null,sy(t,a,d={stylesheets:null,count:0,imgCount:0,imgBytes:0,suspenseyImages:[],waitingForImages:!0,waitingForViewTransition:!1,unsuspend:tL}),v&&(g=d,null!=(v=(9===(v=e.containerInfo).nodeType?v:v.ownerDocument).__reactViewTransition)&&(g.count++,g.waitingForViewTransition=!0,g=dv.bind(g),v.finished.then(g,g))),null!==(h=d,m=g=(0x3c00000&a)===a?sV-em():(4194048&a)===a?sB-em():0,h.stylesheets&&0===h.count&&dx(h,h.stylesheets),g=0<h.count||0<h.imgCount?function(e){var t=setTimeout(function(){if(h.stylesheets&&dx(h,h.stylesheets),h.unsuspend){var e=h.unsuspend;h.unsuspend=null,e()}},6e4+m);0<h.imgBytes&&0===dm&&(dm=62500*function(){if("function"==typeof performance.getEntriesByType){for(var e=0,t=0,r=performance.getEntriesByType("resource"),n=0;n<r.length;n++){var o=r[n],a=o.transferSize,i=o.initiatorType,l=o.duration;if(a&&l&&ul(i)){for(i=0,l=o.responseEnd,n+=1;n<r.length;n++){var s=r[n],c=s.startTime;if(c>l)break;var u=s.transferSize,d=s.initiatorType;u&&ul(d)&&(i+=u*((s=s.responseEnd)<l?1:(l-c)/(s-c)))}if(--n,t+=8*(a+i)/(o.duration/1e3),10<++e)break}}if(0<e)return t/e/1e6}return navigator.connection&&"number"==typeof(e=navigator.connection.downlink)?e:5}());var r=setTimeout(function(){if(h.waitingForImages=!1,0===h.count&&(h.stylesheets&&dx(h,h.stylesheets),h.unsuspend)){var e=h.unsuspend;h.unsuspend=null,e()}},(h.imgBytes>dm?50:800)+m);return h.unsuspend=e,function(){h.unsuspend=null,clearTimeout(t),clearTimeout(r)}}:null))){sQ=a,e.cancelPendingCommit=g(cy.bind(null,e,t,a,r,n,o,i,l,s,c,u,d,null,f,p)),cn(e,a,i,!c);return}cy(e,t,a,r,n,o,i,l,s,c,u,d)}function cn(e,t,r,n){t&=~sD,t&=~sA,e.suspendedLanes|=t,e.pingedLanes&=~t,n&&(e.warmLanes|=t),n=e.expirationTimes;for(var o=t;0<o;){var a=31-eE(o),i=1<<a;n[a]=-1,o&=~i}0!==r&&eZ(e,r,t)}function co(){return 0!=(6&sS)||(cU(0,!1),!1)}function ca(){if(null!==sE){if(0===sN)var e=sE.return;else e=sE,n5=n4=null,aS(e),oR=null,oO=0,e=sE;for(;null!==e;)lv(e.alternate,e),e=e.return;sE=null}}function ci(e,t){var r=e.timeoutHandle;-1!==r&&(e.timeoutHandle=-1,ug(r)),null!==(r=e.cancelPendingCommit)&&(e.cancelPendingCommit=null,r()),sQ=0,ca(),sC=e,sE=r=n_(e.current,null),sT=t,sN=0,sL=null,sI=!1,sP=eO(e,t),sz=!1,sF=sZ=sD=sA=sM=sO=0,s$=sU=null,sH=!1,0!=(8&t)&&(t|=32&t);var n=e.entangledLanes;if(0!==n)for(e=e.entanglements,n&=t;0<n;){var o=31-eE(n),a=1<<o;t|=e[o],n&=~a}return sR=t,nd(),r}function cl(e,t){al=null,V.H=iC,t===oj||t===oC?(t=oP(),sN=3):t===oS?(t=oP(),sN=4):sN=t===iH?8:null!==t&&"object"==typeof t&&"function"==typeof t.then?6:1,sL=t,null===sE&&(sO=1,iD(e,nN(t,e.current)))}function cs(){var e=o5.current;return null===e||((4194048&sT)===sT?null===o6:((0x3c00000&sT)===sT||0!=(0x20000000&sT))&&e===o6)}function cc(){var e=V.H;return V.H=iC,null===e?iC:e}function cu(){var e=V.A;return V.A=sk,e}function cd(){sO=4,sI||(4194048&sT)!==sT&&null!==o5.current||(sP=!0),0==(0x7ffffff&sM)&&0==(0x7ffffff&sA)||null===sC||cn(sC,sT,sZ,!1)}function cf(e,t,r){var n=sS;sS|=2;var o=cc(),a=cu();(sC!==e||sT!==t)&&(sW=null,ci(e,t)),t=!1;var i=sO;e:for(;;)try{if(0!==sN&&null!==sE){var l=sE,s=sL;switch(sN){case 8:ca(),i=6;break e;case 3:case 2:case 9:case 6:null===o5.current&&(t=!0);var c=sN;if(sN=0,sL=null,cm(e,l,s,c),r&&sP){i=0;break e}break;default:c=sN,sN=0,sL=null,cm(e,l,s,c)}}(function(){for(;null!==sE;)cp(sE)})(),i=sO;break}catch(t){cl(e,t)}return t&&e.shellSuspendCounter++,n5=n4=null,sS=n,V.H=o,V.A=a,null===sE&&(sC=null,sT=0,nd()),i}function cp(e){var t=lu(e.alternate,e,sR);e.memoizedProps=e.pendingProps,null===t?cg(e):sE=t}function ch(e){var t=e,r=t.alternate;switch(t.tag){case 15:case 0:t=i2(r,t,t.pendingProps,t.type,void 0,sT);break;case 11:t=i2(r,t,t.pendingProps,t.type.render,t.ref,sT);break;case 5:aS(t);var n=t;n===nV&&(nq?(nQ(n),5===n.tag&&null!=n.stateNode&&(nB=n.stateNode)):(nQ(n),nq=!0));default:lv(r,t),t=lu(r,t=sE=nw(t,sR),sR)}e.memoizedProps=e.pendingProps,null===t?cg(e):sE=t}function cm(e,t,r,n){n5=n4=null,aS(t),oR=null,oO=0;var o=t.return;try{if(function(e,t,r,n,o){if(r.flags|=32768,null!==n&&"object"==typeof n&&"function"==typeof n.then){if(null!==(t=r.alternate)&&oe(t,r,o,!0),null!==(r=o5.current)){switch(r.tag){case 31:case 13:case 19:return null===o6?cd():null===r.alternate&&0===sO&&(sO=3),r.flags&=-257,r.flags|=65536,r.lanes=o,n===oE?r.flags|=16384:(null===(t=r.updateQueue)?r.updateQueue=new Set([n]):t.add(n),cN(e,n,o)),!1;case 22:return r.flags|=65536,n===oE?r.flags|=16384:(null===(t=r.updateQueue)?(t={transitions:null,markerInstances:null,retryQueue:new Set([n])},r.updateQueue=t):null===(r=t.retryQueue)?t.retryQueue=new Set([n]):r.add(n),cN(e,n,o)),!1}throw Error(l(435,r.tag))}return cN(e,n,o),cd(),!1}if(nq)return null!==(t=o5.current)?(0==(65536&t.flags)&&(t.flags|=256),t.flags|=65536,t.lanes=o,n!==nY&&n2(nN(e=Error(l(422),{cause:n}),r))):(n!==nY&&n2(nN(t=Error(l(423),{cause:n}),r)),e=e.current.alternate,e.flags|=65536,o&=-o,e.lanes|=o,n=nN(n,r),o=iF(e.stateNode,n,o),oK(e,o),4!==sO&&(sO=2)),!1;var a=Error(l(520),{cause:n});if(a=nN(a,r),null===sU?sU=[a]:sU.push(a),4!==sO&&(sO=2),null===t)return!0;n=nN(n,r),r=t;do{switch(r.tag){case 3:return r.flags|=65536,e=o&-o,r.lanes|=e,e=iF(r.stateNode,n,e),oK(r,e),!1;case 1:if(t=r.type,a=r.stateNode,0==(128&r.flags)&&("function"==typeof t.getDerivedStateFromError||null!==a&&"function"==typeof a.componentDidCatch&&(null===sK||!sK.has(a))))return r.flags|=65536,o&=-o,r.lanes|=o,i$(o=iU(o),e,r,n),oK(r,o),!1;break;case 22:if(null!==r.memoizedState)return r.flags|=65536,!1}r=r.return}while(null!==r);return!1}(e,o,t,r,sT)){sO=1,iD(e,nN(r,e.current)),sE=null;return}}catch(t){if(null!==o)throw sE=o,t;sO=1,iD(e,nN(r,e.current)),sE=null;return}32768&t.flags?(nq||1===n?e=!0:sP||0!=(0x20000000&sT)?e=!1:(sI=e=!0,(2===n||9===n||3===n||6===n)&&null!==(n=o5.current)&&13===n.tag&&(n.flags|=16384)),cv(t,e)):cg(t)}function cg(e){var t=e;do{if(0!=(32768&t.flags))return void cv(t,sI);e=t.return;var r=function(e,t,r){var n=t.pendingProps;switch(n$(t),t.tag){case 16:case 15:case 0:case 11:case 7:case 8:case 12:case 9:case 14:case 1:return lg(t),null;case 3:return r=t.stateNode,n=null,null!==e&&(n=e.memoizedState.cache),t.memoizedState.cache!==n&&(t.flags|=2048),n9(oc),en(),r.pendingContext&&(r.context=r.pendingContext,r.pendingContext=null),(null===e||null===e.child)&&(nJ(t)?ld(t):null===e||e.memoizedState.isDehydrated&&0==(256&t.flags)||(t.flags|=1024,n1())),lg(t),null;case 26:var o=t.type,a=t.memoizedState;return null===e?(ld(t),null!==a?(lg(t),lp(t,a)):(lg(t),lf(t,o,null,n,r))):a?a!==e.memoizedState?(ld(t),lg(t),lp(t,a)):(lg(t),t.flags&=-0x1000001):((e=e.memoizedProps)!==n&&ld(t),lg(t),lf(t,o,e,n,r)),null;case 27:if(ea(t),r=ee.current,o=t.type,null!==e&&null!=t.stateNode)e.memoizedProps!==n&&ld(t);else{if(!n){if(null===t.stateNode)throw Error(l(166));return lg(t),t.subtreeFlags&=-0x2000001,null}e=Q.current,nJ(t)?nG(t,e):(t.stateNode=e=uJ(o,n,r),ld(t))}return lg(t),t.subtreeFlags&=-0x2000001,null;case 5:if(ea(t),o=t.type,null!==e&&null!=t.stateNode)e.memoizedProps!==n&&ld(t);else{if(!n){if(null===t.stateNode)throw Error(l(166));return lg(t),t.subtreeFlags&=-0x2000001,null}if(a=Q.current,nJ(t))nG(t,a);else{var i=uu(ee.current);switch(a){case 1:a=i.createElementNS("http://www.w3.org/2000/svg",o);break;case 2:a=i.createElementNS("http://www.w3.org/1998/Math/MathML",o);break;default:switch(o){case"svg":a=i.createElementNS("http://www.w3.org/2000/svg",o);break;case"math":a=i.createElementNS("http://www.w3.org/1998/Math/MathML",o);break;case"script":(a=i.createElement("div")).innerHTML="<script><\/script>",a=a.removeChild(a.firstChild);break;case"select":a="string"==typeof n.is?i.createElement("select",{is:n.is}):i.createElement("select"),n.multiple?a.multiple=!0:n.size&&(a.size=n.size);break;default:a="string"==typeof n.is?i.createElement(o,{is:n.is}):i.createElement(o)}}a[eW]=t,a[eK]=n;e:for(i=t.child;null!==i;){if(5===i.tag||6===i.tag)a.appendChild(i.stateNode);else if(4!==i.tag&&27!==i.tag&&null!==i.child){i.child.return=i,i=i.child;continue}if(i===t)break;for(;null===i.sibling;){if(null===i.return||i.return===t)break e;i=i.return}i.sibling.return=i.return,i=i.sibling}switch(t.stateNode=a,ui(a,o,n),o){case"button":case"input":case"select":case"textarea":n=!!n.autoFocus;break;case"img":n=!0;break;default:n=!1}n&&ld(t)}}return lg(t),t.subtreeFlags&=-0x2000001,lf(t,t.type,null===e?null:e.memoizedProps,t.pendingProps,r),null;case 6:if(e&&null!=t.stateNode)e.memoizedProps!==n&&ld(t);else{if("string"!=typeof n&&null===t.stateNode)throw Error(l(166));if(e=ee.current,nJ(t)){if(e=t.stateNode,r=t.memoizedProps,n=null,null!==(o=nV))switch(o.tag){case 27:case 5:n=o.memoizedProps}e[eW]=t,(e=!!(e.nodeValue===r||null!==n&&!0===n.suppressHydrationWarning||un(e.nodeValue,r)))||nX(t,!0)}else(e=uu(e).createTextNode(n))[eW]=t,t.stateNode=e}return lg(t),null;case 31:if(r=t.memoizedState,null===e||null!==e.memoizedState){if(n=nJ(t),null!==r){if(null===e){if(!n)throw Error(l(318));if(!(e=null!==(e=t.memoizedState)?e.dehydrated:null))throw Error(l(557));e[eW]=t}else n0(),0==(128&t.flags)&&(t.memoizedState=null),t.flags|=4;lg(t),e=!1}else r=n1(),null!==e&&null!==e.memoizedState&&(e.memoizedState.hydrationErrors=r),e=!0;if(!e){if(256&t.flags)return at(t),t;return at(t),null}if(0!=(128&t.flags))throw Error(l(558))}return lg(t),null;case 13:if(n=t.memoizedState,null===e||null!==e.memoizedState&&null!==e.memoizedState.dehydrated){if(o=nJ(t),null!==n&&null!==n.dehydrated){if(null===e){if(!o)throw Error(l(318));if(!(o=null!==(o=t.memoizedState)?o.dehydrated:null))throw Error(l(317));o[eW]=t}else n0(),0==(128&t.flags)&&(t.memoizedState=null),t.flags|=4;lg(t),o=!1}else o=n1(),null!==e&&null!==e.memoizedState&&(e.memoizedState.hydrationErrors=o),o=!0;if(!o){if(256&t.flags)return at(t),t;return at(t),null}}if(at(t),0!=(128&t.flags))return t.lanes=r,t;return r=null!==n,e=null!==e&&null!==e.memoizedState,r&&(n=t.child,o=null,null!==n.alternate&&null!==n.alternate.memoizedState&&null!==n.alternate.memoizedState.cachePool&&(o=n.alternate.memoizedState.cachePool.pool),a=null,null!==n.memoizedState&&null!==n.memoizedState.cachePool&&(a=n.memoizedState.cachePool.pool),a!==o&&(n.flags|=2048)),r!==e&&r&&(t.child.flags|=8192),lh(t,t.updateQueue),lg(t),null;case 4:return en(),null===e&&c3(t.stateNode.containerInfo),t.flags|=0x4000000,lg(t),null;case 10:return n9(t.type),lg(t),null;case 19:if(ao(t),null===(n=t.memoizedState))return lg(t),null;if(o=0!=(128&t.flags),null===(a=n.rendering))if(o)lm(n,!1);else{if(0!==sO||null!==e&&0!=(128&e.flags))for(e=t.child;null!==e;){if(null!==(a=aa(e))){for(t.flags|=128,lm(n,!1),t.updateQueue=e=a.updateQueue,lh(t,e),t.subtreeFlags=0,e=r,r=t.child;null!==r;)nw(r,e),r=r.sibling;return an(t,1&ar.current|2),nq&&nZ(t,n.treeForkCount),t.child}e=e.sibling}null!==n.tail&&em()>sq&&(t.flags|=128,o=!0,lm(n,!1),t.lanes=4194304)}else{if(!o)if(null!==(e=aa(a))){if(t.flags|=128,o=!0,t.updateQueue=e=e.updateQueue,lh(t,e),lm(n,!0),null===n.tail&&"collapsed"!==n.tailMode&&"visible"!==n.tailMode&&!a.alternate&&!nq)return lg(t),null}else 2*em()-n.renderingStartTime>sq&&0x20000000!==r&&(t.flags|=128,o=!0,lm(n,!1),t.lanes=4194304);n.isBackwards?(a.sibling=t.child,t.child=a):(null!==(e=n.last)?e.sibling=a:t.child=a,n.last=a)}if(null!==n.tail){e=n.tail;e:{for(r=e;null!==r;){if(null!==r.alternate){r=!1;break e}r=r.sibling}r=!0}return n.rendering=e,n.tail=e.sibling,n.renderingStartTime=em(),e.sibling=null,a=ar.current,a=o?1&a|2:1&a,"visible"===n.tailMode||"collapsed"===n.tailMode||!r||nq?an(t,a):(r=a,G(o5,t),G(ar,r),null===o6&&(o6=t)),nq&&nZ(t,n.treeForkCount),e}return lg(t),null;case 22:case 23:return at(t),o4(),n=null!==t.memoizedState,null!==e?null!==e.memoizedState!==n&&(t.flags|=8192):n&&(t.flags|=8192),n?0!=(0x20000000&r)&&0==(128&t.flags)&&(lg(t),6&t.subtreeFlags&&(t.flags|=8192)):lg(t),null!==(r=t.updateQueue)&&lh(t,r.retryQueue),r=null,null!==e&&null!==e.memoizedState&&null!==e.memoizedState.cachePool&&(r=e.memoizedState.cachePool.pool),n=null,null!==t.memoizedState&&null!==t.memoizedState.cachePool&&(n=t.memoizedState.cachePool.pool),n!==r&&(t.flags|=2048),null!==e&&X(ox),null;case 24:return r=null,null!==e&&(r=e.memoizedState.cache),t.memoizedState.cache!==r&&(t.flags|=2048),n9(oc),lg(t),null;case 25:return null;case 30:return t.flags|=0x2000000,lg(t),null}throw Error(l(156,t.tag))}(t.alternate,t,sR);if(null!==r){sE=r;return}if(null!==(t=t.sibling)){sE=t;return}sE=t=e}while(null!==t);0===sO&&(sO=5)}function cv(e,t){do{var r=function(e,t){switch(n$(t),t.tag){case 1:return 65536&(e=t.flags)?(t.flags=-65537&e|128,t):null;case 3:return n9(oc),en(),0!=(65536&(e=t.flags))&&0==(128&e)?(t.flags=-65537&e|128,t):null;case 26:case 27:case 5:return ea(t),null;case 31:if(null!==t.memoizedState){if(at(t),null===t.alternate)throw Error(l(340));n0()}return 65536&(e=t.flags)?(t.flags=-65537&e|128,t):null;case 13:if(at(t),null!==(e=t.memoizedState)&&null!==e.dehydrated){if(null===t.alternate)throw Error(l(340));n0()}return 65536&(e=t.flags)?(t.flags=-65537&e|128,t):null;case 19:return ao(t),65536&(e=t.flags)?(t.flags=-65537&e|128,null!==(e=t.memoizedState)&&(e.rendering=null,e.tail=null),t.flags|=4,t):null;case 4:return en(),null;case 10:return n9(t.type),null;case 22:case 23:return at(t),o4(),null!==e&&X(ox),65536&(e=t.flags)?(t.flags=-65537&e|128,t):null;case 24:return n9(oc),null;default:return null}}(e.alternate,e);if(null!==r){r.flags&=32767,sE=r;return}if(null!==(r=e.return)&&(r.flags|=32768,r.subtreeFlags=0,r.deletions=null),!t&&null!==(e=e.sibling)){sE=e;return}sE=e=r}while(null!==e);sO=6,sE=null}function cy(e,t,r,n,o,a,i,s,c,u,d,f){e.cancelPendingCommit=null;do cS();while(0!==sY);if(0!=(6&sS))throw Error(l(327));if(null!==t){if(t===e.current)throw Error(l(177));e===sC&&(sE=sC=null,sT=0),sG=t,sX=e,sQ=r,s0=o,s1=n,function(e,t,r,n,o,a,i){var l,s=t.lanes|t.childLanes;if(sJ=s,!function(e,t,r,n,o,a){var i=e.pendingLanes;e.pendingLanes=r,e.suspendedLanes=0,e.pingedLanes=0,e.warmLanes=0,e.expiredLanes&=r,e.entangledLanes&=r,e.errorRecoveryDisabledLanes&=r,e.shellSuspendCounter=0;var l=e.entanglements,s=e.expirationTimes,c=e.hiddenUpdates;for(r=i&~r;0<r;){var u=31-eE(r),d=1<<u;l[u]=0,s[u]=-1;var f=c[u];if(null!==f)for(c[u]=null,u=0;u<f.length;u++){var p=f[u];null!==p&&(p.lane&=-0x20000001)}r&=~d}0!==n&&eZ(e,n,0),0!==a&&0===o&&0!==e.tag&&(e.suspendedLanes|=a&~(i&~t))}(e,r,s|=nu,n,o,a),s3=null,(0x13ffff00&r)===r?(l=e.transitionTypes,e.transitionTypes=null,s4=l,n=10262):(s4=null,n=10256),0!=(t.subtreeFlags&n)||0!=(t.flags&n)?(e.callbackNode=null,e.callbackPriority=0,ed(eb,function(){return cC(),null})):(e.callbackNode=null,e.callbackPriority=0),lz=!1,n=0!=(13878&t.flags),0!=(13878&t.subtreeFlags)||n){n=V.T,V.T=null,o=B.p,B.p=2,a=sS,sS|=4;try{!function(e,t,r){if(e=e.containerInfo,us=dN,rB(e=rV(e))){if("selectionStart"in e)var n={start:e.selectionStart,end:e.selectionEnd};else e:{var o=(n=(n=e.ownerDocument)&&n.defaultView||window).getSelection&&n.getSelection();if(o&&0!==o.rangeCount){n=o.anchorNode;var a,i=o.anchorOffset,l=o.focusNode;o=o.focusOffset;try{n.nodeType,l.nodeType}catch(e){n=null;break e}var s=0,c=-1,u=-1,d=0,f=0,p=e,h=null;t:for(;;){for(;p!==n||0!==i&&3!==p.nodeType||(c=s+i),p!==l||0!==o&&3!==p.nodeType||(u=s+o),3===p.nodeType&&(s+=p.nodeValue.length),null!==(a=p.firstChild);)h=p,p=a;for(;;){if(p===e)break t;if(h===n&&++d===i&&(c=s),h===l&&++f===o&&(u=s),null!==(a=p.nextSibling))break;h=(p=h).parentNode}p=a}n=-1===c||-1===u?null:{start:c,end:u}}else n=null}n=n||{start:0,end:0}}else n=null;for(uc={focusedElem:e,selectionRange:n},dN=!1,r=(0x13ffff00&r)===r,lJ=t,t=r?9270:1028;null!==lJ;){if(e=lJ,r&&null!==(n=e.deletions))for(i=0;i<n.length;i++)r&&lV(n[i]);if(null===e.alternate&&0!=(2&e.flags))r&&lO(e),l4(r);else{if(22===e.tag){if(n=e.alternate,null!==e.memoizedState){null!==n&&null===n.memoizedState&&r&&lV(n),l4(r);continue}else if(null!==n&&null!==n.memoizedState){r&&lO(e),l4(r);continue}}n=e.child,0!=(e.subtreeFlags&t)&&null!==n?(n.return=e,lJ=n):(r&&function e(t){for(t=t.child;null!==t;){if(30===t.tag){var r=t.memoizedProps,n=no(r,t.stateNode);r=ni(r.default,r.update),t.flags&=-5,"none"!==r&&lZ(t,n,r,t.memoizedState=[],!1)}else 0!=(0x2000000&t.subtreeFlags)&&e(t);t=t.sibling}}(e),l4(r))}}lR=null}(e,t,r)}finally{sS=a,B.p=o,V.T=n}}sY=1,lz?s2=function(e,t,r,n,o,a,i,l,s){var c=9===t.nodeType?t:t.ownerDocument;try{var u=c.startViewTransition({update:function(){var t=c.defaultView,r=t.navigation&&t.navigation.transition,i=c.fonts.status;n();var l=[];if("loaded"===i&&(c.documentElement.clientHeight,"loading"===c.fonts.status&&l.push(c.fonts.ready)),i=l.length,null!==e)for(var s=e.suspenseyImages,u=0,d=0;d<s.length;d++){var f=s[d];if(!f.complete){var p=f.getBoundingClientRect();if(0<p.bottom&&0<p.right&&p.top<t.innerHeight&&p.left<t.innerWidth){if((u+=dp(f))>dm){l.length=i;break}f=new Promise(uT.bind(f)),l.push(f)}}}return 0<l.length?(t=Promise.race([Promise.all(l),new Promise(function(e){return setTimeout(e,500)})]).then(o,o),(r?Promise.allSettled([r.finished,t]):t).then(a,a)):(o(),r)?r.finished.then(a,a):void a()},types:r});c.__reactViewTransition=u;var d=[];return u.ready.then(function(){for(var e=c.documentElement.getAnimations({subtree:!0}),t=0;t<e.length;t++){var r=e[t],n=r.effect,o=n.pseudoElement;if(null!=o&&o.startsWith("::view-transition")){d.push(r),r=n.getKeyframes();for(var a=o=void 0,l=!0,s=0;s<r.length;s++){var u=r[s],f=u.width;if(void 0===o)o=f;else if(o!==f){l=!1;break}if(f=u.height,void 0===a)a=f;else if(a!==f){l=!1;break}delete u.width,delete u.height,"none"===u.transform&&delete u.transform}l&&void 0!==o&&void 0!==a&&(n.setKeyframes(r),(l=getComputedStyle(n.target,n.pseudoElement)).width!==o||l.height!==a)&&((l=r[0]).width=o,l.height=a,(l=r[r.length-1]).width=o,l.height=a,n.setKeyframes(r))}}i()},function(e){c.__reactViewTransition===u&&(c.__reactViewTransition=null);try{"object"==typeof e&&null!==e&&"InvalidStateError"===e.name&&("View transition was skipped because document visibility state is hidden."===e.message||"Skipping view transition because document visibility state has become hidden."===e.message||"Skipping view transition because viewport size changed."===e.message||"Transition was aborted because of invalid state"===e.message)&&(e=null),null!==e&&s(e)}finally{n(),o(),i()}}),u.finished.finally(function(){for(var e=0;e<d.length;e++)d[e].cancel();c.__reactViewTransition===u&&(c.__reactViewTransition=null),l()}),u}catch(e){return n(),o(),i(),null}}(i,e.containerInfo,s4,c_,cw,cx,ck,cC,cb,null,null):(c_(),cw(),ck())}(e,t,r,i,s,c,f)}}function cb(e){0!==sY&&(0,sX.onRecoverableError)(e,{componentStack:null})}function cx(){3===sY&&(sY=0,sc(sG,sX),sY=4)}function c_(){if(1===sY){sY=0;var e=sX,t=sG,r=sQ,n=0!=(13878&t.flags);if(0!=(13878&t.subtreeFlags)||n){n=V.T,V.T=null;var o=B.p;B.p=2;var a=sS;sS|=4;try{l1=l2=!1,si(t,e,r),r=uc;var i=rV(e.containerInfo),l=r.focusedElem,s=r.selectionRange;if(i!==l&&l&&l.ownerDocument&&function e(t,r){return!!t&&!!r&&(t===r||(!t||3!==t.nodeType)&&(r&&3===r.nodeType?e(t,r.parentNode):"contains"in t?t.contains(r):!!t.compareDocumentPosition&&!!(16&t.compareDocumentPosition(r))))}(l.ownerDocument.documentElement,l)){if(null!==s&&rB(l)){var c=s.start,u=s.end;if(void 0===u&&(u=c),"selectionStart"in l)l.selectionStart=c,l.selectionEnd=Math.min(u,l.value.length);else{var d=l.ownerDocument||document,f=d&&d.defaultView||window;if(f.getSelection){var p=f.getSelection(),h=l.textContent.length,m=Math.min(s.start,h),g=void 0===s.end?m:Math.min(s.end,h);!p.extend&&m>g&&(i=g,g=m,m=i);var v=rH(l,m),y=rH(l,g);if(v&&y&&(1!==p.rangeCount||p.anchorNode!==v.node||p.anchorOffset!==v.offset||p.focusNode!==y.node||p.focusOffset!==y.offset)){var b=d.createRange();b.setStart(v.node,v.offset),p.removeAllRanges(),m>g?(p.addRange(b),p.extend(y.node,y.offset)):(b.setEnd(y.node,y.offset),p.addRange(b))}}}}for(d=[],p=l;p=p.parentNode;)1===p.nodeType&&d.push({element:p,left:p.scrollLeft,top:p.scrollTop});for("function"==typeof l.focus&&l.focus(),l=0;l<d.length;l++){var x=d[l];x.element.scrollLeft=x.left,x.element.scrollTop=x.top}}dN=!!us,uc=us=null}finally{sS=a,B.p=o,V.T=n}}e.current=t,sY=2}}function cw(){if(2===sY){sY=0;var e=sX,t=sG,r=0!=(8772&t.flags);if(0!=(8772&t.subtreeFlags)||r){r=V.T,V.T=null;var n=B.p;B.p=2;var o=sS;sS|=4;try{l5(e,t.alternate,t)}finally{sS=o,B.p=n,V.T=r}}sY=3}}function ck(){if(4===sY||3===sY){sY=0;var e=s2;s2=null,eh();var t=sX,r=sG,n=sQ,o=s1,a=(0x13ffff00&n)===n?10262:10256;if(0!=(r.subtreeFlags&a)||0!=(r.flags&a)?sY=5:(sY=0,sG=sX=null,cj(t,t.pendingLanes)),0===(a=t.pendingLanes)&&(sK=null),eH(n),r=r.stateNode,eS&&"function"==typeof eS.onCommitFiberRoot)try{eS.onCommitFiberRoot(ej,r,void 0,128==(128&r.current.flags))}catch(e){}if(null!==o){r=V.T,a=B.p,B.p=2,V.T=null;try{for(var i=t.onRecoverableError,l=0;l<o.length;l++){var s=o[l];i(s.value,{componentStack:s.stack})}}finally{V.T=r,B.p=a}}if(o=s3,i=s4,s4=null,null!==o&&(s3=null,null===i&&(i=[]),null!==e))for(s=0;s<o.length;s++)void 0!==(r=(0,o[s])(i))&&e.finished.finally(r);0!=(3&sQ)&&cS(),cF(t),a=t.pendingLanes,0!=(261930&n)&&0!=(42&a)?t===s6?s5++:(s5=0,s6=t):s5=0,cU(0,!1)}}function cj(e,t){0==(e.pooledCacheLanes&=t)&&null!=(t=e.pooledCache)&&(e.pooledCache=null,od(t))}function cS(){return null!==s2&&(s2.skipTransition(),s2=null),c_(),cw(),ck(),cC()}function cC(){if(5!==sY)return!1;var e=sX,t=sJ;sJ=0;var r=eH(sQ),n=V.T,o=B.p;try{B.p=32>r?32:r,V.T=null,r=s0,s0=null;var a=sX,i=sQ;if(sY=0,sG=sX=null,sQ=0,0!=(6&sS))throw Error(l(331));var s=sS;if(sS|=4,s_(a.current),sh(a,a.current,i,r),sS=s,cU(0,!1),eS&&"function"==typeof eS.onPostCommitFiberRoot)try{eS.onPostCommitFiberRoot(ej,a)}catch(e){}return!0}finally{B.p=o,V.T=n,cj(e,t)}}function cE(e,t,r){t=nN(r,t),t=iF(e.stateNode,t,2),null!==(e=oq(e,t,2))&&(eD(e,2),cF(e))}function cT(e,t,r){if(3===e.tag)cE(e,e,r);else for(;null!==t;){if(3===t.tag){cE(t,e,r);break}if(1===t.tag){var n=t.stateNode;if("function"==typeof t.type.getDerivedStateFromError||"function"==typeof n.componentDidCatch&&(null===sK||!sK.has(n))){e=nN(r,e),null!==(n=oq(t,r=iU(2),2))&&(i$(r,n,t,e),eD(n,2),cF(n));break}}t=t.return}}function cN(e,t,r){var n=e.pingCache;if(null===n){n=e.pingCache=new sj;var o=new Set;n.set(t,o)}else void 0===(o=n.get(t))&&(o=new Set,n.set(t,o));o.has(r)||(sz=!0,o.add(r),e=cL.bind(null,e,t,r),t.then(e,e))}function cL(e,t,r){var n=e.pingCache;null!==n&&n.delete(t),e.pingedLanes|=e.suspendedLanes&r,e.warmLanes&=~r,sC===e&&(sT&r)===r&&(4===sO||3===sO&&(0x3c00000&sT)===sT&&300>em()-sV?0==(2&sS)&&ci(e,0):sD|=r,sF===sT&&(sF=0)),cF(e)}function cI(e,t){0===t&&(t=eM()),null!==(e=nh(e,t))&&(eD(e,t),cF(e))}function cP(e){var t=e.memoizedState,r=0;null!==t&&(r=t.retryLane),cI(e,r)}function cz(e,t){var r=0;switch(e.tag){case 31:case 13:var n=e.stateNode,o=e.memoizedState;null!==o&&(r=o.retryLane);break;case 19:n=e.stateNode;break;case 22:n=e.stateNode._retryCache;break;default:throw Error(l(314))}null!==n&&n.delete(t),cI(e,r)}var cR=null,cO=null,cM=!1,cA=!1,cD=!1,cZ=0;function cF(e){e!==cO&&null===e.next&&(null===cO?cR=cO=e:cO=cO.next=e),cA=!0,cM||(cM=!0,uy(function(){0!=(6&sS)?ed(ev,c$):cH()}))}function cU(e,t){if(!cD&&cA){cD=!0;do for(var r=!1,n=cR;null!==n;){if(!t)if(0!==e){var o=n.pendingLanes;if(0===o)var a=0;else{var i=n.suspendedLanes,l=n.pingedLanes;a=0xc000095&(a=(1<<31-eE(42|e)+1)-1&(o&~(i&~l)))?0xc000095&a|1:a?2|a:0}0!==a&&(r=!0,cq(n,a))}else a=sT,0==(3&(a=eR(n,n===sC?a:0,null!==n.cancelPendingCommit||-1!==n.timeoutHandle)))||eO(n,a)||(r=!0,cq(n,a));n=n.next}while(r);cD=!1}}function c$(){cH()}function cH(){cA=cM=!1;var e,t=0;0===cZ||((e=window.event)&&"popstate"===e.type?e===uh||(uh=e,0):(uh=null,1))||(t=cZ);for(var r=em(),n=null,o=cR;null!==o;){var a=o.next,i=cV(o,r);0===i?(o.next=null,null===n?cR=a:n.next=a,null===a&&(cO=n)):(n=o,(0!==t||0!=(3&i))&&(cA=!0)),o=a}0!==sY&&5!==sY||cU(t,!1),0!==cZ&&(cZ=0)}function cV(e,t){for(var r=e.suspendedLanes,n=e.pingedLanes,o=e.expirationTimes,a=-0x3c00001&e.pendingLanes;0<a;){var i=31-eE(a),l=1<<i,s=o[i];-1===s?(0==(l&r)||0!=(l&n))&&(o[i]=function(e,t){switch(e){case 1:case 2:case 4:case 8:case 64:return t+250;case 16:case 32:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:return t+5e3;default:return -1}}(l,t)):s<=t&&(e.expiredLanes|=l),a&=~l}if(t=sC,r=sT,r=eR(e,e===t?r:0,null!==e.cancelPendingCommit||-1!==e.timeoutHandle),n=e.callbackNode,0===r||e===t&&(2===sN||9===sN)||null!==e.cancelPendingCommit)return null!==n&&null!==n&&ef(n),e.callbackNode=null,e.callbackPriority=0;if(0==(3&r)||eO(e,r)){if((t=r&-r)===e.callbackPriority)return t;switch(null!==n&&ef(n),eH(r)){case 2:case 8:r=ey;break;case 32:default:r=eb;break;case 0x10000000:r=e_}return r=ed(r,n=cB.bind(null,e)),e.callbackPriority=t,e.callbackNode=r,t}return null!==n&&null!==n&&ef(n),e.callbackPriority=2,e.callbackNode=null,2}function cB(e,t){if(0!==sY&&5!==sY)return e.callbackNode=null,e.callbackPriority=0,null;var r=e.callbackNode;if(cS()&&e.callbackNode!==r)return null;var n=sT;return 0===(n=eR(e,e===sC?n:0,null!==e.cancelPendingCommit||-1!==e.timeoutHandle))?null:(ct(e,n,t),cV(e,em()),null!=e.callbackNode&&e.callbackNode===r?cB.bind(null,e):null)}function cq(e,t){if(cS())return null;ct(e,t,!0)}function cW(){if(0===cZ){var e=og;0===e&&(e=eL,0==(261888&(eL<<=1))&&(eL=256)),cZ=e}return cZ}function cK(e){return null==e||"symbol"==typeof e||"boolean"==typeof e?null:"function"==typeof e?e:tN(e)}for(var cY=0;cY<nt.length;cY++){var cX=nt[cY];nr(cX.toLowerCase(),"on"+(cX[0].toUpperCase()+cX.slice(1)))}nr(r3,"onAnimationEnd"),nr(r4,"onAnimationIteration"),nr(r5,"onAnimationStart"),nr("dblclick","onDoubleClick"),nr("focusin","onFocus"),nr("focusout","onBlur"),nr(r6,"onTransitionRun"),nr(r9,"onTransitionStart"),nr(r8,"onTransitionCancel"),nr(r7,"onTransitionEnd"),te("onMouseEnter",["mouseout","mouseover"]),te("onMouseLeave",["mouseout","mouseover"]),te("onPointerEnter",["pointerout","pointerover"]),te("onPointerLeave",["pointerout","pointerover"]),e7("onChange","change click focusin focusout input keydown keyup selectionchange".split(" ")),e7("onSelect","focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" ")),e7("onBeforeInput",["compositionend","keypress","textInput","paste"]),e7("onCompositionEnd","compositionend focusout keydown keypress keyup mousedown".split(" ")),e7("onCompositionStart","compositionstart focusout keydown keypress keyup mousedown".split(" ")),e7("onCompositionUpdate","compositionupdate focusout keydown keypress keyup mousedown".split(" "));var cG="abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "),cQ=new Set("beforetoggle cancel close invalid load scroll scrollend toggle".split(" ").concat(cG));function cJ(e,t){t=0!=(4&t);for(var r=0;r<e.length;r++){var n=e[r],o=n.event;n=n.listeners;e:{var a=void 0;if(t)for(var i=n.length-1;0<=i;i--){var l=n[i],s=l.instance,c=l.currentTarget;if(l=l.listener,s!==a&&o.isPropagationStopped())break e;a=l,o.currentTarget=c;try{a(o)}catch(e){nl(e)}o.currentTarget=null,a=s}else for(i=0;i<n.length;i++){if(s=(l=n[i]).instance,c=l.currentTarget,l=l.listener,s!==a&&o.isPropagationStopped())break e;a=l,o.currentTarget=c;try{a(o)}catch(e){nl(e)}o.currentTarget=null,a=s}}}}function c0(e,t){var r=t[eX];void 0===r&&(r=t[eX]=new Set);var n=e+"__bubble";r.has(n)||(c4(t,e,2,!1),r.add(n))}function c1(e,t,r){var n=0;t&&(n|=4),c4(r,e,n,t)}var c2="_reactListening"+Math.random().toString(36).slice(2);function c3(e){if(!e[c2]){e[c2]=!0,e9.forEach(function(t){"selectionchange"!==t&&(cQ.has(t)||c1(t,!1,e),c1(t,!0,e))});var t=9===e.nodeType?e:e.ownerDocument;null===t||t[c2]||(t[c2]=!0,c1("selectionchange",!1,t))}}function c4(e,t,r,n){switch(dM(t)){case 2:var o=dL;break;case 8:o=dI;break;default:o=dP}r=o.bind(null,t,r,e),o=void 0,tF&&("touchstart"===t||"touchmove"===t||"wheel"===t)&&(o=!0),n?void 0!==o?e.addEventListener(t,r,{capture:!0,passive:o}):e.addEventListener(t,r,!0):void 0!==o?e.addEventListener(t,r,{passive:o}):e.addEventListener(t,r,!1)}function c5(e,t,r,n,o){var a=n;if(0==(1&t)&&0==(2&t)&&null!==n)e:for(;;){if(null===n)return;var i=n.tag;if(3===i||4===i){var l=n.stateNode.containerInfo;if(l===o)break;if(4===i)for(i=n.return;null!==i;){var c=i.tag;if((3===c||4===c)&&i.stateNode.containerInfo===o)return;i=i.return}for(;null!==l;){if(null===(i=e2(l)))return;if(5===(c=i.tag)||6===c||26===c||27===c){n=a=i;continue e}l=l.parentNode}}n=n.return}tA(function(){var n=a,o=tP(r),i=[];e:{var l=ne.get(e);if(void 0!==l){var c=t2,u=e;switch(e){case"keypress":if(0===tq(r))break e;case"keydown":case"keyup":c=rl;break;case"focusin":u="focus",c=t8;break;case"focusout":u="blur",c=t8;break;case"beforeblur":case"afterblur":c=t8;break;case"click":if(2===r.button)break e;case"auxclick":case"dblclick":case"mousedown":case"mousemove":case"mouseup":case"mouseout":case"mouseover":case"contextmenu":c=t6;break;case"drag":case"dragend":case"dragenter":case"dragexit":case"dragleave":case"dragover":case"dragstart":case"drop":c=t9;break;case"touchcancel":case"touchend":case"touchmove":case"touchstart":c=ru;break;case r3:case r4:case r5:c=t7;break;case r7:c=rd;break;case"scroll":case"scrollend":c=t4;break;case"wheel":c=rf;break;case"copy":case"cut":case"paste":c=re;break;case"gotpointercapture":case"lostpointercapture":case"pointercancel":case"pointerdown":case"pointermove":case"pointerout":case"pointerover":case"pointerup":c=rs;break;case"submit":c=rc;break;case"toggle":case"beforetoggle":c=rp}var d=0!=(4&t),f=!d&&("scroll"===e||"scrollend"===e),p=d?null!==l?l+"Capture":null:l;d=[];for(var h,m=n;null!==m;){var g=m;if(h=g.stateNode,5!==(g=g.tag)&&26!==g&&27!==g||null===h||null===p||null!=(g=tD(m,p))&&d.push(c6(m,g,h)),f)break;m=m.return}0<d.length&&(l=new c(l,u,null,r,o),i.push({event:l,listeners:d}))}}if(0==(7&t)){c="mouseover"===e||"pointerover"===e,l="mouseout"===e||"pointerout"===e,!(c&&r!==tI&&(u=r.relatedTarget||r.fromElement)&&(e2(u)||u[eY]))&&(l||c)&&(u=o.window===o?o:(c=o.ownerDocument)?c.defaultView||c.parentWindow:window,l?(c=r.relatedTarget||r.toElement,l=n,null!==(c=c?e2(c):null)&&(f=s(c),d=c.tag,c!==f||5!==d&&27!==d&&6!==d)&&(c=null)):(l=null,c=n),l!==c&&(d=t6,g="onMouseLeave",p="onMouseEnter",m="mouse",("pointerout"===e||"pointerover"===e)&&(d=rs,g="onPointerLeave",p="onPointerEnter",m="pointer"),f=null==l?u:e4(l),h=null==c?u:e4(c),(u=new d(g,m+"leave",l,r,o)).target=f,u.relatedTarget=h,g=null,e2(o)===n&&((d=new d(p,m+"enter",c,r,o)).target=h,d.relatedTarget=f,g=d),f=g,d=l&&c?_(l,c,c8):null,null!==l&&c7(i,u,l,d,!1),null!==c&&null!==f&&c7(i,f,c,d,!0)));e:{if("select"===(c=(l=n?e4(n):window).nodeName&&l.nodeName.toLowerCase())||"input"===c&&"file"===l.type)var v,y=rL;else if(rj(l))if(rI)y=rZ;else{y=rA;var b=rM}else(c=l.nodeName)&&"input"===c.toLowerCase()&&("checkbox"===l.type||"radio"===l.type)?y=rD:n&&tC(n.elementType)&&(y=rL);if(y&&(y=y(e,n))){rS(i,y,r,o);break e}b&&b(e,l,n),"focusout"===e&&n&&"number"===l.type&&null!=n.memoizedProps.value&&ty(l,"number",l.value)}switch(b=n?e4(n):window,e){case"focusin":(rj(b)||"true"===b.contentEditable)&&(rW=b,rK=n,rY=null);break;case"focusout":rY=rK=rW=null;break;case"mousedown":rX=!0;break;case"contextmenu":case"mouseup":case"dragend":rX=!1,rG(i,r,o);break;case"selectionchange":if(rq)break;case"keydown":case"keyup":rG(i,r,o)}if(rm)t:{switch(e){case"compositionstart":var x="onCompositionStart";break t;case"compositionend":x="onCompositionEnd";break t;case"compositionupdate":x="onCompositionUpdate";break t}x=void 0}else rw?rx(e,r)&&(x="onCompositionEnd"):"keydown"===e&&229===r.keyCode&&(x="onCompositionStart");x&&(ry&&"ko"!==r.locale&&(rw||"onCompositionStart"!==x?"onCompositionEnd"===x&&rw&&(v=tB()):(tH="value"in(t$=o)?t$.value:t$.textContent,rw=!0)),0<(b=c9(n,x)).length&&(x=new rt(x,e,null,r,o),i.push({event:x,listeners:b}),v?x.data=v:null!==(v=r_(r))&&(x.data=v))),(v=rv?function(e,t){switch(e){case"compositionend":return r_(t);case"keypress":if(32!==t.which)return null;return rb=!0," ";case"textInput":return" "===(e=t.data)&&rb?null:e;default:return null}}(e,r):function(e,t){if(rw)return"compositionend"===e||!rm&&rx(e,t)?(e=tB(),tV=tH=t$=null,rw=!1,e):null;switch(e){case"paste":default:return null;case"keypress":if(!(t.ctrlKey||t.altKey||t.metaKey)||t.ctrlKey&&t.altKey){if(t.char&&1<t.char.length)return t.char;if(t.which)return String.fromCharCode(t.which)}return null;case"compositionend":return ry&&"ko"!==t.locale?null:t.data}}(e,r))&&0<(x=c9(n,"onBeforeInput")).length&&(b=new rt("onBeforeInput","beforeinput",null,r,o),i.push({event:b,listeners:x}),b.data=v);var w=e;if("submit"===w&&n&&n.stateNode===o){var k=cK((o[eK]||null).action),j=r.submitter;j&&null!==(w=(w=j[eK]||null)?cK(w.formAction):j.getAttribute("formAction"))&&(k=w,j=null);var S=new t2("action","action",null,r,o);i.push({event:S,listeners:[{instance:null,listener:function(){if(r.defaultPrevented){if(0!==cZ){var e=new FormData(o,j);id(n,{pending:!0,data:e,method:o.method,action:k},null,e)}}else"function"==typeof k&&(S.preventDefault(),id(n,{pending:!0,data:e=new FormData(o,j),method:o.method,action:k},k,e))},currentTarget:o}]})}}cJ(i,t)})}function c6(e,t,r){return{instance:e,listener:t,currentTarget:r}}function c9(e,t){for(var r=t+"Capture",n=[];null!==e;){var o=e,a=o.stateNode;if(5!==(o=o.tag)&&26!==o&&27!==o||null===a||(null!=(o=tD(e,r))&&n.unshift(c6(e,o,a)),null!=(o=tD(e,t))&&n.push(c6(e,o,a))),3===e.tag)return n;e=e.return}return[]}function c8(e){if(null===e)return null;do e=e.return;while(e&&5!==e.tag&&27!==e.tag);return e||null}function c7(e,t,r,n,o){for(var a=t._reactName,i=[];null!==r&&r!==n;){var l=r,s=l.alternate,c=l.stateNode;if(l=l.tag,null!==s&&s===n)break;5!==l&&26!==l&&27!==l||null===c||(s=c,o?null!=(c=tD(r,a))&&i.unshift(c6(r,c,s)):o||null!=(c=tD(r,a))&&i.push(c6(r,c,s))),r=r.return}0!==i.length&&e.push({event:t,listeners:i})}var ue=/\r\n?/g,ut=/\u0000|\uFFFD/g;function ur(e){return("string"==typeof e?e:""+e).replace(ue,"\n").replace(ut,"")}function un(e,t){return t=ur(t),ur(e)===t}function uo(e,t,r,n,o,a){switch(r){case"children":if("string"==typeof n)"body"===t||"textarea"===t&&""===n||tw(e,n);else{if("number"!=typeof n&&"bigint"!=typeof n)return;"body"!==t&&tw(e,""+n)}break;case"className":tl(e,"class",n);break;case"tabIndex":tl(e,"tabindex",n);break;case"dir":case"role":case"viewBox":case"width":case"height":tl(e,r,n);break;case"style":tS(e,n,a);return;case"data":if("object"!==t){tl(e,"data",n);break}case"src":case"href":if(""===n&&("a"!==t||"href"!==r)||null==n||"function"==typeof n||"symbol"==typeof n||"boolean"==typeof n){e.removeAttribute(r);break}n=tN(n),e.setAttribute(r,n);break;case"action":case"formAction":if("function"==typeof n){e.setAttribute(r,"javascript:throw new Error('A React form was unexpectedly submitted. If you called form.submit() manually, consider using form.requestSubmit() instead. If you\\'re trying to use event.stopPropagation() in a submit event handler, consider also calling event.preventDefault().')");break}if("function"==typeof a&&("formAction"===r?("input"!==t&&uo(e,t,"name",o.name,o,null),uo(e,t,"formEncType",o.formEncType,o,null),uo(e,t,"formMethod",o.formMethod,o,null),uo(e,t,"formTarget",o.formTarget,o,null)):(uo(e,t,"encType",o.encType,o,null),uo(e,t,"method",o.method,o,null),uo(e,t,"target",o.target,o,null))),null==n||"symbol"==typeof n||"boolean"==typeof n){e.removeAttribute(r);break}n=tN(n),e.setAttribute(r,n);break;case"onClick":null!=n&&(e.onclick=tL);return;case"onScroll":null!=n&&c0("scroll",e);return;case"onScrollEnd":null!=n&&c0("scrollend",e);return;case"dangerouslySetInnerHTML":if(null!=n){if("object"!=typeof n||!("__html"in n))throw Error(l(61));if(null!=(r=n.__html)){if(null!=o.children)throw Error(l(60));e.innerHTML=r}}break;case"multiple":e.multiple=n&&"function"!=typeof n&&"symbol"!=typeof n;break;case"muted":e.muted=n&&"function"!=typeof n&&"symbol"!=typeof n;break;case"suppressContentEditableWarning":case"suppressHydrationWarning":case"defaultValue":case"defaultChecked":case"innerHTML":case"ref":case"autoFocus":break;case"xlinkHref":if(null==n||"function"==typeof n||"boolean"==typeof n||"symbol"==typeof n){e.removeAttribute("xlink:href");break}r=tN(n),e.setAttributeNS("http://www.w3.org/1999/xlink","xlink:href",r);break;case"contentEditable":case"spellCheck":case"draggable":case"value":case"autoReverse":case"externalResourcesRequired":case"focusable":case"preserveAlpha":null!=n&&"function"!=typeof n&&"symbol"!=typeof n?e.setAttribute(r,n):e.removeAttribute(r);break;case"inert":case"allowFullScreen":case"async":case"autoPlay":case"controls":case"default":case"defer":case"disabled":case"disablePictureInPicture":case"disableRemotePlayback":case"formNoValidate":case"hidden":case"loop":case"noModule":case"noValidate":case"open":case"playsInline":case"readOnly":case"required":case"reversed":case"scoped":case"seamless":case"itemScope":n&&"function"!=typeof n&&"symbol"!=typeof n?e.setAttribute(r,""):e.removeAttribute(r);break;case"capture":case"download":!0===n?e.setAttribute(r,""):!1!==n&&null!=n&&"function"!=typeof n&&"symbol"!=typeof n?e.setAttribute(r,n):e.removeAttribute(r);break;case"cols":case"rows":case"size":case"span":null!=n&&"function"!=typeof n&&"symbol"!=typeof n&&!isNaN(n)&&1<=n?e.setAttribute(r,n):e.removeAttribute(r);break;case"rowSpan":case"start":null==n||"function"==typeof n||"symbol"==typeof n||isNaN(n)?e.removeAttribute(r):e.setAttribute(r,n);break;case"popover":c0("beforetoggle",e),c0("toggle",e),ti(e,"popover",n);break;case"xlinkActuate":ts(e,"http://www.w3.org/1999/xlink","xlink:actuate",n);break;case"xlinkArcrole":ts(e,"http://www.w3.org/1999/xlink","xlink:arcrole",n);break;case"xlinkRole":ts(e,"http://www.w3.org/1999/xlink","xlink:role",n);break;case"xlinkShow":ts(e,"http://www.w3.org/1999/xlink","xlink:show",n);break;case"xlinkTitle":ts(e,"http://www.w3.org/1999/xlink","xlink:title",n);break;case"xlinkType":ts(e,"http://www.w3.org/1999/xlink","xlink:type",n);break;case"xmlBase":ts(e,"http://www.w3.org/XML/1998/namespace","xml:base",n);break;case"xmlLang":ts(e,"http://www.w3.org/XML/1998/namespace","xml:lang",n);break;case"xmlSpace":ts(e,"http://www.w3.org/XML/1998/namespace","xml:space",n);break;case"is":ti(e,"is",n);break;case"innerText":case"textContent":return;default:if(2<r.length&&("o"===r[0]||"O"===r[0])&&("n"===r[1]||"N"===r[1]))return;ti(e,r=tE.get(r)||r,n)}to=!0}function ua(e,t,r,n,o,a){switch(r){case"style":tS(e,n,a);return;case"dangerouslySetInnerHTML":if(null!=n){if("object"!=typeof n||!("__html"in n))throw Error(l(61));if(null!=(r=n.__html)){if(null!=o.children)throw Error(l(60));e.innerHTML=r}}break;case"children":if("string"==typeof n)tw(e,n);else{if("number"!=typeof n&&"bigint"!=typeof n)return;tw(e,""+n)}break;case"onScroll":null!=n&&c0("scroll",e);return;case"onScrollEnd":null!=n&&c0("scrollend",e);return;case"onClick":null!=n&&(e.onclick=tL);return;case"suppressContentEditableWarning":case"suppressHydrationWarning":case"innerHTML":case"ref":case"innerText":case"textContent":return;default:if(!e8.hasOwnProperty(r))e:{if("o"===r[0]&&"n"===r[1]&&(o=r.endsWith("Capture"),t=r.slice(2,o?r.length-7:void 0),"function"==typeof(a=null!=(a=e[eK]||null)?a[r]:null)&&e.removeEventListener(t,a,o),"function"==typeof n)){"function"!=typeof a&&null!==a&&(r in e?e[r]=null:e.hasAttribute(r)&&e.removeAttribute(r)),e.addEventListener(t,n,o);break e}to=!0,r in e?e[r]=n:!0===n?e.setAttribute(r,""):ti(e,r,n)}return}to=!0}function ui(e,t,r){switch(t){case"div":case"span":case"svg":case"path":case"a":case"g":case"p":case"li":break;case"img":c0("error",e),c0("load",e);var n,o=!1,a=!1;for(n in r)if(r.hasOwnProperty(n)){var i=r[n];if(null!=i)switch(n){case"src":o=!0;break;case"srcSet":a=!0;break;case"children":case"dangerouslySetInnerHTML":throw Error(l(137,t));default:uo(e,t,n,i,r,null)}}a&&uo(e,t,"srcSet",r.srcSet,r,null),o&&uo(e,t,"src",r.src,r,null);return;case"input":c0("invalid",e);var s=n=i=a=null,c=null,u=null;for(o in r)if(r.hasOwnProperty(o)){var d=r[o];if(null!=d)switch(o){case"name":a=d;break;case"type":i=d;break;case"checked":c=d;break;case"defaultChecked":u=d;break;case"value":n=d;break;case"defaultValue":s=d;break;case"children":case"dangerouslySetInnerHTML":if(null!=d)throw Error(l(137,t));break;default:uo(e,t,o,d,r,null)}}tv(e,n,s,c,u,i,a,!1);return;case"select":for(a in c0("invalid",e),o=i=n=null,r)if(r.hasOwnProperty(a)&&null!=(s=r[a]))switch(a){case"value":n=s;break;case"defaultValue":i=s;break;case"multiple":o=s;default:uo(e,t,a,s,r,null)}t=n,r=i,e.multiple=!!o,null!=t?tb(e,!!o,t,!1):null!=r&&tb(e,!!o,r,!0);return;case"textarea":for(i in c0("invalid",e),n=a=o=null,r)if(r.hasOwnProperty(i)&&null!=(s=r[i]))switch(i){case"value":o=s;break;case"defaultValue":a=s;break;case"children":n=s;break;case"dangerouslySetInnerHTML":if(null!=s)throw Error(l(91));break;default:uo(e,t,i,s,r,null)}t_(e,o,a,n);return;case"option":for(c in r)r.hasOwnProperty(c)&&null!=(o=r[c])&&("selected"===c?e.selected=o&&"function"!=typeof o&&"symbol"!=typeof o:uo(e,t,c,o,r,null));return;case"dialog":c0("beforetoggle",e),c0("toggle",e),c0("cancel",e),c0("close",e);break;case"iframe":case"object":c0("load",e);break;case"video":case"audio":for(o=0;o<cG.length;o++)c0(cG[o],e);break;case"image":c0("error",e),c0("load",e);break;case"details":c0("toggle",e);break;case"embed":case"source":case"link":c0("error",e),c0("load",e);case"area":case"base":case"br":case"col":case"hr":case"keygen":case"meta":case"param":case"track":case"wbr":case"menuitem":for(u in r)if(r.hasOwnProperty(u)&&null!=(o=r[u]))switch(u){case"children":case"dangerouslySetInnerHTML":throw Error(l(137,t));default:uo(e,t,u,o,r,null)}return;default:if(tC(t)){for(d in r)r.hasOwnProperty(d)&&void 0!==(o=r[d])&&ua(e,t,d,o,r,void 0);return}}for(s in r)r.hasOwnProperty(s)&&null!=(o=r[s])&&uo(e,t,s,o,r,null)}function ul(e){switch(e){case"css":case"script":case"font":case"img":case"image":case"input":case"link":return!0;default:return!1}}var us=null,uc=null;function uu(e){return 9===e.nodeType?e:e.ownerDocument}function ud(e){switch(e){case"http://www.w3.org/2000/svg":return 1;case"http://www.w3.org/1998/Math/MathML":return 2;default:return 0}}function uf(e,t){if(0===e)switch(t){case"svg":return 1;case"math":return 2;default:return 0}return 1===e&&"foreignObject"===t?0:e}function up(e,t){return"textarea"===e||"noscript"===e||"string"==typeof t.children||"number"==typeof t.children||"bigint"==typeof t.children||"object"==typeof t.dangerouslySetInnerHTML&&null!==t.dangerouslySetInnerHTML&&null!=t.dangerouslySetInnerHTML.__html}var uh=null,um="function"==typeof setTimeout?setTimeout:void 0,ug="function"==typeof clearTimeout?clearTimeout:void 0,uv="function"==typeof Promise?Promise:void 0,uy="function"==typeof queueMicrotask?queueMicrotask:void 0!==uv?function(e){return uv.resolve(null).then(e).catch(ub)}:um;function ub(e){setTimeout(function(){throw e})}function ux(e){return"head"===e}function u_(e,t){var r=t,n=0;do{var o=r.nextSibling;if(e.removeChild(r),o&&8===o.nodeType)if("/$"===(r=o.data)||"/&"===r){if(0===n){e.removeChild(o),d0(t);return}n--}else if("$"===r||"$?"===r||"$~"===r||"$!"===r||"&"===r)n++;else if("html"===r)u0(e.ownerDocument.documentElement);else if("head"===r){u0(r=e.ownerDocument.head);for(var a=r.firstChild;a;){var i=a.nextSibling,l=a.nodeName;a[e0]||"SCRIPT"===l||"STYLE"===l||"LINK"===l&&"stylesheet"===a.rel.toLowerCase()||r.removeChild(a),a=i}}else"body"===r&&u0(e.ownerDocument.body);r=o}while(r);d0(t)}function uw(e,t){var r=e;e=0;do{var n=r.nextSibling;if(1===r.nodeType?t?(r._stashedDisplay=r.style.display,r.style.display="none"):(r.style.display=r._stashedDisplay||"",""===r.getAttribute("style")&&r.removeAttribute("style")):3===r.nodeType&&(t?(r._stashedText=r.nodeValue,r.nodeValue=""):r.nodeValue=r._stashedText||""),n&&8===n.nodeType)if("/$"===(r=n.data))if(0===e)break;else e--;else"$"!==r&&"$?"!==r&&"$~"!==r&&"$!"!==r||e++;r=n}while(r)}function uk(e,t,r){if(t=CSS.escape(t)!==t?"r-"+btoa(t).replace(/=/g,""):t,e.style.viewTransitionName=t,null!=r&&(e.style.viewTransitionClass=r),"inline"===(r=getComputedStyle(e)).display){if(1===(t=e.getClientRects()).length)var n=1;else for(var o=n=0;o<t.length;o++){var a=t[o];0<a.width&&0<a.height&&n++}1===n&&((e=e.style).display=1===t.length?"inline-block":"block",e.marginTop="-"+r.paddingTop,e.marginBottom="-"+r.paddingBottom)}}function uj(e,t){e=e.style;var r=null!=(t=t.style)?t.hasOwnProperty("viewTransitionName")?t.viewTransitionName:t.hasOwnProperty("view-transition-name")?t["view-transition-name"]:null:null;e.viewTransitionName=null==r||"boolean"==typeof r?"":(""+r).trim(),r=null!=t?t.hasOwnProperty("viewTransitionClass")?t.viewTransitionClass:t.hasOwnProperty("view-transition-class")?t["view-transition-class"]:null:null,e.viewTransitionClass=null==r||"boolean"==typeof r?"":(""+r).trim(),"inline-block"===e.display&&(null==t?e.display=e.margin="":(r=t.display,e.display=null==r||"boolean"==typeof r?"":r,null!=(r=t.margin)?e.margin=r:(r=t.hasOwnProperty("marginTop")?t.marginTop:t["margin-top"],e.marginTop=null==r||"boolean"==typeof r?"":r,t=t.hasOwnProperty("marginBottom")?t.marginBottom:t["margin-bottom"],e.marginBottom=null==t||"boolean"==typeof t?"":t)))}function uS(e,t,r){return r=r.ownerDocument.defaultView,{rect:e,abs:"absolute"===t.position||"fixed"===t.position,clip:"none"!==t.clipPath||"visible"!==t.overflow||"none"!==t.filter||"none"!==t.mask||"none"!==t.mask||"0px"!==t.borderRadius,view:0<=e.bottom&&0<=e.right&&e.top<=r.innerHeight&&e.left<=r.innerWidth}}function uC(e){return uS(e.getBoundingClientRect(),getComputedStyle(e),e)}function uE(e){var t=e.getBoundingClientRect();return uS(t=new DOMRect(t.x+2e4,t.y+2e4,t.width,t.height),getComputedStyle(e),e)}function uT(e){this.addEventListener("load",e),this.addEventListener("error",e)}function uN(e,t){this._scope=document.documentElement,this._selector="::view-transition-"+e+"("+t+")"}function uL(e){return{name:e,group:new uN("group",e),imagePair:new uN("image-pair",e),old:new uN("old",e),new:new uN("new",e)}}function uI(e){this._fragmentFiber=e,this._observers=this._eventListeners=null}function uP(e,t,r,n){return h(e).addEventListener(t,r,n),!1}function uz(e,t,r,n){return h(e).removeEventListener(t,r,n),!1}function uR(e){return null==e?"0":"boolean"==typeof e?"c="+(e?"1":"0"):"c="+(e.capture?"1":"0")+"&o="+(e.once?"1":"0")+"&p="+(e.passive?"1":"0")}function uO(e,t,r,n){if(0===e.length)return -1;n=uR(n);for(var o=0;o<e.length;o++){var a=e[o];if(a.type===t&&a.listener===r&&uR(a.optionsOrUseCapture)===n)return o}return -1}function uM(e,t){return 6!==e.tag&&function(e,t){function r(){n=!0}if(e.ownerDocument.activeElement===e)return!0;var n=!1;try{e.ownerDocument.addEventListener("focus",r,!0),(e.focus||HTMLElement.prototype.focus).call(e,t)}finally{e.ownerDocument.removeEventListener("focus",r,!0)}return n}(e=h(e),t)}function uA(e,t){return t.push(e),!1}function uD(e,t){return 6!==e.tag&&(e=h(e))===t&&(e.blur(),!0)}function uZ(e,t){return 6!==e.tag&&(e=h(e),t.observe(e),!1)}function uF(e,t){return 6!==e.tag&&(e=h(e),t.unobserve(e),!1)}function uU(e,t){if(6===e.tag){var r=(e=e.stateNode).ownerDocument.createRange();r.selectNodeContents(e),t.push.apply(t,r.getClientRects())}else e=h(e),t.push.apply(t,e.getClientRects());return!1}function u$(e,t){return null!=(e=h(e))&&uH(e,t),!1}function uH(e,t){null==e.reactFragments&&(e.reactFragments=new Set),e.reactFragments.add(t)}function uV(e,t){if(3!==e.nodeType){var r=t._eventListeners;if(null!==r)for(var n=0;n<r.length;n++){var o=r[n];e.addEventListener(o.type,o.listener,o.optionsOrUseCapture)}null!==t._observers&&t._observers.forEach(function(t){t.observe(e)}),uH(e,t)}}function uB(e){var t=e.firstChild;for(t&&10===t.nodeType&&(t=t.nextSibling);t;){var r=t;switch(t=t.nextSibling,r.nodeName){case"HTML":case"HEAD":case"BODY":uB(r),e1(r);continue;case"SCRIPT":case"STYLE":continue;case"LINK":if("stylesheet"===r.rel.toLowerCase())continue}e.removeChild(r)}}function uq(e,t){for(;8!==e.nodeType;)if((1!==e.nodeType||"INPUT"!==e.nodeName||"hidden"!==e.type)&&!t||null===(e=uY(e.nextSibling)))return null;return e}function uW(e){return"$?"===e.data||"$~"===e.data}function uK(e){return"$!"===e.data||"$?"===e.data&&"loading"!==e.ownerDocument.readyState}function uY(e){for(;null!=e;e=e.nextSibling){var t=e.nodeType;if(1===t||3===t)break;if(8===t){if("$"===(t=e.data)||"$!"===t||"$?"===t||"$~"===t||"&"===t||"F!"===t||"F"===t)break;if("/$"===t||"/&"===t)return null}}return e}uN.prototype.animate=function(e,t){return(t="number"==typeof t?{duration:t}:w({},t)).pseudoElement=this._selector,this._scope.animate(e,t)},uN.prototype.getAnimations=function(){for(var e=this._scope,t=this._selector,r=e.getAnimations({subtree:!0}),n=[],o=0;o<r.length;o++){var a=r[o].effect;null!==a&&a.target===e&&a.pseudoElement===t&&n.push(r[o])}return n},uN.prototype.getComputedStyle=function(){return getComputedStyle(this._scope,this._selector)},uI.prototype.addEventListener=function(e,t,r){null===this._eventListeners&&(this._eventListeners=[]);var n=this._eventListeners;-1===uO(n,e,t,r)&&(n.push({type:e,listener:t,optionsOrUseCapture:r}),f(this._fragmentFiber.child,!1,uP,e,t,r)),this._eventListeners=n},uI.prototype.removeEventListener=function(e,t,r){var n=this._eventListeners;null!=n&&0<n.length&&(f(this._fragmentFiber.child,!1,uz,e,t,r),e=uO(n,e,t,r),null!==this._eventListeners&&this._eventListeners.splice(e,1))},uI.prototype.dispatchEvent=function(e){var t=p(this._fragmentFiber);if(null===t)return!0;t=h(t);var r=this._eventListeners;if(null!==r&&0<r.length||!e.bubbles){var n=document.createTextNode("");if(r)for(var o=0;o<r.length;o++){var a=r[o];n.addEventListener(a.type,a.listener,a.optionsOrUseCapture)}if(t.appendChild(n),e=n.dispatchEvent(e),r)for(o=0;o<r.length;o++)a=r[o],n.removeEventListener(a.type,a.listener,a.optionsOrUseCapture);return t.removeChild(n),e}return t.dispatchEvent(e)},uI.prototype.focus=function(e){f(this._fragmentFiber.child,!0,uM,e,void 0,void 0)},uI.prototype.focusLast=function(e){var t=[];f(this._fragmentFiber.child,!0,uA,t,void 0,void 0);for(var r=t.length-1;0<=r&&!uM(t[r],e);r--);},uI.prototype.blur=function(){var e=p(this._fragmentFiber);if(null!==e){var t=(e=h(e)).ownerDocument.activeElement;null!==t&&e.contains(t)&&f(this._fragmentFiber.child,!1,uD,t,void 0,void 0)}},uI.prototype.observeUsing=function(e){null===this._observers&&(this._observers=new Set),this._observers.add(e),f(this._fragmentFiber.child,!1,uZ,e,void 0,void 0)},uI.prototype.unobserveUsing=function(e){var t=this._observers;null!==t&&t.has(e)&&(t.delete(e),f(this._fragmentFiber.child,!1,uF,e,void 0,void 0))},uI.prototype.getClientRects=function(){var e=[];return f(this._fragmentFiber.child,!1,uU,e,void 0,void 0),e},uI.prototype.getRootNode=function(e){var t=p(this._fragmentFiber);return null===t?this:h(t).getRootNode(e)},uI.prototype.compareDocumentPosition=function(e){var t=p(this._fragmentFiber);if(null===t)return Node.DOCUMENT_POSITION_DISCONNECTED;var r=[];f(this._fragmentFiber.child,!1,uA,r,void 0,void 0);var n=h(t);if(0===r.length){r=this._fragmentFiber;var o=n.compareDocumentPosition(e);return t=o,n===e?t=Node.DOCUMENT_POSITION_CONTAINS:o&Node.DOCUMENT_POSITION_CONTAINED_BY&&(f(r.sibling,!1,v),r=m,m=null,t=null===r?Node.DOCUMENT_POSITION_PRECEDING:0===(e=h(r).compareDocumentPosition(e))||e&Node.DOCUMENT_POSITION_FOLLOWING?Node.DOCUMENT_POSITION_FOLLOWING:Node.DOCUMENT_POSITION_PRECEDING),t|Node.DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC}t=h(r[0]),o=h(r[r.length-1]);for(var a=!1,i=this._fragmentFiber.return;null!==i&&(4===i.tag&&(a=!0),3!==i.tag&&5!==i.tag);)i=i.return;if(null==(a=a?t.parentElement:n))return Node.DOCUMENT_POSITION_DISCONNECTED;n=a.compareDocumentPosition(t)&Node.DOCUMENT_POSITION_CONTAINED_BY,a=a.compareDocumentPosition(o)&Node.DOCUMENT_POSITION_CONTAINED_BY,i=t.compareDocumentPosition(e);var l=o.compareDocumentPosition(e),s=i&Node.DOCUMENT_POSITION_CONTAINED_BY||l&Node.DOCUMENT_POSITION_CONTAINED_BY;return l=n&&a&&i&Node.DOCUMENT_POSITION_FOLLOWING&&l&Node.DOCUMENT_POSITION_PRECEDING,(t=n&&t===e||a&&o===e||s||l?Node.DOCUMENT_POSITION_CONTAINED_BY:(n||t!==e)&&(a||o!==e)?i:Node.DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC)&Node.DOCUMENT_POSITION_DISCONNECTED||t&Node.DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC||function(e,t,r,n,o){var a=e2(o);if(e&Node.DOCUMENT_POSITION_CONTAINED_BY){if(r=!!a)e:{for(;null!==a;){if(7===a.tag&&(a===t||a.alternate===t)){r=!0;break e}a=a.return}r=!1}return r}if(e&Node.DOCUMENT_POSITION_CONTAINS){if(null===a)return a=o.ownerDocument,o===a||o===a.body;e:{for(a=t,t=p(t);null!==a;){if((5===a.tag||3===a.tag)&&(a===t||a.alternate===t)){a=!0;break e}a=a.return}a=!1}return a}return e&Node.DOCUMENT_POSITION_PRECEDING?((t=!!a)&&!(t=a===r)&&(null===(t=_(r,a,x))?t=!1:(f(t,!0,y,a,r),a=m,m=null,t=null!==a)),t):!!(e&Node.DOCUMENT_POSITION_FOLLOWING)&&((t=!!a)&&!(t=a===n)&&(null===(t=_(n,a,x))?t=!1:(f(t,!0,b,a,n),a=m,g=m=null,t=null!==a)),t)}(t,this._fragmentFiber,r[0],r[r.length-1],e)?t:Node.DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC},uI.prototype.scrollIntoView=function(e){if("object"==typeof e)throw Error(l(566));var t=[];f(this._fragmentFiber.child,!1,uA,t,void 0,void 0);var r=!1!==e;if(0===t.length){t=this._fragmentFiber;var n=[null,null],o=p(t);null!==o&&function e(t,r,n){for(var o=3<arguments.length&&void 0!==arguments[3]&&arguments[3];null!==n;){if(n===r)if(o=!0,!n.sibling)return!0;else n=n.sibling;if(5===n.tag){if(o)return t[1]=n,!0;t[0]=n}else if((22!==n.tag||null===n.memoizedState)&&e(t,r,n.child,o))return!0;n=n.sibling}return!1}(n,t,o.child),null!==(r=r?n[1]||n[0]||p(this._fragmentFiber):n[0]||n[1])&&h(r).scrollIntoView(e)}else for(n=r?t.length-1:0;n!==(r?-1:t.length);){if(6===(o=t[n]).tag){var a=(o=o.stateNode).ownerDocument.createRange();a.selectNodeContents(o),o=a.getBoundingClientRect(),window.scrollTo(window.scrollX+o.left,r?window.scrollY+o.top:window.scrollY+o.bottom-window.innerHeight)}else h(o).scrollIntoView(e);n+=r?-1:1}};var uX=null;function uG(e){e=e.nextSibling;for(var t=0;e;){if(8===e.nodeType){var r=e.data;if("/$"===r||"/&"===r){if(0===t)return uY(e.nextSibling);t--}else"$"!==r&&"$!"!==r&&"$?"!==r&&"$~"!==r&&"&"!==r||t++}e=e.nextSibling}return null}function uQ(e){e=e.previousSibling;for(var t=0;e;){if(8===e.nodeType){var r=e.data;if("$"===r||"$!"===r||"$?"===r||"$~"===r||"&"===r){if(0===t)return e;t--}else"/$"!==r&&"/&"!==r||t++}e=e.previousSibling}return null}function uJ(e,t,r){switch(t=uu(r),e){case"html":if(!(e=t.documentElement))throw Error(l(452));return e;case"head":if(!(e=t.head))throw Error(l(453));return e;case"body":if(!(e=t.body))throw Error(l(454));return e;default:throw Error(l(451))}}function u0(e){for(var t=e.attributes;t.length;)e.removeAttributeNode(t[0]);e1(e)}var u1=new Map,u2=new Set;function u3(e){return"function"==typeof e.getRootNode?e.getRootNode():9===e.nodeType?e:e.ownerDocument}var u4=B.d;B.d={f:function(){var e=u4.f(),t=co();return e||t},r:function(e){var t=e3(e);null!==t&&5===t.tag&&"form"===t.type?ih(t):u4.r(e)},D:function(e){u4.D(e),u6("dns-prefetch",e,null)},C:function(e,t){u4.C(e,t),u6("preconnect",e,t)},L:function(e,t,r){if(u4.L(e,t,r),u5&&e&&t){var n='link[rel="preload"][as="'+tm(t)+'"]';"image"===t&&r&&r.imageSrcSet?(n+='[imagesrcset="'+tm(r.imageSrcSet)+'"]',"string"==typeof r.imageSizes&&(n+='[imagesizes="'+tm(r.imageSizes)+'"]')):n+='[href="'+tm(e)+'"]';var o=n;switch(t){case"style":o=u8(e);break;case"script":o=dt(e)}u1.has(o)||(e=w({rel:"preload",href:"image"===t&&r&&r.imageSrcSet?void 0:e,as:t},r),u1.set(o,e),null!==u5.querySelector(n)||"style"===t&&u5.querySelector(u7(o))||"script"===t&&u5.querySelector(dr(o))||(ui(t=u5.createElement("link"),"link",e),e6(t),u5.head.appendChild(t)))}},m:function(e,t){if(u4.m(e,t),u5&&e){var r=t&&"string"==typeof t.as?t.as:"script",n='link[rel="modulepreload"][as="'+tm(r)+'"][href="'+tm(e)+'"]',o=n;switch(r){case"audioworklet":case"paintworklet":case"serviceworker":case"sharedworker":case"worker":case"script":o=dt(e)}if(!u1.has(o)&&(e=w({rel:"modulepreload",href:e},t),u1.set(o,e),null===u5.querySelector(n))){switch(r){case"audioworklet":case"paintworklet":case"serviceworker":case"sharedworker":case"worker":case"script":if(u5.querySelector(dr(o)))return}ui(r=u5.createElement("link"),"link",e),e6(r),u5.head.appendChild(r)}}},X:function(e,t){if(u4.X(e,t),u5&&e){var r=e5(u5).hoistableScripts,n=dt(e),o=r.get(n);o||((o=u5.querySelector(dr(n)))||(e=w({src:e,async:!0},t),(t=u1.get(n))&&dl(e,t),e6(o=u5.createElement("script")),ui(o,"link",e),u5.head.appendChild(o)),o={type:"script",instance:o,count:1,state:null},r.set(n,o))}},S:function(e,t,r){if(u4.S(e,t,r),u5&&e){var n=e5(u5).hoistableStyles,o=u8(e);t=t||"default";var a=n.get(o);if(!a){var i={loading:0,preload:null};if(a=u5.querySelector(u7(o)))i.loading=5;else{e=w({rel:"stylesheet",href:e,"data-precedence":t},r),(r=u1.get(o))&&di(e,r);var l=a=u5.createElement("link");e6(l),ui(l,"link",e),l._p=new Promise(function(e,t){l.onload=e,l.onerror=t}),l.addEventListener("load",function(){i.loading|=1}),l.addEventListener("error",function(){i.loading|=2}),i.loading|=4,da(a,t,u5)}a={type:"stylesheet",instance:a,count:1,state:i},n.set(o,a)}}},M:function(e,t){if(u4.M(e,t),u5&&e){var r=e5(u5).hoistableScripts,n=dt(e),o=r.get(n);o||((o=u5.querySelector(dr(n)))||(e=w({src:e,async:!0,type:"module"},t),(t=u1.get(n))&&dl(e,t),e6(o=u5.createElement("script")),ui(o,"link",e),u5.head.appendChild(o)),o={type:"script",instance:o,count:1,state:null},r.set(n,o))}}};var u5="undefined"==typeof document?null:document;function u6(e,t,r){if(u5&&"string"==typeof t&&t){var n=tm(t);n='link[rel="'+e+'"][href="'+n+'"]',"string"==typeof r&&(n+='[crossorigin="'+r+'"]'),u2.has(n)||(u2.add(n),e={rel:e,crossOrigin:r,href:t},null===u5.querySelector(n)&&(ui(t=u5.createElement("link"),"link",e),e6(t),u5.head.appendChild(t)))}}function u9(e,t,r,n){var o=(o=ee.current)?u3(o):null;if(!o)throw Error(l(446));switch(e){case"meta":case"title":return null;case"style":return"string"==typeof r.precedence&&"string"==typeof r.href?(t=u8(r.href),(n=(r=e5(o).hoistableStyles).get(t))||(n={type:"style",instance:null,count:0,state:null},r.set(t,n)),n):{type:"void",instance:null,count:0,state:null};case"link":if("stylesheet"===r.rel&&"string"==typeof r.href&&"string"==typeof r.precedence){e=u8(r.href);var a,i,s,c,u=e5(o).hoistableStyles,d=u.get(e);if(d||(o=o.ownerDocument||o,d={type:"stylesheet",instance:null,count:0,state:{loading:0,preload:null}},u.set(e,d),(u=o.querySelector(u7(e)))&&!u._p&&(d.instance=u,d.state.loading=5),u1.has(e)||(r={rel:"preload",as:"style",href:r.href,crossOrigin:r.crossOrigin,integrity:r.integrity,media:r.media,hrefLang:r.hrefLang,referrerPolicy:r.referrerPolicy},u1.set(e,r),u||(a=o,i=e,s=r,c=d.state,a.querySelector('link[rel="preload"][as="style"]['+i+"]")?c.loading=1:(c.preload=i=a.createElement("link"),i.addEventListener("load",function(){return c.loading|=1}),i.addEventListener("error",function(){return c.loading|=2}),ui(i,"link",s),e6(i),a.head.appendChild(i))))),t&&null===n)throw Error(l(528,""));return d}if(t&&null!==n)throw Error(l(529,""));return null;case"script":return t=r.async,"string"==typeof(r=r.src)&&t&&"function"!=typeof t&&"symbol"!=typeof t?(t=dt(r),(n=(r=e5(o).hoistableScripts).get(t))||(n={type:"script",instance:null,count:0,state:null},r.set(t,n)),n):{type:"void",instance:null,count:0,state:null};default:throw Error(l(444,e))}}function u8(e){return'href="'+tm(e)+'"'}function u7(e){return'link[rel="stylesheet"]['+e+"]"}function de(e){return w({},e,{"data-precedence":e.precedence,precedence:null})}function dt(e){return'[src="'+tm(e)+'"]'}function dr(e){return"script[async]"+e}function dn(e,t,r){if(t.count++,null===t.instance)switch(t.type){case"style":var n=e.querySelector('style[data-href~="'+tm(r.href)+'"]');if(n)return t.instance=n,e6(n),n;var o=w({},r,{"data-href":r.href,"data-precedence":r.precedence,href:null,precedence:null});return e6(n=(e.ownerDocument||e).createElement("style")),ui(n,"style",o),da(n,r.precedence,e),t.instance=n;case"stylesheet":o=u8(r.href);var a=e.querySelector(u7(o));if(a)return t.state.loading|=4,t.instance=a,e6(a),a;n=de(r),(o=u1.get(o))&&di(n,o),e6(a=(e.ownerDocument||e).createElement("link"));var i=a;return i._p=new Promise(function(e,t){i.onload=e,i.onerror=t}),ui(a,"link",n),t.state.loading|=4,da(a,r.precedence,e),t.instance=a;case"script":if(a=dt(r.src),o=e.querySelector(dr(a)))return t.instance=o,e6(o),o;return n=r,(o=u1.get(a))&&dl(n=w({},r),o),e6(o=(e=e.ownerDocument||e).createElement("script")),ui(o,"link",n),e.head.appendChild(o),t.instance=o;case"void":return null;default:throw Error(l(443,t.type))}return"stylesheet"===t.type&&0==(4&t.state.loading)&&(n=t.instance,t.state.loading|=4,da(n,r.precedence,e)),t.instance}function da(e,t,r){for(var n=r.querySelectorAll('link[rel="stylesheet"][data-precedence],style[data-precedence]'),o=n.length?n[n.length-1]:null,a=o,i=0;i<n.length;i++){var l=n[i];if(l.dataset.precedence===t)a=l;else if(a!==o)break}a?a.parentNode.insertBefore(e,a.nextSibling):(t=9===r.nodeType?r.head:r).insertBefore(e,t.firstChild)}function di(e,t){null==e.crossOrigin&&(e.crossOrigin=t.crossOrigin),null==e.referrerPolicy&&(e.referrerPolicy=t.referrerPolicy),null==e.title&&(e.title=t.title)}function dl(e,t){null==e.crossOrigin&&(e.crossOrigin=t.crossOrigin),null==e.referrerPolicy&&(e.referrerPolicy=t.referrerPolicy),null==e.integrity&&(e.integrity=t.integrity)}var ds=null;function dc(e,t,r){if(null===ds){var n=new Map,o=ds=new Map;o.set(r,n)}else(n=(o=ds).get(r))||(n=new Map,o.set(r,n));if(n.has(e))return n;for(n.set(e,null),r=r.getElementsByTagName(e),o=0;o<r.length;o++){var a=r[o];if(!(a[e0]||a[eW]||"link"===e&&"stylesheet"===a.getAttribute("rel"))&&"http://www.w3.org/2000/svg"!==a.namespaceURI){var i=a.getAttribute(t)||"";i=e+i;var l=n.get(i);l?l.push(a):n.set(i,[a])}}return n}function du(e,t,r){(e=e.ownerDocument||e).head.insertBefore(r,"title"===t?e.querySelector("head > title"):null)}function dd(e,t){return"img"===e&&null!=t.src&&""!==t.src&&null==t.onLoad&&"lazy"!==t.loading}function df(e){return"stylesheet"!==e.type||0!=(3&e.state.loading)}function dp(e){return(e.width||100)*(e.height||100)*("number"==typeof devicePixelRatio?devicePixelRatio:1)*.25}function dh(e,t){"function"==typeof t.decode&&(e.imgCount++,t.complete||(e.imgBytes+=dp(t),e.suspenseyImages.push(t)),e=dy.bind(e),t.decode().then(e,e))}var dm=0;function dg(e){if(0===e.count&&(0===e.imgCount||!e.waitingForImages)){if(e.stylesheets)dx(e,e.stylesheets);else if(e.unsuspend){var t=e.unsuspend;e.unsuspend=null,t()}}}function dv(){this.count--,dg(this)}function dy(){this.imgCount--,dg(this)}var db=null;function dx(e,t){e.stylesheets=null,null!==e.unsuspend&&(e.count++,db=new Map,t.forEach(d_,e),db=null,dv.call(e))}function d_(e,t){if(!(4&t.state.loading)){var r=db.get(e);if(r)var n=r.get(null);else{r=new Map,db.set(e,r);for(var o=e.querySelectorAll("link[data-precedence],style[data-precedence]"),a=0;a<o.length;a++){var i=o[a];("LINK"===i.nodeName||"not all"!==i.getAttribute("media"))&&(r.set(i.dataset.precedence,i),n=i)}n&&r.set(null,n)}i=(o=t.instance).getAttribute("data-precedence"),(a=r.get(i)||n)===n&&r.set(null,o),r.set(i,o),this.count++,n=dv.bind(this),o.addEventListener("load",n),o.addEventListener("error",n),a?a.parentNode.insertBefore(o,a.nextSibling):(e=9===e.nodeType?e.head:e).insertBefore(o,e.firstChild),t.state.loading|=4}}var dw={$$typeof:L,Provider:null,Consumer:null,_currentValue:q,_currentValue2:q,_threadCount:0};function dk(e,t,r,n,o,a,i,l,s){this.tag=1,this.containerInfo=e,this.pingCache=this.current=this.pendingChildren=null,this.timeoutHandle=-1,this.callbackNode=this.next=this.pendingContext=this.context=this.cancelPendingCommit=null,this.callbackPriority=0,this.expirationTimes=eA(-1),this.entangledLanes=this.shellSuspendCounter=this.errorRecoveryDisabledLanes=this.expiredLanes=this.warmLanes=this.pingedLanes=this.suspendedLanes=this.pendingLanes=0,this.entanglements=eA(0),this.hiddenUpdates=eA(null),this.identifierPrefix=n,this.onUncaughtError=o,this.onCaughtError=a,this.onRecoverableError=i,this.pooledCache=null,this.pooledCacheLanes=0,this.formState=s,this.transitionTypes=null,this.incompleteTransitions=new Map}function dj(e,t,r,n,o,a){o=o?nv:nv,null===n.context?n.context=o:n.pendingContext=o,(n=oB(t)).payload={element:r},null!==(a=void 0===a?null:a)&&(n.callback=a),null!==(r=oq(e,n,t))&&(ce(r,e,t),oW(r,e,t))}function dS(e,t){if(null!==(e=e.memoizedState)&&null!==e.dehydrated){var r=e.retryLane;e.retryLane=0!==r&&r<t?r:t}}function dC(e,t){dS(e,t),(e=e.alternate)&&dS(e,t)}function dE(e){if(13===e.tag||31===e.tag){var t=nh(e,0x4000000);null!==t&&ce(t,e,0x4000000),dC(e,0x4000000)}}function dT(e){if(13===e.tag||31===e.tag){var t=s9(),r=nh(e,t=e$(t));null!==r&&ce(r,e,t),dC(e,t)}}var dN=!0;function dL(e,t,r,n){var o=V.T;V.T=null;var a=B.p;try{B.p=2,dP(e,t,r,n)}finally{B.p=a,V.T=o}}function dI(e,t,r,n){var o=V.T;V.T=null;var a=B.p;try{B.p=8,dP(e,t,r,n)}finally{B.p=a,V.T=o}}function dP(e,t,r,n){if(dN){var o=dz(n);if(null===o)c5(e,t,n,dR,r),dB(e,n);else if(function(e,t,r,n,o){switch(t){case"focusin":return dD=dq(dD,e,t,r,n,o),!0;case"dragenter":return dZ=dq(dZ,e,t,r,n,o),!0;case"mouseover":return dF=dq(dF,e,t,r,n,o),!0;case"pointerover":var a=o.pointerId;return dU.set(a,dq(dU.get(a)||null,e,t,r,n,o)),!0;case"gotpointercapture":return a=o.pointerId,d$.set(a,dq(d$.get(a)||null,e,t,r,n,o)),!0}return!1}(o,e,t,r,n))n.stopPropagation();else if(dB(e,n),4&t&&-1<dV.indexOf(e)){for(;null!==o;){var a=e3(o);if(null!==a)switch(a.tag){case 3:if((a=a.stateNode).current.memoizedState.isDehydrated){var i=ez(a.pendingLanes);if(0!==i){var l=a;for(l.pendingLanes|=2,l.entangledLanes|=2;i;){var s=1<<31-eE(i);l.entanglements[1]|=s,i&=~s}cF(a),0==(6&sS)&&(sq=em()+500,cU(0,!1))}}break;case 31:case 13:null!==(l=nh(a,2))&&ce(l,a,2),co(),dC(a,2)}if(null===(a=dz(n))&&c5(e,t,n,dR,r),a===o)break;o=a}null!==o&&n.stopPropagation()}else c5(e,t,n,null,r)}}function dz(e){return dO(e=tP(e))}var dR=null;function dO(e){if(dR=null,null!==(e=e2(e))){var t=s(e);if(null===t)e=null;else{var r=t.tag;if(13===r){if(null!==(e=c(t)))return e;e=null}else if(31===r){if(null!==(e=u(t)))return e;e=null}else if(3===r){if(t.stateNode.current.memoizedState.isDehydrated)return 3===t.tag?t.stateNode.containerInfo:null;e=null}else t!==e&&(e=null)}}return dR=e,null}function dM(e){switch(e){case"beforetoggle":case"cancel":case"click":case"close":case"contextmenu":case"copy":case"cut":case"auxclick":case"dblclick":case"dragend":case"dragstart":case"drop":case"focusin":case"focusout":case"input":case"invalid":case"keydown":case"keypress":case"keyup":case"mousedown":case"mouseup":case"paste":case"pause":case"play":case"pointercancel":case"pointerdown":case"pointerup":case"ratechange":case"reset":case"seeked":case"submit":case"toggle":case"touchcancel":case"touchend":case"touchstart":case"volumechange":case"change":case"selectionchange":case"textInput":case"compositionstart":case"compositionend":case"compositionupdate":case"beforeblur":case"afterblur":case"beforeinput":case"blur":case"fullscreenchange":case"fullscreenerror":case"focus":case"hashchange":case"popstate":case"select":case"selectstart":return 2;case"drag":case"dragenter":case"dragexit":case"dragleave":case"dragover":case"mousemove":case"mouseout":case"mouseover":case"pointermove":case"pointerout":case"pointerover":case"resize":case"scroll":case"touchmove":case"wheel":case"mouseenter":case"mouseleave":case"pointerenter":case"pointerleave":return 8;case"message":switch(eg()){case ev:return 2;case ey:return 8;case eb:case ex:return 32;case e_:return 0x10000000;default:return 32}default:return 32}}var dA=!1,dD=null,dZ=null,dF=null,dU=new Map,d$=new Map,dH=[],dV="mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset".split(" ");function dB(e,t){switch(e){case"focusin":case"focusout":dD=null;break;case"dragenter":case"dragleave":dZ=null;break;case"mouseover":case"mouseout":dF=null;break;case"pointerover":case"pointerout":dU.delete(t.pointerId);break;case"gotpointercapture":case"lostpointercapture":d$.delete(t.pointerId)}}function dq(e,t,r,n,o,a){return null===e||e.nativeEvent!==a?(e={blockedOn:t,domEventName:r,eventSystemFlags:n,nativeEvent:a,targetContainers:[o]},null!==t&&null!==(t=e3(t))&&dE(t)):(e.eventSystemFlags|=n,t=e.targetContainers,null!==o&&-1===t.indexOf(o)&&t.push(o)),e}function dW(e){var t=e2(e.target);if(null!==t){var r=s(t);if(null!==r){if(13===(t=r.tag)){if(null!==(t=c(r))){e.blockedOn=t,eB(e.priority,function(){dT(r)});return}}else if(31===t){if(null!==(t=u(r))){e.blockedOn=t,eB(e.priority,function(){dT(r)});return}}else if(3===t&&r.stateNode.current.memoizedState.isDehydrated){e.blockedOn=3===r.tag?r.stateNode.containerInfo:null;return}}}e.blockedOn=null}function dK(e){if(null!==e.blockedOn)return!1;for(var t=e.targetContainers;0<t.length;){var r=dz(e.nativeEvent);if(null!==r)return null!==(t=e3(r))&&dE(t),e.blockedOn=r,!1;var n=new(r=e.nativeEvent).constructor(r.type,r);tI=n,r.target.dispatchEvent(n),tI=null,t.shift()}return!0}function dY(e,t,r){dK(e)&&r.delete(t)}function dX(){dA=!1,null!==dD&&dK(dD)&&(dD=null),null!==dZ&&dK(dZ)&&(dZ=null),null!==dF&&dK(dF)&&(dF=null),dU.forEach(dY),d$.forEach(dY)}function dG(e,t){e.blockedOn===t&&(e.blockedOn=null,dA||(dA=!0,o.unstable_scheduleCallback(o.unstable_NormalPriority,dX)))}var dQ=null;function dJ(e){dQ!==e&&(dQ=e,o.unstable_scheduleCallback(o.unstable_NormalPriority,function(){dQ===e&&(dQ=null);for(var t=0;t<e.length;t+=3){var r=e[t],n=e[t+1],o=e[t+2];if("function"!=typeof n)if(null===dO(n||r))continue;else break;var a=e3(r);null!==a&&(e.splice(t,3),t-=3,id(a,{pending:!0,data:o,method:r.method,action:n},n,o))}}))}function d0(e){function t(t){return dG(t,e)}null!==dD&&dG(dD,e),null!==dZ&&dG(dZ,e),null!==dF&&dG(dF,e),dU.forEach(t),d$.forEach(t);for(var r=0;r<dH.length;r++){var n=dH[r];n.blockedOn===e&&(n.blockedOn=null)}for(;0<dH.length&&null===(r=dH[0]).blockedOn;)dW(r),null===r.blockedOn&&dH.shift();if(null!=(r=(e.ownerDocument||e).$$reactFormReplay))for(n=0;n<r.length;n+=3){var o=r[n],a=r[n+1],i=o[eK]||null;if("function"==typeof a)i||dJ(r);else if(i){var l=null;if(a&&a.hasAttribute("formAction")){if(o=a,i=a[eK]||null)l=i.formAction;else if(null!==dO(o))continue}else l=i.action;"function"==typeof l?r[n+1]=l:(r.splice(n,3),n-=3),dJ(r)}}}function d1(){function e(e){e.canIntercept&&"react-transition"===e.info&&e.intercept({handler:function(){return new Promise(function(e){return o=e})},focusReset:"manual",scroll:"manual"})}function t(){null!==o&&(o(),o=null),n||setTimeout(r,20)}function r(){if(!n&&!navigation.transition){var e=navigation.currentEntry;e&&null!=e.url&&navigation.navigate(e.url,{state:e.getState(),info:"react-transition",history:"replace"})}}if("object"==typeof navigation){var n=!1,o=null;return navigation.addEventListener("navigate",e),navigation.addEventListener("navigatesuccess",t),navigation.addEventListener("navigateerror",t),setTimeout(r,100),function(){n=!0,navigation.removeEventListener("navigate",e),navigation.removeEventListener("navigatesuccess",t),navigation.removeEventListener("navigateerror",t),null!==o&&(o(),o=null)}}}function d2(e){this._internalRoot=e}function d3(e){this._internalRoot=e}d3.prototype.render=d2.prototype.render=function(e){var t=this._internalRoot;if(null===t)throw Error(l(409));dj(t.current,s9(),e,t,null,null)},d3.prototype.unmount=d2.prototype.unmount=function(){var e=this._internalRoot;if(null!==e){this._internalRoot=null;var t=e.containerInfo;dj(e.current,2,null,e,null,null),co(),t[eY]=null}},d3.prototype.unstable_scheduleHydration=function(e){if(e){var t=eV();e={blockedOn:null,target:e,priority:t};for(var r=0;r<dH.length&&0!==t&&t<dH[r].priority;r++);dH.splice(r,0,e),0===r&&dW(e)}};var d4=a.version;if("19.3.0-canary-3f0b9e61-20260317"!==d4)throw Error(l(527,d4,"19.3.0-canary-3f0b9e61-20260317"));if(B.findDOMNode=function(e){var t=e._reactInternals;if(void 0===t){if("function"==typeof e.render)throw Error(l(188));throw Error(l(268,e=Object.keys(e).join(",")))}return null===(e=null!==(e=function(e){var t=e.alternate;if(!t){if(null===(t=s(e)))throw Error(l(188));return t!==e?null:e}for(var r=e,n=t;;){var o=r.return;if(null===o)break;var a=o.alternate;if(null===a){if(null!==(n=o.return)){r=n;continue}break}if(o.child===a.child){for(a=o.child;a;){if(a===r)return d(o),e;if(a===n)return d(o),t;a=a.sibling}throw Error(l(188))}if(r.return!==n.return)r=o,n=a;else{for(var i=!1,c=o.child;c;){if(c===r){i=!0,r=o,n=a;break}if(c===n){i=!0,n=o,r=a;break}c=c.sibling}if(!i){for(c=a.child;c;){if(c===r){i=!0,r=a,n=o;break}if(c===n){i=!0,n=a,r=o;break}c=c.sibling}if(!i)throw Error(l(189))}}if(r.alternate!==n)throw Error(l(190))}if(3!==r.tag)throw Error(l(188));return r.stateNode.current===r?e:t}(t))?function e(t){var r=t.tag;if(5===r||26===r||27===r||6===r)return t;for(t=t.child;null!==t;){if(null!==(r=e(t)))return r;t=t.sibling}return null}(e):null)?null:e.stateNode},"undefined"!=typeof __REACT_DEVTOOLS_GLOBAL_HOOK__){var d5=__REACT_DEVTOOLS_GLOBAL_HOOK__;if(!d5.isDisabled&&d5.supportsFiber)try{ej=d5.inject({bundleType:0,version:"19.3.0-canary-3f0b9e61-20260317",rendererPackageName:"react-dom",currentDispatcherRef:V,reconcilerVersion:"19.3.0-canary-3f0b9e61-20260317"}),eS=d5}catch(e){}}t.createRoot=function(e,t){if(!(r=e)||1!==r.nodeType&&9!==r.nodeType&&11!==r.nodeType)throw Error(l(299));var r,n,o,a,i,s,c,u,d=!1,f="",p=iO,h=iM,m=iA;return null!=t&&(!0===t.unstable_strictMode&&(d=!0),void 0!==t.identifierPrefix&&(f=t.identifierPrefix),void 0!==t.onUncaughtError&&(p=t.onUncaughtError),void 0!==t.onCaughtError&&(h=t.onCaughtError),void 0!==t.onRecoverableError&&(m=t.onRecoverableError)),n=e,o=1,a=!1,i=null,s=0,c=d,u=null,n=new dk(n,o,a,f,p,h,m,d1,null),o=1,!0===c&&(o|=24),c=nb(3,null,null,o),n.current=c,c.stateNode=n,o=ou(),o.refCount++,n.pooledCache=o,o.refCount++,c.memoizedState={element:null,isDehydrated:a,cache:o},oH(c),t=n,e[eY]=t.current,c3(e),new d2(t)}},"./dist/compiled/react-dom/cjs/react-dom.production.js"(e,t,r){"use strict";var n=r("./dist/compiled/react/index.js");function o(e){var t="https://react.dev/errors/"+e;if(1<arguments.length){t+="?args[]="+encodeURIComponent(arguments[1]);for(var r=2;r<arguments.length;r++)t+="&args[]="+encodeURIComponent(arguments[r])}return"Minified React error #"+e+"; visit "+t+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}function a(){}var i={d:{f:a,r:function(){throw Error(o(522))},D:a,C:a,L:a,m:a,X:a,S:a,M:a},p:0,findDOMNode:null},l=Symbol.for("react.portal"),s=Symbol.for("react.optimistic_key"),c=n.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE;function u(e,t){return"font"===e?"":"string"==typeof t?"use-credentials"===t?t:"":void 0}t.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE=i,t.createPortal=function(e,t){var r=2<arguments.length&&void 0!==arguments[2]?arguments[2]:null;if(!t||1!==t.nodeType&&9!==t.nodeType&&11!==t.nodeType)throw Error(o(299));return function(e,t,r){var n=3<arguments.length&&void 0!==arguments[3]?arguments[3]:null;return{$$typeof:l,key:null==n?null:n===s?s:""+n,children:e,containerInfo:t,implementation:r}}(e,t,null,r)},t.flushSync=function(e){var t=c.T,r=i.p;try{if(c.T=null,i.p=2,e)return e()}finally{c.T=t,i.p=r,i.d.f()}},t.preconnect=function(e,t){"string"==typeof e&&(t=t?"string"==typeof(t=t.crossOrigin)?"use-credentials"===t?t:"":void 0:null,i.d.C(e,t))},t.prefetchDNS=function(e){"string"==typeof e&&i.d.D(e)},t.preinit=function(e,t){if("string"==typeof e&&t&&"string"==typeof t.as){var r=t.as,n=u(r,t.crossOrigin),o="string"==typeof t.integrity?t.integrity:void 0,a="string"==typeof t.fetchPriority?t.fetchPriority:void 0;"style"===r?i.d.S(e,"string"==typeof t.precedence?t.precedence:void 0,{crossOrigin:n,integrity:o,fetchPriority:a}):"script"===r&&i.d.X(e,{crossOrigin:n,integrity:o,fetchPriority:a,nonce:"string"==typeof t.nonce?t.nonce:void 0})}},t.preinitModule=function(e,t){if("string"==typeof e)if("object"==typeof t&&null!==t){if(null==t.as||"script"===t.as){var r=u(t.as,t.crossOrigin);i.d.M(e,{crossOrigin:r,integrity:"string"==typeof t.integrity?t.integrity:void 0,nonce:"string"==typeof t.nonce?t.nonce:void 0})}}else null==t&&i.d.M(e)},t.preload=function(e,t){if("string"==typeof e&&"object"==typeof t&&null!==t&&"string"==typeof t.as){var r=t.as,n=u(r,t.crossOrigin);i.d.L(e,r,{crossOrigin:n,integrity:"string"==typeof t.integrity?t.integrity:void 0,nonce:"string"==typeof t.nonce?t.nonce:void 0,type:"string"==typeof t.type?t.type:void 0,fetchPriority:"string"==typeof t.fetchPriority?t.fetchPriority:void 0,referrerPolicy:"string"==typeof t.referrerPolicy?t.referrerPolicy:void 0,imageSrcSet:"string"==typeof t.imageSrcSet?t.imageSrcSet:void 0,imageSizes:"string"==typeof t.imageSizes?t.imageSizes:void 0,media:"string"==typeof t.media?t.media:void 0})}},t.preloadModule=function(e,t){if("string"==typeof e)if(t){var r=u(t.as,t.crossOrigin);i.d.m(e,{as:"string"==typeof t.as&&"script"!==t.as?t.as:void 0,crossOrigin:r,integrity:"string"==typeof t.integrity?t.integrity:void 0})}else i.d.m(e)},t.requestFormReset=function(e){i.d.r(e)},t.unstable_batchedUpdates=function(e,t){return e(t)},t.useFormState=function(e,t,r){return c.H.useFormState(e,t,r)},t.useFormStatus=function(){return c.H.useHostTransitionStatus()},t.version="19.3.0-canary-3f0b9e61-20260317"},"./dist/compiled/react-dom/client.js"(e,t,r){"use strict";!function e(){if("undefined"!=typeof __REACT_DEVTOOLS_GLOBAL_HOOK__&&"function"==typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE)try{__REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(e)}catch(e){console.error(e)}}(),e.exports=r("./dist/compiled/react-dom/cjs/react-dom-client.production.js")},"./dist/compiled/react-dom/index.js"(e,t,r){"use strict";!function e(){if("undefined"!=typeof __REACT_DEVTOOLS_GLOBAL_HOOK__&&"function"==typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE)try{__REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(e)}catch(e){console.error(e)}}(),e.exports=r("./dist/compiled/react-dom/cjs/react-dom.production.js")},"./dist/compiled/react/cjs/react-compiler-runtime.production.js"(e,t,r){"use strict";var n=r("./dist/compiled/react/index.js").__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE;t.c=function(e){return n.H.useMemoCache(e)}},"./dist/compiled/react/cjs/react-jsx-runtime.production.js"(e,t){"use strict";var r=Symbol.for("react.transitional.element");function n(e,t,n){var o=null;if(void 0!==n&&(o=""+n),void 0!==t.key&&(o=""+t.key),"key"in t)for(var a in n={},t)"key"!==a&&(n[a]=t[a]);else n=t;return{$$typeof:r,type:e,key:o,ref:void 0!==(t=n.ref)?t:null,props:n}}t.Fragment=Symbol.for("react.fragment"),t.jsx=n,t.jsxs=n},"./dist/compiled/react/cjs/react.production.js"(e,t){"use strict";var r=Symbol.for("react.transitional.element"),n=Symbol.for("react.portal"),o=Symbol.for("react.fragment"),a=Symbol.for("react.strict_mode"),i=Symbol.for("react.profiler"),l=Symbol.for("react.consumer"),s=Symbol.for("react.context"),c=Symbol.for("react.forward_ref"),u=Symbol.for("react.suspense"),d=Symbol.for("react.memo"),f=Symbol.for("react.lazy"),p=Symbol.for("react.activity"),h=Symbol.for("react.view_transition"),m=Symbol.iterator,g={isMounted:function(){return!1},enqueueForceUpdate:function(){},enqueueReplaceState:function(){},enqueueSetState:function(){}},v=Object.assign,y={};function b(e,t,r){this.props=e,this.context=t,this.refs=y,this.updater=r||g}function x(){}function _(e,t,r){this.props=e,this.context=t,this.refs=y,this.updater=r||g}b.prototype.isReactComponent={},b.prototype.setState=function(e,t){if("object"!=typeof e&&"function"!=typeof e&&null!=e)throw Error("takes an object of state variables to update or a function which returns an object of state variables.");this.updater.enqueueSetState(this,e,t,"setState")},b.prototype.forceUpdate=function(e){this.updater.enqueueForceUpdate(this,e,"forceUpdate")},x.prototype=b.prototype;var w=_.prototype=new x;w.constructor=_,v(w,b.prototype),w.isPureReactComponent=!0;var k=Array.isArray;function j(){}var S={H:null,A:null,T:null,S:null},C=Object.prototype.hasOwnProperty;function E(e,t,n){var o=n.ref;return{$$typeof:r,type:e,key:t,ref:void 0!==o?o:null,props:n}}function T(e){return"object"==typeof e&&null!==e&&e.$$typeof===r}var N=/\/+/g;function L(e,t){var r,n;return"object"==typeof e&&null!==e&&null!=e.key?(r=""+e.key,n={"=":"=0",":":"=2"},"$"+r.replace(/[=:]/g,function(e){return n[e]})):t.toString(36)}function I(e,t,o){if(null==e)return e;var a=[],i=0;return!function e(t,o,a,i,l){var s,c,u,d=typeof t;("undefined"===d||"boolean"===d)&&(t=null);var p=!1;if(null===t)p=!0;else switch(d){case"bigint":case"string":case"number":p=!0;break;case"object":switch(t.$$typeof){case r:case n:p=!0;break;case f:return e((p=t._init)(t._payload),o,a,i,l)}}if(p)return l=l(t),p=""===i?"."+L(t,0):i,k(l)?(a="",null!=p&&(a=p.replace(N,"$&/")+"/"),e(l,o,a,"",function(e){return e})):null!=l&&(T(l)&&(s=l,c=a+(null==l.key||t&&t.key===l.key?"":(""+l.key).replace(N,"$&/")+"/")+p,l=E(s.type,c,s.props)),o.push(l)),1;p=0;var h=""===i?".":i+":";if(k(t))for(var g=0;g<t.length;g++)d=h+L(i=t[g],g),p+=e(i,o,a,d,l);else if("function"==typeof(g=null===(u=t)||"object"!=typeof u?null:"function"==typeof(u=m&&u[m]||u["@@iterator"])?u:null))for(t=g.call(t),g=0;!(i=t.next()).done;)d=h+L(i=i.value,g++),p+=e(i,o,a,d,l);else if("object"===d){if("function"==typeof t.then)return e(function(e){switch(e.status){case"fulfilled":return e.value;case"rejected":throw e.reason;default:switch("string"==typeof e.status?e.then(j,j):(e.status="pending",e.then(function(t){"pending"===e.status&&(e.status="fulfilled",e.value=t)},function(t){"pending"===e.status&&(e.status="rejected",e.reason=t)})),e.status){case"fulfilled":return e.value;case"rejected":throw e.reason}}throw e}(t),o,a,i,l);throw Error("Objects are not valid as a React child (found: "+("[object Object]"===(o=String(t))?"object with keys {"+Object.keys(t).join(", ")+"}":o)+"). If you meant to render a collection of children, use an array instead.")}return p}(e,a,"","",function(e){return t.call(o,e,i++)}),a}function P(e){if(-1===e._status){var t=(0,e._result)();t.then(function(r){(0===e._status||-1===e._status)&&(e._status=1,e._result=r,void 0===t.status&&(t.status="fulfilled",t.value=r))},function(r){(0===e._status||-1===e._status)&&(e._status=2,e._result=r,void 0===t.status&&(t.status="rejected",t.reason=r))}),-1===e._status&&(e._status=0,e._result=t)}if(1===e._status)return e._result.default;throw e._result}var z="function"==typeof reportError?reportError:function(e){if("object"==typeof window&&"function"==typeof window.ErrorEvent){var t=new window.ErrorEvent("error",{bubbles:!0,cancelable:!0,message:"object"==typeof e&&null!==e&&"string"==typeof e.message?String(e.message):String(e),error:e});if(!window.dispatchEvent(t))return}else if("object"==typeof process&&"function"==typeof process.emit)return void process.emit("uncaughtException",e);console.error(e)};function R(e){var t=S.T,r={};r.types=null!==t?t.types:null,S.T=r;try{var n=e(),o=S.S;null!==o&&o(r,n),"object"==typeof n&&null!==n&&"function"==typeof n.then&&n.then(j,z)}catch(e){z(e)}finally{null!==t&&null!==r.types&&(t.types=r.types),S.T=t}}function O(e){var t=S.T;if(null!==t){var r=t.types;null===r?t.types=[e]:-1===r.indexOf(e)&&r.push(e)}else R(O.bind(null,e))}t.Activity=p,t.Children={map:I,forEach:function(e,t,r){I(e,function(){t.apply(this,arguments)},r)},count:function(e){var t=0;return I(e,function(){t++}),t},toArray:function(e){return I(e,function(e){return e})||[]},only:function(e){if(!T(e))throw Error("React.Children.only expected to receive a single React element child.");return e}},t.Component=b,t.Fragment=o,t.Profiler=i,t.PureComponent=_,t.StrictMode=a,t.Suspense=u,t.ViewTransition=h,t.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE=S,t.__COMPILER_RUNTIME={__proto__:null,c:function(e){return S.H.useMemoCache(e)}},t.addTransitionType=O,t.cache=function(e){return function(){return e.apply(null,arguments)}},t.cacheSignal=function(){return null},t.cloneElement=function(e,t,r){if(null==e)throw Error("The argument must be a React element, but you passed "+e+".");var n=v({},e.props),o=e.key;if(null!=t)for(a in void 0!==t.key&&(o=""+t.key),t)C.call(t,a)&&"key"!==a&&"__self"!==a&&"__source"!==a&&("ref"!==a||void 0!==t.ref)&&(n[a]=t[a]);var a=arguments.length-2;if(1===a)n.children=r;else if(1<a){for(var i=Array(a),l=0;l<a;l++)i[l]=arguments[l+2];n.children=i}return E(e.type,o,n)},t.createContext=function(e){return(e={$$typeof:s,_currentValue:e,_currentValue2:e,_threadCount:0,Provider:null,Consumer:null}).Provider=e,e.Consumer={$$typeof:l,_context:e},e},t.createElement=function(e,t,r){var n,o={},a=null;if(null!=t)for(n in void 0!==t.key&&(a=""+t.key),t)C.call(t,n)&&"key"!==n&&"__self"!==n&&"__source"!==n&&(o[n]=t[n]);var i=arguments.length-2;if(1===i)o.children=r;else if(1<i){for(var l=Array(i),s=0;s<i;s++)l[s]=arguments[s+2];o.children=l}if(e&&e.defaultProps)for(n in i=e.defaultProps)void 0===o[n]&&(o[n]=i[n]);return E(e,a,o)},t.createRef=function(){return{current:null}},t.forwardRef=function(e){return{$$typeof:c,render:e}},t.isValidElement=T,t.lazy=function(e){return{$$typeof:f,_payload:{_status:-1,_result:e},_init:P}},t.memo=function(e,t){return{$$typeof:d,type:e,compare:void 0===t?null:t}},t.startTransition=R,t.unstable_useCacheRefresh=function(){return S.H.useCacheRefresh()},t.use=function(e){return S.H.use(e)},t.useActionState=function(e,t,r){return S.H.useActionState(e,t,r)},t.useCallback=function(e,t){return S.H.useCallback(e,t)},t.useContext=function(e){return S.H.useContext(e)},t.useDebugValue=function(){},t.useDeferredValue=function(e,t){return S.H.useDeferredValue(e,t)},t.useEffect=function(e,t){return S.H.useEffect(e,t)},t.useEffectEvent=function(e){return S.H.useEffectEvent(e)},t.useId=function(){return S.H.useId()},t.useImperativeHandle=function(e,t,r){return S.H.useImperativeHandle(e,t,r)},t.useInsertionEffect=function(e,t){return S.H.useInsertionEffect(e,t)},t.useLayoutEffect=function(e,t){return S.H.useLayoutEffect(e,t)},t.useMemo=function(e,t){return S.H.useMemo(e,t)},t.useOptimistic=function(e,t){return S.H.useOptimistic(e,t)},t.useReducer=function(e,t,r){return S.H.useReducer(e,t,r)},t.useRef=function(e){return S.H.useRef(e)},t.useState=function(e){return S.H.useState(e)},t.useSyncExternalStore=function(e,t,r){return S.H.useSyncExternalStore(e,t,r)},t.useTransition=function(){return S.H.useTransition()},t.version="19.3.0-canary-3f0b9e61-20260317"},"./dist/compiled/react/compiler-runtime.js"(e,t,r){"use strict";e.exports=r("./dist/compiled/react/cjs/react-compiler-runtime.production.js")},"./dist/compiled/react/index.js"(e,t,r){"use strict";e.exports=r("./dist/compiled/react/cjs/react.production.js")},"./dist/compiled/react/jsx-runtime.js"(e,t,r){"use strict";e.exports=r("./dist/compiled/react/cjs/react-jsx-runtime.production.js")},"./dist/compiled/scheduler/cjs/scheduler.production.js"(e,t){"use strict";function r(e,t){var r=e.length;for(e.push(t);0<r;){var n=r-1>>>1,o=e[n];if(0<a(o,t))e[n]=t,e[r]=o,r=n;else break}}function n(e){return 0===e.length?null:e[0]}function o(e){if(0===e.length)return null;var t=e[0],r=e.pop();if(r!==t){e[0]=r;for(var n=0,o=e.length,i=o>>>1;n<i;){var l=2*(n+1)-1,s=e[l],c=l+1,u=e[c];if(0>a(s,r))c<o&&0>a(u,s)?(e[n]=u,e[c]=r,n=c):(e[n]=s,e[l]=r,n=l);else if(c<o&&0>a(u,r))e[n]=u,e[c]=r,n=c;else break}}return t}function a(e,t){var r=e.sortIndex-t.sortIndex;return 0!==r?r:e.id-t.id}if(t.unstable_now=void 0,"object"==typeof performance&&"function"==typeof performance.now){var i,l=performance;t.unstable_now=function(){return l.now()}}else{var s=Date,c=s.now();t.unstable_now=function(){return s.now()-c}}var u=[],d=[],f=1,p=null,h=3,m=!1,g=!1,v=!1,y=!1,b="function"==typeof setTimeout?setTimeout:null,x="function"==typeof clearTimeout?clearTimeout:null,_="undefined"!=typeof setImmediate?setImmediate:null;function w(e){for(var t=n(d);null!==t;){if(null===t.callback)o(d);else if(t.startTime<=e)o(d),t.sortIndex=t.expirationTime,r(u,t);else break;t=n(d)}}function k(e){if(v=!1,w(e),!g)if(null!==n(u))g=!0,j||(j=!0,i());else{var t=n(d);null!==t&&P(k,t.startTime-e)}}var j=!1,S=-1,C=5,E=-1;function T(){return!!y||!(t.unstable_now()-E<C)}function N(){if(y=!1,j){var e=t.unstable_now();E=e;var r=!0;try{e:{g=!1,v&&(v=!1,x(S),S=-1),m=!0;var a=h;try{t:{for(w(e),p=n(u);null!==p&&!(p.expirationTime>e&&T());){var l=p.callback;if("function"==typeof l){p.callback=null,h=p.priorityLevel;var s=l(p.expirationTime<=e);if(e=t.unstable_now(),"function"==typeof s){p.callback=s,w(e),r=!0;break t}p===n(u)&&o(u),w(e)}else o(u);p=n(u)}if(null!==p)r=!0;else{var c=n(d);null!==c&&P(k,c.startTime-e),r=!1}}break e}finally{p=null,h=a,m=!1}}}finally{r?i():j=!1}}}if("function"==typeof _)i=function(){_(N)};else if("undefined"!=typeof MessageChannel){var L=new MessageChannel,I=L.port2;L.port1.onmessage=N,i=function(){I.postMessage(null)}}else i=function(){b(N,0)};function P(e,r){S=b(function(){e(t.unstable_now())},r)}t.unstable_IdlePriority=5,t.unstable_ImmediatePriority=1,t.unstable_LowPriority=4,t.unstable_NormalPriority=3,t.unstable_Profiling=null,t.unstable_UserBlockingPriority=2,t.unstable_cancelCallback=function(e){e.callback=null},t.unstable_forceFrameRate=function(e){0>e||125<e?console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported"):C=0<e?Math.floor(1e3/e):5},t.unstable_getCurrentPriorityLevel=function(){return h},t.unstable_next=function(e){switch(h){case 1:case 2:case 3:var t=3;break;default:t=h}var r=h;h=t;try{return e()}finally{h=r}},t.unstable_requestPaint=function(){y=!0},t.unstable_runWithPriority=function(e,t){switch(e){case 1:case 2:case 3:case 4:case 5:break;default:e=3}var r=h;h=e;try{return t()}finally{h=r}},t.unstable_scheduleCallback=function(e,o,a){var l=t.unstable_now();switch(a="object"==typeof a&&null!==a&&"number"==typeof(a=a.delay)&&0<a?l+a:l,e){case 1:var s=-1;break;case 2:s=250;break;case 5:s=0x3fffffff;break;case 4:s=1e4;break;default:s=5e3}return s=a+s,e={id:f++,callback:o,priorityLevel:e,startTime:a,expirationTime:s,sortIndex:-1},a>l?(e.sortIndex=a,r(d,e),null===n(u)&&e===n(d)&&(v?(x(S),S=-1):v=!0,P(k,a-l))):(e.sortIndex=s,r(u,e),g||m||(g=!0,j||(j=!0,i()))),e},t.unstable_shouldYield=T,t.unstable_wrapCallback=function(e){var t=h;return function(){var r=h;h=t;try{return e.apply(this,arguments)}finally{h=r}}}},"./dist/compiled/scheduler/index.js"(e,t,r){"use strict";e.exports=r("./dist/compiled/scheduler/cjs/scheduler.production.js")},"./dist/compiled/stacktrace-parser/stack-trace-parser.cjs.js"(e){(()=>{"use strict";"undefined"!=typeof __nccwpck_require__&&(__nccwpck_require__.ab="//");var t,r,n,o,a,i,l,s,c={};Object.defineProperty(c,"__esModule",{value:!0}),t="<unknown>",r=/^\s*at (.*?) ?\(((?:file|https?|blob|chrome-extension|native|eval|webpack|webpack-internal|rsc|about|turbopack|<anonymous>|\/|[a-z]:\\|\\\\).*?)(?::(\d+))?(?::(\d+))?\)?\s*$/i,n=/\((\S*)(?::(\d+))(?::(\d+))\)/,o=/^\s*at (?:((?:\[object object\])?.+) )?\(?((?:file|ms-appx|https?|webpack|webpack-internal|rsc|about|turbopack|blob):.*?):(\d+)(?::(\d+))?\)?\s*$/i,a=/^\s*(.*?)(?:\((.*?)\))?(?:^|@)((?:file|https?|blob|chrome|webpack|webpack-internal|rsc|about|turbopack|resource|\[native).*?|[^@]*bundle)(?::(\d+))?(?::(\d+))?\s*$/i,i=/(\S+) line (\d+)(?: > eval line \d+)* > eval/i,l=/^\s*(?:([^@]*)(?:\((.*?)\))?@)?(\S.*?):(\d+)(?::(\d+))?\s*$/i,s=/^\s*at (?:((?:\[object object\])?[^\\/]+(?: \[as \S+\])?) )?\(?(.*?):(\d+)(?::(\d+))?\)?\s*$/i,c.parse=function(e){return e.split("\n").reduce(function(e,c){var u,d,f,p,h,m,g=function(e){var o=r.exec(e);if(!o)return null;var a=o[2]&&0===o[2].indexOf("native"),i=o[2]&&0===o[2].indexOf("eval"),l=n.exec(o[2]);return i&&null!=l&&(o[2]=l[1],o[3]=l[2],o[4]=l[3]),{file:a?null:o[2],methodName:o[1]||t,arguments:a?[o[2]]:[],lineNumber:o[3]?+o[3]:null,column:o[4]?+o[4]:null}}(c)||(u=c,(d=o.exec(u))?{file:d[2],methodName:d[1]||t,arguments:[],lineNumber:+d[3],column:d[4]?+d[4]:null}:null)||function(e){var r=a.exec(e);if(!r)return null;var n=r[3]&&r[3].indexOf(" > eval")>-1,o=i.exec(r[3]);return n&&null!=o&&(r[3]=o[1],r[4]=o[2],r[5]=null),{file:r[3],methodName:r[1]||t,arguments:r[2]?r[2].split(","):[],lineNumber:r[4]?+r[4]:null,column:r[5]?+r[5]:null}}(c)||(f=c,(p=s.exec(f))?{file:p[2],methodName:p[1]||t,arguments:[],lineNumber:+p[3],column:p[4]?+p[4]:null}:null)||(h=c,(m=l.exec(h))?{file:m[3],methodName:m[1]||t,arguments:[],lineNumber:+m[4],column:m[5]?+m[5]:null}:null);return g&&e.push(g),e},[])},e.exports=c})()},"./dist/compiled/strip-ansi/index.js"(e){(()=>{"use strict";var t={511:e=>{e.exports=({onlyFirst:e=!1}={})=>RegExp("[\\u001B\\u009B][[\\]()#;?]*(?:(?:(?:(?:;[-a-zA-Z\\d\\/#&.:=?%@~_]+)*|[a-zA-Z\\d]+(?:;[-a-zA-Z\\d\\/#&.:=?%@~_]*)*)?\\u0007)|(?:(?:\\d{1,4}(?:;\\d{0,4})*)?[\\dA-PR-TZcf-ntqry=><~]))",e?void 0:"g")},532:(e,t,r)=>{let n=r(511);e.exports=e=>"string"==typeof e?e.replace(n(),""):e}},r={};function n(e){var o=r[e];if(void 0!==o)return o.exports;var a=r[e]={exports:{}},i=!0;try{t[e](a,a.exports,n),i=!1}finally{i&&delete r[e]}return a.exports}n.ab="//",e.exports=n(532)})()},"./src/build/webpack/loaders/devtool/devtool-style-inject.js"(e){function t(){let e=window._nextjsDevtoolsStyleCache;if(e.cachedShadowRoot)return e.cachedShadowRoot;let t=document.querySelector("nextjs-portal"),r=t?.shadowRoot||null;return r&&(e.cachedShadowRoot=r),r}function r(e,t){let r=window._nextjsDevtoolsStyleCache;r.lastInsertedElement?r.lastInsertedElement.nextSibling?t.insertBefore(e,r.lastInsertedElement.nextSibling):t.appendChild(e):t.insertBefore(e,t.firstChild),r.lastInsertedElement=e}function n(){let e=window._nextjsDevtoolsStyleCache,n=t();n&&(e.pendingElements.forEach(e=>{r(e,n)}),e.pendingElements=[])}"undefined"!=typeof window&&(window._nextjsDevtoolsStyleCache=window._nextjsDevtoolsStyleCache||{pendingElements:[],isObserving:!1,lastInsertedElement:null,cachedShadowRoot:null}),e.exports=function(e){e.setAttribute("data-nextjs-dev-tool-style","true");let o=t();o?r(e,o):(window._nextjsDevtoolsStyleCache.pendingElements.push(e),function(){let e=window._nextjsDevtoolsStyleCache;if(e.isObserving)return;if(e.isObserving=!0,t())return n();let r=new MutationObserver(o=>{if(0!==o.length){for(let a of o)if(0!==a.addedNodes.length)for(let o of a.addedNodes){if(o.nodeType!==Node.ELEMENT_NODE)continue;let a=null;if("SCRIPT"===o.tagName&&o.getAttribute("data-nextjs-dev-overlay")?a=o.firstChild:"NEXTJS-PORTAL"===o.tagName&&(a=o),a){let o=()=>{t()?(n(),r.disconnect(),e.isObserving=!1):setTimeout(o,20)};o();return}}}});r.observe(document.body,{childList:!0,subtree:!0})}())}},"./dist/compiled/zod/index.cjs"(e){(()=>{"use strict";var t={629:function(e,t,r){var n=this&&this.__createBinding||(Object.create?function(e,t,r,n){void 0===n&&(n=r);var o=Object.getOwnPropertyDescriptor(t,r);(!o||("get"in o?!t.__esModule:o.writable||o.configurable))&&(o={enumerable:!0,get:function(){return t[r]}}),Object.defineProperty(e,n,o)}:function(e,t,r,n){void 0===n&&(n=r),e[n]=t[r]}),o=this&&this.__setModuleDefault||(Object.create?function(e,t){Object.defineProperty(e,"default",{enumerable:!0,value:t})}:function(e,t){e.default=t}),a=this&&this.__importStar||function(e){if(e&&e.__esModule)return e;var t={};if(null!=e)for(var r in e)"default"!==r&&Object.prototype.hasOwnProperty.call(e,r)&&n(t,e,r);return o(t,e),t},i=this&&this.__exportStar||function(e,t){for(var r in e)"default"===r||Object.prototype.hasOwnProperty.call(t,r)||n(t,e,r)};Object.defineProperty(t,"__esModule",{value:!0}),t.z=void 0;let l=a(r(923));t.z=l,i(r(923),t),t.default=l},348:(e,t,r)=>{Object.defineProperty(t,"__esModule",{value:!0}),t.ZodError=t.quotelessJson=t.ZodIssueCode=void 0;let n=r(709);t.ZodIssueCode=n.util.arrayToEnum(["invalid_type","invalid_literal","custom","invalid_union","invalid_union_discriminator","invalid_enum_value","unrecognized_keys","invalid_arguments","invalid_return_type","invalid_date","invalid_string","too_small","too_big","invalid_intersection_types","not_multiple_of","not_finite"]),t.quotelessJson=e=>JSON.stringify(e,null,2).replace(/"([^"]+)":/g,"$1:");class o extends Error{get errors(){return this.issues}constructor(e){super(),this.issues=[],this.addIssue=e=>{this.issues=[...this.issues,e]},this.addIssues=(e=[])=>{this.issues=[...this.issues,...e]};const t=new.target.prototype;Object.setPrototypeOf?Object.setPrototypeOf(this,t):this.__proto__=t,this.name="ZodError",this.issues=e}format(e){let t=e||function(e){return e.message},r={_errors:[]},n=e=>{for(let o of e.issues)if("invalid_union"===o.code)o.unionErrors.map(n);else if("invalid_return_type"===o.code)n(o.returnTypeError);else if("invalid_arguments"===o.code)n(o.argumentsError);else if(0===o.path.length)r._errors.push(t(o));else{let e=r,n=0;for(;n<o.path.length;){let r=o.path[n];n===o.path.length-1?(e[r]=e[r]||{_errors:[]},e[r]._errors.push(t(o))):e[r]=e[r]||{_errors:[]},e=e[r],n++}}};return n(this),r}static assert(e){if(!(e instanceof o))throw Error(`Not a ZodError: ${e}`)}toString(){return this.message}get message(){return JSON.stringify(this.issues,n.util.jsonStringifyReplacer,2)}get isEmpty(){return 0===this.issues.length}flatten(e=e=>e.message){let t={},r=[];for(let n of this.issues)if(n.path.length>0){let r=n.path[0];t[r]=t[r]||[],t[r].push(e(n))}else r.push(e(n));return{formErrors:r,fieldErrors:t}}get formErrors(){return this.flatten()}}t.ZodError=o,o.create=e=>new o(e)},61:function(e,t,r){var n=this&&this.__importDefault||function(e){return e&&e.__esModule?e:{default:e}};Object.defineProperty(t,"__esModule",{value:!0}),t.defaultErrorMap=void 0,t.setErrorMap=function(e){a=e},t.getErrorMap=function(){return a};let o=n(r(871));t.defaultErrorMap=o.default;let a=o.default},923:function(e,t,r){var n=this&&this.__createBinding||(Object.create?function(e,t,r,n){void 0===n&&(n=r);var o=Object.getOwnPropertyDescriptor(t,r);(!o||("get"in o?!t.__esModule:o.writable||o.configurable))&&(o={enumerable:!0,get:function(){return t[r]}}),Object.defineProperty(e,n,o)}:function(e,t,r,n){void 0===n&&(n=r),e[n]=t[r]}),o=this&&this.__exportStar||function(e,t){for(var r in e)"default"===r||Object.prototype.hasOwnProperty.call(t,r)||n(t,e,r)};Object.defineProperty(t,"__esModule",{value:!0}),o(r(61),t),o(r(818),t),o(r(515),t),o(r(709),t),o(r(155),t),o(r(348),t)},538:(e,t)=>{var r,n;Object.defineProperty(t,"__esModule",{value:!0}),t.errorUtil=void 0,(n=r||(t.errorUtil=r={})).errToObj=e=>"string"==typeof e?{message:e}:e||{},n.toString=e=>"string"==typeof e?e:e?.message},818:function(e,t,r){var n=this&&this.__importDefault||function(e){return e&&e.__esModule?e:{default:e}};Object.defineProperty(t,"__esModule",{value:!0}),t.isAsync=t.isValid=t.isDirty=t.isAborted=t.OK=t.DIRTY=t.INVALID=t.ParseStatus=t.EMPTY_PATH=t.makeIssue=void 0,t.addIssueToContext=function(e,r){let n=(0,o.getErrorMap)(),i=(0,t.makeIssue)({issueData:r,data:e.data,path:e.path,errorMaps:[e.common.contextualErrorMap,e.schemaErrorMap,n,n===a.default?void 0:a.default].filter(e=>!!e)});e.common.issues.push(i)};let o=r(61),a=n(r(871));t.makeIssue=e=>{let{data:t,path:r,errorMaps:n,issueData:o}=e,a=[...r,...o.path||[]],i={...o,path:a};if(void 0!==o.message)return{...o,path:a,message:o.message};let l="";for(let e of n.filter(e=>!!e).slice().reverse())l=e(i,{data:t,defaultError:l}).message;return{...o,path:a,message:l}},t.EMPTY_PATH=[];class i{constructor(){this.value="valid"}dirty(){"valid"===this.value&&(this.value="dirty")}abort(){"aborted"!==this.value&&(this.value="aborted")}static mergeArray(e,r){let n=[];for(let o of r){if("aborted"===o.status)return t.INVALID;"dirty"===o.status&&e.dirty(),n.push(o.value)}return{status:e.value,value:n}}static async mergeObjectAsync(e,t){let r=[];for(let e of t){let t=await e.key,n=await e.value;r.push({key:t,value:n})}return i.mergeObjectSync(e,r)}static mergeObjectSync(e,r){let n={};for(let o of r){let{key:r,value:a}=o;if("aborted"===r.status||"aborted"===a.status)return t.INVALID;"dirty"===r.status&&e.dirty(),"dirty"===a.status&&e.dirty(),"__proto__"!==r.value&&(void 0!==a.value||o.alwaysSet)&&(n[r.value]=a.value)}return{status:e.value,value:n}}}t.ParseStatus=i,t.INVALID=Object.freeze({status:"aborted"}),t.DIRTY=e=>({status:"dirty",value:e}),t.OK=e=>({status:"valid",value:e}),t.isAborted=e=>"aborted"===e.status,t.isDirty=e=>"dirty"===e.status,t.isValid=e=>"valid"===e.status,t.isAsync=e=>"undefined"!=typeof Promise&&e instanceof Promise},515:(e,t)=>{Object.defineProperty(t,"__esModule",{value:!0})},709:(e,t)=>{var r,n,o;Object.defineProperty(t,"__esModule",{value:!0}),t.getParsedType=t.ZodParsedType=t.objectUtil=t.util=void 0,(o=r||(t.util=r={})).assertEqual=e=>{},o.assertIs=function(e){},o.assertNever=function(e){throw Error()},o.arrayToEnum=e=>{let t={};for(let r of e)t[r]=r;return t},o.getValidEnumValues=e=>{let t=o.objectKeys(e).filter(t=>"number"!=typeof e[e[t]]),r={};for(let n of t)r[n]=e[n];return o.objectValues(r)},o.objectValues=e=>o.objectKeys(e).map(function(t){return e[t]}),o.objectKeys="function"==typeof Object.keys?e=>Object.keys(e):e=>{let t=[];for(let r in e)Object.prototype.hasOwnProperty.call(e,r)&&t.push(r);return t},o.find=(e,t)=>{for(let r of e)if(t(r))return r},o.isInteger="function"==typeof Number.isInteger?e=>Number.isInteger(e):e=>"number"==typeof e&&Number.isFinite(e)&&Math.floor(e)===e,o.joinValues=function(e,t=" | "){return e.map(e=>"string"==typeof e?`'${e}'`:e).join(t)},o.jsonStringifyReplacer=(e,t)=>"bigint"==typeof t?t.toString():t,(n||(t.objectUtil=n={})).mergeShapes=(e,t)=>({...e,...t}),t.ZodParsedType=r.arrayToEnum(["string","nan","number","integer","float","boolean","date","bigint","symbol","function","undefined","null","array","object","unknown","promise","void","never","map","set"]),t.getParsedType=e=>{switch(typeof e){case"undefined":return t.ZodParsedType.undefined;case"string":return t.ZodParsedType.string;case"number":return Number.isNaN(e)?t.ZodParsedType.nan:t.ZodParsedType.number;case"boolean":return t.ZodParsedType.boolean;case"function":return t.ZodParsedType.function;case"bigint":return t.ZodParsedType.bigint;case"symbol":return t.ZodParsedType.symbol;case"object":if(Array.isArray(e))return t.ZodParsedType.array;if(null===e)return t.ZodParsedType.null;if(e.then&&"function"==typeof e.then&&e.catch&&"function"==typeof e.catch)return t.ZodParsedType.promise;if("undefined"!=typeof Map&&e instanceof Map)return t.ZodParsedType.map;if("undefined"!=typeof Set&&e instanceof Set)return t.ZodParsedType.set;if("undefined"!=typeof Date&&e instanceof Date)return t.ZodParsedType.date;return t.ZodParsedType.object;default:return t.ZodParsedType.unknown}}},871:(e,t,r)=>{Object.defineProperty(t,"__esModule",{value:!0});let n=r(348),o=r(709);t.default=(e,t)=>{let r;switch(e.code){case n.ZodIssueCode.invalid_type:r=e.received===o.ZodParsedType.undefined?"Required":`Expected ${e.expected}, received ${e.received}`;break;case n.ZodIssueCode.invalid_literal:r=`Invalid literal value, expected ${JSON.stringify(e.expected,o.util.jsonStringifyReplacer)}`;break;case n.ZodIssueCode.unrecognized_keys:r=`Unrecognized key(s) in object: ${o.util.joinValues(e.keys,", ")}`;break;case n.ZodIssueCode.invalid_union:r="Invalid input";break;case n.ZodIssueCode.invalid_union_discriminator:r=`Invalid discriminator value. Expected ${o.util.joinValues(e.options)}`;break;case n.ZodIssueCode.invalid_enum_value:r=`Invalid enum value. Expected ${o.util.joinValues(e.options)}, received '${e.received}'`;break;case n.ZodIssueCode.invalid_arguments:r="Invalid function arguments";break;case n.ZodIssueCode.invalid_return_type:r="Invalid function return type";break;case n.ZodIssueCode.invalid_date:r="Invalid date";break;case n.ZodIssueCode.invalid_string:"object"==typeof e.validation?"includes"in e.validation?(r=`Invalid input: must include "${e.validation.includes}"`,"number"==typeof e.validation.position&&(r=`${r} at one or more positions greater than or equal to ${e.validation.position}`)):"startsWith"in e.validation?r=`Invalid input: must start with "${e.validation.startsWith}"`:"endsWith"in e.validation?r=`Invalid input: must end with "${e.validation.endsWith}"`:o.util.assertNever(e.validation):r="regex"!==e.validation?`Invalid ${e.validation}`:"Invalid";break;case n.ZodIssueCode.too_small:r="array"===e.type?`Array must contain ${e.exact?"exactly":e.inclusive?"at least":"more than"} ${e.minimum} element(s)`:"string"===e.type?`String must contain ${e.exact?"exactly":e.inclusive?"at least":"over"} ${e.minimum} character(s)`:"number"===e.type||"bigint"===e.type?`Number must be ${e.exact?"exactly equal to ":e.inclusive?"greater than or equal to ":"greater than "}${e.minimum}`:"date"===e.type?`Date must be ${e.exact?"exactly equal to ":e.inclusive?"greater than or equal to ":"greater than "}${new Date(Number(e.minimum))}`:"Invalid input";break;case n.ZodIssueCode.too_big:r="array"===e.type?`Array must contain ${e.exact?"exactly":e.inclusive?"at most":"less than"} ${e.maximum} element(s)`:"string"===e.type?`String must contain ${e.exact?"exactly":e.inclusive?"at most":"under"} ${e.maximum} character(s)`:"number"===e.type?`Number must be ${e.exact?"exactly":e.inclusive?"less than or equal to":"less than"} ${e.maximum}`:"bigint"===e.type?`BigInt must be ${e.exact?"exactly":e.inclusive?"less than or equal to":"less than"} ${e.maximum}`:"date"===e.type?`Date must be ${e.exact?"exactly":e.inclusive?"smaller than or equal to":"smaller than"} ${new Date(Number(e.maximum))}`:"Invalid input";break;case n.ZodIssueCode.custom:r="Invalid input";break;case n.ZodIssueCode.invalid_intersection_types:r="Intersection results could not be merged";break;case n.ZodIssueCode.not_multiple_of:r=`Number must be a multiple of ${e.multipleOf}`;break;case n.ZodIssueCode.not_finite:r="Number must be finite";break;default:r=t.defaultError,o.util.assertNever(e)}return{message:r}}},155:(e,t,r)=>{var n,o;let a;Object.defineProperty(t,"__esModule",{value:!0}),t.discriminatedUnion=t.date=t.boolean=t.bigint=t.array=t.any=t.coerce=t.ZodFirstPartyTypeKind=t.late=t.ZodSchema=t.Schema=t.ZodReadonly=t.ZodPipeline=t.ZodBranded=t.BRAND=t.ZodNaN=t.ZodCatch=t.ZodDefault=t.ZodNullable=t.ZodOptional=t.ZodTransformer=t.ZodEffects=t.ZodPromise=t.ZodNativeEnum=t.ZodEnum=t.ZodLiteral=t.ZodLazy=t.ZodFunction=t.ZodSet=t.ZodMap=t.ZodRecord=t.ZodTuple=t.ZodIntersection=t.ZodDiscriminatedUnion=t.ZodUnion=t.ZodObject=t.ZodArray=t.ZodVoid=t.ZodNever=t.ZodUnknown=t.ZodAny=t.ZodNull=t.ZodUndefined=t.ZodSymbol=t.ZodDate=t.ZodBoolean=t.ZodBigInt=t.ZodNumber=t.ZodString=t.ZodType=void 0,t.NEVER=t.void=t.unknown=t.union=t.undefined=t.tuple=t.transformer=t.symbol=t.string=t.strictObject=t.set=t.record=t.promise=t.preprocess=t.pipeline=t.ostring=t.optional=t.onumber=t.oboolean=t.object=t.number=t.nullable=t.null=t.never=t.nativeEnum=t.nan=t.map=t.literal=t.lazy=t.intersection=t.instanceof=t.function=t.enum=t.effect=void 0,t.datetimeRegex=P,t.custom=ey;let i=r(348),l=r(61),s=r(538),c=r(818),u=r(709);class d{constructor(e,t,r,n){this._cachedPath=[],this.parent=e,this.data=t,this._path=r,this._key=n}get path(){return this._cachedPath.length||(Array.isArray(this._key)?this._cachedPath.push(...this._path,...this._key):this._cachedPath.push(...this._path,this._key)),this._cachedPath}}let f=(e,t)=>{if((0,c.isValid)(t))return{success:!0,data:t.value};if(!e.common.issues.length)throw Error("Validation failed but no issues detected.");return{success:!1,get error(){if(this._error)return this._error;let t=new i.ZodError(e.common.issues);return this._error=t,this._error}}};function p(e){if(!e)return{};let{errorMap:t,invalid_type_error:r,required_error:n,description:o}=e;if(t&&(r||n))throw Error('Can\'t use "invalid_type_error" or "required_error" in conjunction with custom error map.');return t?{errorMap:t,description:o}:{errorMap:(t,o)=>{let{message:a}=e;return"invalid_enum_value"===t.code?{message:a??o.defaultError}:void 0===o.data?{message:a??n??o.defaultError}:"invalid_type"!==t.code?{message:o.defaultError}:{message:a??r??o.defaultError}},description:o}}class h{get description(){return this._def.description}_getType(e){return(0,u.getParsedType)(e.data)}_getOrReturnCtx(e,t){return t||{common:e.parent.common,data:e.data,parsedType:(0,u.getParsedType)(e.data),schemaErrorMap:this._def.errorMap,path:e.path,parent:e.parent}}_processInputParams(e){return{status:new c.ParseStatus,ctx:{common:e.parent.common,data:e.data,parsedType:(0,u.getParsedType)(e.data),schemaErrorMap:this._def.errorMap,path:e.path,parent:e.parent}}}_parseSync(e){let t=this._parse(e);if((0,c.isAsync)(t))throw Error("Synchronous parse encountered promise.");return t}_parseAsync(e){return Promise.resolve(this._parse(e))}parse(e,t){let r=this.safeParse(e,t);if(r.success)return r.data;throw r.error}safeParse(e,t){let r={common:{issues:[],async:t?.async??!1,contextualErrorMap:t?.errorMap},path:t?.path||[],schemaErrorMap:this._def.errorMap,parent:null,data:e,parsedType:(0,u.getParsedType)(e)},n=this._parseSync({data:e,path:r.path,parent:r});return f(r,n)}"~validate"(e){let t={common:{issues:[],async:!!this["~standard"].async},path:[],schemaErrorMap:this._def.errorMap,parent:null,data:e,parsedType:(0,u.getParsedType)(e)};if(!this["~standard"].async)try{let r=this._parseSync({data:e,path:[],parent:t});return(0,c.isValid)(r)?{value:r.value}:{issues:t.common.issues}}catch(e){e?.message?.toLowerCase()?.includes("encountered")&&(this["~standard"].async=!0),t.common={issues:[],async:!0}}return this._parseAsync({data:e,path:[],parent:t}).then(e=>(0,c.isValid)(e)?{value:e.value}:{issues:t.common.issues})}async parseAsync(e,t){let r=await this.safeParseAsync(e,t);if(r.success)return r.data;throw r.error}async safeParseAsync(e,t){let r={common:{issues:[],contextualErrorMap:t?.errorMap,async:!0},path:t?.path||[],schemaErrorMap:this._def.errorMap,parent:null,data:e,parsedType:(0,u.getParsedType)(e)},n=this._parse({data:e,path:r.path,parent:r});return f(r,await ((0,c.isAsync)(n)?n:Promise.resolve(n)))}refine(e,t){return this._refinement((r,n)=>{let o=e(r),a=()=>n.addIssue({code:i.ZodIssueCode.custom,..."string"==typeof t||void 0===t?{message:t}:"function"==typeof t?t(r):t});return"undefined"!=typeof Promise&&o instanceof Promise?o.then(e=>!!e||(a(),!1)):!!o||(a(),!1)})}refinement(e,t){return this._refinement((r,n)=>!!e(r)||(n.addIssue("function"==typeof t?t(r,n):t),!1))}_refinement(e){return new es({schema:this,typeName:n.ZodEffects,effect:{type:"refinement",refinement:e}})}superRefine(e){return this._refinement(e)}constructor(e){this.spa=this.safeParseAsync,this._def=e,this.parse=this.parse.bind(this),this.safeParse=this.safeParse.bind(this),this.parseAsync=this.parseAsync.bind(this),this.safeParseAsync=this.safeParseAsync.bind(this),this.spa=this.spa.bind(this),this.refine=this.refine.bind(this),this.refinement=this.refinement.bind(this),this.superRefine=this.superRefine.bind(this),this.optional=this.optional.bind(this),this.nullable=this.nullable.bind(this),this.nullish=this.nullish.bind(this),this.array=this.array.bind(this),this.promise=this.promise.bind(this),this.or=this.or.bind(this),this.and=this.and.bind(this),this.transform=this.transform.bind(this),this.brand=this.brand.bind(this),this.default=this.default.bind(this),this.catch=this.catch.bind(this),this.describe=this.describe.bind(this),this.pipe=this.pipe.bind(this),this.readonly=this.readonly.bind(this),this.isNullable=this.isNullable.bind(this),this.isOptional=this.isOptional.bind(this),this["~standard"]={version:1,vendor:"zod",validate:e=>this["~validate"](e)}}optional(){return ec.create(this,this._def)}nullable(){return eu.create(this,this._def)}nullish(){return this.nullable().optional()}array(){return B.create(this)}promise(){return el.create(this,this._def)}or(e){return W.create([this,e],this._def)}and(e){return X.create(this,e,this._def)}transform(e){return new es({...p(this._def),schema:this,typeName:n.ZodEffects,effect:{type:"transform",transform:e}})}default(e){return new ed({...p(this._def),innerType:this,defaultValue:"function"==typeof e?e:()=>e,typeName:n.ZodDefault})}brand(){return new eh({typeName:n.ZodBranded,type:this,...p(this._def)})}catch(e){return new ef({...p(this._def),innerType:this,catchValue:"function"==typeof e?e:()=>e,typeName:n.ZodCatch})}describe(e){return new this.constructor({...this._def,description:e})}pipe(e){return em.create(this,e)}readonly(){return eg.create(this)}isOptional(){return this.safeParse(void 0).success}isNullable(){return this.safeParse(null).success}}t.ZodType=h,t.Schema=h,t.ZodSchema=h;let m=/^c[^\s-]{8,}$/i,g=/^[0-9a-z]+$/,v=/^[0-9A-HJKMNP-TV-Z]{26}$/i,y=/^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$/i,b=/^[a-z0-9_-]{21}$/i,x=/^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]*$/,_=/^[-+]?P(?!$)(?:(?:[-+]?\d+Y)|(?:[-+]?\d+[.,]\d+Y$))?(?:(?:[-+]?\d+M)|(?:[-+]?\d+[.,]\d+M$))?(?:(?:[-+]?\d+W)|(?:[-+]?\d+[.,]\d+W$))?(?:(?:[-+]?\d+D)|(?:[-+]?\d+[.,]\d+D$))?(?:T(?=[\d+-])(?:(?:[-+]?\d+H)|(?:[-+]?\d+[.,]\d+H$))?(?:(?:[-+]?\d+M)|(?:[-+]?\d+[.,]\d+M$))?(?:[-+]?\d+(?:[.,]\d+)?S)?)??$/,w=/^(?!\.)(?!.*\.\.)([A-Z0-9_'+\-\.]*)[A-Z0-9_+-]@([A-Z0-9][A-Z0-9\-]*\.)+[A-Z]{2,}$/i,k=/^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$/,j=/^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\/(3[0-2]|[12]?[0-9])$/,S=/^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$/,C=/^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\/(12[0-8]|1[01][0-9]|[1-9]?[0-9])$/,E=/^([0-9a-zA-Z+/]{4})*(([0-9a-zA-Z+/]{2}==)|([0-9a-zA-Z+/]{3}=))?$/,T=/^([0-9a-zA-Z-_]{4})*(([0-9a-zA-Z-_]{2}(==)?)|([0-9a-zA-Z-_]{3}(=)?))?$/,N="((\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-((0[13578]|1[02])-(0[1-9]|[12]\\d|3[01])|(0[469]|11)-(0[1-9]|[12]\\d|30)|(02)-(0[1-9]|1\\d|2[0-8])))",L=RegExp(`^${N}$`);function I(e){let t="[0-5]\\d";e.precision?t=`${t}\\.\\d{${e.precision}}`:null==e.precision&&(t=`${t}(\\.\\d+)?`);let r=e.precision?"+":"?";return`([01]\\d|2[0-3]):[0-5]\\d(:${t})${r}`}function P(e){let t=`${N}T${I(e)}`,r=[];return r.push(e.local?"Z?":"Z"),e.offset&&r.push("([+-]\\d{2}:?\\d{2})"),t=`${t}(${r.join("|")})`,RegExp(`^${t}$`)}class z extends h{_parse(e){var t,r,n,o;let l;if(this._def.coerce&&(e.data=String(e.data)),this._getType(e)!==u.ZodParsedType.string){let t=this._getOrReturnCtx(e);return(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_type,expected:u.ZodParsedType.string,received:t.parsedType}),c.INVALID}let s=new c.ParseStatus;for(let d of this._def.checks)if("min"===d.kind)e.data.length<d.value&&(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{code:i.ZodIssueCode.too_small,minimum:d.value,type:"string",inclusive:!0,exact:!1,message:d.message}),s.dirty());else if("max"===d.kind)e.data.length>d.value&&(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{code:i.ZodIssueCode.too_big,maximum:d.value,type:"string",inclusive:!0,exact:!1,message:d.message}),s.dirty());else if("length"===d.kind){let t=e.data.length>d.value,r=e.data.length<d.value;(t||r)&&(l=this._getOrReturnCtx(e,l),t?(0,c.addIssueToContext)(l,{code:i.ZodIssueCode.too_big,maximum:d.value,type:"string",inclusive:!0,exact:!0,message:d.message}):r&&(0,c.addIssueToContext)(l,{code:i.ZodIssueCode.too_small,minimum:d.value,type:"string",inclusive:!0,exact:!0,message:d.message}),s.dirty())}else if("email"===d.kind)w.test(e.data)||(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{validation:"email",code:i.ZodIssueCode.invalid_string,message:d.message}),s.dirty());else if("emoji"===d.kind)a||(a=RegExp("^(\\p{Extended_Pictographic}|\\p{Emoji_Component})+$","u")),a.test(e.data)||(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{validation:"emoji",code:i.ZodIssueCode.invalid_string,message:d.message}),s.dirty());else if("uuid"===d.kind)y.test(e.data)||(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{validation:"uuid",code:i.ZodIssueCode.invalid_string,message:d.message}),s.dirty());else if("nanoid"===d.kind)b.test(e.data)||(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{validation:"nanoid",code:i.ZodIssueCode.invalid_string,message:d.message}),s.dirty());else if("cuid"===d.kind)m.test(e.data)||(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{validation:"cuid",code:i.ZodIssueCode.invalid_string,message:d.message}),s.dirty());else if("cuid2"===d.kind)g.test(e.data)||(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{validation:"cuid2",code:i.ZodIssueCode.invalid_string,message:d.message}),s.dirty());else if("ulid"===d.kind)v.test(e.data)||(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{validation:"ulid",code:i.ZodIssueCode.invalid_string,message:d.message}),s.dirty());else if("url"===d.kind)try{new URL(e.data)}catch{l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{validation:"url",code:i.ZodIssueCode.invalid_string,message:d.message}),s.dirty()}else"regex"===d.kind?(d.regex.lastIndex=0,d.regex.test(e.data)||(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{validation:"regex",code:i.ZodIssueCode.invalid_string,message:d.message}),s.dirty())):"trim"===d.kind?e.data=e.data.trim():"includes"===d.kind?e.data.includes(d.value,d.position)||(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{code:i.ZodIssueCode.invalid_string,validation:{includes:d.value,position:d.position},message:d.message}),s.dirty()):"toLowerCase"===d.kind?e.data=e.data.toLowerCase():"toUpperCase"===d.kind?e.data=e.data.toUpperCase():"startsWith"===d.kind?e.data.startsWith(d.value)||(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{code:i.ZodIssueCode.invalid_string,validation:{startsWith:d.value},message:d.message}),s.dirty()):"endsWith"===d.kind?e.data.endsWith(d.value)||(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{code:i.ZodIssueCode.invalid_string,validation:{endsWith:d.value},message:d.message}),s.dirty()):"datetime"===d.kind?P(d).test(e.data)||(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{code:i.ZodIssueCode.invalid_string,validation:"datetime",message:d.message}),s.dirty()):"date"===d.kind?L.test(e.data)||(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{code:i.ZodIssueCode.invalid_string,validation:"date",message:d.message}),s.dirty()):"time"===d.kind?RegExp(`^${I(d)}$`).test(e.data)||(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{code:i.ZodIssueCode.invalid_string,validation:"time",message:d.message}),s.dirty()):"duration"===d.kind?_.test(e.data)||(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{validation:"duration",code:i.ZodIssueCode.invalid_string,message:d.message}),s.dirty()):"ip"===d.kind?(t=e.data,!(("v4"===(r=d.version)||!r)&&k.test(t)||("v6"===r||!r)&&S.test(t))&&1&&(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{validation:"ip",code:i.ZodIssueCode.invalid_string,message:d.message}),s.dirty())):"jwt"===d.kind?!function(e,t){if(!x.test(e))return!1;try{let[r]=e.split(".");if(!r)return!1;let n=r.replace(/-/g,"+").replace(/_/g,"/").padEnd(r.length+(4-r.length%4)%4,"="),o=JSON.parse(atob(n));if("object"!=typeof o||null===o||"typ"in o&&o?.typ!=="JWT"||!o.alg||t&&o.alg!==t)return!1;return!0}catch{return!1}}(e.data,d.alg)&&(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{validation:"jwt",code:i.ZodIssueCode.invalid_string,message:d.message}),s.dirty()):"cidr"===d.kind?(n=e.data,!(("v4"===(o=d.version)||!o)&&j.test(n)||("v6"===o||!o)&&C.test(n))&&1&&(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{validation:"cidr",code:i.ZodIssueCode.invalid_string,message:d.message}),s.dirty())):"base64"===d.kind?E.test(e.data)||(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{validation:"base64",code:i.ZodIssueCode.invalid_string,message:d.message}),s.dirty()):"base64url"===d.kind?T.test(e.data)||(l=this._getOrReturnCtx(e,l),(0,c.addIssueToContext)(l,{validation:"base64url",code:i.ZodIssueCode.invalid_string,message:d.message}),s.dirty()):u.util.assertNever(d);return{status:s.value,value:e.data}}_regex(e,t,r){return this.refinement(t=>e.test(t),{validation:t,code:i.ZodIssueCode.invalid_string,...s.errorUtil.errToObj(r)})}_addCheck(e){return new z({...this._def,checks:[...this._def.checks,e]})}email(e){return this._addCheck({kind:"email",...s.errorUtil.errToObj(e)})}url(e){return this._addCheck({kind:"url",...s.errorUtil.errToObj(e)})}emoji(e){return this._addCheck({kind:"emoji",...s.errorUtil.errToObj(e)})}uuid(e){return this._addCheck({kind:"uuid",...s.errorUtil.errToObj(e)})}nanoid(e){return this._addCheck({kind:"nanoid",...s.errorUtil.errToObj(e)})}cuid(e){return this._addCheck({kind:"cuid",...s.errorUtil.errToObj(e)})}cuid2(e){return this._addCheck({kind:"cuid2",...s.errorUtil.errToObj(e)})}ulid(e){return this._addCheck({kind:"ulid",...s.errorUtil.errToObj(e)})}base64(e){return this._addCheck({kind:"base64",...s.errorUtil.errToObj(e)})}base64url(e){return this._addCheck({kind:"base64url",...s.errorUtil.errToObj(e)})}jwt(e){return this._addCheck({kind:"jwt",...s.errorUtil.errToObj(e)})}ip(e){return this._addCheck({kind:"ip",...s.errorUtil.errToObj(e)})}cidr(e){return this._addCheck({kind:"cidr",...s.errorUtil.errToObj(e)})}datetime(e){return"string"==typeof e?this._addCheck({kind:"datetime",precision:null,offset:!1,local:!1,message:e}):this._addCheck({kind:"datetime",precision:void 0===e?.precision?null:e?.precision,offset:e?.offset??!1,local:e?.local??!1,...s.errorUtil.errToObj(e?.message)})}date(e){return this._addCheck({kind:"date",message:e})}time(e){return"string"==typeof e?this._addCheck({kind:"time",precision:null,message:e}):this._addCheck({kind:"time",precision:void 0===e?.precision?null:e?.precision,...s.errorUtil.errToObj(e?.message)})}duration(e){return this._addCheck({kind:"duration",...s.errorUtil.errToObj(e)})}regex(e,t){return this._addCheck({kind:"regex",regex:e,...s.errorUtil.errToObj(t)})}includes(e,t){return this._addCheck({kind:"includes",value:e,position:t?.position,...s.errorUtil.errToObj(t?.message)})}startsWith(e,t){return this._addCheck({kind:"startsWith",value:e,...s.errorUtil.errToObj(t)})}endsWith(e,t){return this._addCheck({kind:"endsWith",value:e,...s.errorUtil.errToObj(t)})}min(e,t){return this._addCheck({kind:"min",value:e,...s.errorUtil.errToObj(t)})}max(e,t){return this._addCheck({kind:"max",value:e,...s.errorUtil.errToObj(t)})}length(e,t){return this._addCheck({kind:"length",value:e,...s.errorUtil.errToObj(t)})}nonempty(e){return this.min(1,s.errorUtil.errToObj(e))}trim(){return new z({...this._def,checks:[...this._def.checks,{kind:"trim"}]})}toLowerCase(){return new z({...this._def,checks:[...this._def.checks,{kind:"toLowerCase"}]})}toUpperCase(){return new z({...this._def,checks:[...this._def.checks,{kind:"toUpperCase"}]})}get isDatetime(){return!!this._def.checks.find(e=>"datetime"===e.kind)}get isDate(){return!!this._def.checks.find(e=>"date"===e.kind)}get isTime(){return!!this._def.checks.find(e=>"time"===e.kind)}get isDuration(){return!!this._def.checks.find(e=>"duration"===e.kind)}get isEmail(){return!!this._def.checks.find(e=>"email"===e.kind)}get isURL(){return!!this._def.checks.find(e=>"url"===e.kind)}get isEmoji(){return!!this._def.checks.find(e=>"emoji"===e.kind)}get isUUID(){return!!this._def.checks.find(e=>"uuid"===e.kind)}get isNANOID(){return!!this._def.checks.find(e=>"nanoid"===e.kind)}get isCUID(){return!!this._def.checks.find(e=>"cuid"===e.kind)}get isCUID2(){return!!this._def.checks.find(e=>"cuid2"===e.kind)}get isULID(){return!!this._def.checks.find(e=>"ulid"===e.kind)}get isIP(){return!!this._def.checks.find(e=>"ip"===e.kind)}get isCIDR(){return!!this._def.checks.find(e=>"cidr"===e.kind)}get isBase64(){return!!this._def.checks.find(e=>"base64"===e.kind)}get isBase64url(){return!!this._def.checks.find(e=>"base64url"===e.kind)}get minLength(){let e=null;for(let t of this._def.checks)"min"===t.kind&&(null===e||t.value>e)&&(e=t.value);return e}get maxLength(){let e=null;for(let t of this._def.checks)"max"===t.kind&&(null===e||t.value<e)&&(e=t.value);return e}}t.ZodString=z,z.create=e=>new z({checks:[],typeName:n.ZodString,coerce:e?.coerce??!1,...p(e)});class R extends h{constructor(){super(...arguments),this.min=this.gte,this.max=this.lte,this.step=this.multipleOf}_parse(e){let t;if(this._def.coerce&&(e.data=Number(e.data)),this._getType(e)!==u.ZodParsedType.number){let t=this._getOrReturnCtx(e);return(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_type,expected:u.ZodParsedType.number,received:t.parsedType}),c.INVALID}let r=new c.ParseStatus;for(let n of this._def.checks)"int"===n.kind?u.util.isInteger(e.data)||(t=this._getOrReturnCtx(e,t),(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_type,expected:"integer",received:"float",message:n.message}),r.dirty()):"min"===n.kind?(n.inclusive?e.data<n.value:e.data<=n.value)&&(t=this._getOrReturnCtx(e,t),(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.too_small,minimum:n.value,type:"number",inclusive:n.inclusive,exact:!1,message:n.message}),r.dirty()):"max"===n.kind?(n.inclusive?e.data>n.value:e.data>=n.value)&&(t=this._getOrReturnCtx(e,t),(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.too_big,maximum:n.value,type:"number",inclusive:n.inclusive,exact:!1,message:n.message}),r.dirty()):"multipleOf"===n.kind?0!==function(e,t){let r=(e.toString().split(".")[1]||"").length,n=(t.toString().split(".")[1]||"").length,o=r>n?r:n;return Number.parseInt(e.toFixed(o).replace(".",""))%Number.parseInt(t.toFixed(o).replace(".",""))/10**o}(e.data,n.value)&&(t=this._getOrReturnCtx(e,t),(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.not_multiple_of,multipleOf:n.value,message:n.message}),r.dirty()):"finite"===n.kind?Number.isFinite(e.data)||(t=this._getOrReturnCtx(e,t),(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.not_finite,message:n.message}),r.dirty()):u.util.assertNever(n);return{status:r.value,value:e.data}}gte(e,t){return this.setLimit("min",e,!0,s.errorUtil.toString(t))}gt(e,t){return this.setLimit("min",e,!1,s.errorUtil.toString(t))}lte(e,t){return this.setLimit("max",e,!0,s.errorUtil.toString(t))}lt(e,t){return this.setLimit("max",e,!1,s.errorUtil.toString(t))}setLimit(e,t,r,n){return new R({...this._def,checks:[...this._def.checks,{kind:e,value:t,inclusive:r,message:s.errorUtil.toString(n)}]})}_addCheck(e){return new R({...this._def,checks:[...this._def.checks,e]})}int(e){return this._addCheck({kind:"int",message:s.errorUtil.toString(e)})}positive(e){return this._addCheck({kind:"min",value:0,inclusive:!1,message:s.errorUtil.toString(e)})}negative(e){return this._addCheck({kind:"max",value:0,inclusive:!1,message:s.errorUtil.toString(e)})}nonpositive(e){return this._addCheck({kind:"max",value:0,inclusive:!0,message:s.errorUtil.toString(e)})}nonnegative(e){return this._addCheck({kind:"min",value:0,inclusive:!0,message:s.errorUtil.toString(e)})}multipleOf(e,t){return this._addCheck({kind:"multipleOf",value:e,message:s.errorUtil.toString(t)})}finite(e){return this._addCheck({kind:"finite",message:s.errorUtil.toString(e)})}safe(e){return this._addCheck({kind:"min",inclusive:!0,value:Number.MIN_SAFE_INTEGER,message:s.errorUtil.toString(e)})._addCheck({kind:"max",inclusive:!0,value:Number.MAX_SAFE_INTEGER,message:s.errorUtil.toString(e)})}get minValue(){let e=null;for(let t of this._def.checks)"min"===t.kind&&(null===e||t.value>e)&&(e=t.value);return e}get maxValue(){let e=null;for(let t of this._def.checks)"max"===t.kind&&(null===e||t.value<e)&&(e=t.value);return e}get isInt(){return!!this._def.checks.find(e=>"int"===e.kind||"multipleOf"===e.kind&&u.util.isInteger(e.value))}get isFinite(){let e=null,t=null;for(let r of this._def.checks)if("finite"===r.kind||"int"===r.kind||"multipleOf"===r.kind)return!0;else"min"===r.kind?(null===t||r.value>t)&&(t=r.value):"max"===r.kind&&(null===e||r.value<e)&&(e=r.value);return Number.isFinite(t)&&Number.isFinite(e)}}t.ZodNumber=R,R.create=e=>new R({checks:[],typeName:n.ZodNumber,coerce:e?.coerce||!1,...p(e)});class O extends h{constructor(){super(...arguments),this.min=this.gte,this.max=this.lte}_parse(e){let t;if(this._def.coerce)try{e.data=BigInt(e.data)}catch{return this._getInvalidInput(e)}if(this._getType(e)!==u.ZodParsedType.bigint)return this._getInvalidInput(e);let r=new c.ParseStatus;for(let n of this._def.checks)"min"===n.kind?(n.inclusive?e.data<n.value:e.data<=n.value)&&(t=this._getOrReturnCtx(e,t),(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.too_small,type:"bigint",minimum:n.value,inclusive:n.inclusive,message:n.message}),r.dirty()):"max"===n.kind?(n.inclusive?e.data>n.value:e.data>=n.value)&&(t=this._getOrReturnCtx(e,t),(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.too_big,type:"bigint",maximum:n.value,inclusive:n.inclusive,message:n.message}),r.dirty()):"multipleOf"===n.kind?e.data%n.value!==BigInt(0)&&(t=this._getOrReturnCtx(e,t),(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.not_multiple_of,multipleOf:n.value,message:n.message}),r.dirty()):u.util.assertNever(n);return{status:r.value,value:e.data}}_getInvalidInput(e){let t=this._getOrReturnCtx(e);return(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_type,expected:u.ZodParsedType.bigint,received:t.parsedType}),c.INVALID}gte(e,t){return this.setLimit("min",e,!0,s.errorUtil.toString(t))}gt(e,t){return this.setLimit("min",e,!1,s.errorUtil.toString(t))}lte(e,t){return this.setLimit("max",e,!0,s.errorUtil.toString(t))}lt(e,t){return this.setLimit("max",e,!1,s.errorUtil.toString(t))}setLimit(e,t,r,n){return new O({...this._def,checks:[...this._def.checks,{kind:e,value:t,inclusive:r,message:s.errorUtil.toString(n)}]})}_addCheck(e){return new O({...this._def,checks:[...this._def.checks,e]})}positive(e){return this._addCheck({kind:"min",value:BigInt(0),inclusive:!1,message:s.errorUtil.toString(e)})}negative(e){return this._addCheck({kind:"max",value:BigInt(0),inclusive:!1,message:s.errorUtil.toString(e)})}nonpositive(e){return this._addCheck({kind:"max",value:BigInt(0),inclusive:!0,message:s.errorUtil.toString(e)})}nonnegative(e){return this._addCheck({kind:"min",value:BigInt(0),inclusive:!0,message:s.errorUtil.toString(e)})}multipleOf(e,t){return this._addCheck({kind:"multipleOf",value:e,message:s.errorUtil.toString(t)})}get minValue(){let e=null;for(let t of this._def.checks)"min"===t.kind&&(null===e||t.value>e)&&(e=t.value);return e}get maxValue(){let e=null;for(let t of this._def.checks)"max"===t.kind&&(null===e||t.value<e)&&(e=t.value);return e}}t.ZodBigInt=O,O.create=e=>new O({checks:[],typeName:n.ZodBigInt,coerce:e?.coerce??!1,...p(e)});class M extends h{_parse(e){if(this._def.coerce&&(e.data=!!e.data),this._getType(e)!==u.ZodParsedType.boolean){let t=this._getOrReturnCtx(e);return(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_type,expected:u.ZodParsedType.boolean,received:t.parsedType}),c.INVALID}return(0,c.OK)(e.data)}}t.ZodBoolean=M,M.create=e=>new M({typeName:n.ZodBoolean,coerce:e?.coerce||!1,...p(e)});class A extends h{_parse(e){let t;if(this._def.coerce&&(e.data=new Date(e.data)),this._getType(e)!==u.ZodParsedType.date){let t=this._getOrReturnCtx(e);return(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_type,expected:u.ZodParsedType.date,received:t.parsedType}),c.INVALID}if(Number.isNaN(e.data.getTime())){let t=this._getOrReturnCtx(e);return(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_date}),c.INVALID}let r=new c.ParseStatus;for(let n of this._def.checks)"min"===n.kind?e.data.getTime()<n.value&&(t=this._getOrReturnCtx(e,t),(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.too_small,message:n.message,inclusive:!0,exact:!1,minimum:n.value,type:"date"}),r.dirty()):"max"===n.kind?e.data.getTime()>n.value&&(t=this._getOrReturnCtx(e,t),(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.too_big,message:n.message,inclusive:!0,exact:!1,maximum:n.value,type:"date"}),r.dirty()):u.util.assertNever(n);return{status:r.value,value:new Date(e.data.getTime())}}_addCheck(e){return new A({...this._def,checks:[...this._def.checks,e]})}min(e,t){return this._addCheck({kind:"min",value:e.getTime(),message:s.errorUtil.toString(t)})}max(e,t){return this._addCheck({kind:"max",value:e.getTime(),message:s.errorUtil.toString(t)})}get minDate(){let e=null;for(let t of this._def.checks)"min"===t.kind&&(null===e||t.value>e)&&(e=t.value);return null!=e?new Date(e):null}get maxDate(){let e=null;for(let t of this._def.checks)"max"===t.kind&&(null===e||t.value<e)&&(e=t.value);return null!=e?new Date(e):null}}t.ZodDate=A,A.create=e=>new A({checks:[],coerce:e?.coerce||!1,typeName:n.ZodDate,...p(e)});class D extends h{_parse(e){if(this._getType(e)!==u.ZodParsedType.symbol){let t=this._getOrReturnCtx(e);return(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_type,expected:u.ZodParsedType.symbol,received:t.parsedType}),c.INVALID}return(0,c.OK)(e.data)}}t.ZodSymbol=D,D.create=e=>new D({typeName:n.ZodSymbol,...p(e)});class Z extends h{_parse(e){if(this._getType(e)!==u.ZodParsedType.undefined){let t=this._getOrReturnCtx(e);return(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_type,expected:u.ZodParsedType.undefined,received:t.parsedType}),c.INVALID}return(0,c.OK)(e.data)}}t.ZodUndefined=Z,Z.create=e=>new Z({typeName:n.ZodUndefined,...p(e)});class F extends h{_parse(e){if(this._getType(e)!==u.ZodParsedType.null){let t=this._getOrReturnCtx(e);return(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_type,expected:u.ZodParsedType.null,received:t.parsedType}),c.INVALID}return(0,c.OK)(e.data)}}t.ZodNull=F,F.create=e=>new F({typeName:n.ZodNull,...p(e)});class U extends h{constructor(){super(...arguments),this._any=!0}_parse(e){return(0,c.OK)(e.data)}}t.ZodAny=U,U.create=e=>new U({typeName:n.ZodAny,...p(e)});class $ extends h{constructor(){super(...arguments),this._unknown=!0}_parse(e){return(0,c.OK)(e.data)}}t.ZodUnknown=$,$.create=e=>new $({typeName:n.ZodUnknown,...p(e)});class H extends h{_parse(e){let t=this._getOrReturnCtx(e);return(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_type,expected:u.ZodParsedType.never,received:t.parsedType}),c.INVALID}}t.ZodNever=H,H.create=e=>new H({typeName:n.ZodNever,...p(e)});class V extends h{_parse(e){if(this._getType(e)!==u.ZodParsedType.undefined){let t=this._getOrReturnCtx(e);return(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_type,expected:u.ZodParsedType.void,received:t.parsedType}),c.INVALID}return(0,c.OK)(e.data)}}t.ZodVoid=V,V.create=e=>new V({typeName:n.ZodVoid,...p(e)});class B extends h{_parse(e){let{ctx:t,status:r}=this._processInputParams(e),n=this._def;if(t.parsedType!==u.ZodParsedType.array)return(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_type,expected:u.ZodParsedType.array,received:t.parsedType}),c.INVALID;if(null!==n.exactLength){let e=t.data.length>n.exactLength.value,o=t.data.length<n.exactLength.value;(e||o)&&((0,c.addIssueToContext)(t,{code:e?i.ZodIssueCode.too_big:i.ZodIssueCode.too_small,minimum:o?n.exactLength.value:void 0,maximum:e?n.exactLength.value:void 0,type:"array",inclusive:!0,exact:!0,message:n.exactLength.message}),r.dirty())}if(null!==n.minLength&&t.data.length<n.minLength.value&&((0,c.addIssueToContext)(t,{code:i.ZodIssueCode.too_small,minimum:n.minLength.value,type:"array",inclusive:!0,exact:!1,message:n.minLength.message}),r.dirty()),null!==n.maxLength&&t.data.length>n.maxLength.value&&((0,c.addIssueToContext)(t,{code:i.ZodIssueCode.too_big,maximum:n.maxLength.value,type:"array",inclusive:!0,exact:!1,message:n.maxLength.message}),r.dirty()),t.common.async)return Promise.all([...t.data].map((e,r)=>n.type._parseAsync(new d(t,e,t.path,r)))).then(e=>c.ParseStatus.mergeArray(r,e));let o=[...t.data].map((e,r)=>n.type._parseSync(new d(t,e,t.path,r)));return c.ParseStatus.mergeArray(r,o)}get element(){return this._def.type}min(e,t){return new B({...this._def,minLength:{value:e,message:s.errorUtil.toString(t)}})}max(e,t){return new B({...this._def,maxLength:{value:e,message:s.errorUtil.toString(t)}})}length(e,t){return new B({...this._def,exactLength:{value:e,message:s.errorUtil.toString(t)}})}nonempty(e){return this.min(1,e)}}t.ZodArray=B,B.create=(e,t)=>new B({type:e,minLength:null,maxLength:null,exactLength:null,typeName:n.ZodArray,...p(t)});class q extends h{constructor(){super(...arguments),this._cached=null,this.nonstrict=this.passthrough,this.augment=this.extend}_getCached(){if(null!==this._cached)return this._cached;let e=this._def.shape(),t=u.util.objectKeys(e);return this._cached={shape:e,keys:t},this._cached}_parse(e){if(this._getType(e)!==u.ZodParsedType.object){let t=this._getOrReturnCtx(e);return(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_type,expected:u.ZodParsedType.object,received:t.parsedType}),c.INVALID}let{status:t,ctx:r}=this._processInputParams(e),{shape:n,keys:o}=this._getCached(),a=[];if(!(this._def.catchall instanceof H&&"strip"===this._def.unknownKeys))for(let e in r.data)o.includes(e)||a.push(e);let l=[];for(let e of o){let t=n[e],o=r.data[e];l.push({key:{status:"valid",value:e},value:t._parse(new d(r,o,r.path,e)),alwaysSet:e in r.data})}if(this._def.catchall instanceof H){let e=this._def.unknownKeys;if("passthrough"===e)for(let e of a)l.push({key:{status:"valid",value:e},value:{status:"valid",value:r.data[e]}});else if("strict"===e)a.length>0&&((0,c.addIssueToContext)(r,{code:i.ZodIssueCode.unrecognized_keys,keys:a}),t.dirty());else if("strip"===e);else throw Error("Internal ZodObject error: invalid unknownKeys value.")}else{let e=this._def.catchall;for(let t of a){let n=r.data[t];l.push({key:{status:"valid",value:t},value:e._parse(new d(r,n,r.path,t)),alwaysSet:t in r.data})}}return r.common.async?Promise.resolve().then(async()=>{let e=[];for(let t of l){let r=await t.key,n=await t.value;e.push({key:r,value:n,alwaysSet:t.alwaysSet})}return e}).then(e=>c.ParseStatus.mergeObjectSync(t,e)):c.ParseStatus.mergeObjectSync(t,l)}get shape(){return this._def.shape()}strict(e){return s.errorUtil.errToObj,new q({...this._def,unknownKeys:"strict",...void 0!==e?{errorMap:(t,r)=>{let n=this._def.errorMap?.(t,r).message??r.defaultError;return"unrecognized_keys"===t.code?{message:s.errorUtil.errToObj(e).message??n}:{message:n}}}:{}})}strip(){return new q({...this._def,unknownKeys:"strip"})}passthrough(){return new q({...this._def,unknownKeys:"passthrough"})}extend(e){return new q({...this._def,shape:()=>({...this._def.shape(),...e})})}merge(e){return new q({unknownKeys:e._def.unknownKeys,catchall:e._def.catchall,shape:()=>({...this._def.shape(),...e._def.shape()}),typeName:n.ZodObject})}setKey(e,t){return this.augment({[e]:t})}catchall(e){return new q({...this._def,catchall:e})}pick(e){let t={};for(let r of u.util.objectKeys(e))e[r]&&this.shape[r]&&(t[r]=this.shape[r]);return new q({...this._def,shape:()=>t})}omit(e){let t={};for(let r of u.util.objectKeys(this.shape))e[r]||(t[r]=this.shape[r]);return new q({...this._def,shape:()=>t})}deepPartial(){return function e(t){if(t instanceof q){let r={};for(let n in t.shape){let o=t.shape[n];r[n]=ec.create(e(o))}return new q({...t._def,shape:()=>r})}if(t instanceof B)return new B({...t._def,type:e(t.element)});if(t instanceof ec)return ec.create(e(t.unwrap()));if(t instanceof eu)return eu.create(e(t.unwrap()));if(t instanceof G)return G.create(t.items.map(t=>e(t)));else return t}(this)}partial(e){let t={};for(let r of u.util.objectKeys(this.shape)){let n=this.shape[r];e&&!e[r]?t[r]=n:t[r]=n.optional()}return new q({...this._def,shape:()=>t})}required(e){let t={};for(let r of u.util.objectKeys(this.shape))if(e&&!e[r])t[r]=this.shape[r];else{let e=this.shape[r];for(;e instanceof ec;)e=e._def.innerType;t[r]=e}return new q({...this._def,shape:()=>t})}keyof(){return eo(u.util.objectKeys(this.shape))}}t.ZodObject=q,q.create=(e,t)=>new q({shape:()=>e,unknownKeys:"strip",catchall:H.create(),typeName:n.ZodObject,...p(t)}),q.strictCreate=(e,t)=>new q({shape:()=>e,unknownKeys:"strict",catchall:H.create(),typeName:n.ZodObject,...p(t)}),q.lazycreate=(e,t)=>new q({shape:e,unknownKeys:"strip",catchall:H.create(),typeName:n.ZodObject,...p(t)});class W extends h{_parse(e){let{ctx:t}=this._processInputParams(e),r=this._def.options;if(t.common.async)return Promise.all(r.map(async e=>{let r={...t,common:{...t.common,issues:[]},parent:null};return{result:await e._parseAsync({data:t.data,path:t.path,parent:r}),ctx:r}})).then(function(e){for(let t of e)if("valid"===t.result.status)return t.result;for(let r of e)if("dirty"===r.result.status)return t.common.issues.push(...r.ctx.common.issues),r.result;let r=e.map(e=>new i.ZodError(e.ctx.common.issues));return(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_union,unionErrors:r}),c.INVALID});{let e,n=[];for(let o of r){let r={...t,common:{...t.common,issues:[]},parent:null},a=o._parseSync({data:t.data,path:t.path,parent:r});if("valid"===a.status)return a;"dirty"!==a.status||e||(e={result:a,ctx:r}),r.common.issues.length&&n.push(r.common.issues)}if(e)return t.common.issues.push(...e.ctx.common.issues),e.result;let o=n.map(e=>new i.ZodError(e));return(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_union,unionErrors:o}),c.INVALID}}get options(){return this._def.options}}t.ZodUnion=W,W.create=(e,t)=>new W({options:e,typeName:n.ZodUnion,...p(t)});let K=e=>{if(e instanceof er)return K(e.schema);if(e instanceof es)return K(e.innerType());if(e instanceof en)return[e.value];if(e instanceof ea)return e.options;if(e instanceof ei)return u.util.objectValues(e.enum);else if(e instanceof ed)return K(e._def.innerType);else if(e instanceof Z)return[void 0];else if(e instanceof F)return[null];else if(e instanceof ec)return[void 0,...K(e.unwrap())];else if(e instanceof eu)return[null,...K(e.unwrap())];else if(e instanceof eh)return K(e.unwrap());else if(e instanceof eg)return K(e.unwrap());else if(e instanceof ef)return K(e._def.innerType);else return[]};class Y extends h{_parse(e){let{ctx:t}=this._processInputParams(e);if(t.parsedType!==u.ZodParsedType.object)return(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_type,expected:u.ZodParsedType.object,received:t.parsedType}),c.INVALID;let r=this.discriminator,n=t.data[r],o=this.optionsMap.get(n);return o?t.common.async?o._parseAsync({data:t.data,path:t.path,parent:t}):o._parseSync({data:t.data,path:t.path,parent:t}):((0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_union_discriminator,options:Array.from(this.optionsMap.keys()),path:[r]}),c.INVALID)}get discriminator(){return this._def.discriminator}get options(){return this._def.options}get optionsMap(){return this._def.optionsMap}static create(e,t,r){let o=new Map;for(let r of t){let t=K(r.shape[e]);if(!t.length)throw Error(`A discriminator value for key \`${e}\` could not be extracted from all schema options`);for(let n of t){if(o.has(n))throw Error(`Discriminator property ${String(e)} has duplicate value ${String(n)}`);o.set(n,r)}}return new Y({typeName:n.ZodDiscriminatedUnion,discriminator:e,options:t,optionsMap:o,...p(r)})}}t.ZodDiscriminatedUnion=Y;class X extends h{_parse(e){let{status:t,ctx:r}=this._processInputParams(e),n=(e,n)=>{if((0,c.isAborted)(e)||(0,c.isAborted)(n))return c.INVALID;let o=function e(t,r){let n=(0,u.getParsedType)(t),o=(0,u.getParsedType)(r);if(t===r)return{valid:!0,data:t};if(n===u.ZodParsedType.object&&o===u.ZodParsedType.object){let n=u.util.objectKeys(r),o=u.util.objectKeys(t).filter(e=>-1!==n.indexOf(e)),a={...t,...r};for(let n of o){let o=e(t[n],r[n]);if(!o.valid)return{valid:!1};a[n]=o.data}return{valid:!0,data:a}}if(n===u.ZodParsedType.array&&o===u.ZodParsedType.array){if(t.length!==r.length)return{valid:!1};let n=[];for(let o=0;o<t.length;o++){let a=e(t[o],r[o]);if(!a.valid)return{valid:!1};n.push(a.data)}return{valid:!0,data:n}}if(n===u.ZodParsedType.date&&o===u.ZodParsedType.date&&+t==+r)return{valid:!0,data:t};return{valid:!1}}(e.value,n.value);return o.valid?(((0,c.isDirty)(e)||(0,c.isDirty)(n))&&t.dirty(),{status:t.value,value:o.data}):((0,c.addIssueToContext)(r,{code:i.ZodIssueCode.invalid_intersection_types}),c.INVALID)};return r.common.async?Promise.all([this._def.left._parseAsync({data:r.data,path:r.path,parent:r}),this._def.right._parseAsync({data:r.data,path:r.path,parent:r})]).then(([e,t])=>n(e,t)):n(this._def.left._parseSync({data:r.data,path:r.path,parent:r}),this._def.right._parseSync({data:r.data,path:r.path,parent:r}))}}t.ZodIntersection=X,X.create=(e,t,r)=>new X({left:e,right:t,typeName:n.ZodIntersection,...p(r)});class G extends h{_parse(e){let{status:t,ctx:r}=this._processInputParams(e);if(r.parsedType!==u.ZodParsedType.array)return(0,c.addIssueToContext)(r,{code:i.ZodIssueCode.invalid_type,expected:u.ZodParsedType.array,received:r.parsedType}),c.INVALID;if(r.data.length<this._def.items.length)return(0,c.addIssueToContext)(r,{code:i.ZodIssueCode.too_small,minimum:this._def.items.length,inclusive:!0,exact:!1,type:"array"}),c.INVALID;!this._def.rest&&r.data.length>this._def.items.length&&((0,c.addIssueToContext)(r,{code:i.ZodIssueCode.too_big,maximum:this._def.items.length,inclusive:!0,exact:!1,type:"array"}),t.dirty());let n=[...r.data].map((e,t)=>{let n=this._def.items[t]||this._def.rest;return n?n._parse(new d(r,e,r.path,t)):null}).filter(e=>!!e);return r.common.async?Promise.all(n).then(e=>c.ParseStatus.mergeArray(t,e)):c.ParseStatus.mergeArray(t,n)}get items(){return this._def.items}rest(e){return new G({...this._def,rest:e})}}t.ZodTuple=G,G.create=(e,t)=>{if(!Array.isArray(e))throw Error("You must pass an array of schemas to z.tuple([ ... ])");return new G({items:e,typeName:n.ZodTuple,rest:null,...p(t)})};class Q extends h{get keySchema(){return this._def.keyType}get valueSchema(){return this._def.valueType}_parse(e){let{status:t,ctx:r}=this._processInputParams(e);if(r.parsedType!==u.ZodParsedType.object)return(0,c.addIssueToContext)(r,{code:i.ZodIssueCode.invalid_type,expected:u.ZodParsedType.object,received:r.parsedType}),c.INVALID;let n=[],o=this._def.keyType,a=this._def.valueType;for(let e in r.data)n.push({key:o._parse(new d(r,e,r.path,e)),value:a._parse(new d(r,r.data[e],r.path,e)),alwaysSet:e in r.data});return r.common.async?c.ParseStatus.mergeObjectAsync(t,n):c.ParseStatus.mergeObjectSync(t,n)}get element(){return this._def.valueType}static create(e,t,r){return new Q(t instanceof h?{keyType:e,valueType:t,typeName:n.ZodRecord,...p(r)}:{keyType:z.create(),valueType:e,typeName:n.ZodRecord,...p(t)})}}t.ZodRecord=Q;class J extends h{get keySchema(){return this._def.keyType}get valueSchema(){return this._def.valueType}_parse(e){let{status:t,ctx:r}=this._processInputParams(e);if(r.parsedType!==u.ZodParsedType.map)return(0,c.addIssueToContext)(r,{code:i.ZodIssueCode.invalid_type,expected:u.ZodParsedType.map,received:r.parsedType}),c.INVALID;let n=this._def.keyType,o=this._def.valueType,a=[...r.data.entries()].map(([e,t],a)=>({key:n._parse(new d(r,e,r.path,[a,"key"])),value:o._parse(new d(r,t,r.path,[a,"value"]))}));if(r.common.async){let e=new Map;return Promise.resolve().then(async()=>{for(let r of a){let n=await r.key,o=await r.value;if("aborted"===n.status||"aborted"===o.status)return c.INVALID;("dirty"===n.status||"dirty"===o.status)&&t.dirty(),e.set(n.value,o.value)}return{status:t.value,value:e}})}{let e=new Map;for(let r of a){let n=r.key,o=r.value;if("aborted"===n.status||"aborted"===o.status)return c.INVALID;("dirty"===n.status||"dirty"===o.status)&&t.dirty(),e.set(n.value,o.value)}return{status:t.value,value:e}}}}t.ZodMap=J,J.create=(e,t,r)=>new J({valueType:t,keyType:e,typeName:n.ZodMap,...p(r)});class ee extends h{_parse(e){let{status:t,ctx:r}=this._processInputParams(e);if(r.parsedType!==u.ZodParsedType.set)return(0,c.addIssueToContext)(r,{code:i.ZodIssueCode.invalid_type,expected:u.ZodParsedType.set,received:r.parsedType}),c.INVALID;let n=this._def;null!==n.minSize&&r.data.size<n.minSize.value&&((0,c.addIssueToContext)(r,{code:i.ZodIssueCode.too_small,minimum:n.minSize.value,type:"set",inclusive:!0,exact:!1,message:n.minSize.message}),t.dirty()),null!==n.maxSize&&r.data.size>n.maxSize.value&&((0,c.addIssueToContext)(r,{code:i.ZodIssueCode.too_big,maximum:n.maxSize.value,type:"set",inclusive:!0,exact:!1,message:n.maxSize.message}),t.dirty());let o=this._def.valueType;function a(e){let r=new Set;for(let n of e){if("aborted"===n.status)return c.INVALID;"dirty"===n.status&&t.dirty(),r.add(n.value)}return{status:t.value,value:r}}let l=[...r.data.values()].map((e,t)=>o._parse(new d(r,e,r.path,t)));return r.common.async?Promise.all(l).then(e=>a(e)):a(l)}min(e,t){return new ee({...this._def,minSize:{value:e,message:s.errorUtil.toString(t)}})}max(e,t){return new ee({...this._def,maxSize:{value:e,message:s.errorUtil.toString(t)}})}size(e,t){return this.min(e,t).max(e,t)}nonempty(e){return this.min(1,e)}}t.ZodSet=ee,ee.create=(e,t)=>new ee({valueType:e,minSize:null,maxSize:null,typeName:n.ZodSet,...p(t)});class et extends h{constructor(){super(...arguments),this.validate=this.implement}_parse(e){let{ctx:t}=this._processInputParams(e);if(t.parsedType!==u.ZodParsedType.function)return(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_type,expected:u.ZodParsedType.function,received:t.parsedType}),c.INVALID;function r(e,r){return(0,c.makeIssue)({data:e,path:t.path,errorMaps:[t.common.contextualErrorMap,t.schemaErrorMap,(0,l.getErrorMap)(),l.defaultErrorMap].filter(e=>!!e),issueData:{code:i.ZodIssueCode.invalid_arguments,argumentsError:r}})}function n(e,r){return(0,c.makeIssue)({data:e,path:t.path,errorMaps:[t.common.contextualErrorMap,t.schemaErrorMap,(0,l.getErrorMap)(),l.defaultErrorMap].filter(e=>!!e),issueData:{code:i.ZodIssueCode.invalid_return_type,returnTypeError:r}})}let o={errorMap:t.common.contextualErrorMap},a=t.data;if(this._def.returns instanceof el){let e=this;return(0,c.OK)(async function(...t){let l=new i.ZodError([]),s=await e._def.args.parseAsync(t,o).catch(e=>{throw l.addIssue(r(t,e)),l}),c=await Reflect.apply(a,this,s);return await e._def.returns._def.type.parseAsync(c,o).catch(e=>{throw l.addIssue(n(c,e)),l})})}{let e=this;return(0,c.OK)(function(...t){let l=e._def.args.safeParse(t,o);if(!l.success)throw new i.ZodError([r(t,l.error)]);let s=Reflect.apply(a,this,l.data),c=e._def.returns.safeParse(s,o);if(!c.success)throw new i.ZodError([n(s,c.error)]);return c.data})}}parameters(){return this._def.args}returnType(){return this._def.returns}args(...e){return new et({...this._def,args:G.create(e).rest($.create())})}returns(e){return new et({...this._def,returns:e})}implement(e){return this.parse(e)}strictImplement(e){return this.parse(e)}static create(e,t,r){return new et({args:e||G.create([]).rest($.create()),returns:t||$.create(),typeName:n.ZodFunction,...p(r)})}}t.ZodFunction=et;class er extends h{get schema(){return this._def.getter()}_parse(e){let{ctx:t}=this._processInputParams(e);return this._def.getter()._parse({data:t.data,path:t.path,parent:t})}}t.ZodLazy=er,er.create=(e,t)=>new er({getter:e,typeName:n.ZodLazy,...p(t)});class en extends h{_parse(e){if(e.data!==this._def.value){let t=this._getOrReturnCtx(e);return(0,c.addIssueToContext)(t,{received:t.data,code:i.ZodIssueCode.invalid_literal,expected:this._def.value}),c.INVALID}return{status:"valid",value:e.data}}get value(){return this._def.value}}function eo(e,t){return new ea({values:e,typeName:n.ZodEnum,...p(t)})}t.ZodLiteral=en,en.create=(e,t)=>new en({value:e,typeName:n.ZodLiteral,...p(t)});class ea extends h{_parse(e){if("string"!=typeof e.data){let t=this._getOrReturnCtx(e),r=this._def.values;return(0,c.addIssueToContext)(t,{expected:u.util.joinValues(r),received:t.parsedType,code:i.ZodIssueCode.invalid_type}),c.INVALID}if(this._cache||(this._cache=new Set(this._def.values)),!this._cache.has(e.data)){let t=this._getOrReturnCtx(e),r=this._def.values;return(0,c.addIssueToContext)(t,{received:t.data,code:i.ZodIssueCode.invalid_enum_value,options:r}),c.INVALID}return(0,c.OK)(e.data)}get options(){return this._def.values}get enum(){let e={};for(let t of this._def.values)e[t]=t;return e}get Values(){let e={};for(let t of this._def.values)e[t]=t;return e}get Enum(){let e={};for(let t of this._def.values)e[t]=t;return e}extract(e,t=this._def){return ea.create(e,{...this._def,...t})}exclude(e,t=this._def){return ea.create(this.options.filter(t=>!e.includes(t)),{...this._def,...t})}}t.ZodEnum=ea,ea.create=eo;class ei extends h{_parse(e){let t=u.util.getValidEnumValues(this._def.values),r=this._getOrReturnCtx(e);if(r.parsedType!==u.ZodParsedType.string&&r.parsedType!==u.ZodParsedType.number){let e=u.util.objectValues(t);return(0,c.addIssueToContext)(r,{expected:u.util.joinValues(e),received:r.parsedType,code:i.ZodIssueCode.invalid_type}),c.INVALID}if(this._cache||(this._cache=new Set(u.util.getValidEnumValues(this._def.values))),!this._cache.has(e.data)){let e=u.util.objectValues(t);return(0,c.addIssueToContext)(r,{received:r.data,code:i.ZodIssueCode.invalid_enum_value,options:e}),c.INVALID}return(0,c.OK)(e.data)}get enum(){return this._def.values}}t.ZodNativeEnum=ei,ei.create=(e,t)=>new ei({values:e,typeName:n.ZodNativeEnum,...p(t)});class el extends h{unwrap(){return this._def.type}_parse(e){let{ctx:t}=this._processInputParams(e);if(t.parsedType!==u.ZodParsedType.promise&&!1===t.common.async)return(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_type,expected:u.ZodParsedType.promise,received:t.parsedType}),c.INVALID;let r=t.parsedType===u.ZodParsedType.promise?t.data:Promise.resolve(t.data);return(0,c.OK)(r.then(e=>this._def.type.parseAsync(e,{path:t.path,errorMap:t.common.contextualErrorMap})))}}t.ZodPromise=el,el.create=(e,t)=>new el({type:e,typeName:n.ZodPromise,...p(t)});class es extends h{innerType(){return this._def.schema}sourceType(){return this._def.schema._def.typeName===n.ZodEffects?this._def.schema.sourceType():this._def.schema}_parse(e){let{status:t,ctx:r}=this._processInputParams(e),n=this._def.effect||null,o={addIssue:e=>{(0,c.addIssueToContext)(r,e),e.fatal?t.abort():t.dirty()},get path(){return r.path}};if(o.addIssue=o.addIssue.bind(o),"preprocess"===n.type){let e=n.transform(r.data,o);if(r.common.async)return Promise.resolve(e).then(async e=>{if("aborted"===t.value)return c.INVALID;let n=await this._def.schema._parseAsync({data:e,path:r.path,parent:r});return"aborted"===n.status?c.INVALID:"dirty"===n.status||"dirty"===t.value?(0,c.DIRTY)(n.value):n});{if("aborted"===t.value)return c.INVALID;let n=this._def.schema._parseSync({data:e,path:r.path,parent:r});return"aborted"===n.status?c.INVALID:"dirty"===n.status||"dirty"===t.value?(0,c.DIRTY)(n.value):n}}if("refinement"===n.type){let e=e=>{let t=n.refinement(e,o);if(r.common.async)return Promise.resolve(t);if(t instanceof Promise)throw Error("Async refinement encountered during synchronous parse operation. Use .parseAsync instead.");return e};if(!1!==r.common.async)return this._def.schema._parseAsync({data:r.data,path:r.path,parent:r}).then(r=>"aborted"===r.status?c.INVALID:("dirty"===r.status&&t.dirty(),e(r.value).then(()=>({status:t.value,value:r.value}))));{let n=this._def.schema._parseSync({data:r.data,path:r.path,parent:r});return"aborted"===n.status?c.INVALID:("dirty"===n.status&&t.dirty(),e(n.value),{status:t.value,value:n.value})}}if("transform"===n.type)if(!1!==r.common.async)return this._def.schema._parseAsync({data:r.data,path:r.path,parent:r}).then(e=>(0,c.isValid)(e)?Promise.resolve(n.transform(e.value,o)).then(e=>({status:t.value,value:e})):c.INVALID);else{let e=this._def.schema._parseSync({data:r.data,path:r.path,parent:r});if(!(0,c.isValid)(e))return c.INVALID;let a=n.transform(e.value,o);if(a instanceof Promise)throw Error("Asynchronous transform encountered during synchronous parse operation. Use .parseAsync instead.");return{status:t.value,value:a}}u.util.assertNever(n)}}t.ZodEffects=es,t.ZodTransformer=es,es.create=(e,t,r)=>new es({schema:e,typeName:n.ZodEffects,effect:t,...p(r)}),es.createWithPreprocess=(e,t,r)=>new es({schema:t,effect:{type:"preprocess",transform:e},typeName:n.ZodEffects,...p(r)});class ec extends h{_parse(e){return this._getType(e)===u.ZodParsedType.undefined?(0,c.OK)(void 0):this._def.innerType._parse(e)}unwrap(){return this._def.innerType}}t.ZodOptional=ec,ec.create=(e,t)=>new ec({innerType:e,typeName:n.ZodOptional,...p(t)});class eu extends h{_parse(e){return this._getType(e)===u.ZodParsedType.null?(0,c.OK)(null):this._def.innerType._parse(e)}unwrap(){return this._def.innerType}}t.ZodNullable=eu,eu.create=(e,t)=>new eu({innerType:e,typeName:n.ZodNullable,...p(t)});class ed extends h{_parse(e){let{ctx:t}=this._processInputParams(e),r=t.data;return t.parsedType===u.ZodParsedType.undefined&&(r=this._def.defaultValue()),this._def.innerType._parse({data:r,path:t.path,parent:t})}removeDefault(){return this._def.innerType}}t.ZodDefault=ed,ed.create=(e,t)=>new ed({innerType:e,typeName:n.ZodDefault,defaultValue:"function"==typeof t.default?t.default:()=>t.default,...p(t)});class ef extends h{_parse(e){let{ctx:t}=this._processInputParams(e),r={...t,common:{...t.common,issues:[]}},n=this._def.innerType._parse({data:r.data,path:r.path,parent:{...r}});return(0,c.isAsync)(n)?n.then(e=>({status:"valid",value:"valid"===e.status?e.value:this._def.catchValue({get error(){return new i.ZodError(r.common.issues)},input:r.data})})):{status:"valid",value:"valid"===n.status?n.value:this._def.catchValue({get error(){return new i.ZodError(r.common.issues)},input:r.data})}}removeCatch(){return this._def.innerType}}t.ZodCatch=ef,ef.create=(e,t)=>new ef({innerType:e,typeName:n.ZodCatch,catchValue:"function"==typeof t.catch?t.catch:()=>t.catch,...p(t)});class ep extends h{_parse(e){if(this._getType(e)!==u.ZodParsedType.nan){let t=this._getOrReturnCtx(e);return(0,c.addIssueToContext)(t,{code:i.ZodIssueCode.invalid_type,expected:u.ZodParsedType.nan,received:t.parsedType}),c.INVALID}return{status:"valid",value:e.data}}}t.ZodNaN=ep,ep.create=e=>new ep({typeName:n.ZodNaN,...p(e)}),t.BRAND=Symbol("zod_brand");class eh extends h{_parse(e){let{ctx:t}=this._processInputParams(e),r=t.data;return this._def.type._parse({data:r,path:t.path,parent:t})}unwrap(){return this._def.type}}t.ZodBranded=eh;class em extends h{_parse(e){let{status:t,ctx:r}=this._processInputParams(e);if(r.common.async)return(async()=>{let e=await this._def.in._parseAsync({data:r.data,path:r.path,parent:r});return"aborted"===e.status?c.INVALID:"dirty"===e.status?(t.dirty(),(0,c.DIRTY)(e.value)):this._def.out._parseAsync({data:e.value,path:r.path,parent:r})})();{let e=this._def.in._parseSync({data:r.data,path:r.path,parent:r});return"aborted"===e.status?c.INVALID:"dirty"===e.status?(t.dirty(),{status:"dirty",value:e.value}):this._def.out._parseSync({data:e.value,path:r.path,parent:r})}}static create(e,t){return new em({in:e,out:t,typeName:n.ZodPipeline})}}t.ZodPipeline=em;class eg extends h{_parse(e){let t=this._def.innerType._parse(e),r=e=>((0,c.isValid)(e)&&(e.value=Object.freeze(e.value)),e);return(0,c.isAsync)(t)?t.then(e=>r(e)):r(t)}unwrap(){return this._def.innerType}}function ev(e,t){let r="function"==typeof e?e(t):"string"==typeof e?{message:e}:e;return"string"==typeof r?{message:r}:r}function ey(e,t={},r){return e?U.create().superRefine((n,o)=>{let a=e(n);if(a instanceof Promise)return a.then(e=>{if(!e){let e=ev(t,n),a=e.fatal??r??!0;o.addIssue({code:"custom",...e,fatal:a})}});if(!a){let e=ev(t,n),a=e.fatal??r??!0;o.addIssue({code:"custom",...e,fatal:a})}}):U.create()}t.ZodReadonly=eg,eg.create=(e,t)=>new eg({innerType:e,typeName:n.ZodReadonly,...p(t)}),t.late={object:q.lazycreate},(o=n||(t.ZodFirstPartyTypeKind=n={})).ZodString="ZodString",o.ZodNumber="ZodNumber",o.ZodNaN="ZodNaN",o.ZodBigInt="ZodBigInt",o.ZodBoolean="ZodBoolean",o.ZodDate="ZodDate",o.ZodSymbol="ZodSymbol",o.ZodUndefined="ZodUndefined",o.ZodNull="ZodNull",o.ZodAny="ZodAny",o.ZodUnknown="ZodUnknown",o.ZodNever="ZodNever",o.ZodVoid="ZodVoid",o.ZodArray="ZodArray",o.ZodObject="ZodObject",o.ZodUnion="ZodUnion",o.ZodDiscriminatedUnion="ZodDiscriminatedUnion",o.ZodIntersection="ZodIntersection",o.ZodTuple="ZodTuple",o.ZodRecord="ZodRecord",o.ZodMap="ZodMap",o.ZodSet="ZodSet",o.ZodFunction="ZodFunction",o.ZodLazy="ZodLazy",o.ZodLiteral="ZodLiteral",o.ZodEnum="ZodEnum",o.ZodEffects="ZodEffects",o.ZodNativeEnum="ZodNativeEnum",o.ZodOptional="ZodOptional",o.ZodNullable="ZodNullable",o.ZodDefault="ZodDefault",o.ZodCatch="ZodCatch",o.ZodPromise="ZodPromise",o.ZodBranded="ZodBranded",o.ZodPipeline="ZodPipeline",o.ZodReadonly="ZodReadonly",t.instanceof=(e,t={message:`Input not instance of ${e.name}`})=>ey(t=>t instanceof e,t);let eb=z.create;t.string=eb;let ex=R.create;t.number=ex,t.nan=ep.create,t.bigint=O.create;let e_=M.create;t.boolean=e_,t.date=A.create,t.symbol=D.create,t.undefined=Z.create,t.null=F.create,t.any=U.create,t.unknown=$.create,t.never=H.create,t.void=V.create,t.array=B.create,t.object=q.create,t.strictObject=q.strictCreate,t.union=W.create,t.discriminatedUnion=Y.create,t.intersection=X.create,t.tuple=G.create,t.record=Q.create,t.map=J.create,t.set=ee.create,t.function=et.create,t.lazy=er.create,t.literal=en.create,t.enum=ea.create,t.nativeEnum=ei.create,t.promise=el.create;let ew=es.create;t.effect=ew,t.transformer=ew,t.optional=ec.create,t.nullable=eu.create,t.preprocess=es.createWithPreprocess,t.pipeline=em.create,t.ostring=()=>eb().optional(),t.onumber=()=>ex().optional(),t.oboolean=()=>e_().optional(),t.coerce={string:e=>z.create({...e,coerce:!0}),number:e=>R.create({...e,coerce:!0}),boolean:e=>M.create({...e,coerce:!0}),bigint:e=>O.create({...e,coerce:!0}),date:e=>A.create({...e,coerce:!0})},t.NEVER=c.INVALID}},r={};function n(e){var o=r[e];if(void 0!==o)return o.exports;var a=r[e]={exports:{}},i=!0;try{t[e].call(a.exports,a,a.exports,n),i=!1}finally{i&&delete r[e]}return a.exports}n.ab="//",e.exports=n(629)})()}},__webpack_module_cache__={};function __webpack_require__(e){var t=__webpack_module_cache__[e];if(void 0!==t)return t.exports;var r=__webpack_module_cache__[e]={id:e,exports:{}};return __webpack_modules__[e](r,r.exports,__webpack_require__),r.exports}__webpack_require__.n=e=>{var t=e&&e.__esModule?()=>e.default:()=>e;return __webpack_require__.d(t,{a:t}),t},(()=>{var e,t=Object.getPrototypeOf?e=>Object.getPrototypeOf(e):e=>e.__proto__;__webpack_require__.t=function(r,n){if(1&n&&(r=this(r)),8&n||"object"==typeof r&&r&&(4&n&&r.__esModule||16&n&&"function"==typeof r.then))return r;var o=Object.create(null);__webpack_require__.r(o);var a={};e=e||[null,t({}),t([]),t(t)];for(var i=2&n&&r;("object"==typeof i||"function"==typeof i)&&!~e.indexOf(i);i=t(i))Object.getOwnPropertyNames(i).forEach(e=>{a[e]=()=>r[e]});return a.default=()=>r,__webpack_require__.d(o,a),o}})(),__webpack_require__.d=(e,t)=>{for(var r in t)__webpack_require__.o(t,r)&&!__webpack_require__.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:t[r]})},__webpack_require__.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),__webpack_require__.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},__webpack_require__.nc=void 0;var __webpack_exports__={};for(var __rspack_i in(()=>{"use strict";let e,t,r;__webpack_require__.r(__webpack_exports__),__webpack_require__.d(__webpack_exports__,{DevOverlayContext:()=>ul,dispatcher:()=>ua,renderPagesDevOverlay:()=>up,getSerializedOverlayState:()=>ur,useDevOverlayContext:()=>us,renderAppDevOverlay:()=>uf,getSegmentTrieData:()=>un});var n,o,a,i,l,s=__webpack_require__("../../node_modules/.pnpm/style-loader@4.0.0_webpack@5.98.0_@swc+core@1.11.24_@swc+helpers@0.5.15__esbuild@0.25.9_/node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js"),c=__webpack_require__.n(s),u=__webpack_require__("../../node_modules/.pnpm/style-loader@4.0.0_webpack@5.98.0_@swc+core@1.11.24_@swc+helpers@0.5.15__esbuild@0.25.9_/node_modules/style-loader/dist/runtime/styleDomAPI.js"),d=__webpack_require__.n(u),f=__webpack_require__("./src/build/webpack/loaders/devtool/devtool-style-inject.js"),p=__webpack_require__.n(f),h=__webpack_require__("../../node_modules/.pnpm/style-loader@4.0.0_webpack@5.98.0_@swc+core@1.11.24_@swc+helpers@0.5.15__esbuild@0.25.9_/node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js"),m=__webpack_require__.n(h),g=__webpack_require__("../../node_modules/.pnpm/style-loader@4.0.0_webpack@5.98.0_@swc+core@1.11.24_@swc+helpers@0.5.15__esbuild@0.25.9_/node_modules/style-loader/dist/runtime/insertStyleElement.js"),v=__webpack_require__.n(g),y=__webpack_require__("../../node_modules/.pnpm/style-loader@4.0.0_webpack@5.98.0_@swc+core@1.11.24_@swc+helpers@0.5.15__esbuild@0.25.9_/node_modules/style-loader/dist/runtime/styleTagTransform.js"),b=__webpack_require__.n(y),x=__webpack_require__("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/global.css"),_={};_.styleTagTransform=b(),_.setAttributes=m(),_.insert=p(),_.domAPI=d(),_.insertStyleElement=v(),c()(x.A,_),x.A&&x.A.locals&&x.A.locals;var w=__webpack_require__("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/components/toast/style.css"),k={};k.styleTagTransform=b(),k.setAttributes=m(),k.insert=p(),k.domAPI=d(),k.insertStyleElement=v(),c()(w.A,k),w.A&&w.A.locals&&w.A.locals;var j=__webpack_require__("./dist/compiled/react/jsx-runtime.js"),S=__webpack_require__("./dist/compiled/react/compiler-runtime.js"),C=__webpack_require__("./dist/compiled/react/index.js"),E=__webpack_require__.t(C,2),T=__webpack_require__("./dist/compiled/stacktrace-parser/stack-trace-parser.cjs.js");let N=/\/_next(\/static\/.+)/;function L(e,t=process.env.__NEXT_DIST_DIR){return e?(e=e.split("\n").map(e=>(e.includes("(eval ")&&(e=e.replace(/eval code/g,"eval").replace(/\(eval at [^()]* \(/,"(file://").replace(/\),.*$/g,")")),e)).join("\n"),(0,T.parse)(e).map(e=>{try{let r=new URL(e.file),n=N.exec(r.pathname);if(n){let o=t?.replace(/\\/g,"/")?.replace(/\/$/,"");o&&(e.file="file://"+o.concat(n.pop())+r.search)}}catch{}return{file:e.file,line1:e.lineNumber,column1:e.column,methodName:e.methodName,arguments:e.arguments}})):[]}let I=Symbol.for("next.console.error.digest"),P="next-instant-navigation-testing";function z(e){try{let t=JSON.parse(e);if(Array.isArray(t)&&t.length>=3){let e=t[2];if(null===e)return{state:"mpa"};if("object"==typeof e&&null!==e){let t=e.from??["",{}],r=e.to??null;return{state:"spa",fromTree:t,toTree:r}}return{state:"spa",fromTree:["",{}],toTree:null}}}catch{}return{state:"pending"}}function R(e){let t=[],r=e;for(;r;){let e=r[0],n=r[1];if("string"==typeof e)""===e||e.startsWith("__PAGE__")||"__DEFAULT__"===e||e.startsWith("(")&&e.endsWith(")")||t.push(e);else if(Array.isArray(e)){let r=e[0],n=e[2];"c"===n||n.startsWith("ci")?t.push(`[...${r}]`):"oc"===n?t.push(`[[...${r}]]`):t.push(`[${r}]`)}r=n?.children}return"/"+t.join("/")}function O(){if(void 0!==r)return r;if("undefined"==typeof document)return"";let e=document.cookie.match(/next-instant-navigation-testing=([^;]*)/);return e?e[1]:""}function M(e){if("undefined"==typeof cookieStore)return()=>{};function t(t){for(let n of t.changed)if(n.name===P){r=n.value??"",e();return}for(let n of t.deleted)if(n.name===P){r="",e();return}}return cookieStore.addEventListener("change",t),()=>{cookieStore.removeEventListener("change",t)}}let A={Small:16/14,Medium:1,Large:16/18},D="cache-indicator",Z="static-indicator",F="build-ok",U="build-error",$="before-fast-refresh",H="fast-refresh",V="version-info",B="unhandled-error",q="unhandled-rejection",W="debug-info",K="dev-indicator",Y="dev-indicator-disable",X="error-overlay-open",G="error-overlay-close",Q="error-overlay-toggle",J="building-indicator-show",ee="building-indicator-hide",et="rendering-indicator-show",er="rendering-indicator-hide",en="devtools-position",eo="devtools-panel-position",ea="devtools-scale",ei="devtools-config",el="instant-navs-toggle",es="instant-navs-reset",ec="__nextjs-dev-tools-panel-position",eu="__nextjs-dev-tools-panel-size",ed="__nextjs-dev-tools-shared-panel-size",ef="__nextjs-dev-tools-shared-panel-location",ep="segment-explorer-update-route-state",eh=/\s+(at Object\.react_stack_bottom_frame.*)|(react_stack_bottom_frame@.*)|(at react-stack-bottom-frame.*)|(react-stack-bottom-frame@.*)/;function em(e){return e?.split(eh)[0]}let eg=process.env.__NEXT_DEV_INDICATOR?.toString()==="false",ev=process.env.__NEXT_DEV_INDICATOR_POSITION??"bottom-left",ey=!!process.env.__NEXT_INSTANT_NAV_TOGGLE&&null!==function(){if("undefined"==typeof document)return null;let e=document.cookie.match(/next-instant-navigation-testing=([^;]*)/);return e?z(e[1]).state:null}(),eb={nextId:1,buildError:null,errors:[],notFound:!1,renderingIndicator:!1,cacheIndicator:"disabled",staticIndicator:"disabled",showIndicator:ey,disableDevIndicator:!1,buildingIndicator:!1,refreshState:{type:"idle"},versionInfo:{installed:"0.0.0",staleness:"unknown"},debugInfo:{devtoolsFrontendUrl:void 0},devToolsPosition:ev,devToolsPanelPosition:{[ef]:ev},devToolsPanelSize:{},scale:A.Medium,page:"",tree:null,theme:"system",hideShortcut:null,instantNavs:ey};var ex=__webpack_require__("./dist/compiled/react-dom/client.js");function e_(e,...t){let r=e.length-1;return(e.slice(0,r).reduce((e,r,n)=>e+r+t[n],"")+e[r]).replace(/\/\*[\s\S]*?\*\//g,"").replace(/\s+/g," ").replace(/\s*([:;,{}])\s*/g,"$1").replace(/;+}/g,"}").trim()}let ew=()=>{let e,t=(0,S.c)(1);return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=[],t[0]=e):e=t[0],(0,C.useInsertionEffect)(ek,e),null};function ek(){let e=document.createElement("style");return e.textContent=e_`
      /* latin-ext */
      @font-face {
        font-family: '__nextjs-Geist';
        font-style: normal;
        font-weight: 400 600;
        font-display: swap;
        src: url(/__nextjs_font/geist-latin-ext.woff2) format('woff2');
        unicode-range:
          U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF,
          U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020,
          U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF;
      }
      /* latin-ext */
      @font-face {
        font-family: '__nextjs-Geist Mono';
        font-style: normal;
        font-weight: 400 600;
        font-display: swap;
        src: url(/__nextjs_font/geist-mono-latin-ext.woff2) format('woff2');
        unicode-range:
          U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF,
          U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020,
          U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF;
      }
      /* latin */
      @font-face {
        font-family: '__nextjs-Geist';
        font-style: normal;
        font-weight: 400 600;
        font-display: swap;
        src: url(/__nextjs_font/geist-latin.woff2) format('woff2');
        unicode-range:
          U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC,
          U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193,
          U+2212, U+2215, U+FEFF, U+FFFD;
      }
      /* latin */
      @font-face {
        font-family: '__nextjs-Geist Mono';
        font-style: normal;
        font-weight: 400 600;
        font-display: swap;
        src: url(/__nextjs_font/geist-mono-latin.woff2) format('woff2');
        unicode-range:
          U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC,
          U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193,
          U+2212, U+2215, U+FEFF, U+FFFD;
      }
    `,document.head.appendChild(e),()=>{document.head.removeChild(e)}}var ej=__webpack_require__("./dist/compiled/react-dom/index.js");function eS(e){let t,r=(0,S.c)(3),{children:n}=e,{shadowRoot:o}=us();return r[0]!==n||r[1]!==o?(t=(0,ej.createPortal)(n,o),r[0]=n,r[1]=o,r[2]=t):t=r[2],t}function eC(e){if(""===e.trim())throw Error("can't decode empty hex");let t=parseInt(e,16);if(isNaN(t))throw Error(`invalid hex: \`${e}\``);return String.fromCodePoint(t)}let eE=/^__TURBOPACK__([a-zA-Z0-9_$]+)__$/,eT=/__TURBOPACK__[a-zA-Z0-9_$]+__/g;function eN(e){return e.replace(/\[project\]/g,".").replace(/\s\[([^\]]*)\]/g,"").replace(/\s\(([^)]*)\)/g,"").replace(/\s<([^>]*)>/g,"").trim()}let eL=/https?:\/\/[^\s/$.?#].[^\s)'"]*/i,eI=function(e){let t,r,n=(0,S.c)(7),{text:o,matcher:a}=e;if(n[0]!==a||n[1]!==o){let e,r=function(e){let t=e.replace(/\(0\s*,\s*(__TURBOPACK__[a-zA-Z0-9_$]+__\.[^\s)]+)\)/g,"$1"),r=[],n=0,o=RegExp(eT.source,"g");for(let e=o.exec(t);null!==e;e=o.exec(t)){let a=e.index,i=o.lastIndex,l=e[0];if(a>n){let e=t.substring(n,a);r.push(["raw",e])}try{let e=function(e){let t=e.match(eE);if(!t)return e;let r=t[1],n="",o=0,a="";for(let e=0;e<r.length;e++){let t=r[e];if(0===o)"_"===t?o=1:"$"===t?o=2:n+=t;else if(1===o)"_"===t?(n+=" ",o=0):"$"===t?(n+="_",o=2):(n+=t,o=0);else if(2===o)if(2===a.length&&(n+=eC(a),a=""),"_"===t){if(""!==a)throw Error(`invalid hex: \`${a}\``);o=3}else if("$"===t){if(""!==a)throw Error(`invalid hex: \`${a}\``);o=0}else a+=t;else if(3===o)if("_"===t)throw Error(`invalid hex: \`${a+t}\``);else"$"===t?(n+=eC(a),a="",o=0):a+=t}return n}(l);if(e!==l){let t=e.match(/^imported module (.+)$/);if(t){let e=t[1],n=eN(e);r.push(["deobfuscated",`{imported module ${n}}`])}else{let t=eN(e);r.push(["deobfuscated",`{${t}}`])}}else r.push(["raw",l])}catch(e){r.push(["deobfuscated",`{${l} (decoding failed: ${e})}`])}n=i}if(n<t.length){let e=t.substring(n);r.push(["raw",e])}return r}(o);n[3]!==a?(e=(e,t)=>{let[r,n]=e;if("raw"===r)return n.split(/(\s+|https?:\/\/[^\s/$.?#].[^\s)'"]*)/).map((e,r)=>{if(!eL.test(e))return(0,j.jsx)(C.Fragment,{children:e},`text-${t}-${r}`);{let n=eL.exec(e)[0],o=null;return"function"==typeof a&&null===(o=a(n))?(0,j.jsx)(C.Fragment,{children:e},`link-${t}-${r}`):(0,j.jsx)(C.Fragment,{children:(0,j.jsx)("a",{href:n,target:"_blank",rel:"noreferrer noopener",className:o||void 0,children:e})},`link-${t}-${r}`)}});if("deobfuscated"===r)return(0,j.jsx)("i",{children:n},`ident-${t}`);throw Error(`Unknown text part type: ${r}`)},n[3]=a,n[4]=e):e=n[4],t=r.map(e),n[0]=a,n[1]=o,n[2]=t}else t=n[2];return n[5]!==t?(r=(0,j.jsx)(j.Fragment,{children:t}),n[5]=t,n[6]=r):r=n[6],r},eP=[/^webpack-internal:\/\/\/(\([\w-]+\)\/)?/,/^(webpack:\/\/\/|webpack:\/\/(_N_E\/)?)(\([\w-]+\)\/)?/];function ez(e){for(let t of eP){if(t.test(e))return!0;e=e.replace(t,"")}return!1}function eR(e){for(let t of eP)e=e.replace(t,"");return e}function eO(e,t){async function r(){if("rejected"===t.status)throw Error(t.reason);let r=t.value;return{error:!1,reason:null,external:!1,sourceStackFrame:e,originalStackFrame:r.originalStackFrame,originalCodeFrame:r.originalCodeFrame||null,ignored:r.originalStackFrame?.ignored||!1}}return"file://"===e.file||e.file?.match(/https?:\/\//)?Promise.resolve({error:!1,reason:null,external:!0,sourceStackFrame:e,originalStackFrame:null,originalCodeFrame:null,ignored:!0}):r().catch(t=>({error:!0,reason:t?.message??t?.toString()??"Unknown Error",external:!1,sourceStackFrame:e,originalStackFrame:null,originalCodeFrame:null,ignored:!1}))}async function eM(e,t,r){let n,o;try{n=await fetch("/__nextjs_original-stack-frames",{method:"POST",body:JSON.stringify({frames:e,isServer:"server"===t,isEdgeServer:"edge-server"===t,isAppDirectory:r})})}catch(e){o=e+""}if(n&&n.ok&&204!==n.status){let t=await n.json();return Promise.all(e.map((e,r)=>eO(e,t[r])))}return n&&(o=await n.text()),Promise.all(e.map(e=>eO(e,{status:"rejected",reason:`Failed to fetch the original stack frames ${o?`: ${o}`:""}`})))}function eA(e){if(!e.file)return"";let t=ez(e.file),r="";if(t)r=eR(e.file);else try{let t=new URL(e.file),n="";globalThis.location?.origin!==t.origin&&("null"===t.origin?n+=t.protocol:n+=t.origin),n+=t.pathname,r=eR(n)}catch{r=eR(e.file)}return!ez(e.file)&&null!=e.line1&&r&&"<anonymous>"!==e.file&&(null!=e.column1?r+=` (${e.line1}:${e.column1})`:r+=` (${e.line1})`),r}function eD(e){let t,r,n=(0,S.c)(6);n[0]!==e?(t=void 0===e?{}:e,n[0]=e,n[1]=t):t=n[1];let{file:o,line1:a,column1:i}=t;return n[2]!==i||n[3]!==o||n[4]!==a?(r=()=>{if(null==o||null==a||null==i)return;let e=new URLSearchParams;e.append("file",o),e.append("line1",String(a)),e.append("column1",String(i)),self.fetch(`${process.env.__NEXT_ROUTER_BASEPATH||""}/__nextjs_launch-editor?${e.toString()}`).then(eZ,e=>{console.error(`Failed to open file "${o} (${a}:${i})" in your editor. Cause:`,e)})},n[2]=i,n[3]=o,n[4]=a,n[5]=r):r=n[5],r}function eZ(){}function eF(e){let t,r,n=(0,S.c)(3);return n[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",fill:"currentColor",d:"M11.5 9.75V11.25C11.5 11.3881 11.3881 11.5 11.25 11.5H4.75C4.61193 11.5 4.5 11.3881 4.5 11.25L4.5 4.75C4.5 4.61193 4.61193 4.5 4.75 4.5H6.25H7V3H6.25H4.75C3.7835 3 3 3.7835 3 4.75V11.25C3 12.2165 3.7835 13 4.75 13H11.25C12.2165 13 13 12.2165 13 11.25V9.75V9H11.5V9.75ZM8.5 3H9.25H12.2495C12.6637 3 12.9995 3.33579 12.9995 3.75V6.75V7.5H11.4995V6.75V5.56066L8.53033 8.52978L8 9.06011L6.93934 7.99945L7.46967 7.46912L10.4388 4.5H9.25H8.5V3Z"}),n[0]=t):t=n[0],n[1]!==e?(r=(0,j.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:"16",height:"16",viewBox:"0 0 16 16",fill:"none",...e,children:t}),n[1]=e,n[2]=r):r=n[2],r}function eU(e){let t,r,n=(0,S.c)(3);return n[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M8.55846 2H7.44148L1.88975 13.5H14.1102L8.55846 2ZM9.90929 1.34788C9.65902 0.829456 9.13413 0.5 8.55846 0.5H7.44148C6.86581 0.5 6.34092 0.829454 6.09065 1.34787L0.192608 13.5653C-0.127943 14.2293 0.355835 15 1.09316 15H14.9068C15.6441 15 16.1279 14.2293 15.8073 13.5653L9.90929 1.34788ZM8.74997 4.75V5.5V8V8.75H7.24997V8V5.5V4.75H8.74997ZM7.99997 12C8.55226 12 8.99997 11.5523 8.99997 11C8.99997 10.4477 8.55226 10 7.99997 10C7.44769 10 6.99997 10.4477 6.99997 11C6.99997 11.5523 7.44769 12 7.99997 12Z",fill:"currentColor"}),n[0]=t):t=n[0],n[1]!==e?(r=(0,j.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",height:"16",strokeLinejoin:"round",viewBox:"-4 -4 24 24",width:"16",...e,children:t}),n[1]=e,n[2]=r):r=n[2],r}function e$(e){let t=(0,S.c)(6),{lang:r}=e;if(!r){let e;return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)(eq,{}),t[0]=e):e=t[0],e}switch(r.toLowerCase()){case"jsx":case"tsx":{let e;return t[1]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)(eW,{}),t[1]=e):e=t[1],e}case"ts":case"typescript":{let e;return t[2]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)(eB,{}),t[2]=e):e=t[2],e}case"javascript":case"js":case"mjs":{let e;return t[3]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)(eV,{}),t[3]=e):e=t[3],e}case"json":{let e;return t[4]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)(eH,{}),t[4]=e):e=t[4],e}default:{let e;return t[5]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)(eq,{}),t[5]=e):e=t[5],e}}}function eH(){let e,t=(0,S.c)(1);return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("svg",{clipRule:"evenodd",fillRule:"evenodd",height:"16",viewBox:"0 0 1321.45 1333.33",width:"16",children:(0,j.jsx)("path",{d:"M221.37 618.44h757.94V405.15H755.14c-23.5 0-56.32-12.74-71.82-28.24-15.5-15.5-25-43.47-25-66.97V82.89H88.39c-1.99 0-3.49 1-4.49 2-1.5 1-2 2.5-2 4.5v1155.04c0 1.5 1 3.5 2 4.5 1 1.49 3 1.99 4.49 1.99H972.8c2 0 1.89-.99 2.89-1.99 1.5-1 3.61-3 3.61-4.5v-121.09H221.36c-44.96 0-82-36.9-82-81.99V700.44c0-45.1 36.9-82 82-82zm126.51 117.47h75.24v146.61c0 30.79-2.44 54.23-7.33 70.31-4.92 16.03-14.8 29.67-29.65 40.85-14.86 11.12-33.91 16.72-57.05 16.72-24.53 0-43.51-3.71-56.94-11.06-13.5-7.36-23.89-18.1-31.23-32.3-7.35-14.14-11.69-31.67-12.99-52.53l71.5-10.81c.11 11.81 1.07 20.61 2.81 26.33 1.76 5.78 4.75 10.37 9 13.95 2.87 2.33 6.94 3.46 12.25 3.46 8.4 0 14.58-3.46 18.53-10.37 3.9-6.92 5.87-18.6 5.87-35V735.92zm112.77 180.67l71.17-4.97c1.54 12.81 4.69 22.62 9.44 29.28 7.74 10.88 18.74 16.34 33.09 16.34 10.68 0 18.93-2.76 24.68-8.36 5.81-5.58 8.7-12.07 8.7-19.41 0-6.97-2.71-13.26-8.2-18.79-5.47-5.53-18.23-10.68-38.28-15.65-32.89-8.17-56.27-19.1-70.26-32.74-14.12-13.57-21.18-30.92-21.18-52.03 0-13.83 3.61-26.89 10.85-39.21 7.22-12.38 18.07-22.06 32.59-29.09 14.52-7.04 34.4-10.56 59.65-10.56 31 0 54.62 6.41 70.88 19.29 16.28 12.81 25.92 33.24 29.04 61.27l-70.5 4.65c-1.87-12.25-5.81-21.17-11.81-26.7-6.05-5.6-14.35-8.36-24.9-8.36-8.71 0-15.31 2.07-19.73 6.16-4.4 4.09-6.59 9.12-6.59 15.02 0 4.27 1.81 8.11 5.37 11.57 3.45 3.59 11.8 6.85 25.02 9.93 32.75 7.86 56.2 15.84 70.31 23.87 14.18 8.05 24.52 17.98 30.96 29.92 6.44 11.88 9.66 25.2 9.66 39.96 0 17.29-4.3 33.24-12.88 47.89-8.63 14.58-20.61 25.7-36.08 33.24-15.41 7.54-34.85 11.31-58.33 11.31-41.24 0-69.81-8.86-85.68-26.52-15.88-17.65-24.85-40.09-26.96-67.3zm248.74-45.5c0-44.05 11.02-78.36 33.09-102.87 22.09-24.57 52.82-36.82 92.24-36.82 40.38 0 71.5 12.07 93.34 36.13 21.86 24.13 32.77 57.94 32.77 101.37 0 31.54-4.75 57.36-14.3 77.54-9.54 20.18-23.37 35.89-41.4 47.13-18.07 11.24-40.55 16.84-67.48 16.84-27.33 0-49.99-4.83-67.94-14.52-17.92-9.74-32.49-25.07-43.62-46.06-11.13-20.92-16.72-47.19-16.72-78.74zm74.89.19c0 27.21 4.57 46.81 13.68 58.68 9.13 11.88 21.57 17.85 37.26 17.85 16.1 0 28.65-5.84 37.45-17.47 8.87-11.68 13.28-32.54 13.28-62.77 0-25.39-4.63-43.92-13.84-55.61-9.26-11.76-21.75-17.6-37.56-17.6-15.13 0-27.34 5.97-36.49 17.85-9.21 11.88-13.78 31.61-13.78 59.07zm209.08-135.36h69.99l90.98 149.05V735.91h70.83v269.96h-70.83l-90.48-148.24v148.24h-70.49V735.91zm67.71-117.47h178.37c45.1 0 82 37.04 82 82v340.91c0 44.96-37.03 81.99-82 81.99h-178.37v147c0 17.5-6.99 32.99-18.5 44.5-11.5 11.49-27 18.5-44.5 18.5H62.97c-17.5 0-32.99-7-44.5-18.5-11.49-11.5-18.5-27-18.5-44.5V63.49c0-17.5 7-33 18.5-44.5S45.97.49 62.97.49H700.1c1.5-.5 3-.5 4.5-.5 7 0 14 3 19 7.49h1c1 .5 1.5 1 2.5 2l325.46 329.47c5.5 5.5 9.5 13 9.5 21.5 0 2.5-.5 4.5-1 7v250.98zM732.61 303.47V96.99l232.48 235.47H761.6c-7.99 0-14.99-3.5-20.5-8.49-4.99-5-8.49-12.5-8.49-20.5z",fill:"currentColor"})}),t[0]=e):e=t[0],e}function eV(){let e,t=(0,S.c)(1);return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("svg",{height:"16",viewBox:"0 0 50 50",width:"16",xmlns:"http://www.w3.org/2000/svg",children:(0,j.jsx)("path",{d:"M 43.335938 4 L 6.667969 4 C 5.195313 4 4 5.195313 4 6.667969 L 4 43.332031 C 4 44.804688 5.195313 46 6.667969 46 L 43.332031 46 C 44.804688 46 46 44.804688 46 43.335938 L 46 6.667969 C 46 5.195313 44.804688 4 43.335938 4 Z M 27 36.183594 C 27 40.179688 24.65625 42 21.234375 42 C 18.140625 42 15.910156 39.925781 15 38 L 18.144531 36.097656 C 18.75 37.171875 19.671875 38 21 38 C 22.269531 38 23 37.503906 23 35.574219 L 23 23 L 27 23 Z M 35.675781 42 C 32.132813 42 30.121094 40.214844 29 38 L 32 36 C 32.816406 37.335938 33.707031 38.613281 35.589844 38.613281 C 37.171875 38.613281 38 37.824219 38 36.730469 C 38 35.425781 37.140625 34.960938 35.402344 34.199219 L 34.449219 33.789063 C 31.695313 32.617188 29.863281 31.148438 29.863281 28.039063 C 29.863281 25.179688 32.046875 23 35.453125 23 C 37.878906 23 39.621094 23.84375 40.878906 26.054688 L 37.910156 27.964844 C 37.253906 26.789063 36.550781 26.328125 35.453125 26.328125 C 34.335938 26.328125 33.628906 27.039063 33.628906 27.964844 C 33.628906 29.109375 34.335938 29.570313 35.972656 30.28125 L 36.925781 30.691406 C 40.171875 32.078125 42 33.496094 42 36.683594 C 42 40.117188 39.300781 42 35.675781 42 Z",fill:"currentColor"})}),t[0]=e):e=t[0],e}function eB(){let e,t=(0,S.c)(1);return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsxs)("svg",{fill:"none",height:"14",viewBox:"0 0 512 512",width:"14",xmlns:"http://www.w3.org/2000/svg",children:[(0,j.jsx)("rect",{fill:"currentColor",height:"512",rx:"50",width:"512"}),(0,j.jsx)("rect",{fill:"currentColor",height:"512",rx:"50",width:"512"}),(0,j.jsx)("path",{clipRule:"evenodd",d:"m316.939 407.424v50.061c8.138 4.172 17.763 7.3 28.875 9.386s22.823 3.129 35.135 3.129c11.999 0 23.397-1.147 34.196-3.442 10.799-2.294 20.268-6.075 28.406-11.342 8.138-5.266 14.581-12.15 19.328-20.65s7.121-19.007 7.121-31.522c0-9.074-1.356-17.026-4.069-23.857s-6.625-12.906-11.738-18.225c-5.112-5.319-11.242-10.091-18.389-14.315s-15.207-8.213-24.18-11.967c-6.573-2.712-12.468-5.345-17.685-7.9-5.217-2.556-9.651-5.163-13.303-7.822-3.652-2.66-6.469-5.476-8.451-8.448-1.982-2.973-2.974-6.336-2.974-10.091 0-3.441.887-6.544 2.661-9.308s4.278-5.136 7.512-7.118c3.235-1.981 7.199-3.52 11.894-4.615 4.696-1.095 9.912-1.642 15.651-1.642 4.173 0 8.581.313 13.224.938 4.643.626 9.312 1.591 14.008 2.894 4.695 1.304 9.259 2.947 13.694 4.928 4.434 1.982 8.529 4.276 12.285 6.884v-46.776c-7.616-2.92-15.937-5.084-24.962-6.492s-19.381-2.112-31.066-2.112c-11.895 0-23.163 1.278-33.805 3.833s-20.006 6.544-28.093 11.967c-8.086 5.424-14.476 12.333-19.171 20.729-4.695 8.395-7.043 18.433-7.043 30.114 0 14.914 4.304 27.638 12.912 38.172 8.607 10.533 21.675 19.45 39.204 26.751 6.886 2.816 13.303 5.579 19.25 8.291s11.086 5.528 15.415 8.448c4.33 2.92 7.747 6.101 10.252 9.543 2.504 3.441 3.756 7.352 3.756 11.733 0 3.233-.783 6.231-2.348 8.995s-3.939 5.162-7.121 7.196-7.147 3.624-11.894 4.771c-4.748 1.148-10.303 1.721-16.668 1.721-10.851 0-21.597-1.903-32.24-5.71-10.642-3.806-20.502-9.516-29.579-17.13zm-84.159-123.342h64.22v-41.082h-179v41.082h63.906v182.918h50.874z",fill:"var(--color-background-100)",fillRule:"evenodd"})]}),t[0]=e):e=t[0],e}function eq(){let e,t=(0,S.c)(1);return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("svg",{width:"16",height:"17",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M14.5 7v7a2.5 2.5 0 0 1-2.5 2.5H4A2.5 2.5 0 0 1 1.5 14V.5h7.586a1 1 0 0 1 .707.293l4.414 4.414a1 1 0 0 1 .293.707V7zM13 7v7a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2h5v5h5zM9.5 2.621V5.5h2.879L9.5 2.621z",fill:"currentColor"})}),t[0]=e):e=t[0],e}function eW(){let e,t,r=(0,S.c)(2);return r[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("g",{clipPath:"url(#file_react_clip0_872_3183)",children:(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M4.5 1.93782C4.70129 1.82161 4.99472 1.7858 5.41315 1.91053C5.83298 2.03567 6.33139 2.31073 6.87627 2.73948C7.01136 2.84578 7.14803 2.96052 7.28573 3.08331C6.86217 3.53446 6.44239 4.04358 6.03752 4.60092C5.35243 4.67288 4.70164 4.78186 4.09916 4.92309C4.06167 4.74244 4.03064 4.56671 4.00612 4.39656C3.90725 3.71031 3.91825 3.14114 4.01979 2.71499C4.12099 2.29025 4.29871 2.05404 4.5 1.93782ZM7.49466 1.95361C7.66225 2.08548 7.83092 2.22804 7.99999 2.38067C8.16906 2.22804 8.33773 2.08548 8.50532 1.95361C9.10921 1.47842 9.71982 1.12549 10.3012 0.952202C10.8839 0.778496 11.4838 0.7738 12 1.0718C12.5161 1.3698 12.812 1.89169 12.953 2.48322C13.0936 3.07333 13.0932 3.77858 12.9836 4.53917C12.9532 4.75024 12.9141 4.9676 12.8665 5.19034C13.0832 5.26044 13.291 5.33524 13.489 5.41444C14.2025 5.69983 14.8134 6.05217 15.2542 6.46899C15.696 6.8868 16 7.404 16 8C16 8.596 15.696 9.11319 15.2542 9.53101C14.8134 9.94783 14.2025 10.3002 13.489 10.5856C13.291 10.6648 13.0832 10.7396 12.8665 10.8097C12.9141 11.0324 12.9532 11.2498 12.9837 11.4608C13.0932 12.2214 13.0936 12.9267 12.953 13.5168C12.812 14.1083 12.5161 14.6302 12 14.9282C11.4839 15.2262 10.8839 15.2215 10.3012 15.0478C9.71984 14.8745 9.10923 14.5216 8.50534 14.0464C8.33775 13.9145 8.16906 13.7719 7.99999 13.6193C7.83091 13.7719 7.66223 13.9145 7.49464 14.0464C6.89075 14.5216 6.28014 14.8745 5.69879 15.0478C5.11605 15.2215 4.51613 15.2262 3.99998 14.9282C3.48383 14.6302 3.18794 14.1083 3.047 13.5168C2.9064 12.9267 2.90674 12.2214 3.01632 11.4608C3.04673 11.2498 3.08586 11.0324 3.13351 10.8097C2.91679 10.7395 2.709 10.6648 2.511 10.5856C1.79752 10.3002 1.18658 9.94783 0.745833 9.53101C0.304028 9.11319 0 8.596 0 8C0 7.404 0.304028 6.8868 0.745833 6.46899C1.18658 6.05217 1.79752 5.69983 2.511 5.41444C2.709 5.33524 2.9168 5.26044 3.13352 5.19034C3.08587 4.9676 3.04675 4.75024 3.01634 4.53917C2.90676 3.77858 2.90642 3.07332 3.04702 2.48321C3.18796 1.89169 3.48385 1.3698 4 1.0718C4.51615 0.773798 5.11607 0.778495 5.69881 0.952201C6.28016 1.12549 6.89077 1.47841 7.49466 1.95361ZM7.36747 4.51025C7.57735 4.25194 7.78881 4.00927 7.99999 3.78356C8.21117 4.00927 8.42263 4.25194 8.63251 4.51025C8.42369 4.50346 8.21274 4.5 8 4.5C7.78725 4.5 7.5763 4.50345 7.36747 4.51025ZM8.71425 3.08331C9.13781 3.53447 9.55759 4.04358 9.96246 4.60092C10.6475 4.67288 11.2983 4.78186 11.9008 4.92309C11.9383 4.74244 11.9693 4.56671 11.9939 4.39657C12.0927 3.71031 12.0817 3.14114 11.9802 2.71499C11.879 2.29025 11.7013 2.05404 11.5 1.93782C11.2987 1.82161 11.0053 1.7858 10.5868 1.91053C10.167 2.03568 9.66859 2.31073 9.12371 2.73948C8.98862 2.84578 8.85196 2.96052 8.71425 3.08331ZM8 5.5C8.48433 5.5 8.95638 5.51885 9.41188 5.55456C9.67056 5.93118 9.9229 6.33056 10.1651 6.75C10.4072 7.16944 10.6269 7.58766 10.8237 7.99998C10.6269 8.41232 10.4072 8.83055 10.165 9.25C9.92288 9.66944 9.67053 10.0688 9.41185 10.4454C8.95636 10.4812 8.48432 10.5 8 10.5C7.51567 10.5 7.04363 10.4812 6.58813 10.4454C6.32945 10.0688 6.0771 9.66944 5.83494 9.25C5.59277 8.83055 5.37306 8.41232 5.17624 7.99998C5.37306 7.58765 5.59275 7.16944 5.83492 6.75C6.07708 6.33056 6.32942 5.93118 6.5881 5.55456C7.04361 5.51884 7.51566 5.5 8 5.5ZM11.0311 6.25C11.1375 6.43423 11.2399 6.61864 11.3385 6.80287C11.4572 6.49197 11.5616 6.18752 11.6515 5.89178C11.3505 5.82175 11.0346 5.75996 10.706 5.70736C10.8163 5.8848 10.9247 6.06576 11.0311 6.25ZM11.0311 9.75C11.1374 9.56576 11.2399 9.38133 11.3385 9.19709C11.4572 9.50801 11.5617 9.81246 11.6515 10.1082C11.3505 10.1782 11.0346 10.24 10.7059 10.2926C10.8162 10.1152 10.9247 9.93424 11.0311 9.75ZM11.9249 7.99998C12.2051 8.62927 12.4362 9.24738 12.6151 9.83977C12.7903 9.78191 12.958 9.72092 13.1176 9.65708C13.7614 9.39958 14.2488 9.10547 14.5671 8.80446C14.8843 8.50445 15 8.23243 15 8C15 7.76757 14.8843 7.49555 14.5671 7.19554C14.2488 6.89453 13.7614 6.60042 13.1176 6.34292C12.958 6.27907 12.7903 6.21808 12.6151 6.16022C12.4362 6.7526 12.2051 7.37069 11.9249 7.99998ZM9.96244 11.3991C10.6475 11.3271 11.2983 11.2181 11.9008 11.0769C11.9383 11.2576 11.9694 11.4333 11.9939 11.6034C12.0928 12.2897 12.0817 12.8589 11.9802 13.285C11.879 13.7098 11.7013 13.946 11.5 14.0622C11.2987 14.1784 11.0053 14.2142 10.5868 14.0895C10.167 13.9643 9.66861 13.6893 9.12373 13.2605C8.98863 13.1542 8.85196 13.0395 8.71424 12.9167C9.1378 12.4655 9.55758 11.9564 9.96244 11.3991ZM8.63249 11.4898C8.42262 11.7481 8.21116 11.9907 7.99999 12.2164C7.78881 11.9907 7.57737 11.7481 7.36749 11.4897C7.57631 11.4965 7.78726 11.5 8 11.5C8.21273 11.5 8.42367 11.4965 8.63249 11.4898ZM4.96891 9.75C5.07528 9.93424 5.18375 10.1152 5.29404 10.2926C4.9654 10.24 4.64951 10.1782 4.34844 10.1082C4.43833 9.81246 4.54276 9.508 4.66152 9.19708C4.76005 9.38133 4.86254 9.56575 4.96891 9.75ZM6.03754 11.3991C5.35244 11.3271 4.70163 11.2181 4.09914 11.0769C4.06165 11.2576 4.03062 11.4333 4.0061 11.6034C3.90723 12.2897 3.91823 12.8589 4.01977 13.285C4.12097 13.7098 4.29869 13.946 4.49998 14.0622C4.70127 14.1784 4.9947 14.2142 5.41313 14.0895C5.83296 13.9643 6.33137 13.6893 6.87625 13.2605C7.01135 13.1542 7.14802 13.0395 7.28573 12.9167C6.86217 12.4655 6.4424 11.9564 6.03754 11.3991ZM4.07507 7.99998C3.79484 8.62927 3.56381 9.24737 3.38489 9.83977C3.20969 9.78191 3.042 9.72092 2.88239 9.65708C2.23864 9.39958 1.75123 9.10547 1.43294 8.80446C1.11571 8.50445 1 8.23243 1 8C1 7.76757 1.11571 7.49555 1.43294 7.19554C1.75123 6.89453 2.23864 6.60042 2.88239 6.34292C3.042 6.27907 3.2097 6.21808 3.3849 6.16022C3.56383 6.75261 3.79484 7.37069 4.07507 7.99998ZM4.66152 6.80287C4.54277 6.49197 4.43835 6.18752 4.34846 5.89178C4.64952 5.82175 4.96539 5.75996 5.29402 5.70736C5.18373 5.8848 5.07526 6.06576 4.96889 6.25C4.86253 6.43423 4.76005 6.61864 4.66152 6.80287ZM9.25 8C9.25 8.69036 8.69036 9.25 8 9.25C7.30964 9.25 6.75 8.69036 6.75 8C6.75 7.30965 7.30964 6.75 8 6.75C8.69036 6.75 9.25 7.30965 9.25 8Z",fill:"currentColor"})}),r[0]=e):e=r[0],r[1]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsxs)("svg",{height:"16",strokeLinejoin:"round",viewBox:"0 0 16 16",width:"16",children:[e,(0,j.jsx)("defs",{children:(0,j.jsx)("clipPath",{id:"file_react_clip0_872_3183",children:(0,j.jsx)("rect",{width:"16",height:"16",fill:"white"})})})]}),r[1]=t):t=r[1],t}var eK=__webpack_require__("./dist/compiled/anser/index.js"),eY=__webpack_require__.n(eK),eX=__webpack_require__("./dist/compiled/strip-ansi/index.js"),eG=__webpack_require__.n(eX);function eQ(e){let t=e.split(/\r?\n/g),r=t.map(e=>null===/^>? +\d+ +\| [ ]+/.exec(eG()(e))?null:/^>? +\d+ +\| ( *)/.exec(eG()(e))).filter(Boolean).map(e=>e.pop()).reduce((e,t)=>isNaN(e)?t.length:Math.min(e,t.length),NaN);return r>1?t.map((e,t)=>~(t=e.indexOf("|"))?e.substring(0,t)+e.substring(t).replace(`^\\ {${r}}`,""):e).join("\n"):t.join("\n")}function eJ(e){let t,r,n,o,a,i,l,s,c,u,d,f,p,h=(0,S.c)(34),{stackFrame:m,codeFrame:g}=e;if(h[0]!==g||h[1]!==m){let e,r=function(e){let t=eY().ansiToJson(e,{json:!0,use_classes:!0,remove_empty:!0}),r=[],n=[];for(let e of t)if("string"==typeof e.content&&e.content.includes("\n")){let t=e.content.split("\n");for(let o=0;o<t.length;o++){let a=t[o];a&&n.push({...e,content:a}),o<t.length-1&&(r.push(n),n=[])}}else n.push(e);return n.length>0&&r.push(n),r}(eQ(g));h[3]!==m?(e=e=>{var t,r;let n,o;return{line:e,parsedLine:(t=e,r=m,(t[0]?.content===">"||t[0]?.content===" ")&&(n=t[1],o=n?.content?.replace("|","")?.trim()),{lineNumber:o,isErroredLine:o===r.line1?.toString()})}},h[3]=m,h[4]=e):e=h[4],t=r.map(e),h[0]=g,h[1]=m,h[2]=t}else t=h[2];let v=t,y=m.line1??1,b=m.column1??1;h[5]!==m.file||h[6]!==y||h[7]!==b?(r={file:m.file,line1:y,column1:b},h[5]=m.file,h[6]=y,h[7]=b,h[8]=r):r=h[8];let x=eD(r);h[9]!==m.file?(n=m?.file?.split(".").pop(),h[9]=m.file,h[10]=n):n=h[10];let _=n;return h[11]!==_?(o=(0,j.jsx)("span",{className:"code-frame-icon",children:(0,j.jsx)(e$,{lang:_})}),h[11]=_,h[12]=o):o=h[12],h[13]!==m?(a=eA(m),h[13]=m,h[14]=a):a=h[14],h[15]!==m.methodName?(i=(0,j.jsx)(eI,{text:m.methodName}),h[15]=m.methodName,h[16]=i):i=h[16],h[17]!==a||h[18]!==i?(l=(0,j.jsxs)("span",{"data-text":!0,children:[a," @"," ",i]}),h[17]=a,h[18]=i,h[19]=l):l=h[19],h[20]===Symbol.for("react.memo_cache_sentinel")?(s=(0,j.jsx)("span",{className:"code-frame-icon","data-icon":"right",children:(0,j.jsx)(eF,{width:16,height:16})}),h[20]=s):s=h[20],h[21]!==x?(c=(0,j.jsx)("button",{"aria-label":"Open in editor","data-with-open-in-editor-link-source-file":!0,onClick:x,children:s}),h[21]=x,h[22]=c):c=h[22],h[23]!==c||h[24]!==o||h[25]!==l?(u=(0,j.jsx)("div",{className:"code-frame-header",children:(0,j.jsxs)("p",{className:"code-frame-link",children:[o,l,c]})}),h[23]=c,h[24]=o,h[25]=l,h[26]=u):u=h[26],h[27]!==v?(d=v.map(e0),h[27]=v,h[28]=d):d=h[28],h[29]!==d?(f=(0,j.jsx)("pre",{className:"code-frame-pre",children:(0,j.jsx)("div",{className:"code-frame-lines",children:d})}),h[29]=d,h[30]=f):f=h[30],h[31]!==u||h[32]!==f?(p=(0,j.jsxs)("div",{"data-nextjs-codeframe":!0,children:[u,f]}),h[31]=u,h[32]=f,h[33]=p):p=h[33],p}function e0(e,t){let{line:r,parsedLine:n}=e,{lineNumber:o,isErroredLine:a}=n,i={};return o&&(i["data-nextjs-codeframe-line"]=o),a&&(i["data-nextjs-codeframe-line--errored"]=!0),(0,j.jsx)("div",{...i,children:r.map(e1)},`line-${t}`)}function e1(e,t){return(0,j.jsx)("span",{style:{color:e.fg?`var(--color-${e.fg})`:void 0,..."bold"===e.decoration?{fontWeight:500}:"italic"===e.decoration?{fontStyle:"italic"}:void 0},children:e.content},`frame-${t}`)}let e2=`
  [data-nextjs-codeframe] {
    --code-frame-padding: 12px;
    --code-frame-line-height: var(--size-16);
    background-color: var(--color-background-200);
    color: var(--color-gray-1000);
    text-overflow: ellipsis;
    border: 1px solid var(--color-gray-400);
    border-radius: 8px;
    font-family: var(--font-stack-monospace);
    font-size: var(--size-12);
    line-height: var(--code-frame-line-height);
    margin: 8px 0;

    svg {
      width: var(--size-16);
      height: var(--size-16);
    }
  }

  .code-frame-link,
  .code-frame-pre {
    padding: var(--code-frame-padding);
  }

  .code-frame-link svg {
    flex-shrink: 0;
  }

  .code-frame-lines {
    min-width: max-content;
  }

  .code-frame-link [data-text] {
    text-align: left;
    margin: auto 6px;
  }

  .code-frame-header {
    width: 100%;
    transition: background 100ms ease-out;
    border-radius: 8px 8px 0 0;
    border-bottom: 1px solid var(--color-gray-400);
  }

  [data-with-open-in-editor-link-source-file] {
    padding: 4px;
    margin: -4px 0 -4px auto;
    border-radius: var(--rounded-full);
    margin-left: auto;

    &:focus-visible {
      outline: var(--focus-ring);
      outline-offset: -2px;
    }

    &:hover {
      background: var(--color-gray-100);
    }
  }

  [data-nextjs-codeframe]::selection,
  [data-nextjs-codeframe] *::selection {
    background-color: var(--color-ansi-selection);
  }

  [data-nextjs-codeframe] *:not(a) {
    color: inherit;
    background-color: transparent;
    font-family: var(--font-stack-monospace);
  }

  [data-nextjs-codeframe-line][data-nextjs-codeframe-line--errored="true"] {
    position: relative;
    isolation: isolate;

    > span { 
      position: relative;
      z-index: 1;
    }

    &::after {
      content: "";
      width: calc(100% + var(--code-frame-padding) * 2);
      height: var(--code-frame-line-height);
      left: calc(-1 * var(--code-frame-padding));
      background: var(--color-red-200);
      box-shadow: 2px 0 0 0 var(--color-red-900) inset;
      position: absolute;
    }
  }


  [data-nextjs-codeframe] > * {
    margin: 0;
  }

  .code-frame-link {
    display: flex;
    margin: 0;
    outline: 0;
  }
  .code-frame-link [data-icon='right'] {
    margin-left: auto;
  }

  [data-nextjs-codeframe] div > pre {
    overflow: hidden;
    display: inline-block;
  }

  [data-nextjs-codeframe] svg {
    color: var(--color-gray-900);
  }
`,e3=function(e){let t,r,n,o,a=(0,S.c)(8);return a[0]!==e?({children:t,className:r,...n}=e,a[0]=e,a[1]=t,a[2]=r,a[3]=n):(t=a[1],r=a[2],n=a[3]),a[4]!==t||a[5]!==r||a[6]!==n?(o=(0,j.jsx)("div",{"data-nextjs-dialog-body":!0,className:r,...n,children:t}),a[4]=t,a[5]=r,a[6]=n,a[7]=o):o=a[7],o},e4=function(e){let t,r,n,o,a=(0,S.c)(8);return a[0]!==e?({children:t,className:r,...n}=e,a[0]=e,a[1]=t,a[2]=r,a[3]=n):(t=a[1],r=a[2],n=a[3]),a[4]!==t||a[5]!==r||a[6]!==n?(o=(0,j.jsx)("div",{"data-nextjs-dialog-content":!0,className:r,...n,children:t}),a[4]=t,a[5]=r,a[6]=n,a[7]=o):o=a[7],o},e5=e_`
  [data-nextjs-dialog-root] {
    --next-dialog-radius: var(--rounded-xl);
    --next-dialog-max-width: 960px;
    --next-dialog-row-padding: 16px;
    --next-dialog-padding: 12px;
    --next-dialog-notch-height: 42px;
    --next-dialog-border-width: 1px;

    display: flex;
    flex-direction: column;
    width: 100%;
    max-height: calc(100% - 56px);
    max-width: var(--next-dialog-max-width);
    margin-right: auto;
    margin-left: auto;
    scale: 0.97;
    opacity: 0;
    transition-property: scale, opacity;
    transition-duration: var(--transition-duration);
    transition-timing-function: var(--timing-overlay);

    &[data-rendered='true'] {
      opacity: 1;
      scale: 1;
    }

    [data-nextjs-scroll-fader][data-side='top'] {
      left: 1px;
      top: calc(
        var(--next-dialog-notch-height) + var(--next-dialog-border-width)
      );
      width: calc(100% - var(--next-dialog-padding));
      opacity: 0;
    }
  }

  [data-nextjs-dialog] {
    outline: 0;
  }

  [data-nextjs-dialog-backdrop] {
    opacity: 0;
    transition: opacity var(--transition-duration) var(--timing-overlay);
  }

  [data-nextjs-dialog-overlay] {
    margin: 8px;
  }

  [data-nextjs-dialog-overlay][data-rendered='true']
    [data-nextjs-dialog-backdrop] {
    opacity: 1;
  }

  [data-nextjs-dialog-content] {
    border: none;
    margin: 0;
    display: flex;
    flex-direction: column;
    position: relative;
    padding: var(--next-dialog-padding);
  }

  [data-nextjs-dialog-content] > [data-nextjs-dialog-header] {
    flex-shrink: 0;
    margin-bottom: 8px;
  }

  [data-nextjs-dialog-content] > [data-nextjs-dialog-body] {
    position: relative;
    flex: 1 1 auto;
  }

  @media (max-height: 812px) {
    [data-nextjs-dialog-overlay] {
      max-height: calc(100% - 15px);
    }
  }

  @media (min-width: 576px) {
    [data-nextjs-dialog-root] {
      --next-dialog-max-width: 540px;
    }
  }

  @media (min-width: 768px) {
    [data-nextjs-dialog-root] {
      --next-dialog-max-width: 720px;
    }
  }

  @media (min-width: 992px) {
    [data-nextjs-dialog-root] {
      --next-dialog-max-width: 960px;
    }
  }
`;function e6(...e){return e.filter(Boolean).join(" ")}function e9(e){return navigator.clipboard.writeText(e).then(e7,e8)}function e8(e){return{state:"error",error:e}}function e7(){return{state:"success"}}function te(e){let t,r,n,o,a,i,l,s,c,u,d,f,p,h,m,g,v=(0,S.c)(39);v[0]!==e?({content:r,getContent:o,actionLabel:t,successLabel:l,icon:a,disabled:n,...i}=e,v[0]=e,v[1]=t,v[2]=r,v[3]=n,v[4]=o,v[5]=a,v[6]=i,v[7]=l):(t=v[1],r=v[2],n=v[3],o=v[4],a=v[5],i=v[6],l=v[7]),v[8]!==r||v[9]!==o?(s=()=>r?Promise.resolve(r):o?o():Promise.resolve(""),v[8]=r,v[9]=o,v[10]=s):s=v[10];let[y,b,x,_]=function(e){let t,r,n,o,a,i=(0,S.c)(8);i[0]!==e?(t=(t,r)=>"reset"===r?{state:"initial"}:"copy"===r?navigator.clipboard?e().then(e9):{state:"error",error:"Copy to clipboard is not supported in this browser"}:t,i[0]=e,i[1]=t):t=i[1],i[2]===Symbol.for("react.memo_cache_sentinel")?(r={state:"initial"},i[2]=r):r=i[2];let[l,s,c]=C.useActionState(t,r);i[3]===Symbol.for("react.memo_cache_sentinel")?(n=function(){C.startTransition(()=>{s("copy")})},i[3]=n):n=i[3];let u=n;i[4]===Symbol.for("react.memo_cache_sentinel")?(o=()=>{s("reset")},i[4]=o):o=i[4];let d=o;return i[5]!==l||i[6]!==c?(a=[l,u,d,c],i[5]=l,i[6]=c,i[7]=a):a=i[7],a}(s),w="error"===y.state?y.error:null;v[11]!==w?(c=()=>{null!==w&&console.warn(w)},u=[w],v[11]=w,v[12]=c,v[13]=u):(c=v[12],u=v[13]),C.useEffect(c,u),v[14]!==y.state||v[15]!==x?(d=()=>{if("success"===y.state){let e=setTimeout(()=>{x()},2e3);return()=>{clearTimeout(e)}}},v[14]=y.state,v[15]=x,v[16]=d):d=v[16],v[17]!==y.state||v[18]!==_||v[19]!==x?(f=[_,y.state,x],v[17]=y.state,v[18]=_,v[19]=x,v[20]=f):f=v[20],C.useEffect(d,f);let k=!navigator.clipboard||_||n||!!w,E="success"===y.state?l:t;v[21]!==y.state||v[22]!==a?(p="success"===y.state?(0,j.jsx)(tr,{}):a||(0,j.jsx)(tt,{width:14,height:14,className:"error-overlay-toolbar-button-icon"}),v[21]=y.state,v[22]=a,v[23]=p):p=v[23];let T=p,N=`nextjs-data-copy-button--${y.state}`;v[24]!==e.className||v[25]!==N?(h=e6(e.className,"nextjs-data-copy-button",N),v[24]=e.className,v[25]=N,v[26]=h):h=v[26],v[27]!==b||v[28]!==k?(m=()=>{k||b()},v[27]=b,v[28]=k,v[29]=m):m=v[29];let L="error"===y.state?` ${y.error}`:null;return v[30]!==k||v[31]!==_||v[32]!==E||v[33]!==T||v[34]!==i||v[35]!==h||v[36]!==m||v[37]!==L?(g=(0,j.jsxs)("button",{...i,type:"button",title:E,"aria-label":E,"aria-disabled":k,"data-nextjs-copy-button":!0,"data-pending":_,className:h,onClick:m,children:[T,L]}),v[30]=k,v[31]=_,v[32]=E,v[33]=T,v[34]=i,v[35]=h,v[36]=m,v[37]=L,v[38]=g):g=v[38],g}function tt(e){let t,r,n=(0,S.c)(3);return n[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M2.406.438c-.845 0-1.531.685-1.531 1.53v6.563c0 .846.686 1.531 1.531 1.531H3.937V8.75H2.406a.219.219 0 0 1-.219-.219V1.97c0-.121.098-.219.22-.219h4.812c.12 0 .218.098.218.219v.656H8.75v-.656c0-.846-.686-1.532-1.531-1.532H2.406zm4.375 3.5c-.845 0-1.531.685-1.531 1.53v6.563c0 .846.686 1.531 1.531 1.531h4.813c.845 0 1.531-.685 1.531-1.53V5.468c0-.846-.686-1.532-1.531-1.532H6.78zm-.218 1.53c0-.12.097-.218.218-.218h4.813c.12 0 .219.098.219.219v6.562c0 .121-.098.219-.22.219H6.782a.219.219 0 0 1-.218-.219V5.47z",fill:"currentColor"}),n[0]=t):t=n[0],n[1]!==e?(r=(0,j.jsx)("svg",{width:"14",height:"14",viewBox:"0 0 14 14",fill:"none",xmlns:"http://www.w3.org/2000/svg",...e,children:t}),n[1]=e,n[2]=r):r=n[2],r}function tr(){let e,t=(0,S.c)(1);return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("svg",{height:"16",xlinkTitle:"copied",viewBox:"0 0 16 16",width:"16",stroke:"currentColor",fill:"currentColor",children:(0,j.jsx)("path",{d:"M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"})}),t[0]=e):e=t[0],e}let tn=`
  .nextjs-data-copy-button {
    color: inherit;

    svg {
      width: var(--size-16);
      height: var(--size-16);
    }
  }
  .nextjs-data-copy-button[aria-disabled="true"] {
    background-color: var(--color-gray-100);
    cursor: not-allowed;
  }
  .nextjs-data-copy-button[data-pending="true"] {
    cursor: wait;
  }
  .nextjs-data-copy-button--initial:hover:not([aria-disabled="true"]) {
    cursor: pointer;
  }
  .nextjs-data-copy-button--error:not([aria-disabled="true"]),
  .nextjs-data-copy-button--error:hover:not([aria-disabled="true"]) {
    color: var(--color-ansi-red);
  }
  .nextjs-data-copy-button--success:not([aria-disabled="true"]) {
    color: var(--color-ansi-green);
  }
`;function to(e){let t,r,n,o,a,i,l,s,c,u,d,f,p,h=(0,S.c)(14);return h[0]===Symbol.for("react.memo_cache_sentinel")?(t={maskType:"luminance"},h[0]=t):t=h[0],h[1]===Symbol.for("react.memo_cache_sentinel")?(r=(0,j.jsx)("mask",{id:"nodejs_icon_mask_a",style:t,maskUnits:"userSpaceOnUse",x:"0",y:"0",width:"14",height:"14",children:(0,j.jsx)("path",{d:"M6.67.089 1.205 3.256a.663.663 0 0 0-.33.573v6.339c0 .237.126.455.33.574l5.466 3.17a.66.66 0 0 0 .66 0l5.465-3.17a.664.664 0 0 0 .329-.574V3.829a.663.663 0 0 0-.33-.573L7.33.089a.663.663 0 0 0-.661 0",fill:"#fff"})}),h[1]=r):r=h[1],h[2]===Symbol.for("react.memo_cache_sentinel")?(n=(0,j.jsx)("g",{mask:"url(#nodejs_icon_mask_a)",children:(0,j.jsx)("path",{d:"M18.648 2.717 3.248-4.86-4.648 11.31l15.4 7.58 7.896-16.174z",fill:"url(#nodejs_icon_linear_gradient_b)"})}),h[2]=n):n=h[2],h[3]===Symbol.for("react.memo_cache_sentinel")?(o={maskType:"luminance"},h[3]=o):o=h[3],h[4]===Symbol.for("react.memo_cache_sentinel")?(a=(0,j.jsx)("mask",{id:"nodejs_icon_mask_c",style:o,maskUnits:"userSpaceOnUse",x:"1",y:"0",width:"12",height:"14",children:(0,j.jsx)("path",{d:"M1.01 10.57a.663.663 0 0 0 .195.17l4.688 2.72.781.45a.66.66 0 0 0 .51.063l5.764-10.597a.653.653 0 0 0-.153-.122L9.216 1.18 7.325.087a.688.688 0 0 0-.171-.07L1.01 10.57z",fill:"#fff"})}),h[4]=a):a=h[4],h[5]===Symbol.for("react.memo_cache_sentinel")?(i=(0,j.jsx)("g",{mask:"url(#nodejs_icon_mask_c)",children:(0,j.jsx)("path",{d:"M-5.647 4.958 5.226 19.734l14.38-10.667L8.734-5.71-5.647 4.958z",fill:"url(#nodejs_icon_linear_gradient_d)"})}),h[5]=i):i=h[5],h[6]===Symbol.for("react.memo_cache_sentinel")?(l={maskType:"luminance"},h[6]=l):l=h[6],h[7]===Symbol.for("react.memo_cache_sentinel")?(s=(0,j.jsx)("mask",{id:"nodejs_icon_mask_e",style:l,maskUnits:"userSpaceOnUse",x:"1",y:"0",width:"13",height:"14",children:(0,j.jsx)("path",{d:"M6.934.004A.665.665 0 0 0 6.67.09L1.22 3.247l5.877 10.746a.655.655 0 0 0 .235-.08l5.465-3.17a.665.665 0 0 0 .319-.453L7.126.015a.684.684 0 0 0-.189-.01",fill:"#fff"})}),h[7]=s):s=h[7],h[8]===Symbol.for("react.memo_cache_sentinel")?(c=(0,j.jsxs)("g",{children:[s,(0,j.jsx)("g",{mask:"url(#nodejs_icon_mask_e)",children:(0,j.jsx)("path",{d:"M1.22.002v13.992h11.894V.002H1.22z",fill:"url(#nodejs_icon_linear_gradient_f)"})})]}),h[8]=c):c=h[8],h[9]===Symbol.for("react.memo_cache_sentinel")?(u=(0,j.jsxs)("linearGradient",{id:"nodejs_icon_linear_gradient_b",x1:"10.943",y1:"-1.084",x2:"2.997",y2:"15.062",gradientUnits:"userSpaceOnUse",children:[(0,j.jsx)("stop",{offset:".3",stopColor:"#3E863D"}),(0,j.jsx)("stop",{offset:".5",stopColor:"#55934F"}),(0,j.jsx)("stop",{offset:".8",stopColor:"#5AAD45"})]}),h[9]=u):u=h[9],h[10]===Symbol.for("react.memo_cache_sentinel")?(d=(0,j.jsxs)("linearGradient",{id:"nodejs_icon_linear_gradient_d",x1:"-.145",y1:"12.431",x2:"14.277",y2:"1.818",gradientUnits:"userSpaceOnUse",children:[(0,j.jsx)("stop",{offset:".57",stopColor:"#3E863D"}),(0,j.jsx)("stop",{offset:".72",stopColor:"#619857"}),(0,j.jsx)("stop",{offset:"1",stopColor:"#76AC64"})]}),h[10]=d):d=h[10],h[11]===Symbol.for("react.memo_cache_sentinel")?(f=(0,j.jsxs)("defs",{children:[u,d,(0,j.jsxs)("linearGradient",{id:"nodejs_icon_linear_gradient_f",x1:"1.225",y1:"6.998",x2:"13.116",y2:"6.998",gradientUnits:"userSpaceOnUse",children:[(0,j.jsx)("stop",{offset:".16",stopColor:"#6BBF47"}),(0,j.jsx)("stop",{offset:".38",stopColor:"#79B461"}),(0,j.jsx)("stop",{offset:".47",stopColor:"#75AC64"}),(0,j.jsx)("stop",{offset:".7",stopColor:"#659E5A"}),(0,j.jsx)("stop",{offset:".9",stopColor:"#3E863D"})]})]}),h[11]=f):f=h[11],h[12]!==e?(p=(0,j.jsxs)("svg",{width:"14",height:"14",viewBox:"0 0 14 14",fill:"none",xmlns:"http://www.w3.org/2000/svg",...e,children:[r,n,a,i,c,f]}),h[12]=e,h[13]=p):p=h[13],p}function ta(e){let t,r,n,o,a,i,l,s,c,u,d,f,p,h=(0,S.c)(14);return h[0]===Symbol.for("react.memo_cache_sentinel")?(t={maskType:"luminance"},h[0]=t):t=h[0],h[1]===Symbol.for("react.memo_cache_sentinel")?(r=(0,j.jsx)("mask",{id:"nodejs_icon_mask_a",style:t,maskUnits:"userSpaceOnUse",x:"0",y:"0",width:"14",height:"14",children:(0,j.jsx)("path",{d:"M6.67.089 1.205 3.256a.663.663 0 0 0-.33.573v6.339c0 .237.126.455.33.574l5.466 3.17a.66.66 0 0 0 .66 0l5.465-3.17a.664.664 0 0 0 .329-.574V3.829a.663.663 0 0 0-.33-.573L7.33.089a.663.663 0 0 0-.661 0",fill:"#fff"})}),h[1]=r):r=h[1],h[2]===Symbol.for("react.memo_cache_sentinel")?(n=(0,j.jsx)("g",{mask:"url(#nodejs_icon_mask_a)",children:(0,j.jsx)("path",{d:"M18.648 2.717 3.248-4.86-4.646 11.31l15.399 7.58 7.896-16.174z",fill:"url(#nodejs_icon_linear_gradient_b)"})}),h[2]=n):n=h[2],h[3]===Symbol.for("react.memo_cache_sentinel")?(o={maskType:"luminance"},h[3]=o):o=h[3],h[4]===Symbol.for("react.memo_cache_sentinel")?(a=(0,j.jsx)("mask",{id:"nodejs_icon_mask_c",style:o,maskUnits:"userSpaceOnUse",x:"1",y:"0",width:"12",height:"15",children:(0,j.jsx)("path",{d:"M1.01 10.571a.66.66 0 0 0 .195.172l4.688 2.718.781.451a.66.66 0 0 0 .51.063l5.764-10.597a.653.653 0 0 0-.153-.122L9.216 1.181 7.325.09a.688.688 0 0 0-.171-.07L1.01 10.572z",fill:"#fff"})}),h[4]=a):a=h[4],h[5]===Symbol.for("react.memo_cache_sentinel")?(i=(0,j.jsx)("g",{mask:"url(#nodejs_icon_mask_c)",children:(0,j.jsx)("path",{d:"M-5.647 4.96 5.226 19.736 19.606 9.07 8.734-5.707-5.647 4.96z",fill:"url(#nodejs_icon_linear_gradient_d)"})}),h[5]=i):i=h[5],h[6]===Symbol.for("react.memo_cache_sentinel")?(l={maskType:"luminance"},h[6]=l):l=h[6],h[7]===Symbol.for("react.memo_cache_sentinel")?(s=(0,j.jsx)("mask",{id:"nodejs_icon_mask_e",style:l,maskUnits:"userSpaceOnUse",x:"1",y:"0",width:"13",height:"14",children:(0,j.jsx)("path",{d:"M6.935.003a.665.665 0 0 0-.264.085l-5.45 3.158 5.877 10.747a.653.653 0 0 0 .235-.082l5.465-3.17a.665.665 0 0 0 .319-.452L7.127.014a.684.684 0 0 0-.189-.01",fill:"#fff"})}),h[7]=s):s=h[7],h[8]===Symbol.for("react.memo_cache_sentinel")?(c=(0,j.jsxs)("g",{children:[s,(0,j.jsx)("g",{mask:"url(#nodejs_icon_mask_e)",children:(0,j.jsx)("path",{d:"M1.222.001v13.992h11.893V0H1.222z",fill:"url(#nodejs_icon_linear_gradient_f)"})})]}),h[8]=c):c=h[8],h[9]===Symbol.for("react.memo_cache_sentinel")?(u=(0,j.jsxs)("linearGradient",{id:"nodejs_icon_linear_gradient_b",x1:"10.944",y1:"-1.084",x2:"2.997",y2:"15.062",gradientUnits:"userSpaceOnUse",children:[(0,j.jsx)("stop",{offset:".3",stopColor:"#676767"}),(0,j.jsx)("stop",{offset:".5",stopColor:"#858585"}),(0,j.jsx)("stop",{offset:".8",stopColor:"#989A98"})]}),h[9]=u):u=h[9],h[10]===Symbol.for("react.memo_cache_sentinel")?(d=(0,j.jsxs)("linearGradient",{id:"nodejs_icon_linear_gradient_d",x1:"-.145",y1:"12.433",x2:"14.277",y2:"1.819",gradientUnits:"userSpaceOnUse",children:[(0,j.jsx)("stop",{offset:".57",stopColor:"#747474"}),(0,j.jsx)("stop",{offset:".72",stopColor:"#707070"}),(0,j.jsx)("stop",{offset:"1",stopColor:"#929292"})]}),h[10]=d):d=h[10],h[11]===Symbol.for("react.memo_cache_sentinel")?(f=(0,j.jsxs)("defs",{children:[u,d,(0,j.jsxs)("linearGradient",{id:"nodejs_icon_linear_gradient_f",x1:"1.226",y1:"6.997",x2:"13.117",y2:"6.997",gradientUnits:"userSpaceOnUse",children:[(0,j.jsx)("stop",{offset:".16",stopColor:"#878787"}),(0,j.jsx)("stop",{offset:".38",stopColor:"#A9A9A9"}),(0,j.jsx)("stop",{offset:".47",stopColor:"#A5A5A5"}),(0,j.jsx)("stop",{offset:".7",stopColor:"#8F8F8F"}),(0,j.jsx)("stop",{offset:".9",stopColor:"#626262"})]})]}),h[11]=f):f=h[11],h[12]!==e?(p=(0,j.jsxs)("svg",{width:"14",height:"14",viewBox:"0 0 14 14",fill:"none",xmlns:"http://www.w3.org/2000/svg",...e,children:[r,n,a,i,c,f]}),h[12]=e,h[13]=p):p=h[13],p}function ti({defaultDevtoolsFrontendUrl:e}){let[t,r,n]=(0,C.useActionState)(async()=>{try{let e=await fetch("/__nextjs_attach-nodejs-inspector",{method:"POST"});if(!e.ok)throw Error(`${e.status} ${e.statusText}: ${await e.text()}`);let t=await e.json();return{status:"fulfilled",value:t}}catch(e){return{status:"rejected",reason:Error("Failed to attach Node.js inspector: "+String(e))}}},{status:"fulfilled",value:e}),o="fulfilled"===t.status?t.value:void 0;(0,C.useEffect)(()=>{"rejected"===t.status&&console.error(t.reason)},[t]);let a=C.startTransition.bind(null,r);return void 0===o?(0,j.jsx)("button",{className:"nodejs-inspector-button","data-pending":n,onClick:n?void 0:a,title:"rejected"===t.status?"Retry attaching Node.js inspector":"Attach Node.js inspector",children:(0,j.jsx)(ta,{className:"error-overlay-toolbar-button-icon",width:14,height:14})}):(0,j.jsx)(te,{"data-nextjs-data-runtime-error-copy-devtools-url":!0,className:"nodejs-inspector-button",actionLabel:"Copy DevTools URL for Chrome",successLabel:"Copied",content:o,icon:(0,j.jsx)(to,{className:"error-overlay-toolbar-button-icon",width:14,height:14})})}function tl(e){let t,r=(0,S.c)(3),{error:n,generateErrorInfo:o}=e,a=!n;return r[0]!==o||r[1]!==a?(t=(0,j.jsx)(te,{"data-nextjs-data-runtime-error-copy-stack":!0,className:"copy-error-button",actionLabel:"Copy Error Info",successLabel:"Error Info Copied",getContent:o,disabled:a}),r[0]=o,r[1]=a,r[2]=t):t=r[2],t}let ts="https://react.dev/link/hydration-mismatch",tc="https://nextjs.org/docs/messages/react-hydration-error",tu=[/^In HTML, (.+?) cannot be a child of <(.+?)>\.(.*)\nThis will cause a hydration error\.(.*)/,/^In HTML, (.+?) cannot be a descendant of <(.+?)>\.\nThis will cause a hydration error\.(.*)/,/^In HTML, text nodes cannot be a child of <(.+?)>\.\nThis will cause a hydration error\./,/^In HTML, whitespace text nodes cannot be a child of <(.+?)>\. Make sure you don't have any extra whitespace between tags on each line of your source code\.\nThis will cause a hydration error\./];function td(e){return tu.some(t=>t.test(e))}let tf=["https://nextjs.org","https://react.dev"];function tp(e){return tf.some(t=>e.startsWith(t))}function th(e){let t,r,n,o=(0,S.c)(6),{errorMessage:a}=e;o[0]!==a?(t=function(e){var t,r;let n,o=(t=e,r=tp,n=Array.from(t.matchAll(/https?:\/\/[^\s/$.?#].[^\s)'"]*/gi),e=>e[0]),r?n.filter(e=>r(e)):n);if(0===o.length)return null;let a=o[0];return a===ts?tc:a}(a),o[0]=a,o[1]=t):t=o[1];let i=t;if(!i){let e;return o[2]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("button",{title:"No related documentation found","aria-label":"No related documentation found",className:"docs-link-button",disabled:!0,children:(0,j.jsx)(tm,{className:"error-overlay-toolbar-button-icon",width:14,height:14})}),o[2]=e):e=o[2],e}return o[3]===Symbol.for("react.memo_cache_sentinel")?(r=(0,j.jsx)(tm,{className:"error-overlay-toolbar-button-icon",width:14,height:14}),o[3]=r):r=o[3],o[4]!==i?(n=(0,j.jsx)("a",{title:"Go to related documentation","aria-label":"Go to related documentation",className:"docs-link-button",href:i,target:"_blank",rel:"noopener noreferrer",children:r}),o[4]=i,o[5]=n):n=o[5],n}function tm(e){let t,r,n=(0,S.c)(3);return n[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M0 .875h4.375C5.448.875 6.401 1.39 7 2.187A3.276 3.276 0 0 1 9.625.875H14v11.156H9.4c-.522 0-1.023.208-1.392.577l-.544.543h-.928l-.544-.543c-.369-.37-.87-.577-1.392-.577H0V.875zm6.344 3.281a1.969 1.969 0 0 0-1.969-1.968H1.312v8.53H4.6c.622 0 1.225.177 1.744.502V4.156zm1.312 7.064V4.156c0-1.087.882-1.968 1.969-1.968h3.063v8.53H9.4c-.622 0-1.225.177-1.744.502z",fill:"currentColor"}),n[0]=t):t=n[0],n[1]!==e?(r=(0,j.jsx)("svg",{width:"14",height:"14",viewBox:"0 0 14 14",fill:"none",xmlns:"http://www.w3.org/2000/svg",...e,children:t}),n[1]=e,n[2]=r):r=n[2],r}function tg(e){let t,r,n,o,a=(0,S.c)(13),{error:i,debugInfo:l,feedbackButton:s,generateErrorInfo:c}=e;a[0]!==i||a[1]!==c?(t=(0,j.jsx)(tl,{error:i,generateErrorInfo:c}),a[0]=i,a[1]=c,a[2]=t):t=a[2],a[3]!==i.message?(r=(0,j.jsx)(th,{errorMessage:i.message}),a[3]=i.message,a[4]=r):r=a[4];let u=l?.devtoolsFrontendUrl,d=l?.devtoolsFrontendUrl;return a[5]!==u||a[6]!==d?(n=(0,j.jsx)(ti,{defaultDevtoolsFrontendUrl:d},u),a[5]=u,a[6]=d,a[7]=n):n=a[7],a[8]!==s||a[9]!==t||a[10]!==r||a[11]!==n?(o=(0,j.jsxs)("span",{className:"error-overlay-toolbar",children:[s,t,r,n]}),a[8]=s,a[9]=t,a[10]=r,a[11]=n,a[12]=o):o=a[12],o}let tv=`
  .error-overlay-toolbar {
    display: flex;
    gap: 6px;
  }

  .nodejs-inspector-button,
  .copy-error-button,
  .docs-link-button {
    display: flex;
    justify-content: center;
    align-items: center;

    width: var(--size-28);
    height: var(--size-28);
    background: var(--color-background-100);
    background-clip: padding-box;
    border: 1px solid var(--color-gray-alpha-400);
    box-shadow: var(--shadow-small);
    border-radius: var(--rounded-full);

    svg {
      width: var(--size-14);
      height: var(--size-14);
    }

    &:focus {
      outline: var(--focus-ring);
    }

    &:not(:disabled):hover {
      background: var(--color-gray-alpha-100);
    }

    &:not(:disabled):active {
      background: var(--color-gray-alpha-200);
    }

    &:disabled {
      background-color: var(--color-gray-100);
      cursor: not-allowed;
    }
  }

  .nodejs-inspector-button[data-pending='true'] {
    cursor: wait;
  }

  .error-overlay-toolbar-button-icon {
    color: var(--color-gray-900);
  }
`;function ty(e){let t,r,n=(0,S.c)(3);return n[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("g",{id:"thumb-up-16",children:(0,j.jsx)("path",{id:"Union",fillRule:"evenodd",clipRule:"evenodd",d:"M6.89531 2.23959C6.72984 2.1214 6.5 2.23968 6.5 2.44303V5.24989C6.5 6.21639 5.7165 6.99989 4.75 6.99989H2.5V13.4999H12.1884C12.762 13.4999 13.262 13.1095 13.4011 12.5531L14.4011 8.55306C14.5984 7.76412 14.0017 6.99989 13.1884 6.99989H9.25H8.5V6.24989V3.51446C8.5 3.43372 8.46101 3.35795 8.39531 3.31102L6.89531 2.23959ZM5 2.44303C5 1.01963 6.6089 0.191656 7.76717 1.01899L9.26717 2.09042C9.72706 2.41892 10 2.94929 10 3.51446V5.49989H13.1884C14.9775 5.49989 16.2903 7.18121 15.8563 8.91686L14.8563 12.9169C14.5503 14.1411 13.4503 14.9999 12.1884 14.9999H1.75H1V14.2499V6.24989V5.49989H1.75H4.75C4.88807 5.49989 5 5.38796 5 5.24989V2.44303Z",fill:"currentColor"})}),n[0]=t):t=n[0],n[1]!==e?(r=(0,j.jsx)("svg",{width:"16",height:"16",viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg",className:"thumbs-up-icon",...e,children:t}),n[1]=e,n[2]=r):r=n[2],r}function tb(e){let t,r,n=(0,S.c)(3);return n[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M5.89531 12.7603C5.72984 12.8785 5.5 12.7602 5.5 12.5569V9.75C5.5 8.7835 4.7165 8 3.75 8H1.5V1.5H11.1884C11.762 1.5 12.262 1.89037 12.4011 2.44683L13.4011 6.44683C13.5984 7.23576 13.0017 8 12.1884 8H8.25H7.5V8.75V11.4854C7.5 11.5662 7.46101 11.6419 7.39531 11.6889L5.89531 12.7603ZM4 12.5569C4 13.9803 5.6089 14.8082 6.76717 13.9809L8.26717 12.9095C8.72706 12.581 9 12.0506 9 11.4854V9.5H12.1884C13.9775 9.5 15.2903 7.81868 14.8563 6.08303L13.8563 2.08303C13.5503 0.858816 12.4503 0 11.1884 0H0.75H0V0.75V8.75V9.5H0.75H3.75C3.88807 9.5 4 9.61193 4 9.75V12.5569Z",fill:"currentColor"}),n[0]=t):t=n[0],n[1]!==e?(r=(0,j.jsx)("svg",{width:"16",height:"16",viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg",className:"thumbs-down-icon",...e,children:t}),n[1]=e,n[2]=r):r=n[2],r}function tx(e){let t,r,n,o,a,i=(0,S.c)(12),{errorCode:l,className:s}=e;i[0]===Symbol.for("react.memo_cache_sentinel")?(t={},i[0]=t):t=i[0];let[c,u]=(0,C.useState)(t),d=c[l],f=void 0!==d,p=process.env.__NEXT_TELEMETRY_DISABLED;i[1]!==l?(r=async e=>{u(t=>({...t,[l]:e}));try{(await fetch(`${process.env.__NEXT_ROUTER_BASEPATH||""}/__nextjs_error_feedback?${new URLSearchParams({errorCode:l,wasHelpful:e.toString()})}`)).ok||console.error("Failed to record feedback on the server.")}catch(e){console.error("Failed to record feedback:",e)}},i[1]=l,i[2]=r):r=i[2];let h=r;return i[3]!==s?(n=e6("error-feedback",s),i[3]=s,i[4]=n):n=i[4],i[5]!==h||i[6]!==f||i[7]!==d?(o=f?(0,j.jsx)("p",{className:"error-feedback-thanks",role:"status","aria-live":"polite",children:"Thanks for your feedback!"}):(0,j.jsxs)(j.Fragment,{children:[(0,j.jsx)("p",{children:(0,j.jsx)("a",{href:"https://nextjs.org/telemetry#error-feedback",rel:"noopener noreferrer",target:"_blank",children:"Was this helpful?"})}),(0,j.jsx)("button",{"aria-disabled":p?"true":void 0,"aria-label":"Mark as helpful",onClick:p?void 0:()=>h(!0),className:e6("feedback-button",!0===d&&"voted"),title:p?"Feedback disabled due to setting NEXT_TELEMETRY_DISABLED":void 0,type:"button",children:(0,j.jsx)(ty,{"aria-hidden":"true"})}),(0,j.jsx)("button",{"aria-disabled":p?"true":void 0,"aria-label":"Mark as not helpful",onClick:p?void 0:()=>h(!1),className:e6("feedback-button",!1===d&&"voted"),title:p?"Feedback disabled due to setting NEXT_TELEMETRY_DISABLED":void 0,type:"button",children:(0,j.jsx)(tb,{"aria-hidden":"true",style:{translate:"1px 1px"}})})]}),i[5]=h,i[6]=f,i[7]=d,i[8]=o):o=i[8],i[9]!==n||i[10]!==o?(a=(0,j.jsx)("div",{className:n,role:"region","aria-label":"Error feedback",children:o}),i[9]=n,i[10]=o,i[11]=a):a=i[11],a}let t_=`
  .error-feedback {
    display: flex;
    align-items: center;
    gap: 8px;
    white-space: nowrap;
    color: var(--color-gray-900);
  }

  .error-feedback-thanks {
    height: var(--size-24);
    display: flex;
    align-items: center;
    padding-right: 4px; /* To match the 4px inner padding of the thumbs up and down icons */
  }

  .feedback-button {
    background: none;
    border: none;
    border-radius: var(--rounded-md);
    width: var(--size-24);
    height: var(--size-24);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;

    &:focus {
      outline: var(--focus-ring);
    }

    &:hover {
      background: var(--color-gray-alpha-100);
    }

    &:active {
      background: var(--color-gray-alpha-200);
    }
  }

  .feedback-button[aria-disabled='true'] {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .feedback-button.voted {
    background: var(--color-gray-alpha-200);
  }

  .thumbs-up-icon,
  .thumbs-down-icon {
    color: var(--color-gray-900);
    width: var(--size-16);
    height: var(--size-16);
  }
`;function tw(e){let t,r,n=(0,S.c)(4),{errorCode:o}=e;return n[0]!==o?(t=o?(0,j.jsx)(tx,{className:"error-feedback",errorCode:o}):null,n[0]=o,n[1]=t):t=n[1],n[2]!==t?(r=(0,j.jsx)("footer",{"data-nextjs-error-overlay-footer":!0,className:"error-overlay-footer",children:t}),n[2]=t,n[3]=r):r=n[3],r}let tk=`
  .error-overlay-footer {
    display: flex;
    flex-direction: row;
    justify-content: space-between;

    gap: 8px;
    padding: 12px;
    background: var(--color-background-200);
    border-top: 1px solid var(--color-gray-400);
  }

  .error-feedback {
    margin-left: auto;

    p {
      font-size: var(--size-14);
      font-weight: 500;
      margin: 0;
    }
  }

  ${t_}
`;function tj(e){let t,r,n,o,a,i=(0,S.c)(12),{errorMessage:l,errorType:s}=e,[c,u]=(0,C.useState)(!1),[d,f]=(0,C.useState)(!1),p=(0,C.useRef)(null);if(i[0]===Symbol.for("react.memo_cache_sentinel")?(t=()=>{p.current&&f(p.current.scrollHeight>200)},i[0]=t):t=i[0],i[1]!==l?(r=[l],i[1]=l,i[2]=r):r=i[2],(0,C.useLayoutEffect)(t,r),!l)return null;let h=d&&"Blocking Route"!==s,m=`nextjs__container_errors_desc ${h&&!c?"truncated":""}`;return i[3]!==l||i[4]!==m?(n=(0,j.jsx)("div",{ref:p,id:"nextjs__container_errors_desc",className:m,children:l}),i[3]=l,i[4]=m,i[5]=n):n=i[5],i[6]!==c||i[7]!==h?(o=h&&!c&&(0,j.jsxs)(j.Fragment,{children:[(0,j.jsx)("div",{className:"nextjs__container_errors_gradient_overlay"}),(0,j.jsx)("button",{onClick:()=>u(!0),className:"nextjs__container_errors_expand_button","aria-expanded":c,"aria-controls":"nextjs__container_errors_desc",children:"Show More"})]}),i[6]=c,i[7]=h,i[8]=o):o=i[8],i[9]!==n||i[10]!==o?(a=(0,j.jsxs)("div",{className:"nextjs__container_errors_wrapper",children:[n,o]}),i[9]=n,i[10]=o,i[11]=a):a=i[11],a}let tS=`
  .nextjs__container_errors_wrapper {
    position: relative;
  }

  .nextjs__container_errors_desc {
    margin: 0;
    margin-left: 4px;
    color: var(--color-red-900);
    font-weight: 500;
    font-size: var(--size-16);
    letter-spacing: -0.32px;
    line-height: var(--size-24);
    overflow-wrap: break-word;
    white-space: pre-wrap;
  }

  .nextjs__container_errors_desc.truncated {
    max-height: 200px;
    overflow: hidden;
  }

  .nextjs__container_errors_gradient_overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 85px;
    background: linear-gradient(
      180deg,
      rgba(250, 250, 250, 0) 0%,
      var(--color-background-100) 100%
    );
  }

  .nextjs__container_errors_expand_button {
    position: absolute;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    align-items: center;
    padding: 6px 8px;
    background: var(--color-background-100);
    border: 1px solid var(--color-gray-alpha-400);
    border-radius: 999px;
    box-shadow:
      0px 2px 2px var(--color-gray-alpha-100),
      0px 8px 8px -8px var(--color-gray-alpha-100);
    font-size: var(--size-13);
    cursor: pointer;
    color: var(--color-gray-900);
    font-weight: 500;
    transition: background-color 0.2s ease;
  }

  .nextjs__container_errors_expand_button:hover {
    background: var(--color-gray-100);
  }
`;function tC(e){let t,r=(0,S.c)(3),{errorType:n}=e,o=`nextjs__container_errors_label ${"Blocking Route"===n||"Ambiguous Metadata"===n?"nextjs__container_errors_label_blocking_page":""}`;return r[0]!==n||r[1]!==o?(t=(0,j.jsx)("span",{id:"nextjs__container_errors_label",className:o,children:n}),r[0]=n,r[1]=o,r[2]=t):t=r[2],t}let tE=`
  .nextjs__container_errors_label {
    padding: 2px 6px;
    margin: 0;
    border-radius: var(--rounded-md-2);
    background: var(--color-red-100);
    font-weight: 600;
    font-size: var(--size-12);
    color: var(--color-red-900);
    font-family: var(--font-stack-monospace);
    line-height: var(--size-20);
  }

  .nextjs__container_errors_label_blocking_page {
    background: var(--color-blue-100);
    color: var(--color-blue-900);
  }
`;function tT(e){let t,r,n=(0,S.c)(4),{title:o,className:a}=e;return n[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M9.24996 12.0608L8.71963 11.5304L5.89641 8.70722C5.50588 8.3167 5.50588 7.68353 5.89641 7.29301L8.71963 4.46978L9.24996 3.93945L10.3106 5.00011L9.78029 5.53044L7.31062 8.00011L9.78029 10.4698L10.3106 11.0001L9.24996 12.0608Z",fill:"currentColor"}),n[0]=t):t=n[0],n[1]!==a||n[2]!==o?(r=(0,j.jsx)("svg",{width:"16",height:"16",viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg","aria-label":o,className:a,children:t}),n[1]=a,n[2]=o,n[3]=r):r=n[3],r}function tN(e){let t,r,n=(0,S.c)(4),{title:o,className:a}=e;return n[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M6.75011 3.93945L7.28044 4.46978L10.1037 7.29301C10.4942 7.68353 10.4942 8.3167 10.1037 8.70722L7.28044 11.5304L6.75011 12.0608L5.68945 11.0001L6.21978 10.4698L8.68945 8.00011L6.21978 5.53044L5.68945 5.00011L6.75011 3.93945Z",fill:"currentColor"}),n[0]=t):t=n[0],n[1]!==a||n[2]!==o?(r=(0,j.jsx)("svg",{width:"16",height:"16",viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg",className:a,"aria-label":o,children:t}),n[1]=a,n[2]=o,n[3]=r):r=n[3],r}function tL(e){let t,r,n,o,a,i,l,s,c,u,d,f,p,h,m,g=(0,S.c)(40),{runtimeErrors:v,activeIdx:y,onActiveIndexChange:b}=e;g[0]!==y||g[1]!==b?(t=()=>(0,C.startTransition)(()=>{y>0&&b(Math.max(0,y-1))}),g[0]=y,g[1]=b,g[2]=t):t=g[2];let x=t;g[3]!==y||g[4]!==b||g[5]!==v.length?(r=()=>(0,C.startTransition)(()=>{y<v.length-1&&b(Math.max(0,Math.min(v.length-1,y+1)))}),g[3]=y,g[4]=b,g[5]=v.length,g[6]=r):r=g[6];let _=r,w=(0,C.useRef)(null),k=(0,C.useRef)(null),[E,T]=(0,C.useState)(null);g[7]===Symbol.for("react.memo_cache_sentinel")?(n=e=>{T(e)},g[7]=n):n=g[7];let N=n;g[8]!==_||g[9]!==x||g[10]!==E?(o=()=>{if(null==E)return;let e=E.getRootNode(),t=self.document,r=function(e){"ArrowLeft"===e.key?(e.preventDefault(),e.stopPropagation(),x&&x()):"ArrowRight"===e.key&&(e.preventDefault(),e.stopPropagation(),_&&_())};return e.addEventListener("keydown",r),e!==t&&t.addEventListener("keydown",r),function(){e.removeEventListener("keydown",r),e!==t&&t.removeEventListener("keydown",r)}},a=[E,_,x],g[8]=_,g[9]=x,g[10]=E,g[11]=o,g[12]=a):(o=g[11],a=g[12]),(0,C.useEffect)(o,a),g[13]!==y||g[14]!==E||g[15]!==v.length?(i=()=>{if(null==E)return;let e=E.getRootNode();if(e instanceof ShadowRoot){let t=e.activeElement;0===y?w.current&&t===w.current&&w.current.blur():y===v.length-1&&k.current&&t===k.current&&k.current.blur()}},l=[E,y,v.length],g[13]=y,g[14]=E,g[15]=v.length,g[16]=i,g[17]=l):(i=g[16],l=g[17]),(0,C.useEffect)(i,l);let L=0===y,I=0===y;g[18]===Symbol.for("react.memo_cache_sentinel")?(s=(0,j.jsx)(tT,{title:"previous",className:"error-overlay-pagination-button-icon"}),g[18]=s):s=g[18],g[19]!==x||g[20]!==L||g[21]!==I?(c=(0,j.jsx)("button",{ref:w,type:"button",disabled:L,"aria-disabled":I,onClick:x,"data-nextjs-dialog-error-previous":!0,className:"error-overlay-pagination-button",children:s}),g[19]=x,g[20]=L,g[21]=I,g[22]=c):c=g[22];let P=y+1;g[23]!==y||g[24]!==P?(u=(0,j.jsxs)("span",{"data-nextjs-dialog-error-index":y,children:[P,"/"]}),g[23]=y,g[24]=P,g[25]=u):u=g[25];let z=v.length||1;g[26]!==z?(d=(0,j.jsx)("span",{"data-nextjs-dialog-header-total-count":!0,children:z}),g[26]=z,g[27]=d):d=g[27],g[28]!==u||g[29]!==d?(f=(0,j.jsxs)("div",{className:"error-overlay-pagination-count",children:[u,d]}),g[28]=u,g[29]=d,g[30]=f):f=g[30];let R=y>=v.length-1,O=y>=v.length-1;return g[31]===Symbol.for("react.memo_cache_sentinel")?(p=(0,j.jsx)(tN,{title:"next",className:"error-overlay-pagination-button-icon"}),g[31]=p):p=g[31],g[32]!==_||g[33]!==R||g[34]!==O?(h=(0,j.jsx)("button",{ref:k,type:"button",disabled:R,"aria-disabled":O,onClick:_,"data-nextjs-dialog-error-next":!0,className:"error-overlay-pagination-button",children:p}),g[32]=_,g[33]=R,g[34]=O,g[35]=h):h=g[35],g[36]!==c||g[37]!==f||g[38]!==h?(m=(0,j.jsxs)("nav",{className:"error-overlay-pagination dialog-exclude-closing-from-outside-click",ref:N,children:[c,f,h]}),g[36]=c,g[37]=f,g[38]=h,g[39]=m):m=g[39],m}let tI=`
  .error-overlay-pagination {
    -webkit-font-smoothing: antialiased;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    width: fit-content;
  }

  .error-overlay-pagination-count {
    color: var(--color-gray-900);
    text-align: center;
    font-size: var(--size-14);
    font-weight: 500;
    line-height: var(--size-16);
    font-variant-numeric: tabular-nums;
  }

  .error-overlay-pagination-button {
    display: flex;
    justify-content: center;
    align-items: center;

    width: var(--size-24);
    height: var(--size-24);
    background: var(--color-gray-300);
    flex-shrink: 0;

    border: none;
    border-radius: var(--rounded-full);

    svg {
      width: var(--size-16);
      height: var(--size-16);
    }

    &:focus-visible {
      outline: var(--focus-ring);
    }

    &:not(:disabled):active {
      background: var(--color-gray-500);
    }

    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  }

  .error-overlay-pagination-button-icon {
    color: var(--color-gray-1000);
  }
`;function tP(e){let t,r,n=(0,S.c)(3);return n[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("circle",{cx:"7",cy:"7",r:"5.5",strokeWidth:"3"}),n[0]=t):t=n[0],n[1]!==e?(r=(0,j.jsx)("svg",{width:"14",height:"14",viewBox:"0 0 14 14",fill:"none",xmlns:"http://www.w3.org/2000/svg",...e,children:t}),n[1]=e,n[2]=r):r=n[2],r}function tz(e){let t,r,n,o,a,i,l,s,c,u,d,f,p=(0,S.c)(31),{versionInfo:h,bundlerName:m}=e,{staleness:g}=h;if(p[0]!==m||p[1]!==g||p[2]!==h){a=Symbol.for("react.early_return_sentinel");r:{let{text:e,indicatorClass:s,title:c}=function({installed:e,staleness:t,expected:r}){let n="",o="",a="",i=`Next.js ${e}`;switch(t){case"newer-than-npm":case"fresh":n=i,o=`Latest available version is detected (${e}).`,a="fresh";break;case"stale-patch":case"stale-minor":n=`${i} (stale)`,o=`There is a newer version (${r}) available, upgrade recommended! `,a="stale";break;case"stale-major":n=`${i} (outdated)`,o=`An outdated version detected (latest is ${r}), upgrade is highly recommended!`,a="outdated";break;case"stale-prerelease":n=`${i} (stale)`,o=`There is a newer canary version (${r}) available, please upgrade! `,a="stale";break;case"unknown":n=`${i} (unknown)`,o="No Next.js version data was found.",a="unknown"}return{text:n,indicatorClass:a,title:o}}(h);if(i=e,l=c,r="Turbopack"===m,g.startsWith("stale")){let e,t,n=r&&"turbopack-text";p[10]!==n?(e=e6(n),p[10]=n,p[11]=e):e=p[11],p[12]!==m||p[13]!==e?(t=(0,j.jsx)("span",{className:e,children:m}),p[12]=m,p[13]=e,p[14]=t):t=p[14],a=(0,j.jsxs)("a",{className:"nextjs-container-build-error-version-status dialog-exclude-closing-from-outside-click",target:"_blank",rel:"noopener noreferrer",href:"https://nextjs.org/docs/messages/version-staleness",children:[(0,j.jsx)(tP,{className:e6("version-staleness-indicator",s)}),(0,j.jsx)("span",{"data-nextjs-version-checker":!0,title:l,children:i}),t]});break r}o="nextjs-container-build-error-version-status dialog-exclude-closing-from-outside-click",t=tP,n=e6("version-staleness-indicator",s)}p[0]=m,p[1]=g,p[2]=h,p[3]=t,p[4]=r,p[5]=n,p[6]=o,p[7]=a,p[8]=i,p[9]=l}else t=p[3],r=p[4],n=p[5],o=p[6],a=p[7],i=p[8],l=p[9];if(a!==Symbol.for("react.early_return_sentinel"))return a;p[15]!==t||p[16]!==n?(s=(0,j.jsx)(t,{className:n}),p[15]=t,p[16]=n,p[17]=s):s=p[17],p[18]!==i||p[19]!==l?(c=(0,j.jsx)("span",{"data-nextjs-version-checker":!0,title:l,children:i}),p[18]=i,p[19]=l,p[20]=c):c=p[20];let v=r&&"turbopack-text";return p[21]!==v?(u=e6(v),p[21]=v,p[22]=u):u=p[22],p[23]!==m||p[24]!==u?(d=(0,j.jsx)("span",{className:u,children:m}),p[23]=m,p[24]=u,p[25]=d):d=p[25],p[26]!==o||p[27]!==s||p[28]!==c||p[29]!==d?(f=(0,j.jsxs)("span",{className:o,children:[s,c,d]}),p[26]=o,p[27]=s,p[28]=c,p[29]=d,p[30]=f):f=p[30],f}let tR=`
  .nextjs-container-build-error-version-status {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 4px;

    height: var(--size-26);
    padding: 6px 8px 6px 6px;
    background: var(--color-background-100);
    background-clip: padding-box;
    border: 1px solid var(--color-gray-alpha-400);
    box-shadow: var(--shadow-small);
    border-radius: var(--rounded-full);

    color: var(--color-gray-900);
    font-size: var(--size-12);
    font-weight: 500;
    line-height: var(--size-16);
  }

  a.nextjs-container-build-error-version-status {
    text-decoration: none;
    color: var(--color-gray-900);

    &:hover {
      background: var(--color-gray-100);
    }

    &:focus {
      outline: var(--focus-ring);
    }
  }

  .version-staleness-indicator.fresh {
    fill: var(--color-green-800);
    stroke: var(--color-green-300);
  }
  .version-staleness-indicator.stale {
    fill: var(--color-amber-800);
    stroke: var(--color-amber-300);
  }
  .version-staleness-indicator.outdated {
    fill: var(--color-red-800);
    stroke: var(--color-red-300);
  }
  .version-staleness-indicator.unknown {
    fill: var(--color-gray-800);
    stroke: var(--color-gray-300);
  }

  .nextjs-container-build-error-version-status > .turbopack-text {
    background: linear-gradient(
      to right,
      var(--color-turbopack-text-red) 0%,
      var(--color-turbopack-text-blue) 100%
    );
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
`;function tO(e){let t,r,n,o,a=(0,S.c)(11),{runtimeErrors:i,activeIdx:l,setActiveIndex:s,versionInfo:c}=e,u=process.env.__NEXT_BUNDLER||"Turbopack";a[0]!==i?(t=i??[],a[0]=i,a[1]=t):t=a[1];let d=l??0,f=s??tM;return a[2]!==t||a[3]!==d||a[4]!==f?(r=(0,j.jsx)(tD,{side:"left",children:(0,j.jsx)(tL,{runtimeErrors:t,activeIdx:d,onActiveIndexChange:f})}),a[2]=t,a[3]=d,a[4]=f,a[5]=r):r=a[5],a[6]!==c?(n=c&&(0,j.jsx)(tD,{side:"right",children:(0,j.jsx)(tz,{versionInfo:c,bundlerName:u})}),a[6]=c,a[7]=n):n=a[7],a[8]!==r||a[9]!==n?(o=(0,j.jsxs)("div",{"data-nextjs-error-overlay-nav":!0,children:[r,n]}),a[8]=r,a[9]=n,a[10]=o):o=a[10],o}function tM(){}let tA=`
  [data-nextjs-error-overlay-nav] {
    --stroke-color: var(--color-gray-400);
    --background-color: var(--color-background-100);
    display: flex;
    justify-content: space-between;
    align-items: center;

    width: 100%;

    position: relative;
    z-index: 2;
    outline: none;
    translate: var(--next-dialog-border-width) var(--next-dialog-border-width);
    max-width: var(--next-dialog-max-width);

    .error-overlay-notch {
      translate: calc(var(--next-dialog-border-width) * -1);
      width: auto;
      height: var(--next-dialog-notch-height);
      padding: 12px;
      background: var(--background-color);
      border: var(--next-dialog-border-width) solid var(--stroke-color);
      border-bottom: none;
      position: relative;

      &[data-side='left'] {
        padding-right: 0;
        border-radius: var(--next-dialog-radius) 0 0 0;

        .error-overlay-notch-tail {
          right: -54px;
        }

        > *:not(.error-overlay-notch-tail) {
          margin-right: -10px;
        }
      }

      &[data-side='right'] {
        padding-left: 0;
        border-radius: 0 var(--next-dialog-radius) 0 0;

        .error-overlay-notch-tail {
          left: -54px;
          transform: rotateY(180deg);
        }

        > *:not(.error-overlay-notch-tail) {
          margin-left: -12px;
        }
      }

      .error-overlay-notch-tail {
        position: absolute;
        top: calc(var(--next-dialog-border-width) * -1);
        pointer-events: none;
        z-index: -1;
        height: calc(100% + var(--next-dialog-border-width));
      }
    }
  }

  @media (max-width: 600px) {
    [data-nextjs-error-overlay-nav] {
      background: var(--background-color);
      border-radius: var(--next-dialog-radius) var(--next-dialog-radius) 0 0;
      border: var(--next-dialog-border-width) solid var(--stroke-color);
      border-bottom: none;
      overflow: hidden;
      translate: 0 var(--next-dialog-border-width);
      
      .error-overlay-notch {
        border-radius: 0;
        border: 0;

        &[data-side="left"], &[data-side="right"] {
          border-radius: 0;
        }

        .error-overlay-notch-tail {
          display: none;
        }
      }
    }
  }
`;function tD(e){let t,r,n=(0,S.c)(4),{children:o,side:a}=e,i=void 0===a?"left":a;return n[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)(tZ,{}),n[0]=t):t=n[0],n[1]!==o||n[2]!==i?(r=(0,j.jsxs)("div",{className:"error-overlay-notch","data-side":i,children:[o,t]}),n[1]=o,n[2]=i,n[3]=r):r=n[3],r}function tZ(){let e,t,r,n=(0,S.c)(3);return n[0]===Symbol.for("react.memo_cache_sentinel")?(e={maskType:"alpha"},n[0]=e):e=n[0],n[1]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsxs)("mask",{id:"error_overlay_nav_mask0_2667_14687",style:e,maskUnits:"userSpaceOnUse",x:"0",y:"-1",width:"60",height:"43",children:[(0,j.jsxs)("mask",{id:"error_overlay_nav_path_1_outside_1_2667_14687",maskUnits:"userSpaceOnUse",x:"0",y:"-1",width:"60",height:"43",fill:"black",children:[(0,j.jsx)("rect",{fill:"white",y:"-1",width:"60",height:"43"}),(0,j.jsx)("path",{d:"M1 0L8.0783 0C15.772 0 22.7836 4.41324 26.111 11.3501L34.8889 29.6498C38.2164 36.5868 45.228 41 52.9217 41H60H1L1 0Z"})]}),(0,j.jsx)("path",{d:"M1 0L8.0783 0C15.772 0 22.7836 4.41324 26.111 11.3501L34.8889 29.6498C38.2164 36.5868 45.228 41 52.9217 41H60H1L1 0Z",fill:"white"}),(0,j.jsx)("path",{d:"M1 0V-1H0V0L1 0ZM1 41H0V42H1V41ZM34.8889 29.6498L33.9873 30.0823L34.8889 29.6498ZM26.111 11.3501L27.0127 10.9177L26.111 11.3501ZM1 1H8.0783V-1H1V1ZM60 40H1V42H60V40ZM2 41V0L0 0L0 41H2ZM25.2094 11.7826L33.9873 30.0823L35.7906 29.2174L27.0127 10.9177L25.2094 11.7826ZM52.9217 42H60V40H52.9217V42ZM33.9873 30.0823C37.4811 37.3661 44.8433 42 52.9217 42V40C45.6127 40 38.9517 35.8074 35.7906 29.2174L33.9873 30.0823ZM8.0783 1C15.3873 1 22.0483 5.19257 25.2094 11.7826L27.0127 10.9177C23.5188 3.6339 16.1567 -1 8.0783 -1V1Z",fill:"black",mask:"url(#error_overlay_nav_path_1_outside_1_2667_14687)"})]}),n[1]=t):t=n[1],n[2]===Symbol.for("react.memo_cache_sentinel")?(r=(0,j.jsxs)("svg",{width:"60",height:"42",viewBox:"0 0 60 42",fill:"none",xmlns:"http://www.w3.org/2000/svg",className:"error-overlay-notch-tail",preserveAspectRatio:"none",children:[t,(0,j.jsxs)("g",{mask:"url(#error_overlay_nav_mask0_2667_14687)",children:[(0,j.jsxs)("mask",{id:"error_overlay_nav_path_3_outside_2_2667_14687",maskUnits:"userSpaceOnUse",x:"-1",y:"0.0244141",width:"60",height:"43",fill:"black",children:[(0,j.jsx)("rect",{fill:"white",x:"-1",y:"0.0244141",width:"60",height:"43"}),(0,j.jsx)("path",{d:"M0 1.02441H7.0783C14.772 1.02441 21.7836 5.43765 25.111 12.3746L33.8889 30.6743C37.2164 37.6112 44.228 42.0244 51.9217 42.0244H59H0L0 1.02441Z"})]}),(0,j.jsx)("path",{d:"M0 1.02441H7.0783C14.772 1.02441 21.7836 5.43765 25.111 12.3746L33.8889 30.6743C37.2164 37.6112 44.228 42.0244 51.9217 42.0244H59H0L0 1.02441Z",fill:"var(--background-color)"}),(0,j.jsx)("path",{d:"M0 1.02441L0 0.0244141H-1V1.02441H0ZM0 42.0244H-1V43.0244H0L0 42.0244ZM33.8889 30.6743L32.9873 31.1068L33.8889 30.6743ZM25.111 12.3746L26.0127 11.9421L25.111 12.3746ZM0 2.02441H7.0783V0.0244141H0L0 2.02441ZM59 41.0244H0L0 43.0244H59V41.0244ZM1 42.0244L1 1.02441H-1L-1 42.0244H1ZM24.2094 12.8071L32.9873 31.1068L34.7906 30.2418L26.0127 11.9421L24.2094 12.8071ZM51.9217 43.0244H59V41.0244H51.9217V43.0244ZM32.9873 31.1068C36.4811 38.3905 43.8433 43.0244 51.9217 43.0244V41.0244C44.6127 41.0244 37.9517 36.8318 34.7906 30.2418L32.9873 31.1068ZM7.0783 2.02441C14.3873 2.02441 21.0483 6.21699 24.2094 12.8071L26.0127 11.9421C22.5188 4.65831 15.1567 0.0244141 7.0783 0.0244141V2.02441Z",fill:"var(--stroke-color)",mask:"url(#error_overlay_nav_path_3_outside_2_2667_14687)"})]})]}),n[2]=r):r=n[2],r}let tF=["[data-next-mark]","[data-issues-open]","#nextjs-dev-tools-menu","[data-nextjs-error-overlay-nav]","[data-info-popover]","[data-nextjs-devtools-panel-overlay]","[data-nextjs-devtools-panel-footer]","[data-nextjs-error-overlay-footer]"],tU=function(e){var t,r,n;let o,a,i,l,s,c,u,d,f,p,h,m,g,v,y,b,x=(0,S.c)(23);x[0]!==e?({children:i,className:l,onClose:s,"aria-labelledby":a,"aria-describedby":o,...c}=e,x[0]=e,x[1]=o,x[2]=a,x[3]=i,x[4]=l,x[5]=s,x[6]=c):(o=x[1],a=x[2],i=x[3],l=x[4],s=x[5],c=x[6]);let _=C.useRef(null),[w,k]=C.useState("undefined"!=typeof document&&document.hasFocus()?"dialog":void 0);return x[7]!==s?(u=e=>(e.preventDefault(),s?.()),x[7]=s,x[8]=u):u=x[8],t=_,r=tF,n=u,(b=(0,S.c)(5))[0]!==r||b[1]!==t||b[2]!==n?(v=()=>{let e=t&&"current"in t?t.current:t;if(null==e||null==n)return;let o=t=>{!e||e.contains(t.target)||r.some(e=>t.target.closest(e))||n(t)},a=e.getRootNode();return a.addEventListener("mouseup",o),a.addEventListener("touchend",o,{passive:!1}),function(){a.removeEventListener("mouseup",o),a.removeEventListener("touchend",o)}},y=[n,t,r],b[0]=r,b[1]=t,b[2]=n,b[3]=v,b[4]=y):(v=b[3],y=b[4]),C.useEffect(v,y),x[9]===Symbol.for("react.memo_cache_sentinel")?(d=()=>{if(null==_.current)return;let e=function(){k(document.hasFocus()?"dialog":void 0)};return window.addEventListener("focus",e),window.addEventListener("blur",e),()=>{window.removeEventListener("focus",e),window.removeEventListener("blur",e)}},f=[],x[9]=d,x[10]=f):(d=x[9],f=x[10]),C.useEffect(d,f),x[11]===Symbol.for("react.memo_cache_sentinel")?(p=()=>{let e=_.current,t=e?.getRootNode(),r=t instanceof ShadowRoot?t?.activeElement:null;return e?.focus(),()=>{e?.blur(),r?.focus()}},h=[],x[11]=p,x[12]=h):(p=x[11],h=x[12]),C.useEffect(p,h),x[13]!==s?(m=e=>{"Escape"===e.key&&s?.()},x[13]=s,x[14]=m):m=x[14],x[15]!==o||x[16]!==a||x[17]!==i||x[18]!==l||x[19]!==c||x[20]!==w||x[21]!==m?(g=(0,j.jsx)("div",{ref:_,tabIndex:-1,"data-nextjs-dialog":!0,"data-nextjs-scrollable-content":!0,role:w,"aria-labelledby":a,"aria-describedby":o,"aria-modal":"true",className:l,onKeyDown:m,...c,children:i}),x[15]=o,x[16]=a,x[17]=i,x[18]=l,x[19]=c,x[20]=w,x[21]=m,x[22]=g):g=x[22],g};function t$(e){let t,r,n,o,a,i,l=(0,S.c)(12);return l[0]!==e?({children:t,onClose:n,footer:r,...o}=e,l[0]=e,l[1]=t,l[2]=r,l[3]=n,l[4]=o):(t=l[1],r=l[2],n=l[3],o=l[4]),l[5]!==t||l[6]!==n||l[7]!==o?(a=(0,j.jsx)(tU,{"aria-labelledby":"nextjs__container_errors_label","aria-describedby":"nextjs__container_errors_desc",className:"error-overlay-dialog-scroll",onClose:n,...o,children:t}),l[5]=t,l[6]=n,l[7]=o,l[8]=a):a=l[8],l[9]!==r||l[10]!==a?(i=(0,j.jsxs)("div",{className:"error-overlay-dialog-container",children:[a,r]}),l[9]=r,l[10]=a,l[11]=i):i=l[11],i}let tH=`
  .error-overlay-dialog-container {
    display: flex;
    flex-direction: column;
    background: var(--color-background-100);
    background-clip: padding-box;
    border: var(--next-dialog-border-width) solid var(--color-gray-400);
    border-radius: 0 0 var(--next-dialog-radius) var(--next-dialog-radius);
    box-shadow: var(--shadow-menu);
    position: relative;
    overflow: hidden;
  }

  .error-overlay-dialog-scroll {
    overflow-y: auto;
    height: 100%;
  }
`;function tV(e){let t,r=(0,S.c)(2);return r[0]!==e?(t=(0,j.jsx)("div",{"data-nextjs-dialog-header":!0,...e,children:e.children}),r[0]=e,r[1]=t):t=r[1],t}function tB(e){let t,r=(0,S.c)(2),{children:n}=e;return r[0]!==n?(t=(0,j.jsx)(tV,{className:"nextjs-container-errors-header",children:n}),r[0]=n,r[1]=t):t=r[1],t}let tq=`
  .nextjs-container-errors-header {
    position: relative;
  }
  .nextjs-container-errors-header > h1 {
    font-size: var(--size-20);
    line-height: var(--size-24);
    font-weight: bold;
    margin: calc(16px * 1.5) 0;
    color: var(--color-title-h1);
  }
  .nextjs-container-errors-header small {
    font-size: var(--size-14);
    color: var(--color-accents-1);
    margin-left: 16px;
  }
  .nextjs-container-errors-header small > span {
    font-family: var(--font-stack-monospace);
  }
  .nextjs-container-errors-header > div > small {
    margin: 0;
    margin-top: 4px;
  }
  .nextjs-container-errors-header > p > a {
    color: inherit;
    font-weight: bold;
  }
  .nextjs-container-errors-header
    > .nextjs-container-build-error-version-status {
    position: absolute;
    top: 16px;
    right: 16px;
  }
`;function tW(e){let t,r=(0,S.c)(2),{children:n}=e;return r[0]!==n?(t=(0,j.jsx)(e3,{className:"nextjs-container-errors-body",children:n}),r[0]=n,r[1]=t):t=r[1],t}let tK=0,tY=function(e){let t,r,n,o,a,i=(0,S.c)(9);return i[0]!==e?({className:r,children:t,...n}=e,i[0]=e,i[1]=t,i[2]=r,i[3]=n):(t=i[1],r=i[2],n=i[3]),i[4]===Symbol.for("react.memo_cache_sentinel")?(o=[],i[4]=o):o=i[4],C.useEffect(tG,o),i[5]!==t||i[6]!==r||i[7]!==n?(a=(0,j.jsx)("div",{"data-nextjs-dialog-overlay":!0,className:r,...n,children:t}),i[5]=t,i[6]=r,i[7]=n,i[8]=a):a=i[8],a};function tX(){setTimeout(()=>{0!==tK&&0==--tK&&(void 0!==e&&(document.body.style.paddingRight=e,e=void 0),void 0!==t&&(document.body.style.overflow=t,t=void 0))})}function tG(){return setTimeout(()=>{if(tK++>0)return;let r=window.innerWidth-document.documentElement.clientWidth;r>0&&(e=document.body.style.paddingRight,document.body.style.paddingRight=`${r}px`),t=document.body.style.overflow,document.body.style.overflow="hidden"}),tX}function tQ(e){let t,r,n,o=(0,S.c)(6);return o[0]!==e?({children:t,...r}=e,o[0]=e,o[1]=t,o[2]=r):(t=o[1],r=o[2]),o[3]!==t||o[4]!==r?(n=(0,j.jsx)(tY,{...r,children:t}),o[3]=t,o[4]=r,o[5]=n):n=o[5],n}let tJ=e_`
  [data-nextjs-dialog-overlay] {
    padding: initial;
    top: 10vh;
  }
`;function t0(e){let t,r,n,o=(0,S.c)(4),{errorCount:a,activeIdx:i}=e,l=Math.min(a-i-1,2);return o[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("div",{className:"error-overlay-bottom-stack-layer error-overlay-bottom-stack-layer-1",children:"1"}),r=(0,j.jsx)("div",{className:"error-overlay-bottom-stack-layer error-overlay-bottom-stack-layer-2",children:"2"}),o[0]=t,o[1]=r):(t=o[0],r=o[1]),o[2]!==l?(n=(0,j.jsx)("div",{"aria-hidden":!0,className:"error-overlay-bottom-stack",children:(0,j.jsxs)("div",{className:"error-overlay-bottom-stack-stack","data-stack-count":l,children:[t,r]})}),o[2]=l,o[3]=n):n=o[3],n}let t1=`
  .error-overlay-bottom-stack-layer {
    width: 100%;
    height: var(--stack-layer-height);
    position: relative;
    border: 1px solid var(--color-gray-400);
    border-radius: var(--rounded-xl);
    background: var(--color-background-200);
    transition:
      translate 350ms var(--timing-swift),
      box-shadow 350ms var(--timing-swift);
  }

  .error-overlay-bottom-stack-layer-1 {
    width: calc(100% - var(--size-24));
  }

  .error-overlay-bottom-stack-layer-2 {
    width: calc(100% - var(--size-48));
    z-index: -1;
  }

  .error-overlay-bottom-stack {
    width: 100%;
    position: absolute;
    bottom: -1px;
    height: 0;
    overflow: visible;
  }

  .error-overlay-bottom-stack-stack {
    --stack-layer-height: 44px;
    --stack-layer-height-half: calc(var(--stack-layer-height) / 2);
    --stack-layer-trim: 13px;
    --shadow: 0px 0.925px 0.925px 0px rgba(0, 0, 0, 0.02),
      0px 3.7px 7.4px -3.7px rgba(0, 0, 0, 0.04),
      0px 14.8px 22.2px -7.4px rgba(0, 0, 0, 0.06);

    display: grid;
    place-items: center center;
    width: 100%;
    position: fixed;
    height: 0;
    overflow: visible;
    z-index: -1;
    max-width: var(--next-dialog-max-width);

    .error-overlay-bottom-stack-layer {
      grid-area: 1 / 1;
      /* Hide */
      translate: 0 calc(var(--stack-layer-height) * -1);
    }

    &[data-stack-count='1'],
    &[data-stack-count='2'] {
      .error-overlay-bottom-stack-layer-1 {
        translate: 0
          calc(var(--stack-layer-height-half) * -1 - var(--stack-layer-trim));
      }
    }

    &[data-stack-count='2'] {
      .error-overlay-bottom-stack-layer-2 {
        translate: 0 calc(var(--stack-layer-trim) * -1 * 2);
      }
    }

    /* Only the bottom stack should have the shadow */
    &[data-stack-count='1'] .error-overlay-bottom-stack-layer-1 {
      box-shadow: var(--shadow);
    }

    &[data-stack-count='2'] {
      .error-overlay-bottom-stack-layer-2 {
        box-shadow: var(--shadow);
      }
    }
  }
`;function t2(e){let t,r=(0,S.c)(2),{environmentName:n}=e;return r[0]!==n?(t=(0,j.jsx)("span",{"data-nextjs-environment-name-label":!0,children:n}),r[0]=n,r[1]=t):t=r[1],t}let t3=`
  [data-nextjs-environment-name-label] {
    padding: 2px 6px;
    margin: 0;
    border-radius: var(--rounded-md-2);
    background: var(--color-gray-100);
    font-weight: 600;
    font-size: var(--size-12);
    color: var(--color-gray-900);
    font-family: var(--font-stack-monospace);
    line-height: var(--size-20);
  }
`;function t4(e){let t=e?.getRootNode();return t instanceof ShadowRoot?t?.activeElement:null}function t5(e,t,r,n,o){let a,i,l=(0,S.c)(7);l[0]!==r||l[1]!==n||l[2]!==o||l[3]!==e||l[4]!==t?(a=()=>{if(!r)return;let a=o||e.current?.ownerDocument,i=function(r){let o=r.target;!(e.current&&e.current.contains(o))&&(e.current?.getBoundingClientRect()&&r.clientX>=e.current.getBoundingClientRect().left-10&&r.clientX<=e.current.getBoundingClientRect().right+10&&r.clientY>=e.current.getBoundingClientRect().top-10&&r.clientY<=e.current.getBoundingClientRect().bottom+10||t.current?.getBoundingClientRect()&&r.clientX>=t.current.getBoundingClientRect().left-10&&r.clientX<=t.current.getBoundingClientRect().right+10&&r.clientY>=t.current.getBoundingClientRect().top-10&&r.clientY<=t.current.getBoundingClientRect().bottom+10||n("outside"))},l=function(e){"Escape"===e.key&&n("escape")};return a?.addEventListener("mousedown",i),a?.addEventListener("keydown",l),()=>{a?.removeEventListener("mousedown",i),a?.removeEventListener("keydown",l)}},i=[r,n,o,e,t],l[0]=r,l[1]=n,l[2]=o,l[3]=e,l[4]=t,l[5]=a,l[6]=i):(a=l[5],i=l[6]),(0,C.useEffect)(a,i)}let t6="cubic-bezier(0.175, 0.885, 0.32, 1.1)",t9=(0,C.forwardRef)(function(e,t){let r,n,o=(0,S.c)(9),{stop:a,blur:i,side:l,style:s,height:c}=e,u=`${c}px`;o[0]!==i||o[1]!==a||o[2]!==s||o[3]!==u?(r={"--stop":a,"--blur":i,"--height":u,...s},o[0]=i,o[1]=a,o[2]=s,o[3]=u,o[4]=r):r=o[4];let d=r;return o[5]!==t||o[6]!==l||o[7]!==d?(n=(0,j.jsx)("div",{ref:t,"aria-hidden":!0,"data-nextjs-scroll-fader":!0,className:"nextjs-scroll-fader","data-side":l,style:d}),o[5]=t,o[6]=l,o[7]=d,o[8]=n):n=o[8],n}),t8=`
  .nextjs-scroll-fader {
    --blur: 1px;
    --stop: 25%;
    --height: 150px;
    --color-bg: var(--color-background-100);
    position: absolute;
    pointer-events: none;
    user-select: none;
    width: 100%;
    height: var(--height);
    left: 0;
    backdrop-filter: blur(var(--blur));

    &[data-side="top"] {
      top: 0;
      background: linear-gradient(to top, transparent, var(--color-bg));
      mask-image: linear-gradient(to bottom, var(--color-bg) var(--stop), transparent);
    }
  }
`,t7=(0,C.forwardRef)(function(e,t){let r,n,o,a,i,l,s=(0,S.c)(13);s[0]!==e?({children:r,measure:n,...o}=e,s[0]=e,s[1]=r,s[2]=n,s[3]=o):(r=s[1],n=s[2],o=s[3]);let[c,u]=(0,C.useState)(null),[d,f]=function(e,t){let r,n,o,a=(0,S.c)(7),[i,l]=(0,C.useState)(0),[s,c]=(0,C.useState)(!0);return a[0]!==e||a[1]!==t?(r=()=>{let r;if(!t||!e)return;let n=new ResizeObserver(e=>{let[t]=e,{contentRect:n}=t;clearTimeout(r),r=window.setTimeout(()=>{c(!1)},100),l(n.height)});return n.observe(e),()=>n.disconnect()},n=[t,e],a[0]=e,a[1]=t,a[2]=r,a[3]=n):(r=a[2],n=a[3]),(0,C.useEffect)(r,n),a[4]!==i||a[5]!==s?(o=[i,s],a[4]=i,a[5]=s,a[6]=o):o=a[6],o}(c,n),p=f?"auto":d;return s[4]!==p?(a={height:p,transition:"height 250ms var(--timing-swift)"},s[4]=p,s[5]=a):a=s[5],s[6]!==r?(i=(0,j.jsx)("div",{ref:u,children:r}),s[6]=r,s[7]=i):i=s[7],s[8]!==o||s[9]!==t||s[10]!==a||s[11]!==i?(l=(0,j.jsx)("div",{...o,ref:t,style:a,children:i}),s[8]=o,s[9]=t,s[10]=a,s[11]=i,s[12]=l):l=s[12],l});function re(e){let t,r,n,o=(0,S.c)(6);o[0]!==e?({fixed:t,...r}=e,o[0]=e,o[1]=t,o[2]=r):(t=o[1],r=o[2]);let a=!!t||void 0;return o[3]!==r||o[4]!==a?(n=(0,j.jsx)("div",{"data-nextjs-dialog-backdrop":!0,"data-nextjs-dialog-backdrop-fixed":a,...r}),o[3]=r,o[4]=a,o[5]=n):n=o[5],n}function rt(e){var t,r;let n,o,a,i,l,s,c,u,d,f,p,h,m,g,v,y,b,x,_,w,k,E,T,N,L,I,P,z=(0,S.c)(66),{errorMessage:R,errorType:O,children:M,errorCode:A,errorCount:D,error:Z,debugInfo:F,isBuildError:U,onClose:$,versionInfo:H,runtimeErrors:V,activeIdx:B,setActiveIndex:q,isTurbopack:W,dialogResizerRef:K,generateErrorInfo:Y,rendered:X,transitionDurationMs:G}=e,Q=void 0===X||X,J=`${G}ms`;z[0]!==J?(n={"--transition-duration":J},z[0]=J,z[1]=n):n=z[1];let ee=n;z[2]!==Q||z[3]!==ee?(o={"data-rendered":Q,style:ee},z[2]=Q,z[3]=ee,z[4]=o):o=z[4];let et=o,[er,en]=C.useState(!!G),eo=C.useRef(null),ea=!!A,ei=C.useRef(null);t=ei,r=Q,void 0!==(I=(0,S.c)(11))[0]?(T=e=>{e?.focus()},I[0]=void 0,I[1]=T):T=I[1],P=(0,C.useEffectEvent)(T),I[2]!==r||I[3]!==P||I[4]!==t||null!==I[5]?(N=()=>{let e=null,n=function(t){let r;if("Tab"!==t.key||null===e)return;let[n,o]=(r=e.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'))?[r[0],r[r.length-1]]:[],a=t4(e);t.shiftKey?a===n&&(o?.focus(),t.preventDefault()):a===o&&(n?.focus(),t.preventDefault())},o=setTimeout(()=>{if(e=t.current,r)P(e),e?.addEventListener("keydown",n);else t4(e)});return()=>{clearTimeout(o),e?.removeEventListener("keydown",n)}},I[2]=r,I[3]=P,I[4]=t,I[5]=null,I[6]=N):N=I[6],I[7]!==r||I[8]!==t||null!==I[9]?(L=[r,t,null],I[7]=r,I[8]=t,I[9]=null,I[10]=L):L=I[10],(0,C.useEffect)(N,L),z[5]===Symbol.for("react.memo_cache_sentinel")?(a=function(e){if(eo.current){let t=function(e,[t,r]){return Math.min(Math.max(e,t),r)}(e.currentTarget.scrollTop/17,[0,1]);eo.current.style.opacity=String(t)}},z[5]=a):a=z[5];let el=a;z[6]===Symbol.for("react.memo_cache_sentinel")?(i=function(e){let{propertyName:t,target:r}=e;"scale"===t&&r===ei.current&&en(!1)},z[6]=i):i=z[6];let es=i;z[7]!==U?(l=(0,j.jsx)(re,{fixed:U}),z[7]=U,z[8]=l):l=z[8],z[9]!==B||z[10]!==W||z[11]!==V||z[12]!==q||z[13]!==H?(s=(0,j.jsx)(tO,{runtimeErrors:V,activeIdx:B,setActiveIndex:q,versionInfo:H,isTurbopack:W}),z[9]=B,z[10]=W,z[11]=V,z[12]=q,z[13]=H,z[14]=s):s=z[14],z[15]!==A||z[16]!==ea?(c=ea&&(0,j.jsx)(tw,{errorCode:A}),z[15]=A,z[16]=ea,z[17]=c):c=z[17];let ec=!er;z[18]!==O?(u=(0,j.jsx)(tC,{errorType:O}),z[18]=O,z[19]=u):u=z[19],z[20]!==Z.environmentName?(d=Z.environmentName&&(0,j.jsx)(t2,{environmentName:Z.environmentName}),z[20]=Z.environmentName,z[21]=d):d=z[21],z[22]!==u||z[23]!==d?(f=(0,j.jsxs)("span",{"data-nextjs-error-label-group":!0,children:[u,d]}),z[22]=u,z[23]=d,z[24]=f):f=z[24],z[25]!==F||z[26]!==Z||z[27]!==Y?(p=(0,j.jsx)(tg,{error:Z,debugInfo:F,generateErrorInfo:Y}),z[25]=F,z[26]=Z,z[27]=Y,z[28]=p):p=z[28],z[29]!==A||z[30]!==f||z[31]!==p?(h=(0,j.jsxs)("div",{className:"nextjs__container_errors__error_title","data-nextjs-error-code":A,children:[f,p]}),z[29]=A,z[30]=f,z[31]=p,z[32]=h):h=z[32],z[33]!==R||z[34]!==O?(m=(0,j.jsx)(tj,{errorMessage:R,errorType:O}),z[33]=R,z[34]=O,z[35]=m):m=z[35],z[36]!==h||z[37]!==m?(g=(0,j.jsxs)(tB,{children:[h,m]}),z[36]=h,z[37]=m,z[38]=g):g=z[38],z[39]!==M?(v=(0,j.jsx)(tW,{children:M}),z[39]=M,z[40]=v):v=z[40],z[41]!==g||z[42]!==v?(y=(0,j.jsxs)(e4,{children:[g,v]}),z[41]=g,z[42]=v,z[43]=y):y=z[43],z[44]!==K||z[45]!==ec||z[46]!==y?(b=(0,j.jsx)(t7,{ref:K,measure:ec,"data-nextjs-dialog-sizer":!0,children:y}),z[44]=K,z[45]=ec,z[46]=y,z[47]=b):b=z[47];let eu=B??0;return z[48]!==D||z[49]!==eu?(x=(0,j.jsx)(t0,{errorCount:D,activeIdx:eu}),z[48]=D,z[49]=eu,z[50]=x):x=z[50],z[51]!==ea||z[52]!==$||z[53]!==c||z[54]!==b||z[55]!==x?(_=(0,j.jsxs)(t$,{onClose:$,"data-has-footer":ea,onScroll:el,footer:c,children:[b,x]}),z[51]=ea,z[52]=$,z[53]=c,z[54]=b,z[55]=x,z[56]=_):_=z[56],z[57]===Symbol.for("react.memo_cache_sentinel")?(w=(0,j.jsx)(t9,{ref:eo,side:"top",stop:"50%",blur:"4px",height:48}),z[57]=w):w=z[57],z[58]!==et||z[59]!==_||z[60]!==s?(k=(0,j.jsxs)("div",{"data-nextjs-dialog-root":!0,onTransitionEnd:es,ref:ei,...et,children:[s,_,w]}),z[58]=et,z[59]=_,z[60]=s,z[61]=k):k=z[61],z[62]!==et||z[63]!==k||z[64]!==l?(E=(0,j.jsxs)(tQ,{...et,children:[l,k]}),z[62]=et,z[63]=k,z[64]=l,z[65]=E):E=z[65],E}let rr=`
  ${tJ}
  ${tH}
  ${tq}
  

  ${tA}
  ${tE}
  ${tS}
  ${tv}

  [data-nextjs-error-label-group] {
    display: flex;
    align-items: center;
    gap: 8px;
  }
`,rn=e_`
  [data-nextjs-dialog-overlay] {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    /* secondary z-index, -1 than toast z-index */
    z-index: 2147483646;

    display: flex;
    align-content: center;
    align-items: center;
    flex-direction: column;
    padding: 10vh 15px 0;
    /* color schemes we handle. Every other scheme the UA would need to overwrite */
    color-scheme: dark light;
  }

  @media (max-height: 812px) {
    [data-nextjs-dialog-overlay] {
      padding: 15px 15px 0;
    }
  }

  [data-nextjs-dialog-backdrop] {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background-color: var(--color-backdrop);
    backdrop-filter: blur(10px);
    pointer-events: all;
    z-index: -1;
  }

  [data-nextjs-dialog-backdrop-fixed] {
    cursor: not-allowed;
    -webkit-backdrop-filter: blur(8px);
    backdrop-filter: blur(8px);
  }
`;function ro(e){let t,r,n,o=(0,S.c)(9),{file:a,location:i}=e,l=i?.line??1,s=i?.column??1;o[0]!==a||o[1]!==l||o[2]!==s?(t={file:a,line1:l,column1:s},o[0]=a,o[1]=l,o[2]=s,o[3]=t):t=o[3];let c=eD(t),u=i?`:${i.line}:${i.column}`:null;return o[4]===Symbol.for("react.memo_cache_sentinel")?(r=(0,j.jsxs)("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",fill:"none",stroke:"currentColor",strokeWidth:"2",strokeLinecap:"round",strokeLinejoin:"round",children:[(0,j.jsx)("path",{d:"M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"}),(0,j.jsx)("polyline",{points:"15 3 21 3 21 9"}),(0,j.jsx)("line",{x1:"10",y1:"14",x2:"21",y2:"3"})]}),o[4]=r):r=o[4],o[5]!==a||o[6]!==c||o[7]!==u?(n=(0,j.jsxs)("div",{"data-with-open-in-editor-link":!0,"data-with-open-in-editor-link-import-trace":!0,role:"link",onClick:c,title:"Click to open in your editor",children:[a,u,r]}),o[5]=a,o[6]=c,o[7]=u,o[8]=n):n=o[8],n}let ra=`
  [data-with-open-in-editor-link] svg {
    width: auto;
    height: var(--size-14);
    margin-left: 8px;
  }
  [data-with-open-in-editor-link] {
    cursor: pointer;
  }
  [data-with-open-in-editor-link]:hover {
    text-decoration: underline dotted;
  }
  [data-with-open-in-editor-link-import-trace] {
    margin-left: 16px;
  }
`,ri=function(e){let t,r,n,o,a,i,l,s,c,u,d,f,p,h,m,g,v,y,b=(0,S.c)(42),{content:x}=e;if(b[0]!==x){let e,r,n;r=function(e){let t=e.shift();if(!t)return null;let[r,n,o]=t.split(":",3),a=Number(n),i=Number(o),l=!Number.isNaN(a)&&!Number.isNaN(i);return{fileName:l?r:t,location:l?{line1:a,column1:i}:void 0}}(e=x.split("\n")),n=function(e){if(e.some(e=>/ReactServerComponentsError:/.test(e))||e.some(e=>/Import trace for requested module:/.test(e))){let t=[];for(;/.+\..+/.test(e[e.length-1])&&!e[e.length-1].includes(":");){let r=e.pop().trim();t.unshift(r)}return t}return[]}(e),t={file:r,source:e.join("\n"),importTraceFiles:n},b[0]=x,b[1]=t}else t=b[1];let{file:_,source:w,importTraceFiles:k}=t;b[2]!==w?(r=eY().ansiToJson(w,{json:!0,use_classes:!0,remove_empty:!0}),b[2]=w,b[3]=r):r=b[3];let C=r,E=_?.fileName,T=_?.location?.line1??1,N=_?.location?.column1??1;b[4]!==E||b[5]!==T||b[6]!==N?(n={file:E,line1:T,column1:N},b[4]=E,b[5]=T,b[6]=N,b[7]=n):n=b[7];let L=eD(n),I=_?.fileName??null;if(b[8]!==_?.location?.column1||b[9]!==_?.location?.line1||b[10]!==I){let e={file:I,methodName:"",arguments:[],line1:_?.location?.line1??null,column1:_?.location?.column1??null},t=e?.file?.split(".").pop();l=!0,i="code-frame-header",o="code-frame-link",a=(0,j.jsx)("span",{className:"code-frame-icon",children:(0,j.jsx)(e$,{lang:t})}),s=!0,c=eA(e),b[8]=_?.location?.column1,b[9]=_?.location?.line1,b[10]=I,b[11]=o,b[12]=a,b[13]=i,b[14]=l,b[15]=s,b[16]=c}else o=b[11],a=b[12],i=b[13],l=b[14],s=b[15],c=b[16];return b[17]!==s||b[18]!==c?(u=(0,j.jsx)("span",{"data-text":s,children:c}),b[17]=s,b[18]=c,b[19]=u):u=b[19],b[20]===Symbol.for("react.memo_cache_sentinel")?(d=(0,j.jsx)("span",{className:"code-frame-icon","data-icon":"right",children:(0,j.jsx)(eF,{width:16,height:16})}),b[20]=d):d=b[20],b[21]!==L?(f=(0,j.jsx)("button",{"aria-label":"Open in editor","data-with-open-in-editor-link-source-file":!0,onClick:L,children:d}),b[21]=L,b[22]=f):f=b[22],b[23]!==o||b[24]!==a||b[25]!==u||b[26]!==f?(p=(0,j.jsxs)("div",{className:o,children:[a,u,f]}),b[23]=o,b[24]=a,b[25]=u,b[26]=f,b[27]=p):p=b[27],b[28]!==i||b[29]!==p?(h=(0,j.jsx)("div",{className:i,children:p}),b[28]=i,b[29]=p,b[30]=h):h=b[30],b[31]!==C?(m=C.map(rs),b[31]=C,b[32]=m):m=b[32],b[33]!==k?(g=k.map(rc),b[33]=k,b[34]=g):g=b[34],b[35]!==m||b[36]!==g?(v=(0,j.jsx)("pre",{className:"code-frame-pre",children:(0,j.jsxs)("div",{className:"code-frame-lines",children:[m,g]})}),b[35]=m,b[36]=g,b[37]=v):v=b[37],b[38]!==l||b[39]!==h||b[40]!==v?(y=(0,j.jsxs)("div",{"data-nextjs-codeframe":l,children:[h,v]}),b[38]=l,b[39]=h,b[40]=v,b[41]=y):y=b[41],y},rl=`
  [data-nextjs-terminal]::selection,
  [data-nextjs-terminal] *::selection {
    background-color: var(--color-ansi-selection);
  }

  [data-nextjs-terminal] * {
    color: inherit;
    background-color: transparent;
    font-family: var(--font-stack-monospace);
  }

  [data-nextjs-terminal] > div > p {
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    margin: 0;
  }
  [data-nextjs-terminal] > div > p:hover {
    text-decoration: underline dotted;
  }
  [data-nextjs-terminal] div > pre {
    overflow: hidden;
    display: inline-block;
  }
`;function rs(e,t){return(0,j.jsx)("span",{style:{color:e.fg?`var(--color-${e.fg})`:void 0,..."bold"===e.decoration?{fontWeight:500}:"italic"===e.decoration?{fontStyle:"italic"}:void 0},children:(0,j.jsx)(eI,{text:e.content})},`terminal-entry-${t}`)}function rc(e){return(0,j.jsx)(ro,{isSourceFile:!1,file:e},e)}let ru=function(e){let t,r,n,o,a,i,l,s=(0,S.c)(19);s[0]!==e?({message:t,...r}=e,s[0]=e,s[1]=t,s[2]=r):(t=s[1],r=s[2]),s[3]!==t?(n=Error(t),s[3]=t,s[4]=n):n=s[4];let c=n;if(s[5]!==t){let e;e=t.split("\n"),o=eG()(e[1]||"").replace(/^Error: /,"")||"Failed to compile",s[5]=t,s[6]=o}else o=s[6];let u=o;s[7]!==u||s[8]!==t||s[9]!==r.versionInfo.installed?(a=async()=>{let e=[];if(e.push("## Error Type\nBuild Error"),u&&e.push(`## Error Message
${u}`),t){let r=eG()(t);e.push(`## Build Output
${r}`)}return`${e.join("\n\n")}

Next.js version: ${r.versionInfo.installed} (${process.env.__NEXT_BUNDLER})
`},s[7]=u,s[8]=t,s[9]=r.versionInfo.installed,s[10]=a):a=s[10];let d=a;return s[11]!==t?(i=(0,j.jsx)(ri,{content:t}),s[11]=t,s[12]=i):i=s[12],s[13]!==c||s[14]!==u||s[15]!==d||s[16]!==r||s[17]!==i?(l=(0,j.jsx)(rt,{errorType:"Build Error",errorMessage:u,onClose:rd,error:c,generateErrorInfo:d,...r,children:i}),s[13]=c,s[14]=u,s[15]=d,s[16]=r,s[17]=i,s[18]=l):l=s[18],l};function rd(){}let rf=function(e){let t,r,n,o,a,i,l,s,c=(0,S.c)(26),{frame:u}=e,d=u.originalStackFrame??u.sourceStackFrame,f=!!u.originalCodeFrame;c[0]!==d||c[1]!==f?(t=f?{file:d.file,line1:d.line1??1,column1:d.column1??1}:void 0,c[0]=d,c[1]=f,c[2]=t):t=c[2];let p=eD(t);c[3]!==d?(r=eA(d),c[3]=d,c[4]=r):r=c[4];let h=r;if(!h)return null;let m=!f;return c[5]!==d.methodName?(n=(0,j.jsx)(eI,{text:d.methodName}),c[5]=d.methodName,c[6]=n):n=c[6],c[7]!==d.methodName||c[8]!==f||c[9]!==p?(o=f&&(0,j.jsx)("button",{onClick:p,className:"open-in-editor-button","aria-label":`Open ${d.methodName} in editor`,children:(0,j.jsx)(eF,{width:16,height:16})}),c[7]=d.methodName,c[8]=f,c[9]=p,c[10]=o):o=c[10],c[11]!==u.error||c[12]!==u.reason?(a=u.error?(0,j.jsx)("button",{className:"source-mapping-error-button",onClick:()=>console.error(u.reason),title:"Sourcemapping failed. Click to log cause of error.",children:(0,j.jsx)(eU,{width:16,height:16})}):null,c[11]=u.error,c[12]=u.reason,c[13]=a):a=c[13],c[14]!==n||c[15]!==o||c[16]!==a?(i=(0,j.jsxs)("div",{className:"call-stack-frame-method-name",children:[n,o,a]}),c[14]=n,c[15]=o,c[16]=a,c[17]=i):i=c[17],c[18]!==f||c[19]!==h?(l=(0,j.jsx)("span",{className:"call-stack-frame-file","data-has-original-code-frame":f,children:h}),c[18]=f,c[19]=h,c[20]=l):l=c[20],c[21]!==u.ignored||c[22]!==m||c[23]!==i||c[24]!==l?(s=(0,j.jsxs)("div",{"data-nextjs-call-stack-frame":!0,"data-nextjs-call-stack-frame-no-source":m,"data-nextjs-call-stack-frame-ignored":u.ignored,children:[i,l]}),c[21]=u.ignored,c[22]=m,c[23]=i,c[24]=l,c[25]=s):s=c[25],s},rp=`
  [data-nextjs-call-stack-frame-no-source] {
    padding: 6px 8px;
    margin-bottom: 4px;

    border-radius: var(--rounded-lg);
  }

  [data-nextjs-call-stack-frame-no-source]:last-child {
    margin-bottom: 0;
  }

  [data-nextjs-call-stack-frame-ignored="true"] {
    opacity: 0.6;
  }

  [data-nextjs-call-stack-frame] {
    user-select: text;
    display: block;
    box-sizing: border-box;

    user-select: text;
    -webkit-user-select: text;
    -moz-user-select: text;
    -ms-user-select: text;

    padding: 6px 8px;

    border-radius: var(--rounded-lg);
  }

  .call-stack-frame-method-name {
    display: flex;
    align-items: center;
    gap: 4px;

    margin-bottom: 4px;
    font-family: var(--font-stack-monospace);

    color: var(--color-gray-1000);
    font-size: var(--size-14);
    font-weight: 500;
    line-height: var(--size-20);

    svg {
      width: var(--size-16px);
      height: var(--size-16px);
    }
  }

  .open-in-editor-button, .source-mapping-error-button {
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--rounded-full);
    padding: 4px;
    color: var(--color-font);

    svg {
      width: var(--size-16);
      height: var(--size-16);
    }

    &:focus-visible {
      outline: var(--focus-ring);
      outline-offset: -2px;
    }

    &:hover {
      background: var(--color-gray-100);
    }
  }

  .call-stack-frame-file {
    color: var(--color-gray-900);
    font-size: var(--size-14);
    line-height: var(--size-20);
    word-wrap: break-word;
  }
`;function rh(){let e,t=(0,S.c)(1);return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("svg",{width:"16",height:"16",viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M8.70722 2.39641C8.3167 2.00588 7.68353 2.00588 7.29301 2.39641L4.46978 5.21963L3.93945 5.74996L5.00011 6.81062L5.53044 6.28029L8.00011 3.81062L10.4698 6.28029L11.0001 6.81062L12.0608 5.74996L11.5304 5.21963L8.70722 2.39641ZM5.53044 9.71963L5.00011 9.1893L3.93945 10.25L4.46978 10.7803L7.29301 13.6035C7.68353 13.994 8.3167 13.994 8.70722 13.6035L11.5304 10.7803L12.0608 10.25L11.0001 9.1893L10.4698 9.71963L8.00011 12.1893L5.53044 9.71963Z",fill:"currentColor"})}),t[0]=e):e=t[0],e}function rm(e){let t,r,n,o,a,i=(0,S.c)(17),{frames:l,isIgnoreListOpen:s,ignoredFramesTally:c,onToggleIgnoreList:u}=e;if(i[0]!==l.length?(t=(0,j.jsxs)("p",{"data-nextjs-call-stack-title":!0,children:["Call Stack ",(0,j.jsx)("span",{"data-nextjs-call-stack-count":!0,children:l.length})]}),i[0]=l.length,i[1]=t):t=i[1],i[2]!==c||i[3]!==s||i[4]!==u?(r=c>0&&(0,j.jsxs)("button",{"data-nextjs-call-stack-ignored-list-toggle-button":s,onClick:u,children:[`${s?"Hide":"Show"} ${c} ignore-listed frame(s)`,(0,j.jsx)(rh,{})]}),i[2]=c,i[3]=s,i[4]=u,i[5]=r):r=i[5],i[6]!==t||i[7]!==r?(n=(0,j.jsxs)("div",{"data-nextjs-call-stack-header":!0,children:[t,r]}),i[6]=t,i[7]=r,i[8]=n):n=i[8],i[9]!==l||i[10]!==s){let e;i[12]!==s?(e=(e,t)=>!e.ignored||s?(0,j.jsx)(rf,{frame:e},t):null,i[12]=s,i[13]=e):e=i[13],o=l.map(e),i[9]=l,i[10]=s,i[11]=o}else o=i[11];return i[14]!==n||i[15]!==o?(a=(0,j.jsxs)("div",{"data-nextjs-call-stack-container":!0,children:[n,o]}),i[14]=n,i[15]=o,i[16]=a):a=i[16],a}let rg=e_`
  [data-nextjs-call-stack-container] {
    position: relative;
    margin-top: 8px;
  }

  [data-nextjs-call-stack-header] {
    display: flex;
    justify-content: space-between;
    align-items: center;
    min-height: var(--size-28);
    padding: 8px 8px 12px 4px;
    width: 100%;
  }

  [data-nextjs-call-stack-title] {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;

    margin: 0;

    color: var(--color-gray-1000);
    font-size: var(--size-16);
    font-weight: 500;
  }

  [data-nextjs-call-stack-count] {
    display: flex;
    justify-content: center;
    align-items: center;

    width: var(--size-20);
    height: var(--size-20);
    gap: 4px;

    color: var(--color-gray-1000);
    text-align: center;
    font-size: var(--size-11);
    font-weight: 500;
    line-height: var(--size-16);

    border-radius: var(--rounded-full);
    background: var(--color-gray-300);
  }

  [data-nextjs-call-stack-ignored-list-toggle-button] {
    all: unset;
    display: flex;
    align-items: center;
    gap: 6px;
    color: var(--color-gray-900);
    font-size: var(--size-14);
    line-height: var(--size-20);
    border-radius: 6px;
    padding: 4px 6px;
    margin-right: -6px;
    transition: background 150ms ease;

    &:hover {
      background: var(--color-gray-100);
    }

    &:focus {
      outline: var(--focus-ring);
    }

    svg {
      width: var(--size-16);
      height: var(--size-16);
    }
  }
`;function rv({frames:e,dialogResizerRef:t}){let r=(0,C.useRef)(NaN),[n,o]=(0,C.useState)(!1),a=(0,C.useMemo)(()=>e.reduce((e,t)=>e+ +!!t.ignored,0),[e]);return(0,j.jsx)(rm,{frames:e,isIgnoreListOpen:n,onToggleIgnoreList:function(){let e=t?.current;if(n){if(!e)return void o(!1);let{height:t}=e.getBoundingClientRect();r.current||(r.current=t),e.style.height=`${r.current}px`,e.addEventListener("transitionend",function t(){e.removeEventListener("transitionend",t),o(!1)})}else{if(e){let{height:t}=e.getBoundingClientRect();r.current||(r.current=t)}o(!0)}},ignoredFramesTally:a})}function ry(e){let t,r,n,o,a=(0,S.c)(8);a[0]!==e?(t=void 0===e?{}:e,a[0]=e,a[1]=t):t=a[1];let{collapsed:i}=t;return a[2]!==i?(r="boolean"==typeof i?{style:{transform:i?void 0:"rotate(90deg)"}}:{},a[2]=i,a[3]=r):r=a[3],a[4]===Symbol.for("react.memo_cache_sentinel")?(n=(0,j.jsx)("path",{style:{fill:"var(--color-font)"},fillRule:"evenodd",d:"m6.75 3.94.53.53 2.824 2.823a1 1 0 0 1 0 1.414L7.28 11.53l-.53.53L5.69 11l.53-.53L8.69 8 6.22 5.53 5.69 5l1.06-1.06Z",clipRule:"evenodd"}),a[4]=n):n=a[4],a[5]!==i||a[6]!==r?(o=(0,j.jsx)("svg",{"data-nextjs-call-stack-chevron-icon":!0,"data-collapsed":i,width:"16",height:"16",fill:"none",...r,children:n}),a[5]=i,a[6]=r,a[7]=o):o=a[7],o}function rb(e){let t,r,n,o,a,i,l,s,c,u=(0,S.c)(19),{reactOutputComponentDiff:d}=e,[f,p]=(0,C.useState)(!0);u[0]!==d?(t=[],d.split("\n").forEach((e,r)=>{let n="+"===e[0]||"-"===e[0],o=">"===e[0],a=n||o,i=a?e[0]:"",l=a?e.indexOf(i):-1,[s,c]=a?[e.slice(0,l),e.slice(l+1)]:[e,""];n?t.push((0,j.jsx)("span",{"data-nextjs-container-errors-pseudo-html-line":!0,"data-nextjs-container-errors-pseudo-html--diff":"+"===i?"add":"remove",children:(0,j.jsxs)("span",{children:[s,(0,j.jsx)("span",{"data-nextjs-container-errors-pseudo-html-line-sign":!0,children:i}),c,"\n"]})},"comp-diff"+r)):t.push((0,j.jsxs)("span",{"data-nextjs-container-errors-pseudo-html-line":!0,...o?{"data-nextjs-container-errors-pseudo-html--diff":"error"}:void 0,children:[s,(0,j.jsx)("span",{"data-nextjs-container-errors-pseudo-html-line-sign":!0,children:i}),c,"\n"]},"comp-diff"+r))}),u[0]=d,u[1]=t):t=u[1];let h=t,m=!f;return u[2]!==f?(r=()=>p(!f),n=(0,j.jsx)(ry,{collapsed:f}),u[2]=f,u[3]=r,u[4]=n):(r=u[3],n=u[4]),u[5]!==m||u[6]!==r||u[7]!==n?(o=(0,j.jsx)("button",{"aria-expanded":m,"aria-label":"complete Component Stack","data-nextjs-container-errors-pseudo-html-collapse-button":!0,onClick:r,children:n}),u[5]=m,u[6]=r,u[7]=n,u[8]=o):o=u[8],u[9]===Symbol.for("react.memo_cache_sentinel")?(a=(0,j.jsxs)("span",{"data-nextjs-hydration-diff-badge-item":"client",children:[(0,j.jsx)("span",{children:"+"})," Client"]}),u[9]=a):a=u[9],u[10]===Symbol.for("react.memo_cache_sentinel")?(i=(0,j.jsxs)("div",{"data-nextjs-hydration-diff-badge":!0,children:[a,(0,j.jsxs)("span",{"data-nextjs-hydration-diff-badge-item":"server",children:[(0,j.jsx)("span",{children:"-"})," Server"]})]}),u[10]=i):i=u[10],u[11]!==o?(l=(0,j.jsxs)("div",{"data-nextjs-hydration-diff-header":!0,children:[o,i]}),u[11]=o,u[12]=l):l=u[12],u[13]!==h?(s=(0,j.jsx)("pre",{className:"nextjs__container_errors__component-stack",children:(0,j.jsx)("code",{children:h})}),u[13]=h,u[14]=s):s=u[14],u[15]!==f||u[16]!==l||u[17]!==s?(c=(0,j.jsxs)("div",{"data-nextjs-container-errors-pseudo-html":!0,"data-nextjs-container-errors-pseudo-html-collapse":f,children:[l,s]}),u[15]=f,u[16]=l,u[17]=s,u[18]=c):c=u[18],c}let rx=`
  [data-nextjs-container-errors-pseudo-html] {
    padding: 8px 0;
    margin: 8px 0;
    border: 1px solid var(--color-gray-400);
    background: var(--color-background-200);
    color: var(--color-syntax-constant);
    font-family: var(--font-stack-monospace);
    font-size: var(--size-12);
    line-height: 1.33em; /* 16px in 12px font size */
    border-radius: var(--rounded-md-2);
  }
  [data-nextjs-container-errors-pseudo-html-line] {
    display: inline-block;
    width: 100%;
    padding-left: 40px;
    line-height: calc(5 / 3);
  }
  [data-nextjs-container-errors-pseudo-html--diff='error'] {
    background: var(--color-amber-100);
    box-shadow: 2px 0 0 0 var(--color-amber-900) inset;
    font-weight: bold;
  }
  [data-nextjs-container-errors-pseudo-html-collapse-button] {
    all: unset;
    margin-left: 12px;
    &:focus {
      outline: none;
    }
  }
  [data-nextjs-container-errors-pseudo-html--diff='add'] {
    background: var(--color-green-300);
  }
  [data-nextjs-container-errors-pseudo-html-line-sign] {
    margin-left: calc(24px * -1);
    margin-right: 24px;
  }
  [data-nextjs-container-errors-pseudo-html--diff='add']
    [data-nextjs-container-errors-pseudo-html-line-sign] {
    color: var(--color-green-900);
  }
  [data-nextjs-container-errors-pseudo-html--diff='remove'] {
    background: var(--color-red-300);
  }
  [data-nextjs-container-errors-pseudo-html--diff='remove']
    [data-nextjs-container-errors-pseudo-html-line-sign] {
    color: var(--color-red-900);
    margin-left: calc(24px * -1);
    margin-right: 24px;
  }
  [data-nextjs-container-errors-pseudo-html--diff='error']
    [data-nextjs-container-errors-pseudo-html-line-sign] {
    color: var(--color-amber-900);
  }
  
  [data-nextjs-container-errors-pseudo-html--hint] {
    display: inline-block;
    font-size: 0;
    height: 0;
  }
  [data-nextjs-container-errors-pseudo-html--tag-adjacent='false'] {
    color: var(--color-accents-1);
  }
  .nextjs__container_errors__component-stack {
    margin: 0;
  }
  [data-nextjs-container-errors-pseudo-html-collapse='true']
    .nextjs__container_errors__component-stack
    code {
    max-height: 120px;
    mask-image: linear-gradient(to bottom,rgba(0,0,0,0) 0%,black 10%);
    padding-bottom: 40px;
  }
  .nextjs__container_errors__component-stack code {
    display: block;
    width: 100%;
    white-space: pre-wrap;
    scroll-snap-type: y mandatory;
    overflow-y: hidden;
  }
  [data-nextjs-container-errors-pseudo-html--diff] {
    scroll-snap-align: center;
  }
  .error-overlay-hydration-error-diff-plus-icon {
    color: var(--color-green-900);
  }
  .error-overlay-hydration-error-diff-minus-icon {
    color: var(--color-red-900);
  }
  [data-nextjs-hydration-diff-header] {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 12px 0 0;
  }
  [data-nextjs-hydration-diff-badge] {
    display: flex;
    gap: 8px;
    font-size: var(--size-12);
  }
  [data-nextjs-hydration-diff-badge-item] {
    display: flex;
    align-items: center;
    gap: 4px;
    color: var(--color-gray-900);
  }
  [data-nextjs-hydration-diff-badge-item='client'] span:first-child {
    color: var(--color-green-900);
    font-weight: bold;
  }
  [data-nextjs-hydration-diff-badge-item='server'] span:first-child {
    color: var(--color-red-900);
    font-weight: bold;
  }
`;function r_(e){let t,r,n,o,a,i,l,s,c=(0,S.c)(22),{cause:u,dialogResizerRef:d}=e;c[0]!==u?(t=u.frames(),c[0]=u,c[1]=t):t=c[1];let f=C.use(t);c[2]!==u.error.message?(r=u.error.message.trim(),c[2]=u.error.message,c[3]=r):r=c[3];let p=r,h=f.findIndex(rw),m=f[h]??null,g=u.error.name||"Error";return c[4]!==g?(n=(0,j.jsx)("div",{className:"error-cause-header",children:(0,j.jsxs)("span",{className:"error-cause-label",children:["Caused by: ",g]})}),c[4]=g,c[5]=n):n=c[5],c[6]!==p?(o=p?(0,j.jsx)("p",{className:"error-cause-message",children:p}):null,c[6]=p,c[7]=o):o=c[7],c[8]!==m?(a=m&&(0,j.jsx)(eJ,{stackFrame:m.originalStackFrame,codeFrame:m.originalCodeFrame}),c[8]=m,c[9]=a):a=c[9],c[10]!==d||c[11]!==f?(i=f.length>0&&(0,j.jsx)(rv,{dialogResizerRef:d,frames:f}),c[10]=d,c[11]=f,c[12]=i):i=c[12],c[13]!==u.cause||c[14]!==d?(l=u.cause&&(0,j.jsx)(r_,{cause:u.cause,dialogResizerRef:d}),c[13]=u.cause,c[14]=d,c[15]=l):l=c[15],c[16]!==n||c[17]!==o||c[18]!==a||c[19]!==i||c[20]!==l?(s=(0,j.jsxs)("div",{"data-nextjs-error-cause":!0,children:[n,o,a,i,l]}),c[16]=n,c[17]=o,c[18]=a,c[19]=i,c[20]=l,c[21]=s):s=c[21],s}function rw(e){return!e.ignored&&!!e.originalCodeFrame&&!!e.originalStackFrame}let rk=`
  [data-nextjs-error-cause] {
    border-top: 1px solid var(--color-gray-400);
    margin-top: 16px;
    padding-top: 16px;
  }

  .error-cause-header {
    display: flex;
    align-items: center;
    margin-bottom: 8px;
  }

  .error-cause-label {
    padding: 2px 6px;
    margin: 0;
    border-radius: var(--rounded-md-2);
    background: var(--color-red-100);
    font-weight: 600;
    font-size: var(--size-12);
    color: var(--color-red-900);
    font-family: var(--font-stack-monospace);
    line-height: var(--size-20);
  }

  .error-cause-message {
    margin: 0;
    margin-left: 4px;
    color: var(--color-red-900);
    font-weight: 500;
    font-size: var(--size-16);
    letter-spacing: -0.32px;
    line-height: var(--size-24);
    overflow-wrap: break-word;
    white-space: pre-wrap;
  }
`,rj=Symbol.for("NextjsError");function rS(e){return e[rj]||null}function rC(e){let t=e();return function(){return t}}function rE(e){let t,r,n,o,a=(0,S.c)(12),{error:i,dialogResizerRef:l}=e,s=(e=>{if(!e)return[];let t=e.frames;return C.use(t())})(i),c=s.findIndex(rT),u=s[c]??null;return a[0]!==u?(t=u&&(0,j.jsx)(eJ,{stackFrame:u.originalStackFrame,codeFrame:u.originalCodeFrame}),a[0]=u,a[1]=t):t=a[1],a[2]!==l||a[3]!==s?(r=s.length>0&&(0,j.jsx)(rv,{dialogResizerRef:l,frames:s}),a[2]=l,a[3]=s,a[4]=r):r=a[4],a[5]!==l||a[6]!==i.cause?(n=i.cause&&(0,j.jsx)(r_,{cause:i.cause,dialogResizerRef:l}),a[5]=l,a[6]=i.cause,a[7]=n):n=a[7],a[8]!==t||a[9]!==r||a[10]!==n?(o=(0,j.jsxs)(j.Fragment,{children:[t,r,n]}),a[8]=t,a[9]=r,a[10]=n,a[11]=o):o=a[11],o}function rT(e){return!e.ignored&&!!e.originalCodeFrame&&!!e.originalStackFrame}let rN=`
  ${rx}
  ${rk}
`;function rL(e){return e.startsWith("https://nextjs.org")?"nextjs-link":e.startsWith("https://")||e.startsWith("http://")?"external-link":null}function rI(e){let t,r=(0,S.c)(2),{message:n}=e;return r[0]!==n?(t=(0,j.jsx)(eI,{text:n,matcher:rL}),r[0]=n,r[1]=t):t=r[1],t}function rP(e){let t,r,n=(0,S.c)(7),{error:o}=e,a="environmentName"in o?o.environmentName:"",i=a?`[ ${a} ] `:"",l=o.message;if(l.startsWith(i)){let e;n[0]!==i.length||n[1]!==l?(e=l.slice(i.length),n[0]=i.length,n[1]=l,n[2]=e):e=n[2],l=e}return(n[3]!==l?(t=l.trim(),n[3]=l,n[4]=t):t=n[4],l=t)?(n[5]!==l?(r=(0,j.jsx)(j.Fragment,{children:(0,j.jsx)(eI,{text:l,matcher:rL})}),n[5]=l,n[6]=r):r=n[6],r):null}function rz(e){let t=(0,S.c)(20),{variant:r}=e;if("navigation"===r){let e,r,n,o,a,i,l,s,c,u;return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsxs)("h3",{className:"nextjs__blocking_page_load_error_description_title",children:["Data that blocks navigation was accessed inside"," ",(0,j.jsx)("code",{children:"generateMetadata()"})," in an otherwise prerenderable page"]}),t[0]=e):e=t[0],t[1]===Symbol.for("react.memo_cache_sentinel")?(r=(0,j.jsx)("code",{children:"fetch(...)"}),t[1]=r):r=t[1],t[2]===Symbol.for("react.memo_cache_sentinel")?(n=(0,j.jsxs)("p",{children:["When Document metadata is the only part of a page that cannot be prerendered Next.js expects you to either make it prerenderable or make some other part of the page non-prerenderable to avoid unintentional partially dynamic pages. Uncached data such as"," ",r,", cached data with a low expire time, or"," ",(0,j.jsx)("code",{children:"connection()"})," are all examples of data that only resolve on navigation."]}),o=(0,j.jsx)("h4",{children:"To fix this:"}),t[2]=n,t[3]=o):(n=t[2],o=t[3]),t[4]===Symbol.for("react.memo_cache_sentinel")?(a=(0,j.jsxs)("strong",{children:["Move the asynchronous await into a Cache Component (",(0,j.jsx)("code",{children:'"use cache"'}),")"]}),t[4]=a):a=t[4],t[5]===Symbol.for("react.memo_cache_sentinel")?(i=(0,j.jsxs)("p",{className:"nextjs__blocking_page_load_error_fix_option",children:[a,". This allows Next.js to statically prerender"," ",(0,j.jsx)("code",{children:"generateMetadata()"})," as part of the HTML document, so it's instantly visible to the user."]}),l=(0,j.jsx)("h4",{className:"nextjs__blocking_page_load_error_fix_option_separator",children:"or"}),t[5]=i,t[6]=l):(i=t[5],l=t[6]),t[7]===Symbol.for("react.memo_cache_sentinel")?(s=(0,j.jsx)("code",{children:"connection()"}),t[7]=s):s=t[7],t[8]===Symbol.for("react.memo_cache_sentinel")?(c=(0,j.jsxs)("p",{className:"nextjs__blocking_page_load_error_fix_option",children:[(0,j.jsxs)("strong",{children:["add ",s," inside a ",(0,j.jsx)("code",{children:"<Suspense>"})]})," ","somewhere in a Page or Layout. This tells Next.js that the page is intended to have some non-prerenderable parts."]}),t[8]=c):c=t[8],t[9]===Symbol.for("react.memo_cache_sentinel")?(u=(0,j.jsxs)("div",{className:"nextjs__blocking_page_load_error_description",children:[e,n,o,i,l,c,(0,j.jsxs)("p",{children:["Learn more:"," ",(0,j.jsx)("a",{href:"https://nextjs.org/docs/messages/next-prerender-dynamic-metadata",children:"https://nextjs.org/docs/messages/next-prerender-dynamic-metadata"})]})]}),t[9]=u):u=t[9],u}{let e,r,n,o,a,i,l,s,c,u;return t[10]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsxs)("h3",{className:"nextjs__blocking_page_load_error_description_title",children:["Runtime data was accessed inside ",(0,j.jsx)("code",{children:"generateMetadata()"})," or file-based metadata"]}),r=(0,j.jsx)("p",{children:"When Document metadata is the only part of a page that cannot be prerendered Next.js expects you to either make it prerenderable or make some other part of the page non-prerenderable to avoid unintentional partially dynamic pages."}),n=(0,j.jsx)("h4",{children:"To fix this:"}),t[10]=e,t[11]=r,t[12]=n):(e=t[10],r=t[11],n=t[12]),t[13]===Symbol.for("react.memo_cache_sentinel")?(o=(0,j.jsxs)("strong",{children:["Remove the Runtime data access from ",(0,j.jsx)("code",{children:"generateMetadata()"})]}),t[13]=o):o=t[13],t[14]===Symbol.for("react.memo_cache_sentinel")?(a=(0,j.jsxs)("p",{className:"nextjs__blocking_page_load_error_fix_option",children:[o,". This allows Next.js to statically prerender"," ",(0,j.jsx)("code",{children:"generateMetadata()"})," as part of the HTML document, so it's instantly visible to the user."]}),i=(0,j.jsx)("h4",{className:"nextjs__blocking_page_load_error_fix_option_separator",children:"or"}),t[14]=a,t[15]=i):(a=t[14],i=t[15]),t[16]===Symbol.for("react.memo_cache_sentinel")?(l=(0,j.jsx)("code",{children:"connection()"}),t[16]=l):l=t[16],t[17]===Symbol.for("react.memo_cache_sentinel")?(s=(0,j.jsxs)("p",{className:"nextjs__blocking_page_load_error_fix_option",children:[(0,j.jsxs)("strong",{children:["add ",l," inside a ",(0,j.jsx)("code",{children:"<Suspense>"})]})," ","somewhere in a Page or Layout. This tells Next.js that the page is intended to have some non-prerenderable parts."]}),c=(0,j.jsx)("p",{children:"Note that if you are using file-based metadata, such as icons, inside a route with dynamic params then the only recourse is to make some other part of the page non-prerenderable."}),t[17]=s,t[18]=c):(s=t[17],c=t[18]),t[19]===Symbol.for("react.memo_cache_sentinel")?(u=(0,j.jsxs)("div",{className:"nextjs__blocking_page_load_error_description",children:[e,r,n,a,i,s,c,(0,j.jsxs)("p",{children:["Learn more:"," ",(0,j.jsx)("a",{href:"https://nextjs.org/docs/messages/next-prerender-dynamic-metadata",children:"https://nextjs.org/docs/messages/next-prerender-dynamic-metadata"})]})]}),t[19]=u):u=t[19],u}}function rR(e){let t=(0,S.c)(62),{variant:r,refinement:n}=e;if("generateViewport"===n)if("navigation"===r){let e,r,n,o,a,i,l,s,c,u;return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsxs)("h3",{className:"nextjs__blocking_page_load_error_description_title",children:["Data that blocks navigation was accessed inside"," ",(0,j.jsx)("code",{children:"generateViewport()"})]}),t[0]=e):e=t[0],t[1]===Symbol.for("react.memo_cache_sentinel")?(r=(0,j.jsx)("code",{children:"fetch(...)"}),t[1]=r):r=t[1],t[2]===Symbol.for("react.memo_cache_sentinel")?(n=(0,j.jsxs)("p",{children:["Viewport metadata needs to be available on page load so accessing data that waits for a user navigation while producing it prevents Next.js from prerendering an initial UI. Uncached data such as"," ",r,", cached data with a low expire time, or"," ",(0,j.jsx)("code",{children:"connection()"})," are all examples of data that only resolve on navigation."]}),o=(0,j.jsx)("h4",{children:"To fix this:"}),t[2]=n,t[3]=o):(n=t[2],o=t[3]),t[4]===Symbol.for("react.memo_cache_sentinel")?(a=(0,j.jsxs)("strong",{children:["Move the asynchronous await into a Cache Component (",(0,j.jsx)("code",{children:'"use cache"'}),")"]}),t[4]=a):a=t[4],t[5]===Symbol.for("react.memo_cache_sentinel")?(i=(0,j.jsxs)("p",{className:"nextjs__blocking_page_load_error_fix_option",children:[a,". This allows Next.js to statically prerender"," ",(0,j.jsx)("code",{children:"generateViewport()"})," as part of the HTML document, so it's instantly visible to the user."]}),l=(0,j.jsx)("h4",{className:"nextjs__blocking_page_load_error_fix_option_separator",children:"or"}),t[5]=i,t[6]=l):(i=t[5],l=t[6]),t[7]===Symbol.for("react.memo_cache_sentinel")?(s=(0,j.jsx)("code",{children:"<Suspense>"}),t[7]=s):s=t[7],t[8]===Symbol.for("react.memo_cache_sentinel")?(c=(0,j.jsxs)("p",{className:"nextjs__blocking_page_load_error_fix_option",children:[(0,j.jsxs)("strong",{children:["Put a ",s," around your document"," ",(0,j.jsx)("code",{children:"<body>"}),"."]}),"This indicate to Next.js that you are opting into allowing blocking navigations for any page."]}),t[8]=c):c=t[8],t[9]===Symbol.for("react.memo_cache_sentinel")?(u=(0,j.jsxs)("div",{className:"nextjs__blocking_page_load_error_description",children:[e,n,o,i,l,c,(0,j.jsxs)("p",{children:["Learn more:"," ",(0,j.jsx)("a",{href:"https://nextjs.org/docs/messages/next-prerender-dynamic-viewport",children:"https://nextjs.org/docs/messages/next-prerender-dynamic-viewport"})]})]}),t[9]=u):u=t[9],u}else{let e,r,n,o,a,i,l,s,c,u,d,f,p,h;return t[10]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsxs)("h3",{className:"nextjs__blocking_page_load_error_description_title",children:["Runtime data was accessed inside ",(0,j.jsx)("code",{children:"generateViewport()"})]}),t[10]=e):e=t[10],t[11]===Symbol.for("react.memo_cache_sentinel")?(r=(0,j.jsx)("code",{children:"cookies()"}),t[11]=r):r=t[11],t[12]===Symbol.for("react.memo_cache_sentinel")?(n=(0,j.jsx)("code",{children:"headers()"}),t[12]=n):n=t[12],t[13]===Symbol.for("react.memo_cache_sentinel")?(o=(0,j.jsxs)("p",{children:["Viewport metadata needs to be available on page load so accessing data that comes from a user Request while producing it prevents Next.js from prerendering an initial UI.",r,", ",n,", and"," ",(0,j.jsx)("code",{children:"searchParams"}),", are examples of Runtime data that can only come from a user request."]}),a=(0,j.jsx)("h4",{children:"To fix this:"}),t[13]=o,t[14]=a):(o=t[13],a=t[14]),t[15]===Symbol.for("react.memo_cache_sentinel")?(i=(0,j.jsx)("strong",{children:"Remove the Runtime data requirement"}),t[15]=i):i=t[15],t[16]===Symbol.for("react.memo_cache_sentinel")?(l=(0,j.jsx)("code",{children:"generateViewport"}),t[16]=l):l=t[16],t[17]===Symbol.for("react.memo_cache_sentinel")?(s=(0,j.jsxs)("p",{className:"nextjs__blocking_page_load_error_fix_option",children:[i," from"," ",l,". This allows Next.js to statically prerender ",(0,j.jsx)("code",{children:"generateViewport()"})," as part of the HTML document, so it's instantly visible to the user."]}),c=(0,j.jsx)("h4",{className:"nextjs__blocking_page_load_error_fix_option_separator",children:"or"}),t[17]=s,t[18]=c):(s=t[17],c=t[18]),t[19]===Symbol.for("react.memo_cache_sentinel")?(u=(0,j.jsx)("code",{children:"<Suspense>"}),t[19]=u):u=t[19],t[20]===Symbol.for("react.memo_cache_sentinel")?(d=(0,j.jsxs)("p",{className:"nextjs__blocking_page_load_error_fix_option",children:[(0,j.jsxs)("strong",{children:["Put a ",u," around your document"," ",(0,j.jsx)("code",{children:"<body>"}),"."]}),"This indicate to Next.js that you are opting into allowing blocking navigations for any page."]}),f=(0,j.jsx)("code",{children:"params"}),t[20]=d,t[21]=f):(d=t[20],f=t[21]),t[22]===Symbol.for("react.memo_cache_sentinel")?(p=(0,j.jsxs)("p",{children:[f," are usually considered Runtime data but if all params are provided a value using ",(0,j.jsx)("code",{children:"generateStaticParams"})," ","they can be statically prerendered."]}),t[22]=p):p=t[22],t[23]===Symbol.for("react.memo_cache_sentinel")?(h=(0,j.jsxs)("div",{className:"nextjs__blocking_page_load_error_description",children:[e,o,a,s,c,d,p,(0,j.jsxs)("p",{children:["Learn more:"," ",(0,j.jsx)("a",{href:"https://nextjs.org/docs/messages/next-prerender-dynamic-viewport",children:"https://nextjs.org/docs/messages/next-prerender-dynamic-viewport"})]})]}),t[23]=h):h=t[23],h}if("generateMetadata"===n)if("navigation"===r){let e,r,n,o,a,i,l,s,c,u;return t[24]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsxs)("h3",{className:"nextjs__blocking_page_load_error_description_title",children:["Data that blocks navigation was accessed inside"," ",(0,j.jsx)("code",{children:"generateMetadata()"})," in an otherwise prerenderable page"]}),t[24]=e):e=t[24],t[25]===Symbol.for("react.memo_cache_sentinel")?(r=(0,j.jsx)("code",{children:"fetch(...)"}),t[25]=r):r=t[25],t[26]===Symbol.for("react.memo_cache_sentinel")?(n=(0,j.jsxs)("p",{children:["When Document metadata is the only part of a page that cannot be prerendered Next.js expects you to either make it prerenderable or make some other part of the page non-prerenderable to avoid unintentional partially dynamic pages. Uncached data such as"," ",r,", cached data with a low expire time, or"," ",(0,j.jsx)("code",{children:"connection()"})," are all examples of data that only resolve on navigation."]}),o=(0,j.jsx)("h4",{children:"To fix this:"}),t[26]=n,t[27]=o):(n=t[26],o=t[27]),t[28]===Symbol.for("react.memo_cache_sentinel")?(a=(0,j.jsxs)("strong",{children:["Move the asynchronous await into a Cache Component (",(0,j.jsx)("code",{children:'"use cache"'}),")"]}),t[28]=a):a=t[28],t[29]===Symbol.for("react.memo_cache_sentinel")?(i=(0,j.jsxs)("p",{className:"nextjs__blocking_page_load_error_fix_option",children:[a,". This allows Next.js to statically prerender"," ",(0,j.jsx)("code",{children:"generateMetadata()"})," as part of the HTML document, so it's instantly visible to the user."]}),l=(0,j.jsx)("h4",{className:"nextjs__blocking_page_load_error_fix_option_separator",children:"or"}),t[29]=i,t[30]=l):(i=t[29],l=t[30]),t[31]===Symbol.for("react.memo_cache_sentinel")?(s=(0,j.jsx)("code",{children:"connection()"}),t[31]=s):s=t[31],t[32]===Symbol.for("react.memo_cache_sentinel")?(c=(0,j.jsxs)("p",{className:"nextjs__blocking_page_load_error_fix_option",children:[(0,j.jsxs)("strong",{children:["add ",s," inside a ",(0,j.jsx)("code",{children:"<Suspense>"})]})," ","somewhere in a Page or Layout. This tells Next.js that the page is intended to have some non-prerenderable parts."]}),t[32]=c):c=t[32],t[33]===Symbol.for("react.memo_cache_sentinel")?(u=(0,j.jsxs)("div",{className:"nextjs__blocking_page_load_error_description",children:[e,n,o,i,l,c,(0,j.jsxs)("p",{children:["Learn more:"," ",(0,j.jsx)("a",{href:"https://nextjs.org/docs/messages/next-prerender-dynamic-metadata",children:"https://nextjs.org/docs/messages/next-prerender-dynamic-metadata"})]})]}),t[33]=u):u=t[33],u}else{let e,r,n,o,a,i,l,s,c,u;return t[34]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsxs)("h3",{className:"nextjs__blocking_page_load_error_description_title",children:["Runtime data was accessed inside ",(0,j.jsx)("code",{children:"generateMetadata()"})," or file-based metadata"]}),r=(0,j.jsx)("p",{children:"When Document metadata is the only part of a page that cannot be prerendered Next.js expects you to either make it prerenderable or make some other part of the page non-prerenderable to avoid unintentional partially dynamic pages."}),n=(0,j.jsx)("h4",{children:"To fix this:"}),t[34]=e,t[35]=r,t[36]=n):(e=t[34],r=t[35],n=t[36]),t[37]===Symbol.for("react.memo_cache_sentinel")?(o=(0,j.jsxs)("strong",{children:["Remove the Runtime data access from"," ",(0,j.jsx)("code",{children:"generateMetadata()"})]}),t[37]=o):o=t[37],t[38]===Symbol.for("react.memo_cache_sentinel")?(a=(0,j.jsxs)("p",{className:"nextjs__blocking_page_load_error_fix_option",children:[o,". This allows Next.js to statically prerender"," ",(0,j.jsx)("code",{children:"generateMetadata()"})," as part of the HTML document, so it's instantly visible to the user."]}),i=(0,j.jsx)("h4",{className:"nextjs__blocking_page_load_error_fix_option_separator",children:"or"}),t[38]=a,t[39]=i):(a=t[38],i=t[39]),t[40]===Symbol.for("react.memo_cache_sentinel")?(l=(0,j.jsx)("code",{children:"connection()"}),t[40]=l):l=t[40],t[41]===Symbol.for("react.memo_cache_sentinel")?(s=(0,j.jsxs)("p",{className:"nextjs__blocking_page_load_error_fix_option",children:[(0,j.jsxs)("strong",{children:["add ",l," inside a ",(0,j.jsx)("code",{children:"<Suspense>"})]})," ","somewhere in a Page or Layout. This tells Next.js that the page is intended to have some non-prerenderable parts."]}),c=(0,j.jsx)("p",{children:"Note that if you are using file-based metadata, such as icons, inside a route with dynamic params then the only recourse is to make some other part of the page non-prerenderable."}),t[41]=s,t[42]=c):(s=t[41],c=t[42]),t[43]===Symbol.for("react.memo_cache_sentinel")?(u=(0,j.jsxs)("div",{className:"nextjs__blocking_page_load_error_description",children:[e,r,n,a,i,s,c,(0,j.jsxs)("p",{children:["Learn more:"," ",(0,j.jsx)("a",{href:"https://nextjs.org/docs/messages/next-prerender-dynamic-metadata",children:"https://nextjs.org/docs/messages/next-prerender-dynamic-metadata"})]})]}),t[43]=u):u=t[43],u}if("runtime"===r){let e,r,n,o,a,i,l,s,c,u;return t[44]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsxs)("h3",{className:"nextjs__blocking_page_load_error_description_title",children:["Runtime data was accessed outside of ","<Suspense>"]}),t[44]=e):e=t[44],t[45]===Symbol.for("react.memo_cache_sentinel")?(r=(0,j.jsx)("code",{children:"cookies()"}),t[45]=r):r=t[45],t[46]===Symbol.for("react.memo_cache_sentinel")?(n=(0,j.jsx)("code",{children:"headers()"}),t[46]=n):n=t[46],t[47]===Symbol.for("react.memo_cache_sentinel")?(o=(0,j.jsxs)("p",{children:["This delays the entire page from rendering, resulting in a slow user experience. Next.js uses this error to ensure your app loads instantly on every navigation. ",r,", ",n,", and ",(0,j.jsx)("code",{children:"searchParams"}),", are examples of Runtime data that can only come from a user request."]}),a=(0,j.jsx)("h4",{children:"To fix this:"}),t[47]=o,t[48]=a):(o=t[47],a=t[48]),t[49]===Symbol.for("react.memo_cache_sentinel")?(i=(0,j.jsxs)("p",{className:"nextjs__blocking_page_load_error_fix_option",children:[(0,j.jsxs)("strong",{children:["Provide a fallback UI using ","<Suspense>"]})," around this component."]}),l=(0,j.jsx)("h4",{className:"nextjs__blocking_page_load_error_fix_option_separator",children:"or"}),t[49]=i,t[50]=l):(i=t[49],l=t[50]),t[51]===Symbol.for("react.memo_cache_sentinel")?(s=(0,j.jsx)("p",{className:"nextjs__blocking_page_load_error_fix_option",children:(0,j.jsxs)("strong",{children:["Move the Runtime data access into a deeper component wrapped in"," ","<Suspense>","."]})}),c=(0,j.jsx)("p",{children:"In either case this allows Next.js to stream its contents to the user when they request the page, while still providing an initial UI that is prerendered and prefetchable for instant navigations."}),t[51]=s,t[52]=c):(s=t[51],c=t[52]),t[53]===Symbol.for("react.memo_cache_sentinel")?(u=(0,j.jsxs)("div",{className:"nextjs__blocking_page_load_error_description",children:[e,o,a,i,l,s,c,(0,j.jsxs)("p",{children:["Learn more:"," ",(0,j.jsx)("a",{href:"https://nextjs.org/docs/messages/blocking-route",children:"https://nextjs.org/docs/messages/blocking-route"})]})]}),t[53]=u):u=t[53],u}{let e,r,n,o,a,i,l,s;return t[54]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsxs)("h3",{className:"nextjs__blocking_page_load_error_description_title",children:["Data that blocks navigation was accessed outside of ","<Suspense>"]}),t[54]=e):e=t[54],t[55]===Symbol.for("react.memo_cache_sentinel")?(r=(0,j.jsx)("code",{children:"fetch(...)"}),t[55]=r):r=t[55],t[56]===Symbol.for("react.memo_cache_sentinel")?(n=(0,j.jsxs)("p",{children:["This delays the entire page from rendering, resulting in a slow user experience. Next.js uses this error to ensure your app loads instantly on every navigation. Uncached data such as ",r,", cached data with a low expire time, or ",(0,j.jsx)("code",{children:"connection()"})," are all examples of data that only resolve on navigation."]}),o=(0,j.jsx)("h4",{children:"To fix this, you can either:"}),t[56]=n,t[57]=o):(n=t[56],o=t[57]),t[58]===Symbol.for("react.memo_cache_sentinel")?(a=(0,j.jsxs)("p",{className:"nextjs__blocking_page_load_error_fix_option",children:[(0,j.jsxs)("strong",{children:["Provide a fallback UI using ","<Suspense>"]})," around this component. This allows Next.js to stream its contents to the user as soon as it's ready, without blocking the rest of the app."]}),i=(0,j.jsx)("h4",{className:"nextjs__blocking_page_load_error_fix_option_separator",children:"or"}),t[58]=a,t[59]=i):(a=t[58],i=t[59]),t[60]===Symbol.for("react.memo_cache_sentinel")?(l=(0,j.jsxs)("p",{className:"nextjs__blocking_page_load_error_fix_option",children:[(0,j.jsxs)("strong",{children:["Move the asynchronous await into a Cache Component (",(0,j.jsx)("code",{children:'"use cache"'}),")"]}),". This allows Next.js to statically prerender the component as part of the HTML document, so it's instantly visible to the user."]}),t[60]=l):l=t[60],t[61]===Symbol.for("react.memo_cache_sentinel")?(s=(0,j.jsxs)("div",{className:"nextjs__blocking_page_load_error_description",children:[e,n,o,a,i,l,(0,j.jsxs)("p",{children:["Learn more:"," ",(0,j.jsx)("a",{href:"https://nextjs.org/docs/messages/blocking-route",children:"https://nextjs.org/docs/messages/blocking-route"})]})]}),t[61]=s):s=t[61],s}}let rO={type:"empty"};function rM(e){let t,r,n,o,a,i,l,s,c,u,d,f,p=(0,S.c)(54);p[0]!==e?({getSquashedHydrationErrorDetails:r,runtimeErrors:a,debugInfo:t,onClose:n,...o}=e,p[0]=e,p[1]=t,p[2]=r,p[3]=n,p[4]=o,p[5]=a):(t=p[1],r=p[2],n=p[3],o=p[4],a=p[5]);let h=(0,C.useRef)(null);p[6]!==r||p[7]!==a?(i={runtimeErrors:a,getSquashedHydrationErrorDetails:r},p[6]=r,p[7]=a,p[8]=i):i=p[8];let{isLoading:m,errorCode:g,errorType:v,activeIdx:y,errorDetails:b,activeError:x,setActiveIndex:_}=function(e){var t,r,n,o;let a,i,l,s=(0,S.c)(16),{runtimeErrors:c,getSquashedHydrationErrorDetails:u}=e,[d,f]=(0,C.useState)(0),p=0===c.length,h=c[d]??null,m=function(e,t){let r,n=(0,S.c)(5);r:{var o;let a,i;if(void 0===e){r=rO;break r}n[0]!==e||n[1]!==t?(a=function(e,t){var r;let n=t(e);if(null!==n)return{type:"hydration",warning:n.warning??null,notes:null,reactOutputComponentDiff:n.reactOutputComponentDiff??null};if(!(td((r=e).message)||/Hydration failed because the server rendered (text|HTML) didn't match the client\./.test(r.message)||/A tree hydrated but some attributes of the server rendered HTML didn't match the client properties./.test(r.message)))return null;let{message:o,notes:a,diff:i}=function(e){let t=e.message;if(td(t)){let[e,r=""]=t.split("\n\n"),n=r.trim();return{message:""===n?t.trim():e.trim(),diff:n,notes:null}}let[r,n]=t.split(`${ts}`),o=r.trim();if(void 0!==n&&n.length>1){let e=[];n.split("\n").forEach(t=>{""!==t.trim()&&(t.trim().startsWith("at ")||e.push(t))});let[t,...r]=o.split("\n\n");return{message:t,diff:e.join("\n"),notes:r.join("\n\n")||null}}{let[e,...t]=o.split("\n\n");return{message:e,diff:null,notes:t.join("\n\n")}}}(e);return null===o?null:{type:"hydration",warning:o,notes:a,reactOutputComponentDiff:i}}(e,t),n[0]=e,n[1]=t,n[2]=a):a=n[2];let l=a;if(l){r=l;break r}n[3]!==e?(i=(o=e).message.includes("/blocking-route")?{type:"blocking-route",variant:o.message.includes("cookies()")?"runtime":"navigation",refinement:""}:o.message.includes("/next-prerender-dynamic-metadata")?{type:"dynamic-metadata",variant:o.message.includes("cookies()")?"runtime":"navigation"}:o.message.includes("/next-prerender-dynamic-viewport")?{type:"blocking-route",variant:o.message.includes("cookies()")?"runtime":"navigation",refinement:"generateViewport"}:null,n[3]=e,n[4]=i):i=n[4];let s=i;if(s){r=s;break r}r=rO}return r}(h?.error,u);if(p||!h){let e;return s[0]!==d||s[1]!==p?(e={isLoading:p,activeIdx:d,setActiveIndex:f,activeError:null,errorDetails:null,errorCode:null,errorType:null},s[0]=d,s[1]=p,s[2]=e):e=s[2],e}let g=h.error;if(s[3]!==g){a="object"==typeof(t=g)&&null!==t&&"__NEXT_ERROR_CODE"in t&&"string"==typeof t.__NEXT_ERROR_CODE?t.__NEXT_ERROR_CODE:"object"==typeof t&&null!==t&&"digest"in t&&"string"==typeof t.digest?t.digest.split("@").find(e=>e.startsWith("E")):void 0,s[3]=g,s[4]=a}else a=s[4];let v=a;s[5]!==h.type||s[6]!==g||s[7]!==m?(r=g,n=h.type,i="blocking-route"===(o=m).type?"Blocking Route":"dynamic-metadata"===o.type?"Ambiguous Metadata":"recoverable"===n?`Recoverable ${r.name}`:"console"===n?`Console ${r.name}`:`Runtime ${r.name}`,s[5]=h.type,s[6]=g,s[7]=m,s[8]=i):i=s[8];let y=i;return s[9]!==h||s[10]!==d||s[11]!==v||s[12]!==m||s[13]!==y||s[14]!==p?(l={isLoading:p,activeIdx:d,setActiveIndex:f,activeError:h,errorDetails:m,errorCode:v,errorType:y},s[9]=h,s[10]=d,s[11]=v,s[12]=m,s[13]=y,s[14]=p,s[15]=l):l=s[15],l}(i);p[9]!==x||p[10]!==v||p[11]!==o.versionInfo?(l=async()=>{if(!x)return"";let e=[];v&&e.push(`## Error Type
${v}`);let t=x.error,r=t.message;if("environmentName"in t&&t.environmentName){let e=`[ ${t.environmentName} ] `;r.startsWith(e)&&(r=r.slice(e.length))}r&&e.push(`## Error Message
${r}`);let n=await Promise.race([x.frames(),new Promise(rF)]);if(null===n)e.push("Unable to retrieve stack frames for this error. Falling back to unsourcemapped stack\n\n"+t.stack);else{if(n.length>0){let t=n.filter(rZ);if(t.length>0){let r=t.map(rD).filter(Boolean);r.length>0&&e.push(`
${r.join("\n")}`)}}let t=n.findIndex(rA),r=n[t]??null;if(r?.originalCodeFrame){let t=eG()(eQ(r.originalCodeFrame));e.push(`## Code Frame
${t}`)}}return`${e.join("\n\n")}

Next.js version: ${o.versionInfo.installed} (${process.env.__NEXT_BUNDLER})
`},p[9]=x,p[10]=v,p[11]=o.versionInfo,p[12]=l):l=p[12];let w=l;if(m){let e;return p[13]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)(tY,{children:(0,j.jsx)(re,{})}),p[13]=e):e=p[13],e}if(!x)return null;let k=x.error,E=["server","edge-server"].includes(rS(k)||""),T=null,N=null;switch(b.type){case"hydration":{let e,t,r,n;if(p[14]!==b.warning||p[15]!==k?(e=b.warning?(0,j.jsx)(rI,{message:b.warning}):(0,j.jsx)(rP,{error:k}),p[14]=b.warning,p[15]=k,p[16]=e):e=p[16],s=e,p[17]!==b.notes?(t=b.notes?(0,j.jsx)(j.Fragment,{children:(0,j.jsx)("p",{id:"nextjs__container_errors__notes",className:"nextjs__container_errors__notes",children:b.notes})}):null,p[17]=b.notes,p[18]=t):t=p[18],p[19]!==b.warning?(r=b.warning?(0,j.jsx)("p",{id:"nextjs__container_errors__link",className:"nextjs__container_errors__link",children:(0,j.jsx)(eI,{text:`See more info here: ${tc}`})}):null,p[19]=b.warning,p[20]=r):r=p[20],p[21]!==t||p[22]!==r?(n=(0,j.jsxs)("div",{className:"error-overlay-notes-container",children:[t,r]}),p[21]=t,p[22]=r,p[23]=n):n=p[23],T=n,b.reactOutputComponentDiff){let e,t=b.reactOutputComponentDiff||"";p[24]!==t?(e=(0,j.jsx)(rb,{reactOutputComponentDiff:t}),p[24]=t,p[25]=e):e=p[25],N=e}break}case"blocking-route":{let e;p[26]!==b.refinement||p[27]!==b.variant?(e=(0,j.jsx)(rR,{variant:b.variant,refinement:b.refinement}),p[26]=b.refinement,p[27]=b.variant,p[28]=e):e=p[28],s=e;break}case"dynamic-metadata":{let e;p[29]!==b.variant?(e=(0,j.jsx)(rz,{variant:b.variant}),p[29]=b.variant,p[30]=e):e=p[30],s=e;break}case"empty":{let e;p[31]!==k?(e=(0,j.jsx)(rP,{error:k}),p[31]=k,p[32]=e):e=p[32],s=e}}let L=s,I=E?void 0:n,P=T,z=N;return p[33]===Symbol.for("react.memo_cache_sentinel")?(c=(0,j.jsx)("div",{"data-nextjs-error-suspended":!0}),p[33]=c):c=p[33],p[34]!==x.id?(u=x.id.toString(),p[34]=x.id,p[35]=u):u=p[35],p[36]!==x||p[37]!==u?(d=(0,j.jsx)(C.Suspense,{fallback:c,children:(0,j.jsx)(rE,{error:x,dialogResizerRef:h},u)}),p[36]=x,p[37]=u,p[38]=d):d=p[38],p[39]!==y||p[40]!==t||p[41]!==g||p[42]!==s||p[43]!==v||p[44]!==k||p[45]!==w||p[46]!==N||p[47]!==T||p[48]!==o||p[49]!==a||p[50]!==_||p[51]!==I||p[52]!==d?(f=(0,j.jsxs)(rt,{errorCode:g,errorType:v,errorMessage:L,onClose:I,debugInfo:t,error:k,runtimeErrors:a,activeIdx:y,setActiveIndex:_,dialogResizerRef:h,generateErrorInfo:w,...o,children:[P,z,d]}),p[39]=y,p[40]=t,p[41]=g,p[42]=s,p[43]=v,p[44]=k,p[45]=w,p[46]=N,p[47]=T,p[48]=o,p[49]=a,p[50]=_,p[51]=I,p[52]=d,p[53]=f):f=p[53],f}function rA(e){return!e.ignored&&!!e.originalCodeFrame&&!!e.originalStackFrame}function rD(e){if(e.originalStackFrame){let{methodName:t,file:r,line1:n,column1:o}=e.originalStackFrame;return`    at ${t} (${r}:${n}:${o})`}if(e.sourceStackFrame){let{methodName:t,file:r,line1:n,column1:o}=e.sourceStackFrame;return`    at ${t} (${r}:${n}:${o})`}return""}function rZ(e){return!e.ignored}function rF(e){return setTimeout(()=>e(null),2e3)}let rU=`
  .nextjs-error-with-static {
    bottom: calc(16px * 4.5);
  }
  p.nextjs__container_errors__link {
    font-size: var(--size-14);
  }
  p.nextjs__container_errors__notes {
    color: var(--color-stack-notes);
    font-size: var(--size-14);
    line-height: 1.5;
  }
  .nextjs-container-errors-body > h2:not(:first-child) {
    margin-top: calc(16px + 8px);
  }
  .nextjs-container-errors-body > h2 {
    color: var(--color-title-color);
    margin-bottom: 8px;
    font-size: var(--size-20);
  }
  .nextjs-toast-errors-parent {
    cursor: pointer;
    transition: transform 0.2s ease;
  }
  .nextjs-toast-errors-parent:hover {
    transform: scale(1.1);
  }
  .nextjs-toast-errors {
    display: flex;
    align-items: center;
    justify-content: flex-start;
  }
  .nextjs-toast-errors > svg {
    margin-right: 8px;
  }
  .nextjs-toast-hide-button {
    margin-left: 24px;
    border: none;
    background: none;
    color: var(--color-ansi-bright-white);
    padding: 0;
    transition: opacity 0.25s ease;
    opacity: 0.7;
  }
  .nextjs-toast-hide-button:hover {
    opacity: 1;
  }
  .nextjs__container_errors__error_title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
  }
  .error-overlay-notes-container {
    margin: 8px 2px;
  }
  .error-overlay-notes-container p {
    white-space: pre-wrap;
  }
  .nextjs__blocking_page_load_error_description {
    color: var(--color-stack-notes);
  }
  .nextjs__blocking_page_load_error_description_title {
    color: var(--color-title-color);
  }
  .nextjs__blocking_page_load_error_fix_option {
    background-color: var(--color-background-200);
    padding: 14px;
    border-radius: var(--rounded-md-2);
    border: 1px solid var(--color-gray-alpha-400);
  }
  .external-link, .external-link:hover {
    color:inherit;
  }
`;function r$(){let e,t=(0,S.c)(1);return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:"16",height:"16",fill:"none",children:(0,j.jsx)("path",{fill:"currentColor",fillRule:"evenodd",d:"m.191 2.063.56.498 13.5 12 .561.498.997-1.121-.56-.498-1.81-1.608 2.88-3.342v-.98l-3.204-3.72C10.645.923 6.365.686 3.594 3.08L1.748 1.44 1.188.94.19 2.063ZM14.761 8l-2.442 2.836-1.65-1.466a3.001 3.001 0 0 0-4.342-3.86l-1.6-1.422a5.253 5.253 0 0 1 7.251.682L14.76 8ZM7.526 6.576l1.942 1.727a1.499 1.499 0 0 0-1.942-1.727Zm-7.845.935 1.722-2 1.137.979L1.24 8l2.782 3.23A5.25 5.25 0 0 0 9.9 12.703l.54 1.4a6.751 6.751 0 0 1-7.555-1.892L-.318 8.49v-.98Z",clipRule:"evenodd"})}),t[0]=e):e=t[0],e}function rH(){let e,t,r=(0,S.c)(2);return r[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("g",{clipPath:"url(#light_icon_clip_path)",children:(0,j.jsx)("path",{fill:"currentColor",fillRule:"evenodd",d:"M8.75.75V0h-1.5v2h1.5V.75ZM3.26 4.32l-.53-.53-.354-.353-.53-.53 1.06-1.061.53.53.354.354.53.53-1.06 1.06Zm8.42-1.06.53-.53.353-.354.53-.53 1.061 1.06-.53.53-.354.354-.53.53-1.06-1.06ZM8 11.25a3.25 3.25 0 1 0 0-6.5 3.25 3.25 0 0 0 0 6.5Zm0 1.5a4.75 4.75 0 1 0 0-9.5 4.75 4.75 0 0 0 0 9.5Zm6-5.5h2v1.5h-2v-1.5Zm-13.25 0H0v1.5h2v-1.5H.75Zm1.62 5.32-.53.53 1.06 1.06.53-.53.354-.353.53-.53-1.06-1.061-.53.53-.354.354Zm10.2 1.06.53.53 1.06-1.06-.53-.53-.354-.354-.53-.53-1.06 1.06.53.53.353.354ZM8.75 14v2h-1.5v-2h1.5Z",clipRule:"evenodd"})}),r[0]=e):e=r[0],r[1]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsxs)("svg",{xmlns:"http://www.w3.org/2000/svg",width:"20",height:"16",viewBox:"0 0 16 16",fill:"none",children:[e,(0,j.jsx)("defs",{children:(0,j.jsx)("clipPath",{id:"light_icon_clip_path",children:(0,j.jsx)("path",{fill:"currentColor",d:"M0 0h16v16H0z"})})})]}),r[1]=t):t=r[1],t}function rV(){let e,t=(0,S.c)(1);return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("svg",{"data-testid":"geist-icon",height:"16",strokeLinejoin:"round",viewBox:"0 0 16 16",width:"16",children:(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M1.5 8.00005C1.5 5.53089 2.99198 3.40932 5.12349 2.48889C4.88136 3.19858 4.75 3.95936 4.75 4.7501C4.75 8.61609 7.88401 11.7501 11.75 11.7501C11.8995 11.7501 12.048 11.7454 12.1953 11.7361C11.0955 13.1164 9.40047 14.0001 7.5 14.0001C4.18629 14.0001 1.5 11.3138 1.5 8.00005ZM6.41706 0.577759C2.78784 1.1031 0 4.22536 0 8.00005C0 12.1422 3.35786 15.5001 7.5 15.5001C10.5798 15.5001 13.2244 13.6438 14.3792 10.9921L13.4588 9.9797C12.9218 10.155 12.3478 10.2501 11.75 10.2501C8.71243 10.2501 6.25 7.78767 6.25 4.7501C6.25 3.63431 6.58146 2.59823 7.15111 1.73217L6.41706 0.577759ZM13.25 1V1.75V2.75L14.25 2.75H15V4.25H14.25H13.25V5.25V6H11.75V5.25V4.25H10.75L10 4.25V2.75H10.75L11.75 2.75V1.75V1H13.25Z",fill:"currentColor"})}),t[0]=e):e=t[0],e}function rB(){let e,t=(0,S.c)(1);return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("svg",{width:"16",height:"16",strokeLinejoin:"round",children:(0,j.jsx)("path",{fill:"currentColor",fillRule:"evenodd",d:"M0 2a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v8.5a1 1 0 0 1-1 1H8.75v3h1.75V16h-5v-1.5h1.75v-3H1a1 1 0 0 1-1-1V2Zm1.5.5V10h13V2.5h-13Z",clipRule:"evenodd"})}),t[0]=e):e=t[0],e}let rq=["Meta","Control","Ctrl","Alt","Option","Shift"];function rW(e){let t,r,n,o,a,i,l,s,c,u,d,f,p,h=(0,S.c)(33),{value:m,onChange:g}=e,[v,y]=(0,C.useState)(!0),[b,x]=(0,C.useState)(!1);h[0]!==m?(t=m??[],h[0]=m,h[1]=t):t=h[1];let[_,w]=(0,C.useState)(t),[k,E]=(0,C.useState)(!1),T=(0,C.useRef)(null),N=(0,C.useRef)(null),L=!!m||_.length>0;h[2]!==g||h[3]!==v||h[4]!==b?(r=function(e){if(e.target!==N.current||"Tab"===e.key)return;T.current&&clearTimeout(T.current),b||x(!0),v&&(w([]),y(!1));let t=function(e){T.current=window.setTimeout(()=>{E(!0),g(e.join("+")),T.current=window.setTimeout(()=>{x(!1)},1e3)},180)};e.preventDefault(),e.stopPropagation(),w(r=>{if(r.includes(e.code)||r.includes(e.key))return r;if(!rq.includes(e.key)){let n=r.findIndex(rX);if(-1!==n){let o=[...r];return o[n]=e.code,t(o),o}let o=[...r,e.code];return t(o),o}let n=[...r],o=rq.indexOf(e.key),a=0;for(let e=0;e<n.length;e++)if(rq.includes(n[e])){if(o<rq.indexOf(n[e])){a=e;break}a=e+1}else break;return n.splice(a,0,e.key),t(n),n})},h[2]=g,h[3]=v,h[4]=b,h[5]=r):r=h[5];let I=r;h[6]!==g?(n=function(){N.current?.focus(),w([]),E(!1),setTimeout(()=>{x(!0)}),g(null)},h[6]=g,h[7]=n):n=h[7];let P=n;h[8]===Symbol.for("react.memo_cache_sentinel")?(o=function(){E(!1),x(!1),y(!0)},h[8]=o):o=h[8];let z=o;h[9]===Symbol.for("react.memo_cache_sentinel")?(a=function(){T.current&&clearTimeout(T.current),x(!0),N.current?.focus()},h[9]=a):a=h[9];let R=a;h[10]!==L||h[11]!==_?(i=L?(0,j.jsx)("div",{className:"shortcut-recorder-keys",children:_.map(rY)}):"Record Shortcut",h[10]=L,h[11]=_,h[12]=i):i=h[12],h[13]!==P||h[14]!==L?(l=L&&(0,j.jsx)("div",{className:"shortcut-recorder-clear-button",role:"button",onClick:P,onFocus:rK,onKeyDown:e=>{("Enter"===e.key||" "===e.key)&&(P(),e.stopPropagation())},"aria-label":"Clear shortcut",tabIndex:0,children:(0,j.jsx)(r0,{})}),h[13]=P,h[14]=L,h[15]=l):l=h[15],h[16]!==I||h[17]!==L||h[18]!==i||h[19]!==l?(s=(0,j.jsxs)("button",{className:"shortcut-recorder-button",ref:N,onClick:R,onFocus:R,onBlur:z,onKeyDown:I,"data-has-shortcut":L,"data-shortcut-recorder":"true",children:[i,l]}),h[16]=I,h[17]=L,h[18]=i,h[19]=l,h[20]=s):s=h[20],h[21]!==k?(c=(0,j.jsx)("div",{className:"shortcut-recorder-status-icon","data-success":k}),h[21]=k,h[22]=c):c=h[22];let O=k?"Shortcut set":"Recording";return h[23]!==O||h[24]!==c?(u=(0,j.jsxs)("div",{className:"shortcut-recorder-status",children:[c,O]}),h[23]=O,h[24]=c,h[25]=u):u=h[25],h[26]===Symbol.for("react.memo_cache_sentinel")?(d=(0,j.jsx)(rG,{}),h[26]=d):d=h[26],h[27]!==b||h[28]!==u?(f=(0,j.jsxs)("div",{className:"shortcut-recorder-tooltip","data-show":b,children:[u,d]}),h[27]=b,h[28]=u,h[29]=f):f=h[29],h[30]!==f||h[31]!==s?(p=(0,j.jsxs)("div",{className:"shortcut-recorder",children:[s,f]}),h[30]=f,h[31]=s,h[32]=p):p=h[32],p}function rK(e){return e.stopPropagation()}function rY(e){return(0,j.jsx)(rQ,{children:e},e)}function rX(e){return!rq.includes(e)}function rG(){let e,t=(0,S.c)(1);return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("svg",{fill:"none",height:"6",viewBox:"0 0 14 6",width:"14",xmlns:"http://www.w3.org/2000/svg",children:(0,j.jsx)("path",{d:"M13.8284 0H0.17157C0.702003 0 1.21071 0.210714 1.58578 0.585787L5.58578 4.58579C6.36683 5.36684 7.63316 5.36683 8.41421 4.58579L12.4142 0.585786C12.7893 0.210714 13.298 0 13.8284 0Z",fill:"var(--background)"})}),t[0]=e):e=t[0],e}function rQ(e){let t,r,n,o,a=(0,S.c)(9),{children:i}=e;a[0]!==i?(t=function(e){switch(e){case"Meta":return(0,j.jsx)(rJ,{});case"Alt":case"Option":return"⌥";case"Control":case"Ctrl":return"Ctrl";case"Shift":return"⇧";case"Enter":return"⏎";case"Escape":case"Esc":return"Esc";case" ":case"Space":case"Spacebar":return"Space";case"ArrowUp":return"↑";case"ArrowDown":return"↓";case"ArrowLeft":return"←";case"ArrowRight":return"→";case"Tab":return"Tab";case"Backspace":return"⌫";case"Delete":return"⌦";default:if(1===i.length)return i.toUpperCase();return i}},a[0]=i,a[1]=t):t=a[1];let l=t;if(a[2]!==i||a[3]!==l){let e=l(i);r="string"==typeof e&&1===e.length,n=function(e){if("string"!=typeof e)return e;let t={Minus:"-",Equal:"=",BracketLeft:"[",BracketRight:"]",Backslash:"\\",Semicolon:";",Quote:"'",Comma:",",Period:".",Backquote:"`",Space:" ",Slash:"/",IntlBackslash:"\\"};return t[e]?t[e]:/^Key([A-Z])$/.test(e)?e.replace(/^Key/,""):/^Digit([0-9])$/.test(e)?e.replace(/^Digit/,""):/^Numpad([0-9])$/.test(e)?e.replace(/^Numpad/,""):"NumpadAdd"===e?"+":"NumpadSubtract"===e?"-":"NumpadMultiply"===e?"*":"NumpadDivide"===e?"/":"NumpadDecimal"===e?".":"NumpadEnter"===e?"Enter":e}(e),a[2]=i,a[3]=l,a[4]=r,a[5]=n}else r=a[4],n=a[5];return a[6]!==r||a[7]!==n?(o=(0,j.jsx)("kbd",{"data-symbol":r,children:n}),a[6]=r,a[7]=n,a[8]=o):o=a[8],o}function rJ(){let e,t=(0,S.c)(1),r=r2(/^Mac/)||r2(/^iPhone/)||r2(/^iPad/)||r2(/^Mac/)&&navigator.maxTouchPoints>1?"⌘":"Ctrl";return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("span",{style:{minWidth:"1em",display:"inline-block"},children:r}),t[0]=e):e=t[0],e}function r0(){let e,t=(0,S.c)(1);return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("svg",{height:"16",strokeLinejoin:"round",viewBox:"0 0 16 16",width:"16",children:(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M12.4697 13.5303L13 14.0607L14.0607 13L13.5303 12.4697L9.06065 7.99999L13.5303 3.53032L14.0607 2.99999L13 1.93933L12.4697 2.46966L7.99999 6.93933L3.53032 2.46966L2.99999 1.93933L1.93933 2.99999L2.46966 3.53032L6.93933 7.99999L2.46966 12.4697L1.93933 13L2.99999 14.0607L3.53032 13.5303L7.99999 9.06065L12.4697 13.5303Z",fill:"currentColor"})}),t[0]=e):e=t[0],e}let r1=e_`
  .shortcut-recorder {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    position: relative;
    font-family: var(--font-stack-sans);

    .shortcut-recorder-button {
      display: flex;
      align-items: center;
      gap: 4px;
      background: transparent;
      border: 1px dashed var(--color-gray-500);
      border-radius: var(--rounded-lg);
      padding: 6px 8px;
      font-weight: 400;
      font-size: var(--size-14);
      color: var(--color-gray-1000);
      transition: border-color 150ms var(--timing-swift);

      &[data-has-shortcut='true'] {
        border: 1px solid var(--color-gray-alpha-400);

        &:hover {
          border-color: var(--color-gray-500);
        }
      }

      &:hover {
        border-color: var(--color-gray-600);
      }

      &::placeholder {
        color: var(--color-gray-900);
      }

      &[data-pristine='false']::placeholder {
        color: transparent;
      }

      &:focus-visible {
        outline: var(--focus-ring);
        outline-offset: -1px;
      }
    }

    kbd {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-stack-sans);
      background: var(--color-gray-200);
      min-width: 20px;
      height: 20px;
      font-size: 14px;
      border-radius: 4px;
      color: var(--color-gray-1000);

      &[data-symbol='false'] {
        padding: 0 4px;
      }
    }

    .shortcut-recorder-clear-button {
      cursor: pointer;
      color: var(--color-gray-1000);
      width: 20px;
      height: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 4px;
      transition: background 150ms var(--timing-swift);

      &:hover {
        background: var(--color-gray-300);
      }

      &:focus-visible {
        outline: var(--focus-ring);
      }

      svg {
        width: 14px;
        height: 14px;
      }
    }
  }

  .shortcut-recorder-keys {
    pointer-events: none;
    user-select: none;
    display: flex;
    align-items: center;
    gap: 2px;
  }

  .shortcut-recorder-tooltip {
    --gap: 8px;
    --background: var(--color-gray-1000);
    background: var(--background);
    color: var(--color-background-100);
    font-size: var(--size-14);
    padding: 4px 8px;
    border-radius: 8px;
    position: absolute;
    bottom: calc(100% + var(--gap));
    text-align: center;
    opacity: 0;
    scale: 0.96;
    white-space: nowrap;
    user-select: none;
    transition:
      opacity 150ms var(--timing-swift),
      scale 150ms var(--timing-swift);

    &[data-show='true'] {
      opacity: 1;
      scale: 1;
    }

    svg {
      position: absolute;
      transform: translateX(-50%);
      bottom: -6px;
      left: 50%;
    }

    .shortcut-recorder-status {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .shortcut-recorder-status-icon {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      flex-shrink: 0;
      background: var(--color-red-700);

      &[data-success='true'] {
        background: var(--color-green-700);
      }
    }
  }
`;function r2(e){return null!=window.navigator?e.test(window.navigator.platform):void 0}var r3=__webpack_require__("./dist/compiled/zod/index.cjs");let r4=r3.z.object({theme:r3.z.enum(["light","dark","system"]).optional(),disableDevIndicator:r3.z.boolean().optional(),devToolsPosition:r3.z.enum(["top-left","top-right","bottom-left","bottom-right"]).optional(),devToolsPanelPosition:r3.z.record(r3.z.string(),r3.z.enum(["top-left","top-right","bottom-left","bottom-right"])).optional(),devToolsPanelSize:r3.z.record(r3.z.string(),r3.z.object({width:r3.z.number(),height:r3.z.number()})).optional(),scale:r3.z.number().optional(),hideShortcut:r3.z.string().nullable().optional()}),r5={},r6=null;function r9(){if(0===Object.keys(r5).length)return;let e=JSON.stringify(r5);r5={},fetch("/__nextjs_devtools_config",{method:"POST",headers:{"Content-Type":"application/json"},body:e,keepalive:!0}).catch(t=>{console.warn("[Next.js DevTools] Failed to save config:",{data:e,error:t})})}function r8(e){let t=r4.safeParse(e);t.success?(r5=function e(t,r){if(!r||"object"!=typeof r||Array.isArray(r)||!t||"object"!=typeof t||Array.isArray(t))return r;let n={...t};for(let o in r){let a=r[o],i=t[o];void 0!==a&&(a&&"object"==typeof a&&!Array.isArray(a)&&i&&"object"==typeof i&&!Array.isArray(i)?n[o]=e(i,a):n[o]=a)}return n}(r5,e),r6&&clearTimeout(r6),r6=setTimeout(r9,120)):console.warn("[Next.js DevTools] Invalid config patch:",t.error.message)}function r7(e){let t,r,n,o,a,i,l,s,c,u,d,f,p,h,m,g,v,y,b,x,_,w,k,E,T,N,L,I,P,z,R,O,M,D,Z=(0,S.c)(61),{theme:F,hide:U,hideShortcut:$,setHideShortcut:H,scale:V,setPosition:B,setScale:q,position:W}=e,{restartServer:K,isPending:Y}=function(){let[e,t]=(0,C.useState)(!1);return{restartServer:async({invalidateFileSystemCache:e})=>{t(!0);let r=!1;try{let t=await fetch("/__nextjs_server_status").then(e=>e.json()).then(e=>e.executionId).catch(e=>(console.log("[Next.js DevTools] Failed to fetch server status while restarting dev server.",e),null));if(!t)return void console.log("[Next.js DevTools] Failed to get the current server execution ID while restarting dev server.");let n=await fetch(e?"/__nextjs_restart_dev?invalidateFileSystemCache=1":"/__nextjs_restart_dev",{method:"POST"});if(!n.ok)return void console.log("[Next.js DevTools] Failed to fetch restart server endpoint. Status:",n.status);for(let e=0;e<10;e++){await new Promise(e=>setTimeout(e,1e3));try{let e=await fetch("/__nextjs_server_status").then(e=>e.json()).then(e=>e.executionId);if(t!==e){r=!0,window.location.reload();return}}catch(e){continue}}console.log("[Next.js DevTools] Failed to restart server. Exhausted all polling attempts.");return}catch(e){console.log("[Next.js DevTools] Failed to restart server.",e);return}finally{r||t(!1)}},isPending:e}}(),{shadowRoot:X}=us();Z[0]!==X.host?(t=e=>{let t=X.host;if("system"===e.target.value){t.classList.remove("dark"),t.classList.remove("light"),r8({theme:"system"});return}"dark"===e.target.value?(t.classList.add("dark"),t.classList.remove("light"),r8({theme:"dark"})):(t.classList.remove("dark"),t.classList.add("light"),r8({theme:"light"}))},Z[0]=X.host,Z[1]=t):t=Z[1];let G=t;Z[2]!==B?(r=function(e){B(e.target.value),r8({devToolsPosition:e.target.value})},Z[2]=B,Z[3]=r):r=Z[3];let Q=r;Z[4]!==q?(n=function(e){let{target:t}=e,r=Number(t.value);q(r),r8({scale:r})},Z[4]=q,Z[5]=n):n=Z[5];let J=n;return Z[6]===Symbol.for("react.memo_cache_sentinel")?(o=(0,j.jsxs)("div",{className:"preference-header",children:[(0,j.jsx)("label",{htmlFor:"theme",children:"Theme"}),(0,j.jsx)("p",{className:"preference-description",children:"Select your theme preference."})]}),Z[6]=o):o=Z[6],Z[7]!==F?(a=(0,j.jsx)(nr,{theme:F}),Z[7]=F,Z[8]=a):a=Z[8],Z[9]===Symbol.for("react.memo_cache_sentinel")?(i=(0,j.jsx)("option",{value:"system",children:"System"}),l=(0,j.jsx)("option",{value:"light",children:"Light"}),s=(0,j.jsx)("option",{value:"dark",children:"Dark"}),Z[9]=i,Z[10]=l,Z[11]=s):(i=Z[9],l=Z[10],s=Z[11]),Z[12]!==G||Z[13]!==a||Z[14]!==F?(c=(0,j.jsxs)("div",{className:"preference-section",children:[o,(0,j.jsxs)(nt,{id:"theme",name:"theme",prefix:a,value:F,onChange:G,children:[i,l,s]})]}),Z[12]=G,Z[13]=a,Z[14]=F,Z[15]=c):c=Z[15],Z[16]===Symbol.for("react.memo_cache_sentinel")?(u=(0,j.jsxs)("div",{className:"preference-header",children:[(0,j.jsx)("label",{htmlFor:"position",children:"Position"}),(0,j.jsx)("p",{className:"preference-description",children:"Adjust the placement of your dev tools."})]}),Z[16]=u):u=Z[16],Z[17]===Symbol.for("react.memo_cache_sentinel")?(d=(0,j.jsx)("option",{value:"bottom-left",children:"Bottom Left"}),f=(0,j.jsx)("option",{value:"bottom-right",children:"Bottom Right"}),p=(0,j.jsx)("option",{value:"top-left",children:"Top Left"}),h=(0,j.jsx)("option",{value:"top-right",children:"Top Right"}),Z[17]=d,Z[18]=f,Z[19]=p,Z[20]=h):(d=Z[17],f=Z[18],p=Z[19],h=Z[20]),Z[21]!==Q||Z[22]!==W?(m=(0,j.jsxs)("div",{className:"preference-section",children:[u,(0,j.jsxs)(nt,{id:"position",name:"position",value:W,onChange:Q,children:[d,f,p,h]})]}),Z[21]=Q,Z[22]=W,Z[23]=m):m=Z[23],Z[24]===Symbol.for("react.memo_cache_sentinel")?(g=(0,j.jsxs)("div",{className:"preference-header",children:[(0,j.jsx)("label",{htmlFor:"size",children:"Size"}),(0,j.jsx)("p",{className:"preference-description",children:"Adjust the size of your dev tools."})]}),Z[24]=g):g=Z[24],Z[25]===Symbol.for("react.memo_cache_sentinel")?(v=Object.entries(A).map(ne),Z[25]=v):v=Z[25],Z[26]!==J||Z[27]!==V?(y=(0,j.jsxs)("div",{className:"preference-section",children:[g,(0,j.jsx)(nt,{id:"size",name:"size",value:V,onChange:J,children:v})]}),Z[26]=J,Z[27]=V,Z[28]=y):y=Z[28],Z[29]===Symbol.for("react.memo_cache_sentinel")?(b=(0,j.jsxs)("div",{className:"preference-header",children:[(0,j.jsx)("label",{id:"hide-dev-tools",children:"Hide Dev Tools for this session"}),(0,j.jsx)("p",{className:"preference-description",children:"Hide Dev Tools until you restart your dev server, or 1 day."})]}),Z[29]=b):b=Z[29],Z[30]===Symbol.for("react.memo_cache_sentinel")?(x=(0,j.jsx)(r$,{}),_=(0,j.jsx)("span",{children:"Hide"}),Z[30]=x,Z[31]=_):(x=Z[30],_=Z[31]),Z[32]!==U?(w=(0,j.jsxs)("div",{className:"preference-section",children:[b,(0,j.jsx)("div",{className:"preference-control",children:(0,j.jsxs)("button",{"aria-describedby":"hide-dev-tools",name:"hide-dev-tools","data-hide-dev-tools":!0,className:"action-button",onClick:U,children:[x,_]})})]}),Z[32]=U,Z[33]=w):w=Z[33],Z[34]===Symbol.for("react.memo_cache_sentinel")?(k=(0,j.jsxs)("div",{className:"preference-header",children:[(0,j.jsx)("label",{id:"hide-dev-tools",children:"Hide Dev Tools shortcut"}),(0,j.jsx)("p",{className:"preference-description",children:"Set a custom keyboard shortcut to toggle visibility."})]}),Z[34]=k):k=Z[34],Z[35]!==$?(E=$?.split("+")??null,Z[35]=$,Z[36]=E):E=Z[36],Z[37]!==H||Z[38]!==E?(T=(0,j.jsxs)("div",{className:"preference-section",children:[k,(0,j.jsx)("div",{className:"preference-control",children:(0,j.jsx)(rW,{value:E,onChange:H})})]}),Z[37]=H,Z[38]=E,Z[39]=T):T=Z[39],Z[40]===Symbol.for("react.memo_cache_sentinel")?(N=(0,j.jsx)("label",{children:"Disable Dev Tools for this project"}),Z[40]=N):N=Z[40],Z[41]===Symbol.for("react.memo_cache_sentinel")?(L=(0,j.jsx)("code",{className:"dev-tools-info-code",children:"devIndicators: false"}),Z[41]=L):L=Z[41],Z[42]===Symbol.for("react.memo_cache_sentinel")?(I=(0,j.jsx)("div",{className:"preference-section",children:(0,j.jsxs)("div",{className:"preference-header",children:[N,(0,j.jsxs)("p",{className:"preference-description",children:["To disable this UI completely, set"," ",L," in your ",(0,j.jsx)("code",{className:"dev-tools-info-code",children:"next.config"})," file."]})]})}),Z[42]=I):I=Z[42],Z[43]===Symbol.for("react.memo_cache_sentinel")?(P=(0,j.jsxs)("div",{className:"preference-header",children:[(0,j.jsx)("label",{id:"restart-dev-server",children:"Restart Dev Server"}),(0,j.jsx)("p",{className:"preference-description",children:"Restarts the development server without needing to leave the browser."})]}),Z[43]=P):P=Z[43],Z[44]!==K?(z=()=>K({invalidateFileSystemCache:!1}),Z[44]=K,Z[45]=z):z=Z[45],Z[46]===Symbol.for("react.memo_cache_sentinel")?(R=(0,j.jsx)("span",{children:"Restart"}),Z[46]=R):R=Z[46],Z[47]!==Y||Z[48]!==z?(O=(0,j.jsxs)("div",{className:"preference-section",children:[P,(0,j.jsx)("div",{className:"preference-control",children:(0,j.jsx)("button",{"aria-describedby":"restart-dev-server",title:"Restarts the development server without needing to leave the browser.",name:"restart-dev-server","data-restart-dev-server":!0,className:"action-button",onClick:z,disabled:Y,children:R})})]}),Z[47]=Y,Z[48]=z,Z[49]=O):O=Z[49],Z[50]!==Y||Z[51]!==K?(M=process.env.__NEXT_BUNDLER_HAS_PERSISTENT_CACHE?(0,j.jsxs)("div",{className:"preference-section",children:[(0,j.jsxs)("div",{className:"preference-header",children:[(0,j.jsx)("label",{id:"reset-bundler-cache",children:"Reset Bundler Cache"}),(0,j.jsx)("p",{className:"preference-description",children:"Clears the bundler cache and restarts the dev server. Helpful if you are seeing stale errors or changes are not appearing."})]}),(0,j.jsx)("div",{className:"preference-control",children:(0,j.jsx)("button",{"aria-describedby":"reset-bundler-cache",title:"Clears the bundler cache and restarts the dev server. Helpful if you are seeing stale errors or changes are not appearing.",name:"reset-bundler-cache","data-reset-bundler-cache":!0,className:"action-button",onClick:()=>K({invalidateFileSystemCache:!0}),disabled:Y,children:(0,j.jsx)("span",{children:"Reset Cache"})})})]}):null,Z[50]=Y,Z[51]=K,Z[52]=M):M=Z[52],Z[53]!==c||Z[54]!==m||Z[55]!==y||Z[56]!==w||Z[57]!==T||Z[58]!==O||Z[59]!==M?(D=(0,j.jsxs)("div",{className:"preferences-container",children:[c,m,y,w,T,I,O,M]}),Z[53]=c,Z[54]=m,Z[55]=y,Z[56]=w,Z[57]=T,Z[58]=O,Z[59]=M,Z[60]=D):D=Z[60],D}function ne(e){let[t,r]=e;return(0,j.jsx)("option",{value:r,children:t},t)}function nt(e){let t,r,n,o,a,i,l=(0,S.c)(11);return l[0]!==e?({children:t,prefix:r,...n}=e,l[0]=e,l[1]=t,l[2]=r,l[3]=n):(t=l[1],r=l[2],n=l[3]),l[4]!==t||l[5]!==n?(o=(0,j.jsx)("select",{...n,children:t}),l[4]=t,l[5]=n,l[6]=o):o=l[6],l[7]===Symbol.for("react.memo_cache_sentinel")?(a=(0,j.jsx)(no,{}),l[7]=a):a=l[7],l[8]!==r||l[9]!==o?(i=(0,j.jsxs)("div",{className:"select-button",children:[r,o,a]}),l[8]=r,l[9]=o,l[10]=i):i=l[10],i}function nr(e){let t=(0,S.c)(3),{theme:r}=e;switch(r){case"system":{let e;return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)(rB,{}),t[0]=e):e=t[0],e}case"dark":{let e;return t[1]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)(rV,{}),t[1]=e):e=t[1],e}case"light":{let e;return t[2]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)(rH,{}),t[2]=e):e=t[2],e}default:return null}}let nn=e_`
  .preferences-container {
    width: 100%;
  }

  @media (min-width: 576px) {
    .preferences-container {
      width: 480px;
    }
  }

  .preference-section:first-child {
    padding-top: 0;
  }

  .preference-section {
    padding: 12px 0;
    border-bottom: 1px solid var(--color-gray-400);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 24px;
  }

  .preference-section:last-child {
    border-bottom: none;
  }

  .preference-header {
    margin-bottom: 0;
    flex: 1;
  }

  .preference-header label {
    font-size: var(--size-14);
    font-weight: 500;
    color: var(--color-gray-1000);
    margin: 0;
  }

  .preference-description {
    color: var(--color-gray-900);
    font-size: var(--size-14);
    margin: 0;
  }

  .select-button,
  .action-button {
    display: flex;
    align-items: center;
    gap: 8px;
    background: var(--color-background-100);
    border: 1px solid var(--color-gray-400);
    border-radius: var(--rounded-lg);
    font-weight: 400;
    font-size: var(--size-14);
    color: var(--color-gray-1000);
    padding: 6px 8px;
    transition: border-color 150ms var(--timing-swift);

    &:hover {
      border-color: var(--color-gray-500);
    }

    svg {
      width: 14px;
      height: 14px;
      overflow: visible;
    }
  }

  .select-button {
    &:focus-within {
      outline: var(--focus-ring);
      outline-offset: -1px;
    }

    select {
      all: unset;
    }

    option {
      color: var(--color-gray-1000);
      background: var(--color-background-100);
    }
  }

  .preference-section button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  :global(.icon) {
    width: 18px;
    height: 18px;
    color: #666;
  }
`;function no(){let e,t=(0,S.c)(1);return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("svg",{width:"16",height:"16",viewBox:"0 0 16 16","aria-hidden":!0,children:(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M14.0607 5.49999L13.5303 6.03032L8.7071 10.8535C8.31658 11.2441 7.68341 11.2441 7.29289 10.8535L2.46966 6.03032L1.93933 5.49999L2.99999 4.43933L3.53032 4.96966L7.99999 9.43933L12.4697 4.96966L13 4.43933L14.0607 5.49999Z",fill:"currentColor"})}),t[0]=e):e=t[0],e}function na(){return(0,j.jsx)("style",{children:e_`
        ${tn}
        ${rp}
        ${rg}
        ${t3}
        ${rn}
        ${e5}
        ${rr}
        ${tk}
        ${t1}
        ${tI}
        ${e2}
        ${rl}
        ${ra}
        ${""}
        ${rU}
        ${rN}
        ${tR}
        ${nn}
        ${t8}
        ${r1}
      `})}function ni(e,t){let r,n,o,a,i=(0,S.c)(10),l=void 0!==e&&e;i[0]!==t?(r=void 0===t?{}:t,i[0]=t,i[1]=r):r=i[1];let s=r,[c,u]=(0,C.useState)(l),[d,f]=(0,C.useState)(!1),{enterDelay:p,exitDelay:h}=s,m=void 0===p?1:p,g=void 0===h?0:h;return i[2]!==l||i[3]!==m||i[4]!==g?(n=()=>{let e,t;return l?(u(!0),m<=0?f(!0):e=setTimeout(()=>{f(!0)},m)):(f(!1),g<=0?u(!1):t=setTimeout(()=>{u(!1)},g)),()=>{clearTimeout(e),clearTimeout(t)}},o=[l,m,g],i[2]=l,i[3]=m,i[4]=g,i[5]=n,i[6]=o):(n=i[5],o=i[6]),(0,C.useEffect)(n,o),i[7]!==c||i[8]!==d?(a={mounted:c,rendered:d},i[7]=c,i[8]=d,i[9]=a):a=i[9],a}function nl(e){let t,r,n,o,a,i=(0,S.c)(19),{state:l,dispatch:s,getSquashedHydrationErrorDetails:c,runtimeErrors:u,errorCount:d}=e,f=!!process.env.TURBOPACK;i[0]===Symbol.for("react.memo_cache_sentinel")?(t={exitDelay:200},i[0]=t):t=i[0];let{mounted:p,rendered:h}=ni(l.isErrorOverlayOpen,t);i[1]!==d||i[2]!==h||i[3]!==l.versionInfo?(r={rendered:h,transitionDurationMs:200,isTurbopack:f,versionInfo:l.versionInfo,errorCount:d},i[1]=d,i[2]=h,i[3]=l.versionInfo,i[4]=r):r=i[4];let m=r;if(null!==l.buildError){let e;return i[5]!==m||i[6]!==l.buildError?(e=(0,j.jsx)(ru,{...m,message:l.buildError,rendered:!0}),i[5]=m,i[6]=l.buildError,i[7]=e):e=i[7],e}if(!u.length)return null;let g=p?"visible":"hidden";return i[8]!==s?(n=()=>{s({type:G})},i[8]=s,i[9]=n):n=i[9],i[10]!==m||i[11]!==c||i[12]!==u||i[13]!==l.debugInfo||i[14]!==n?(o=(0,j.jsx)(rM,{...m,debugInfo:l.debugInfo,getSquashedHydrationErrorDetails:c,runtimeErrors:u,onClose:n}),i[10]=m,i[11]=c,i[12]=u,i[13]=l.debugInfo,i[14]=n,i[15]=o):o=i[15],i[16]!==g||i[17]!==o?(a=(0,j.jsx)(C.Activity,{mode:g,children:o}),i[16]=g,i[17]=o,i[18]=a):a=i[18],a}let ns=e=>{let t=(0,S.c)(4),{state:r}=e;if(r.buildError){let r;return t[0]!==e?(r=(0,j.jsx)(nu,{...e}),t[0]=e,t[1]=r):r=t[1],r}{let r;return t[2]!==e?(r=(0,j.jsx)(nc,{...e}),t[2]=e,t[3]=r):r=t[3],r}},nc=e=>{let t,r,n,o,a,i=(0,S.c)(12),{children:l,state:s,isAppDir:c}=e,{errors:u}=s;i[0]===Symbol.for("react.memo_cache_sentinel")?(t={},i[0]=t):t=i[0];let[d,f]=(0,C.useState)(t);if(i[1]!==u||i[2]!==d){let e=[],t=null;for(let r=0;r<u.length;++r){let n=u[r],{id:o}=n;if(o in d){e.push(d[o]);continue}t=n;break}r=[e,t],i[1]=u,i[2]=d,i[3]=r}else r=i[3];let[p,h]=r;i[4]!==c||i[5]!==h?(n=()=>{var e,t;if(null==h)return;let r=(e=h,t=c,{id:e.id,runtime:!0,error:e.error,type:e.type,frames:rC(async()=>await eM(e.frames,rS(e.error),t)),cause:function e(t,r,n=0){if(n>=5)return;let o=t.cause;if(!(o instanceof Error))return;let a=L(o.stack||"");return{error:o,frames:rC(async()=>await eM(a,rS(o),r)),cause:e(o,r,n+1)}}(e.error,t)});f(e=>({...e,[r.id]:r}))},o=[h,c],i[4]=c,i[5]=h,i[6]=n,i[7]=o):(n=i[6],o=i[7]),(0,C.useEffect)(n,o);let m=u.length;return i[8]!==l||i[9]!==p||i[10]!==m?(a=l({runtimeErrors:p,totalErrorCount:m}),i[8]=l,i[9]=p,i[10]=m,i[11]=a):a=i[11],a},nu=({children:e})=>e({runtimeErrors:[],totalErrorCount:1});function nd(){let e,t,r=(0,S.c)(4),{shadowRoot:n,state:o}=us();return r[0]!==n||r[1]!==o.scale?(e=()=>{n?.host&&n.host.style.setProperty("--nextjs-dev-tools-scale",String(o.scale||1))},t=[n,o.scale],r[0]=n,r[1]=o.scale,r[2]=e,r[3]=t):(e=r[2],t=r[3]),(0,C.useLayoutEffect)(e,t),null}var nf=__webpack_require__("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/components/devtools-indicator/devtools-indicator.css"),np={};function nh(e){let t,r,n=(0,S.c)(3);return n[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M3.08889 11.8384L2.62486 12.3024L1.69678 11.3744L2.16082 10.9103L6.07178 6.99937L2.16082 3.08841L1.69678 2.62437L2.62486 1.69629L3.08889 2.16033L6.99986 6.07129L10.9108 2.16033L11.3749 1.69629L12.3029 2.62437L11.8389 3.08841L7.92793 6.99937L11.8389 10.9103L12.3029 11.3744L11.3749 12.3024L10.9108 11.8384L6.99986 7.92744L3.08889 11.8384Z",fill:"currentColor"}),n[0]=t):t=n[0],n[1]!==e?(r=(0,j.jsx)("svg",{width:"12",height:"12",viewBox:"0 0 14 14",fill:"none",xmlns:"http://www.w3.org/2000/svg",...e,children:t}),n[1]=e,n[2]=r):r=n[2],r}function nm(e){let t,r,n=(0,S.c)(3);return n[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M3.98071 1.125L1.125 3.98071L1.125 8.01929L3.98071 10.875H8.01929L10.875 8.01929V3.98071L8.01929 1.125H3.98071ZM3.82538 0C3.62647 0 3.4357 0.0790176 3.29505 0.21967L0.21967 3.29505C0.0790176 3.4357 0 3.62647 0 3.82538V8.17462C0 8.37353 0.0790178 8.5643 0.21967 8.70495L3.29505 11.7803C3.4357 11.921 3.62647 12 3.82538 12H8.17462C8.37353 12 8.5643 11.921 8.70495 11.7803L11.7803 8.70495C11.921 8.5643 12 8.37353 12 8.17462V3.82538C12 3.62647 11.921 3.4357 11.7803 3.29505L8.70495 0.21967C8.5643 0.0790177 8.37353 0 8.17462 0H3.82538ZM6.5625 2.8125V3.375V6V6.5625H5.4375V6V3.375V2.8125H6.5625ZM6 9C6.41421 9 6.75 8.66421 6.75 8.25C6.75 7.83579 6.41421 7.5 6 7.5C5.58579 7.5 5.25 7.83579 5.25 8.25C5.25 8.66421 5.58579 9 6 9Z",fill:"currentColor"}),n[0]=t):t=n[0],n[1]!==e?(r=(0,j.jsx)("svg",{width:"12",height:"12",viewBox:"0 0 12 12",fill:"none",xmlns:"http://www.w3.org/2000/svg",...e,children:t}),n[1]=e,n[2]=r):r=n[2],r}np.styleTagTransform=b(),np.setAttributes=m(),np.insert=p(),np.domAPI=d(),np.insertStyleElement=v(),c()(nf.A,np),nf.A&&nf.A.locals&&nf.A.locals;let ng=(0,C.createContext)(null),nv=()=>(0,C.useContext)(ng);function ny(e){return nR+36/e.scale+9}var nb=((n={}).None="none",n.Rendering="rendering",n.Compiling="compiling",n.Prerendering="prerendering",n.CacheBypassing="cache-bypassing",n);function nx(e){let t,r,n,o,a,i,l=(0,S.c)(13),{status:s,onClick:c}=e;l[0]===Symbol.for("react.memo_cache_sentinel")?(t={none:"","cache-bypassing":"Cache disabled",prerendering:"Prerendering",compiling:"Compiling",rendering:"Rendering"},l[0]=t):t=l[0];let u=t;l[1]===Symbol.for("react.memo_cache_sentinel")?(r={none:"","cache-bypassing":"",prerendering:"#f5a623",compiling:"#f5a623",rendering:"#50e3c2"},l[1]=r):r=l[1];let d=r;if("none"===s)return null;l[2]===Symbol.for("react.memo_cache_sentinel")?(n=(0,j.jsx)("style",{children:e_`
          [data-indicator-status] {
            --padding-left: 8px;
            display: flex;
            gap: 6px;
            align-items: center;
            padding-left: 12px;
            padding-right: 8px;
            height: var(--size-32);
            margin-right: 2px;
            border-radius: var(--rounded-full);
            transition: background var(--duration-short) ease;
            color: white;
            font-size: var(--size-13);
            font-weight: 500;
            white-space: nowrap;
            border: none;
            background: transparent;
            cursor: pointer;
            outline: none;
          }

          [data-indicator-status]:focus-visible {
            outline: 2px solid var(--color-blue-800, #3b82f6);
            outline-offset: 3px;
          }

          [data-status-dot] {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            flex-shrink: 0;
          }

          [data-status-text-animation] {
            display: inline-flex;
            align-items: center;
            position: relative;
            overflow: hidden;
            height: 100%;

            > * {
              white-space: nowrap;
              line-height: 1;
            }

            [data-status-text-enter] {
              animation: slotMachineEnter 150ms cubic-bezier(0, 0, 0.2, 1)
                forwards;
            }
          }

          [data-status-ellipsis] {
            display: inline-flex;
            margin-left: 2px;
          }

          [data-status-ellipsis] span {
            animation: ellipsisFade 1.2s infinite;
            margin: 0 1px;
          }

          [data-status-ellipsis] span:nth-child(2) {
            animation-delay: 0.2s;
          }

          [data-status-ellipsis] span:nth-child(3) {
            animation-delay: 0.4s;
          }

          @keyframes ellipsisFade {
            0%,
            60%,
            100% {
              opacity: 0.2;
            }
            30% {
              opacity: 1;
            }
          }

          @keyframes slotMachineEnter {
            0% {
              transform: translateY(0.8em);
              opacity: 0;
            }
            50% {
              opacity: 0.8;
            }
            100% {
              transform: translateY(0);
              opacity: 1;
            }
          }
        `}),l[2]=n):n=l[2],l[3]!==s?(o=d[s]&&(0,j.jsx)("div",{"data-status-dot":!0,style:{backgroundColor:d[s]}}),l[3]=s,l[4]=o):o=l[4];let f="cache-bypassing"!==s,p=u[s];return l[5]!==s||l[6]!==f||l[7]!==p?(a=(0,j.jsx)(n_,{statusKey:s,showEllipsis:f,children:p},s),l[5]=s,l[6]=f,l[7]=p,l[8]=a):a=l[8],l[9]!==c||l[10]!==o||l[11]!==a?(i=(0,j.jsxs)(j.Fragment,{children:[n,(0,j.jsxs)("button",{"data-indicator-status":!0,"data-nextjs-dev-tools-button":!0,onClick:c,"aria-label":"Open Next.js Dev Tools",children:[o,a]})]}),l[9]=c,l[10]=o,l[11]=a,l[12]=i):i=l[12],i}function n_(e){let t,r,n=(0,S.c)(5),{children:o,showEllipsis:a}=e,i=void 0===a||a;return n[0]!==i?(t=i&&(0,j.jsxs)("span",{"data-status-ellipsis":!0,children:[(0,j.jsx)("span",{children:"."}),(0,j.jsx)("span",{children:"."}),(0,j.jsx)("span",{children:"."})]}),n[0]=i,n[1]=t):t=n[1],n[2]!==t||n[3]!==o?(r=(0,j.jsx)("div",{"data-status-text-animation":!0,children:(0,j.jsxs)("div",{"data-status-text-enter":!0,children:[o,t]})}),n[2]=t,n[3]=o,n[4]=r):r=n[4],r}function nw(e){let t,r,n,o,a,i,l,s,c,u,d,f,p,h=(0,S.c)(54);h[0]!==e?({onTriggerClick:r,...t}=e,h[0]=e,h[1]=t,h[2]=r):(t=h[1],r=h[2]);let{state:m,dispatch:g}=us(),{totalErrorCount:v}=c9(),y=36/m.scale,{panel:b,triggerRef:x,setPanel:_}=nv(),w="panel-selector"===b,k=v>0,[E,T]=(0,C.useState)(k),[N,L]=(0,C.useState)(k);N!==k&&(L(k),T(k));let[I,P]=(0,C.useState)(!1),z=function(e,t){let r,n,o=(0,S.c)(4),a=150,i=(0,C.useRef)(null),[l,s]=(0,C.useState)(!1);return o[0]!==a||o[1]!==e?(r=()=>{if(e>0){let e=i.current?Date.now()-i.current:-1;if(i.current=Date.now(),e<=a)return;s(!0);let t=window.setTimeout(()=>{s(!1)},a);return()=>{clearTimeout(t)}}},n=[e,a],o[0]=a,o[1]=e,o[2]=r,o[3]=n):(r=o[2],n=o[3]),(0,C.useEffect)(r,n),l}(v,0),R="filling"===m.cacheIndicator,O="bypass"===m.cacheIndicator,M=m.buildingIndicator||m.renderingIndicator||R;h[3]===Symbol.for("react.memo_cache_sentinel")?(n={enterDelay:400,exitDelay:500},h[3]=n):n=h[3];let{rendered:A}=ni(M,n),D=(0,C.useRef)(null),Z=function(e){let t,r,n=(0,S.c)(3),[o,a]=(0,C.useState)(0);return n[0]!==e?(t=()=>{let t=e.current;if(!t)return;let r=new ResizeObserver(e=>{let[t]=e,{contentRect:r}=t;a(r.width)});return r.observe(t),()=>r.disconnect()},r=[e],n[0]=e,n[1]=t,n[2]=r):(t=n[1],r=n[2]),(0,C.useEffect)(t,r),o}(D);if(h[4]!==m.buildingIndicator||h[5]!==m.cacheIndicator||h[6]!==m.renderingIndicator){var F,U,$;F=m.buildingIndicator,U=m.renderingIndicator,$=m.cacheIndicator,o=F?"compiling":"filling"===$?"prerendering":U?"rendering":"none",h[4]=m.buildingIndicator,h[5]=m.cacheIndicator,h[6]=m.renderingIndicator,h[7]=o}else o=h[7];let H=o,V=A?H:nb.None,B=E||O||A||m.disableDevIndicator,q=0===Z?"auto":Z,W=`${y}px`,K=m.disableDevIndicator&&(!k||I)?"none":"block";h[8]!==W||h[9]!==K?(a={"--size":W,"--duration-short":"150ms",display:K},h[8]=W,h[9]=K,h[10]=a):a=h[10];let Y=a;h[11]===Symbol.for("react.memo_cache_sentinel")?(i=(0,j.jsx)("style",{children:e_`
          [data-next-badge-root] {
            --timing: cubic-bezier(0.23, 0.88, 0.26, 0.92);
            --duration-long: 250ms;
            --color-outer-border: #171717;
            --color-inner-border: hsla(0, 0%, 100%, 0.14);
            --color-hover-alpha-subtle: hsla(0, 0%, 100%, 0.13);
            --color-hover-alpha-error: hsla(0, 0%, 100%, 0.2);
            --color-hover-alpha-error-2: hsla(0, 0%, 100%, 0.25);
            --mark-size: calc(var(--size) - var(--size-2) * 2);

            --focus-color: var(--color-blue-800);
            --focus-ring: 2px solid var(--focus-color);

            &:has([data-next-badge][data-error='true']) {
              --focus-color: #fff;
            }
          }

          [data-disabled-icon] {
            display: flex;
            align-items: center;
            justify-content: center;
            padding-right: 4px;
          }

          [data-next-badge] {
            width: var(--size);
            height: var(--size);
            display: flex;
            align-items: center;
            position: relative;
            background: rgba(0, 0, 0, 0.8);
            box-shadow:
              0 0 0 1px var(--color-outer-border),
              inset 0 0 0 1px var(--color-inner-border),
              0px 16px 32px -8px rgba(0, 0, 0, 0.24);
            backdrop-filter: blur(48px);
            border-radius: var(--rounded-full);
            user-select: none;
            cursor: pointer;
            scale: 1;
            overflow: hidden;
            will-change: scale, box-shadow, width, background;
            transition:
              scale var(--duration-short) var(--timing),
              width var(--duration-long) var(--timing),
              box-shadow var(--duration-long) var(--timing),
              background var(--duration-short) ease;

            &:active[data-error='false'] {
              scale: 0.95;
            }

            &[data-animate='true']:not(:hover) {
              scale: 1.02;
            }

            &[data-error='false']:has([data-next-mark]:focus-visible) {
              outline: var(--focus-ring);
              outline-offset: 3px;
            }

            &[data-error='true'] {
              background: #ca2a30;
              --color-inner-border: #e5484d;

              [data-next-mark] {
                background: var(--color-hover-alpha-error);
                outline-offset: 0px;

                &:focus-visible {
                  outline: var(--focus-ring);
                  outline-offset: -1px;
                }

                &:hover {
                  background: var(--color-hover-alpha-error-2);
                }
              }
            }

            &[data-cache-bypassing='true']:not([data-error='true']) {
              background: rgba(217, 119, 6, 0.95);
              --color-inner-border: rgba(245, 158, 11, 0.9);

              [data-issues-open] {
                color: white;
              }
            }

            &[data-error-expanded='false'][data-error='true'] ~ [data-dot] {
              scale: 1;
            }

            > div {
              display: flex;
            }
          }

          [data-issues-collapse]:focus-visible {
            outline: var(--focus-ring);
          }

          [data-issues]:has([data-issues-open]:focus-visible) {
            outline: var(--focus-ring);
            outline-offset: -1px;
          }

          [data-dot] {
            content: '';
            width: var(--size-8);
            height: var(--size-8);
            background: #fff;
            box-shadow: 0 0 0 1px var(--color-outer-border);
            border-radius: 50%;
            position: absolute;
            top: 2px;
            right: 0px;
            scale: 0;
            pointer-events: none;
            transition: scale 200ms var(--timing);
            transition-delay: var(--duration-short);
          }

          [data-issues] {
            --padding-left: 8px;
            display: flex;
            gap: 2px;
            align-items: center;
            padding-left: 8px;
            padding-right: 8px;
            height: var(--size-32);
            margin-right: 2px;
            border-radius: var(--rounded-full);
            transition: background var(--duration-short) ease;

            &:has([data-issues-open]:hover) {
              background: var(--color-hover-alpha-error);
            }

            &:has([data-issues-collapse]) {
              padding-right: calc(var(--padding-left) / 2);
            }
          }

          [data-issues-open] {
            font-size: var(--size-13);
            color: white;
            width: fit-content;
            height: 100%;
            display: flex;
            gap: 2px;
            align-items: center;
            margin: 0;
            line-height: var(--size-36);
            font-weight: 500;
            z-index: 2;
            white-space: nowrap;

            &:focus-visible {
              outline: 0;
            }
          }

          [data-issues-collapse] {
            width: var(--size-24);
            height: var(--size-24);
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: var(--rounded-full);
            transition: background var(--duration-short) ease;

            &:hover {
              background: var(--color-hover-alpha-error);
            }
          }

          [data-cross] {
            color: #fff;
            width: var(--size-12);
            height: var(--size-12);
          }

          [data-next-mark] {
            width: var(--mark-size);
            height: var(--mark-size);
            margin: 0 2px;
            display: flex;
            align-items: center;
            border-radius: var(--rounded-full);
            transition: background var(--duration-long) var(--timing);

            &:focus-visible {
              outline: 0;
            }

            &:hover {
              background: var(--color-hover-alpha-subtle);
            }

            svg {
              flex-shrink: 0;
              width: var(--size-40);
              height: var(--size-40);
            }
          }

          [data-issues-count-animation] {
            display: grid;
            place-items: center center;
            font-variant-numeric: tabular-nums;

            &[data-animate='false'] {
              [data-issues-count-exit],
              [data-issues-count-enter] {
                animation-duration: 0ms;
              }
            }

            > * {
              grid-area: 1 / 1;
            }

            [data-issues-count-exit] {
              animation: fadeOut 300ms var(--timing) forwards;
            }

            [data-issues-count-enter] {
              animation: fadeIn 300ms var(--timing) forwards;
            }
          }

          [data-issues-count-plural] {
            display: inline-block;
            &[data-animate='true'] {
              animation: fadeIn 300ms var(--timing) forwards;
            }
          }

          .paused {
            stroke-dashoffset: 0;
          }

          @keyframes fadeIn {
            0% {
              opacity: 0;
              filter: blur(2px);
              transform: translateY(8px);
            }
            100% {
              opacity: 1;
              filter: blur(0px);
              transform: translateY(0);
            }
          }

          @keyframes fadeOut {
            0% {
              opacity: 1;
              filter: blur(0px);
              transform: translateY(0);
            }
            100% {
              opacity: 0;
              transform: translateY(-12px);
              filter: blur(2px);
            }
          }

          @media (prefers-reduced-motion) {
            [data-issues-count-exit],
            [data-issues-count-enter],
            [data-issues-count-plural] {
              animation-duration: 0ms !important;
            }
          }
        `}),h[11]=i):i=h[11];let Q=k||O?nb.None:H;return h[12]!==q?(l={width:q},h[12]=q,h[13]=l):l=h[13],h[14]!==t||h[15]!==k||h[16]!==O||h[17]!==w||h[18]!==r||h[19]!==A||h[20]!==m.disableDevIndicator||h[21]!==x?(s=!m.disableDevIndicator&&(0,j.jsx)("button",{id:"next-logo",ref:x,"data-next-mark":!0,onClick:r,disabled:m.disableDevIndicator,"aria-haspopup":"menu","aria-expanded":w,"aria-controls":"nextjs-dev-tools-menu","aria-label":`${w?"Close":"Open"} Next.js Dev Tools`,"data-nextjs-dev-tools-button":!0,style:{display:!A||k||O?"flex":"none"},...t,children:(0,j.jsx)(nS,{})}),h[14]=t,h[15]=k,h[16]=O,h[17]=w,h[18]=r,h[19]=A,h[20]=m.disableDevIndicator,h[21]=x,h[22]=s):s=h[22],h[23]!==g||h[24]!==V||h[25]!==k||h[26]!==O||h[27]!==E||h[28]!==B||h[29]!==z||h[30]!==r||h[31]!==_||h[32]!==A||h[33]!==m.buildError||h[34]!==m.disableDevIndicator||h[35]!==m.isErrorOverlayOpen||h[36]!==v||h[37]!==x?(c=B&&(0,j.jsxs)(j.Fragment,{children:[(E||m.disableDevIndicator)&&(0,j.jsxs)("div",{"data-issues":!0,children:[(0,j.jsxs)("button",{"data-issues-open":!0,"aria-label":"Open issues overlay",onClick:()=>{m.isErrorOverlayOpen?g({type:G}):(g({type:X}),_(null))},children:[m.disableDevIndicator&&(0,j.jsx)("div",{"data-disabled-icon":!0,children:(0,j.jsx)(nm,{})}),(0,j.jsx)(nk,{animate:z,"data-issues-count-animation":!0,children:v},v)," ",(0,j.jsxs)("div",{children:["Issue",v>1&&(0,j.jsx)("span",{"aria-hidden":!0,"data-issues-count-plural":!0,"data-animate":z&&2===v,children:"s"})]})]}),!m.buildError&&(0,j.jsx)("button",{"data-issues-collapse":!0,"aria-label":"Collapse issues badge",onClick:()=>{m.disableDevIndicator?P(!0):T(!1),x.current?.focus()},children:(0,j.jsx)(nh,{"data-cross":!0})})]}),O&&!k&&!m.disableDevIndicator&&(0,j.jsx)(nj,{onTriggerClick:r,triggerRef:x}),A&&!k&&!O&&!m.disableDevIndicator&&(0,j.jsx)(nx,{status:V,onClick:r})]}),h[23]=g,h[24]=V,h[25]=k,h[26]=O,h[27]=E,h[28]=B,h[29]=z,h[30]=r,h[31]=_,h[32]=A,h[33]=m.buildError,h[34]=m.disableDevIndicator,h[35]=m.isErrorOverlayOpen,h[36]=v,h[37]=x,h[38]=c):c=h[38],h[39]!==s||h[40]!==c?(u=(0,j.jsxs)("div",{ref:D,children:[s,c]}),h[39]=s,h[40]=c,h[41]=u):u=h[41],h[42]!==k||h[43]!==O||h[44]!==B||h[45]!==z||h[46]!==u||h[47]!==Q||h[48]!==l?(d=(0,j.jsx)("div",{"data-next-badge":!0,"data-error":k,"data-error-expanded":B,"data-status":Q,"data-cache-bypassing":O,"data-animate":z,style:l,children:u}),h[42]=k,h[43]=O,h[44]=B,h[45]=z,h[46]=u,h[47]=Q,h[48]=l,h[49]=d):d=h[49],h[50]===Symbol.for("react.memo_cache_sentinel")?(f=(0,j.jsx)("div",{"aria-hidden":!0,"data-dot":!0}),h[50]=f):f=h[50],h[51]!==d||h[52]!==Y?(p=(0,j.jsxs)("div",{"data-next-badge-root":!0,style:Y,children:[i,d,f]}),h[51]=d,h[52]=Y,h[53]=p):p=h[53],p}function nk(e){let t,r,n,o,a,i,l=(0,S.c)(13);l[0]!==e?({children:t,animate:n,...r}=e,l[0]=e,l[1]=t,l[2]=r,l[3]=n):(t=l[1],r=l[2],n=l[3]);let s=void 0===n||n,c=t-1;return l[4]!==c?(o=(0,j.jsx)("div",{"aria-hidden":!0,"data-issues-count-exit":!0,children:c}),l[4]=c,l[5]=o):o=l[5],l[6]!==t?(a=(0,j.jsx)("div",{"data-issues-count":!0,"data-issues-count-enter":!0,children:t}),l[6]=t,l[7]=a):a=l[7],l[8]!==s||l[9]!==r||l[10]!==o||l[11]!==a?(i=(0,j.jsxs)("div",{...r,"data-animate":s,children:[o,a]}),l[8]=s,l[9]=r,l[10]=o,l[11]=a,l[12]=i):i=l[12],i}function nj(e){let t,r,n,o,a,i=(0,S.c)(10),{onTriggerClick:l,triggerRef:s}=e,[c,u]=(0,C.useState)(!1);return c?null:(i[0]!==l?(t=(0,j.jsx)("button",{"data-issues-open":!0,"data-nextjs-dev-tools-button":!0,"aria-label":"Open Next.js Dev Tools",onClick:l,children:"Cache disabled"}),i[0]=l,i[1]=t):t=i[1],i[2]!==s?(r=()=>{u(!0),s.current?.focus()},i[2]=s,i[3]=r):r=i[3],i[4]===Symbol.for("react.memo_cache_sentinel")?(n=(0,j.jsx)(nh,{"data-cross":!0}),i[4]=n):n=i[4],i[5]!==r?(o=(0,j.jsx)("button",{"data-issues-collapse":!0,"aria-label":"Collapse cache bypass badge",onClick:r,children:n}),i[5]=r,i[6]=o):o=i[6],i[7]!==t||i[8]!==o?(a=(0,j.jsxs)("div",{"data-issues":!0,"data-cache-bypass-badge":!0,children:[t,o]}),i[7]=t,i[8]=o,i[9]=a):a=i[9],a)}function nS(){let e,t,r,n,o=(0,S.c)(4);return o[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsxs)("g",{transform:"translate(8.5, 13)",children:[(0,j.jsx)("path",{className:"paused",d:"M13.3 15.2 L2.34 1 V12.6",fill:"none",stroke:"url(#next_logo_paint0_linear_1357_10853)",strokeWidth:"1.86",mask:"url(#next_logo_mask0)",strokeDasharray:"29.6",strokeDashoffset:"29.6"}),(0,j.jsx)("path",{className:"paused",d:"M11.825 1.5 V13.1",strokeWidth:"1.86",stroke:"url(#next_logo_paint1_linear_1357_10853)",strokeDasharray:"11.6",strokeDashoffset:"11.6"})]}),o[0]=e):e=o[0],o[1]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsxs)("linearGradient",{id:"next_logo_paint0_linear_1357_10853",x1:"9.95555",y1:"11.1226",x2:"15.4778",y2:"17.9671",gradientUnits:"userSpaceOnUse",children:[(0,j.jsx)("stop",{stopColor:"white"}),(0,j.jsx)("stop",{offset:"0.604072",stopColor:"white",stopOpacity:"0"}),(0,j.jsx)("stop",{offset:"1",stopColor:"white",stopOpacity:"0"})]}),o[1]=t):t=o[1],o[2]===Symbol.for("react.memo_cache_sentinel")?(r=(0,j.jsxs)("linearGradient",{id:"next_logo_paint1_linear_1357_10853",x1:"11.8222",y1:"1.40039",x2:"11.791",y2:"9.62542",gradientUnits:"userSpaceOnUse",children:[(0,j.jsx)("stop",{stopColor:"white"}),(0,j.jsx)("stop",{offset:"1",stopColor:"white",stopOpacity:"0"})]}),o[2]=r):r=o[2],o[3]===Symbol.for("react.memo_cache_sentinel")?(n=(0,j.jsxs)("svg",{width:"40",height:"40",viewBox:"0 0 40 40",fill:"none",children:[e,(0,j.jsxs)("defs",{children:[t,r,(0,j.jsxs)("mask",{id:"next_logo_mask0",children:[(0,j.jsx)("rect",{width:"100%",height:"100%",fill:"white"}),(0,j.jsx)("rect",{width:"5",height:"1.5",fill:"black"})]})]})]}),o[3]=n):n=o[3],n}let nC=C.forwardRef(function(e,t){let r,n,o,a,i,l,s,c=(0,S.c)(15);return c[0]!==e?({onClick:o,children:r,className:n,...a}=e,c[0]=e,c[1]=r,c[2]=n,c[3]=o,c[4]=a):(r=c[1],n=c[2],o=c[3],a=c[4]),c[5]!==o?(i=e=>(e.target.closest("a")||e.preventDefault(),o?.()),c[5]=o,c[6]=i):i=c[6],c[7]!==n?(l=e6("nextjs-toast",n),c[7]=n,c[8]=l):l=c[8],c[9]!==r||c[10]!==a||c[11]!==t||c[12]!==i||c[13]!==l?(s=(0,j.jsx)("div",{...a,ref:t,onClick:i,className:l,children:r}),c[9]=r,c[10]=a,c[11]=t,c[12]=i,c[13]=l,c[14]=s):s=c[14],s}),nE=(0,C.createContext)(null);function nT({children:e,disabled:t=!1}){let r=(0,C.useRef)(new Set),n=(0,C.useCallback)(e=>{r.current.add(e)},[]),o=(0,C.useCallback)(e=>{r.current.delete(e)},[]),a=(0,C.useMemo)(()=>({register:n,unregister:o,handles:r.current,disabled:t}),[n,o,t]);return(0,j.jsx)(nE.Provider,{value:a,children:e})}function nN(){return(0,C.useContext)(nE)}function nL(e){let t,r,n,o,a,i,l,s,c,u=(0,S.c)(19);u[0]!==e?({children:t,ref:n,...r}=e,u[0]=e,u[1]=t,u[2]=r,u[3]=n):(t=u[1],r=u[2],n=u[3]);let d=(0,C.useRef)(null),f=nN();u[4]!==n?(o=e=>{d.current=e??null,"function"==typeof n?n(e):n&&"object"==typeof n&&(n.current=e)},u[4]=n,u[5]=o):o=u[5];let p=o;u[6]!==f?(a=()=>{if(!f||!d.current||f.disabled)return;let e=d.current;return f.register(e),()=>f.unregister(e)},i=[f],u[6]=f,u[7]=a,u[8]=i):(a=u[7],i=u[8]),(0,C.useEffect)(a,i);let h=f?.disabled?"default":"grab";return u[9]!==r.style?(l=r.style||{},u[9]=r.style,u[10]=l):l=u[10],u[11]!==h||u[12]!==l?(s={cursor:h,...l},u[11]=h,u[12]=l,u[13]=s):s=u[13],u[14]!==t||u[15]!==r||u[16]!==p||u[17]!==s?(c=(0,j.jsx)("div",{ref:p,...r,style:s,children:t}),u[14]=t,u[15]=r,u[16]=p,u[17]=s,u[18]=c):c=u[18],c}function nI(e){let t,r,n,o,a,i,l,s,c,u,d=(0,S.c)(15);d[0]!==e?({children:r,padding:i,position:n,setPosition:s,onDragStart:a,dragHandleSelector:o,disableDrag:c,avoidZone:t,...l}=e,d[0]=e,d[1]=t,d[2]=r,d[3]=n,d[4]=o,d[5]=a,d[6]=i,d[7]=l,d[8]=s,d[9]=c):(t=d[1],r=d[2],n=d[3],o=d[4],a=d[5],i=d[6],l=d[7],s=d[8],c=d[9]);let{ref:f,animate:p,...h}=function(e){let t=(0,C.useRef)(null),r=(0,C.useRef)({state:"idle"}),n=(0,C.useRef)(null),o=(0,C.useRef)({x:0,y:0}),a=(0,C.useRef)({x:0,y:0}),i=(0,C.useRef)(0),l=(0,C.useRef)([]),s=(0,C.useCallback)(()=>{"drag"===r.current.state&&t.current?.releasePointerCapture(r.current.pointerId),r.current="drag"===r.current.state?{state:"drag-end"}:{state:"idle"},null!==n.current&&(n.current(),n.current=null),l.current=[],t.current?.classList.remove("dev-tools-grabbing"),t.current?.style.removeProperty("-webkit-user-select"),document.body.style.removeProperty("user-select"),document.body.style.removeProperty("-webkit-user-select")},[]);function c(e){t.current&&(a.current=e,t.current.style.translate=`${e.x}px ${e.y}px`)}function u(r){let n=t.current;null!==n&&(n.style.transition="translate 491.22ms var(--timing-bounce)",n.addEventListener("transitionend",function t(o){"translate"===o.propertyName&&(e.onAnimationEnd?.(r),a.current={x:0,y:0},n.style.transition="",n.removeEventListener("transitionend",t))}),c(r.translation))}function d(e){"drag-end"===r.current.state&&(e.preventDefault(),e.stopPropagation(),r.current={state:"idle"},t.current?.removeEventListener("click",d))}function f(n){if("press"===r.current.state){let a=n.clientX-o.current.x,i=n.clientY-o.current.y;Math.sqrt(a*a+i*i)>=e.threshold&&(r.current={state:"drag",pointerId:n.pointerId},t.current?.setPointerCapture(n.pointerId),t.current?.classList.add("dev-tools-grabbing"),t.current?.style.setProperty("-webkit-user-select","none"),document.body.style.userSelect="none",document.body.style.webkitUserSelect="none",e.onDragStart?.())}if("drag"!==r.current.state)return;let s={x:n.clientX,y:n.clientY},u=s.x-o.current.x,d=s.y-o.current.y;o.current=s,c({x:a.current.x+u,y:a.current.y+d});let f=Date.now();f-i.current>=10&&(l.current=[...l.current.slice(-5),{position:s,timestamp:f}]),i.current=f,e.onDrag?.(a.current)}function p(){let t=function(e){if(e.length<2)return{x:0,y:0};let t=e[0],r=e[e.length-1],n=r.timestamp-t.timestamp;if(0===n)return{x:0,y:0};let o=(r.position.x-t.position.x)/n;return{x:1e3*o,y:1e3*((r.position.y-t.position.y)/n)}}(l.current);s(),e.onDragEnd?.(a.current,t)}return(0,C.useLayoutEffect)(()=>{e.disabled&&s()},[s,e.disabled]),e.disabled?{ref:t,animate:u}:{ref:t,onPointerDown:function(a){0!==a.button||function(r){if(!r||!t.current)return!0;if(e.handles&&e.handles.size>0){let n=r;for(;n&&n!==t.current;){if(e.handles.has(n))return!0;n=n.parentElement}return!1}return!e.dragHandleSelector||null!==r.closest(e.dragHandleSelector)}(a.target)&&(o.current={x:a.clientX,y:a.clientY},r.current={state:"press"},window.addEventListener("pointermove",f),window.addEventListener("pointerup",p),null!==n.current&&(n.current(),n.current=null),n.current=()=>{window.removeEventListener("pointermove",f),window.removeEventListener("pointerup",p)},t.current?.addEventListener("click",d))},animate:u}}({disabled:void 0!==c&&c,handles:nN()?.handles,threshold:5,onDragStart:a,onDragEnd:function(e,r){0===Math.sqrt(e.x*e.x+e.y*e.y)?f.current?.style.removeProperty("translate"):p(function(e){let r,o,a,l,s,c,u,{x:d,y:p}=e,h=(r=2*i,o=f.current?.offsetWidth||0,a=f.current?.offsetHeight||0,l=window.innerWidth-document.documentElement.clientWidth,c=(s=function(e){let n=e.includes("right"),i=e.includes("bottom"),s=n?window.innerWidth-l-r-o:0,c=i?window.innerHeight-r-a:0;if(t&&t.corner===e){let e=t.square+t.padding;i?c-=e:c+=e}return{x:s,y:c}})(n),{"top-left":(u=function(e){return{x:e.x-c.x,y:e.y-c.y}})(s("top-left")),"top-right":u(s("top-right")),"bottom-left":u(s("bottom-left")),"bottom-right":u(s("bottom-right"))}),m=Object.entries(h).map(e=>{let[t,r]=e;return{key:t,distance:Math.sqrt((d-r.x)**2+(p-r.y)**2)}}),g=Math.min(...m.map(nP)),v=m.find(e=>e.distance===g);return v?{translation:h[v.key],corner:v.key}:{corner:n,translation:h[n]}}({x:e.x+nz(r.x),y:e.y+nz(r.y)}))},onAnimationEnd:function(e){let{corner:t}=e;setTimeout(()=>{f.current?.style.removeProperty("translate"),s(t)})},dragHandleSelector:o});return d[10]!==r||d[11]!==h||d[12]!==l||d[13]!==f?(u=(0,j.jsx)("div",{...l,...h,ref:f,children:r}),d[10]=r,d[11]=h,d[12]=l,d[13]=f,d[14]=u):u=d[14],u}function nP(e){return e.distance}function nz(e,t=.999){return e/1e3*t/(1-t)}let nR=20;function nO(){let e,t,r,n,o,a,i=(0,S.c)(20),{state:l,dispatch:s}=us(),{panel:c,setPanel:u,setSelectedIndex:d}=nv(),f=nM();i[0]!==l.devToolsPosition?(e=l.devToolsPosition.split("-",2),i[0]=l.devToolsPosition,i[1]=e):e=i[1];let[p,h]=e;i[2]!==h||i[3]!==p?(t={"--animate-out-duration-ms":"200ms","--animate-out-timing-function":t6,boxShadow:"none",[p]:`${nR}px`,[h]:`${nR}px`},i[2]=h,i[3]=p,i[4]=t):t=i[4];let m=t,g=null!==c;return i[5]!==s||i[6]!==f?(r=e=>{s({type:en,devToolsPosition:e}),r8({devToolsPosition:e}),f(e)},i[5]=s,i[6]=f,i[7]=r):r=i[7],i[8]!==c||i[9]!==u||i[10]!==d?(n=(0,j.jsx)(nw,{onTriggerClick:()=>{let e="panel-selector"===c?null:"panel-selector";if(u(e),!e)return void d(-1)}}),i[8]=c,i[9]=u,i[10]=d,i[11]=n):n=i[11],i[12]!==l.devToolsPosition||i[13]!==g||i[14]!==r||i[15]!==n?(o=(0,j.jsx)(nI,{disableDrag:g,padding:nR,position:l.devToolsPosition,setPosition:r,children:n}),i[12]=l.devToolsPosition,i[13]=g,i[14]=r,i[15]=n,i[16]=o):o=i[16],i[17]!==m||i[18]!==o?(a=(0,j.jsx)(nC,{id:"devtools-indicator","data-nextjs-toast":!0,style:m,children:o}),i[17]=m,i[18]=o,i[19]=a):a=i[19],a}let nM=()=>{let e,t=(0,S.c)(3),{state:r,dispatch:n}=us();return t[0]!==n||t[1]!==r.devToolsPanelPosition?(e=e=>{n({type:eo,devToolsPanelPosition:e,key:ef});let t=Object.keys(r.devToolsPanelPosition).filter(nA),o={[ef]:e};t.forEach(t=>{n({type:eo,devToolsPanelPosition:e,key:t}),o[t]=e}),r8({devToolsPanelPosition:o})},t[0]=n,t[1]=r.devToolsPanelPosition,t[2]=e):e=t[2],e};function nA(e){return e.startsWith(ec)}let nD=(0,C.createContext)({});function nZ(e){let t,r,n,o,a,i,l,s,c,u,d,f,p,h=(0,S.c)(37);h[0]!==e?({index:r,label:n,value:i,onClick:o,href:t,...a}=e,h[0]=e,h[1]=t,h[2]=r,h[3]=n,h[4]=o,h[5]=a,h[6]=i):(t=h[1],r=h[2],n=h[3],o=h[4],a=h[5],i=h[6]);let m="function"==typeof o||"string"==typeof t,{closeMenu:g,selectedIndex:v,setSelectedIndex:y}=(0,C.useContext)(nD),b=v===r;h[7]!==g||h[8]!==t||h[9]!==m||h[10]!==o?(l=function(){m&&(o?.(),g?.(),t&&window.open(t,"_blank","noopener, noreferrer"))},h[7]=g,h[8]=t,h[9]=m,h[10]=o,h[11]=l):l=h[11];let x=l;h[12]!==r||h[13]!==m||h[14]!==v||h[15]!==y?(s=()=>{m&&void 0!==r&&v!==r&&y(r)},h[12]=r,h[13]=m,h[14]=v,h[15]=y,h[16]=s):s=h[16],h[17]!==y?(c=()=>y(-1),h[17]=y,h[18]=c):c=h[18],h[19]!==x?(u=e=>{("Enter"===e.key||" "===e.key)&&x()},h[19]=x,h[20]=u):u=h[20];let _=m?"menuitem":void 0,w=b?0:-1;return h[21]!==n?(d=(0,j.jsx)("span",{className:"dev-tools-indicator-label",children:n}),h[21]=n,h[22]=d):d=h[22],h[23]!==i?(f=(0,j.jsx)("span",{className:"dev-tools-indicator-value",children:i}),h[23]=i,h[24]=f):f=h[24],h[25]!==x||h[26]!==r||h[27]!==a||h[28]!==b||h[29]!==s||h[30]!==c||h[31]!==u||h[32]!==_||h[33]!==w||h[34]!==d||h[35]!==f?(p=(0,j.jsxs)("div",{className:"dev-tools-indicator-item","data-index":r,"data-selected":b,onClick:x,onMouseMove:s,onMouseLeave:c,onKeyDown:u,role:_,tabIndex:w,...a,children:[d,f]}),h[25]=x,h[26]=r,h[27]=a,h[28]=b,h[29]=s,h[30]=c,h[31]=u,h[32]=_,h[33]=w,h[34]=d,h[35]=f,h[36]=p):p=h[36],p}let nF=e=>{let t,r,n,o,a,i,l,s,c,u,d,f,p,h,m,g,v,y,b,x,_,w,k,E,T=(0,S.c)(63),{closeOnClickOutside:N,items:L}=e,I=void 0===N||N,{state:P}=us(),{setPanel:z,triggerRef:R,setSelectedIndex:O,selectedIndex:M}=nv(),{mounted:A}=c2();T[0]!==P.devToolsPosition?(t=P.devToolsPosition.split("-",2),T[0]=P.devToolsPosition,T[1]=t):t=T[1];let[D,Z]=t,F=(0,C.useRef)(null);T[2]!==I||T[3]!==z||T[4]!==O?(r=e=>{switch(e){case"escape":z(null),O(-1);return;case"outside":if(!I)return;z(null),O(-1);return;default:return null}},T[2]=I,T[3]=z,T[4]=O,T[5]=r):r=T[5],t5(F,R,I&&A,r),T[6]!==M||T[7]!==O?(n=()=>{nV({index:-1===M?"first":M,menuRef:F,setSelectedIndex:O})},T[6]=M,T[7]=O,T[8]=n):n=T[8];let U=(0,C.useEffectEvent)(n);T[9]!==U?(o=()=>{F.current?.focus(),U()},T[9]=U,T[10]=o):o=T[10],T[11]===Symbol.for("react.memo_cache_sentinel")?(a=[],T[11]=a):a=T[11],(0,C.useLayoutEffect)(o,a),T[12]!==P?(i=ny(P),T[12]=P,T[13]=i):i=T[13];let $=i,[H,V]=P.devToolsPosition.split("-",2),B=D===H&&Z===V?$:nR,q=`${B}px`,W="top"===D?"bottom":"top",K="left"===Z?"right":"left";T[14]!==Z||T[15]!==K||T[16]!==q||T[17]!==W||T[18]!==D?(l={[D]:q,[Z]:`${nR}px`,[W]:"auto",[K]:"auto"},T[14]=Z,T[15]=K,T[16]=q,T[17]=W,T[18]=D,T[19]=l):l=T[19];let Y=l;if(T[20]!==L||T[21]!==Y||T[22]!==M||T[23]!==O){let e,t=L.filter(nB),r=t.filter(nq),n=t.filter(nW);p=F,h=function(e){e.preventDefault();let r=t.filter(nK).length;switch(e.key){case"ArrowDown":nV({index:M>=r-1?0:M+1,menuRef:F,setSelectedIndex:O});break;case"ArrowUp":nV({index:M<=0?r-1:M-1,menuRef:F,setSelectedIndex:O});break;case"Home":nV({index:"first",menuRef:F,setSelectedIndex:O});break;case"End":nV({index:"last",menuRef:F,setSelectedIndex:O});break;case"n":e.ctrlKey&&nV({index:M>=r-1?0:M+1,menuRef:F,setSelectedIndex:O});break;case"p":e.ctrlKey&&nV({index:M<=0?r-1:M-1,menuRef:F,setSelectedIndex:O})}},m="nextjs-dev-tools-menu",g="menu",v="ltr",y="vertical",b="Next.js Dev Tools Items",x=-1,T[38]!==Y?(_={outline:0,WebkitFontSmoothing:"antialiased",display:"flex",flexDirection:"column",alignItems:"flex-start",background:"var(--color-background-100)",backgroundClip:"padding-box",boxShadow:"var(--shadow-menu)",borderRadius:"var(--rounded-xl)",position:"fixed",fontFamily:"var(--font-stack-sans)",zIndex:"var(--top-z-index)",overflow:"hidden",opacity:1,minWidth:"248px",transition:"opacity var(--animate-out-duration-ms) var(--animate-out-timing-function)",border:"1px solid var(--color-gray-alpha-400)",...Y},T[38]=Y,T[39]=_):_=T[39],s=nD,T[40]!==M||T[41]!==O?(d={selectedIndex:M,setSelectedIndex:O},T[40]=M,T[41]=O,T[42]=d):d=T[42],T[43]===Symbol.for("react.memo_cache_sentinel")?(e={padding:"6px",width:"100%"},T[43]=e):e=T[43],f=(0,j.jsx)("div",{style:e,children:r.map((e,t)=>(0,j.jsx)(nZ,{title:e.title,label:e.label,value:e.value,onClick:e.onClick,index:e.onClick?nU(r,t):void 0,...e.attributes},e.label))}),c="dev-tools-indicator-footer",u=n.map((e,t)=>{var o;return(0,j.jsx)(nZ,{title:e.title,label:e.label,value:e.value,onClick:e.onClick,...e.attributes,index:e.onClick?nU(n,t)+(o=r).filter(e=>e.onClick).length:void 0},e.label)}),T[20]=L,T[21]=Y,T[22]=M,T[23]=O,T[24]=s,T[25]=c,T[26]=u,T[27]=d,T[28]=f,T[29]=p,T[30]=h,T[31]=m,T[32]=g,T[33]=v,T[34]=y,T[35]=b,T[36]=x,T[37]=_}else s=T[24],c=T[25],u=T[26],d=T[27],f=T[28],p=T[29],h=T[30],m=T[31],g=T[32],v=T[33],y=T[34],b=T[35],x=T[36],_=T[37];return T[44]!==c||T[45]!==u?(w=(0,j.jsx)("div",{className:c,children:u}),T[44]=c,T[45]=u,T[46]=w):w=T[46],T[47]!==s||T[48]!==d||T[49]!==f||T[50]!==w?(k=(0,j.jsxs)(s,{value:d,children:[f,w]}),T[47]=s,T[48]=d,T[49]=f,T[50]=w,T[51]=k):k=T[51],T[52]!==p||T[53]!==h||T[54]!==m||T[55]!==g||T[56]!==v||T[57]!==y||T[58]!==b||T[59]!==x||T[60]!==_||T[61]!==k?(E=(0,j.jsx)("div",{ref:p,onKeyDown:h,id:m,role:g,dir:v,"aria-orientation":y,"aria-label":b,tabIndex:x,style:_,children:k}),T[52]=p,T[53]=h,T[54]=m,T[55]=g,T[56]=v,T[57]=y,T[58]=b,T[59]=x,T[60]=_,T[61]=k,T[62]=E):E=T[62],E};function nU(e,t){let r=0;for(let n=0;n<=t&&n<e.length;n++)if(e[n].onClick){if(n===t)return r;r++}return r}function n$(e){let t,r,n=(0,S.c)(4),{children:o}=e,a=o>0;return n[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("span",{className:"dev-tools-indicator-issue-count-indicator"}),n[0]=t):t=n[0],n[1]!==o||n[2]!==a?(r=(0,j.jsxs)("span",{className:"dev-tools-indicator-issue-count","data-has-issues":a,children:[t,o]}),n[1]=o,n[2]=a,n[3]=r):r=n[3],r}function nH(){let e,t=(0,S.c)(1);return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:"16",height:"16",viewBox:"0 0 16 16",fill:"none",children:(0,j.jsx)("path",{fill:"#666",fillRule:"evenodd",clipRule:"evenodd",d:"M5.50011 1.93945L6.03044 2.46978L10.8537 7.293C11.2442 7.68353 11.2442 8.31669 10.8537 8.70722L6.03044 13.5304L5.50011 14.0608L4.43945 13.0001L4.96978 12.4698L9.43945 8.00011L4.96978 3.53044L4.43945 3.00011L5.50011 1.93945Z"})}),t[0]=e):e=t[0],e}function nV({index:e,menuRef:t,setSelectedIndex:r}){if("first"===e)return void setTimeout(()=>{let e=t.current?.querySelectorAll('[role="menuitem"]');e&&nV({index:Number(e[0].getAttribute("data-index")),menuRef:t,setSelectedIndex:r})});if("last"===e)return void setTimeout(()=>{let e=t.current?.querySelectorAll('[role="menuitem"]');e&&nV({index:e.length-1,menuRef:t,setSelectedIndex:r})});let n=t.current?.querySelector(`[data-index="${e}"]`);n&&(r(e),n?.focus())}function nB(e){return!!e}function nq(e){return!e.footer}function nW(e){return e.footer}function nK(e){return e.onClick}let nY=(0,C.createContext)(null),nX=e=>{let t=.95*window.innerWidth,r=.95*window.innerHeight;return{width:Math.min(t,Math.max(e.minWidth,e.width)),height:Math.min(r,Math.max(e.minHeight,e.height))}},nG=e=>{let t,r,n,o,a,i,l,s,c=(0,S.c)(34),{value:u,children:d}=e,f=u.minWidth??100,p=u.minHeight??80,h=u.maxWidth,m=u.maxHeight,[g,v]=(0,C.useState)(null),y=u.storageKey??ed,{resizeRef:b}=u;c[0]!==g||c[1]!==p||c[2]!==f||c[3]!==b||c[4]!==y||c[5]!==u.devToolsPanelSize?(t=()=>{if(!b.current||null!==g)return;let e=u.devToolsPanelSize[y];if(!e)return;let{height:t,width:r}=nX({...e,minWidth:f??100,minHeight:p??80});return b.current.style.width=`${r}px`,b.current.style.height=`${t}px`,!0},c[0]=g,c[1]=p,c[2]=f,c[3]=b,c[4]=y,c[5]=u.devToolsPanelSize,c[6]=t):t=c[6];let x=t;c[7]!==x||c[8]!==p||c[9]!==f||c[10]!==b||c[11]!==u.initialSize?(r=()=>{if(!x()&&b.current&&u.initialSize?.height&&u.initialSize.width){let{height:e,width:t}=nX({height:u.initialSize.height,width:u.initialSize.width,minWidth:f??100,minHeight:p??80});b.current.style.width=`${t}px`,b.current.style.height=`${e}px`}},c[7]=x,c[8]=p,c[9]=f,c[10]=b,c[11]=u.initialSize,c[12]=r):r=c[12];let _=(0,C.useEffectEvent)(r);c[13]!==_?(n=()=>{_()},c[13]=_,c[14]=n):n=c[14],c[15]===Symbol.for("react.memo_cache_sentinel")?(o=[],c[15]=o):o=c[15],(0,C.useLayoutEffect)(n,o),c[16]!==x?(a=()=>(window.addEventListener("resize",x),()=>window.removeEventListener("resize",x)),c[16]=x,c[17]=a):a=c[17];let w=u.initialSize?.height,k=u.initialSize?.width;return c[18]!==x||c[19]!==w||c[20]!==k||c[21]!==u.resizeRef?(i=[x,w,k,u.resizeRef],c[18]=x,c[19]=w,c[20]=k,c[21]=u.resizeRef,c[22]=i):i=c[22],(0,C.useLayoutEffect)(a,i),c[23]!==g||c[24]!==m||c[25]!==h||c[26]!==p||c[27]!==f||c[28]!==y||c[29]!==u.resizeRef?(l={resizeRef:u.resizeRef,minWidth:f,minHeight:p,maxWidth:h,maxHeight:m,draggingDirection:g,setDraggingDirection:v,storageKey:y},c[23]=g,c[24]=m,c[25]=h,c[26]=p,c[27]=f,c[28]=y,c[29]=u.resizeRef,c[30]=l):l=c[30],c[31]!==d||c[32]!==l?(s=(0,j.jsx)(nY.Provider,{value:l,children:d}),c[31]=d,c[32]=l,c[33]=s):s=c[33],s};var nQ=__webpack_require__("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/components/devtools-panel/resize/resize-handle.css"),nJ={};nJ.styleTagTransform=b(),nJ.setAttributes=m(),nJ.insert=p(),nJ.domAPI=d(),nJ.insertStyleElement=v(),c()(nQ.A,nJ),nQ.A&&nQ.A.locals&&nQ.A.locals;let n0=e=>{let t,r,n,o,a,i,l,s,c=(0,S.c)(31),{direction:u,position:d}=e,{resizeRef:f,minWidth:p,minHeight:h,maxWidth:m,maxHeight:g,storageKey:v,draggingDirection:y,setDraggingDirection:b}=(()=>{let e=(0,C.useContext)(nY);if(!e)throw Error("useResize must be used within a Resize provider");return e})();c[0]===Symbol.for("react.memo_cache_sentinel")?(t={top:0,right:0,bottom:0,left:0},c[0]=t):t=c[0];let[x,_]=(0,C.useState)(t);c[1]!==f?(r=()=>{if(!f.current)return;let e=f.current,t=window.getComputedStyle(e),r=parseFloat(t.borderTopWidth)||0,n=parseFloat(t.borderRightWidth)||0,o=parseFloat(t.borderBottomWidth)||0;_({top:r,right:n,bottom:o,left:parseFloat(t.borderLeftWidth)||0})},n=[f],c[1]=f,c[2]=r,c[3]=n):(r=c[2],n=c[3]),(0,C.useLayoutEffect)(r,n),c[4]!==u||c[5]!==g||c[6]!==m||c[7]!==h||c[8]!==p||c[9]!==f||c[10]!==b||c[11]!==v?(o=e=>{if(e.preventDefault(),!f.current)return;b(u);let t=f.current,r=t.getBoundingClientRect(),n=e.clientX,o=e.clientY,a=e=>{let a=e.clientX-n,{newWidth:i,newHeight:l}=n1(u,a,e.clientY-o,r,p,h,m,g);void 0!==i&&(t.style.width=`${i}px`),void 0!==l&&(t.style.height=`${l}px`)},i=()=>{if(b(null),document.removeEventListener("mousemove",a),document.removeEventListener("mouseup",i),!f.current)return;let{width:e,height:t}=f.current.getBoundingClientRect();r8({devToolsPanelSize:{[v]:{width:e,height:t}}})};document.addEventListener("mousemove",a),document.addEventListener("mouseup",i)},c[4]=u,c[5]=g,c[6]=m,c[7]=h,c[8]=p,c[9]=f,c[10]=b,c[11]=v,c[12]=o):o=c[12];let w=o;if(!(!d.split("-").includes(u)&&(!u.includes("-")||u===n2(d))))return null;let k=x.left+x.right,E=x.top+x.bottom;c[13]!==u?(a=u.includes("-"),c[13]=u,c[14]=a):a=c[14];let T=a,N=`resize-container ${u} ${y&&y!==u?"no-hover":""}`;return c[15]!==w||c[16]!==N?(i=(0,j.jsx)("div",{className:N,onMouseDown:w}),c[15]=w,c[16]=N,c[17]=i):i=c[17],c[18]!==x.bottom||c[19]!==x.left||c[20]!==x.right||c[21]!==x.top||c[22]!==u||c[23]!==y||c[24]!==T||c[25]!==k||c[26]!==E?(l=!T&&(0,j.jsx)("div",{className:`resize-line ${u} ${y===u?"dragging":""}`,style:{"--border-horizontal":`${k}px`,"--border-vertical":`${E}px`,"--border-top":`${x.top}px`,"--border-right":`${x.right}px`,"--border-bottom":`${x.bottom}px`,"--border-left":`${x.left}px`}}),c[18]=x.bottom,c[19]=x.left,c[20]=x.right,c[21]=x.top,c[22]=u,c[23]=y,c[24]=T,c[25]=k,c[26]=E,c[27]=l):l=c[27],c[28]!==i||c[29]!==l?(s=(0,j.jsxs)(j.Fragment,{children:[i,l]}),c[28]=i,c[29]=l,c[30]=s):s=c[30],s},n1=(e,t,r,n,o,a,i,l)=>{let s=i??.95*window.innerWidth,c=l??.95*window.innerHeight;switch(e){case"right":return{newWidth:Math.min(s,Math.max(o,n.width+t)),newHeight:n.height};case"left":return{newWidth:Math.min(s,Math.max(o,n.width-t)),newHeight:n.height};case"bottom":return{newWidth:n.width,newHeight:Math.min(c,Math.max(a,n.height+r))};case"top":return{newWidth:n.width,newHeight:Math.min(c,Math.max(a,n.height-r))};case"top-left":return{newWidth:Math.min(s,Math.max(o,n.width-t)),newHeight:Math.min(c,Math.max(a,n.height-r))};case"top-right":return{newWidth:Math.min(s,Math.max(o,n.width+t)),newHeight:Math.min(c,Math.max(a,n.height-r))};case"bottom-left":return{newWidth:Math.min(s,Math.max(o,n.width-t)),newHeight:Math.min(c,Math.max(a,n.height+r))};case"bottom-right":return{newWidth:Math.min(s,Math.max(o,n.width+t)),newHeight:Math.min(c,Math.max(a,n.height+r))};default:return null}};function n2(e){switch(e){case"top-left":return"bottom-right";case"top-right":return"bottom-left";case"bottom-left":return"top-right";case"bottom-right":return"top-left";default:return null}}var n3=__webpack_require__("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/panel/dynamic-panel.css"),n4={};function n5(e,t="width"){if("number"==typeof e)return e;let r=document.createElement("div");r.style.position="absolute",r.style.visibility="hidden","width"===t?r.style.width=e:r.style.height=e,document.body.appendChild(r);let n="width"===t?r.offsetWidth:r.offsetHeight;return document.body.removeChild(r),n}function n6(e){let t,r,n,o,a,i,l,s,c,u,d,f,p,h,m,g,v,y,b,x,_,w=(0,S.c)(81),{header:k,children:E,draggable:T,sizeConfig:N,closeOnClickOutside:L,sharePanelSizeGlobally:I,sharePanelPositionGlobally:P,containerProps:z}=e,R=void 0!==T&&T;w[0]!==N?(t=void 0===N?{kind:"resizable",minWidth:400,minHeight:350,maxWidth:1e3,maxHeight:1e3,initialSize:{height:400,width:500}}:N,w[0]=N,w[1]=t):t=w[1];let O=t,M=void 0!==L&&L,{setPanel:A}=nv(),{name:D,mounted:Z}=c2(),F=void 0===I||I?ed:`${eu}_${D}`,U=void 0===P||P?ef:`${ec}_${D}`,{dispatch:$,state:H}=us(),V=H.devToolsPanelPosition[U]??H.devToolsPosition;w[2]!==V?(r=V.split("-",2),w[2]=V,w[3]=r):r=w[3];let[B,q]=r,W=(0,C.useRef)(null),{triggerRef:K}=nv();w[4]!==M||w[5]!==A?(n=e=>{switch(e){case"escape":return void A("panel-selector");case"outside":M&&A("panel-selector");return;default:return null}},w[4]=M,w[5]=A,w[6]=n):n=w[6],t5(W,K,Z,n),w[7]!==H?(o=ny(H),w[7]=H,w[8]=o):o=w[8];let Y=o,[X,G]=H.devToolsPosition.split("-",2),Q=B===X&&q===G?Y:nR,J=`${Q}px`,ee="top"===B?"bottom":"top",et="left"===q?"right":"left";w[9]!==q||w[10]!==B||w[11]!==J||w[12]!==ee||w[13]!==et?(a={[B]:J,[q]:`${nR}px`,[ee]:"auto",[et]:"auto"},w[9]=q,w[10]=B,w[11]=J,w[12]=ee,w[13]=et,w[14]=a):a=w[14];let er=a,en="resizable"===O.kind,ea=function(e,t,r,n){let o,a,i,l=(0,S.c)(11);l[0]!==n||l[1]!==r||l[2]!==t||l[3]!==e?(o=()=>({minWidth:e?n5(e,"width"):void 0,minHeight:t?n5(t,"height"):void 0,maxWidth:r?n5(r,"width"):void 0,maxHeight:n?n5(n,"height"):void 0}),l[0]=n,l[1]=r,l[2]=t,l[3]=e,l[4]=o):o=l[4];let[s,c]=(0,C.useState)(o);return l[5]!==n||l[6]!==r||l[7]!==t||l[8]!==e?(a=()=>{let o=()=>{c({minWidth:e?n5(e,"width"):void 0,minHeight:t?n5(t,"height"):void 0,maxWidth:r?n5(r,"width"):void 0,maxHeight:n?n5(n,"height"):void 0})};return window.addEventListener("resize",o),()=>window.removeEventListener("resize",o)},i=[e,t,r,n],l[5]=n,l[6]=r,l[7]=t,l[8]=e,l[9]=a,l[10]=i):(a=l[9],i=l[10]),(0,C.useEffect)(a,i),s}(en?O.minWidth:void 0,en?O.minHeight:void 0,en?O.maxWidth:void 0,en?O.maxHeight:void 0),ei=ea.minWidth,el=ea.minHeight,es=ea.maxWidth,ep=ea.maxHeight,eh=D?`${eu}_${D}`:ed,em=H.devToolsPanelSize[eh],eg="resizable"===O.kind?O.initialSize:O;w[15]!==ep||w[16]!==es||w[17]!==el||w[18]!==ei||w[19]!==F||w[20]!==H.devToolsPanelSize||w[21]!==H.devToolsPosition||w[22]!==eg?(i={resizeRef:W,initialSize:eg,minWidth:ei,minHeight:el,maxWidth:es,maxHeight:ep,devToolsPosition:H.devToolsPosition,devToolsPanelSize:H.devToolsPanelSize,storageKey:F},w[15]=ep,w[16]=es,w[17]=el,w[18]=ei,w[19]=F,w[20]=H.devToolsPanelSize,w[21]=H.devToolsPosition,w[22]=eg,w[23]=i):i=w[23],w[24]!==en||w[25]!==ep||w[26]!==es||w[27]!==el||w[28]!==ei||w[29]!==em||w[30]!==O.height||w[31]!==O.width?(l=en?{"--panel-min-width":ei?`${ei}px`:void 0,"--panel-min-height":el?`${el}px`:void 0,"--panel-max-width":es?`${es}px`:void 0,"--panel-max-height":ep?`${ep}px`:void 0}:{"--panel-height":`${em?em.height:O.height}px`,"--panel-width":`${em?em.width:O.width}px`},w[24]=en,w[25]=ep,w[26]=es,w[27]=el,w[28]=ei,w[29]=em,w[30]=O.height,w[31]=O.width,w[32]=l):l=w[32],w[33]!==er.bottom||w[34]!==er.left||w[35]!==er.right||w[36]!==er.top||w[37]!==l?(s={"--panel-top":er.top,"--panel-bottom":er.bottom,"--panel-left":er.left,"--panel-right":er.right,...l},w[33]=er.bottom,w[34]=er.left,w[35]=er.right,w[36]=er.top,w[37]=l,w[38]=s):s=w[38];let ev=s,ey=!R,eb=25/H.scale;w[39]!==H.devToolsPosition||w[40]!==eb?(c={corner:H.devToolsPosition,square:eb,padding:nR},w[39]=H.devToolsPosition,w[40]=eb,w[41]=c):c=w[41],w[42]!==$||w[43]!==U||w[44]!==O.kind?(u=e=>{$({type:eo,devToolsPanelPosition:e,key:U}),"resizable"===O.kind&&r8({devToolsPanelPosition:{[U]:e}})},w[42]=$,w[43]=U,w[44]=O.kind,w[45]=u):u=w[45],w[46]===Symbol.for("react.memo_cache_sentinel")?(d={overflow:"auto",width:"100%",height:"100%"},w[46]=d):d=w[46];let ex=!R,e_=`panel-content-container ${z?.className||""}`,ew=z?.style;return w[47]!==ew?(f={...ew},w[47]=ew,w[48]=f):f=w[48],w[49]!==k?(p=(0,j.jsx)(nL,{children:k}),w[49]=k,w[50]=p):p=w[50],w[51]!==E?(h=(0,j.jsx)("div",{"data-nextjs-scrollable-content":!0,className:"draggable-content",children:E}),w[51]=E,w[52]=h):h=w[52],w[53]!==z||w[54]!==e_||w[55]!==f||w[56]!==p||w[57]!==h?(m=(0,j.jsxs)("div",{...z,className:e_,style:f,children:[p,h]}),w[53]=z,w[54]=e_,w[55]=f,w[56]=p,w[57]=h,w[58]=m):m=w[58],w[59]!==V||w[60]!==en||w[61]!==O.sides?(g=en&&(0,j.jsxs)(j.Fragment,{children:[(!O.sides||O.sides.includes("vertical"))&&(0,j.jsxs)(j.Fragment,{children:[(0,j.jsx)(n0,{position:V,direction:"top"}),(0,j.jsx)(n0,{position:V,direction:"bottom"})]}),(!O.sides||O.sides.includes("horizontal"))&&(0,j.jsxs)(j.Fragment,{children:[(0,j.jsx)(n0,{position:V,direction:"right"}),(0,j.jsx)(n0,{position:V,direction:"left"})]}),(!O.sides||O.sides.includes("diagonal"))&&(0,j.jsxs)(j.Fragment,{children:[(0,j.jsx)(n0,{position:V,direction:"top-left"}),(0,j.jsx)(n0,{position:V,direction:"top-right"}),(0,j.jsx)(n0,{position:V,direction:"bottom-left"}),(0,j.jsx)(n0,{position:V,direction:"bottom-right"})]})]}),w[59]=V,w[60]=en,w[61]=O.sides,w[62]=g):g=w[62],w[63]!==m||w[64]!==g?(v=(0,j.jsxs)(j.Fragment,{children:[m,g]}),w[63]=m,w[64]=g,w[65]=v):v=w[65],w[66]!==V||w[67]!==c||w[68]!==u||w[69]!==ex||w[70]!==v?(y=(0,j.jsx)(nI,{dragHandleSelector:".resize-container",avoidZone:c,padding:nR,position:V,setPosition:u,style:d,disableDrag:ex,children:v}),w[66]=V,w[67]=c,w[68]=u,w[69]=ex,w[70]=v,w[71]=y):y=w[71],w[72]!==ey||w[73]!==y?(b=(0,j.jsx)(nT,{disabled:ey,children:y}),w[72]=ey,w[73]=y,w[74]=b):b=w[74],w[75]!==ev||w[76]!==b?(x=(0,j.jsx)("div",{tabIndex:-1,ref:W,className:"dynamic-panel-container",style:ev,children:b}),w[75]=ev,w[76]=b,w[77]=x):x=w[77],w[78]!==i||w[79]!==x?(_=(0,j.jsx)(nG,{value:i,children:x}),w[78]=i,w[79]=x,w[80]=_):_=w[80],_}function n9(e){let t,r,n,o,a,i,l=(0,S.c)(10);l[0]!==e?({routerType:r,...t}=e,l[0]=e,l[1]=t,l[2]=r):(t=l[1],r=l[2]),l[3]===Symbol.for("react.memo_cache_sentinel")?(n=(0,j.jsxs)("p",{className:"dev-tools-info-paragraph",children:["The path"," ",(0,j.jsx)("code",{className:"dev-tools-info-code",children:window.location.pathname})," ",'is marked as "static" since it will be prerendered during the build time.']}),l[3]=n):n=l[3];let s="pages"===r?"https://nextjs.org/docs/pages/building-your-application/data-fetching/incremental-static-regeneration":"https://nextjs.org/docs/app/building-your-application/data-fetching/incremental-static-regeneration";return l[4]!==s?(o=(0,j.jsxs)("p",{className:"dev-tools-info-paragraph",children:["With Static Rendering, routes are rendered at build time, or in the background after"," ",(0,j.jsx)("a",{className:"dev-tools-info-link",href:s,target:"_blank",rel:"noopener noreferrer",children:"data revalidation"}),"."]}),l[4]=s,l[5]=o):o=l[5],l[6]===Symbol.for("react.memo_cache_sentinel")?(a=(0,j.jsx)("p",{className:"dev-tools-info-paragraph",children:"Static rendering is useful when a route has data that is not personalized to the user and can be known at build time, such as a static blog post or a product page."}),l[6]=a):a=l[6],l[7]!==t||l[8]!==o?(i=(0,j.jsxs)("article",{className:"dev-tools-info-article",...t,children:[n,o,a]}),l[7]=t,l[8]=o,l[9]=i):i=l[9],i}function n8(e){let t,r,n,o,a,i,l,s=(0,S.c)(11);return s[0]!==e?({routerType:r,...t}=e,s[0]=e,s[1]=t,s[2]=r):(t=s[1],r=s[2]),s[3]===Symbol.for("react.memo_cache_sentinel")?(n=(0,j.jsx)("code",{className:"dev-tools-info-code",children:window.location.pathname}),s[3]=n):n=s[3],s[4]===Symbol.for("react.memo_cache_sentinel")?(o=(0,j.jsxs)("p",{className:"dev-tools-info-paragraph",children:["The path"," ",n," ",'is marked as "dynamic" since it will be rendered for each user at'," ",(0,j.jsx)("strong",{children:"request time"}),"."]}),a=(0,j.jsx)("p",{className:"dev-tools-info-paragraph",children:"Dynamic rendering is useful when a route has data that is personalized to the user or has information that can only be known at request time, such as cookies or the URL's search params."}),s[4]=o,s[5]=a):(o=s[4],a=s[5]),s[6]!==r?(i="pages"===r?(0,j.jsxs)("p",{className:"dev-tools-info-pagraph",children:["Exporting the"," ",(0,j.jsx)("a",{className:"dev-tools-info-link",href:"https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props",target:"_blank",rel:"noopener noreferrer",children:"getServerSideProps"})," ","function will opt the route into dynamic rendering. This function will be called by the server on every request."]}):(0,j.jsxs)("p",{className:"dev-tools-info-paragraph",children:["During rendering, if a"," ",(0,j.jsx)("a",{className:"dev-tools-info-link",href:"https://nextjs.org/docs/app/building-your-application/rendering/server-components#dynamic-apis",target:"_blank",rel:"noopener noreferrer",children:"Dynamic API"})," ","or a"," ",(0,j.jsx)("a",{className:"dev-tools-info-link",href:"https://nextjs.org/docs/app/api-reference/functions/fetch",target:"_blank",rel:"noopener noreferrer",children:"fetch"})," ","option of"," ",(0,j.jsx)("code",{className:"dev-tools-info-code",children:"{ cache: 'no-store' }"})," ","is discovered, Next.js will switch to dynamically rendering the whole route."]}),s[6]=r,s[7]=i):i=s[7],s[8]!==t||s[9]!==i?(l=(0,j.jsxs)("article",{className:"dev-tools-info-article",...t,children:[o,a,i]}),s[8]=t,s[9]=i,s[10]=l):l=s[10],l}n4.styleTagTransform=b(),n4.setAttributes=m(),n4.insert=p(),n4.domAPI=d(),n4.insertStyleElement=v(),c()(n3.A,n4),n3.A&&n3.A.locals&&n3.A.locals;let n7={pages:{static:"https://nextjs.org/docs/pages/building-your-application/rendering/static-site-generation",dynamic:"https://nextjs.org/docs/pages/building-your-application/rendering/server-side-rendering"},app:{static:"https://nextjs.org/docs/app/building-your-application/rendering/server-components#static-rendering-default",dynamic:"https://nextjs.org/docs/app/building-your-application/rendering/server-components#dynamic-rendering"}};function oe(e){let t,r,n,o,a=(0,S.c)(8);return a[0]!==e?({routerType:n,isStaticRoute:t,...r}=e,a[0]=e,a[1]=t,a[2]=r,a[3]=n):(t=a[1],r=a[2],n=a[3]),a[4]!==t||a[5]!==r||a[6]!==n?(o=t?(0,j.jsx)(n9,{routerType:n,...r}):(0,j.jsx)(n8,{routerType:n,...r}),a[4]=t,a[5]=r,a[6]=n,a[7]=o):o=a[7],o}var ot=__webpack_require__("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/components/overview/segment-explorer.css"),or={};or.styleTagTransform=b(),or.setAttributes=m(),or.insert=p(),or.domAPI=d(),or.insertStyleElement=v(),c()(ot.A,or),ot.A&&ot.A.locals&&ot.A.locals;let on=new Set,{subscribe:oo,getSnapshot:oa,getServerSnapshot:oi}={subscribe:e=>(on.add(e),()=>on.delete(e)),getSnapshot:()=>ol.getRoot(),getServerSnapshot:()=>ol.getRoot()},ol=function({getCharacters:e=e=>[e],compare:t=(e,t)=>e===t}){let r={value:void 0,children:{}};function n(){for(let e of on)e()}return{insert:function(t){let o=r;for(let r of e(t))o.children[r]||(o.children[r]={value:void 0,children:{}}),o=o.children[r];o.value=t,r={...r},n()},remove:function(o){let a=r,i=e(o),l=[],s=!0;for(let e of i){if(!a.children[e]){s=!1;break}l.push(a),a=a.children[e]}if(s&&t(a.value,o)){a.value=void 0;for(let e=l.length-1;e>=0;e--){let t=l[e],r=i[e];0===Object.keys(t.children[r].children).length&&delete t.children[r]}r={...r},n()}},getRoot:function(){return r}}}({compare:(e,t)=>!!e&&!!t&&e.pagePath===t.pagePath&&e.type===t.type&&e.boundaryType===t.boundaryType,getCharacters:e=>e.pagePath.split("/")}),os=ol.insert,oc=ol.remove,ou=ol.getRoot;var od=__webpack_require__("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/components/overview/segment-boundary-trigger.css"),of={};of.styleTagTransform=b(),of.setAttributes=m(),of.insert=p(),of.domAPI=d(),of.insertStyleElement=v(),c()(od.A,of),od.A&&od.A.locals&&od.A.locals;let op={};function oh(e,t){let r=C.useRef(op);return r.current===op&&(r.current=e(t)),r}let om=[];function og(e){C.useEffect(e,om)}class ov{static create(){return new ov}currentId=0;start(e,t){this.clear(),this.currentId=setTimeout(()=>{this.currentId=0,t()},e)}isStarted(){return 0!==this.currentId}clear=()=>{0!==this.currentId&&(clearTimeout(this.currentId),this.currentId=0)};disposeEffect=()=>this.clear}function oy(){let e=oh(ov.create).current;return og(e.disposeEffect),e}let ob=E[`useInsertionEffect${Math.random().toFixed(1)}`.slice(0,-3)],ox=ob&&ob!==C.useLayoutEffect?ob:e=>e();function o_(e){let t=oh(ow).current;return t.next=e,ox(t.effect),t.trampoline}function ow(){let e={next:void 0,callback:ok,trampoline:(...t)=>e.callback?.(...t),effect:()=>{e.callback=e.next}};return e}function ok(){}function oj({controlled:e,default:t,name:r,state:n="value"}){let{current:o}=C.useRef(void 0!==e),[a,i]=C.useState(t),l=C.useCallback(e=>{o||i(e)},[]);return[o?e:a,l]}let oS={...E},oC=0,oE=oS.useId;function oT(e,t){if(void 0!==oE){let r=oE();return e??(t?`${t}-${r}`:r)}return function(e,t="mui"){let[r,n]=C.useState(e),o=e||r;return C.useEffect(()=>{null==r&&(oC+=1,n(`${t}-${oC}`))},[r,t]),o}(e,t)}function oN(){let e=new Map;return{emit(t,r){e.get(t)?.forEach(e=>e(r))},on(t,r){e.has(t)||e.set(t,new Set),e.get(t).add(r)},off(t,r){e.get(t)?.delete(r)}}}let oL="undefined"!=typeof document?C.useLayoutEffect:()=>{},oI=C.createContext(null),oP=C.createContext(null),oz=()=>E.useContext(oI)?.id||null;function oR(e){let{children:t,id:r}=e,n=oz();return(0,j.jsx)(oI.Provider,{value:C.useMemo(()=>({id:r,parentId:n}),[r,n]),children:t})}function oO(e){let{children:t}=e,r=C.useRef([]),n=C.useCallback(e=>{r.current=[...r.current,e]},[]),o=C.useCallback(e=>{r.current=r.current.filter(t=>t!==e)},[]),[a]=C.useState(()=>oN());return(0,j.jsx)(oP.Provider,{value:C.useMemo(()=>({nodesRef:r,addNode:n,removeNode:o,events:a}),[n,o,a]),children:t})}function oM(e){let{open:t=!1,onOpenChange:r,elements:n}=e,o=oT(),a=C.useRef({}),[i]=C.useState(()=>oN()),l=null!=oz(),[s,c]=C.useState(n.reference),u=o_((e,t,n)=>{a.current.openEvent=e?t:void 0,i.emit("openchange",{open:e,event:t,reason:n,nested:l}),r?.(e,t,n)}),d=C.useMemo(()=>({setPositionReference:c}),[]),f=C.useMemo(()=>({reference:s||n.reference||null,floating:n.floating||null,domReference:n.reference}),[s,n.reference,n.floating]);return C.useMemo(()=>({dataRef:a,open:t,onOpenChange:u,elements:f,events:i,floatingId:o,refs:d}),[t,u,f,i,o,d])}function oA(){return"undefined"!=typeof window}function oD(e){return oU(e)?(e.nodeName||"").toLowerCase():"#document"}function oZ(e){var t;return(null==e||null==(t=e.ownerDocument)?void 0:t.defaultView)||window}function oF(e){var t;return null==(t=(oU(e)?e.ownerDocument:e.document)||window.document)?void 0:t.documentElement}function oU(e){return!!oA()&&(e instanceof Node||e instanceof oZ(e).Node)}function o$(e){return!!oA()&&(e instanceof Element||e instanceof oZ(e).Element)}function oH(e){return!!oA()&&(e instanceof HTMLElement||e instanceof oZ(e).HTMLElement)}function oV(e){return!!oA()&&"undefined"!=typeof ShadowRoot&&(e instanceof ShadowRoot||e instanceof oZ(e).ShadowRoot)}let oB=new Set(["inline","contents"]);function oq(e){let{overflow:t,overflowX:r,overflowY:n,display:o}=o3(e);return/auto|scroll|overlay|hidden|clip/.test(t+n+r)&&!oB.has(o)}let oW=new Set(["table","td","th"]),oK=[":popover-open",":modal"];function oY(e){return oK.some(t=>{try{return e.matches(t)}catch(e){return!1}})}let oX=["transform","translate","scale","rotate","perspective"],oG=["transform","translate","scale","rotate","perspective","filter"],oQ=["paint","layout","strict","content"];function oJ(e){let t=o0(),r=o$(e)?o3(e):e;return oX.some(e=>!!r[e]&&"none"!==r[e])||!!r.containerType&&"normal"!==r.containerType||!t&&!!r.backdropFilter&&"none"!==r.backdropFilter||!t&&!!r.filter&&"none"!==r.filter||oG.some(e=>(r.willChange||"").includes(e))||oQ.some(e=>(r.contain||"").includes(e))}function o0(){return"undefined"!=typeof CSS&&!!CSS.supports&&CSS.supports("-webkit-backdrop-filter","none")}let o1=new Set(["html","body","#document"]);function o2(e){return o1.has(oD(e))}function o3(e){return oZ(e).getComputedStyle(e)}function o4(e){return o$(e)?{scrollLeft:e.scrollLeft,scrollTop:e.scrollTop}:{scrollLeft:e.scrollX,scrollTop:e.scrollY}}function o5(e){if("html"===oD(e))return e;let t=e.assignedSlot||e.parentNode||oV(e)&&e.host||oF(e);return oV(t)?t.host:t}function o6(e,t,r){var n;void 0===t&&(t=[]),void 0===r&&(r=!0);let o=function e(t){let r=o5(t);return o2(r)?t.ownerDocument?t.ownerDocument.body:t.body:oH(r)&&oq(r)?r:e(r)}(e),a=o===(null==(n=e.ownerDocument)?void 0:n.body),i=oZ(o);if(a){let e=o9(i);return t.concat(i,i.visualViewport||[],oq(o)?o:[],e&&r?o6(e):[])}return t.concat(o,o6(o,[],r))}function o9(e){return e.parent&&Object.getPrototypeOf(e.parent)?e.frameElement:null}function o8(e){let t=oh(o7,e).current;return t.next=e,oL(t.effect),t}function o7(e){let t={current:e,next:e,effect:()=>{t.current=t.next}};return t}let ae="undefined"!=typeof navigator,at=function(){if(!ae)return{platform:"",maxTouchPoints:-1};let e=navigator.userAgentData;return e?.platform?{platform:e.platform,maxTouchPoints:navigator.maxTouchPoints}:{platform:navigator.platform??"",maxTouchPoints:navigator.maxTouchPoints??-1}}(),ar=function(){if(!ae)return"";let e=navigator.userAgentData;return e?.platform?e.platform:navigator.platform??""}(),an=function(){if(!ae)return"";let e=navigator.userAgentData;return e&&Array.isArray(e.brands)?e.brands.map(({brand:e,version:t})=>`${e}/${t}`).join(" "):navigator.userAgent}(),ao="undefined"!=typeof CSS&&!!CSS.supports&&CSS.supports("-webkit-backdrop-filter:none"),aa="MacIntel"===at.platform&&at.maxTouchPoints>1||/iP(hone|ad|od)|iOS/.test(at.platform);ae&&/firefox/i.test(an);let ai=ae&&/apple/i.test(navigator.vendor),al=ae&&/android/i.test(ar)||/android/i.test(an),as=ae&&ar.toLowerCase().startsWith("mac")&&!navigator.maxTouchPoints,ac=an.includes("jsdom/");function au(e){e.preventDefault(),e.stopPropagation()}function ad(e){return 0===e.mozInputSource&&!!e.isTrusted||(al&&e.pointerType?"click"===e.type&&1===e.buttons:0===e.detail&&!e.pointerType)}function af(e){return!ac&&(!al&&0===e.width&&0===e.height||al&&1===e.width&&1===e.height&&0===e.pressure&&0===e.detail&&"mouse"===e.pointerType||e.width<1&&e.height<1&&0===e.pressure&&0===e.detail&&"touch"===e.pointerType)}function ap(e,t){let r=["mouse","pen"];return t||r.push("",void 0),r.includes(e)}let ah="data-base-ui-focusable",am="active",ag="selected",av="ArrowLeft",ay="ArrowRight",ab="ArrowUp",ax="ArrowDown";function a_(e){let t=e.activeElement;for(;t?.shadowRoot?.activeElement!=null;)t=t.shadowRoot.activeElement;return t}function aw(e,t){if(!e||!t)return!1;let r=t.getRootNode?.();if(e.contains(t))return!0;if(r&&oV(r)){let r=t;for(;r;){if(e===r)return!0;r=r.parentNode||r.host}}return!1}function ak(e){return"composedPath"in e?e.composedPath()[0]:e.target}function aj(e,t){return null!=t&&("composedPath"in e?e.composedPath().includes(t):null!=e.target&&t.contains(e.target))}function aS(e){return e?.ownerDocument||document}function aC(e){return oH(e)&&e.matches("input:not([type='hidden']):not([disabled]),[contenteditable]:not([contenteditable='false']),textarea:not([disabled])")}function aE(e){return!!e&&"combobox"===e.getAttribute("role")&&aC(e)}function aT(e){return e?e.hasAttribute(ah)?e:e.querySelector(`[${ah}]`)||e:null}function aN(e){return`data-base-ui-${e}`}let aL=aN("safe-polygon");function aI(e,t,r){if(r&&!ap(r))return 0;if("number"==typeof e)return e;if("function"==typeof e){let r=e();return"number"==typeof r?r:r?.[t]}return e?.[t]}function aP(e){return"function"==typeof e?e():e}function az(e,t={}){let{open:r,onOpenChange:n,dataRef:o,events:a,elements:i}=e,{enabled:l=!0,delay:s=0,handleClose:c=null,mouseOnly:u=!1,restMs:d=0,move:f=!0}=t,p=C.useContext(oP),h=oz(),m=o8(c),g=o8(s),v=o8(r),y=o8(d),b=C.useRef(void 0),x=oy(),_=C.useRef(void 0),w=oy(),k=C.useRef(!0),j=C.useRef(!1),S=C.useRef(()=>{}),E=C.useRef(!1),T=o_(()=>{let e=o.current.openEvent?.type;return e?.includes("mouse")&&"mousedown"!==e});C.useEffect(()=>{if(l)return a.on("openchange",e),()=>{a.off("openchange",e)};function e({open:e}){e||(x.clear(),w.clear(),k.current=!0,E.current=!1)}},[l,a,x,w]),C.useEffect(()=>{if(!l||!m.current||!r)return;function e(e){T()&&n(!1,e,"hover")}let t=aS(i.floating).documentElement;return t.addEventListener("mouseleave",e),()=>{t.removeEventListener("mouseleave",e)}},[i.floating,r,n,l,m,T]);let N=C.useCallback((e,t=!0,r="hover")=>{let o=aI(g.current,"close",b.current);o&&!_.current?x.start(o,()=>n(!1,e,r)):t&&(x.clear(),n(!1,e,r))},[g,n,x]),L=o_(()=>{S.current(),_.current=void 0}),I=o_(()=>{if(j.current){let e=aS(i.floating).body;e.style.pointerEvents="",e.removeAttribute(aL),j.current=!1}}),P=o_(()=>!!o.current.openEvent&&["click","mousedown"].includes(o.current.openEvent.type));C.useEffect(()=>{if(l&&o$(i.domReference)){let n=i.domReference,o=i.floating;return r&&n.addEventListener("mouseleave",a),f&&n.addEventListener("mousemove",e,{once:!0}),n.addEventListener("mouseenter",e),n.addEventListener("mouseleave",t),o&&(o.addEventListener("mouseleave",a),o.addEventListener("mouseenter",s),o.addEventListener("mouseleave",c)),()=>{r&&n.removeEventListener("mouseleave",a),f&&n.removeEventListener("mousemove",e),n.removeEventListener("mouseenter",e),n.removeEventListener("mouseleave",t),o&&(o.removeEventListener("mouseleave",a),o.removeEventListener("mouseenter",s),o.removeEventListener("mouseleave",c))}}function e(e){if(x.clear(),k.current=!1,u&&!ap(b.current)||aP(y.current)>0&&!aI(g.current,"open"))return;let t=aI(g.current,"open",b.current);t?x.start(t,()=>{v.current||n(!0,e,"hover")}):r||n(!0,e,"hover")}function t(e){if(P())return void I();S.current();let t=aS(i.floating);if(w.clear(),E.current=!1,m.current&&o.current.floatingContext){r||x.clear(),_.current=m.current({...o.current.floatingContext,tree:p,x:e.clientX,y:e.clientY,onClose(){I(),L(),P()||N(e,!0,"safe-polygon")}});let n=_.current;t.addEventListener("mousemove",n),S.current=()=>{t.removeEventListener("mousemove",n)};return}"touch"===b.current&&aw(i.floating,e.relatedTarget)||N(e)}function a(e){P()||o.current.floatingContext&&m.current?.({...o.current.floatingContext,tree:p,x:e.clientX,y:e.clientY,onClose(){I(),L(),P()||N(e)}})(e)}function s(){x.clear()}function c(e){P()||N(e,!1)}},[i,l,e,u,f,N,L,I,n,r,v,p,g,m,o,P,y,x,w]),oL(()=>{if(l&&r&&m.current?.__options?.blockPointerEvents&&T()){j.current=!0;let e=i.floating;if(o$(i.domReference)&&e){let t=aS(i.floating).body;t.setAttribute(aL,"");let r=i.domReference,n=p?.nodesRef.current.find(e=>e.id===h)?.context?.elements.floating;return n&&(n.style.pointerEvents=""),t.style.pointerEvents="none",r.style.pointerEvents="auto",e.style.pointerEvents="auto",()=>{t.style.pointerEvents="",r.style.pointerEvents="",e.style.pointerEvents=""}}}},[l,r,h,i,p,m,T]),oL(()=>{r||(b.current=void 0,E.current=!1,L(),I())},[r,L,I]),C.useEffect(()=>()=>{L(),x.clear(),w.clear(),I()},[l,i.domReference,L,I,x,w]);let z=C.useMemo(()=>{function e(e){b.current=e.pointerType}return{onPointerDown:e,onPointerEnter:e,onMouseMove(e){let{nativeEvent:t}=e;function o(){k.current||v.current||n(!0,t,"hover")}u&&!ap(b.current)||r||0===aP(y.current)||E.current&&e.movementX**2+e.movementY**2<2||(w.clear(),"touch"===b.current?o():(E.current=!0,w.start(aP(y.current),o)))}}},[u,n,r,v,y,w]);return C.useMemo(()=>l?{reference:z}:{},[l,z])}function aR(e,t,r=!0){return e.filter(e=>e.parentId===t&&(!r||e.context?.open)).flatMap(t=>[t,...aR(e,t.id,r)])}function aO(e,t){let r=[],n=e.find(e=>e.id===t)?.parentId;for(;n;){let t=e.find(e=>e.id===n);n=t?.parentId,t&&(r=r.concat(t))}return r}function aM(e,t){let[r,n]=e,o=!1,a=t.length;for(let e=0,i=a-1;e<a;i=e++){let[a,l]=t[e]||[0,0],[s,c]=t[i]||[0,0];l>=n!=c>=n&&r<=(s-a)*(n-l)/(c-l)+a&&(o=!o)}return o}function aA(e={}){let{buffer:t=.5,blockPointerEvents:r=!1,requireIntent:n=!0}=e,o=new ov,a=!1,i=null,l=null,s="undefined"!=typeof performance?performance.now():0,c=({x:e,y:r,placement:c,elements:u,onClose:d,nodeId:f,tree:p})=>function(h){var m,g;function v(){o.clear(),d()}if(o.clear(),!u.domReference||!u.floating||null==c||null==e||null==r)return;let{clientX:y,clientY:b}=h,x=[y,b],_=ak(h),w="mouseleave"===h.type,k=aw(u.floating,_),j=aw(u.domReference,_),S=u.domReference.getBoundingClientRect(),C=u.floating.getBoundingClientRect(),E=c.split("-")[0],T=e>C.right-C.width/2,N=r>C.bottom-C.height/2,L=(m=x,g=S,m[0]>=g.x&&m[0]<=g.x+g.width&&m[1]>=g.y&&m[1]<=g.y+g.height),I=C.width>S.width,P=C.height>S.height,z=(I?S:C).left,R=(I?S:C).right,O=(P?S:C).top,M=(P?S:C).bottom;if(k&&(a=!0,!w))return;if(j&&(a=!1),j&&!w){a=!0;return}if(w&&o$(h.relatedTarget)&&aw(u.floating,h.relatedTarget)||p&&aR(p.nodesRef.current,f).some(({context:e})=>e?.open))return;if("top"===E&&r>=S.bottom-1||"bottom"===E&&r<=S.top+1||"left"===E&&e>=S.right-1||"right"===E&&e<=S.left+1)return v();let A=[];switch(E){case"top":A=[[z,S.top+1],[z,C.bottom-1],[R,C.bottom-1],[R,S.top+1]];break;case"bottom":A=[[z,C.top+1],[z,S.bottom-1],[R,S.bottom-1],[R,C.top+1]];break;case"left":A=[[C.right-1,M],[C.right-1,O],[S.left+1,O],[S.left+1,M]];break;case"right":A=[[S.right-1,M],[S.right-1,O],[C.left+1,O],[C.left+1,M]]}if(!aM([y,b],A)){if(a&&!L)return v();if(!w&&n){let e=function(e,t){let r=performance.now(),n=r-s;if(null===i||null===l||0===n)return i=e,l=t,s=r,null;let o=e-i,a=t-l,c=Math.sqrt(o*o+a*a);return i=e,l=t,s=r,c/n}(h.clientX,h.clientY);if(null!==e&&e<.1)return v()}aM([y,b],function([e,r]){switch(E){case"top":{let n=[[C.left,T||I?C.bottom-t:C.top],[C.right,T?I?C.bottom-t:C.top:C.bottom-t]];return[[I?e+t/2:T?e+4*t:e-4*t,r+t+1],[I?e-t/2:T?e+4*t:e-4*t,r+t+1],...n]}case"bottom":{let n=[[C.left,T||I?C.top+t:C.bottom],[C.right,T?I?C.top+t:C.bottom:C.top+t]];return[[I?e+t/2:T?e+4*t:e-4*t,r-t],[I?e-t/2:T?e+4*t:e-4*t,r-t],...n]}case"left":return[[N||P?C.right-t:C.left,C.top],[N?P?C.right-t:C.left:C.right-t,C.bottom],[e+t+1,P?r+t/2:N?r+4*t:r-4*t],[e+t+1,P?r-t/2:N?r+4*t:r-4*t]];case"right":{let n=[[N||P?C.left+t:C.right,C.top],[N?P?C.left+t:C.right:C.left+t,C.bottom]];return[[e-t,P?r+t/2:N?r+4*t:r-4*t],[e-t,P?r-t/2:N?r+4*t:r-4*t],...n]}default:return[]}}([e,r]))?!a&&n&&o.start(40,v):v()}};return c.__options={blockPointerEvents:r},c}let aD=as&&ai;function aZ(e,t={}){let{open:r,onOpenChange:n,events:o,dataRef:a,elements:i}=e,{enabled:l=!0,visibleOnly:s=!0}=t,c=C.useRef(!1),u=oy(),d=C.useRef(!0);C.useEffect(()=>{if(!l)return;let e=oZ(i.domReference);function t(){!r&&oH(i.domReference)&&i.domReference===a_(aS(i.domReference))&&(c.current=!0)}function n(){d.current=!0}function o(){d.current=!1}return e.addEventListener("blur",t),aD&&(e.addEventListener("keydown",n,!0),e.addEventListener("pointerdown",o,!0)),()=>{e.removeEventListener("blur",t),aD&&(e.removeEventListener("keydown",n,!0),e.removeEventListener("pointerdown",o,!0))}},[i.domReference,r,l]),C.useEffect(()=>{if(l)return o.on("openchange",e),()=>{o.off("openchange",e)};function e({reason:e}){("reference-press"===e||"escape-key"===e)&&(c.current=!0)}},[o,l]);let f=C.useMemo(()=>({onMouseLeave(){c.current=!1},onFocus(e){if(c.current)return;let t=ak(e.nativeEvent);if(s&&o$(t)){if(aD&&!e.relatedTarget){if(!d.current&&!aC(t))return}else if(!function(e){if(!e||ac)return!0;try{return e.matches(":focus-visible")}catch(e){return!0}}(t))return}n(!0,e.nativeEvent,"focus")},onBlur(e){c.current=!1;let t=e.relatedTarget,r=e.nativeEvent,o=o$(t)&&t.hasAttribute(aN("focus-guard"))&&"outside"===t.getAttribute("data-type");u.start(0,()=>{let e=a_(i.domReference?i.domReference.ownerDocument:document);!t&&e===i.domReference||aw(a.current.floatingContext?.refs.floating.current,e)||aw(i.domReference,e)||o||n(!1,r,"focus")})}}),[a,i.domReference,n,s,u]);return C.useMemo(()=>l?{reference:f}:{},[l,f])}let aF=new class{callbacks=[];callbacksCount=0;nextId=1;startId=1;isScheduled=!1;tick=e=>{this.isScheduled=!1;let t=this.callbacks,r=this.callbacksCount;if(this.callbacks=[],this.callbacksCount=0,this.startId=this.nextId,r>0)for(let r=0;r<t.length;r+=1)t[r]?.(e)};request(e){let t=this.nextId;return this.nextId+=1,this.callbacks.push(e),this.callbacksCount+=1,this.isScheduled||(requestAnimationFrame(this.tick),this.isScheduled=!0),t}cancel(e){let t=e-this.startId;t<0||t>=this.callbacks.length||(this.callbacks[t]=null,this.callbacksCount-=1)}};class aU{static create(){return new aU}static request(e){return aF.request(e)}static cancel(e){return aF.cancel(e)}currentId=null;request(e){this.cancel(),this.currentId=aF.request(()=>{this.currentId=null,e()})}cancel=()=>{null!==this.currentId&&(aF.cancel(this.currentId),this.currentId=null)};disposeEffect=()=>this.cancel}function a$(){let e=oh(aU.create).current;return og(e.disposeEffect),e}let aH={style:{transition:"none"}},aV={},aB=[],aq={fallbackAxisSide:"none"},aW={fallbackAxisSide:"end"},aK={intentional:"onClick",sloppy:"onPointerDown"};function aY(e){return{escapeKey:"boolean"==typeof e?e:e?.escapeKey??!1,outsidePress:"boolean"==typeof e?e:e?.outsidePress??!0}}function aX(e,t={}){let{open:r,onOpenChange:n,elements:o,dataRef:a}=e,{enabled:i=!0,escapeKey:l=!0,outsidePress:s=!0,outsidePressEvent:c="sloppy",referencePress:u=!1,referencePressEvent:d="sloppy",ancestorScroll:f=!1,bubbles:p,capture:h}=t,m=C.useContext(oP),g=o_("function"==typeof s?s:()=>!1),v="function"==typeof s?g:s,y=C.useRef(!1),{escapeKey:b,outsidePress:x}=aY(p),{escapeKey:_,outsidePress:w}=aY(h),k=C.useRef(null),j=oy(),S=oy(),E=C.useRef(!1),T=C.useRef(""),N=o_(e=>{T.current=e.pointerType}),L=o_(()=>{let e=T.current;return"string"==typeof c?c:c["pen"!==e&&e?e:"mouse"]}),I=o_(e=>{if(!r||!i||!l||"Escape"!==e.key||E.current)return;let t=a.current.floatingContext?.nodeId,o=m?aR(m.nodesRef.current,t):[];if(!b&&(e.stopPropagation(),o.length>0)){let e=!0;if(o.forEach(t=>{t.context?.open&&!t.context.dataRef.current.__escapeKeyBubbles&&(e=!1)}),!e)return}n(!1,"nativeEvent"in e?e.nativeEvent:e,"escape-key")}),P=o_(e=>{let t=L();return"intentional"===t&&"click"!==e.type||"sloppy"===t&&"click"===e.type}),z=o_(e=>{let t=()=>{I(e),ak(e)?.removeEventListener("keydown",t)};ak(e)?.addEventListener("keydown",t)}),R=o_(e=>{if(P(e))return;let t=a.current.insideReactTree;a.current.insideReactTree=!1;let r=y.current;if(y.current=!1,"intentional"===L()&&r||t||"function"==typeof v&&!v(e))return;let i=ak(e),l=`[${aN("inert")}]`,s=aS(o.floating).querySelectorAll(l),c=o$(i)?i:null;for(;c&&!o2(c);){let e=o5(c);if(o2(e)||!o$(e))break;c=e}if(s.length&&o$(i)&&!i.matches("html,body")&&!aw(i,o.floating)&&Array.from(s).every(e=>!aw(c,e)))return;if(oH(i)){let t=o2(i),r=o3(i),n=/auto|scroll/,o=t||n.test(r.overflowX),a=t||n.test(r.overflowY),l=o&&i.clientWidth>0&&i.scrollWidth>i.clientWidth,s=a&&i.clientHeight>0&&i.scrollHeight>i.clientHeight,c="rtl"===r.direction,u=s&&(c?e.offsetX<=i.offsetWidth-i.clientWidth:e.offsetX>i.clientWidth),d=l&&e.offsetY>i.clientHeight;if(u||d)return}let u=a.current.floatingContext?.nodeId,d=m&&aR(m.nodesRef.current,u).some(t=>aj(e,t.context?.elements.floating));if(aj(e,o.floating)||aj(e,o.domReference)||d)return;let f=m?aR(m.nodesRef.current,u):[];if(f.length>0){let e=!0;if(f.forEach(t=>{t.context?.open&&!t.context.dataRef.current.__outsidePressBubbles&&(e=!1)}),!e)return}n(!1,e,"outside-press")}),O=o_(e=>{if(!("sloppy"!==L()||!r||!i||aj(e,o.floating)||aj(e,o.domReference))){if("touch"===e.pointerType){k.current={startTime:Date.now(),startX:e.clientX,startY:e.clientY,dismissOnPointerUp:!1,dismissOnMouseDown:!0},j.start(1e3,()=>{k.current&&(k.current.dismissOnPointerUp=!1,k.current.dismissOnMouseDown=!1)});return}R(e)}}),M=o_(e=>{if(P(e)||(j.clear(),"mousedown"===e.type&&k.current&&!k.current.dismissOnMouseDown))return;let t=()=>{"pointerdown"===e.type?O(e):R(e),ak(e)?.removeEventListener(e.type,t)};ak(e)?.addEventListener(e.type,t)}),A=o_(e=>{if("sloppy"!==L()||"touch"!==e.pointerType||!k.current||aj(e,o.floating)||aj(e,o.domReference))return;let t=Math.abs(e.clientX-k.current.startX),r=Math.abs(e.clientY-k.current.startY),n=Math.sqrt(t*t+r*r);n>5&&(k.current.dismissOnPointerUp=!0),n>10&&(R(e),j.clear(),k.current=null)}),D=o_(e=>{"sloppy"!==L()||"touch"!==e.pointerType||!k.current||aj(e,o.floating)||aj(e,o.domReference)||(k.current.dismissOnPointerUp&&R(e),j.clear(),k.current=null)});C.useEffect(()=>{if(!r||!i)return;a.current.__escapeKeyBubbles=b,a.current.__outsidePressBubbles=x;let e=new ov;function t(e){n(!1,e,"ancestor-scroll")}function s(){e.clear(),E.current=!0}function c(){e.start(5*!!o0(),()=>{E.current=!1})}let u=aS(o.floating);u.addEventListener("pointerdown",N,!0),l&&(u.addEventListener("keydown",_?z:I,_),u.addEventListener("compositionstart",s),u.addEventListener("compositionend",c)),v&&(u.addEventListener("click",w?M:R,w),u.addEventListener("pointerdown",w?M:R,w),u.addEventListener("pointermove",A,w),u.addEventListener("pointerup",D,w),u.addEventListener("mousedown",M,w));let d=[];return f&&(o$(o.domReference)&&(d=o6(o.domReference)),o$(o.floating)&&(d=d.concat(o6(o.floating))),!o$(o.reference)&&o.reference&&o.reference.contextElement&&(d=d.concat(o6(o.reference.contextElement)))),(d=d.filter(e=>e!==u.defaultView?.visualViewport)).forEach(e=>{e.addEventListener("scroll",t,{passive:!0})}),()=>{u.removeEventListener("pointerdown",N,!0),l&&(u.removeEventListener("keydown",_?z:I,_),u.removeEventListener("compositionstart",s),u.removeEventListener("compositionend",c)),v&&(u.removeEventListener("click",w?M:R,w),u.removeEventListener("pointerdown",w?M:R,w),u.removeEventListener("pointermove",A,w),u.removeEventListener("pointerup",D,w),u.removeEventListener("mousedown",M,w)),d.forEach(e=>{e.removeEventListener("scroll",t)}),e.clear()}},[a,o,l,v,c,r,n,f,i,b,x,I,_,z,R,w,M,O,A,D,N]),C.useEffect(()=>{a.current.insideReactTree=!1},[a,v]);let Z=C.useMemo(()=>({onKeyDown:I,...u&&{[aK[d]]:e=>{n(!1,e.nativeEvent,"reference-press")},..."intentional"!==d&&{onClick(e){n(!1,e.nativeEvent,"reference-press")}}}}),[I,n,u,d]),F=o_(e=>{let t=ak(e.nativeEvent);aw(o.floating,t)&&(y.current=!0)}),U=o_(()=>{a.current.insideReactTree=!0,S.start(0,()=>{a.current.insideReactTree=!1})}),$=C.useMemo(()=>({onKeyDown:I,onMouseDown:F,onMouseUp:F,onPointerDownCapture:U,onMouseDownCapture:U,onClickCapture:U}),[I,F,U]);return C.useMemo(()=>i?{reference:Z,floating:$}:{},[i,Z,$])}let aG=new Map([["select","listbox"],["combobox","listbox"],["label",!1]]),aQ=["top","right","bottom","left"],aJ=Math.min,a0=Math.max,a1=Math.round,a2=Math.floor,a3=e=>({x:e,y:e}),a4={left:"right",right:"left",bottom:"top",top:"bottom"},a5={start:"end",end:"start"};function a6(e,t){return"function"==typeof e?e(t):e}function a9(e){return e.split("-")[0]}function a8(e){return e.split("-")[1]}function a7(e){return"x"===e?"y":"x"}function ie(e){return"y"===e?"height":"width"}let it=new Set(["top","bottom"]);function ir(e){return it.has(a9(e))?"y":"x"}function io(e){return e.replace(/start|end/g,e=>a5[e])}let ia=["left","right"],ii=["right","left"],il=["top","bottom"],is=["bottom","top"];function ic(e){return e.replace(/left|right|bottom|top/g,e=>a4[e])}function iu(e){return"number"!=typeof e?{top:0,right:0,bottom:0,left:0,...e}:{top:e,right:e,bottom:e,left:e}}function id(e){let{x:t,y:r,width:n,height:o}=e;return{width:n,height:o,top:r,left:t,right:t+n,bottom:r+o,x:t,y:r}}function ip(e,t,r){return Math.floor(e/t)!==r}function ih(e,t){return t<0||t>=e.current.length}function im(e,t){return iv(e,{disabledIndices:t})}function ig(e,t){return iv(e,{decrement:!0,startingIndex:e.current.length,disabledIndices:t})}function iv(e,{startingIndex:t=-1,decrement:r=!1,disabledIndices:n,amount:o=1}={}){let a=t;do a+=r?-o:o;while(a>=0&&a<=e.current.length-1&&iy(e,a,n));return a}function iy(e,t,r){if("function"==typeof r)return r(t);if(r)return r.includes(t);let n=e.current[t];return null==n||n.hasAttribute("disabled")||"true"===n.getAttribute("aria-disabled")}let ib=0;function ix(e,t={}){let{preventScroll:r=!1,cancelPrevious:n=!0,sync:o=!1}=t;n&&cancelAnimationFrame(ib);let a=()=>e?.focus({preventScroll:r});o?a():ib=requestAnimationFrame(a)}function i_(e,t,r){switch(e){case"vertical":return t;case"horizontal":return r;default:return t||r}}function iw(e,t){return i_(t,e===ab||e===ax,e===av||e===ay)}function ik(e,t,r){return i_(t,e===ax,r?e===av:e===ay)||"Enter"===e||" "===e||""===e}function ij(e=[]){let t=e.map(e=>e?.reference),r=e.map(e=>e?.floating),n=e.map(e=>e?.item),o=C.useCallback(t=>iS(t,e,"reference"),t),a=C.useCallback(t=>iS(t,e,"floating"),r),i=C.useCallback(t=>iS(t,e,"item"),n);return C.useMemo(()=>({getReferenceProps:o,getFloatingProps:a,getItemProps:i}),[o,a,i])}function iS(e,t,r){let n=new Map,o="item"===r,a={};for(let t in"floating"===r&&(a.tabIndex=-1,a[ah]=""),e)o&&e&&(t===am||t===ag)||(a[t]=e[t]);for(let i=0;i<t.length;i+=1){let l,s=t[i]?.[r];(l="function"==typeof s?e?s(e):null:s)&&iC(a,l,o,n)}return iC(a,e,o,n),a}function iC(e,t,r,n){for(let o in t){let a=t[o];r&&(o===am||o===ag)||(o.startsWith("on")?(n.has(o)||n.set(o,[]),"function"==typeof a&&(n.get(o)?.push(a),e[o]=(...e)=>n.get(o)?.map(t=>t(...e)).find(e=>void 0!==e))):e[o]=a)}}let iE=C.createContext(void 0);function iT(e){let t=C.useContext(iE);if(void 0===t&&!e)throw Error("Base UI: MenuRootContext is missing. Menu parts must be placed within <Menu.Root>.");return t}let iN=C.createContext(null);function iL(e,t=!1,r=!1){let[n,o]=C.useState(e&&t?"idle":void 0),[a,i]=C.useState(e);return e&&!a&&(i(!0),o("starting")),e||!a||"ending"===n||r||o("ending"),e||a||"ending"!==n||o(void 0),oL(()=>{if(!e&&a&&"ending"!==n&&r){let e=aU.request(()=>{o("ending")});return()=>{aU.cancel(e)}}},[e,a,n,r]),oL(()=>{if(!e||t)return;let r=aU.request(()=>{ej.flushSync(()=>{o(void 0)})});return()=>{aU.cancel(r)}},[t,e]),oL(()=>{if(!e||!t)return;e&&a&&"idle"!==n&&o("starting");let r=aU.request(()=>{o("idle")});return()=>{aU.cancel(r)}},[t,e,a,o,n]),C.useMemo(()=>({mounted:a,setMounted:i,transitionStatus:n}),[a,n])}function iI(e){let{enabled:t=!0,open:r,ref:n,onComplete:o}=e,a=o8(r),i=o_(o),l=function(e,t=!1){let r=a$();return o_((n,o=null)=>{let a;if(r.cancel(),null!=e){if("current"in e){if(null==e.current)return;a=e.current}else a=e;"function"!=typeof a.getAnimations||globalThis.BASE_UI_ANIMATIONS_DISABLED?n():r.request(()=>{function e(){a&&Promise.allSettled(a.getAnimations().map(e=>e.finished)).then(()=>{null!=o&&o.aborted||ej.flushSync(n)})}t?r.request(e):e()})}})}(n,r);C.useEffect(()=>{t&&l(()=>{r===a.current&&i()})},[t,r,i,l,a])}let iP=C.createContext(void 0);function iz(e=!0){let t=C.useContext(iP);if(void 0===t&&!e)throw Error("Base UI: DirectionContext is missing.");return t?.direction??"ltr"}function iR(e){return e?.ownerDocument||document}let iO=()=>{},iM={},iA={},iD="";class iZ{lockCount=0;restore=null;timeoutLock=ov.create();timeoutUnlock=ov.create();acquire(e){return this.lockCount+=1,1===this.lockCount&&null===this.restore&&this.timeoutLock.start(0,()=>this.lock(e)),this.release}release=()=>{this.lockCount-=1,0===this.lockCount&&this.restore&&this.timeoutUnlock.start(0,this.unlock)};unlock=()=>{0===this.lockCount&&this.restore&&(this.restore?.(),this.restore=null)};lock(e){let t,r;if(0===this.lockCount||null!==this.restore)return;let n=iR(e).documentElement,o=oZ(n).getComputedStyle(n).overflowY;if("hidden"===o||"clip"===o){this.restore=iO;return}let a=aa||!function(e){if("undefined"==typeof document)return!1;let t=iR(e);return oZ(t).innerWidth-t.documentElement.clientWidth>0}(e);this.restore=a?(r=(t=iR(e).documentElement).style.overflow,t.style.overflow="hidden",()=>{t.style.overflow=r}):function(e){let t=iR(e),r=t.documentElement,n=t.body,o=oZ(r),a=0,i=0,l=aU.create();if(ao&&(o.visualViewport?.scale??1)!==1)return()=>{};function s(){let e=o.getComputedStyle(r),t=o.getComputedStyle(n);a=r.scrollTop,i=r.scrollLeft,iM={scrollbarGutter:r.style.scrollbarGutter,overflowY:r.style.overflowY,overflowX:r.style.overflowX},iD=r.style.scrollBehavior,iA={position:n.style.position,height:n.style.height,width:n.style.width,boxSizing:n.style.boxSizing,overflowY:n.style.overflowY,overflowX:n.style.overflowX,scrollBehavior:n.style.scrollBehavior};let l="undefined"!=typeof CSS&&CSS.supports?.("scrollbar-gutter","stable"),s=r.scrollHeight>r.clientHeight,c=r.scrollWidth>r.clientWidth,u="scroll"===e.overflowY||"scroll"===t.overflowY,d="scroll"===e.overflowX||"scroll"===t.overflowX,f=Math.max(0,o.innerWidth-r.clientWidth),p=Math.max(0,o.innerHeight-r.clientHeight),h=parseFloat(t.marginTop)+parseFloat(t.marginBottom),m=parseFloat(t.marginLeft)+parseFloat(t.marginRight);Object.assign(r.style,{scrollbarGutter:"stable",overflowY:!l&&(s||u)?"scroll":"hidden",overflowX:!l&&(c||d)?"scroll":"hidden"}),Object.assign(n.style,{position:"relative",height:h||p?`calc(100dvh - ${h+p}px)`:"100dvh",width:m||f?`calc(100vw - ${m+f}px)`:"100vw",boxSizing:"border-box",overflow:"hidden",scrollBehavior:"unset"}),n.scrollTop=a,n.scrollLeft=i,r.setAttribute("data-base-ui-scroll-locked",""),r.style.scrollBehavior="unset"}function c(){Object.assign(r.style,iM),Object.assign(n.style,iA),r.scrollTop=a,r.scrollLeft=i,r.removeAttribute("data-base-ui-scroll-locked"),r.style.scrollBehavior=iD}function u(){c(),l.request(s)}return s(),o.addEventListener("resize",u),()=>{l.cancel(),c(),o.removeEventListener("resize",u)}}(e)}}let iF=new iZ;function iU(e){if(e)return({"focus-out":"focus-out","escape-key":"escape-key","outside-press":"outside-press","list-navigation":"list-navigation",click:"trigger-press",hover:"trigger-hover",focus:"trigger-focus","reference-press":"trigger-press","safe-polygon":"trigger-hover","ancestor-scroll":void 0})[e]}let i$=C.createContext(void 0);function iH(e=!0){let t=C.useContext(i$);if(void 0===t&&!e)throw Error("Base UI: ContextMenuRootContext is missing. ContextMenu parts must be placed within <ContextMenu.Root>.");return t}let iV=C.createContext(!1);function iB(e,t){return e&&!t?e:!e&&t?t:e||t?{...e,...t}:void 0}let iq={};function iW(e,t,r,n,o){let a={...iX(e,iq)};return t&&(a=iK(a,t)),r&&(a=iK(a,r)),n&&(a=iK(a,n)),o&&(a=iK(a,o)),a}function iK(e,t){return iY(t)?t(e):function(e,t){if(!t)return e;for(let r in t){let n=t[r];switch(r){case"style":e[r]=iB(e.style,n);break;case"className":e[r]=iQ(e.className,n);break;default:!function(e,t){let r=e.charCodeAt(0),n=e.charCodeAt(1),o=e.charCodeAt(2);return 111===r&&110===n&&o>=65&&o<=90&&("function"==typeof t||void 0===t)}(r,n)?e[r]=n:e[r]=function(e,t){return t?e?r=>{var n;if(null!=(n=r)&&"object"==typeof n&&"nativeEvent"in n){iG(r);let n=t(r);return r.baseUIHandlerPrevented||e?.(r),n}let o=t(r);return e?.(r),o}:t:e}(e[r],n)}}return e}(e,t)}function iY(e){return"function"==typeof e}function iX(e,t){return iY(e)?e(t):e??iq}function iG(e){return e.preventBaseUIHandler=()=>{e.baseUIHandlerPrevented=!0},e}function iQ(e,t){return t?e?t+" "+e:t:e}let iJ=[],i0={current:!1},i1=function(e){let t,r,{children:n,open:o,onOpenChange:a,onOpenChangeComplete:i,defaultOpen:l=!1,disabled:s=!1,modal:c,loop:u=!0,orientation:d="vertical",actionsRef:f,openOnHover:p,delay:h=100,closeDelay:m=0,closeParentOnEsc:g=!0}=e,[v,y]=C.useState(null),[b,x]=C.useState(null),[_,w]=C.useState(),[k,S]=C.useState(!0),[E,T]=C.useState(null),[N,L]=C.useState(null),[I,P]=C.useState(!0),[z,R]=C.useState(!1),O=C.useRef(null),M=C.useRef(null),A=C.useRef(null),D=C.useRef([]),Z=C.useRef([]),F=oy(),U=iH(!0),$=C.useContext(iV);{let e=iT(!0),r=function(e){let t=C.useContext(iN);if(null===t&&!e)throw Error("Base UI: MenubarContext is missing. Menubar parts must be placed within <Menubar>.");return t}(!0);t=$&&e?{type:"menu",context:e}:r?{type:"menubar",context:r}:U?{type:"context-menu",context:U}:{type:void 0}}let H=oT();void 0!==t.type&&(H=t.context.rootId);let V=(void 0===t.type||"context-menu"===t.type)&&(c??!0),B="menu"===t.type?t.context.allowMouseEnter:z,q="menu"===t.type?t.context.setAllowMouseEnter:R,W=p??("menu"===t.type||"menubar"===t.type&&t.context.hasSubmenuOpen),[K,Y]=oj({controlled:o,default:l,name:"MenuRoot",state:"open"}),X=C.useRef("context-menu"!==t.type),G=oy();C.useEffect(()=>{if(K||(O.current=null),"context-menu"===t.type){if(!K){G.clear(),X.current=!1;return}G.start(500,()=>{X.current=!0})}},[G,K,t.type]);let Q=C.useCallback(e=>{A.current=e,x(e)},[]),{mounted:J,setMounted:ee,transitionStatus:et}=iL(K),{openMethod:er,triggerProps:en,reset:eo}=function(e){var t;let r,n,[o,a]=C.useState(null),i=o_((t,r)=>{e||a(r)}),l=o_(()=>{a(null)}),{onClick:s,onPointerDown:c}=(t=i,r=C.useRef(""),n=C.useCallback(e=>{e.defaultPrevented||(r.current=e.pointerType,t(e,e.pointerType))},[t]),{onClick:C.useCallback(e=>{0===e.detail?t(e,"keyboard"):("pointerType"in e&&t(e,e.pointerType),t(e,r.current),r.current="")},[t]),onPointerDown:n});return C.useMemo(()=>({openMethod:o,reset:l,triggerProps:{onClick:s,onPointerDown:c}}),[o,l,s,c])}(K);!function(e){let{enabled:t=!0,mounted:r,open:n,referenceElement:o=null}=e;oL(()=>{if(t&&ao&&r&&!n){let e=iR(o),t=e.body.style.userSelect,r=e.body.style.webkitUserSelect;return e.body.style.userSelect="none",e.body.style.webkitUserSelect="none",()=>{e.body.style.userSelect=t,e.body.style.webkitUserSelect=r}}},[t,r,n,o]),oL(()=>{if(t)return iF.acquire(o)},[t,o])}({enabled:K&&V&&"trigger-hover"!==N&&"touch"!==er,mounted:J,open:K,referenceElement:b}),K||k||S(!0);let ea=o_(()=>{ee(!1),P(!0),q(!1),i?.(!1),eo()});iI({enabled:!f,open:K,ref:M,onComplete(){K||ea()}});let ei=C.useRef(!0),el=oy(),es=o_((e,r,n)=>{if(K===e||!1===e&&r?.type==="click"&&"touch"===r.pointerType&&!ei.current)return;if(!e&&null!==E){let e=D.current[E];queueMicrotask(()=>{e?.setAttribute("tabindex","-1")})}e&&"trigger-focus"===n?(ei.current=!1,el.start(300,()=>{ei.current=!0})):(ei.current=!0,el.clear());let o=("trigger-press"===n||"item-press"===n)&&0===r.detail&&r?.isTrusted,i=!e&&("escape-key"===n||null==n);function l(){a?.(e,r,n),Y(e),L(n??null),O.current=r??null}"trigger-hover"===n?(P(!0),F.start(500,()=>{P(!1)}),ej.flushSync(l)):l(),"menubar"===t.type&&("trigger-focus"===n||"focus-out"===n||"trigger-hover"===n||"list-navigation"===n||"sibling-open"===n)?w("group"):o||i?w(o?"click":"dismiss"):w(void 0)});C.useImperativeHandle(f,()=>({unmount:ea}),[ea]),"context-menu"===t.type&&(r=t.context),C.useImperativeHandle(r?.positionerRef,()=>b,[b]),C.useImperativeHandle(r?.actionsRef,()=>({setOpen:es}),[es]),C.useEffect(()=>{K||F.clear()},[F,K]);let ec=oM({elements:{reference:v,floating:b},open:K,onOpenChange(e,t,r){es(e,t,iU(r))}}),eu=az(ec,{enabled:k&&W&&!s&&"context-menu"!==t.type&&("menubar"!==t.type||t.context.hasSubmenuOpen&&!K),handleClose:aA({blockPointerEvents:!0}),mouseOnly:!0,move:"menu"===t.type,restMs:void 0===t.type||"menu"===t.type&&B?h:void 0,delay:"menu"===t.type?{open:B?h:1e10,close:m}:{close:m}}),ed=aZ(ec,{enabled:!s&&!K&&"menubar"===t.type&&t.context.hasSubmenuOpen&&!U}),ef=function(e,t={}){let{open:r,onOpenChange:n,dataRef:o}=e,{enabled:a=!0,event:i="click",toggle:l=!0,ignoreMouse:s=!1,stickIfOpen:c=!0}=t,u=C.useRef(void 0),d=a$(),f=C.useMemo(()=>({onPointerDown(e){u.current=e.pointerType},onMouseDown(e){let t=u.current,a=e.nativeEvent;if(0!==e.button||"click"===i||ap(t,!0)&&s)return;let f=o.current.openEvent,p=f?.type,h=!(r&&l&&(!f||!c||"click"===p||"mousedown"===p));d.request(()=>{n(h,a,"click")})},onClick(e){let t=u.current;if("mousedown"===i&&t){u.current=void 0;return}if(ap(t,!0)&&s)return;let a=o.current.openEvent,d=a?.type;n(!(r&&l&&(!a||!c||"click"===d||"mousedown"===d||"keydown"===d||"keyup"===d)),e.nativeEvent,"click")},onKeyDown(){u.current=void 0}}),[o,i,s,n,r,c,l,d]);return C.useMemo(()=>a?{reference:f}:aV,[a,f])}(ec,{enabled:!s&&"context-menu"!==t.type,event:K&&"menubar"===t.type?"click":"mousedown",toggle:!W||"menu"!==t.type,ignoreMouse:W&&"menu"===t.type,stickIfOpen:void 0===t.type&&I}),ep=aX(ec,{enabled:!s,bubbles:g&&"menu"===t.type,outsidePress:()=>"context-menu"!==t.type||O.current?.type==="contextmenu"||X.current}),eh=function(e,t={}){let{open:r,elements:n,floatingId:o}=e,{enabled:a=!0,role:i="dialog"}=t,l=oT(),s=n.domReference?.id||l,c=C.useMemo(()=>aT(n.floating)?.id||o,[n.floating,o]),u=aG.get(i)??i,d=null!=oz(),f=C.useMemo(()=>"tooltip"===u||"label"===i?{[`aria-${"label"===i?"labelledby":"describedby"}`]:r?c:void 0}:{"aria-expanded":r?"true":"false","aria-haspopup":"alertdialog"===u?"dialog":u,"aria-controls":r?c:void 0,..."listbox"===u&&{role:"combobox"},..."menu"===u&&{id:s},..."menu"===u&&d&&{role:"menuitem"},..."select"===i&&{"aria-autocomplete":"none"},..."combobox"===i&&{"aria-autocomplete":"list"}},[u,c,d,r,s,i]),p=C.useMemo(()=>{let e={id:c,...u&&{role:u}};return"tooltip"===u||"label"===i?e:{...e,..."menu"===u&&{"aria-labelledby":s}}},[u,c,s,i]),h=C.useCallback(({active:e,selected:t})=>{let r={role:"option",...e&&{id:`${c}-fui-option`}};switch(i){case"select":case"combobox":return{...r,"aria-selected":t}}return{}},[c,i]);return C.useMemo(()=>a?{reference:f,floating:p,item:h}:{},[a,f,p,h])}(ec,{role:"menu"}),em=iz(),eg=function(e,t){let{open:r,onOpenChange:n,elements:o,floatingId:a}=e,{listRef:i,activeIndex:l,onNavigate:s=()=>{},enabled:c=!0,selectedIndex:u=null,allowEscape:d=!1,loop:f=!1,nested:p=!1,rtl:h=!1,virtual:m=!1,focusItemOnOpen:g="auto",focusItemOnHover:v=!0,openOnArrowKeyDown:y=!0,disabledIndices:b,orientation:x="vertical",parentOrientation:_,cols:w=1,scrollItemIntoView:k=!0,virtualItemRef:j,itemSizes:S,dense:E=!1}=t,T=o8(aT(o.floating)),N=oz(),L=C.useContext(oP);oL(()=>{e.dataRef.current.orientation=x},[e,x]);let I=aE(o.domReference),P=C.useRef(g),z=C.useRef(u??-1),R=C.useRef(null),O=C.useRef(!0),M=o_(()=>{s(-1===z.current?null:z.current)}),A=C.useRef(M),D=C.useRef(!!o.floating),Z=C.useRef(r),F=C.useRef(!1),U=C.useRef(!1),$=o8(b),H=o8(r),V=o8(k),B=o8(u),[q,W]=C.useState(),K=o_(()=>{function e(e){m?(e.id?.endsWith("-fui-option")&&(e.id=`${a}-${Math.random().toString(16).slice(2,10)}`),W(e.id),L?.events.emit("virtualfocus",e),j&&(j.current=e)):ix(e,{sync:F.current,preventScroll:!0})}let t=i.current[z.current],r=U.current;t&&e(t),(F.current?e=>e():requestAnimationFrame)(()=>{let n=i.current[z.current]||t;if(!n)return;t||e(n);let o=V.current;o&&X&&(r||!O.current)&&n.scrollIntoView?.("boolean"==typeof o?{block:"nearest",inline:"nearest"}:o)})});oL(()=>{c&&(r&&o.floating?P.current&&null!=u&&(U.current=!0,z.current=u,M()):D.current&&(z.current=-1,A.current()))},[c,r,o.floating,u,M]),oL(()=>{if(c&&r&&o.floating)if(null==l){if(F.current=!1,null!=B.current)return;if(D.current&&(z.current=-1,K()),(!Z.current||!D.current)&&P.current&&(null!=R.current||!0===P.current&&null==R.current)){let e=0,t=()=>{null==i.current[0]?(e<2&&(e?requestAnimationFrame:queueMicrotask)(t),e+=1):(z.current=null==R.current||ik(R.current,x,h)||p?im(i,$.current):ig(i,$.current),R.current=null,M())};t()}}else ih(i,l)||(z.current=l,K(),U.current=!1)},[c,r,o.floating,l,B,p,i,x,h,M,K,$]),oL(()=>{if(!c||o.floating||!L||m||!D.current)return;let e=L.nodesRef.current,t=e.find(e=>e.id===N)?.context?.elements.floating,r=a_(aS(o.floating)),n=e.some(e=>e.context&&aw(e.context.elements.floating,r));t&&!n&&O.current&&t.focus({preventScroll:!0})},[c,o.floating,L,N,m]),oL(()=>{A.current=M,Z.current=r,D.current=!!o.floating}),oL(()=>{r||(R.current=null,P.current=g)},[r,g]);let Y=null!=l,X=C.useMemo(()=>{function e(e){if(!H.current)return;let t=i.current.indexOf(e);-1!==t&&z.current!==t&&(z.current=t,M())}return{onFocus({currentTarget:t}){F.current=!0,e(t)},onClick:({currentTarget:e})=>e.focus({preventScroll:!0}),onMouseMove({currentTarget:t}){F.current=!0,U.current=!1,v&&e(t)},onPointerLeave({pointerType:e}){!O.current||"touch"===e||(F.current=!0,v&&(z.current=-1,M(),m||T.current?.focus({preventScroll:!0})))}}},[H,T,v,i,M,m]),G=C.useCallback(()=>_??L?.nodesRef.current.find(e=>e.id===N)?.context?.dataRef?.current.orientation,[N,L,_]),Q=o_(e=>{var t,a,l,s,c,u,g,v;if(O.current=!1,F.current=!0,229===e.which||!H.current&&e.currentTarget===T.current)return;if(p&&(t=e.key,a=x,l=h,s=w,"both"===a||"horizontal"===a&&s&&s>1?"Escape"===t:i_(a,l?t===ay:t===av,t===ab))){iw(e.key,G())||au(e),n(!1,e.nativeEvent,"list-navigation"),oH(o.domReference)&&(m?L?.events.emit("virtualfocus",o.domReference):o.domReference.focus());return}let y=z.current,_=im(i,b),k=ig(i,b);if(I||("Home"===e.key&&(au(e),z.current=_,M()),"End"===e.key&&(au(e),z.current=k,M())),w>1){let t,r,n=S||Array.from({length:i.current.length},()=>({width:1,height:1})),o=(c=n,u=w,g=E,t=[],r=0,c.forEach(({width:e,height:n},o)=>{let a=!1;for(g&&(r=0);!a;){let i=[];for(let t=0;t<e;t+=1)for(let e=0;e<n;e+=1)i.push(r+t+e*u);r%u+e<=u&&i.every(e=>null==t[e])?(i.forEach(e=>{t[e]=o}),a=!0):r+=1}}),[...t]),a=o.findIndex(e=>null!=e&&!iy(i,e,b)),l=o.reduce((e,t,r)=>null==t||iy(i,t,b)?e:r,-1),s=o[function(e,{event:t,orientation:r,loop:n,rtl:o,cols:a,disabledIndices:i,minIndex:l,maxIndex:s,prevIndex:c,stopEvent:u=!1}){let d=c;if(t.key===ab){if(u&&au(t),-1===c)d=s;else if(d=iv(e,{startingIndex:d,amount:a,decrement:!0,disabledIndices:i}),n&&(c-a<l||d<0)){let e=c%a,t=s%a,r=s-(t-e);d=t===e?s:t>e?r:r-a}ih(e,d)&&(d=c)}if(t.key===ax&&(u&&au(t),-1===c?d=l:(d=iv(e,{startingIndex:c,amount:a,disabledIndices:i}),n&&c+a>s&&(d=iv(e,{startingIndex:c%a-a,amount:a,disabledIndices:i}))),ih(e,d)&&(d=c)),"both"===r){let r=a2(c/a);t.key===(o?av:ay)&&(u&&au(t),c%a!=a-1?(d=iv(e,{startingIndex:c,disabledIndices:i}),n&&ip(d,a,r)&&(d=iv(e,{startingIndex:c-c%a-1,disabledIndices:i}))):n&&(d=iv(e,{startingIndex:c-c%a-1,disabledIndices:i})),ip(d,a,r)&&(d=c)),t.key===(o?ay:av)&&(u&&au(t),c%a!=0?(d=iv(e,{startingIndex:c,decrement:!0,disabledIndices:i}),n&&ip(d,a,r)&&(d=iv(e,{startingIndex:c+(a-c%a),decrement:!0,disabledIndices:i}))):n&&(d=iv(e,{startingIndex:c+(a-c%a),decrement:!0,disabledIndices:i})),ip(d,a,r)&&(d=c));let l=a2(s/a)===r;ih(e,d)&&(d=n&&l?t.key===(o?ay:av)?s:iv(e,{startingIndex:c-c%a-1,disabledIndices:i}):c)}return d}({current:o.map(e=>null!=e?i.current[e]:null)},{event:e,orientation:x,loop:f,rtl:h,cols:w,disabledIndices:(v=[...("function"!=typeof b?b:null)||i.current.map((e,t)=>iy(i,t,b)?t:void 0),void 0],o.flatMap((e,t)=>v.includes(e)?[t]:[])),minIndex:a,maxIndex:l,prevIndex:function(e,t,r,n,o){if(-1===e)return -1;let a=r.indexOf(e),i=t[e];switch(o){case"tl":return a;case"tr":if(!i)return a;return a+i.width-1;case"bl":if(!i)return a;return a+(i.height-1)*n;case"br":return r.lastIndexOf(e);default:return -1}}(z.current>k?_:z.current,n,o,w,e.key===ax?"bl":e.key===(h?av:ay)?"tr":"tl"),stopEvent:!0})];if(null!=s&&(z.current=s,M()),"both"===x)return}if(iw(e.key,x)){if(au(e),r&&!m&&a_(e.currentTarget.ownerDocument)===e.currentTarget){z.current=ik(e.key,x,h)?_:k,M();return}ik(e.key,x,h)?f?z.current=y>=k?d&&y!==i.current.length?-1:_:iv(i,{startingIndex:y,disabledIndices:b}):z.current=Math.min(k,iv(i,{startingIndex:y,disabledIndices:b})):f?z.current=y<=_?d&&-1!==y?i.current.length:k:iv(i,{startingIndex:y,decrement:!0,disabledIndices:b}):z.current=Math.max(_,iv(i,{startingIndex:y,decrement:!0,disabledIndices:b})),ih(i,z.current)&&(z.current=-1),M()}}),J=C.useMemo(()=>m&&r&&Y&&{"aria-activedescendant":q},[m,r,Y,q]),ee=C.useMemo(()=>({"aria-orientation":"both"===x?void 0:x,...!I?J:{},onKeyDown(e){if("Tab"===e.key&&e.shiftKey&&r&&!m){au(e),n(!1,e.nativeEvent,"list-navigation"),oH(o.domReference)&&o.domReference.focus();return}Q(e)},onPointerMove(){O.current=!0}}),[J,Q,x,I,n,r,m,o.domReference]),et=C.useMemo(()=>{function e(e){"auto"===g&&ad(e.nativeEvent)&&(P.current=!0)}function t(e){P.current=g,"auto"===g&&af(e.nativeEvent)&&(P.current=!0)}return{...J,onKeyDown(e){var t,o;O.current=!1;let a=e.key.startsWith("Arrow"),l=(t=e.key,o=G(),i_(o,h?t===av:t===ay,t===ax)),s=iw(e.key,x),c=(p?l:s)||"Enter"===e.key||""===e.key.trim();if(m&&r)return Q(e);if(r||y||!a){if(c){let t=iw(e.key,G());R.current=p&&t?null:e.key}if(p){l&&(au(e),r?(z.current=im(i,$.current),M()):n(!0,e.nativeEvent,"list-navigation"));return}s&&(null!=u&&(z.current=u),au(e),!r&&y?n(!0,e.nativeEvent,"list-navigation"):Q(e),r&&M())}},onFocus(){r&&!m&&(z.current=-1,M())},onPointerDown:t,onPointerEnter:t,onMouseDown:e,onClick:e}},[J,Q,$,g,i,p,M,n,r,y,x,G,h,u,m]);return C.useMemo(()=>c?{reference:et,floating:ee,item:X}:{},[c,et,ee,X])}(ec,{enabled:!s,listRef:D,activeIndex:E,nested:void 0!==t.type,loop:u,orientation:d,parentOrientation:"menubar"===t.type?t.context.orientation:void 0,rtl:"rtl"===em,disabledIndices:iJ,onNavigate:T,openOnArrowKeyDown:"context-menu"!==t.type}),ev=C.useRef(!1),ey=function(e,t){let{open:r,dataRef:n}=e,{listRef:o,activeIndex:a,onMatch:i,onTypingChange:l,enabled:s=!0,findMatch:c=null,resetMs:u=750,ignoreKeys:d=[],selectedIndex:f=null}=t,p=oy(),h=C.useRef(""),m=C.useRef(f??a??-1),g=C.useRef(null),v=o_(i),y=o_(l),b=o8(c),x=o8(d);oL(()=>{r&&(p.clear(),g.current=null,h.current="")},[r,p]),oL(()=>{r&&""===h.current&&(m.current=f??a??-1)},[r,f,a]);let _=o_(e=>{e?n.current.typing||(n.current.typing=e,y(e)):n.current.typing&&(n.current.typing=e,y(e))}),w=o_(e=>{function t(e,t,r){let n=b.current?b.current(t,r):t.find(e=>e?.toLocaleLowerCase().indexOf(r.toLocaleLowerCase())===0);return n?e.indexOf(n):-1}let n=o.current;if(h.current.length>0&&" "!==h.current[0]&&(-1===t(n,n,h.current)?_(!1):" "===e.key&&au(e)),null==n||x.current.includes(e.key)||1!==e.key.length||e.ctrlKey||e.metaKey||e.altKey)return;r&&" "!==e.key&&(au(e),_(!0)),n.every(e=>!e||e[0]?.toLocaleLowerCase()!==e[1]?.toLocaleLowerCase())&&h.current===e.key&&(h.current="",m.current=g.current),h.current+=e.key,p.start(u,()=>{h.current="",m.current=g.current,_(!1)});let a=m.current,i=t(n,[...n.slice((a||0)+1),...n.slice(0,(a||0)+1)],h.current);-1!==i?(v(i),g.current=i):" "!==e.key&&(h.current="",_(!1))}),k=C.useMemo(()=>({onKeyDown:w}),[w]),j=C.useMemo(()=>({onKeyDown:w,onKeyUp(e){" "===e.key&&_(!1)}}),[w,_]);return C.useMemo(()=>s?{reference:k,floating:j}:{},[s,k,j])}(ec,{listRef:Z,activeIndex:E,resetMs:500,onMatch:e=>{K&&e!==E&&T(e)},onTypingChange:C.useCallback(e=>{ev.current=e},[])}),{getReferenceProps:eb,getFloatingProps:ex,getItemProps:e_}=ij([eu,ef,ep,ed,eh,eg,ey]),ew=function(e){let{enabled:t=!0,mouseDownAction:r,open:n}=e,o=C.useRef(!1);return C.useMemo(()=>t?{onMouseDown:e=>{("open"===r&&!n||"close"===r&&n)&&(o.current=!0,iR(e.currentTarget).addEventListener("click",()=>{o.current=!1},{once:!0}))},onClick:e=>{o.current&&(o.current=!1,e.preventBaseUIHandler())}}:aV,[t,r,n])}({open:K,enabled:"menubar"===t.type,mouseDownAction:"open"}),ek=C.useMemo(()=>{let e=iW(eb(),{onMouseEnter(){S(!0)},onMouseMove(){q(!0)}},en,ew);return delete e.role,e},[eb,ew,q,en]),eS=C.useMemo(()=>ex({onMouseEnter(){W&&"menu"!==t.type||S(!1)},onMouseMove(){q(!0)},onClick(){W&&S(!1)}}),[ex,W,t.type,q]),eC=C.useMemo(()=>e_(),[e_]),eE=C.useMemo(()=>({activeIndex:E,setActiveIndex:T,allowMouseUpTriggerRef:t.type?t.context.allowMouseUpTriggerRef:i0,floatingRootContext:ec,itemProps:eC,popupProps:eS,triggerProps:ek,itemDomElements:D,itemLabels:Z,mounted:J,open:K,popupRef:M,positionerRef:A,setOpen:es,setPositionerElement:Q,triggerElement:v,setTriggerElement:y,transitionStatus:et,lastOpenChangeReason:N,instantType:_,onOpenChangeComplete:i,setHoverEnabled:S,typingRef:ev,modal:V,disabled:s,parent:t,rootId:H,allowMouseEnter:B,setAllowMouseEnter:q}),[E,ec,eC,eS,ek,D,Z,J,K,A,es,et,v,Q,N,_,i,V,s,t,H,B,q]),eT=(0,j.jsx)(iE.Provider,{value:eE,children:n});return void 0===t.type||"context-menu"===t.type?(0,j.jsx)(oO,{children:eT}):eT};function i2(e,t,r,n){var o,a,i,l,s;let c=oh(i3).current;return o=c,a=e,i=t,l=r,s=n,(o.refs[0]!==a||o.refs[1]!==i||o.refs[2]!==l||o.refs[3]!==s)&&i4(c,[e,t,r,n]),c.callback}function i3(){return{callback:null,cleanup:null,refs:[]}}function i4(e,t){if(e.refs=t,t.every(e=>null==e)){e.callback=null;return}e.callback=r=>{if(e.cleanup&&(e.cleanup(),e.cleanup=null),null!=r){let n=Array(t.length).fill(null);for(let e=0;e<t.length;e+=1){let o=t[e];if(null!=o)switch(typeof o){case"function":{let t=o(r);"function"==typeof t&&(n[e]=t);break}case"object":o.current=r}}e.cleanup=()=>{for(let e=0;e<t.length;e+=1){let r=t[e];if(null!=r)switch(typeof r){case"function":{let t=n[e];"function"==typeof t?t():r(null);break}case"object":r.current=null}}}}}}let i5=((o={}).startingStyle="data-starting-style",o.endingStyle="data-ending-style",o),i6={[i5.startingStyle]:""},i9={[i5.endingStyle]:""},i8={transitionStatus:e=>"starting"===e?i6:"ending"===e?i9:null},i7=((a={}).open="data-open",a.closed="data-closed",a[a.startingStyle=i5.startingStyle]="startingStyle",a[a.endingStyle=i5.endingStyle]="endingStyle",a.anchorHidden="data-anchor-hidden",a),le=((i={}).popupOpen="data-popup-open",i.pressed="data-pressed",i),lt={[le.popupOpen]:""},lr={[le.popupOpen]:"",[le.pressed]:""},ln={[i7.open]:""},lo={[i7.closed]:""},la={[i7.anchorHidden]:""},li={open:e=>e?lt:null},ll={open:e=>e?lr:null},ls={open:e=>e?ln:lo,anchorHidden:e=>e?la:null},lc=parseInt(C.version,10);function lu(e,t,r={}){let n=t.render,o=function(e,t={}){var r,n,o,a,i;let l,{className:s,render:c}=e,{state:u=aV,ref:d,props:f,disableStyleHooks:p,customStyleHookMapping:h,enabled:m=!0}=t,g=m?(r=s,n=u,"function"==typeof r?r(n):r):void 0;!0!==p&&(l=C.useMemo(()=>m?function(e,t){let r={};for(let n in e){let o=e[n];if(t?.hasOwnProperty(n)){let e=t[n](o);null!=e&&Object.assign(r,e);continue}!0===o?r[`data-${n.toLowerCase()}`]="":o&&(r[`data-${n.toLowerCase()}`]=o.toString())}return r}(u,h):aV,[u,h,m]));let v=m?iB(l,Array.isArray(f)?function(e){if(0===e.length)return iq;if(1===e.length)return iX(e[0],iq);let t={...iX(e[0],iq)};for(let r=1;r<e.length;r+=1)t=iK(t,e[r]);return t}(f):f)??aV:aV;if("undefined"!=typeof document)if(m)if(Array.isArray(d)){let e;o=[v.ref,ld(c),...d],a=e=oh(i3).current,i=o,(a.refs.length!==i.length||a.refs.some((e,t)=>e!==i[t]))&&i4(e,o),v.ref=e.callback}else v.ref=i2(v.ref,ld(c),d);else i2(null,null);return m?(void 0!==g&&(v.className=iQ(v.className,g)),v):aV}(t,r);return!1===r.enabled?null:function(e,t,r,n){if(t){if("function"==typeof t)return t(r,n);let e=iW(r,t.props);return e.ref=r.ref,C.cloneElement(t,e)}if(e&&"string"==typeof e){var o,a;return o=e,a=r,"button"===o?(0,j.jsx)("button",{type:"button",...a}):"img"===o?(0,j.jsx)("img",{alt:"",...a}):C.createElement(o,a)}throw Error("Base UI: Render element or function are not defined.")}(e,n,o,r.state??aV)}function ld(e){return e&&"function"!=typeof e?lc>=19?e.props.ref:e.ref:null}let lf=C.createContext(void 0);function lp(e=!1){let t=C.useContext(lf);if(void 0===t&&!e)throw Error("Base UI: CompositeRootContext is missing. Composite parts must be placed within <Composite.Root>.");return t}function lh(e={}){let{disabled:t=!1,focusableWhenDisabled:r,tabIndex:n=0,native:o=!0}=e,a=C.useRef(null),i=void 0!==lp(!0),l=o_(()=>{let e=a.current;return!!(e?.tagName==="A"&&e?.href)}),{props:s}=function(e){let{focusableWhenDisabled:t,disabled:r,composite:n=!1,tabIndex:o=0,isNativeButton:a}=e,i=n&&!1!==t,l=n&&!1===t;return{props:C.useMemo(()=>{let e={onKeyDown(e){r&&t&&"Tab"!==e.key&&e.preventDefault()}};return n||(e.tabIndex=o,!a&&r&&(e.tabIndex=t?o:-1)),(a&&(t||i)||!a&&r)&&(e["aria-disabled"]=r),a&&(!t||l)&&(e.disabled=r),e},[n,r,t,i,l,a,o])}}({focusableWhenDisabled:r,disabled:t,composite:i,tabIndex:n,isNativeButton:o});return oL(()=>{let e=a.current;e instanceof HTMLButtonElement&&i&&t&&void 0===s.disabled&&e.disabled&&(e.disabled=!1)},[t,s.disabled,i]),{getButtonProps:C.useCallback((e={})=>{let{onClick:r,onMouseDown:n,onKeyUp:a,onKeyDown:i,onPointerDown:c,...u}=e;return iW({type:o?"button":void 0,onClick(e){t?e.preventDefault():r?.(e)},onMouseDown(e){t||n?.(e)},onKeyDown(e){if(t||(iG(e),i?.(e)),e.baseUIHandlerPrevented)return;let n=e.target===e.currentTarget&&!o&&!l()&&!t,a="Enter"===e.key,s=" "===e.key;n&&((s||a)&&e.preventDefault(),a&&r?.(e))},onKeyUp(e){t||(iG(e),a?.(e)),!e.baseUIHandlerPrevented&&(e.target!==e.currentTarget||o||t||" "!==e.key||r?.(e))},onPointerDown(e){t?e.preventDefault():c?.(e)}},o?void 0:{role:"button"},s,u)},[t,s,o,l]),buttonRef:a}}let lm=C.createContext({register:()=>{},unregister:()=>{},subscribeMapChange:()=>()=>{},elementsRef:{current:[]},nextIndexRef:{current:0}}),lg=((l={})[l.None=0]="None",l[l.GuessFromOrder=1]="GuessFromOrder",l);function lv(e={}){let{label:t,metadata:r,textRef:n,indexGuessBehavior:o}=e,{register:a,unregister:i,subscribeMapChange:l,elementsRef:s,labelsRef:c,nextIndexRef:u}=C.useContext(lm),d=C.useRef(-1),[f,p]=C.useState(o===lg.GuessFromOrder?()=>{if(-1===d.current){let e=u.current;u.current+=1,d.current=e}return d.current}:-1),h=C.useRef(null),m=C.useCallback(e=>{if(h.current=e,-1!==f&&null!==e&&(s.current[f]=e,c)){let r=void 0!==t;c.current[f]=r?t:n?.current?.textContent??e.textContent}},[f,s,c,t,n]);return oL(()=>{let e=h.current;if(e)return a(e,r),()=>{i(e)}},[a,i,r]),oL(()=>l(e=>{let t=h.current?e.get(h.current)?.index:null;null!=t&&p(t)}),[l,p]),C.useMemo(()=>({ref:m,index:f}),[f,m])}function ly(e){let{render:t,className:r,state:n=aV,props:o=aB,refs:a=aB,metadata:i,customStyleHookMapping:l,tag:s="div",...c}=e,{compositeProps:u,compositeRef:d}=function(e={}){let{highlightItemOnHover:t,highlightedIndex:r,onHighlightedIndexChange:n}=lp(),{ref:o,index:a}=lv(e),i=r===a,l=C.useRef(null),s=i2(o,l);return{compositeProps:C.useMemo(()=>({tabIndex:i?0:-1,onFocus(){n(a)},onMouseMove(){let e=l.current;if(!t||!e)return;let r=e.hasAttribute("disabled")||"true"===e.ariaDisabled;i||r||e.focus()}}),[i,n,a,t]),compositeRef:s,index:a}}({metadata:i});return lu(s,e,{state:n,ref:[...a,d],props:[u,...o,c],customStyleHookMapping:l})}let lb=C.forwardRef(function(e,t){let{render:r,className:n,disabled:o=!1,nativeButton:a=!0,...i}=e,{triggerProps:l,disabled:s,setTriggerElement:c,open:u,allowMouseUpTriggerRef:d,positionerRef:f,parent:p,lastOpenChangeReason:h,rootId:m}=iT(),g=o||s,v=C.useRef(null),y=oy(),{getButtonProps:b,buttonRef:x}=lh({disabled:g,native:a}),_=i2(x,c),{events:w}=C.useContext(oP);C.useEffect(()=>{u||void 0!==p.type||(d.current=!1)},[d,u,p.type]);let k=o_(e=>{if(!v.current)return;y.clear(),d.current=!1;let t=e.target;if(aw(v.current,t)||aw(f.current,t)||t===v.current||null!=t&&function e(t){return oH(t)&&t.hasAttribute("data-rootownerid")?t.getAttribute("data-rootownerid")??void 0:o2(t)?void 0:e(o5(t))}(t)===m)return;let r=function(e){let t=e.getBoundingClientRect(),r=window.getComputedStyle(e,"::before"),n=window.getComputedStyle(e,"::after");if("none"===r.content&&"none"===n.content)return t;let o=parseFloat(r.width)||0,a=parseFloat(r.height)||0,i=parseFloat(n.width)||0,l=parseFloat(n.height)||0,s=Math.max(t.width,o,i),c=Math.max(t.height,a,l),u=s-t.width,d=c-t.height;return{left:t.left-u/2,right:t.right+u/2,top:t.top-d/2,bottom:t.bottom+d/2}}(v.current);e.clientX>=r.left-2&&e.clientX<=r.right+2&&e.clientY>=r.top-2&&e.clientY<=r.bottom+2||w.emit("close",{domEvent:e,reason:"cancel-open"})});C.useEffect(()=>{u&&"trigger-hover"===h&&iR(v.current).addEventListener("mouseup",k,{once:!0})},[u,k,h]);let S="menubar"===p.type,E=C.useCallback(e=>iW(S?{role:"menuitem"}:{},{"aria-haspopup":"menu",ref:_,onMouseDown:e=>{u||(y.start(200,()=>{d.current=!0}),iR(e.currentTarget).addEventListener("mouseup",k,{once:!0}))}},e,b),[b,_,u,d,y,k,S]),T=C.useMemo(()=>({disabled:g,open:u}),[g,u]),N=[v,t,x],L=[l,i,E],I=lu("button",e,{enabled:!S,customStyleHookMapping:ll,state:T,ref:N,props:L});return S?(0,j.jsx)(ly,{tag:"button",render:r,className:n,state:T,refs:N,props:L,customStyleHookMapping:ll}):I}),lx={clip:"rect(0 0 0 0)",overflow:"hidden",whiteSpace:"nowrap",position:"fixed",top:0,left:0,border:0,padding:0,width:1,height:1,margin:-1},l_=C.forwardRef(function(e,t){let[r,n]=C.useState();return oL(()=>{ai&&n("button")},[]),(0,j.jsx)("span",{...e,ref:t,tabIndex:0,role:r,"aria-hidden":!r||void 0,style:lx,"data-base-ui-focus-guard":""})});var lw='input:not([inert]),select:not([inert]),textarea:not([inert]),a[href]:not([inert]),button:not([inert]),[tabindex]:not(slot):not([inert]),audio[controls]:not([inert]),video[controls]:not([inert]),[contenteditable]:not([contenteditable="false"]):not([inert]),details>summary:first-of-type:not([inert]),details:not([inert])',lk="undefined"==typeof Element,lj=lk?function(){}:Element.prototype.matches||Element.prototype.msMatchesSelector||Element.prototype.webkitMatchesSelector,lS=!lk&&Element.prototype.getRootNode?function(e){var t;return null==e||null==(t=e.getRootNode)?void 0:t.call(e)}:function(e){return null==e?void 0:e.ownerDocument},lC=function e(t,r){void 0===r&&(r=!0);var n,o=null==t||null==(n=t.getAttribute)?void 0:n.call(t,"inert");return""===o||"true"===o||r&&t&&e(t.parentNode)},lE=function(e){var t,r=null==e||null==(t=e.getAttribute)?void 0:t.call(e,"contenteditable");return""===r||"true"===r},lT=function(e,t,r){if(lC(e))return[];var n=Array.prototype.slice.apply(e.querySelectorAll(lw));return t&&lj.call(e,lw)&&n.unshift(e),n=n.filter(r)},lN=function e(t,r,n){for(var o=[],a=Array.from(t);a.length;){var i=a.shift();if(!lC(i,!1))if("SLOT"===i.tagName){var l=i.assignedElements(),s=e(l.length?l:i.children,!0,n);n.flatten?o.push.apply(o,s):o.push({scopeParent:i,candidates:s})}else{lj.call(i,lw)&&n.filter(i)&&(r||!t.includes(i))&&o.push(i);var c=i.shadowRoot||"function"==typeof n.getShadowRoot&&n.getShadowRoot(i),u=!lC(c,!1)&&(!n.shadowRootFilter||n.shadowRootFilter(i));if(c&&u){var d=e(!0===c?i.children:c.children,!0,n);n.flatten?o.push.apply(o,d):o.push({scopeParent:i,candidates:d})}else a.unshift.apply(a,i.children)}}return o},lL=function(e){return!isNaN(parseInt(e.getAttribute("tabindex"),10))},lI=function(e){if(!e)throw Error("No node provided");return e.tabIndex<0&&(/^(AUDIO|VIDEO|DETAILS)$/.test(e.tagName)||lE(e))&&!lL(e)?0:e.tabIndex},lP=function(e,t){var r=lI(e);return r<0&&t&&!lL(e)?0:r},lz=function(e,t){return e.tabIndex===t.tabIndex?e.documentOrder-t.documentOrder:e.tabIndex-t.tabIndex},lR=function(e){return"INPUT"===e.tagName},lO=function(e,t){for(var r=0;r<e.length;r++)if(e[r].checked&&e[r].form===t)return e[r]},lM=function(e){if(!e.name)return!0;var t,r=e.form||lS(e),n=function(e){return r.querySelectorAll('input[type="radio"][name="'+e+'"]')};if("undefined"!=typeof window&&void 0!==window.CSS&&"function"==typeof window.CSS.escape)t=n(window.CSS.escape(e.name));else try{t=n(e.name)}catch(e){return console.error("Looks like you have a radio button with a name attribute containing invalid CSS selector characters and need the CSS.escape polyfill: %s",e.message),!1}var o=lO(t,e.form);return!o||o===e},lA=function(e){var t;return lR(t=e)&&"radio"===t.type&&!lM(e)},lD=function(e){var t,r,n,o,a,i,l,s=e&&lS(e),c=null==(t=s)?void 0:t.host,u=!1;if(s&&s!==e)for(u=!!(null!=(r=c)&&null!=(n=r.ownerDocument)&&n.contains(c)||null!=e&&null!=(o=e.ownerDocument)&&o.contains(e));!u&&c;)u=!!(null!=(i=c=null==(a=s=lS(c))?void 0:a.host)&&null!=(l=i.ownerDocument)&&l.contains(c));return u},lZ=function(e){var t=e.getBoundingClientRect(),r=t.width,n=t.height;return 0===r&&0===n},lF=function(e,t){var r=t.displayCheck,n=t.getShadowRoot;if("hidden"===getComputedStyle(e).visibility)return!0;var o=lj.call(e,"details>summary:first-of-type")?e.parentElement:e;if(lj.call(o,"details:not([open]) *"))return!0;if(r&&"full"!==r&&"legacy-full"!==r){if("non-zero-area"===r)return lZ(e)}else{if("function"==typeof n){for(var a=e;e;){var i=e.parentElement,l=lS(e);if(i&&!i.shadowRoot&&!0===n(i))return lZ(e);e=e.assignedSlot?e.assignedSlot:i||l===e.ownerDocument?i:l.host}e=a}if(lD(e))return!e.getClientRects().length;if("legacy-full"!==r)return!0}return!1},lU=function(e){if(/^(INPUT|BUTTON|SELECT|TEXTAREA)$/.test(e.tagName))for(var t=e.parentElement;t;){if("FIELDSET"===t.tagName&&t.disabled){for(var r=0;r<t.children.length;r++){var n=t.children.item(r);if("LEGEND"===n.tagName)return!!lj.call(t,"fieldset[disabled] *")||!n.contains(e)}return!0}t=t.parentElement}return!1},l$=function(e,t){var r,n;return!(t.disabled||lC(t)||lR(r=t)&&"hidden"===r.type||lF(t,e)||"DETAILS"===(n=t).tagName&&Array.prototype.slice.apply(n.children).some(function(e){return"SUMMARY"===e.tagName})||lU(t))},lH=function(e,t){return!(lA(t)||0>lI(t))&&!!l$(e,t)},lV=function(e){var t=parseInt(e.getAttribute("tabindex"),10);return!!isNaN(t)||!!(t>=0)},lB=function e(t){var r=[],n=[];return t.forEach(function(t,o){var a=!!t.scopeParent,i=a?t.scopeParent:t,l=lP(i,a),s=a?e(t.candidates):i;0===l?a?r.push.apply(r,s):r.push(i):n.push({documentOrder:o,tabIndex:l,item:t,isScope:a,content:s})}),n.sort(lz).reduce(function(e,t){return t.isScope?e.push.apply(e,t.content):e.push(t.content),e},[]).concat(r)},lq=function(e,t){return lB((t=t||{}).getShadowRoot?lN([e],t.includeContainer,{filter:lH.bind(null,t),flatten:!1,getShadowRoot:t.getShadowRoot,shadowRootFilter:lV}):lT(e,t.includeContainer,lH.bind(null,t)))},lW=function(e,t){return(t=t||{}).getShadowRoot?lN([e],t.includeContainer,{filter:l$.bind(null,t),flatten:!0,getShadowRoot:t.getShadowRoot}):lT(e,t.includeContainer,l$.bind(null,t))},lK=function(e,t){if(t=t||{},!e)throw Error("No node provided");return!1!==lj.call(e,lw)&&lH(t,e)};let lY=()=>({getShadowRoot:!0,displayCheck:"function"==typeof ResizeObserver&&ResizeObserver.toString().includes("[native code]")?"full":"none"});function lX(e,t){let r=lq(e,lY()),n=r.length;if(0===n)return;let o=a_(aS(e)),a=r.indexOf(o);return r[-1===a?1===t?0:n-1:a+t]}function lG(e){return lX(aS(e).body,1)||e}function lQ(e){return lX(aS(e).body,-1)||e}function lJ(e,t){let r=t||e.currentTarget,n=e.relatedTarget;return!n||!aw(r,n)}function l0(e){lq(e,lY()).forEach(e=>{e.dataset.tabindex=e.getAttribute("tabindex")||"",e.setAttribute("tabindex","-1")})}function l1(e){e.querySelectorAll("[data-tabindex]").forEach(e=>{let t=e.dataset.tabindex;delete e.dataset.tabindex,t?e.setAttribute("tabindex",t):e.removeAttribute("tabindex")})}let l2=C.createContext(null),l3=aN("portal");function l4(e={}){let{id:t,root:r}=e,n=oT(),o=C.useContext(l2),[a,i]=C.useState(null),l=C.useRef(null);return oL(()=>()=>{a?.remove(),queueMicrotask(()=>{l.current=null})},[a]),oL(()=>{if(!n||l.current)return;let e=t?document.getElementById(t):null;if(!e)return;let r=document.createElement("div");r.id=n,r.setAttribute(l3,""),e.appendChild(r),l.current=r,i(r)},[t,n]),oL(()=>{if(null===r||!n||l.current)return;let e=r||o?.portalNode;e&&!oU(e)&&(e=e.current),e=e||document.body;let a=null;t&&((a=document.createElement("div")).id=t,e.appendChild(a));let s=document.createElement("div");s.id=n,s.setAttribute(l3,""),(e=a||e).appendChild(s),l.current=s,i(s)},[t,r,n,o]),a}function l5(e){let{children:t,id:r,root:n,preserveTabOrder:o=!0}=e,a=l4({id:r,root:n}),[i,l]=C.useState(null),s=C.useRef(null),c=C.useRef(null),u=C.useRef(null),d=C.useRef(null),f=i?.modal,p=i?.open,h=!!i&&!i.modal&&i.open&&o&&!!(n||a);return C.useEffect(()=>{if(a&&o&&!f)return a.addEventListener("focusin",e,!0),a.addEventListener("focusout",e,!0),()=>{a.removeEventListener("focusin",e,!0),a.removeEventListener("focusout",e,!0)};function e(e){if(a&&lJ(e)){let t="focusin"===e.type;(t?l1:l0)(a)}}},[a,o,f]),C.useEffect(()=>{!a||p||l1(a)},[p,a]),(0,j.jsxs)(l2.Provider,{value:C.useMemo(()=>({preserveTabOrder:o,beforeOutsideRef:s,afterOutsideRef:c,beforeInsideRef:u,afterInsideRef:d,portalNode:a,setFocusManagerState:l}),[o,a]),children:[h&&a&&(0,j.jsx)(l_,{"data-type":"outside",ref:s,onFocus:e=>{if(lJ(e,a))u.current?.focus();else{let e=lQ(i?i.domReference:null);e?.focus()}}}),h&&a&&(0,j.jsx)("span",{"aria-owns":a.id,style:lx}),a&&ej.createPortal(t,a),h&&a&&(0,j.jsx)(l_,{"data-type":"outside",ref:c,onFocus:e=>{if(lJ(e,a))d.current?.focus();else{let t=lG(i?i.domReference:null);t?.focus(),i?.closeOnFocusOut&&i?.onOpenChange(!1,e.nativeEvent,"focus-out")}}})]})}let l6=C.createContext(void 0);function l9(e){let{children:t,keepMounted:r=!1,container:n}=e,{mounted:o}=iT();return o||r?(0,j.jsx)(l6.Provider,{value:r,children:(0,j.jsx)(l5,{root:n,children:t})}):null}let l8=C.createContext(void 0);function l7(e,t,r){let n,{reference:o,floating:a}=e,i=ir(t),l=a7(ir(t)),s=ie(l),c=a9(t),u="y"===i,d=o.x+o.width/2-a.width/2,f=o.y+o.height/2-a.height/2,p=o[s]/2-a[s]/2;switch(c){case"top":n={x:d,y:o.y-a.height};break;case"bottom":n={x:d,y:o.y+o.height};break;case"right":n={x:o.x+o.width,y:f};break;case"left":n={x:o.x-a.width,y:f};break;default:n={x:o.x,y:o.y}}switch(a8(t)){case"start":n[l]-=p*(r&&u?-1:1);break;case"end":n[l]+=p*(r&&u?-1:1)}return n}let se=async(e,t,r)=>{let{placement:n="bottom",strategy:o="absolute",middleware:a=[],platform:i}=r,l=a.filter(Boolean),s=await (null==i.isRTL?void 0:i.isRTL(t)),c=await i.getElementRects({reference:e,floating:t,strategy:o}),{x:u,y:d}=l7(c,n,s),f=n,p={},h=0;for(let r=0;r<l.length;r++){let{name:a,fn:m}=l[r],{x:g,y:v,data:y,reset:b}=await m({x:u,y:d,initialPlacement:n,placement:f,strategy:o,middlewareData:p,rects:c,platform:i,elements:{reference:e,floating:t}});u=null!=g?g:u,d=null!=v?v:d,p={...p,[a]:{...p[a],...y}},b&&h<=50&&(h++,"object"==typeof b&&(b.placement&&(f=b.placement),b.rects&&(c=!0===b.rects?await i.getElementRects({reference:e,floating:t,strategy:o}):b.rects),{x:u,y:d}=l7(c,f,s)),r=-1)}return{x:u,y:d,placement:f,strategy:o,middlewareData:p}};async function st(e,t){var r;void 0===t&&(t={});let{x:n,y:o,platform:a,rects:i,elements:l,strategy:s}=e,{boundary:c="clippingAncestors",rootBoundary:u="viewport",elementContext:d="floating",altBoundary:f=!1,padding:p=0}=a6(t,e),h=iu(p),m=l[f?"floating"===d?"reference":"floating":d],g=id(await a.getClippingRect({element:null==(r=await (null==a.isElement?void 0:a.isElement(m)))||r?m:m.contextElement||await (null==a.getDocumentElement?void 0:a.getDocumentElement(l.floating)),boundary:c,rootBoundary:u,strategy:s})),v="floating"===d?{x:n,y:o,width:i.floating.width,height:i.floating.height}:i.reference,y=await (null==a.getOffsetParent?void 0:a.getOffsetParent(l.floating)),b=await (null==a.isElement?void 0:a.isElement(y))&&await (null==a.getScale?void 0:a.getScale(y))||{x:1,y:1},x=id(a.convertOffsetParentRelativeRectToViewportRelativeRect?await a.convertOffsetParentRelativeRectToViewportRelativeRect({elements:l,rect:v,offsetParent:y,strategy:s}):v);return{top:(g.top-x.top+h.top)/b.y,bottom:(x.bottom-g.bottom+h.bottom)/b.y,left:(g.left-x.left+h.left)/b.x,right:(x.right-g.right+h.right)/b.x}}function sr(e,t){return{top:e.top-t.height,right:e.right-t.width,bottom:e.bottom-t.height,left:e.left-t.width}}function sn(e){return aQ.some(t=>e[t]>=0)}let so=new Set(["left","top"]);async function sa(e,t){let{placement:r,platform:n,elements:o}=e,a=await (null==n.isRTL?void 0:n.isRTL(o.floating)),i=a9(r),l=a8(r),s="y"===ir(r),c=so.has(i)?-1:1,u=a&&s?-1:1,d=a6(t,e),{mainAxis:f,crossAxis:p,alignmentAxis:h}="number"==typeof d?{mainAxis:d,crossAxis:0,alignmentAxis:null}:{mainAxis:d.mainAxis||0,crossAxis:d.crossAxis||0,alignmentAxis:d.alignmentAxis};return l&&"number"==typeof h&&(p="end"===l?-1*h:h),s?{x:p*u,y:f*c}:{x:f*c,y:p*u}}function si(e){let t=o3(e),r=parseFloat(t.width)||0,n=parseFloat(t.height)||0,o=oH(e),a=o?e.offsetWidth:r,i=o?e.offsetHeight:n,l=a1(r)!==a||a1(n)!==i;return l&&(r=a,n=i),{width:r,height:n,$:l}}function sl(e){return o$(e)?e:e.contextElement}function ss(e){let t=sl(e);if(!oH(t))return a3(1);let r=t.getBoundingClientRect(),{width:n,height:o,$:a}=si(t),i=(a?a1(r.width):r.width)/n,l=(a?a1(r.height):r.height)/o;return i&&Number.isFinite(i)||(i=1),l&&Number.isFinite(l)||(l=1),{x:i,y:l}}let sc=a3(0);function su(e){let t=oZ(e);return o0()&&t.visualViewport?{x:t.visualViewport.offsetLeft,y:t.visualViewport.offsetTop}:sc}function sd(e,t,r,n){var o,a,i;void 0===t&&(t=!1),void 0===r&&(r=!1);let l=e.getBoundingClientRect(),s=sl(e),c=a3(1);t&&(n?o$(n)&&(c=ss(n)):c=ss(e));let u=(o=s,void 0===(a=r)&&(a=!1),(i=n)&&(!a||i===oZ(o))&&a)?su(s):a3(0),d=(l.left+u.x)/c.x,f=(l.top+u.y)/c.y,p=l.width/c.x,h=l.height/c.y;if(s){let e=oZ(s),t=n&&o$(n)?oZ(n):n,r=e,o=o9(r);for(;o&&n&&t!==r;){let e=ss(o),t=o.getBoundingClientRect(),n=o3(o),a=t.left+(o.clientLeft+parseFloat(n.paddingLeft))*e.x,i=t.top+(o.clientTop+parseFloat(n.paddingTop))*e.y;d*=e.x,f*=e.y,p*=e.x,h*=e.y,d+=a,f+=i,o=o9(r=oZ(o))}}return id({width:p,height:h,x:d,y:f})}function sf(e,t){let r=o4(e).scrollLeft;return t?t.left+r:sd(oF(e)).left+r}function sp(e,t,r){void 0===r&&(r=!1);let n=e.getBoundingClientRect(),o=n.left+t.scrollLeft-(r?0:sf(e,n));return{x:o,y:n.top+t.scrollTop}}let sh=new Set(["absolute","fixed"]);function sm(e,t,r){var n,o;let a;if("viewport"===t)a=function(e,t){let r=oZ(e),n=oF(e),o=r.visualViewport,a=n.clientWidth,i=n.clientHeight,l=0,s=0;if(o){a=o.width,i=o.height;let e=o0();(!e||e&&"fixed"===t)&&(l=o.offsetLeft,s=o.offsetTop)}return{width:a,height:i,x:l,y:s}}(e,r);else if("document"===t){let t,r,o,i,l,s,c;n=oF(e),t=oF(n),r=o4(n),o=n.ownerDocument.body,i=a0(t.scrollWidth,t.clientWidth,o.scrollWidth,o.clientWidth),l=a0(t.scrollHeight,t.clientHeight,o.scrollHeight,o.clientHeight),s=-r.scrollLeft+sf(n),c=-r.scrollTop,"rtl"===o3(o).direction&&(s+=a0(t.clientWidth,o.clientWidth)-i),a={width:i,height:l,x:s,y:c}}else if(o$(t)){let e,n,i,l,s,c,u;n=(e=sd(o=t,!0,"fixed"===r)).top+o.clientTop,i=e.left+o.clientLeft,l=oH(o)?ss(o):a3(1),s=o.clientWidth*l.x,c=o.clientHeight*l.y,u=i*l.x,a={width:s,height:c,x:u,y:n*l.y}}else{let r=su(e);a={x:t.x-r.x,y:t.y-r.y,width:t.width,height:t.height}}return id(a)}function sg(e){return"static"===o3(e).position}function sv(e,t){if(!oH(e)||"fixed"===o3(e).position)return null;if(t)return t(e);let r=e.offsetParent;return oF(e)===r&&(r=r.ownerDocument.body),r}function sy(e,t){var r;let n=oZ(e);if(oY(e))return n;if(!oH(e)){let t=o5(e);for(;t&&!o2(t);){if(o$(t)&&!sg(t))return t;t=o5(t)}return n}let o=sv(e,t);for(;o&&(r=o,oW.has(oD(r)))&&sg(o);)o=sv(o,t);return o&&o2(o)&&sg(o)&&!oJ(o)?n:o||function(e){let t=o5(e);for(;oH(t)&&!o2(t);){if(oJ(t))return t;if(oY(t))break;t=o5(t)}return null}(e)||n}let sb=async function(e){let t=this.getOffsetParent||sy,r=this.getDimensions,n=await r(e.floating);return{reference:function(e,t,r){let n=oH(t),o=oF(t),a="fixed"===r,i=sd(e,!0,a,t),l={scrollLeft:0,scrollTop:0},s=a3(0);if(n||!n&&!a)if(("body"!==oD(t)||oq(o))&&(l=o4(t)),n){let e=sd(t,!0,a,t);s.x=e.x+t.clientLeft,s.y=e.y+t.clientTop}else o&&(s.x=sf(o));a&&!n&&o&&(s.x=sf(o));let c=!o||n||a?a3(0):sp(o,l),u=i.left+l.scrollLeft-s.x-c.x;return{x:u,y:i.top+l.scrollTop-s.y-c.y,width:i.width,height:i.height}}(e.reference,await t(e.floating),e.strategy),floating:{x:0,y:0,width:n.width,height:n.height}}},sx={convertOffsetParentRelativeRectToViewportRelativeRect:function(e){let{elements:t,rect:r,offsetParent:n,strategy:o}=e,a="fixed"===o,i=oF(n),l=!!t&&oY(t.floating);if(n===i||l&&a)return r;let s={scrollLeft:0,scrollTop:0},c=a3(1),u=a3(0),d=oH(n);if((d||!d&&!a)&&(("body"!==oD(n)||oq(i))&&(s=o4(n)),oH(n))){let e=sd(n);c=ss(n),u.x=e.x+n.clientLeft,u.y=e.y+n.clientTop}let f=!i||d||a?a3(0):sp(i,s,!0);return{width:r.width*c.x,height:r.height*c.y,x:r.x*c.x-s.scrollLeft*c.x+u.x+f.x,y:r.y*c.y-s.scrollTop*c.y+u.y+f.y}},getDocumentElement:oF,getClippingRect:function(e){let{element:t,boundary:r,rootBoundary:n,strategy:o}=e,a=[..."clippingAncestors"===r?oY(t)?[]:function(e,t){let r=t.get(e);if(r)return r;let n=o6(e,[],!1).filter(e=>o$(e)&&"body"!==oD(e)),o=null,a="fixed"===o3(e).position,i=a?o5(e):e;for(;o$(i)&&!o2(i);){let t=o3(i),r=oJ(i);r||"fixed"!==t.position||(o=null),(a?!r&&!o:!r&&"static"===t.position&&!!o&&sh.has(o.position)||oq(i)&&!r&&function e(t,r){let n=o5(t);return!(n===r||!o$(n)||o2(n))&&("fixed"===o3(n).position||e(n,r))}(e,i))?n=n.filter(e=>e!==i):o=t,i=o5(i)}return t.set(e,n),n}(t,this._c):[].concat(r),n],i=a[0],l=a.reduce((e,r)=>{let n=sm(t,r,o);return e.top=a0(n.top,e.top),e.right=aJ(n.right,e.right),e.bottom=aJ(n.bottom,e.bottom),e.left=a0(n.left,e.left),e},sm(t,i,o));return{width:l.right-l.left,height:l.bottom-l.top,x:l.left,y:l.top}},getOffsetParent:sy,getElementRects:sb,getClientRects:function(e){return Array.from(e.getClientRects())},getDimensions:function(e){let{width:t,height:r}=si(e);return{width:t,height:r}},getScale:ss,isElement:o$,isRTL:function(e){return"rtl"===o3(e).direction}};function s_(e,t){return e.x===t.x&&e.y===t.y&&e.width===t.width&&e.height===t.height}function sw(e,t,r,n){let o;void 0===n&&(n={});let{ancestorScroll:a=!0,ancestorResize:i=!0,elementResize:l="function"==typeof ResizeObserver,layoutShift:s="function"==typeof IntersectionObserver,animationFrame:c=!1}=n,u=sl(e),d=a||i?[...u?o6(u):[],...o6(t)]:[];d.forEach(e=>{a&&e.addEventListener("scroll",r,{passive:!0}),i&&e.addEventListener("resize",r)});let f=u&&s?function(e,t){let r,n=null,o=oF(e);function a(){var e;clearTimeout(r),null==(e=n)||e.disconnect(),n=null}return!function i(l,s){void 0===l&&(l=!1),void 0===s&&(s=1),a();let c=e.getBoundingClientRect(),{left:u,top:d,width:f,height:p}=c;if(l||t(),!f||!p)return;let h=a2(d),m=a2(o.clientWidth-(u+f)),g=a2(o.clientHeight-(d+p)),v={rootMargin:-h+"px "+-m+"px "+-g+"px "+-a2(u)+"px",threshold:a0(0,aJ(1,s))||1},y=!0;function b(t){let n=t[0].intersectionRatio;if(n!==s){if(!y)return i();n?i(!1,n):r=setTimeout(()=>{i(!1,1e-7)},1e3)}1!==n||s_(c,e.getBoundingClientRect())||i(),y=!1}try{n=new IntersectionObserver(b,{...v,root:o.ownerDocument})}catch(e){n=new IntersectionObserver(b,v)}n.observe(e)}(!0),a}(u,r):null,p=-1,h=null;l&&(h=new ResizeObserver(e=>{let[n]=e;n&&n.target===u&&h&&(h.unobserve(t),cancelAnimationFrame(p),p=requestAnimationFrame(()=>{var e;null==(e=h)||e.observe(t)})),r()}),u&&!c&&h.observe(u),h.observe(t));let m=c?sd(e):null;return c&&function t(){let n=sd(e);m&&!s_(m,n)&&r(),m=n,o=requestAnimationFrame(t)}(),r(),()=>{var e;d.forEach(e=>{a&&e.removeEventListener("scroll",r),i&&e.removeEventListener("resize",r)}),null==f||f(),null==(e=h)||e.disconnect(),h=null,c&&cancelAnimationFrame(o)}}var sk="undefined"!=typeof document,sj=sk?C.useLayoutEffect:function(){};function sS(e,t){let r,n,o;if(e===t)return!0;if(typeof e!=typeof t)return!1;if("function"==typeof e&&e.toString()===t.toString())return!0;if(e&&t&&"object"==typeof e){if(Array.isArray(e)){if((r=e.length)!==t.length)return!1;for(n=r;0!=n--;)if(!sS(e[n],t[n]))return!1;return!0}if((r=(o=Object.keys(e)).length)!==Object.keys(t).length)return!1;for(n=r;0!=n--;)if(!({}).hasOwnProperty.call(t,o[n]))return!1;for(n=r;0!=n--;){let r=o[n];if(("_owner"!==r||!e.$$typeof)&&!sS(e[r],t[r]))return!1}return!0}return e!=e&&t!=t}function sC(e){return"undefined"==typeof window?1:(e.ownerDocument.defaultView||window).devicePixelRatio||1}function sE(e,t){let r=sC(e);return Math.round(t*r)/r}function sT(e){let t=C.useRef(e);return sj(()=>{t.current=e}),t}function sN(e,t,r){let n="inline-start"===e||"inline-end"===e;return({top:"top",right:n?r?"inline-start":"inline-end":"right",bottom:"bottom",left:n?r?"inline-end":"inline-start":"left"})[t]}function sL(e,t,r){let{rects:n,placement:o}=e;return{side:sN(t,a9(o),r),align:a8(o)||"center",anchor:{width:n.reference.width,height:n.reference.height},positioner:{width:n.floating.width,height:n.floating.height}}}function sI(e){var t,r,n,o,a,i,l,s,c,u,d,f,p,h,m,g,v;let y,{anchor:b,positionMethod:x="absolute",side:_="bottom",sideOffset:w=0,align:k="center",alignOffset:j=0,collisionBoundary:S,collisionPadding:E=5,sticky:T=!1,arrowPadding:N=5,trackAnchor:L=!0,keepMounted:I=!1,floatingRootContext:P,mounted:z,collisionAvoidance:R,shiftCrossAxis:O=!1,nodeId:M,adaptiveOrigin:A}=e,D=R.side||"flip",Z=R.align||"flip",F=R.fallbackAxisSide||"end",U="function"==typeof b?b:void 0,$=o_(U),H=U?$:b,V=o8(b),B="rtl"===iz(),q={top:"top",right:"right",bottom:"bottom",left:"left","inline-end":B?"left":"right","inline-start":B?"right":"left"}[_],W="center"===k?q:`${q}-${k}`,K={boundary:"clipping-ancestors"===S?"clippingAncestors":S,padding:E},Y=C.useRef(null),X=o8(w),G=o8(j),Q="function"!=typeof w?w:0,J=[(t=e=>{let t=sL(e,_,B),r="function"==typeof X.current?X.current(t):X.current,n="function"==typeof G.current?G.current(t):G.current;return{mainAxis:r,crossAxis:n,alignmentAxis:n}},r=[Q,"function"!=typeof j?j:0,B,_],{...(void 0===(n=t)&&(n=0),{name:"offset",options:n,async fn(e){var t,r;let{x:o,y:a,placement:i,middlewareData:l}=e,s=await sa(e,n);return i===(null==(t=l.offset)?void 0:t.placement)&&null!=(r=l.arrow)&&r.alignmentOffset?{}:{x:o+s.x,y:a+s.y,data:{...s,placement:i}}}}),options:[t,r]})],ee="none"===Z&&"shift"!==D,et=!ee&&(T||O||"shift"===D),er="none"===D?null:{...{name:"flip",options:i=o={...K,mainAxis:!O&&"flip"===D,crossAxis:"flip"===Z&&"alignment",fallbackAxisSideDirection:F},async fn(e){var t,r,n,o,a,l,s,c,u,d,f,p,h;let m,g,v,{placement:y,middlewareData:b,rects:x,initialPlacement:_,platform:w,elements:k}=e,{mainAxis:j=!0,crossAxis:S=!0,fallbackPlacements:C,fallbackStrategy:E="bestFit",fallbackAxisSideDirection:T="none",flipAlignment:N=!0,...L}=a6(i,e);if(null!=(t=b.arrow)&&t.alignmentOffset)return{};let I=a9(y),P=ir(_),z=a9(_)===_,R=await (null==w.isRTL?void 0:w.isRTL(k.floating)),O=C||(z||!N?[ic(_)]:(m=ic(l=_),[io(l),m,io(m)])),M="none"!==T;!C&&M&&O.push(...(s=_,c=N,u=T,d=R,g=a8(s),v=function(e,t,r){switch(e){case"top":case"bottom":if(r)return t?ii:ia;return t?ia:ii;case"left":case"right":return t?il:is;default:return[]}}(a9(s),"start"===u,d),g&&(v=v.map(e=>e+"-"+g),c&&(v=v.concat(v.map(io)))),v));let A=[_,...O],D=await st(e,L),Z=[],F=(null==(r=b.flip)?void 0:r.overflows)||[];if(j&&Z.push(D[I]),S){let e,t,r,n,o=(f=y,p=x,void 0===(h=R)&&(h=!1),e=a8(f),t=a7(ir(f)),r=ie(t),n="x"===t?e===(h?"end":"start")?"right":"left":"start"===e?"bottom":"top",p.reference[r]>p.floating[r]&&(n=ic(n)),[n,ic(n)]);Z.push(D[o[0]],D[o[1]])}if(F=[...F,{placement:y,overflows:Z}],!Z.every(e=>e<=0)){let e=((null==(n=b.flip)?void 0:n.index)||0)+1,t=A[e];if(t&&("alignment"!==S||P===ir(t)||F.every(e=>ir(e.placement)!==P||e.overflows[0]>0)))return{data:{index:e,overflows:F},reset:{placement:t}};let r=null==(o=F.filter(e=>e.overflows[0]<=0).sort((e,t)=>e.overflows[1]-t.overflows[1])[0])?void 0:o.placement;if(!r)switch(E){case"bestFit":{let e=null==(a=F.filter(e=>{if(M){let t=ir(e.placement);return t===P||"y"===t}return!0}).map(e=>[e.placement,e.overflows.filter(e=>e>0).reduce((e,t)=>e+t,0)]).sort((e,t)=>e[1]-t[1])[0])?void 0:a[0];e&&(r=e);break}case"initialPlacement":r=_}if(y!==r)return{reset:{placement:r}}}return{}}},options:[o,a]},en=ee?null:(l=e=>{var t,r,n;let o=iR(e.elements.floating).documentElement;return{...K,rootBoundary:O?{x:0,y:0,width:o.clientWidth,height:o.clientHeight}:void 0,mainAxis:"none"!==Z,crossAxis:et,limiter:T||O?void 0:{...(void 0===(n=t=()=>{if(!Y.current)return{};let{height:e}=Y.current.getBoundingClientRect();return{offset:e/2+("number"==typeof E?E:0)}})&&(n={}),{options:n,fn(e){let{x:t,y:r,placement:o,rects:a,middlewareData:i}=e,{offset:l=0,mainAxis:s=!0,crossAxis:c=!0}=a6(n,e),u={x:t,y:r},d=ir(o),f=a7(d),p=u[f],h=u[d],m=a6(l,e),g="number"==typeof m?{mainAxis:m,crossAxis:0}:{mainAxis:0,crossAxis:0,...m};if(s){let e="y"===f?"height":"width",t=a.reference[f]-a.floating[e]+g.mainAxis,r=a.reference[f]+a.reference[e]-g.mainAxis;p<t?p=t:p>r&&(p=r)}if(c){var v,y;let e="y"===f?"width":"height",t=so.has(a9(o)),r=a.reference[d]-a.floating[e]+(t&&(null==(v=i.offset)?void 0:v[d])||0)+(t?0:g.crossAxis),n=a.reference[d]+a.reference[e]+(t?0:(null==(y=i.offset)?void 0:y[d])||0)-(t?g.crossAxis:0);h<r?h=r:h>n&&(h=n)}return{[f]:p,[d]:h}}}),options:[t,r]}}},s=[K,T,O,E,Z],{...(void 0===(c=l)&&(c={}),{name:"shift",options:c,async fn(e){let{x:t,y:r,placement:n}=e,{mainAxis:o=!0,crossAxis:a=!1,limiter:i={fn:e=>{let{x:t,y:r}=e;return{x:t,y:r}}},...l}=a6(c,e),s={x:t,y:r},u=await st(e,l),d=ir(a9(n)),f=a7(d),p=s[f],h=s[d];if(o){let e="y"===f?"top":"left",t="y"===f?"bottom":"right",r=p+u[e],n=p-u[t];p=a0(r,aJ(p,n))}if(a){let e="y"===d?"top":"left",t="y"===d?"bottom":"right",r=h+u[e],n=h-u[t];h=a0(r,aJ(h,n))}let m=i.fn({...e,[f]:p,[d]:h});return{...m,data:{x:m.x-t,y:m.y-r,enabled:{[f]:o,[d]:a}}}}}),options:[l,s]});"shift"===D||"shift"===Z||"center"===k?J.push(en,er):J.push(er,en),J.push({...{name:"size",options:f=u={...K,apply({elements:{floating:e},rects:{reference:t},availableWidth:r,availableHeight:n}){Object.entries({"--available-width":`${r}px`,"--available-height":`${n}px`,"--anchor-width":`${t.width}px`,"--anchor-height":`${t.height}px`}).forEach(([t,r])=>{e.style.setProperty(t,r)})}},async fn(e){var t,r;let n,o,{placement:a,rects:i,platform:l,elements:s}=e,{apply:c=()=>{},...u}=a6(f,e),d=await st(e,u),p=a9(a),h=a8(a),m="y"===ir(a),{width:g,height:v}=i.floating;"top"===p||"bottom"===p?(n=p,o=h===(await (null==l.isRTL?void 0:l.isRTL(s.floating))?"start":"end")?"left":"right"):(o=p,n="end"===h?"top":"bottom");let y=v-d.top-d.bottom,b=g-d.left-d.right,x=aJ(v-d[n],y),_=aJ(g-d[o],b),w=!e.middlewareData.shift,k=x,j=_;if(null!=(t=e.middlewareData.shift)&&t.enabled.x&&(j=b),null!=(r=e.middlewareData.shift)&&r.enabled.y&&(k=y),w&&!h){let e=a0(d.left,0),t=a0(d.right,0),r=a0(d.top,0),n=a0(d.bottom,0);m?j=g-2*(0!==e||0!==t?e+t:a0(d.left,d.right)):k=v-2*(0!==r||0!==n?r+n:a0(d.top,d.bottom))}await c({...e,availableWidth:j,availableHeight:k});let S=await l.getDimensions(s.floating);return g!==S.width||v!==S.height?{reset:{rects:!0}}:{}}},options:[u,d]},(p=()=>({element:Y.current||document.createElement("div"),padding:N,offsetParent:"floating"}),h=[N],{...{name:"arrow",options:y=p,async fn(e){let{x:t,y:r,placement:n,rects:o,platform:a,elements:i,middlewareData:l}=e,{element:s,padding:c=0,offsetParent:u="real"}=a6(y,e)||{};if(null==s)return{};let d=iu(c),f={x:t,y:r},p=a7(ir(n)),h=ie(p),m=await a.getDimensions(s),g="y"===p,v=g?"clientHeight":"clientWidth",b=o.reference[h]+o.reference[p]-f[p]-o.floating[h],x=f[p]-o.reference[p],_="real"===u?await a.getOffsetParent?.(s):i.floating,w=i.floating[v]||o.floating[h];w&&await a.isElement?.(_)||(w=i.floating[v]||o.floating[h]);let k=w/2-m[h]/2-1,j=Math.min(d[g?"top":"left"],k),S=Math.min(d[g?"bottom":"right"],k),C=w-m[h]-S,E=w/2-m[h]/2+(b/2-x/2),T=a0(j,aJ(E,C)),N=!l.arrow&&null!=a8(n)&&E!==T&&o.reference[h]/2-(E<j?j:S)-m[h]/2<0,L=N?E<j?E-j:E-C:0;return{[p]:f[p]+L,data:{[p]:T,centerOffset:E-T-L,...N&&{alignmentOffset:L}},reset:N}}},options:[p,h]}),{...(void 0===(v=m)&&(v={}),{name:"hide",options:v,async fn(e){let{rects:t}=e,{strategy:r="referenceHidden",...n}=a6(v,e);switch(r){case"referenceHidden":{let r=sr(await st(e,{...n,elementContext:"reference"}),t.reference);return{data:{referenceHiddenOffsets:r,referenceHidden:sn(r)}}}case"escaped":{let r=sr(await st(e,{...n,altBoundary:!0}),t.floating);return{data:{escapedOffsets:r,escaped:sn(r)}}}default:return{}}}}),options:[m,g]},{name:"transformOrigin",fn(e){let{elements:t,middlewareData:r,placement:n,rects:o,y:a}=e,i=a9(n),l=ir(i),s=Y.current,c=r.arrow?.x||0,u=r.arrow?.y||0,d=s?.clientWidth||0,f=s?.clientHeight||0,p=c+d/2,h=u+f/2,m=Math.abs(r.shift?.y||0),g=o.reference.height/2,v=m>("function"==typeof w?w(sL(e,_,B)):w),y={top:`${p}px calc(100% + ${w}px)`,bottom:`${p}px ${-w}px`,left:`calc(100% + ${w}px) ${h}px`,right:`${-w}px ${h}px`}[i],b=`${p}px ${o.reference.y+g-a}px`;return t.floating.style.setProperty("--transform-origin",et&&"y"===l&&v?b:y),{}}},A);let eo=P;!z&&P&&(eo={...P,elements:{reference:null,floating:null,domReference:null}});let ea=C.useMemo(()=>({elementResize:L&&"undefined"!=typeof ResizeObserver,layoutShift:L&&"undefined"!=typeof IntersectionObserver}),[L]),{refs:ei,elements:el,x:es,y:ec,middlewareData:eu,update:ed,placement:ef,context:ep,isPositioned:eh,floatingStyles:em}=function(e={}){let{nodeId:t}=e,r=oM({...e,elements:{reference:null,floating:null,...e.elements}}),n=e.rootContext||r,o=n.elements,[a,i]=C.useState(null),[l,s]=C.useState(null),c=o?.domReference||a,u=C.useRef(null),d=C.useContext(oP);oL(()=>{c&&(u.current=c)},[c]);let f=function(e){void 0===e&&(e={});let{placement:t="bottom",strategy:r="absolute",middleware:n=[],platform:o,elements:{reference:a,floating:i}={},transform:l=!0,whileElementsMounted:s,open:c}=e,[u,d]=C.useState({x:0,y:0,strategy:r,placement:t,middlewareData:{},isPositioned:!1}),[f,p]=C.useState(n);sS(f,n)||p(n);let[h,m]=C.useState(null),[g,v]=C.useState(null),y=C.useCallback(e=>{e!==w.current&&(w.current=e,m(e))},[]),b=C.useCallback(e=>{e!==k.current&&(k.current=e,v(e))},[]),x=a||h,_=i||g,w=C.useRef(null),k=C.useRef(null),j=C.useRef(u),S=null!=s,E=sT(s),T=sT(o),N=sT(c),L=C.useCallback(()=>{var e,n,o;let a,i,l;if(!w.current||!k.current)return;let s={placement:t,strategy:r,middleware:f};T.current&&(s.platform=T.current),(e=w.current,n=k.current,o=s,a=new Map,l={...(i={platform:sx,...o}).platform,_c:a},se(e,n,{...i,platform:l})).then(e=>{let t={...e,isPositioned:!1!==N.current};I.current&&!sS(j.current,t)&&(j.current=t,ej.flushSync(()=>{d(t)}))})},[f,t,r,T,N]);sj(()=>{!1===c&&j.current.isPositioned&&(j.current.isPositioned=!1,d(e=>({...e,isPositioned:!1})))},[c]);let I=C.useRef(!1);sj(()=>(I.current=!0,()=>{I.current=!1}),[]),sj(()=>{if(x&&(w.current=x),_&&(k.current=_),x&&_){if(E.current)return E.current(x,_,L);L()}},[x,_,L,E,S]);let P=C.useMemo(()=>({reference:w,floating:k,setReference:y,setFloating:b}),[y,b]),z=C.useMemo(()=>({reference:x,floating:_}),[x,_]),R=C.useMemo(()=>{let e={position:r,left:0,top:0};if(!z.floating)return e;let t=sE(z.floating,u.x),n=sE(z.floating,u.y);return l?{...e,transform:"translate("+t+"px, "+n+"px)",...sC(z.floating)>=1.5&&{willChange:"transform"}}:{position:r,left:t,top:n}},[r,l,z.floating,u.x,u.y]);return C.useMemo(()=>({...u,update:L,refs:P,elements:z,floatingStyles:R}),[u,L,P,z,R])}({...e,elements:{...o,...l&&{reference:l}}}),p=C.useCallback(e=>{let t=o$(e)?{getBoundingClientRect:()=>e.getBoundingClientRect(),getClientRects:()=>e.getClientRects(),contextElement:e}:e;s(t),f.refs.setReference(t)},[f.refs]),h=C.useCallback(e=>{(o$(e)||null===e)&&(u.current=e,i(e)),(o$(f.refs.reference.current)||null===f.refs.reference.current||null!==e&&!o$(e))&&f.refs.setReference(e)},[f.refs]),m=C.useMemo(()=>({...f.refs,setReference:h,setPositionReference:p,domReference:u}),[f.refs,h,p]),g=C.useMemo(()=>({...f.elements,domReference:c}),[f.elements,c]),v=C.useMemo(()=>({...f,...n,refs:m,elements:g,nodeId:t}),[f,m,g,t,n]);return oL(()=>{n.dataRef.current.floatingContext=v;let e=d?.nodesRef.current.find(e=>e.id===t);e&&(e.context=v)}),C.useMemo(()=>({...f,context:v,refs:m,elements:g}),[f,m,g,v])}({rootContext:eo,placement:W,middleware:J,strategy:x,whileElementsMounted:I?void 0:(...e)=>sw(...e,ea),nodeId:M}),{sideX:eg,sideY:ev}=eu.adaptiveOrigin||{},ey=C.useMemo(()=>A?{position:x,[eg]:`${es}px`,[ev]:`${ec}px`}:em,[A,eg,ev,x,es,ec,em]),eb=C.useRef(null);oL(()=>{if(!z)return;let e=V.current,t="function"==typeof e?e():e,r=(sP(t)?t.current:t)||null;r!==eb.current&&(ei.setPositionReference(r),eb.current=r)},[z,ei,H,V]),C.useEffect(()=>{if(!z)return;let e=V.current;"function"!=typeof e&&sP(e)&&e.current!==eb.current&&(ei.setPositionReference(e.current),eb.current=e.current)},[z,ei,H,V]),C.useEffect(()=>{if(I&&z&&el.domReference&&el.floating)return sw(el.domReference,el.floating,ed,ea)},[I,z,el,ed,ea]);let ex=sN(_,a9(ef),B),e_=a8(ef)||"center",ew=!!eu.hide?.referenceHidden,ek=C.useMemo(()=>({position:"absolute",top:eu.arrow?.y,left:eu.arrow?.x}),[eu.arrow]),eS=eu.arrow?.centerOffset!==0;return C.useMemo(()=>({positionerStyles:ey,arrowStyles:ek,arrowRef:Y,arrowUncentered:eS,side:ex,align:e_,anchorHidden:ew,refs:ei,context:ep,isPositioned:eh,update:ed}),[ey,ek,Y,eS,ex,e_,ew,ei,ep,eh,ed])}function sP(e){return null!=e&&"current"in e}function sz(e){let{children:t,elementsRef:r,labelsRef:n,onMapChange:o}=e,a=C.useRef(0),i=oh(sO).current,l=oh(sR).current,[s,c]=C.useState(0),u=C.useRef(s),d=o_((e,t)=>{l.set(e,t??null),u.current+=1,c(u.current)}),f=o_(e=>{l.delete(e),u.current+=1,c(u.current)}),p=C.useMemo(()=>{let e=new Map;return Array.from(l.keys()).sort(sM).forEach((t,r)=>{let n=l.get(t)??{};e.set(t,{...n,index:r})}),e},[l,s]);oL(()=>{u.current===s&&(r.current.length!==p.size&&(r.current.length=p.size),n&&n.current.length!==p.size&&(n.current.length=p.size)),o?.(p)},[o,p,r,n,s,u]);let h=o_(e=>(i.add(e),()=>{i.delete(e)}));oL(()=>{i.forEach(e=>e(p))},[i,p]);let m=C.useMemo(()=>({register:d,unregister:f,subscribeMapChange:h,elementsRef:r,labelsRef:n,nextIndexRef:a}),[d,f,h,r,n,a]);return(0,j.jsx)(lm.Provider,{value:m,children:t})}function sR(){return new Map}function sO(){return new Set}function sM(e,t){let r=e.compareDocumentPosition(t);return r&Node.DOCUMENT_POSITION_FOLLOWING||r&Node.DOCUMENT_POSITION_CONTAINED_BY?-1:r&Node.DOCUMENT_POSITION_PRECEDING||r&Node.DOCUMENT_POSITION_CONTAINS?1:0}let sA=C.forwardRef(function(e,t){let r,{cutout:n,...o}=e;if(n){let e=n?.getBoundingClientRect();r=`polygon(
      0% 0%,
      100% 0%,
      100% 100%,
      0% 100%,
      0% 0%,
      ${e.left}px ${e.top}px,
      ${e.left}px ${e.bottom}px,
      ${e.right}px ${e.bottom}px,
      ${e.right}px ${e.top}px,
      ${e.left}px ${e.top}px
    )`}return(0,j.jsx)("div",{ref:t,role:"presentation","data-base-ui-inert":"",...o,style:{position:"fixed",inset:0,userSelect:"none",WebkitUserSelect:"none",clipPath:r}})}),sD=C.forwardRef(function(e,t){var r;let n,o,a,i,{anchor:l,positionMethod:s="absolute",className:c,render:u,side:d,align:f,sideOffset:p=0,alignOffset:h=0,collisionBoundary:m="clipping-ancestors",collisionPadding:g=5,arrowPadding:v=5,sticky:y=!1,trackAnchor:b=!0,collisionAvoidance:x=aq,..._}=e,{open:w,setOpen:k,floatingRootContext:S,setPositionerElement:E,itemDomElements:T,itemLabels:N,mounted:L,modal:I,lastOpenChangeReason:P,parent:z,setHoverEnabled:R,triggerElement:O}=iT(),M=function(){let e=C.useContext(l6);if(void 0===e)throw Error("Base UI: <Menu.Portal> is missing.");return e}(),A=(n=oT(),o=C.useContext(oP),i=a=oz(),oL(()=>{if(!n)return;let e={id:n,parentId:i};return o?.addNode(e),()=>{o?.removeNode(e)}},[o,n,i]),n),D=oz(),Z=iH(!0),F=l,U=p,$=h,H=f;"context-menu"===z.type&&(F=z.context?.anchor??l,H=e.align??"start",$=e.alignOffset??2,U=e.sideOffset??-5);let V=d,B=H;"menu"===z.type?(V=V??"inline-end",B=B??"start"):"menubar"===z.type&&(V=V??"bottom",B=B??"start");let q="context-menu"===z.type,W=sI({anchor:F,floatingRootContext:S,positionMethod:Z?"fixed":s,mounted:L,side:V,sideOffset:U,align:B,alignOffset:$,arrowPadding:q?0:v,collisionBoundary:m,collisionPadding:g,sticky:y,nodeId:A,keepMounted:M,trackAnchor:b,collisionAvoidance:x,shiftCrossAxis:q}),{events:K}=C.useContext(oP),Y=C.useMemo(()=>{let e={};return w||(e.pointerEvents="none"),{role:"presentation",hidden:!L,style:{...W.positionerStyles,...e}}},[w,L,W.positionerStyles]);C.useEffect(()=>{function e(e){e.open?(e.parentNodeId===A&&R(!1),e.nodeId!==A&&e.parentNodeId===D&&k(!1,void 0,"sibling-open")):e.parentNodeId===A&&R(!0)}return K.on("openchange",e),()=>{K.off("openchange",e)}},[K,A,D,k,R]),C.useEffect(()=>{K.emit("openchange",{open:w,nodeId:A,parentNodeId:D})},[K,w,A,D]);let X=C.useMemo(()=>({open:w,side:W.side,align:W.align,anchorHidden:W.anchorHidden,nested:"menu"===z.type}),[w,W.side,W.align,W.anchorHidden,z.type]),G=C.useMemo(()=>({side:W.side,align:W.align,arrowRef:W.arrowRef,arrowUncentered:W.arrowUncentered,arrowStyles:W.arrowStyles,floatingContext:W.context}),[W.side,W.align,W.arrowRef,W.arrowUncentered,W.arrowStyles,W.context]),Q=lu("div",e,{state:X,customStyleHookMapping:ls,ref:[t,E],props:{...Y,..._}}),J=L&&"menu"!==z.type&&("menubar"!==z.type&&I&&"trigger-hover"!==P||"menubar"===z.type&&z.context.modal),ee=null;return"menubar"===z.type?ee=z.context.contentElement:void 0===z.type&&(ee=O),(0,j.jsxs)(l8.Provider,{value:G,children:[J&&(0,j.jsx)(sA,{ref:"context-menu"===z.type||"nested-context-menu"===z.type?z.context.internalBackdropRef:null,inert:(r=!w,lc>=19?r:r?"true":void 0),cutout:ee}),(0,j.jsx)(oR,{id:A,children:(0,j.jsx)(sz,{elementsRef:T,labelsRef:N,children:Q})})]})}),sZ={inert:new WeakMap,"aria-hidden":new WeakMap,none:new WeakMap};function sF(e){return"inert"===e?sZ.inert:"aria-hidden"===e?sZ["aria-hidden"]:sZ.none}let sU=new WeakSet,s$={},sH=0,sV=e=>e&&(e.host||sV(e.parentNode)),sB=[];function sq(){sB=sB.filter(e=>e.isConnected)}function sW(){return sq(),sB[sB.length-1]}function sK(e,t){if(!t.current.includes("floating")&&!e.getAttribute("role")?.includes("dialog"))return;let r=lY(),n=lW(e,r).filter(e=>{let t=e.getAttribute("data-tabindex")||"";return lK(e,r)||e.hasAttribute("data-tabindex")&&!t.startsWith("-")}),o=e.getAttribute("tabindex");t.current.includes("floating")||0===n.length?"0"!==o&&e.setAttribute("tabindex","0"):("-1"!==o||e.hasAttribute("data-tabindex")&&"-1"!==e.getAttribute("data-tabindex"))&&(e.setAttribute("tabindex","-1"),e.setAttribute("data-tabindex","-1"))}function sY(e){let{context:t,children:r,disabled:n=!1,order:o=["content"],initialFocus:a=0,returnFocus:i=!0,restoreFocus:l=!1,modal:s=!0,closeOnFocusOut:c=!0,getInsideElements:u=()=>[]}=e,{open:d,onOpenChange:f,events:p,dataRef:h,elements:{domReference:m,floating:g}}=t,v=o_(()=>h.current.floatingContext?.nodeId),y=o_(u),b="number"==typeof a&&a<0,x=aE(m)&&b,_=o8(o),w=o8(a),k=o8(i),S=C.useContext(oP),E=C.useContext(l2),T=C.useRef(null),N=C.useRef(null),L=C.useRef(!1),I=C.useRef(!1),P=C.useRef(-1),z=oy(),R=null!=E,O=aT(g),M=o_((e=O)=>e?lq(e,lY()):[]),A=o_(e=>{let t=M(e);return _.current.map(()=>t).filter(Boolean).flat()});C.useEffect(()=>{if(n||!s)return;function e(e){"Tab"===e.key&&aw(O,a_(aS(O)))&&0===M().length&&!x&&au(e)}let t=aS(O);return t.addEventListener("keydown",e),()=>{t.removeEventListener("keydown",e)}},[n,m,O,s,_,x,M,A]),C.useEffect(()=>{if(!n&&g)return g.addEventListener("focusin",e),()=>{g.removeEventListener("focusin",e)};function e(e){let t=ak(e),r=M().indexOf(t);-1!==r&&(P.current=r)}},[n,g,M]),C.useEffect(()=>{if(n||!c)return;function e(){I.current=!0}function t(e){let t=e.relatedTarget,r=e.currentTarget,n=ak(e);queueMicrotask(()=>{let o=v(),a=!(aw(m,t)||aw(g,t)||aw(t,g)||aw(E?.portalNode,t)||t?.hasAttribute(aN("focus-guard"))||S&&(aR(S.nodesRef.current,o).find(e=>aw(e.context?.elements.floating,t)||aw(e.context?.elements.domReference,t))||aO(S.nodesRef.current,o).find(e=>[e.context?.elements.floating,aT(e.context?.elements.floating)].includes(t)||e.context?.elements.domReference===t)));if(r===m&&O&&sK(O,_),l&&r!==m&&!n?.isConnected&&a_(aS(O))===aS(O).body){oH(O)&&O.focus();let e=P.current,t=M(),r=t[e]||t[t.length-1]||O;oH(r)&&r.focus()}if(h.current.insideReactTree){h.current.insideReactTree=!1;return}if(I.current){I.current=!1;return}(x||!s)&&t&&a&&t!==sW()&&(L.current=!0,f(!1,e,"focus-out"))})}let r=!!(!S&&E);function o(){h.current.insideReactTree=!0,z.start(0,()=>{h.current.insideReactTree=!1})}if(g&&oH(m))return m.addEventListener("focusout",t),m.addEventListener("pointerdown",e),g.addEventListener("focusout",t),r&&g.addEventListener("focusout",o,!0),()=>{m.removeEventListener("focusout",t),m.removeEventListener("pointerdown",e),g.removeEventListener("focusout",t),r&&g.removeEventListener("focusout",o,!0)}},[n,m,g,O,s,S,E,f,c,l,M,x,v,_,h,z]);let D=C.useRef(null),Z=C.useRef(null),F=i2(D,E?.beforeInsideRef),U=i2(Z,E?.afterInsideRef);C.useEffect(()=>{if(n||!g)return;let e=Array.from(E?.portalNode?.querySelectorAll(`[${aN("portal")}]`)||[]),t=S?aO(S.nodesRef.current,v()):[],r=function(e,t=!1,r=!1){var n,o,a;let i,l,s,c,u,d,f,p,h=aS(e[0]).body;return n=e.concat(Array.from(h.querySelectorAll("[aria-live]"))),o=h,a=t,i="data-base-ui-inert",l=r?"inert":a?"aria-hidden":null,s=o,c=n.map(e=>{if(s.contains(e))return e;let t=sV(e);return s.contains(t)?t:null}).filter(e=>null!=e),u=new Set,d=new Set(c),f=[],s$[i]||(s$[i]=new WeakMap),p=s$[i],c.forEach(function e(t){!(!t||u.has(t))&&(u.add(t),t.parentNode&&e(t.parentNode))}),function e(t){!t||d.has(t)||[].forEach.call(t.children,t=>{if("script"!==oD(t))if(u.has(t))e(t);else{let e=l?t.getAttribute(l):null,r=null!==e&&"false"!==e,n=sF(l),o=(n.get(t)||0)+1,a=(p.get(t)||0)+1;n.set(t,o),p.set(t,a),f.push(t),1===o&&r&&sU.add(t),1===a&&t.setAttribute(i,""),!r&&l&&t.setAttribute(l,"inert"===l?"":"true")}})}(o),u.clear(),sH+=1,()=>{f.forEach(e=>{let t=sF(l),r=(t.get(e)||0)-1,n=(p.get(e)||0)-1;t.set(e,r),p.set(e,n),r||(!sU.has(e)&&l&&e.removeAttribute(l),sU.delete(e)),n||e.removeAttribute(i)}),(sH-=1)||(sZ.inert=new WeakMap,sZ["aria-hidden"]=new WeakMap,sZ.none=new WeakMap,sU=new WeakSet,s$={})}}([g,t.find(e=>aE(e.context?.elements.domReference||null))?.context?.elements.domReference,...e,...y(),T.current,N.current,D.current,Z.current,E?.beforeOutsideRef.current,E?.afterOutsideRef.current,x?m:null].filter(e=>null!=e),s||x);return()=>{r()}},[n,m,g,s,_,E,x,S,v,y]),oL(()=>{if(n||!oH(O))return;let e=a_(aS(O));queueMicrotask(()=>{let t=A(O),r=w.current,n=("number"==typeof r?t[r]:r.current)||O,o=aw(O,e);b||o||!d||ix(n,{preventScroll:n===O})})},[n,d,O,b,A,w]),oL(()=>{var e;if(n||!O)return;let t=aS(O);function r({reason:e,event:t,nested:r}){if(["hover","safe-polygon"].includes(e)&&"mouseleave"===t.type&&(L.current=!0),"outside-press"===e)if(r)L.current=!1;else if(ad(t)||af(t))L.current=!1;else{let e=!1;document.createElement("div").focus({get preventScroll(){return e=!0,!1}}),e?L.current=!1:L.current=!0}}e=a_(t),sq(),e&&"body"!==oD(e)&&(sB.push(e),sB.length>20&&(sB=sB.slice(-20))),p.on("openchange",r);let o=t.createElement("span");return o.setAttribute("tabindex","-1"),o.setAttribute("aria-hidden","true"),Object.assign(o.style,lx),R&&m&&m.insertAdjacentElement("afterend",o),()=>{p.off("openchange",r);let e=a_(t),n=aw(g,e)||S&&aR(S.nodesRef.current,v(),!1).some(t=>aw(t.context?.elements.floating,e)),a=function(){if("boolean"==typeof k.current){let e=m||sW();return e&&e.isConnected?e:o}return k.current.current||o}();queueMicrotask(()=>{var r;let i,l=(r=a,i=lY(),lK(r,i)?r:lq(r,i)[0]||r);k.current&&!L.current&&oH(l)&&(l===e||e===t.body||n)&&l.focus({preventScroll:!0}),o.remove()})}},[n,g,O,k,h,p,S,R,m,v]),C.useEffect(()=>{queueMicrotask(()=>{L.current=!1})},[n]),C.useEffect(()=>{if(n||!d)return;function e(e){let t=ak(e);t?.closest("[data-base-ui-click-trigger]")&&(I.current=!0)}let t=aS(O);return t.addEventListener("pointerdown",e,!0),()=>{t.removeEventListener("pointerdown",e,!0)}},[n,d,O]),oL(()=>{if(!n&&E)return E.setFocusManagerState({modal:s,closeOnFocusOut:c,open:d,onOpenChange:f,domReference:m}),()=>{E.setFocusManagerState(null)}},[n,E,s,d,f,c,m]),oL(()=>{if(!n&&O)return sK(O,_),()=>{queueMicrotask(sq)}},[n,O,_]);let $=!n&&(!s||!x)&&(R||s);return(0,j.jsxs)(C.Fragment,{children:[$&&(0,j.jsx)(l_,{"data-type":"inside",ref:F,onFocus:e=>{if(s){let e=A();ix(e[e.length-1])}else if(E?.preserveTabOrder&&E.portalNode)if(L.current=!1,lJ(e,E.portalNode)){let e=lG(m);e?.focus()}else E.beforeOutsideRef.current?.focus()}}),r,$&&(0,j.jsx)(l_,{"data-type":"inside",ref:U,onFocus:e=>{if(s)ix(A()[0]);else if(E?.preserveTabOrder&&E.portalNode)if(c&&(L.current=!0),lJ(e,E.portalNode)){let e=lQ(m);e?.focus()}else E.afterOutsideRef.current?.focus()}})]})}let sX={...ls,...i8},sG=C.forwardRef(function(e,t){let{render:r,className:n,finalFocus:o,...a}=e,{open:i,setOpen:l,popupRef:s,transitionStatus:c,popupProps:u,mounted:d,instantType:f,onOpenChangeComplete:p,parent:h,lastOpenChangeReason:m,rootId:g}=iT(),{side:v,align:y,floatingContext:b}=function(){let e=C.useContext(l8);if(void 0===e)throw Error("Base UI: MenuPositionerContext is missing. MenuPositioner parts must be placed within <Menu.Positioner>.");return e}();iI({open:i,ref:s,onComplete(){i&&p?.(!0)}});let{events:x}=C.useContext(oP);C.useEffect(()=>{function e(e){l(!1,e.domEvent,e.reason)}return x.on("close",e),()=>{x.off("close",e)}},[x,l]);let _=lu("div",e,{state:C.useMemo(()=>({transitionStatus:c,side:v,align:y,open:i,nested:"menu"===h.type,instant:f}),[c,v,y,i,h.type,f]),ref:[t,s],customStyleHookMapping:sX,props:[u,"starting"===c?aH:aV,a,{"data-rootownerid":g}]}),w=void 0===h.type||"context-menu"===h.type;return"menubar"===h.type&&"outside-press"!==m&&(w=!0),(0,j.jsx)(sY,{context:b,modal:!1,disabled:!d,returnFocus:o||w,initialFocus:"menu"===h.type?-1:0,restoreFocus:!0,children:_})}),sQ=C.createContext(void 0),sJ=C.forwardRef(function(e,t){let{render:r,className:n,...o}=e,[a,i]=C.useState(void 0),l=C.useMemo(()=>({setLabelId:i}),[i]),s=lu("div",e,{ref:t,props:{role:"group","aria-labelledby":a,...o}});return(0,j.jsx)(sQ.Provider,{value:l,children:s})});function s0(e){return oT(e,"base-ui")}let s1=C.forwardRef(function(e,t){let{className:r,render:n,id:o,...a}=e,i=s0(o),{setLabelId:l}=function(){let e=C.useContext(sQ);if(void 0===e)throw Error("Base UI: MenuGroupRootContext is missing. Menu group parts must be used within <Menu.Group>.");return e}();return oL(()=>(l(i),()=>{l(void 0)}),[l,i]),lu("div",e,{ref:t,props:{id:i,role:"presentation",...a}})}),s2={type:"regular-item"},s3=C.memo(C.forwardRef(function(e,t){let{className:r,closeOnClick:n=!0,disabled:o=!1,highlighted:a,id:i,menuEvents:l,itemProps:s,render:c,allowMouseUpTriggerRef:u,typingRef:d,nativeButton:f,...p}=e,{getItemProps:h,itemRef:m}=function(e){let{closeOnClick:t,disabled:r=!1,highlighted:n,id:o,menuEvents:a,allowMouseUpTriggerRef:i,typingRef:l,nativeButton:s,itemMetadata:c}=e,u=C.useRef(null),{getButtonProps:d,buttonRef:f}=lh({disabled:r,focusableWhenDisabled:!0,native:s}),p=C.useCallback(e=>iW({id:o,role:"menuitem",tabIndex:n?0:-1,onMouseEnter(){"submenu-trigger"===c.type&&c.setActive()},onKeyUp:e=>{" "===e.key&&l.current&&e.preventBaseUIHandler()},onClick:e=>{t&&a.emit("close",{domEvent:e,reason:"item-press"})},onMouseUp:()=>{u.current&&i.current&&"regular-item"===c.type&&u.current.click()}},e,d),[o,n,d,l,t,a,i,c]),h=i2(u,f);return C.useMemo(()=>({getItemProps:p,itemRef:h}),[p,h])}({closeOnClick:n,disabled:o,highlighted:a,id:i,menuEvents:l,allowMouseUpTriggerRef:u,typingRef:d,nativeButton:f,itemMetadata:s2});return lu("div",e,{state:C.useMemo(()=>({disabled:o,highlighted:a}),[o,a]),ref:[m,t],props:[s,p,h]})})),s4=C.forwardRef(function(e,t){let{id:r,label:n,nativeButton:o=!1,...a}=e,i=C.useRef(null),l=lv({label:n}),s=i2(t,l.ref,i),{itemProps:c,activeIndex:u,allowMouseUpTriggerRef:d,typingRef:f}=iT(),p=s0(r),h=l.index===u,{events:m}=C.useContext(oP);return(0,j.jsx)(s3,{...a,id:p,ref:s,highlighted:h,menuEvents:m,itemProps:c,allowMouseUpTriggerRef:d,typingRef:f,nativeButton:o})}),s5="__next_builtin__";function s6(e){return e.replace(RegExp(`^${s5}`),"").replace(RegExp("@boundary$"),"")}let s9="boundary:";function s8(e){return e.startsWith(s9)}function s7(e){return e.replace(s9,"")}function ce({nodeState:e,boundaries:t}){let{pagePath:r,boundaryType:n,setBoundaryType:o}=e,[a,i]=(0,C.useState)(!1),{shadowRoot:l}=us(),s=(0,C.useRef)(null),c=(0,C.useRef)(null);t5(c,s,a,()=>{i(!1)},s.current?.ownerDocument);let u=(Object.values(t).find(e=>null!==e)||"").split(".").pop()||"js",d=(0,C.useMemo)(()=>Object.fromEntries(Object.entries(t).map(([e,t])=>{let r=s6((t||"").split("/").pop()||`${e}.${u}`);return[e,r]})),[t,u]),f=(r||"").split("/").pop()||"",p=s6(n?`page.${u}`:f||`page.${u}`),h=[{label:d.loading,value:"loading",icon:(0,j.jsx)(ct,{}),disabled:!t.loading},{label:d.error,value:"error",icon:(0,j.jsx)(cr,{}),disabled:!t.error},{label:d["not-found"],value:"not-found",icon:(0,j.jsx)(cn,{}),disabled:!t["not-found"]}],m={label:n?"Reset":p,value:"reset",icon:(0,j.jsx)(co,{}),disabled:null===n},g=(0,C.useCallback)(({filePath:e})=>{let t=new URLSearchParams({file:e,isAppRelativePath:"1"});fetch(`${process.env.__NEXT_ROUTER_BASEPATH||""}/__nextjs_launch-editor?${t.toString()}`).catch(console.warn)},[]),v=(0,C.useCallback)(e=>{switch(e){case"not-found":case"loading":case"error":o(e);break;case"reset":o(null);break;case"open-editor":r&&g({filePath:r})}},[o,r,g]),y=(0,C.useMemo)(()=>"layout"!==e.type&&"template"!==e.type&&Object.values(t).some(e=>null!==e),[e.type,t]);return(0,j.jsxs)(i1,{delay:0,modal:!1,open:a,onOpenChange:i,children:[(0,j.jsx)(lb,{className:"segment-boundary-trigger","data-nextjs-dev-overlay-segment-boundary-trigger-button":!0,render:e=>{let t=((...e)=>t=>{e.forEach(e=>{"function"==typeof e?e(t):e&&(e.current=t)})})(e.ref,s);return(0,j.jsx)(ci,{...e,ref:t})},disabled:!y}),(0,j.jsx)(l9,{container:l,children:(0,j.jsx)(sD,{className:"segment-boundary-dropdown-positioner",side:"bottom",align:"center",sideOffset:6,arrowPadding:8,ref:c,children:(0,j.jsxs)(sG,{className:"segment-boundary-dropdown",children:[(0,j.jsxs)(sJ,{children:[(0,j.jsx)(s1,{className:"segment-boundary-group-label",children:"Toggle Overrides"}),h.map(e=>(0,j.jsxs)(s4,{className:"segment-boundary-dropdown-item",onClick:()=>v(e.value),disabled:e.disabled,children:[e.icon,e.label]},e.value))]}),(0,j.jsx)(sJ,{children:(0,j.jsxs)(s4,{className:"segment-boundary-dropdown-item",onClick:()=>v(m.value),disabled:m.disabled,children:[m.icon,m.label]},m.value)})]})})})]})}function ct(){let e,t,r=(0,S.c)(2);return r[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("g",{clipPath:"url(#clip0_2759_1866)",children:(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M10 3.5C13.5899 3.5 16.5 6.41015 16.5 10C16.5 13.5899 13.5899 16.5 10 16.5C6.41015 16.5 3.5 13.5899 3.5 10C3.5 6.41015 6.41015 3.5 10 3.5ZM2 10C2 14.4183 5.58172 18 10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10ZM10.75 9.62402V6H9.25V9.875C9.25 10.1898 9.39858 10.486 9.65039 10.6748L11.5498 12.0996L12.1504 12.5498L13.0498 11.3496L12.4502 10.9004L10.75 9.62402Z",fill:"currentColor"})}),r[0]=e):e=r[0],r[1]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsxs)("svg",{width:"20px",height:"20px",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e,(0,j.jsx)("defs",{children:(0,j.jsx)("clipPath",{id:"clip0_2759_1866",children:(0,j.jsx)("rect",{width:"16",height:"16",fill:"white",transform:"translate(2 2)"})})})]}),r[1]=t):t=r[1],t}function cr(){let e,t,r=(0,S.c)(2);return r[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("g",{clipPath:"url(#clip0_2759_1881)",children:(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M3.5 7.30762V12.6924L7.30762 16.5H12.6924L16.5 12.6924V7.30762L12.6924 3.5H7.30762L3.5 7.30762ZM18 12.8994L17.9951 12.998C17.9724 13.2271 17.8712 13.4423 17.707 13.6064L13.6064 17.707L13.5332 17.7734C13.3806 17.8985 13.1944 17.9757 12.998 17.9951L12.8994 18H7.10059L7.00195 17.9951C6.80562 17.9757 6.6194 17.8985 6.4668 17.7734L6.39355 17.707L2.29297 13.6064C2.12883 13.4423 2.02756 13.2271 2.00488 12.998L2 12.8994V7.10059C2 6.83539 2.10546 6.58109 2.29297 6.39355L6.39355 2.29297C6.55771 2.12883 6.77294 2.02756 7.00195 2.00488L7.10059 2H12.8994L12.998 2.00488C13.2271 2.02756 13.4423 2.12883 13.6064 2.29297L17.707 6.39355C17.8945 6.58109 18 6.83539 18 7.10059V12.8994ZM9.25 5.75H10.75L10.75 10.75H9.25L9.25 5.75ZM10 14C10.5523 14 11 13.5523 11 13C11 12.4477 10.5523 12 10 12C9.44772 12 9 12.4477 9 13C9 13.5523 9.44772 14 10 14Z",fill:"currentColor"})}),r[0]=e):e=r[0],r[1]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsxs)("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e,(0,j.jsx)("defs",{children:(0,j.jsx)("clipPath",{id:"clip0_2759_1881",children:(0,j.jsx)("rect",{width:"16",height:"16",fill:"white",transform:"translate(2 2)"})})})]}),r[1]=t):t=r[1],t}function cn(){let e,t=(0,S.c)(1);return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("svg",{width:"20px",height:"20px",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M10.5586 2.5C11.1341 2.50004 11.6588 2.8294 11.9091 3.34766L17.8076 15.5654C18.1278 16.2292 17.6442 16.9997 16.9072 17H3.09274C2.35574 16.9997 1.8721 16.2292 2.19235 15.5654L8.09079 3.34766C8.34109 2.8294 8.86583 2.50004 9.44137 2.5H10.5586ZM3.89059 15.5H16.1093L10.5586 4H9.44137L3.89059 15.5ZM9.24997 6.75H10.75L10.75 10.75H9.24997L9.24997 6.75ZM9.99997 14C10.5523 14 11 13.5523 11 13C11 12.4477 10.5523 12 9.99997 12C9.44768 12 8.99997 12.4477 8.99997 13C8.99997 13.5523 9.44768 14 9.99997 14Z",fill:"currentColor"})}),t[0]=e):e=t[0],e}function co(){let e,t=(0,S.c)(1);return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:(0,j.jsx)("path",{d:"M9.96484 3C13.8463 3.00018 17 6.13012 17 10C17 13.8699 13.8463 16.9998 9.96484 17C7.62404 17 5.54877 15.8617 4.27051 14.1123L3.82812 13.5068L5.03906 12.6221L5.48145 13.2275C6.48815 14.6053 8.12092 15.5 9.96484 15.5C13.0259 15.4998 15.5 13.0335 15.5 10C15.5 6.96654 13.0259 4.50018 9.96484 4.5C7.42905 4.5 5.29544 6.19429 4.63867 8.5H8V10H2.75C2.33579 10 2 9.66421 2 9.25V4H3.5V7.2373C4.57781 4.74376 7.06749 3 9.96484 3Z",fill:"currentColor"})}),t[0]=e):e=t[0],e}function ca(e){let t,r,n=(0,S.c)(3);return n[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M8.7071 2.39644C8.31658 2.00592 7.68341 2.00592 7.29289 2.39644L4.46966 5.21966L3.93933 5.74999L4.99999 6.81065L5.53032 6.28032L7.99999 3.81065L10.4697 6.28032L11 6.81065L12.0607 5.74999L11.5303 5.21966L8.7071 2.39644ZM5.53032 9.71966L4.99999 9.18933L3.93933 10.25L4.46966 10.7803L7.29289 13.6035C7.68341 13.9941 8.31658 13.9941 8.7071 13.6035L11.5303 10.7803L12.0607 10.25L11 9.18933L10.4697 9.71966L7.99999 12.1893L5.53032 9.71966Z",fill:"currentColor"}),n[0]=t):t=n[0],n[1]!==e?(r=(0,j.jsx)("svg",{strokeLinejoin:"round",viewBox:"0 0 16 16",...e,children:t}),n[1]=e,n[2]=r):r=n[2],r}function ci(e){let t,r,n=(0,S.c)(3);return n[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("span",{className:"segment-boundary-trigger-text",children:(0,j.jsx)(ca,{className:"plus-icon"})}),n[0]=t):t=n[0],n[1]!==e?(r=(0,j.jsx)("button",{...e,children:t}),n[1]=e,n[2]=r):r=n[2],r}let cl=C.createContext(void 0);function cs(){let e=C.useContext(cl);if(void 0===e)throw Error("Base UI: TooltipRootContext is missing. Tooltip parts must be placed within <Tooltip.Root>.");return e}let cc=C.forwardRef(function(e,t){let{className:r,render:n,...o}=e,{open:a,setTriggerElement:i,triggerProps:l}=cs();return lu("button",e,{state:C.useMemo(()=>({open:a}),[a]),ref:[t,i],props:[l,o],customStyleHookMapping:li})}),cu=C.createContext(void 0);function cd(){let e=C.useContext(cu);if(void 0===e)throw Error("Base UI: TooltipPositionerContext is missing. TooltipPositioner parts must be placed within <Tooltip.Positioner>.");return e}let cf=C.forwardRef(function(e,t){let{className:r,render:n,...o}=e,{open:a,arrowRef:i,side:l,align:s,arrowUncentered:c,arrowStyles:u}=cd();return lu("div",e,{state:C.useMemo(()=>({open:a,side:l,align:s,uncentered:c}),[a,l,s,c]),ref:[t,i],props:[{style:u,"aria-hidden":!0},o],customStyleHookMapping:ls})}),cp={...ls,...i8},ch=C.forwardRef(function(e,t){let{className:r,render:n,...o}=e,{open:a,instantType:i,transitionStatus:l,popupProps:s,popupRef:c,onOpenChangeComplete:u}=cs(),{side:d,align:f}=cd();return iI({open:a,ref:c,onComplete(){a&&u?.(!0)}}),lu("div",e,{state:C.useMemo(()=>({open:a,side:d,align:f,instant:i,transitionStatus:l}),[a,d,f,i,l]),ref:[t,c],props:[s,"starting"===l?aH:aV,o],customStyleHookMapping:cp})}),cm=C.createContext(void 0),cg=C.forwardRef(function(e,t){let{render:r,className:n,anchor:o,positionMethod:a="absolute",side:i="top",align:l="center",sideOffset:s=0,alignOffset:c=0,collisionBoundary:u="clipping-ancestors",collisionPadding:d=5,arrowPadding:f=5,sticky:p=!1,trackAnchor:h=!0,collisionAvoidance:m=aW,...g}=e,{open:v,setPositionerElement:y,mounted:b,floatingRootContext:x,trackCursorAxis:_,hoverable:w}=cs(),k=sI({anchor:o,positionMethod:a,floatingRootContext:x,mounted:b,side:i,sideOffset:s,align:l,alignOffset:c,collisionBoundary:u,collisionPadding:d,sticky:p,arrowPadding:f,trackAnchor:h,keepMounted:function(){let e=C.useContext(cm);if(void 0===e)throw Error("Base UI: <Tooltip.Portal> is missing.");return e}(),collisionAvoidance:m}),S=C.useMemo(()=>{let e={};return v&&"both"!==_&&w||(e.pointerEvents="none"),{role:"presentation",hidden:!b,style:{...k.positionerStyles,...e}}},[v,_,w,b,k.positionerStyles]),E=C.useMemo(()=>({props:S,...k}),[S,k]),T=C.useMemo(()=>({open:v,side:E.side,align:E.align,anchorHidden:E.anchorHidden}),[v,E.side,E.align,E.anchorHidden]),N=C.useMemo(()=>({...T,arrowRef:E.arrowRef,arrowStyles:E.arrowStyles,arrowUncentered:E.arrowUncentered}),[T,E.arrowRef,E.arrowStyles,E.arrowUncentered]),L=lu("div",e,{state:T,props:[E.props,g],ref:[t,y],customStyleHookMapping:ls});return(0,j.jsx)(cu.Provider,{value:N,children:L})});function cv(e){let t=l4({root:e.root});return t&&ej.createPortal(e.children,t)}function cy(e){let{children:t,keepMounted:r=!1,container:n}=e,{mounted:o}=cs();return o||r?(0,j.jsx)(cm.Provider,{value:r,children:(0,j.jsx)(cv,{root:n,children:t})}):null}let cb=C.createContext({hasProvider:!1,timeoutMs:0,delayRef:{current:0},initialDelayRef:{current:0},timeout:new ov,currentIdRef:{current:null},currentContextRef:{current:null}});function cx(e){let{children:t,delay:r,timeoutMs:n=0}=e,o=C.useRef(r),a=C.useRef(r),i=C.useRef(null),l=C.useRef(null),s=oy();return(0,j.jsx)(cb.Provider,{value:C.useMemo(()=>({hasProvider:!0,delayRef:o,initialDelayRef:a,currentIdRef:i,timeoutMs:n,currentContextRef:l,timeout:s}),[n,s]),children:t})}let c_=C.createContext(void 0),cw=function(e){let{delay:t,closeDelay:r,timeout:n=400}=e,o=C.useMemo(()=>({delay:t,closeDelay:r}),[t,r]),a=C.useMemo(()=>({open:t,close:r}),[t,r]);return(0,j.jsx)(c_.Provider,{value:o,children:(0,j.jsx)(cx,{delay:a,timeoutMs:n,children:e.children})})};function ck(e){return null!=e&&null!=e.clientX}function cj(e){let{disabled:t=!1,defaultOpen:r=!1,onOpenChange:n,open:o,delay:a,closeDelay:i,hoverable:l=!0,trackCursorAxis:s="none",actionsRef:c,onOpenChangeComplete:u}=e,d=a??600,f=i??0,[p,h]=C.useState(null),[m,g]=C.useState(null),[v,y]=C.useState(),b=C.useRef(null),[x,_]=oj({controlled:o,default:r,name:"Tooltip",state:"open"}),w=!t&&x;function k(e,t,r){let o="trigger-hover"===r,a=e&&"trigger-focus"===r,i=!e&&("trigger-press"===r||"escape-key"===r);function l(){n?.(e,t,r),_(e)}o?ej.flushSync(l):l(),a||i?y(a?"focus":"dismiss"):"trigger-hover"===r&&y(void 0)}let S=o_(k);x&&t&&k(!1,void 0,"disabled");let{mounted:E,setMounted:T,transitionStatus:N}=iL(w),L=o_(()=>{T(!1),u?.(!1)});iI({enabled:!c,open:w,ref:b,onComplete(){w||L()}}),C.useImperativeHandle(c,()=>({unmount:L}),[L]);let I=oM({elements:{reference:p,floating:m},open:w,onOpenChange(e,t,r){S(e,t,iU(r))}}),P=C.useContext(c_),{delayRef:z,isInstantPhase:R,hasProvider:O}=function(e,t={}){let{open:r,onOpenChange:n,floatingId:o}=e,{enabled:a=!0}=t,{currentIdRef:i,delayRef:l,timeoutMs:s,initialDelayRef:c,currentContextRef:u,hasProvider:d,timeout:f}=C.useContext(cb),[p,h]=C.useState(!1);return oL(()=>{function e(){h(!1),u.current?.setIsInstantPhase(!1),i.current=null,u.current=null,l.current=c.current}if(a&&i.current&&!r&&i.current===o){if(h(!1),s)return f.start(s,e),()=>{f.clear()};e()}},[a,r,o,i,l,s,c,u,f]),oL(()=>{if(!a||!r)return;let e=u.current,t=i.current;u.current={onOpenChange:n,setIsInstantPhase:h},i.current=o,l.current={open:0,close:aI(c.current,"close")},null!==t&&t!==o?(f.clear(),h(!0),e?.setIsInstantPhase(!0),e?.onOpenChange(!1)):(h(!1),e?.setIsInstantPhase(!1))},[a,r,o,n,i,l,s,c,u,f]),oL(()=>()=>{u.current=null},[u]),C.useMemo(()=>({hasProvider:d,delayRef:l,isInstantPhase:p}),[d,l,p])}(I),M=R?"delay":v,A=az(I,{enabled:!t,mouseOnly:!0,move:!1,handleClose:l&&"both"!==s?aA():null,restMs(){let e=P?.delay,t="object"==typeof z.current?z.current.open:void 0,r=d;return O&&(r=0!==t?a??e??d:0),r},delay(){let e="object"==typeof z.current?z.current.close:void 0,t=f;return null==i&&O&&(t=e),{close:t}}}),D=aZ(I,{enabled:!t}),Z=aX(I,{enabled:!t,referencePress:!0}),{getReferenceProps:F,getFloatingProps:U}=ij([A,D,Z,function(e,t={}){let{open:r,dataRef:n,elements:{floating:o,domReference:a},refs:i}=e,{enabled:l=!0,axis:s="both",x:c=null,y:u=null}=t,d=C.useRef(!1),f=C.useRef(null),[p,h]=C.useState(),[m,g]=C.useState([]),v=o_((e,t)=>{if(!d.current&&(!n.current.openEvent||ck(n.current.openEvent))){var r,o;let l,c,u;i.setPositionReference((r=a,o={x:e,y:t,axis:s,dataRef:n,pointerType:p},l=null,c=null,u=!1,{contextElement:r||void 0,getBoundingClientRect(){let e=r?.getBoundingClientRect()||{width:0,height:0,x:0,y:0},t="x"===o.axis||"both"===o.axis,n="y"===o.axis||"both"===o.axis,a=["mouseenter","mousemove"].includes(o.dataRef.current.openEvent?.type||"")&&"touch"!==o.pointerType,i=e.width,s=e.height,d=e.x,f=e.y;return null==l&&o.x&&t&&(l=e.x-o.x),null==c&&o.y&&n&&(c=e.y-o.y),d-=l||0,f-=c||0,i=0,s=0,!u||a?(i="y"===o.axis?e.width:0,s="x"===o.axis?e.height:0,d=t&&null!=o.x?o.x:d,f=n&&null!=o.y?o.y:f):u&&!a&&(s="x"===o.axis?e.height:s,i="y"===o.axis?e.width:i),u=!0,{width:i,height:s,x:d,y:f,top:f,right:d+i,bottom:f+s,left:d}}}))}}),y=o_(e=>{null==c&&null==u&&(r?f.current||g([]):v(e.clientX,e.clientY))}),b=ap(p)?o:r,x=C.useCallback(()=>{if(!b||!l||null!=c||null!=u)return;let e=oZ(o);function t(r){aw(o,ak(r))?(e.removeEventListener("mousemove",t),f.current=null):v(r.clientX,r.clientY)}if(!n.current.openEvent||ck(n.current.openEvent)){e.addEventListener("mousemove",t);let r=()=>{e.removeEventListener("mousemove",t),f.current=null};return f.current=r,r}i.setPositionReference(a)},[b,l,c,u,o,n,i,a,v]);C.useEffect(()=>x(),[x,m]),C.useEffect(()=>{l&&!o&&(d.current=!1)},[l,o]),C.useEffect(()=>{!l&&r&&(d.current=!0)},[l,r]),oL(()=>{l&&(null!=c||null!=u)&&(d.current=!1,v(c,u))},[l,c,u,v]);let _=C.useMemo(()=>{function e(e){h(e.pointerType)}return{onPointerDown:e,onPointerEnter:e,onMouseMove:y,onMouseEnter:y}},[y]);return C.useMemo(()=>l?{reference:_}:{},[l,_])}(I,{enabled:!t&&"none"!==s,axis:"none"===s?void 0:s})]),$=C.useMemo(()=>({open:w,setOpen:S,mounted:E,setMounted:T,setTriggerElement:h,positionerElement:m,setPositionerElement:g,popupRef:b,triggerProps:F(),popupProps:U(),floatingRootContext:I,instantType:M,transitionStatus:N,onOpenChangeComplete:u}),[w,S,E,T,h,m,g,b,F,U,I,M,N,u]),H=C.useMemo(()=>({...$,delay:d,closeDelay:f,trackCursorAxis:s,hoverable:l}),[$,d,f,s,l]);return(0,j.jsx)(cl.Provider,{value:H,children:e.children})}var cS=__webpack_require__("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/components/tooltip/tooltip.css"),cC={};cC.styleTagTransform=b(),cC.setAttributes=m(),cC.insert=p(),cC.domAPI=d(),cC.insertStyleElement=v(),c()(cS.A,cC),cS.A&&cS.A.locals&&cS.A.locals;let cE=(0,C.forwardRef)(function(e,t){let r,n,o,a,i,l,s,c,u,d,f,p,h=(0,S.c)(35),{className:m,children:g,title:v,direction:y,arrowSize:b,offset:x}=e,_=void 0===y?"top":y,w=void 0===b?6:b,{shadowRoot:k}=us();if(!v)return g;h[0]!==g?(r=e=>(0,j.jsx)("span",{...e,children:g}),h[0]=g,h[1]=r):r=h[1],h[2]!==t||h[3]!==r?(n=(0,j.jsx)(cc,{ref:t,render:r}),h[2]=t,h[3]=r,h[4]=n):n=h[4];let C=(void 0===x?8:x)+w,E=`${w}px`,T=`${w}px`;h[5]!==E||h[6]!==T?(o={"--anchor-width":E,"--anchor-height":T},h[5]=E,h[6]=T,h[7]=o):o=h[7];let N=o;h[8]!==m?(a=e6("tooltip",m),h[8]=m,h[9]=a):a=h[9];let L=`${w}px`;h[10]!==L?(i={"--arrow-size":L},h[10]=L,h[11]=i):i=h[11];let I=i,P=`tooltip-arrow--${_}`;h[12]!==P?(l=e6("tooltip-arrow",P),h[12]=P,h[13]=l):l=h[13];let z=`${w}px`;h[14]!==z?(s={"--arrow-size":z},h[14]=z,h[15]=s):s=h[15];let R=s;return h[16]!==l||h[17]!==R?(c=(0,j.jsx)(cf,{className:l,style:R}),h[16]=l,h[17]=R,h[18]=c):c=h[18],h[19]!==a||h[20]!==I||h[21]!==c||h[22]!==v?(u=(0,j.jsxs)(ch,{className:a,style:I,children:[v,c]}),h[19]=a,h[20]=I,h[21]=c,h[22]=v,h[23]=u):u=h[23],h[24]!==_||h[25]!==N||h[26]!==u||h[27]!==C?(d=(0,j.jsx)(cg,{side:_,sideOffset:C,className:"tooltip-positioner",style:N,children:u}),h[24]=_,h[25]=N,h[26]=u,h[27]=C,h[28]=d):d=h[28],h[29]!==k||h[30]!==d?(f=(0,j.jsx)(cy,{container:k,children:d}),h[29]=k,h[30]=d,h[31]=f):f=h[31],h[32]!==f||h[33]!==n?(p=(0,j.jsx)(cw,{children:(0,j.jsxs)(cj,{delay:400,children:[n,f]})}),h[32]=f,h[33]=n,h[34]=p):p=h[34],p});function cT(e){let t,r,n=(0,S.c)(3),{possibleExtension:o,missingGlobalError:a}=e,i=a?`No global-error.${o} found: Add one to ensure users see a helpful message when an unexpected error occurs.`:null;return n[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)(cA,{}),n[0]=t):t=n[0],n[1]!==i?(r=(0,j.jsx)("span",{className:"segment-explorer-suggestions",children:(0,j.jsx)(cE,{className:"segment-explorer-suggestions-tooltip",title:i,children:t})}),n[1]=i,n[2]=r):r=n[2],r}let cN=e=>!!e.value?.type&&!!e.value?.pagePath;function cL(e){let t,r,n=(0,S.c)(3),{page:o}=e;return n[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)(cD,{}),n[0]=t):t=n[0],n[1]!==o?(r=(0,j.jsxs)("div",{className:"segment-explorer-page-route-bar",children:[t,(0,j.jsx)("span",{className:"segment-explorer-page-route-bar-path",children:o})]}),n[1]=o,n[2]=r):r=n[2],r}function cI(e){let t,r,n,o=(0,S.c)(9),{activeBoundariesCount:a,onGlobalReset:i}=e,l=a>0,s=`segment-explorer-footer-button ${!l?"segment-explorer-footer-button--disabled":""}`,c=l?i:void 0,u=!l;return o[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("span",{className:"segment-explorer-footer-text",children:"Clear Segment Overrides"}),o[0]=t):t=o[0],o[1]!==a||o[2]!==l?(r=l&&(0,j.jsx)("span",{className:"segment-explorer-footer-badge",children:a}),o[1]=a,o[2]=l,o[3]=r):r=o[3],o[4]!==s||o[5]!==c||o[6]!==u||o[7]!==r?(n=(0,j.jsx)("div",{className:"segment-explorer-footer",children:(0,j.jsxs)("button",{className:s,onClick:c,disabled:u,type:"button",children:[t,r]})}),o[4]=s,o[5]=c,o[6]=u,o[7]=r,o[8]=n):n=o[8],n}function cP(e){let t,r,n,o,a,i=(0,S.c)(15),{type:l,isBuiltin:s,isOverridden:c,filePath:u,fileName:d}=e,f=`segment-explorer-file-label--${l}`,p=s&&"segment-explorer-file-label--builtin",h=c&&"segment-explorer-file-label--overridden";return i[0]!==f||i[1]!==p||i[2]!==h?(t=e6("segment-explorer-file-label",f,p,h),i[0]=f,i[1]=p,i[2]=h,i[3]=t):t=i[3],i[4]!==u?(r=()=>{!function({filePath:e}){let t=new URLSearchParams({file:e,isAppRelativePath:"1"});fetch(`${process.env.__NEXT_ROUTER_BASEPATH||""}/__nextjs_launch-editor?${t.toString()}`)}({filePath:u})},i[4]=u,i[5]=r):r=i[5],i[6]!==d?(n=(0,j.jsx)("span",{className:"segment-explorer-file-label-text",children:d}),i[6]=d,i[7]=n):n=i[7],i[8]!==s?(o=s?(0,j.jsx)(cA,{}):(0,j.jsx)(cZ,{className:"code-icon"}),i[8]=s,i[9]=o):o=i[9],i[10]!==t||i[11]!==r||i[12]!==n||i[13]!==o?(a=(0,j.jsxs)("span",{className:t,onClick:r,children:[n,o]}),i[10]=t,i[11]=r,i[12]=n,i[13]=o,i[14]=a):a=i[14],a}function cz(e){let t,r,n,o,a,i,l,s,c=(0,S.c)(17),{page:u}=e,d=(0,C.useSyncExternalStore)(oo,oa,oi);c[0]!==d?(t=function e(t){let r=0;return t.value?.setBoundaryType&&null!==t.value.boundaryType&&!s8(t.value.type)&&r++,Object.values(t.children).forEach(t=>{t&&(r+=e(t))}),r}(d),c[0]=d,c[1]=t):t=c[1];let f=t;c[2]!==d?(r=()=>{!function e(t){t.value?.setBoundaryType&&t.value.setBoundaryType(null),Object.values(t.children).forEach(t=>{t&&e(t)})}(d)},c[2]=d,c[3]=r):r=c[3];let p=r;return c[4]===Symbol.for("react.memo_cache_sentinel")?(n={display:"flex",flexDirection:"column",height:"100%"},c[4]=n):n=c[4],c[5]!==u?(o=(0,j.jsx)(cL,{page:u}),c[5]=u,c[6]=o):o=c[6],c[7]===Symbol.for("react.memo_cache_sentinel")?(a={flex:"1 1 auto",overflow:"auto"},c[7]=a):a=c[7],c[8]!==d?(i=(0,j.jsx)("div",{className:"segment-explorer-content","data-nextjs-devtool-segment-explorer":!0,style:a,children:(0,j.jsx)(cO,{node:d,level:0,segment:""})}),c[8]=d,c[9]=i):i=c[9],c[10]!==f||c[11]!==p?(l=(0,j.jsx)(cI,{activeBoundariesCount:f,onGlobalReset:p}),c[10]=f,c[11]=p,c[12]=l):l=c[12],c[13]!==o||c[14]!==i||c[15]!==l?(s=(0,j.jsxs)("div",{"data-nextjs-devtools-panel-segments-explorer":!0,style:n,children:[o,i,l]}),c[13]=o,c[14]=i,c[15]=l,c[16]=s):s=c[16],s}let cR="global-error";function cO(e){let t,r,n,o,a,i,l,s,c,u,d,f,p=(0,S.c)(38),{segment:h,node:m,level:g}=e;p[0]!==m.children?(t=Object.keys(m.children),p[0]=m.children,p[1]=t):t=p[1];let v=t;p[2]!==v||p[3]!==m.children?(r=[],v.forEach(e=>{let t=m.children[e];if(!t||!t.value)return;let n=s7(t.value.type),o=n===cR;(o&&!t.value.pagePath.startsWith(s5)||!o&&s8(t.value.type))&&r.push(n)}),p[2]=v,p[3]=m.children,p[4]=r):r=p[4];let y=0===g&&!r.includes(cR);if(p[5]!==v||p[6]!==g||p[7]!==m.children||p[8]!==h){let e;p[16]!==m.children?(e=(e,t)=>{let r=e.includes("."),n=t.includes(".");if(r&&!n)return -1;if(!r&&n)return 1;if(r&&n){let r=m.children[e]?.value?.type,n=m.children[t]?.value?.type,o=cM,a=o(r),i=o(n);if(a!==i)return a-i;let l=m.children[e]?.value?.pagePath||"",s=m.children[t]?.value?.pagePath||"";return l.localeCompare(s)}return e.localeCompare(t)},p[16]=m.children,p[17]=e):e=p[17];let t=v.sort(e);for(let e of(l=0!==g||h?h:"app",i=[],o=[],t)){let t=m.children[e];if(t){if(cN(t)){o.push(e);continue}i.push(e)}}c=s6(o[0]||"").split(".").pop()||"js",a=null;for(let e=t.length-1;e>=0;e--){let r=m.children[t[e]];if(r&&r.value&&!s8(r.value.type)){a=r;break}}let r=null;for(let e of t){let t=m.children[e];if(t&&t.value&&s8(t.value.type)){r=t;break}}a=a||r,s=o.length>0,n={"not-found":null,loading:null,error:null,"global-error":null},o.forEach(e=>{let t=m.children[e];if(t&&t.value&&s8(t.value.type)){let e=s7(t.value.type);e in n&&(n[e]=t.value.pagePath||null)}}),p[5]=v,p[6]=g,p[7]=m.children,p[8]=h,p[9]=n,p[10]=o,p[11]=a,p[12]=i,p[13]=l,p[14]=s,p[15]=c}else n=p[9],o=p[10],a=p[11],i=p[12],l=p[13],s=p[14],c=p[15];return p[18]!==n||p[19]!==o||p[20]!==a||p[21]!==l||p[22]!==s||p[23]!==g||p[24]!==y||p[25]!==m||p[26]!==c||p[27]!==h?(u=s&&(0,j.jsx)("div",{className:"segment-explorer-item","data-nextjs-devtool-segment-explorer-segment":h+"-"+g,children:(0,j.jsx)("div",{className:"segment-explorer-item-row",style:{...{paddingLeft:`${(g+1)*8}px`}},children:(0,j.jsx)("div",{className:"segment-explorer-item-row-main",children:(0,j.jsxs)("div",{className:"segment-explorer-filename",children:[l&&(0,j.jsxs)("span",{className:"segment-explorer-filename--path",children:[l,(0,j.jsx)("small",{children:"/"})]}),y&&(0,j.jsx)(cT,{possibleExtension:c,missingGlobalError:y}),o.length>0&&(0,j.jsx)("span",{className:"segment-explorer-files",children:o.map(e=>{let t=m.children[e];if(!t||!t.value||s8(t.value.type))return null;let r=t.value.pagePath,n=r.split("/").pop()||"",o=r.startsWith(s5),a=s6(n),i=o?`The default Next.js ${t.value.type} is being shown. You can customize this page by adding your own ${a} file to the app/ directory.`:null,l=null!==t.value.boundaryType;return(0,j.jsx)(cE,{className:"segment-explorer-file-label-tooltip--"+(o?"lg":"sm"),direction:o?"right":"top",title:i,offset:12,children:(0,j.jsx)(cP,{type:t.value.type,isBuiltin:o,isOverridden:l,filePath:r,fileName:a})},e)})}),a&&a.value&&(0,j.jsx)(ce,{nodeState:a.value,boundaries:n})]})})})}),p[18]=n,p[19]=o,p[20]=a,p[21]=l,p[22]=s,p[23]=g,p[24]=y,p[25]=m,p[26]=c,p[27]=h,p[28]=u):u=p[28],p[29]!==i||p[30]!==s||p[31]!==g||p[32]!==m||p[33]!==h?(d=i.map(e=>{let t=m.children[e];if(!t)return null;let r=s?e:h+" / "+e;return(0,j.jsx)(cO,{segment:r,node:t,level:s?g+1:g},e)}),p[29]=i,p[30]=s,p[31]=g,p[32]=m,p[33]=h,p[34]=d):d=p[34],p[35]!==u||p[36]!==d?(f=(0,j.jsxs)(j.Fragment,{children:[u,d]}),p[35]=u,p[36]=d,p[37]=f):f=p[37],f}function cM(e){return e?"layout"===e?1:"template"===e?2:"page"===e?3:s8(e)?4:5:5}function cA(e){let t,r,n,o=(0,S.c)(4);return o[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("path",{d:"M14 8C14 11.3137 11.3137 14 8 14C4.68629 14 2 11.3137 2 8C2 4.68629 4.68629 2 8 2C11.3137 2 14 4.68629 14 8Z",fill:"var(--color-gray-400)"}),r=(0,j.jsx)("path",{d:"M7.75 7C8.30228 7.00001 8.75 7.44772 8.75 8V11.25H7.25V8.5H6.25V7H7.75ZM8 4C8.55228 4 9 4.44772 9 5C9 5.55228 8.55228 6 8 6C7.44772 6 7 5.55228 7 5C7 4.44772 7.44772 4 8 4Z",fill:"var(--color-gray-900)"}),o[0]=t,o[1]=r):(t=o[0],r=o[1]),o[2]!==e?(n=(0,j.jsxs)("svg",{width:"16",height:"16",viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg",...e,children:[t,r]}),o[2]=e,o[3]=n):n=o[3],n}function cD(){let e,t=(0,S.c)(1);return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"var(--color-gray-600)",xmlns:"http://www.w3.org/2000/svg",children:(0,j.jsx)("path",{d:"M4.5 11.25C4.5 11.3881 4.61193 11.5 4.75 11.5H14.4395L11.9395 9L13 7.93945L16.7803 11.7197L16.832 11.7764C17.0723 12.0709 17.0549 12.5057 16.7803 12.7803L13 16.5605L11.9395 15.5L14.4395 13H4.75C3.7835 13 3 12.2165 3 11.25V4.25H4.5V11.25Z"})}),t[0]=e):e=t[0],e}function cZ(e){let t,r,n=(0,S.c)(3);return n[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M7.22763 14.1819L10.2276 2.18193L10.4095 1.45432L8.95432 1.09052L8.77242 1.81812L5.77242 13.8181L5.59051 14.5457L7.04573 14.9095L7.22763 14.1819ZM3.75002 12.0607L3.21969 11.5304L0.39647 8.70713C0.00594559 8.31661 0.00594559 7.68344 0.39647 7.29292L3.21969 4.46969L3.75002 3.93936L4.81068 5.00002L4.28035 5.53035L1.81068 8.00003L4.28035 10.4697L4.81068 11L3.75002 12.0607ZM12.25 12.0607L12.7804 11.5304L15.6036 8.70713C15.9941 8.31661 15.9941 7.68344 15.6036 7.29292L12.7804 4.46969L12.25 3.93936L11.1894 5.00002L11.7197 5.53035L14.1894 8.00003L11.7197 10.4697L11.1894 11L12.25 12.0607Z",fill:"currentColor"}),n[0]=t):t=n[0],n[1]!==e?(r=(0,j.jsx)("svg",{width:"12",height:"12",strokeLinejoin:"round",viewBox:"0 0 16 16",fill:"currentColor",...e,children:t}),n[1]=e,n[2]=r):r=n[2],r}function cF(e){let t,r,n,o,a,i,l,s,c,u,d,f=(0,S.c)(18),{title:p,children:h,ref:m}=e,{setPanel:g}=nv(),v=(0,C.useRef)(null);return f[0]===Symbol.for("react.memo_cache_sentinel")?(t=()=>{v.current?.focus()},r=[],f[0]=t,f[1]=r):(t=f[0],r=f[1]),(0,C.useLayoutEffect)(t,r),f[2]===Symbol.for("react.memo_cache_sentinel")?(n={width:"100%",display:"flex",alignItems:"center",justifyContent:"space-between",padding:"8px 20px",userSelect:"none",WebkitUserSelect:"none",borderBottom:"1px solid var(--color-gray-alpha-400)"},f[2]=n):n=f[2],f[3]===Symbol.for("react.memo_cache_sentinel")?(o={margin:0,fontSize:"14px",color:"var(--color-text-primary)",fontWeight:"normal"},f[3]=o):o=f[3],f[4]!==p?(a=(0,j.jsx)("h3",{style:o,children:p}),f[4]=p,f[5]=a):a=f[5],f[6]!==g?(i=()=>{g("panel-selector")},f[6]=g,f[7]=i):i=f[7],f[8]===Symbol.for("react.memo_cache_sentinel")?(l={background:"none",border:"none",cursor:"pointer",padding:"4px",display:"flex",alignItems:"center",justifyContent:"center",borderRadius:"4px",color:"var(--color-gray-900)"},s=(0,j.jsx)(cU,{}),f[8]=l,f[9]=s):(l=f[8],s=f[9]),f[10]!==i?(c=(0,j.jsx)("button",{ref:v,id:"_next-devtools-panel-close",className:"dev-tools-info-close-button",onClick:i,"aria-label":"Close devtools panel",style:l,children:s}),f[10]=i,f[11]=c):c=f[11],f[12]===Symbol.for("react.memo_cache_sentinel")?(u=(0,j.jsx)("style",{children:e_`
        .dev-tools-info-close-button:focus-visible {
          outline: var(--focus-ring);
        }
      `}),f[12]=u):u=f[12],f[13]!==h||f[14]!==m||f[15]!==a||f[16]!==c?(d=(0,j.jsxs)("div",{style:n,ref:m,children:[a,h,c,u]}),f[13]=h,f[14]=m,f[15]=a,f[16]=c,f[17]=d):d=f[17],d}function cU(e){let t,r,n,o=(0,S.c)(4),{size:a}=e,i=void 0===a?22:a;return o[0]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("path",{d:"M18 6 6 18"}),r=(0,j.jsx)("path",{d:"m6 6 12 12"}),o[0]=t,o[1]=r):(t=o[0],r=o[1]),o[2]!==i?(n=(0,j.jsxs)("svg",{xmlns:"http://www.w3.org/2000/svg",width:i,height:i,viewBox:"0 0 24 24",fill:"none",stroke:"currentColor",strokeWidth:"2",strokeLinecap:"round",strokeLinejoin:"round",children:[t,r]}),o[2]=i,o[3]=n):n=o[3],n}function c$(){let e,t=(0,S.c)(1);return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:"16",height:"16",viewBox:"0 0 20 20",fill:"none",children:(0,j.jsx)("path",{fill:"currentColor",fillRule:"evenodd",d:"m9.7 3.736.045-.236h.51l.044.236a2.024 2.024 0 0 0 1.334 1.536c.19.066.375.143.554.23.618.301 1.398.29 2.03-.143l.199-.136.36.361-.135.199a2.024 2.024 0 0 0-.143 2.03c.087.179.164.364.23.554.224.65.783 1.192 1.536 1.334l.236.044v.51l-.236.044a2.024 2.024 0 0 0-1.536 1.334 4.95 4.95 0 0 1-.23.554 2.024 2.024 0 0 0 .143 2.03l.136.199-.361.36-.199-.135a2.024 2.024 0 0 0-2.03-.143c-.179.087-.364.164-.554.23a2.024 2.024 0 0 0-1.334 1.536l-.044.236h-.51l-.044-.236a2.024 2.024 0 0 0-1.334-1.536 4.952 4.952 0 0 1-.554-.23 2.024 2.024 0 0 0-2.03.143l-.199.136-.36-.361.135-.199a2.024 2.024 0 0 0 .143-2.03 4.958 4.958 0 0 1-.23-.554 2.024 2.024 0 0 0-1.536-1.334l-.236-.044v-.51l.236-.044a2.024 2.024 0 0 0 1.536-1.334 4.96 4.96 0 0 1 .23-.554 2.024 2.024 0 0 0-.143-2.03l-.136-.199.361-.36.199.135a2.024 2.024 0 0 0 2.03.143c.179-.087.364-.164.554-.23a2.024 2.024 0 0 0 1.334-1.536ZM8.5 2h3l.274 1.46c.034.185.17.333.348.394.248.086.49.186.722.3.17.082.37.074.526-.033l1.226-.839 2.122 2.122-.84 1.226a.524.524 0 0 0-.032.526c.114.233.214.474.3.722.061.177.21.314.394.348L18 8.5v3l-1.46.274a.524.524 0 0 0-.394.348 6.47 6.47 0 0 1-.3.722.524.524 0 0 0 .033.526l.839 1.226-2.122 2.122-1.226-.84a.524.524 0 0 0-.526-.032 6.477 6.477 0 0 1-.722.3.524.524 0 0 0-.348.394L11.5 18h-3l-.274-1.46a.524.524 0 0 0-.348-.394 6.477 6.477 0 0 1-.722-.3.524.524 0 0 0-.526.033l-1.226.839-2.122-2.122.84-1.226a.524.524 0 0 0 .032-.526 6.453 6.453 0 0 1-.3-.722.524.524 0 0 0-.394-.348L2 11.5v-3l1.46-.274a.524.524 0 0 0 .394-.348c.086-.248.186-.49.3-.722a.524.524 0 0 0-.033-.526l-.839-1.226 2.122-2.122 1.226.84a.524.524 0 0 0 .526.032 6.46 6.46 0 0 1 .722-.3.524.524 0 0 0 .348-.394L8.5 2Zm3 8a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0Zm1.5 0a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z",clipRule:"evenodd"})}),t[0]=e):e=t[0],e}function cH(){let e,t=(0,S.c)(1);return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("svg",{width:"20px",height:"20px",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:(0,j.jsx)("circle",{cx:"10",cy:"10",r:"7",stroke:"currentColor",strokeWidth:"2",strokeLinecap:"round",strokeDasharray:"32 12",opacity:"0.8",children:(0,j.jsx)("animateTransform",{attributeName:"transform",type:"rotate",from:"0 10 10",to:"360 10 10",dur:"1s",repeatCount:"indefinite"})})}),t[0]=e):e=t[0],e}var cV=__webpack_require__("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/components/instant-navs/instant-navs-panel.css"),cB={};cB.styleTagTransform=b(),cB.setAttributes=m(),cB.insert=p(),cB.domAPI=d(),cB.insertStyleElement=v(),c()(cV.A,cB),cV.A&&cV.A.locals&&cV.A.locals;let cq="next-instant-navigation-testing";function cW(){let e,t,r,n,o,a,i,l,s,c,u=(0,S.c)(60),{state:d,dispatch:f}=us(),p=function(){let e,t=(0,S.c)(2),r=(0,C.useSyncExternalStore)(M,O);r:{let n;if(!r){e=null;break r}t[0]!==r?(n=z(r),t[0]=r,t[1]=n):n=t[1],e=n}return e}(),[h,m]=(0,C.useState)(!1);h&&null!==p&&("spa"===p.state||"mpa"===p.state)&&m(!1),u[0]!==f?(e=()=>()=>{"undefined"!=typeof cookieStore&&cookieStore.delete(cq),f({type:es})},t=[f],u[0]=f,u[1]=e,u[2]=t):(e=u[1],t=u[2]),(0,C.useEffect)(e,t),u[3]===Symbol.for("react.memo_cache_sentinel")?(r=function(){"undefined"!=typeof cookieStore&&cookieStore.set({name:cq,value:JSON.stringify([0,`p${Math.random()}`]),path:"/"}),window.location.reload()},u[3]=r):r=u[3];let g=r;u[4]===Symbol.for("react.memo_cache_sentinel")?(n=function(){"undefined"!=typeof cookieStore&&cookieStore.set({name:cq,value:JSON.stringify([0,`p${Math.random()}`]),path:"/"}),m(!0)},u[4]=n):n=u[4];let v=n;u[5]===Symbol.for("react.memo_cache_sentinel")?(o=function(){"undefined"!=typeof cookieStore&&cookieStore.delete(cq)},u[5]=o):o=u[5];let y=o;u[6]!==p||u[7]!==d.page?(a=function(){let e=new URL(d.page,window.location.origin);return e.searchParams.set("__instant_nav","1"),null!==p&&"spa"===p.state&&(e.searchParams.set("from",R(p.fromTree)),null!==p.toTree&&e.searchParams.set("to",R(p.toTree))),e.toString()},u[6]=p,u[7]=d.page,u[8]=a):a=u[8];let b=a;if(null!==p&&"spa"===p.state){let e,t,r,n,o,a,i,l,s,c,f,h,m,g,v,x=d.renderingIndicator;return u[9]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("div",{className:"instant-nav-section-header",children:(0,j.jsx)("label",{children:"Client navigation"})}),u[9]=e):e=u[9],u[10]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("span",{className:"instant-nav-url-label",children:"From:"}),u[10]=t):t=u[10],u[11]!==p.fromTree?(r=R(p.fromTree),u[11]=p.fromTree,u[12]=r):r=u[12],u[13]!==r?(n=(0,j.jsxs)("div",{className:"instant-nav-url-row",children:[t,(0,j.jsx)("span",{className:"instant-nav-url-value",children:r})]}),u[13]=r,u[14]=n):n=u[14],u[15]===Symbol.for("react.memo_cache_sentinel")?(o=(0,j.jsx)("span",{className:"instant-nav-url-label",children:"To:"}),u[15]=o):o=u[15],u[16]!==p.toTree||u[17]!==x?(a=null===p.toTree||x?(0,j.jsx)("span",{className:"instant-nav-skeleton"}):R(p.toTree),u[16]=p.toTree,u[17]=x,u[18]=a):a=u[18],u[19]!==a?(i=(0,j.jsxs)("div",{className:"instant-nav-url-row",children:[o,(0,j.jsx)("span",{className:"instant-nav-url-value",children:a})]}),u[19]=a,u[20]=i):i=u[20],u[21]!==i||u[22]!==n?(l=(0,j.jsxs)("div",{className:"instant-nav-urls",children:[n,i]}),u[21]=i,u[22]=n,u[23]=l):l=u[23],u[24]===Symbol.for("react.memo_cache_sentinel")?(s=(0,j.jsx)("p",{className:"instant-nav-helper-description",children:"You're viewing the prefetched UI for the previous navigation to the current URL."}),u[24]=s):s=u[24],u[25]!==l?(c=(0,j.jsxs)("div",{className:"instant-nav-content",children:[e,l,s]}),u[25]=l,u[26]=c):c=u[26],u[27]===Symbol.for("react.memo_cache_sentinel")?(f={display:"none"},u[27]=f):f=u[27],u[28]!==b?(h=(0,j.jsx)("span",{style:f,children:(0,j.jsx)(cK,{getShareUrl:b})}),u[28]=b,u[29]=h):h=u[29],u[30]===Symbol.for("react.memo_cache_sentinel")?(m=(0,j.jsx)("button",{className:"instant-nav-footer-button",onClick:y,type:"button",children:"Continue rendering"}),u[30]=m):m=u[30],u[31]!==h?(g=(0,j.jsxs)("div",{className:"instant-nav-footer",children:[h,m]}),u[31]=h,u[32]=g):g=u[32],u[33]!==c||u[34]!==g?(v=(0,j.jsxs)("div",{className:"instant-nav-panel",children:[c,g]}),u[33]=c,u[34]=g,u[35]=v):v=u[35],v}if(null!==p&&"mpa"===p.state){let e,t,r,n,o,a,i,l,s,c,f;return u[36]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("div",{className:"instant-nav-section-header",children:(0,j.jsx)("label",{children:"Page load"})}),u[36]=e):e=u[36],u[37]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)("span",{className:"instant-nav-url-label",children:"Route:"}),u[37]=t):t=u[37],u[38]!==d.renderingIndicator||u[39]!==d.tree?(r=null===d.tree||d.renderingIndicator?(0,j.jsx)("span",{className:"instant-nav-skeleton"}):R(d.tree),u[38]=d.renderingIndicator,u[39]=d.tree,u[40]=r):r=u[40],u[41]!==r?(n=(0,j.jsx)("div",{className:"instant-nav-urls",children:(0,j.jsxs)("div",{className:"instant-nav-url-row",children:[t,(0,j.jsx)("span",{className:"instant-nav-url-value",children:r})]})}),u[41]=r,u[42]=n):n=u[42],u[43]===Symbol.for("react.memo_cache_sentinel")?(o=(0,j.jsx)("p",{className:"instant-nav-helper-description",children:"You're viewing the pre-rendered static UI for the current URL."}),u[43]=o):o=u[43],u[44]!==n?(a=(0,j.jsxs)("div",{className:"instant-nav-content",children:[e,n,o]}),u[44]=n,u[45]=a):a=u[45],u[46]===Symbol.for("react.memo_cache_sentinel")?(i={display:"none"},u[46]=i):i=u[46],u[47]!==b?(l=(0,j.jsx)("span",{style:i,children:(0,j.jsx)(cK,{getShareUrl:b})}),u[47]=b,u[48]=l):l=u[48],u[49]===Symbol.for("react.memo_cache_sentinel")?(s=(0,j.jsx)("button",{className:"instant-nav-footer-button",onClick:y,type:"button",children:"Continue rendering"}),u[49]=s):s=u[49],u[50]!==l?(c=(0,j.jsxs)("div",{className:"instant-nav-footer",children:[l,s]}),u[50]=l,u[51]=c):c=u[51],u[52]!==a||u[53]!==c?(f=(0,j.jsxs)("div",{className:"instant-nav-panel",children:[a,c]}),u[52]=a,u[53]=c,u[54]=f):f=u[54],f}if(h){let e;return u[55]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("div",{className:"instant-nav-panel",children:(0,j.jsxs)("div",{className:"instant-nav-content",children:[(0,j.jsx)("div",{className:"instant-nav-section-header",children:(0,j.jsx)("label",{children:"Client navigation"})}),(0,j.jsx)("p",{className:"instant-nav-helper-description",children:"Click any link in your app to view the prefetched UI for that page."})]})}),u[55]=e):e=u[55],e}return u[56]===Symbol.for("react.memo_cache_sentinel")?(i=(0,j.jsxs)("div",{className:"instant-nav-section-header",children:[(0,j.jsx)("label",{children:"Page load"}),(0,j.jsx)("p",{className:"instant-nav-section-description",children:"View the initial static UI for this page."})]}),u[56]=i):i=u[56],u[57]===Symbol.for("react.memo_cache_sentinel")?(l=(0,j.jsxs)("div",{className:"instant-nav-section",children:[i,(0,j.jsx)("div",{className:"instant-nav-section-control",children:(0,j.jsxs)("button",{className:"action-button",onClick:g,"data-instant-nav-refresh":!0,children:[(0,j.jsx)(cY,{}),(0,j.jsx)("span",{children:"Reload"})]})})]}),u[57]=l):l=u[57],u[58]===Symbol.for("react.memo_cache_sentinel")?(s=(0,j.jsxs)("div",{className:"instant-nav-section-header",children:[(0,j.jsx)("label",{children:"Client navigation"}),(0,j.jsx)("p",{className:"instant-nav-section-description",children:"Freeze the next navigation to view the prefetched UI."})]}),u[58]=s):s=u[58],u[59]===Symbol.for("react.memo_cache_sentinel")?(c=(0,j.jsxs)("div",{className:"instant-nav-panel",children:[l,(0,j.jsxs)("div",{className:"instant-nav-section",children:[s,(0,j.jsx)("div",{className:"instant-nav-section-control",children:(0,j.jsx)("button",{className:"action-button",onClick:v,"data-instant-nav-client":!0,children:(0,j.jsx)("span",{children:"Start"})})})]})]}),u[59]=c):c=u[59],c}function cK(e){let t,r,n=(0,S.c)(5),{getShareUrl:o}=e,[a,i]=(0,C.useState)(!1);n[0]!==o?(t=function(){navigator.clipboard.writeText(o()).then(()=>{i(!0),setTimeout(()=>i(!1),2e3)})},n[0]=o,n[1]=t):t=n[1];let l=t,s=a?"Copied!":"Share";return n[2]!==l||n[3]!==s?(r=(0,j.jsx)("button",{className:"instant-nav-footer-button",onClick:l,type:"button","data-instant-nav-share":!0,children:s}),n[2]=l,n[3]=s,n[4]=r):r=n[4],r}function cY(){let e,t=(0,S.c)(1);return t[0]===Symbol.for("react.memo_cache_sentinel")?(e=(0,j.jsx)("svg",{width:"14",height:"14",strokeLinejoin:"round",viewBox:"0 0 16 16",fill:"none",children:(0,j.jsx)("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M2.5 8C2.5 4.96643 4.97431 2.5 8.03548 2.5C10.5716 2.5 12.7064 4.19393 13.3628 6.5H10.75H10V8H10.75H15.25C15.6642 8 16 7.66421 16 7.25V2.75V2H14.5V2.75V5.23347C13.4215 2.74164 10.9316 1 8.03548 1C4.1539 1 1 4.13001 1 8C1 11.87 4.1539 15 8.03548 15C10.3763 15 12.4513 13.8617 13.7295 12.1122L14.172 11.5066L12.9609 10.6217L12.5184 11.2273C11.5117 12.6051 9.87945 13.5 8.03548 13.5C4.97431 13.5 2.5 11.0336 2.5 8Z",fill:"currentColor"})}),t[0]=e):e=t[0],e}var cX=__webpack_require__("../../node_modules/.pnpm/css-loader@7.1.2_@rspack+core@1.6.7_@swc+helpers@0.5.15__webpack@5.98.0_@swc+core@1.11.24_@sw_bx7gx6l2cs2trwgqreijicltyy/node_modules/css-loader/dist/cjs.js??ruleSet[1].rules[3].use[1]!./src/next-devtools/dev-overlay/menu/panel-router.css"),cG={};cG.styleTagTransform=b(),cG.setAttributes=m(),cG.insert=p(),cG.domAPI=d(),cG.insertStyleElement=v(),c()(cX.A,cG),cX.A&&cX.A.locals&&cX.A.locals;let cQ=()=>{let e,t,r,n,o,a,i,l,s,c,u,d=(0,S.c)(29),{setPanel:f,setSelectedIndex:p}=nv(),{state:h,dispatch:m}=us(),{totalErrorCount:g}=c9(),v="app"===h.routerType;return d[0]!==m||d[1]!==f||d[2]!==p||d[3]!==h.isErrorOverlayOpen||d[4]!==g?(e=g>0&&{title:`${g} ${1===g?"issue":"issues"} found. Click to view details in the dev overlay.`,label:"Issues",value:(0,j.jsx)(n$,{children:g}),onClick:()=>{if(h.isErrorOverlayOpen){m({type:G}),f(null);return}f(null),p(-1),g>0&&m({type:X})}},d[0]=m,d[1]=f,d[2]=p,d[3]=h.isErrorOverlayOpen,d[4]=g,d[5]=e):e=d[5],d[6]!==f||d[7]!==h.staticIndicator?(t="disabled"===h.staticIndicator?void 0:"pending"===h.staticIndicator?{title:"Loading...",label:"Route",value:(0,j.jsx)(cH,{})}:{title:`Current route is ${h.staticIndicator}.`,label:"Route",value:"static"===h.staticIndicator?"Static":"Dynamic",onClick:()=>f("route-type"),attributes:{"data-nextjs-route-type":h.staticIndicator}},d[6]=f,d[7]=h.staticIndicator,d[8]=t):t=d[8],d[9]===Symbol.for("react.memo_cache_sentinel")?(r=process.env.TURBOPACK?{title:"Turbopack is enabled.",label:"Bundler",value:"Turbopack"}:{title:"Learn about Turbopack and how to enable it in your application.",label:"Bundler",value:(0,j.jsx)("a",{href:"https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack",target:"_blank",rel:"noreferrer noopener",className:"turbopack-upgrade-link",children:process.env.__NEXT_BUNDLER||"Turbopack"})},n=!!process.env.__NEXT_CACHE_COMPONENTS&&{title:"Cache Components is enabled.",label:"Cache Components",value:"Enabled"},d[9]=r,d[10]=n):(r=d[9],n=d[10]),d[11]!==v||d[12]!==f?(o=v&&!!process.env.__NEXT_INSTANT_NAV_TOGGLE&&{title:"Test instant navigation behavior.",label:"Instant Navs",value:(0,j.jsx)(nH,{}),onClick:()=>{f("instant-navs")},attributes:{"data-instant-nav":!0}},d[11]=v,d[12]=f,d[13]=o):o=d[13],d[14]!==v||d[15]!==f?(a=v&&{label:"Route Info",value:(0,j.jsx)(nH,{}),onClick:()=>f("segment-explorer"),attributes:{"data-segment-explorer":!0}},d[14]=v,d[15]=f,d[16]=a):a=d[16],d[17]===Symbol.for("react.memo_cache_sentinel")?(i=(0,j.jsx)(c$,{}),d[17]=i):i=d[17],d[18]!==f?(l=()=>f("preferences"),d[18]=f,d[19]=l):l=d[19],d[20]===Symbol.for("react.memo_cache_sentinel")?(s={"data-preferences":!0},d[20]=s):s=d[20],d[21]!==l?(c={label:"Preferences",value:i,onClick:l,footer:!0,attributes:s},d[21]=l,d[22]=c):c=d[22],d[23]!==e||d[24]!==t||d[25]!==o||d[26]!==a||d[27]!==c?(u=(0,j.jsx)(nF,{items:[e,t,r,n,o,a,c]}),d[23]=e,d[24]=t,d[25]=o,d[26]=a,d[27]=c,d[28]=u):u=d[28],u},cJ=()=>{var e,t;let r,n,o,a,i,l,s,c,u,d,f,p,h,m=(0,S.c)(26),{state:g}=us(),{triggerRef:v}=nv(),y=(()=>{let e,t=(0,S.c)(4),{state:r,dispatch:n,shadowRoot:o}=us();return t[0]!==n||t[1]!==o||t[2]!==r.disableDevIndicator?(e=()=>{n({type:Y,disabled:!r.disableDevIndicator});let e=o.getElementById("panel-route"),t=o.getElementById("data-devtools-indicator");if(e&&e.firstElementChild){let t=e.firstElementChild,r="none"===t.style.display;t.style.display=r?"":"none"}if(t){let e="none"===t.style.display;t.style.display=e?"":"none"}},t[0]=n,t[1]=o,t[2]=r.disableDevIndicator,t[3]=e):e=t[3],e})(),b="app"===g.routerType;m[0]!==g.hideShortcut||m[1]!==y?(r=g.hideShortcut?{[g.hideShortcut]:y}:{},m[0]=g.hideShortcut,m[1]=y,m[2]=r):r=m[2],e=r,t=v,(h=(0,S.c)(4))[0]!==t||h[1]!==e?(f=()=>{let r=function(r){var n;let o;if((o=t4((n=t).current))&&("true"===o.contentEditable||"INPUT"===o.tagName||"TEXTAREA"===o.tagName||"SELECT"===o.tagName||"true"===o.dataset["shortcut-recorder"])&&!o.hasAttribute("readonly"))return;let a=[];r.metaKey&&a.push("Meta"),r.ctrlKey&&a.push("Control"),r.altKey&&a.push("Alt"),r.shiftKey&&a.push("Shift"),"Meta"!==r.key&&"Control"!==r.key&&"Alt"!==r.key&&"Shift"!==r.key&&a.push(r.code);let i=a.join("+");e[i]&&(r.preventDefault(),e[i]())};return window.addEventListener("keydown",r),()=>window.removeEventListener("keydown",r)},p=[t,e],h[0]=t,h[1]=e,h[2]=f,h[3]=p):(f=h[2],p=h[3]),(0,C.useEffect)(f,p),m[3]===Symbol.for("react.memo_cache_sentinel")?(n=(0,j.jsx)(c4,{name:"panel-selector",children:(0,j.jsx)(cQ,{})}),m[3]=n):n=m[3];let x=500/g.scale;return m[4]!==x?(o={kind:"fixed",height:x,width:512},m[4]=x,m[5]=o):o=m[5],m[6]===Symbol.for("react.memo_cache_sentinel")?(a=(0,j.jsx)(cF,{title:"Preferences"}),i=(0,j.jsx)(c1,{}),m[6]=a,m[7]=i):(a=m[6],i=m[7]),m[8]!==o?(l=(0,j.jsx)(c4,{name:"preferences",children:(0,j.jsx)(n6,{sharePanelSizeGlobally:!1,sizeConfig:o,closeOnClickOutside:!0,header:a,children:i})}),m[8]=o,m[9]=l):l=m[9],m[10]!==g.routerType||m[11]!==g.scale||m[12]!==g.staticIndicator?(s="disabled"!==g.staticIndicator&&"pending"!==g.staticIndicator&&(0,j.jsx)(c4,{name:"route-type",children:(0,j.jsx)(n6,{sharePanelSizeGlobally:!1,sizeConfig:{kind:"fixed",height:"static"===g.staticIndicator?300/g.scale:325/g.scale,width:400/g.scale},closeOnClickOutside:!0,header:(0,j.jsx)(cF,{title:`${"static"===g.staticIndicator?"Static":"Dynamic"} Route`}),children:(0,j.jsxs)("div",{className:"panel-content",children:[(0,j.jsx)(oe,{routerType:g.routerType,isStaticRoute:"static"===g.staticIndicator}),(0,j.jsx)(c0,{href:n7[g.routerType][g.staticIndicator]})]})},g.staticIndicator)}),m[10]=g.routerType,m[11]=g.scale,m[12]=g.staticIndicator,m[13]=s):s=m[13],m[14]!==b||m[15]!==g.page||m[16]!==g.scale?(c=b&&(0,j.jsx)(c4,{name:"segment-explorer",children:(0,j.jsx)(n6,{sharePanelSizeGlobally:!1,sharePanelPositionGlobally:!1,draggable:!0,sizeConfig:{kind:"resizable",maxHeight:"90vh",maxWidth:"90vw",minHeight:200/g.scale,minWidth:250/g.scale,initialSize:{height:375/g.scale,width:400/g.scale}},header:(0,j.jsx)(cF,{title:"Route Info"}),children:(0,j.jsx)(cz,{page:g.page})})}),m[14]=b,m[15]=g.page,m[16]=g.scale,m[17]=c):c=m[17],m[18]!==b||m[19]!==g.scale?(u=b&&!!process.env.__NEXT_INSTANT_NAV_TOGGLE&&(0,j.jsx)(c4,{name:"instant-navs",children:(0,j.jsx)(n6,{sharePanelSizeGlobally:!1,sizeConfig:{kind:"fixed",height:300/g.scale,width:480/g.scale},header:(0,j.jsx)(cF,{title:"Instant Navs"}),children:(0,j.jsx)(cW,{})})}),m[18]=b,m[19]=g.scale,m[20]=u):u=m[20],m[21]!==l||m[22]!==s||m[23]!==c||m[24]!==u?(d=(0,j.jsxs)(j.Fragment,{children:[n,l,s,c,u]}),m[21]=l,m[22]=s,m[23]=c,m[24]=u,m[25]=d):d=m[25],d},c0=e=>{let t,r=(0,S.c)(2),{href:n}=e;return r[0]!==n?(t=(0,j.jsx)("div",{className:"dev-tools-info-button-container",children:(0,j.jsx)("a",{className:"dev-tools-info-learn-more-button",href:n,target:"_blank",rel:"noreferrer noopener",children:"Learn More"})}),r[0]=n,r[1]=t):t=r[1],t},c1=()=>{let e,t,r,n,o=(0,S.c)(17),{dispatch:a,state:i}=us(),{setPanel:l,setSelectedIndex:s}=nv(),c=nM();return o[0]!==a?(e=e=>{a({type:ea,scale:e})},o[0]=a,o[1]=e):e=o[1],o[2]!==a||o[3]!==c?(t=e=>{a({type:en,devToolsPosition:e}),c(e)},o[2]=a,o[3]=c,o[4]=t):t=o[4],o[5]!==a||o[6]!==l||o[7]!==s?(r=()=>{a({type:Y,disabled:!0}),s(-1),l(null),fetch("/__nextjs_disable_dev_indicator",{method:"POST"})},o[5]=a,o[6]=l,o[7]=s,o[8]=r):r=o[8],o[9]!==i.devToolsPosition||o[10]!==i.hideShortcut||o[11]!==i.scale||o[12]!==i.theme||o[13]!==e||o[14]!==t||o[15]!==r?(n=(0,j.jsx)("div",{className:"user-preferences-wrapper",children:(0,j.jsx)(r7,{theme:i.theme,position:i.devToolsPosition,scale:i.scale,setScale:e,setPosition:t,hideShortcut:i.hideShortcut,setHideShortcut:c5,hide:r})}),o[9]=i.devToolsPosition,o[10]=i.hideShortcut,o[11]=i.scale,o[12]=i.theme,o[13]=e,o[14]=t,o[15]=r,o[16]=n):n=o[16],n},c2=()=>(0,C.useContext)(c3),c3=(0,C.createContext)(null);function c4(e){let t,r,n,o,a,i=(0,S.c)(12),{children:l,name:s}=e,{panel:c}=nv();i[0]===Symbol.for("react.memo_cache_sentinel")?(t={enterDelay:0,exitDelay:200},i[0]=t):t=i[0];let{mounted:u,rendered:d}=ni(s===c,t);if(!u)return null;i[1]!==u||i[2]!==s?(r={name:s,mounted:u},i[1]=u,i[2]=s,i[3]=r):r=i[3];let f=+!!d;i[4]!==f?(n={"--panel-opacity":f,"--panel-transition":`opacity 200ms ${t6}`},i[4]=f,i[5]=n):n=i[5];let p=n;return i[6]!==l||i[7]!==p?(o=(0,j.jsx)("div",{id:"panel-route",className:"panel-route",style:p,children:l}),i[6]=l,i[7]=p,i[8]=o):o=i[8],i[9]!==r||i[10]!==o?(a=(0,j.jsx)(c3,{value:r,children:o}),i[9]=r,i[10]=o,i[11]=a):a=i[11],a}function c5(e){r8({hideShortcut:e})}let c6=(0,C.createContext)(null),c9=()=>(0,C.useContext)(c6);function c8(){let e,t,r,n,o,a=(0,S.c)(13),[i,l]=(0,C.useState)(-1),{state:s,dispatch:c,getSquashedHydrationErrorDetails:u}=us();a[0]!==s.instantNavs?(e=()=>s.instantNavs?"instant-navs":null,a[0]=s.instantNavs,a[1]=e):e=a[1];let[d,f]=(0,C.useState)(e),p=(0,C.useRef)(null);return a[2]===Symbol.for("react.memo_cache_sentinel")?(t=(0,j.jsx)(nd,{}),r=(0,j.jsx)(na,{}),a[2]=t,a[3]=r):(t=a[2],r=a[3]),a[4]!==c||a[5]!==u||a[6]!==d||a[7]!==i||a[8]!==s?(n=e=>{let{runtimeErrors:t,totalErrorCount:r}=e;return(0,j.jsx)(j.Fragment,{children:s.showIndicator?(0,j.jsx)(j.Fragment,{children:(0,j.jsx)(c6,{value:{runtimeErrors:t,totalErrorCount:r},children:(0,j.jsxs)(ng,{value:{panel:d,setPanel:f,triggerRef:p,selectedIndex:i,setSelectedIndex:l},children:[(0,j.jsx)(nl,{state:s,dispatch:c,getSquashedHydrationErrorDetails:u,runtimeErrors:t,errorCount:r}),(0,j.jsx)(cJ,{}),(0,j.jsx)(nO,{})]})})}):null})},a[4]=c,a[5]=u,a[6]=d,a[7]=i,a[8]=s,a[9]=n):n=a[9],a[10]!==s||a[11]!==n?(o=(0,j.jsxs)(eS,{children:[t,r,(0,j.jsx)(ns,{state:s,isAppDir:!0,children:n})]}),a[10]=s,a[11]=n,a[12]=o):o=a[12],o}let c7=null,ue=[],ut=null;function ur(){return ut?{...ut,errors:ut.errors.map(e=>({...e,error:e.error?{name:e.error.name,message:e.error.message,stack:e.error.stack}:null}))}:null}function un(){return ut?{segmentTrie:ou(),routerType:ut.routerType}:null}function uo(e){return(...t)=>{c7?e(c7,...t):ue.push(r=>{e(r,...t)})}}let ua={onBuildOk:uo(e=>{e({type:F})}),onBuildError:uo((e,t)=>{e({type:U,message:t})}),onBeforeRefresh:uo(e=>{e({type:$})}),onRefresh:uo(e=>{e({type:H})}),onVersionInfo:uo((e,t)=>{e({type:V,versionInfo:t})}),onCacheIndicator:uo((e,t)=>{e({type:D,cacheIndicator:t})}),onStaticIndicator:uo((e,t)=>{e({type:Z,staticIndicator:t})}),onDebugInfo:uo((e,t)=>{e({type:W,debugInfo:t})}),onDevIndicator:uo((e,t)=>{e({type:K,devIndicator:t})}),onDevToolsConfig:uo((e,t)=>{e({type:ei,devToolsConfig:t})}),onUnhandledError:uo((e,t)=>{e({type:B,reason:t})}),onUnhandledRejection:uo((e,t)=>{e({type:q,reason:t})}),openErrorOverlay:uo(e=>{e({type:X})}),closeErrorOverlay:uo(e=>{e({type:G})}),toggleErrorOverlay:uo(e=>{e({type:Q})}),buildingIndicatorHide:uo(e=>{e({type:ee})}),buildingIndicatorShow:uo(e=>{e({type:J})}),renderingIndicatorHide:uo(e=>{e({type:er})}),renderingIndicatorShow:uo(e=>{e({type:et})}),segmentExplorerNodeAdd:uo((e,t)=>{os(t)}),segmentExplorerNodeRemove:uo((e,t)=>{oc(t)}),segmentExplorerUpdateRouteState:uo((e,t,r)=>{e({type:ep,page:t,tree:r})}),instantNavsToggle:uo(e=>{e({type:el})})};function ui(e){let t,r,n,o,a,i,l,s,c,u,d=(0,S.c)(22),{enableCacheIndicator:f,getOwnerStack:p,getSquashedHydrationErrorDetails:h,isRecoverableError:m,routerType:g,shadowRoot:v}=e,[y,b]=function(e,t,r,n){let o,a,i,l=(0,S.c)(8);l[0]!==t||l[1]!==r?(o=function(e,n,o){let a,i=t(o),l=L((o.stack||"")+(i||"")),s={id:n,error:o,frames:l,type:r(o)?"recoverable":(a=o)&&"NEXT_CONSOLE_ERROR"===a[I]?"console":"runtime"},c=e.filter(e=>""+e.error!=""+s.error||e.error.stack!==s.error.stack&&em(e.error.stack)!==em(s.error.stack)||t(e.error)!==t(s.error));return c.length===e.length?(c.push(s),c):e},l[0]=t,l[1]=r,l[2]=o):o=l[2];let s=o;if(l[3]!==s?(a=(e,t)=>{switch(t.type){case W:return{...e,debugInfo:t.debugInfo};case D:return{...e,cacheIndicator:t.cacheIndicator};case Z:return{...e,staticIndicator:t.staticIndicator};case F:return{...e,buildError:null};case U:return{...e,buildError:t.message};case $:return{...e,refreshState:{type:"pending",errors:[]}};case H:return{...e,buildError:null,errors:"pending"===e.refreshState.type?e.refreshState.errors:[],refreshState:{type:"idle"}};case B:case q:switch(e.refreshState.type){case"idle":return{...e,nextId:e.nextId+1,errors:s(e.errors,e.nextId,t.reason)};case"pending":return{...e,nextId:e.nextId+1,refreshState:{...e.refreshState,errors:s(e.errors,e.nextId,t.reason)}};default:return e}case V:return{...e,versionInfo:t.versionInfo};case Y:return{...e,disableDevIndicator:t.disabled};case K:return{...e,showIndicator:!0,disableDevIndicator:eg||!!t.devIndicator.disabledUntil};case X:return{...e,isErrorOverlayOpen:!0};case G:return{...e,isErrorOverlayOpen:!1};case Q:return{...e,isErrorOverlayOpen:!e.isErrorOverlayOpen};case J:return{...e,buildingIndicator:!0};case ee:return{...e,buildingIndicator:!1};case et:return{...e,renderingIndicator:!0};case er:return{...e,renderingIndicator:!1};case en:return{...e,devToolsPosition:t.devToolsPosition};case eo:return{...e,devToolsPanelPosition:{...e.devToolsPanelPosition,[t.key]:t.devToolsPanelPosition}};case ea:return{...e,scale:t.scale};case ep:return{...e,page:t.page,tree:t.tree};case ei:{let{theme:r,disableDevIndicator:n,devToolsPosition:o,devToolsPanelPosition:a,devToolsPanelSize:i,scale:l,hideShortcut:s}=t.devToolsConfig;return{...e,theme:r??e.theme,disableDevIndicator:n??e.disableDevIndicator,devToolsPosition:o??e.devToolsPosition,devToolsPanelPosition:a??e.devToolsPanelPosition,scale:l??e.scale,devToolsPanelSize:i??e.devToolsPanelSize,hideShortcut:void 0!==s?s:e.hideShortcut}}case el:return{...e,instantNavs:!e.instantNavs};case es:return{...e,instantNavs:!1};default:return e}},l[3]=s,l[4]=a):a=l[4],l[5]!==n||l[6]!==e){var c,u;c=e,u=n,i={...eb,isErrorOverlayOpen:"pages"===c,routerType:c,cacheIndicator:u?"ready":"disabled"},l[5]=n,l[6]=e,l[7]=i}else i=l[7];return(0,C.useReducer)(a,i)}(g,p,m,f);return d[0]!==g||d[1]!==y?(t=()=>{ut={...y,routerType:g}},r=[y,g],d[0]=g,d[1]=y,d[2]=t,d[3]=r):(t=d[2],r=d[3]),(0,C.useEffect)(t,r),d[4]!==v.host||d[5]!==y.theme?(n=()=>{let e=v.host;"dark"===y.theme?(e.classList.add("dark"),e.classList.remove("light")):"light"===y.theme?(e.classList.add("light"),e.classList.remove("dark")):(e.classList.remove("dark"),e.classList.remove("light"))},d[4]=v.host,d[5]=y.theme,d[6]=n):n=d[6],d[7]!==v||d[8]!==y.theme?(o=[v,y.theme],d[7]=v,d[8]=y.theme,d[9]=o):o=d[9],(0,C.useLayoutEffect)(n,o),d[10]!==b?(a=()=>{c7=b;let e=setTimeout(()=>{var e=b;try{for(let t of ue)t(e)}finally{ue.length=0}});return()=>{c7=null,clearTimeout(e)}},d[10]=b,d[11]=a):a=d[11],d[12]===Symbol.for("react.memo_cache_sentinel")?(i=[],d[12]=i):i=d[12],(0,C.useInsertionEffect)(a,i),d[13]===Symbol.for("react.memo_cache_sentinel")?(l=(0,j.jsx)(ew,{}),d[13]=l):l=d[13],d[14]!==b||d[15]!==h||d[16]!==v||d[17]!==y?(s={dispatch:b,getSquashedHydrationErrorDetails:h,shadowRoot:v,state:y},d[14]=b,d[15]=h,d[16]=v,d[17]=y,d[18]=s):s=d[18],d[19]===Symbol.for("react.memo_cache_sentinel")?(c=(0,j.jsx)(c8,{}),d[19]=c):c=d[19],d[20]!==s?(u=(0,j.jsxs)(j.Fragment,{children:[l,(0,j.jsx)(ul,{value:s,children:c})]}),d[20]=s,d[21]=u):u=d[21],u}let ul=(0,C.createContext)(null),us=()=>(0,C.useContext)(ul),uc=!1,uu=!1;function ud(){return null}function uf(e,t,r){if(uc)throw Error("Next DevTools: Pages Dev Overlay is already mounted. This is a bug in Next.js");if(!uu){let n=document.createElement("script");n.style.display="block",n.style.position="absolute",n.setAttribute("data-nextjs-dev-overlay","true");let o=document.createElement("nextjs-portal");n.appendChild(o),document.body.appendChild(n);let a=(0,ex.createRoot)(o,{identifierPrefix:"ndt-",onDefaultTransitionIndicator:()=>()=>{}}),i=o.attachShadow({mode:"open"});(0,C.startTransition)(()=>{a.render((0,j.jsx)(ui,{enableCacheIndicator:r,getOwnerStack:e,getSquashedHydrationErrorDetails:ud,isRecoverableError:t,routerType:"app",shadowRoot:i}))}),uu=!0}}function up(e,t,r){if(uu)throw Error("Next DevTools: App Dev Overlay is already mounted. This is a bug in Next.js");if(!uc){let n=document.createElement("nextjs-portal");n.style.position="absolute",new MutationObserver(e=>{for(let t of e)if("childList"===t.type)for(let e of t.removedNodes)e===n&&document.body.appendChild(n)}).observe(document.body,{childList:!0}),document.body.appendChild(n);let o=(0,ex.createRoot)(n,{identifierPrefix:"ndt-"}),a=n.attachShadow({mode:"open"});(0,C.startTransition)(()=>{o.render((0,j.jsx)(ui,{enableCacheIndicator:!1,getOwnerStack:e,getSquashedHydrationErrorDetails:t,isRecoverableError:r,routerType:"pages",shadowRoot:a}))}),uc=!0}}})(),exports.DevOverlayContext=__webpack_exports__.DevOverlayContext,exports.dispatcher=__webpack_exports__.dispatcher,exports.getSegmentTrieData=__webpack_exports__.getSegmentTrieData,exports.getSerializedOverlayState=__webpack_exports__.getSerializedOverlayState,exports.renderAppDevOverlay=__webpack_exports__.renderAppDevOverlay,exports.renderPagesDevOverlay=__webpack_exports__.renderPagesDevOverlay,exports.useDevOverlayContext=__webpack_exports__.useDevOverlayContext,__webpack_exports__)-1===["DevOverlayContext","dispatcher","getSegmentTrieData","getSerializedOverlayState","renderAppDevOverlay","renderPagesDevOverlay","useDevOverlayContext"].indexOf(__rspack_i)&&(exports[__rspack_i]=__webpack_exports__[__rspack_i]);Object.defineProperty(exports,"__esModule",{value:!0});
//# sourceMappingURL=index.js.map
})();
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/safe-stable-stringify/index.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {

(function() {
    "use strict";
    var e = {
        879: function(e, t) {
            const { hasOwnProperty: n } = Object.prototype;
            const r = configure();
            r.configure = configure;
            r.stringify = r;
            r.default = r;
            t.stringify = r;
            t.configure = configure;
            e.exports = r;
            const i = /[\u0000-\u001f\u0022\u005c\ud800-\udfff]/;
            function strEscape(e) {
                if (e.length < 5e3 && !i.test(e)) {
                    return `"${e}"`;
                }
                return JSON.stringify(e);
            }
            function sort(e, t) {
                if (e.length > 200 || t) {
                    return e.sort(t);
                }
                for(let t = 1; t < e.length; t++){
                    const n = e[t];
                    let r = t;
                    while(r !== 0 && e[r - 1] > n){
                        e[r] = e[r - 1];
                        r--;
                    }
                    e[r] = n;
                }
                return e;
            }
            const f = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(Object.getPrototypeOf(new Int8Array)), Symbol.toStringTag).get;
            function isTypedArrayWithEntries(e) {
                return f.call(e) !== undefined && e.length !== 0;
            }
            function stringifyTypedArray(e, t, n) {
                if (e.length < n) {
                    n = e.length;
                }
                const r = t === "," ? "" : " ";
                let i = `"0":${r}${e[0]}`;
                for(let f = 1; f < n; f++){
                    i += `${t}"${f}":${r}${e[f]}`;
                }
                return i;
            }
            function getCircularValueOption(e) {
                if (n.call(e, "circularValue")) {
                    const t = e.circularValue;
                    if (typeof t === "string") {
                        return `"${t}"`;
                    }
                    if (t == null) {
                        return t;
                    }
                    if (t === Error || t === TypeError) {
                        return {
                            toString () {
                                throw new TypeError("Converting circular structure to JSON");
                            }
                        };
                    }
                    throw new TypeError('The "circularValue" argument must be of type string or the value null or undefined');
                }
                return '"[Circular]"';
            }
            function getDeterministicOption(e) {
                let t;
                if (n.call(e, "deterministic")) {
                    t = e.deterministic;
                    if (typeof t !== "boolean" && typeof t !== "function") {
                        throw new TypeError('The "deterministic" argument must be of type boolean or comparator function');
                    }
                }
                return t === undefined ? true : t;
            }
            function getBooleanOption(e, t) {
                let r;
                if (n.call(e, t)) {
                    r = e[t];
                    if (typeof r !== "boolean") {
                        throw new TypeError(`The "${t}" argument must be of type boolean`);
                    }
                }
                return r === undefined ? true : r;
            }
            function getPositiveIntegerOption(e, t) {
                let r;
                if (n.call(e, t)) {
                    r = e[t];
                    if (typeof r !== "number") {
                        throw new TypeError(`The "${t}" argument must be of type number`);
                    }
                    if (!Number.isInteger(r)) {
                        throw new TypeError(`The "${t}" argument must be an integer`);
                    }
                    if (r < 1) {
                        throw new RangeError(`The "${t}" argument must be >= 1`);
                    }
                }
                return r === undefined ? Infinity : r;
            }
            function getItemCount(e) {
                if (e === 1) {
                    return "1 item";
                }
                return `${e} items`;
            }
            function getUniqueReplacerSet(e) {
                const t = new Set;
                for (const n of e){
                    if (typeof n === "string" || typeof n === "number") {
                        t.add(String(n));
                    }
                }
                return t;
            }
            function getStrictOption(e) {
                if (n.call(e, "strict")) {
                    const t = e.strict;
                    if (typeof t !== "boolean") {
                        throw new TypeError('The "strict" argument must be of type boolean');
                    }
                    if (t) {
                        return (e)=>{
                            let t = `Object can not safely be stringified. Received type ${typeof e}`;
                            if (typeof e !== "function") t += ` (${e.toString()})`;
                            throw new Error(t);
                        };
                    }
                }
            }
            function configure(e) {
                e = {
                    ...e
                };
                const t = getStrictOption(e);
                if (t) {
                    if (e.bigint === undefined) {
                        e.bigint = false;
                    }
                    if (!("circularValue" in e)) {
                        e.circularValue = Error;
                    }
                }
                const n = getCircularValueOption(e);
                const r = getBooleanOption(e, "bigint");
                const i = getDeterministicOption(e);
                const f = typeof i === "function" ? i : undefined;
                const u = getPositiveIntegerOption(e, "maximumDepth");
                const o = getPositiveIntegerOption(e, "maximumBreadth");
                function stringifyFnReplacer(e, s, l, c, a, g) {
                    let p = s[e];
                    if (typeof p === "object" && p !== null && typeof p.toJSON === "function") {
                        p = p.toJSON(e);
                    }
                    p = c.call(s, e, p);
                    switch(typeof p){
                        case "string":
                            return strEscape(p);
                        case "object":
                            {
                                if (p === null) {
                                    return "null";
                                }
                                if (l.indexOf(p) !== -1) {
                                    return n;
                                }
                                let e = "";
                                let t = ",";
                                const r = g;
                                if (Array.isArray(p)) {
                                    if (p.length === 0) {
                                        return "[]";
                                    }
                                    if (u < l.length + 1) {
                                        return '"[Array]"';
                                    }
                                    l.push(p);
                                    if (a !== "") {
                                        g += a;
                                        e += `\n${g}`;
                                        t = `,\n${g}`;
                                    }
                                    const n = Math.min(p.length, o);
                                    let i = 0;
                                    for(; i < n - 1; i++){
                                        const n = stringifyFnReplacer(String(i), p, l, c, a, g);
                                        e += n !== undefined ? n : "null";
                                        e += t;
                                    }
                                    const f = stringifyFnReplacer(String(i), p, l, c, a, g);
                                    e += f !== undefined ? f : "null";
                                    if (p.length - 1 > o) {
                                        const n = p.length - o - 1;
                                        e += `${t}"... ${getItemCount(n)} not stringified"`;
                                    }
                                    if (a !== "") {
                                        e += `\n${r}`;
                                    }
                                    l.pop();
                                    return `[${e}]`;
                                }
                                let s = Object.keys(p);
                                const y = s.length;
                                if (y === 0) {
                                    return "{}";
                                }
                                if (u < l.length + 1) {
                                    return '"[Object]"';
                                }
                                let d = "";
                                let h = "";
                                if (a !== "") {
                                    g += a;
                                    t = `,\n${g}`;
                                    d = " ";
                                }
                                const $ = Math.min(y, o);
                                if (i && !isTypedArrayWithEntries(p)) {
                                    s = sort(s, f);
                                }
                                l.push(p);
                                for(let n = 0; n < $; n++){
                                    const r = s[n];
                                    const i = stringifyFnReplacer(r, p, l, c, a, g);
                                    if (i !== undefined) {
                                        e += `${h}${strEscape(r)}:${d}${i}`;
                                        h = t;
                                    }
                                }
                                if (y > o) {
                                    const n = y - o;
                                    e += `${h}"...":${d}"${getItemCount(n)} not stringified"`;
                                    h = t;
                                }
                                if (a !== "" && h.length > 1) {
                                    e = `\n${g}${e}\n${r}`;
                                }
                                l.pop();
                                return `{${e}}`;
                            }
                        case "number":
                            return isFinite(p) ? String(p) : t ? t(p) : "null";
                        case "boolean":
                            return p === true ? "true" : "false";
                        case "undefined":
                            return undefined;
                        case "bigint":
                            if (r) {
                                return String(p);
                            }
                        default:
                            return t ? t(p) : undefined;
                    }
                }
                function stringifyArrayReplacer(e, i, f, s, l, c) {
                    if (typeof i === "object" && i !== null && typeof i.toJSON === "function") {
                        i = i.toJSON(e);
                    }
                    switch(typeof i){
                        case "string":
                            return strEscape(i);
                        case "object":
                            {
                                if (i === null) {
                                    return "null";
                                }
                                if (f.indexOf(i) !== -1) {
                                    return n;
                                }
                                const e = c;
                                let t = "";
                                let r = ",";
                                if (Array.isArray(i)) {
                                    if (i.length === 0) {
                                        return "[]";
                                    }
                                    if (u < f.length + 1) {
                                        return '"[Array]"';
                                    }
                                    f.push(i);
                                    if (l !== "") {
                                        c += l;
                                        t += `\n${c}`;
                                        r = `,\n${c}`;
                                    }
                                    const n = Math.min(i.length, o);
                                    let a = 0;
                                    for(; a < n - 1; a++){
                                        const e = stringifyArrayReplacer(String(a), i[a], f, s, l, c);
                                        t += e !== undefined ? e : "null";
                                        t += r;
                                    }
                                    const g = stringifyArrayReplacer(String(a), i[a], f, s, l, c);
                                    t += g !== undefined ? g : "null";
                                    if (i.length - 1 > o) {
                                        const e = i.length - o - 1;
                                        t += `${r}"... ${getItemCount(e)} not stringified"`;
                                    }
                                    if (l !== "") {
                                        t += `\n${e}`;
                                    }
                                    f.pop();
                                    return `[${t}]`;
                                }
                                f.push(i);
                                let a = "";
                                if (l !== "") {
                                    c += l;
                                    r = `,\n${c}`;
                                    a = " ";
                                }
                                let g = "";
                                for (const e of s){
                                    const n = stringifyArrayReplacer(e, i[e], f, s, l, c);
                                    if (n !== undefined) {
                                        t += `${g}${strEscape(e)}:${a}${n}`;
                                        g = r;
                                    }
                                }
                                if (l !== "" && g.length > 1) {
                                    t = `\n${c}${t}\n${e}`;
                                }
                                f.pop();
                                return `{${t}}`;
                            }
                        case "number":
                            return isFinite(i) ? String(i) : t ? t(i) : "null";
                        case "boolean":
                            return i === true ? "true" : "false";
                        case "undefined":
                            return undefined;
                        case "bigint":
                            if (r) {
                                return String(i);
                            }
                        default:
                            return t ? t(i) : undefined;
                    }
                }
                function stringifyIndent(e, s, l, c, a) {
                    switch(typeof s){
                        case "string":
                            return strEscape(s);
                        case "object":
                            {
                                if (s === null) {
                                    return "null";
                                }
                                if (typeof s.toJSON === "function") {
                                    s = s.toJSON(e);
                                    if (typeof s !== "object") {
                                        return stringifyIndent(e, s, l, c, a);
                                    }
                                    if (s === null) {
                                        return "null";
                                    }
                                }
                                if (l.indexOf(s) !== -1) {
                                    return n;
                                }
                                const t = a;
                                if (Array.isArray(s)) {
                                    if (s.length === 0) {
                                        return "[]";
                                    }
                                    if (u < l.length + 1) {
                                        return '"[Array]"';
                                    }
                                    l.push(s);
                                    a += c;
                                    let e = `\n${a}`;
                                    const n = `,\n${a}`;
                                    const r = Math.min(s.length, o);
                                    let i = 0;
                                    for(; i < r - 1; i++){
                                        const t = stringifyIndent(String(i), s[i], l, c, a);
                                        e += t !== undefined ? t : "null";
                                        e += n;
                                    }
                                    const f = stringifyIndent(String(i), s[i], l, c, a);
                                    e += f !== undefined ? f : "null";
                                    if (s.length - 1 > o) {
                                        const t = s.length - o - 1;
                                        e += `${n}"... ${getItemCount(t)} not stringified"`;
                                    }
                                    e += `\n${t}`;
                                    l.pop();
                                    return `[${e}]`;
                                }
                                let r = Object.keys(s);
                                const g = r.length;
                                if (g === 0) {
                                    return "{}";
                                }
                                if (u < l.length + 1) {
                                    return '"[Object]"';
                                }
                                a += c;
                                const p = `,\n${a}`;
                                let y = "";
                                let d = "";
                                let h = Math.min(g, o);
                                if (isTypedArrayWithEntries(s)) {
                                    y += stringifyTypedArray(s, p, o);
                                    r = r.slice(s.length);
                                    h -= s.length;
                                    d = p;
                                }
                                if (i) {
                                    r = sort(r, f);
                                }
                                l.push(s);
                                for(let e = 0; e < h; e++){
                                    const t = r[e];
                                    const n = stringifyIndent(t, s[t], l, c, a);
                                    if (n !== undefined) {
                                        y += `${d}${strEscape(t)}: ${n}`;
                                        d = p;
                                    }
                                }
                                if (g > o) {
                                    const e = g - o;
                                    y += `${d}"...": "${getItemCount(e)} not stringified"`;
                                    d = p;
                                }
                                if (d !== "") {
                                    y = `\n${a}${y}\n${t}`;
                                }
                                l.pop();
                                return `{${y}}`;
                            }
                        case "number":
                            return isFinite(s) ? String(s) : t ? t(s) : "null";
                        case "boolean":
                            return s === true ? "true" : "false";
                        case "undefined":
                            return undefined;
                        case "bigint":
                            if (r) {
                                return String(s);
                            }
                        default:
                            return t ? t(s) : undefined;
                    }
                }
                function stringifySimple(e, s, l) {
                    switch(typeof s){
                        case "string":
                            return strEscape(s);
                        case "object":
                            {
                                if (s === null) {
                                    return "null";
                                }
                                if (typeof s.toJSON === "function") {
                                    s = s.toJSON(e);
                                    if (typeof s !== "object") {
                                        return stringifySimple(e, s, l);
                                    }
                                    if (s === null) {
                                        return "null";
                                    }
                                }
                                if (l.indexOf(s) !== -1) {
                                    return n;
                                }
                                let t = "";
                                const r = s.length !== undefined;
                                if (r && Array.isArray(s)) {
                                    if (s.length === 0) {
                                        return "[]";
                                    }
                                    if (u < l.length + 1) {
                                        return '"[Array]"';
                                    }
                                    l.push(s);
                                    const e = Math.min(s.length, o);
                                    let n = 0;
                                    for(; n < e - 1; n++){
                                        const e = stringifySimple(String(n), s[n], l);
                                        t += e !== undefined ? e : "null";
                                        t += ",";
                                    }
                                    const r = stringifySimple(String(n), s[n], l);
                                    t += r !== undefined ? r : "null";
                                    if (s.length - 1 > o) {
                                        const e = s.length - o - 1;
                                        t += `,"... ${getItemCount(e)} not stringified"`;
                                    }
                                    l.pop();
                                    return `[${t}]`;
                                }
                                let c = Object.keys(s);
                                const a = c.length;
                                if (a === 0) {
                                    return "{}";
                                }
                                if (u < l.length + 1) {
                                    return '"[Object]"';
                                }
                                let g = "";
                                let p = Math.min(a, o);
                                if (r && isTypedArrayWithEntries(s)) {
                                    t += stringifyTypedArray(s, ",", o);
                                    c = c.slice(s.length);
                                    p -= s.length;
                                    g = ",";
                                }
                                if (i) {
                                    c = sort(c, f);
                                }
                                l.push(s);
                                for(let e = 0; e < p; e++){
                                    const n = c[e];
                                    const r = stringifySimple(n, s[n], l);
                                    if (r !== undefined) {
                                        t += `${g}${strEscape(n)}:${r}`;
                                        g = ",";
                                    }
                                }
                                if (a > o) {
                                    const e = a - o;
                                    t += `${g}"...":"${getItemCount(e)} not stringified"`;
                                }
                                l.pop();
                                return `{${t}}`;
                            }
                        case "number":
                            return isFinite(s) ? String(s) : t ? t(s) : "null";
                        case "boolean":
                            return s === true ? "true" : "false";
                        case "undefined":
                            return undefined;
                        case "bigint":
                            if (r) {
                                return String(s);
                            }
                        default:
                            return t ? t(s) : undefined;
                    }
                }
                function stringify(e, t, n) {
                    if (arguments.length > 1) {
                        let r = "";
                        if (typeof n === "number") {
                            r = " ".repeat(Math.min(n, 10));
                        } else if (typeof n === "string") {
                            r = n.slice(0, 10);
                        }
                        if (t != null) {
                            if (typeof t === "function") {
                                return stringifyFnReplacer("", {
                                    "": e
                                }, [], t, r, "");
                            }
                            if (Array.isArray(t)) {
                                return stringifyArrayReplacer("", e, [], getUniqueReplacerSet(t), r, "");
                            }
                        }
                        if (r.length !== 0) {
                            return stringifyIndent("", e, [], r, "");
                        }
                    }
                    return stringifySimple("", e, []);
                }
                return stringify;
            }
        }
    };
    var t = {};
    function __nccwpck_require__(n) {
        var r = t[n];
        if (r !== undefined) {
            return r.exports;
        }
        var i = t[n] = {
            exports: {}
        };
        var f = true;
        try {
            e[n](i, i.exports, __nccwpck_require__);
            f = false;
        } finally{
            if (f) delete t[n];
        }
        return i.exports;
    }
    if (typeof __nccwpck_require__ !== "undefined") __nccwpck_require__.ab = ("TURBOPACK compile-time value", "/ROOT/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/safe-stable-stringify") + "/";
    var n = __nccwpck_require__(879);
    module.exports = n;
})();
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/strip-ansi/index.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {

(()=>{
    "use strict";
    var e = {
        511: (e)=>{
            e.exports = ({ onlyFirst: e = false } = {})=>{
                const r = [
                    "[\\u001B\\u009B][[\\]()#;?]*(?:(?:(?:(?:;[-a-zA-Z\\d\\/#&.:=?%@~_]+)*|[a-zA-Z\\d]+(?:;[-a-zA-Z\\d\\/#&.:=?%@~_]*)*)?\\u0007)",
                    "(?:(?:\\d{1,4}(?:;\\d{0,4})*)?[\\dA-PR-TZcf-ntqry=><~]))"
                ].join("|");
                return new RegExp(r, e ? undefined : "g");
            };
        },
        532: (e, r, _)=>{
            const t = _(511);
            e.exports = (e)=>typeof e === "string" ? e.replace(t(), "") : e;
        }
    };
    var r = {};
    function __nccwpck_require__(_) {
        var t = r[_];
        if (t !== undefined) {
            return t.exports;
        }
        var a = r[_] = {
            exports: {}
        };
        var n = true;
        try {
            e[_](a, a.exports, __nccwpck_require__);
            n = false;
        } finally{
            if (n) delete r[_];
        }
        return a.exports;
    }
    if (typeof __nccwpck_require__ !== "undefined") __nccwpck_require__.ab = ("TURBOPACK compile-time value", "/ROOT/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/strip-ansi") + "/";
    var _ = __nccwpck_require__(532);
    module.exports = _;
})();
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/stacktrace-parser/stack-trace-parser.cjs.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {

(()=>{
    "use strict";
    if (typeof __nccwpck_require__ !== "undefined") __nccwpck_require__.ab = ("TURBOPACK compile-time value", "/ROOT/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/stacktrace-parser") + "/";
    var e = {};
    (()=>{
        var r = e;
        Object.defineProperty(r, "__esModule", {
            value: true
        });
        var n = "<unknown>";
        function parse(e) {
            var r = e.split("\n");
            return r.reduce(function(e, r) {
                var n = parseChrome(r) || parseWinjs(r) || parseGecko(r) || parseNode(r) || parseJSC(r);
                if (n) {
                    e.push(n);
                }
                return e;
            }, []);
        }
        var a = /^\s*at (.*?) ?\(((?:file|https?|blob|chrome-extension|native|eval|webpack|webpack-internal|rsc|about|turbopack|<anonymous>|\/|[a-z]:\\|\\\\).*?)(?::(\d+))?(?::(\d+))?\)?\s*$/i;
        var u = /\((\S*)(?::(\d+))(?::(\d+))\)/;
        function parseChrome(e) {
            var r = a.exec(e);
            if (!r) {
                return null;
            }
            var l = r[2] && r[2].indexOf("native") === 0;
            var t = r[2] && r[2].indexOf("eval") === 0;
            var i = u.exec(r[2]);
            if (t && i != null) {
                r[2] = i[1];
                r[3] = i[2];
                r[4] = i[3];
            }
            return {
                file: !l ? r[2] : null,
                methodName: r[1] || n,
                arguments: l ? [
                    r[2]
                ] : [],
                lineNumber: r[3] ? +r[3] : null,
                column: r[4] ? +r[4] : null
            };
        }
        var l = /^\s*at (?:((?:\[object object\])?.+) )?\(?((?:file|ms-appx|https?|webpack|webpack-internal|rsc|about|turbopack|blob):.*?):(\d+)(?::(\d+))?\)?\s*$/i;
        function parseWinjs(e) {
            var r = l.exec(e);
            if (!r) {
                return null;
            }
            return {
                file: r[2],
                methodName: r[1] || n,
                arguments: [],
                lineNumber: +r[3],
                column: r[4] ? +r[4] : null
            };
        }
        var t = /^\s*(.*?)(?:\((.*?)\))?(?:^|@)((?:file|https?|blob|chrome|webpack|webpack-internal|rsc|about|turbopack|resource|\[native).*?|[^@]*bundle)(?::(\d+))?(?::(\d+))?\s*$/i;
        var i = /(\S+) line (\d+)(?: > eval line \d+)* > eval/i;
        function parseGecko(e) {
            var r = t.exec(e);
            if (!r) {
                return null;
            }
            var a = r[3] && r[3].indexOf(" > eval") > -1;
            var u = i.exec(r[3]);
            if (a && u != null) {
                r[3] = u[1];
                r[4] = u[2];
                r[5] = null;
            }
            return {
                file: r[3],
                methodName: r[1] || n,
                arguments: r[2] ? r[2].split(",") : [],
                lineNumber: r[4] ? +r[4] : null,
                column: r[5] ? +r[5] : null
            };
        }
        var o = /^\s*(?:([^@]*)(?:\((.*?)\))?@)?(\S.*?):(\d+)(?::(\d+))?\s*$/i;
        function parseJSC(e) {
            var r = o.exec(e);
            if (!r) {
                return null;
            }
            return {
                file: r[3],
                methodName: r[1] || n,
                arguments: [],
                lineNumber: +r[4],
                column: r[5] ? +r[5] : null
            };
        }
        var s = /^\s*at (?:((?:\[object object\])?[^\\/]+(?: \[as \S+\])?) )?\(?(.*?):(\d+)(?::(\d+))?\)?\s*$/i;
        function parseNode(e) {
            var r = s.exec(e);
            if (!r) {
                return null;
            }
            return {
                file: r[2],
                methodName: r[1] || n,
                arguments: [],
                lineNumber: +r[3],
                column: r[4] ? +r[4] : null
            };
        }
        r.parse = parse;
    })();
    module.exports = e;
})();
}),
]);

//# sourceMappingURL=08c5_next_dist_compiled_10o-w6b._.js.map