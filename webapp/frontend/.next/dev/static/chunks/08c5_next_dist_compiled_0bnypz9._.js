(globalThis["TURBOPACK"] || (globalThis["TURBOPACK"] = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/process/browser.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {

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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-refresh/cjs/react-refresh-runtime.development.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-refresh/runtime.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
'use strict';
if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
;
else {
    module.exports = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-refresh/cjs/react-refresh-runtime.development.js [app-client] (ecmascript)");
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/@next/react-refresh-utils/dist/internal/helpers.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
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
const runtime_1 = __importDefault(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-refresh/runtime.js [app-client] (ecmascript)"));
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/@next/react-refresh-utils/dist/runtime.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __importDefault = /*TURBOPACK member replacement*/ __turbopack_context__.e && /*TURBOPACK member replacement*/ __turbopack_context__.e.__importDefault || function(mod) {
    return mod && mod.__esModule ? mod : {
        "default": mod
    };
};
Object.defineProperty(exports, "__esModule", {
    value: true
});
const runtime_1 = __importDefault(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-refresh/runtime.js [app-client] (ecmascript)"));
const helpers_1 = __importDefault(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/@next/react-refresh-utils/dist/internal/helpers.js [app-client] (ecmascript)"));
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/cjs/react.development.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
/**
 * @license React
 * react.development.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */ "use strict";
"production" !== ("TURBOPACK compile-time value", "development") && function() {
    function defineDeprecationWarning(methodName, info) {
        Object.defineProperty(Component.prototype, methodName, {
            get: function() {
                console.warn("%s(...) is deprecated in plain JavaScript React classes. %s", info[0], info[1]);
            }
        });
    }
    function getIteratorFn(maybeIterable) {
        if (null === maybeIterable || "object" !== typeof maybeIterable) return null;
        maybeIterable = MAYBE_ITERATOR_SYMBOL && maybeIterable[MAYBE_ITERATOR_SYMBOL] || maybeIterable["@@iterator"];
        return "function" === typeof maybeIterable ? maybeIterable : null;
    }
    function warnNoop(publicInstance, callerName) {
        publicInstance = (publicInstance = publicInstance.constructor) && (publicInstance.displayName || publicInstance.name) || "ReactClass";
        var warningKey = publicInstance + "." + callerName;
        didWarnStateUpdateForUnmountedComponent[warningKey] || (console.error("Can't call %s on a component that is not yet mounted. This is a no-op, but it might indicate a bug in your application. Instead, assign to `this.state` directly or define a `state = {};` class property with the desired state in the %s component.", callerName, publicInstance), didWarnStateUpdateForUnmountedComponent[warningKey] = !0);
    }
    function Component(props, context, updater) {
        this.props = props;
        this.context = context;
        this.refs = emptyObject;
        this.updater = updater || ReactNoopUpdateQueue;
    }
    function ComponentDummy() {}
    function PureComponent(props, context, updater) {
        this.props = props;
        this.context = context;
        this.refs = emptyObject;
        this.updater = updater || ReactNoopUpdateQueue;
    }
    function noop() {}
    function testStringCoercion(value) {
        return "" + value;
    }
    function checkKeyStringCoercion(value) {
        try {
            testStringCoercion(value);
            var JSCompiler_inline_result = !1;
        } catch (e) {
            JSCompiler_inline_result = !0;
        }
        if (JSCompiler_inline_result) {
            JSCompiler_inline_result = console;
            var JSCompiler_temp_const = JSCompiler_inline_result.error;
            var JSCompiler_inline_result$jscomp$0 = "function" === typeof Symbol && Symbol.toStringTag && value[Symbol.toStringTag] || value.constructor.name || "Object";
            JSCompiler_temp_const.call(JSCompiler_inline_result, "The provided key is an unsupported type %s. This value must be coerced to a string before using it here.", JSCompiler_inline_result$jscomp$0);
            return testStringCoercion(value);
        }
    }
    function getComponentNameFromType(type) {
        if (null == type) return null;
        if ("function" === typeof type) return type.$$typeof === REACT_CLIENT_REFERENCE ? null : type.displayName || type.name || null;
        if ("string" === typeof type) return type;
        switch(type){
            case REACT_FRAGMENT_TYPE:
                return "Fragment";
            case REACT_PROFILER_TYPE:
                return "Profiler";
            case REACT_STRICT_MODE_TYPE:
                return "StrictMode";
            case REACT_SUSPENSE_TYPE:
                return "Suspense";
            case REACT_SUSPENSE_LIST_TYPE:
                return "SuspenseList";
            case REACT_ACTIVITY_TYPE:
                return "Activity";
            case REACT_VIEW_TRANSITION_TYPE:
                return "ViewTransition";
        }
        if ("object" === typeof type) switch("number" === typeof type.tag && console.error("Received an unexpected object in getComponentNameFromType(). This is likely a bug in React. Please file an issue."), type.$$typeof){
            case REACT_PORTAL_TYPE:
                return "Portal";
            case REACT_CONTEXT_TYPE:
                return type.displayName || "Context";
            case REACT_CONSUMER_TYPE:
                return (type._context.displayName || "Context") + ".Consumer";
            case REACT_FORWARD_REF_TYPE:
                var innerType = type.render;
                type = type.displayName;
                type || (type = innerType.displayName || innerType.name || "", type = "" !== type ? "ForwardRef(" + type + ")" : "ForwardRef");
                return type;
            case REACT_MEMO_TYPE:
                return innerType = type.displayName || null, null !== innerType ? innerType : getComponentNameFromType(type.type) || "Memo";
            case REACT_LAZY_TYPE:
                innerType = type._payload;
                type = type._init;
                try {
                    return getComponentNameFromType(type(innerType));
                } catch (x) {}
        }
        return null;
    }
    function getTaskName(type) {
        if (type === REACT_FRAGMENT_TYPE) return "<>";
        if ("object" === typeof type && null !== type && type.$$typeof === REACT_LAZY_TYPE) return "<...>";
        try {
            var name = getComponentNameFromType(type);
            return name ? "<" + name + ">" : "<...>";
        } catch (x) {
            return "<...>";
        }
    }
    function getOwner() {
        var dispatcher = ReactSharedInternals.A;
        return null === dispatcher ? null : dispatcher.getOwner();
    }
    function UnknownOwner() {
        return Error("react-stack-top-frame");
    }
    function hasValidKey(config) {
        if (hasOwnProperty.call(config, "key")) {
            var getter = Object.getOwnPropertyDescriptor(config, "key").get;
            if (getter && getter.isReactWarning) return !1;
        }
        return void 0 !== config.key;
    }
    function defineKeyPropWarningGetter(props, displayName) {
        function warnAboutAccessingKey() {
            specialPropKeyWarningShown || (specialPropKeyWarningShown = !0, console.error("%s: `key` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://react.dev/link/special-props)", displayName));
        }
        warnAboutAccessingKey.isReactWarning = !0;
        Object.defineProperty(props, "key", {
            get: warnAboutAccessingKey,
            configurable: !0
        });
    }
    function elementRefGetterWithDeprecationWarning() {
        var componentName = getComponentNameFromType(this.type);
        didWarnAboutElementRef[componentName] || (didWarnAboutElementRef[componentName] = !0, console.error("Accessing element.ref was removed in React 19. ref is now a regular prop. It will be removed from the JSX Element type in a future release."));
        componentName = this.props.ref;
        return void 0 !== componentName ? componentName : null;
    }
    function ReactElement(type, key, props, owner, debugStack, debugTask) {
        var refProp = props.ref;
        type = {
            $$typeof: REACT_ELEMENT_TYPE,
            type: type,
            key: key,
            props: props,
            _owner: owner
        };
        null !== (void 0 !== refProp ? refProp : null) ? Object.defineProperty(type, "ref", {
            enumerable: !1,
            get: elementRefGetterWithDeprecationWarning
        }) : Object.defineProperty(type, "ref", {
            enumerable: !1,
            value: null
        });
        type._store = {};
        Object.defineProperty(type._store, "validated", {
            configurable: !1,
            enumerable: !1,
            writable: !0,
            value: 0
        });
        Object.defineProperty(type, "_debugInfo", {
            configurable: !1,
            enumerable: !1,
            writable: !0,
            value: null
        });
        Object.defineProperty(type, "_debugStack", {
            configurable: !1,
            enumerable: !1,
            writable: !0,
            value: debugStack
        });
        Object.defineProperty(type, "_debugTask", {
            configurable: !1,
            enumerable: !1,
            writable: !0,
            value: debugTask
        });
        Object.freeze && (Object.freeze(type.props), Object.freeze(type));
        return type;
    }
    function cloneAndReplaceKey(oldElement, newKey) {
        newKey = ReactElement(oldElement.type, newKey, oldElement.props, oldElement._owner, oldElement._debugStack, oldElement._debugTask);
        oldElement._store && (newKey._store.validated = oldElement._store.validated);
        return newKey;
    }
    function validateChildKeys(node) {
        isValidElement(node) ? node._store && (node._store.validated = 1) : "object" === typeof node && null !== node && node.$$typeof === REACT_LAZY_TYPE && ("fulfilled" === node._payload.status ? isValidElement(node._payload.value) && node._payload.value._store && (node._payload.value._store.validated = 1) : node._store && (node._store.validated = 1));
    }
    function isValidElement(object) {
        return "object" === typeof object && null !== object && object.$$typeof === REACT_ELEMENT_TYPE;
    }
    function escape(key) {
        var escaperLookup = {
            "=": "=0",
            ":": "=2"
        };
        return "$" + key.replace(/[=:]/g, function(match) {
            return escaperLookup[match];
        });
    }
    function getElementKey(element, index) {
        return "object" === typeof element && null !== element && null != element.key ? (checkKeyStringCoercion(element.key), escape("" + element.key)) : index.toString(36);
    }
    function resolveThenable(thenable) {
        switch(thenable.status){
            case "fulfilled":
                return thenable.value;
            case "rejected":
                throw thenable.reason;
            default:
                switch("string" === typeof thenable.status ? thenable.then(noop, noop) : (thenable.status = "pending", thenable.then(function(fulfilledValue) {
                    "pending" === thenable.status && (thenable.status = "fulfilled", thenable.value = fulfilledValue);
                }, function(error) {
                    "pending" === thenable.status && (thenable.status = "rejected", thenable.reason = error);
                })), thenable.status){
                    case "fulfilled":
                        return thenable.value;
                    case "rejected":
                        throw thenable.reason;
                }
        }
        throw thenable;
    }
    function mapIntoArray(children, array, escapedPrefix, nameSoFar, callback) {
        var type = typeof children;
        if ("undefined" === type || "boolean" === type) children = null;
        var invokeCallback = !1;
        if (null === children) invokeCallback = !0;
        else switch(type){
            case "bigint":
            case "string":
            case "number":
                invokeCallback = !0;
                break;
            case "object":
                switch(children.$$typeof){
                    case REACT_ELEMENT_TYPE:
                    case REACT_PORTAL_TYPE:
                        invokeCallback = !0;
                        break;
                    case REACT_LAZY_TYPE:
                        return invokeCallback = children._init, mapIntoArray(invokeCallback(children._payload), array, escapedPrefix, nameSoFar, callback);
                }
        }
        if (invokeCallback) {
            invokeCallback = children;
            callback = callback(invokeCallback);
            var childKey = "" === nameSoFar ? "." + getElementKey(invokeCallback, 0) : nameSoFar;
            isArrayImpl(callback) ? (escapedPrefix = "", null != childKey && (escapedPrefix = childKey.replace(userProvidedKeyEscapeRegex, "$&/") + "/"), mapIntoArray(callback, array, escapedPrefix, "", function(c) {
                return c;
            })) : null != callback && (isValidElement(callback) && (null != callback.key && (invokeCallback && invokeCallback.key === callback.key || checkKeyStringCoercion(callback.key)), escapedPrefix = cloneAndReplaceKey(callback, escapedPrefix + (null == callback.key || invokeCallback && invokeCallback.key === callback.key ? "" : ("" + callback.key).replace(userProvidedKeyEscapeRegex, "$&/") + "/") + childKey), "" !== nameSoFar && null != invokeCallback && isValidElement(invokeCallback) && null == invokeCallback.key && invokeCallback._store && !invokeCallback._store.validated && (escapedPrefix._store.validated = 2), callback = escapedPrefix), array.push(callback));
            return 1;
        }
        invokeCallback = 0;
        childKey = "" === nameSoFar ? "." : nameSoFar + ":";
        if (isArrayImpl(children)) for(var i = 0; i < children.length; i++)nameSoFar = children[i], type = childKey + getElementKey(nameSoFar, i), invokeCallback += mapIntoArray(nameSoFar, array, escapedPrefix, type, callback);
        else if (i = getIteratorFn(children), "function" === typeof i) for(i === children.entries && (didWarnAboutMaps || console.warn("Using Maps as children is not supported. Use an array of keyed ReactElements instead."), didWarnAboutMaps = !0), children = i.call(children), i = 0; !(nameSoFar = children.next()).done;)nameSoFar = nameSoFar.value, type = childKey + getElementKey(nameSoFar, i++), invokeCallback += mapIntoArray(nameSoFar, array, escapedPrefix, type, callback);
        else if ("object" === type) {
            if ("function" === typeof children.then) return mapIntoArray(resolveThenable(children), array, escapedPrefix, nameSoFar, callback);
            array = String(children);
            throw Error("Objects are not valid as a React child (found: " + ("[object Object]" === array ? "object with keys {" + Object.keys(children).join(", ") + "}" : array) + "). If you meant to render a collection of children, use an array instead.");
        }
        return invokeCallback;
    }
    function mapChildren(children, func, context) {
        if (null == children) return children;
        var result = [], count = 0;
        mapIntoArray(children, result, "", "", function(child) {
            return func.call(context, child, count++);
        });
        return result;
    }
    function lazyInitializer(payload) {
        if (-1 === payload._status) {
            var resolveDebugValue = null, rejectDebugValue = null, ioInfo = payload._ioInfo;
            null != ioInfo && (ioInfo.start = ioInfo.end = performance.now(), ioInfo.value = new Promise(function(resolve, reject) {
                resolveDebugValue = resolve;
                rejectDebugValue = reject;
            }));
            ioInfo = payload._result;
            var thenable = ioInfo();
            thenable.then(function(moduleObject) {
                if (0 === payload._status || -1 === payload._status) {
                    payload._status = 1;
                    payload._result = moduleObject;
                    var _ioInfo = payload._ioInfo;
                    if (null != _ioInfo) {
                        _ioInfo.end = performance.now();
                        var debugValue = null == moduleObject ? void 0 : moduleObject.default;
                        resolveDebugValue(debugValue);
                        _ioInfo.value.status = "fulfilled";
                        _ioInfo.value.value = debugValue;
                    }
                    void 0 === thenable.status && (thenable.status = "fulfilled", thenable.value = moduleObject);
                }
            }, function(error) {
                if (0 === payload._status || -1 === payload._status) {
                    payload._status = 2;
                    payload._result = error;
                    var _ioInfo2 = payload._ioInfo;
                    null != _ioInfo2 && (_ioInfo2.end = performance.now(), _ioInfo2.value.then(noop, noop), rejectDebugValue(error), _ioInfo2.value.status = "rejected", _ioInfo2.value.reason = error);
                    void 0 === thenable.status && (thenable.status = "rejected", thenable.reason = error);
                }
            });
            ioInfo = payload._ioInfo;
            if (null != ioInfo) {
                var displayName = thenable.displayName;
                "string" === typeof displayName && (ioInfo.name = displayName);
            }
            -1 === payload._status && (payload._status = 0, payload._result = thenable);
        }
        if (1 === payload._status) return ioInfo = payload._result, void 0 === ioInfo && console.error("lazy: Expected the result of a dynamic import() call. Instead received: %s\n\nYour code should look like: \n  const MyComponent = lazy(() => import('./MyComponent'))\n\nDid you accidentally put curly braces around the import?", ioInfo), "default" in ioInfo || console.error("lazy: Expected the result of a dynamic import() call. Instead received: %s\n\nYour code should look like: \n  const MyComponent = lazy(() => import('./MyComponent'))", ioInfo), ioInfo.default;
        throw payload._result;
    }
    function resolveDispatcher() {
        var dispatcher = ReactSharedInternals.H;
        null === dispatcher && console.error("Invalid hook call. Hooks can only be called inside of the body of a function component. This could happen for one of the following reasons:\n1. You might have mismatching versions of React and the renderer (such as React DOM)\n2. You might be breaking the Rules of Hooks\n3. You might have more than one copy of React in the same app\nSee https://react.dev/link/invalid-hook-call for tips about how to debug and fix this problem.");
        return dispatcher;
    }
    function releaseAsyncTransition() {
        ReactSharedInternals.asyncTransitions--;
    }
    function startTransition(scope) {
        var prevTransition = ReactSharedInternals.T, currentTransition = {};
        currentTransition.types = null !== prevTransition ? prevTransition.types : null;
        currentTransition._updatedFibers = new Set();
        ReactSharedInternals.T = currentTransition;
        try {
            var returnValue = scope(), onStartTransitionFinish = ReactSharedInternals.S;
            null !== onStartTransitionFinish && onStartTransitionFinish(currentTransition, returnValue);
            "object" === typeof returnValue && null !== returnValue && "function" === typeof returnValue.then && (ReactSharedInternals.asyncTransitions++, returnValue.then(releaseAsyncTransition, releaseAsyncTransition), returnValue.then(noop, reportGlobalError));
        } catch (error) {
            reportGlobalError(error);
        } finally{
            null === prevTransition && currentTransition._updatedFibers && (scope = currentTransition._updatedFibers.size, currentTransition._updatedFibers.clear(), 10 < scope && console.warn("Detected a large number of updates inside startTransition. If this is due to a subscription please re-write it to use React provided hooks. Otherwise concurrent mode guarantees are off the table.")), null !== prevTransition && null !== currentTransition.types && (null !== prevTransition.types && prevTransition.types !== currentTransition.types && console.error("We expected inner Transitions to have transferred the outer types set and that you cannot add to the outer Transition while inside the inner.This is a bug in React."), prevTransition.types = currentTransition.types), ReactSharedInternals.T = prevTransition;
        }
    }
    function addTransitionType(type) {
        var transition = ReactSharedInternals.T;
        if (null !== transition) {
            var transitionTypes = transition.types;
            null === transitionTypes ? transition.types = [
                type
            ] : -1 === transitionTypes.indexOf(type) && transitionTypes.push(type);
        } else 0 === ReactSharedInternals.asyncTransitions && console.error("addTransitionType can only be called inside a `startTransition()` callback. It must be associated with a specific Transition."), startTransition(addTransitionType.bind(null, type));
    }
    function enqueueTask(task) {
        if (null === enqueueTaskImpl) try {
            var requireString = ("require" + Math.random()).slice(0, 7);
            enqueueTaskImpl = (module && module[requireString]).call(module, "timers").setImmediate;
        } catch (_err) {
            enqueueTaskImpl = function(callback) {
                !1 === didWarnAboutMessageChannel && (didWarnAboutMessageChannel = !0, "undefined" === typeof MessageChannel && console.error("This browser does not have a MessageChannel implementation, so enqueuing tasks via await act(async () => ...) will fail. Please file an issue at https://github.com/facebook/react/issues if you encounter this warning."));
                var channel = new MessageChannel();
                channel.port1.onmessage = callback;
                channel.port2.postMessage(void 0);
            };
        }
        return enqueueTaskImpl(task);
    }
    function aggregateErrors(errors) {
        return 1 < errors.length && "function" === typeof AggregateError ? new AggregateError(errors) : errors[0];
    }
    function popActScope(prevActQueue, prevActScopeDepth) {
        prevActScopeDepth !== actScopeDepth - 1 && console.error("You seem to have overlapping act() calls, this is not supported. Be sure to await previous act() calls before making a new one. ");
        actScopeDepth = prevActScopeDepth;
    }
    function recursivelyFlushAsyncActWork(returnValue, resolve, reject) {
        var queue = ReactSharedInternals.actQueue;
        if (null !== queue) if (0 !== queue.length) try {
            flushActQueue(queue);
            enqueueTask(function() {
                return recursivelyFlushAsyncActWork(returnValue, resolve, reject);
            });
            return;
        } catch (error) {
            ReactSharedInternals.thrownErrors.push(error);
        }
        else ReactSharedInternals.actQueue = null;
        0 < ReactSharedInternals.thrownErrors.length ? (queue = aggregateErrors(ReactSharedInternals.thrownErrors), ReactSharedInternals.thrownErrors.length = 0, reject(queue)) : resolve(returnValue);
    }
    function flushActQueue(queue) {
        if (!isFlushing) {
            isFlushing = !0;
            var i = 0;
            try {
                for(; i < queue.length; i++){
                    var callback = queue[i];
                    do {
                        ReactSharedInternals.didUsePromise = !1;
                        var continuation = callback(!1);
                        if (null !== continuation) {
                            if (ReactSharedInternals.didUsePromise) {
                                queue[i] = callback;
                                queue.splice(0, i);
                                return;
                            }
                            callback = continuation;
                        } else break;
                    }while (1)
                }
                queue.length = 0;
            } catch (error) {
                queue.splice(0, i + 1), ReactSharedInternals.thrownErrors.push(error);
            } finally{
                isFlushing = !1;
            }
        }
    }
    "undefined" !== typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ && "function" === typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart(Error());
    var REACT_ELEMENT_TYPE = Symbol.for("react.transitional.element"), REACT_PORTAL_TYPE = Symbol.for("react.portal"), REACT_FRAGMENT_TYPE = Symbol.for("react.fragment"), REACT_STRICT_MODE_TYPE = Symbol.for("react.strict_mode"), REACT_PROFILER_TYPE = Symbol.for("react.profiler"), REACT_CONSUMER_TYPE = Symbol.for("react.consumer"), REACT_CONTEXT_TYPE = Symbol.for("react.context"), REACT_FORWARD_REF_TYPE = Symbol.for("react.forward_ref"), REACT_SUSPENSE_TYPE = Symbol.for("react.suspense"), REACT_SUSPENSE_LIST_TYPE = Symbol.for("react.suspense_list"), REACT_MEMO_TYPE = Symbol.for("react.memo"), REACT_LAZY_TYPE = Symbol.for("react.lazy"), REACT_ACTIVITY_TYPE = Symbol.for("react.activity"), REACT_VIEW_TRANSITION_TYPE = Symbol.for("react.view_transition"), MAYBE_ITERATOR_SYMBOL = Symbol.iterator, didWarnStateUpdateForUnmountedComponent = {}, ReactNoopUpdateQueue = {
        isMounted: function() {
            return !1;
        },
        enqueueForceUpdate: function(publicInstance) {
            warnNoop(publicInstance, "forceUpdate");
        },
        enqueueReplaceState: function(publicInstance) {
            warnNoop(publicInstance, "replaceState");
        },
        enqueueSetState: function(publicInstance) {
            warnNoop(publicInstance, "setState");
        }
    }, assign = Object.assign, emptyObject = {};
    Object.freeze(emptyObject);
    Component.prototype.isReactComponent = {};
    Component.prototype.setState = function(partialState, callback) {
        if ("object" !== typeof partialState && "function" !== typeof partialState && null != partialState) throw Error("takes an object of state variables to update or a function which returns an object of state variables.");
        this.updater.enqueueSetState(this, partialState, callback, "setState");
    };
    Component.prototype.forceUpdate = function(callback) {
        this.updater.enqueueForceUpdate(this, callback, "forceUpdate");
    };
    var deprecatedAPIs = {
        isMounted: [
            "isMounted",
            "Instead, make sure to clean up subscriptions and pending requests in componentWillUnmount to prevent memory leaks."
        ],
        replaceState: [
            "replaceState",
            "Refactor your code to use setState instead (see https://github.com/facebook/react/issues/3236)."
        ]
    };
    for(fnName in deprecatedAPIs)deprecatedAPIs.hasOwnProperty(fnName) && defineDeprecationWarning(fnName, deprecatedAPIs[fnName]);
    ComponentDummy.prototype = Component.prototype;
    deprecatedAPIs = PureComponent.prototype = new ComponentDummy();
    deprecatedAPIs.constructor = PureComponent;
    assign(deprecatedAPIs, Component.prototype);
    deprecatedAPIs.isPureReactComponent = !0;
    var isArrayImpl = Array.isArray, REACT_CLIENT_REFERENCE = Symbol.for("react.client.reference"), ReactSharedInternals = {
        H: null,
        A: null,
        T: null,
        S: null,
        actQueue: null,
        asyncTransitions: 0,
        isBatchingLegacy: !1,
        didScheduleLegacyUpdate: !1,
        didUsePromise: !1,
        thrownErrors: [],
        getCurrentStack: null,
        recentlyCreatedOwnerStacks: 0
    }, hasOwnProperty = Object.prototype.hasOwnProperty, createTask = console.createTask ? console.createTask : function() {
        return null;
    };
    deprecatedAPIs = {
        react_stack_bottom_frame: function(callStackForError) {
            return callStackForError();
        }
    };
    var specialPropKeyWarningShown, didWarnAboutOldJSXRuntime;
    var didWarnAboutElementRef = {};
    var unknownOwnerDebugStack = deprecatedAPIs.react_stack_bottom_frame.bind(deprecatedAPIs, UnknownOwner)();
    var unknownOwnerDebugTask = createTask(getTaskName(UnknownOwner));
    var didWarnAboutMaps = !1, userProvidedKeyEscapeRegex = /\/+/g, reportGlobalError = "function" === typeof reportError ? reportError : function(error) {
        if ("object" === typeof window && "function" === typeof window.ErrorEvent) {
            var event = new window.ErrorEvent("error", {
                bubbles: !0,
                cancelable: !0,
                message: "object" === typeof error && null !== error && "string" === typeof error.message ? String(error.message) : String(error),
                error: error
            });
            if (!window.dispatchEvent(event)) return;
        } else if ("object" === typeof __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"] && "function" === typeof __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].emit) {
            __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].emit("uncaughtException", error);
            return;
        }
        console.error(error);
    }, didWarnAboutMessageChannel = !1, enqueueTaskImpl = null, actScopeDepth = 0, didWarnNoAwaitAct = !1, isFlushing = !1, queueSeveralMicrotasks = "function" === typeof queueMicrotask ? function(callback) {
        queueMicrotask(function() {
            return queueMicrotask(callback);
        });
    } : enqueueTask;
    deprecatedAPIs = Object.freeze({
        __proto__: null,
        c: function(size) {
            return resolveDispatcher().useMemoCache(size);
        }
    });
    var fnName = {
        map: mapChildren,
        forEach: function(children, forEachFunc, forEachContext) {
            mapChildren(children, function() {
                forEachFunc.apply(this, arguments);
            }, forEachContext);
        },
        count: function(children) {
            var n = 0;
            mapChildren(children, function() {
                n++;
            });
            return n;
        },
        toArray: function(children) {
            return mapChildren(children, function(child) {
                return child;
            }) || [];
        },
        only: function(children) {
            if (!isValidElement(children)) throw Error("React.Children.only expected to receive a single React element child.");
            return children;
        }
    };
    exports.Activity = REACT_ACTIVITY_TYPE;
    exports.Children = fnName;
    exports.Component = Component;
    exports.Fragment = REACT_FRAGMENT_TYPE;
    exports.Profiler = REACT_PROFILER_TYPE;
    exports.PureComponent = PureComponent;
    exports.StrictMode = REACT_STRICT_MODE_TYPE;
    exports.Suspense = REACT_SUSPENSE_TYPE;
    exports.ViewTransition = REACT_VIEW_TRANSITION_TYPE;
    exports.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE = ReactSharedInternals;
    exports.__COMPILER_RUNTIME = deprecatedAPIs;
    exports.act = function(callback) {
        var prevActQueue = ReactSharedInternals.actQueue, prevActScopeDepth = actScopeDepth;
        actScopeDepth++;
        var queue = ReactSharedInternals.actQueue = null !== prevActQueue ? prevActQueue : [], didAwaitActCall = !1;
        try {
            var result = callback();
        } catch (error) {
            ReactSharedInternals.thrownErrors.push(error);
        }
        if (0 < ReactSharedInternals.thrownErrors.length) throw popActScope(prevActQueue, prevActScopeDepth), callback = aggregateErrors(ReactSharedInternals.thrownErrors), ReactSharedInternals.thrownErrors.length = 0, callback;
        if (null !== result && "object" === typeof result && "function" === typeof result.then) {
            var thenable = result;
            queueSeveralMicrotasks(function() {
                didAwaitActCall || didWarnNoAwaitAct || (didWarnNoAwaitAct = !0, console.error("You called act(async () => ...) without await. This could lead to unexpected testing behaviour, interleaving multiple act calls and mixing their scopes. You should - await act(async () => ...);"));
            });
            return {
                then: function(resolve, reject) {
                    didAwaitActCall = !0;
                    thenable.then(function(returnValue) {
                        popActScope(prevActQueue, prevActScopeDepth);
                        if (0 === prevActScopeDepth) {
                            try {
                                flushActQueue(queue), enqueueTask(function() {
                                    return recursivelyFlushAsyncActWork(returnValue, resolve, reject);
                                });
                            } catch (error$0) {
                                ReactSharedInternals.thrownErrors.push(error$0);
                            }
                            if (0 < ReactSharedInternals.thrownErrors.length) {
                                var _thrownError = aggregateErrors(ReactSharedInternals.thrownErrors);
                                ReactSharedInternals.thrownErrors.length = 0;
                                reject(_thrownError);
                            }
                        } else resolve(returnValue);
                    }, function(error) {
                        popActScope(prevActQueue, prevActScopeDepth);
                        0 < ReactSharedInternals.thrownErrors.length ? (error = aggregateErrors(ReactSharedInternals.thrownErrors), ReactSharedInternals.thrownErrors.length = 0, reject(error)) : reject(error);
                    });
                }
            };
        }
        var returnValue$jscomp$0 = result;
        popActScope(prevActQueue, prevActScopeDepth);
        0 === prevActScopeDepth && (flushActQueue(queue), 0 !== queue.length && queueSeveralMicrotasks(function() {
            didAwaitActCall || didWarnNoAwaitAct || (didWarnNoAwaitAct = !0, console.error("A component suspended inside an `act` scope, but the `act` call was not awaited. When testing React components that depend on asynchronous data, you must await the result:\n\nawait act(() => ...)"));
        }), ReactSharedInternals.actQueue = null);
        if (0 < ReactSharedInternals.thrownErrors.length) throw callback = aggregateErrors(ReactSharedInternals.thrownErrors), ReactSharedInternals.thrownErrors.length = 0, callback;
        return {
            then: function(resolve, reject) {
                didAwaitActCall = !0;
                0 === prevActScopeDepth ? (ReactSharedInternals.actQueue = queue, enqueueTask(function() {
                    return recursivelyFlushAsyncActWork(returnValue$jscomp$0, resolve, reject);
                })) : resolve(returnValue$jscomp$0);
            }
        };
    };
    exports.addTransitionType = addTransitionType;
    exports.cache = function(fn) {
        return function() {
            return fn.apply(null, arguments);
        };
    };
    exports.cacheSignal = function() {
        return null;
    };
    exports.captureOwnerStack = function() {
        var getCurrentStack = ReactSharedInternals.getCurrentStack;
        return null === getCurrentStack ? null : getCurrentStack();
    };
    exports.cloneElement = function(element, config, children) {
        if (null === element || void 0 === element) throw Error("The argument must be a React element, but you passed " + element + ".");
        var props = assign({}, element.props), key = element.key, owner = element._owner;
        if (null != config) {
            var JSCompiler_inline_result;
            a: {
                if (hasOwnProperty.call(config, "ref") && (JSCompiler_inline_result = Object.getOwnPropertyDescriptor(config, "ref").get) && JSCompiler_inline_result.isReactWarning) {
                    JSCompiler_inline_result = !1;
                    break a;
                }
                JSCompiler_inline_result = void 0 !== config.ref;
            }
            JSCompiler_inline_result && (owner = getOwner());
            hasValidKey(config) && (checkKeyStringCoercion(config.key), key = "" + config.key);
            for(propName in config)!hasOwnProperty.call(config, propName) || "key" === propName || "__self" === propName || "__source" === propName || "ref" === propName && void 0 === config.ref || (props[propName] = config[propName]);
        }
        var propName = arguments.length - 2;
        if (1 === propName) props.children = children;
        else if (1 < propName) {
            JSCompiler_inline_result = Array(propName);
            for(var i = 0; i < propName; i++)JSCompiler_inline_result[i] = arguments[i + 2];
            props.children = JSCompiler_inline_result;
        }
        props = ReactElement(element.type, key, props, owner, element._debugStack, element._debugTask);
        for(key = 2; key < arguments.length; key++)validateChildKeys(arguments[key]);
        return props;
    };
    exports.createContext = function(defaultValue) {
        defaultValue = {
            $$typeof: REACT_CONTEXT_TYPE,
            _currentValue: defaultValue,
            _currentValue2: defaultValue,
            _threadCount: 0,
            Provider: null,
            Consumer: null
        };
        defaultValue.Provider = defaultValue;
        defaultValue.Consumer = {
            $$typeof: REACT_CONSUMER_TYPE,
            _context: defaultValue
        };
        defaultValue._currentRenderer = null;
        defaultValue._currentRenderer2 = null;
        return defaultValue;
    };
    exports.createElement = function(type, config, children) {
        for(var i = 2; i < arguments.length; i++)validateChildKeys(arguments[i]);
        var propName;
        i = {};
        var key = null;
        if (null != config) for(propName in didWarnAboutOldJSXRuntime || !("__self" in config) || "key" in config || (didWarnAboutOldJSXRuntime = !0, console.warn("Your app (or one of its dependencies) is using an outdated JSX transform. Update to the modern JSX transform for faster performance: https://react.dev/link/new-jsx-transform")), hasValidKey(config) && (checkKeyStringCoercion(config.key), key = "" + config.key), config)hasOwnProperty.call(config, propName) && "key" !== propName && "__self" !== propName && "__source" !== propName && (i[propName] = config[propName]);
        var childrenLength = arguments.length - 2;
        if (1 === childrenLength) i.children = children;
        else if (1 < childrenLength) {
            for(var childArray = Array(childrenLength), _i = 0; _i < childrenLength; _i++)childArray[_i] = arguments[_i + 2];
            Object.freeze && Object.freeze(childArray);
            i.children = childArray;
        }
        if (type && type.defaultProps) for(propName in childrenLength = type.defaultProps, childrenLength)void 0 === i[propName] && (i[propName] = childrenLength[propName]);
        key && defineKeyPropWarningGetter(i, "function" === typeof type ? type.displayName || type.name || "Unknown" : type);
        (propName = 1e4 > ReactSharedInternals.recentlyCreatedOwnerStacks++) ? (childArray = Error.stackTraceLimit, Error.stackTraceLimit = 10, childrenLength = Error("react-stack-top-frame"), Error.stackTraceLimit = childArray) : childrenLength = unknownOwnerDebugStack;
        return ReactElement(type, key, i, getOwner(), childrenLength, propName ? createTask(getTaskName(type)) : unknownOwnerDebugTask);
    };
    exports.createRef = function() {
        var refObject = {
            current: null
        };
        Object.seal(refObject);
        return refObject;
    };
    exports.forwardRef = function(render) {
        null != render && render.$$typeof === REACT_MEMO_TYPE ? console.error("forwardRef requires a render function but received a `memo` component. Instead of forwardRef(memo(...)), use memo(forwardRef(...)).") : "function" !== typeof render ? console.error("forwardRef requires a render function but was given %s.", null === render ? "null" : typeof render) : 0 !== render.length && 2 !== render.length && console.error("forwardRef render functions accept exactly two parameters: props and ref. %s", 1 === render.length ? "Did you forget to use the ref parameter?" : "Any additional parameter will be undefined.");
        null != render && null != render.defaultProps && console.error("forwardRef render functions do not support defaultProps. Did you accidentally pass a React component?");
        var elementType = {
            $$typeof: REACT_FORWARD_REF_TYPE,
            render: render
        }, ownName;
        Object.defineProperty(elementType, "displayName", {
            enumerable: !1,
            configurable: !0,
            get: function() {
                return ownName;
            },
            set: function(name) {
                ownName = name;
                render.name || render.displayName || (Object.defineProperty(render, "name", {
                    value: name
                }), render.displayName = name);
            }
        });
        return elementType;
    };
    exports.isValidElement = isValidElement;
    exports.lazy = function(ctor) {
        ctor = {
            _status: -1,
            _result: ctor
        };
        var lazyType = {
            $$typeof: REACT_LAZY_TYPE,
            _payload: ctor,
            _init: lazyInitializer
        }, ioInfo = {
            name: "lazy",
            start: -1,
            end: -1,
            value: null,
            owner: null,
            debugStack: Error("react-stack-top-frame"),
            debugTask: console.createTask ? console.createTask("lazy()") : null
        };
        ctor._ioInfo = ioInfo;
        lazyType._debugInfo = [
            {
                awaited: ioInfo
            }
        ];
        return lazyType;
    };
    exports.memo = function(type, compare) {
        null == type && console.error("memo: The first argument must be a component. Instead received: %s", null === type ? "null" : typeof type);
        compare = {
            $$typeof: REACT_MEMO_TYPE,
            type: type,
            compare: void 0 === compare ? null : compare
        };
        var ownName;
        Object.defineProperty(compare, "displayName", {
            enumerable: !1,
            configurable: !0,
            get: function() {
                return ownName;
            },
            set: function(name) {
                ownName = name;
                type.name || type.displayName || (Object.defineProperty(type, "name", {
                    value: name
                }), type.displayName = name);
            }
        });
        return compare;
    };
    exports.startTransition = startTransition;
    exports.unstable_useCacheRefresh = function() {
        return resolveDispatcher().useCacheRefresh();
    };
    exports.use = function(usable) {
        return resolveDispatcher().use(usable);
    };
    exports.useActionState = function(action, initialState, permalink) {
        return resolveDispatcher().useActionState(action, initialState, permalink);
    };
    exports.useCallback = function(callback, deps) {
        return resolveDispatcher().useCallback(callback, deps);
    };
    exports.useContext = function(Context) {
        var dispatcher = resolveDispatcher();
        Context.$$typeof === REACT_CONSUMER_TYPE && console.error("Calling useContext(Context.Consumer) is not supported and will cause bugs. Did you mean to call useContext(Context) instead?");
        return dispatcher.useContext(Context);
    };
    exports.useDebugValue = function(value, formatterFn) {
        return resolveDispatcher().useDebugValue(value, formatterFn);
    };
    exports.useDeferredValue = function(value, initialValue) {
        return resolveDispatcher().useDeferredValue(value, initialValue);
    };
    exports.useEffect = function(create, deps) {
        null == create && console.warn("React Hook useEffect requires an effect callback. Did you forget to pass a callback to the hook?");
        return resolveDispatcher().useEffect(create, deps);
    };
    exports.useEffectEvent = function(callback) {
        return resolveDispatcher().useEffectEvent(callback);
    };
    exports.useId = function() {
        return resolveDispatcher().useId();
    };
    exports.useImperativeHandle = function(ref, create, deps) {
        return resolveDispatcher().useImperativeHandle(ref, create, deps);
    };
    exports.useInsertionEffect = function(create, deps) {
        null == create && console.warn("React Hook useInsertionEffect requires an effect callback. Did you forget to pass a callback to the hook?");
        return resolveDispatcher().useInsertionEffect(create, deps);
    };
    exports.useLayoutEffect = function(create, deps) {
        null == create && console.warn("React Hook useLayoutEffect requires an effect callback. Did you forget to pass a callback to the hook?");
        return resolveDispatcher().useLayoutEffect(create, deps);
    };
    exports.useMemo = function(create, deps) {
        return resolveDispatcher().useMemo(create, deps);
    };
    exports.useOptimistic = function(passthrough, reducer) {
        return resolveDispatcher().useOptimistic(passthrough, reducer);
    };
    exports.useReducer = function(reducer, initialArg, init) {
        return resolveDispatcher().useReducer(reducer, initialArg, init);
    };
    exports.useRef = function(initialValue) {
        return resolveDispatcher().useRef(initialValue);
    };
    exports.useState = function(initialState) {
        return resolveDispatcher().useState(initialState);
    };
    exports.useSyncExternalStore = function(subscribe, getSnapshot, getServerSnapshot) {
        return resolveDispatcher().useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
    };
    exports.useTransition = function() {
        return resolveDispatcher().useTransition();
    };
    exports.version = "19.3.0-canary-3f0b9e61-20260317";
    "undefined" !== typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ && "function" === typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop(Error());
}();
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
'use strict';
if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
;
else {
    module.exports = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/cjs/react.development.js [app-client] (ecmascript)");
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/cjs/react-jsx-runtime.development.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
/**
 * @license React
 * react-jsx-runtime.development.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */ "use strict";
"production" !== ("TURBOPACK compile-time value", "development") && function() {
    function getComponentNameFromType(type) {
        if (null == type) return null;
        if ("function" === typeof type) return type.$$typeof === REACT_CLIENT_REFERENCE ? null : type.displayName || type.name || null;
        if ("string" === typeof type) return type;
        switch(type){
            case REACT_FRAGMENT_TYPE:
                return "Fragment";
            case REACT_PROFILER_TYPE:
                return "Profiler";
            case REACT_STRICT_MODE_TYPE:
                return "StrictMode";
            case REACT_SUSPENSE_TYPE:
                return "Suspense";
            case REACT_SUSPENSE_LIST_TYPE:
                return "SuspenseList";
            case REACT_ACTIVITY_TYPE:
                return "Activity";
            case REACT_VIEW_TRANSITION_TYPE:
                return "ViewTransition";
        }
        if ("object" === typeof type) switch("number" === typeof type.tag && console.error("Received an unexpected object in getComponentNameFromType(). This is likely a bug in React. Please file an issue."), type.$$typeof){
            case REACT_PORTAL_TYPE:
                return "Portal";
            case REACT_CONTEXT_TYPE:
                return type.displayName || "Context";
            case REACT_CONSUMER_TYPE:
                return (type._context.displayName || "Context") + ".Consumer";
            case REACT_FORWARD_REF_TYPE:
                var innerType = type.render;
                type = type.displayName;
                type || (type = innerType.displayName || innerType.name || "", type = "" !== type ? "ForwardRef(" + type + ")" : "ForwardRef");
                return type;
            case REACT_MEMO_TYPE:
                return innerType = type.displayName || null, null !== innerType ? innerType : getComponentNameFromType(type.type) || "Memo";
            case REACT_LAZY_TYPE:
                innerType = type._payload;
                type = type._init;
                try {
                    return getComponentNameFromType(type(innerType));
                } catch (x) {}
        }
        return null;
    }
    function testStringCoercion(value) {
        return "" + value;
    }
    function checkKeyStringCoercion(value) {
        try {
            testStringCoercion(value);
            var JSCompiler_inline_result = !1;
        } catch (e) {
            JSCompiler_inline_result = !0;
        }
        if (JSCompiler_inline_result) {
            JSCompiler_inline_result = console;
            var JSCompiler_temp_const = JSCompiler_inline_result.error;
            var JSCompiler_inline_result$jscomp$0 = "function" === typeof Symbol && Symbol.toStringTag && value[Symbol.toStringTag] || value.constructor.name || "Object";
            JSCompiler_temp_const.call(JSCompiler_inline_result, "The provided key is an unsupported type %s. This value must be coerced to a string before using it here.", JSCompiler_inline_result$jscomp$0);
            return testStringCoercion(value);
        }
    }
    function getTaskName(type) {
        if (type === REACT_FRAGMENT_TYPE) return "<>";
        if ("object" === typeof type && null !== type && type.$$typeof === REACT_LAZY_TYPE) return "<...>";
        try {
            var name = getComponentNameFromType(type);
            return name ? "<" + name + ">" : "<...>";
        } catch (x) {
            return "<...>";
        }
    }
    function getOwner() {
        var dispatcher = ReactSharedInternals.A;
        return null === dispatcher ? null : dispatcher.getOwner();
    }
    function UnknownOwner() {
        return Error("react-stack-top-frame");
    }
    function hasValidKey(config) {
        if (hasOwnProperty.call(config, "key")) {
            var getter = Object.getOwnPropertyDescriptor(config, "key").get;
            if (getter && getter.isReactWarning) return !1;
        }
        return void 0 !== config.key;
    }
    function defineKeyPropWarningGetter(props, displayName) {
        function warnAboutAccessingKey() {
            specialPropKeyWarningShown || (specialPropKeyWarningShown = !0, console.error("%s: `key` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://react.dev/link/special-props)", displayName));
        }
        warnAboutAccessingKey.isReactWarning = !0;
        Object.defineProperty(props, "key", {
            get: warnAboutAccessingKey,
            configurable: !0
        });
    }
    function elementRefGetterWithDeprecationWarning() {
        var componentName = getComponentNameFromType(this.type);
        didWarnAboutElementRef[componentName] || (didWarnAboutElementRef[componentName] = !0, console.error("Accessing element.ref was removed in React 19. ref is now a regular prop. It will be removed from the JSX Element type in a future release."));
        componentName = this.props.ref;
        return void 0 !== componentName ? componentName : null;
    }
    function ReactElement(type, key, props, owner, debugStack, debugTask) {
        var refProp = props.ref;
        type = {
            $$typeof: REACT_ELEMENT_TYPE,
            type: type,
            key: key,
            props: props,
            _owner: owner
        };
        null !== (void 0 !== refProp ? refProp : null) ? Object.defineProperty(type, "ref", {
            enumerable: !1,
            get: elementRefGetterWithDeprecationWarning
        }) : Object.defineProperty(type, "ref", {
            enumerable: !1,
            value: null
        });
        type._store = {};
        Object.defineProperty(type._store, "validated", {
            configurable: !1,
            enumerable: !1,
            writable: !0,
            value: 0
        });
        Object.defineProperty(type, "_debugInfo", {
            configurable: !1,
            enumerable: !1,
            writable: !0,
            value: null
        });
        Object.defineProperty(type, "_debugStack", {
            configurable: !1,
            enumerable: !1,
            writable: !0,
            value: debugStack
        });
        Object.defineProperty(type, "_debugTask", {
            configurable: !1,
            enumerable: !1,
            writable: !0,
            value: debugTask
        });
        Object.freeze && (Object.freeze(type.props), Object.freeze(type));
        return type;
    }
    function jsxDEVImpl(type, config, maybeKey, isStaticChildren, debugStack, debugTask) {
        var children = config.children;
        if (void 0 !== children) if (isStaticChildren) if (isArrayImpl(children)) {
            for(isStaticChildren = 0; isStaticChildren < children.length; isStaticChildren++)validateChildKeys(children[isStaticChildren]);
            Object.freeze && Object.freeze(children);
        } else console.error("React.jsx: Static children should always be an array. You are likely explicitly calling React.jsxs or React.jsxDEV. Use the Babel transform instead.");
        else validateChildKeys(children);
        if (hasOwnProperty.call(config, "key")) {
            children = getComponentNameFromType(type);
            var keys = Object.keys(config).filter(function(k) {
                return "key" !== k;
            });
            isStaticChildren = 0 < keys.length ? "{key: someKey, " + keys.join(": ..., ") + ": ...}" : "{key: someKey}";
            didWarnAboutKeySpread[children + isStaticChildren] || (keys = 0 < keys.length ? "{" + keys.join(": ..., ") + ": ...}" : "{}", console.error('A props object containing a "key" prop is being spread into JSX:\n  let props = %s;\n  <%s {...props} />\nReact keys must be passed directly to JSX without using spread:\n  let props = %s;\n  <%s key={someKey} {...props} />', isStaticChildren, children, keys, children), didWarnAboutKeySpread[children + isStaticChildren] = !0);
        }
        children = null;
        void 0 !== maybeKey && (checkKeyStringCoercion(maybeKey), children = "" + maybeKey);
        hasValidKey(config) && (checkKeyStringCoercion(config.key), children = "" + config.key);
        if ("key" in config) {
            maybeKey = {};
            for(var propName in config)"key" !== propName && (maybeKey[propName] = config[propName]);
        } else maybeKey = config;
        children && defineKeyPropWarningGetter(maybeKey, "function" === typeof type ? type.displayName || type.name || "Unknown" : type);
        return ReactElement(type, children, maybeKey, getOwner(), debugStack, debugTask);
    }
    function validateChildKeys(node) {
        isValidElement(node) ? node._store && (node._store.validated = 1) : "object" === typeof node && null !== node && node.$$typeof === REACT_LAZY_TYPE && ("fulfilled" === node._payload.status ? isValidElement(node._payload.value) && node._payload.value._store && (node._payload.value._store.validated = 1) : node._store && (node._store.validated = 1));
    }
    function isValidElement(object) {
        return "object" === typeof object && null !== object && object.$$typeof === REACT_ELEMENT_TYPE;
    }
    var React = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)"), REACT_ELEMENT_TYPE = Symbol.for("react.transitional.element"), REACT_PORTAL_TYPE = Symbol.for("react.portal"), REACT_FRAGMENT_TYPE = Symbol.for("react.fragment"), REACT_STRICT_MODE_TYPE = Symbol.for("react.strict_mode"), REACT_PROFILER_TYPE = Symbol.for("react.profiler"), REACT_CONSUMER_TYPE = Symbol.for("react.consumer"), REACT_CONTEXT_TYPE = Symbol.for("react.context"), REACT_FORWARD_REF_TYPE = Symbol.for("react.forward_ref"), REACT_SUSPENSE_TYPE = Symbol.for("react.suspense"), REACT_SUSPENSE_LIST_TYPE = Symbol.for("react.suspense_list"), REACT_MEMO_TYPE = Symbol.for("react.memo"), REACT_LAZY_TYPE = Symbol.for("react.lazy"), REACT_ACTIVITY_TYPE = Symbol.for("react.activity"), REACT_VIEW_TRANSITION_TYPE = Symbol.for("react.view_transition"), REACT_CLIENT_REFERENCE = Symbol.for("react.client.reference"), ReactSharedInternals = React.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE, hasOwnProperty = Object.prototype.hasOwnProperty, isArrayImpl = Array.isArray, createTask = console.createTask ? console.createTask : function() {
        return null;
    };
    React = {
        react_stack_bottom_frame: function(callStackForError) {
            return callStackForError();
        }
    };
    var specialPropKeyWarningShown;
    var didWarnAboutElementRef = {};
    var unknownOwnerDebugStack = React.react_stack_bottom_frame.bind(React, UnknownOwner)();
    var unknownOwnerDebugTask = createTask(getTaskName(UnknownOwner));
    var didWarnAboutKeySpread = {};
    exports.Fragment = REACT_FRAGMENT_TYPE;
    exports.jsx = function(type, config, maybeKey) {
        var trackActualOwner = 1e4 > ReactSharedInternals.recentlyCreatedOwnerStacks++;
        if (trackActualOwner) {
            var previousStackTraceLimit = Error.stackTraceLimit;
            Error.stackTraceLimit = 10;
            var debugStackDEV = Error("react-stack-top-frame");
            Error.stackTraceLimit = previousStackTraceLimit;
        } else debugStackDEV = unknownOwnerDebugStack;
        return jsxDEVImpl(type, config, maybeKey, !1, debugStackDEV, trackActualOwner ? createTask(getTaskName(type)) : unknownOwnerDebugTask);
    };
    exports.jsxs = function(type, config, maybeKey) {
        var trackActualOwner = 1e4 > ReactSharedInternals.recentlyCreatedOwnerStacks++;
        if (trackActualOwner) {
            var previousStackTraceLimit = Error.stackTraceLimit;
            Error.stackTraceLimit = 10;
            var debugStackDEV = Error("react-stack-top-frame");
            Error.stackTraceLimit = previousStackTraceLimit;
        } else debugStackDEV = unknownOwnerDebugStack;
        return jsxDEVImpl(type, config, maybeKey, !0, debugStackDEV, trackActualOwner ? createTask(getTaskName(type)) : unknownOwnerDebugTask);
    };
}();
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/jsx-runtime.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
'use strict';
if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
;
else {
    module.exports = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/cjs/react-jsx-runtime.development.js [app-client] (ecmascript)");
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/safe-stable-stringify/index.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {

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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/scheduler/cjs/scheduler.development.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
/**
 * @license React
 * scheduler.development.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */ "use strict";
"production" !== ("TURBOPACK compile-time value", "development") && function() {
    function performWorkUntilDeadline() {
        needsPaint = !1;
        if (isMessageLoopRunning) {
            var currentTime = exports.unstable_now();
            startTime = currentTime;
            var hasMoreWork = !0;
            try {
                a: {
                    isHostCallbackScheduled = !1;
                    isHostTimeoutScheduled && (isHostTimeoutScheduled = !1, localClearTimeout(taskTimeoutID), taskTimeoutID = -1);
                    isPerformingWork = !0;
                    var previousPriorityLevel = currentPriorityLevel;
                    try {
                        b: {
                            advanceTimers(currentTime);
                            for(currentTask = peek(taskQueue); null !== currentTask && !(currentTask.expirationTime > currentTime && shouldYieldToHost());){
                                var callback = currentTask.callback;
                                if ("function" === typeof callback) {
                                    currentTask.callback = null;
                                    currentPriorityLevel = currentTask.priorityLevel;
                                    var continuationCallback = callback(currentTask.expirationTime <= currentTime);
                                    currentTime = exports.unstable_now();
                                    if ("function" === typeof continuationCallback) {
                                        currentTask.callback = continuationCallback;
                                        advanceTimers(currentTime);
                                        hasMoreWork = !0;
                                        break b;
                                    }
                                    currentTask === peek(taskQueue) && pop(taskQueue);
                                    advanceTimers(currentTime);
                                } else pop(taskQueue);
                                currentTask = peek(taskQueue);
                            }
                            if (null !== currentTask) hasMoreWork = !0;
                            else {
                                var firstTimer = peek(timerQueue);
                                null !== firstTimer && requestHostTimeout(handleTimeout, firstTimer.startTime - currentTime);
                                hasMoreWork = !1;
                            }
                        }
                        break a;
                    } finally{
                        currentTask = null, currentPriorityLevel = previousPriorityLevel, isPerformingWork = !1;
                    }
                    hasMoreWork = void 0;
                }
            } finally{
                hasMoreWork ? schedulePerformWorkUntilDeadline() : isMessageLoopRunning = !1;
            }
        }
    }
    function push(heap, node) {
        var index = heap.length;
        heap.push(node);
        a: for(; 0 < index;){
            var parentIndex = index - 1 >>> 1, parent = heap[parentIndex];
            if (0 < compare(parent, node)) heap[parentIndex] = node, heap[index] = parent, index = parentIndex;
            else break a;
        }
    }
    function peek(heap) {
        return 0 === heap.length ? null : heap[0];
    }
    function pop(heap) {
        if (0 === heap.length) return null;
        var first = heap[0], last = heap.pop();
        if (last !== first) {
            heap[0] = last;
            a: for(var index = 0, length = heap.length, halfLength = length >>> 1; index < halfLength;){
                var leftIndex = 2 * (index + 1) - 1, left = heap[leftIndex], rightIndex = leftIndex + 1, right = heap[rightIndex];
                if (0 > compare(left, last)) rightIndex < length && 0 > compare(right, left) ? (heap[index] = right, heap[rightIndex] = last, index = rightIndex) : (heap[index] = left, heap[leftIndex] = last, index = leftIndex);
                else if (rightIndex < length && 0 > compare(right, last)) heap[index] = right, heap[rightIndex] = last, index = rightIndex;
                else break a;
            }
        }
        return first;
    }
    function compare(a, b) {
        var diff = a.sortIndex - b.sortIndex;
        return 0 !== diff ? diff : a.id - b.id;
    }
    function advanceTimers(currentTime) {
        for(var timer = peek(timerQueue); null !== timer;){
            if (null === timer.callback) pop(timerQueue);
            else if (timer.startTime <= currentTime) pop(timerQueue), timer.sortIndex = timer.expirationTime, push(taskQueue, timer);
            else break;
            timer = peek(timerQueue);
        }
    }
    function handleTimeout(currentTime) {
        isHostTimeoutScheduled = !1;
        advanceTimers(currentTime);
        if (!isHostCallbackScheduled) if (null !== peek(taskQueue)) isHostCallbackScheduled = !0, isMessageLoopRunning || (isMessageLoopRunning = !0, schedulePerformWorkUntilDeadline());
        else {
            var firstTimer = peek(timerQueue);
            null !== firstTimer && requestHostTimeout(handleTimeout, firstTimer.startTime - currentTime);
        }
    }
    function shouldYieldToHost() {
        return needsPaint ? !0 : exports.unstable_now() - startTime < frameInterval ? !1 : !0;
    }
    function requestHostTimeout(callback, ms) {
        taskTimeoutID = localSetTimeout(function() {
            callback(exports.unstable_now());
        }, ms);
    }
    "undefined" !== typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ && "function" === typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart(Error());
    exports.unstable_now = void 0;
    if ("object" === typeof performance && "function" === typeof performance.now) {
        var localPerformance = performance;
        exports.unstable_now = function() {
            return localPerformance.now();
        };
    } else {
        var localDate = Date, initialTime = localDate.now();
        exports.unstable_now = function() {
            return localDate.now() - initialTime;
        };
    }
    var taskQueue = [], timerQueue = [], taskIdCounter = 1, currentTask = null, currentPriorityLevel = 3, isPerformingWork = !1, isHostCallbackScheduled = !1, isHostTimeoutScheduled = !1, needsPaint = !1, localSetTimeout = "function" === typeof setTimeout ? setTimeout : null, localClearTimeout = "function" === typeof clearTimeout ? clearTimeout : null, localSetImmediate = "undefined" !== typeof setImmediate ? setImmediate : null, isMessageLoopRunning = !1, taskTimeoutID = -1, frameInterval = 5, startTime = -1;
    if ("function" === typeof localSetImmediate) var schedulePerformWorkUntilDeadline = function() {
        localSetImmediate(performWorkUntilDeadline);
    };
    else if ("undefined" !== typeof MessageChannel) {
        var channel = new MessageChannel(), port = channel.port2;
        channel.port1.onmessage = performWorkUntilDeadline;
        schedulePerformWorkUntilDeadline = function() {
            port.postMessage(null);
        };
    } else schedulePerformWorkUntilDeadline = function() {
        localSetTimeout(performWorkUntilDeadline, 0);
    };
    exports.unstable_IdlePriority = 5;
    exports.unstable_ImmediatePriority = 1;
    exports.unstable_LowPriority = 4;
    exports.unstable_NormalPriority = 3;
    exports.unstable_Profiling = null;
    exports.unstable_UserBlockingPriority = 2;
    exports.unstable_cancelCallback = function(task) {
        task.callback = null;
    };
    exports.unstable_forceFrameRate = function(fps) {
        0 > fps || 125 < fps ? console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported") : frameInterval = 0 < fps ? Math.floor(1e3 / fps) : 5;
    };
    exports.unstable_getCurrentPriorityLevel = function() {
        return currentPriorityLevel;
    };
    exports.unstable_next = function(eventHandler) {
        switch(currentPriorityLevel){
            case 1:
            case 2:
            case 3:
                var priorityLevel = 3;
                break;
            default:
                priorityLevel = currentPriorityLevel;
        }
        var previousPriorityLevel = currentPriorityLevel;
        currentPriorityLevel = priorityLevel;
        try {
            return eventHandler();
        } finally{
            currentPriorityLevel = previousPriorityLevel;
        }
    };
    exports.unstable_requestPaint = function() {
        needsPaint = !0;
    };
    exports.unstable_runWithPriority = function(priorityLevel, eventHandler) {
        switch(priorityLevel){
            case 1:
            case 2:
            case 3:
            case 4:
            case 5:
                break;
            default:
                priorityLevel = 3;
        }
        var previousPriorityLevel = currentPriorityLevel;
        currentPriorityLevel = priorityLevel;
        try {
            return eventHandler();
        } finally{
            currentPriorityLevel = previousPriorityLevel;
        }
    };
    exports.unstable_scheduleCallback = function(priorityLevel, callback, options) {
        var currentTime = exports.unstable_now();
        "object" === typeof options && null !== options ? (options = options.delay, options = "number" === typeof options && 0 < options ? currentTime + options : currentTime) : options = currentTime;
        switch(priorityLevel){
            case 1:
                var timeout = -1;
                break;
            case 2:
                timeout = 250;
                break;
            case 5:
                timeout = 1073741823;
                break;
            case 4:
                timeout = 1e4;
                break;
            default:
                timeout = 5e3;
        }
        timeout = options + timeout;
        priorityLevel = {
            id: taskIdCounter++,
            callback: callback,
            priorityLevel: priorityLevel,
            startTime: options,
            expirationTime: timeout,
            sortIndex: -1
        };
        options > currentTime ? (priorityLevel.sortIndex = options, push(timerQueue, priorityLevel), null === peek(taskQueue) && priorityLevel === peek(timerQueue) && (isHostTimeoutScheduled ? (localClearTimeout(taskTimeoutID), taskTimeoutID = -1) : isHostTimeoutScheduled = !0, requestHostTimeout(handleTimeout, options - currentTime))) : (priorityLevel.sortIndex = timeout, push(taskQueue, priorityLevel), isHostCallbackScheduled || isPerformingWork || (isHostCallbackScheduled = !0, isMessageLoopRunning || (isMessageLoopRunning = !0, schedulePerformWorkUntilDeadline())));
        return priorityLevel;
    };
    exports.unstable_shouldYield = shouldYieldToHost;
    exports.unstable_wrapCallback = function(callback) {
        var parentPriorityLevel = currentPriorityLevel;
        return function() {
            var previousPriorityLevel = currentPriorityLevel;
            currentPriorityLevel = parentPriorityLevel;
            try {
                return callback.apply(this, arguments);
            } finally{
                currentPriorityLevel = previousPriorityLevel;
            }
        };
    };
    "undefined" !== typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ && "function" === typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop(Error());
}();
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/scheduler/index.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
'use strict';
if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
;
else {
    module.exports = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/scheduler/cjs/scheduler.development.js [app-client] (ecmascript)");
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/strip-ansi/index.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {

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
]);

//# sourceMappingURL=08c5_next_dist_compiled_0bnypz9._.js.map