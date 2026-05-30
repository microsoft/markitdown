(globalThis["TURBOPACK"] || (globalThis["TURBOPACK"] = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/register-deployment-id-global.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
const _deploymentid = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/deployment-id.js [client] (ecmascript)");
const deploymentId = (0, _deploymentid.getDeploymentId)();
globalThis.NEXT_DEPLOYMENT_ID = deploymentId;
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/portal/index.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "Portal", {
    enumerable: true,
    get: function() {
        return Portal;
    }
});
const _react = __turbopack_context__.r("[project]/node_modules/.pnpm/react@19.2.6/node_modules/react/index.js [client] (ecmascript)");
const _reactdom = __turbopack_context__.r("[project]/node_modules/.pnpm/react-dom@19.2.6_react@19.2.6/node_modules/react-dom/index.js [client] (ecmascript)");
const Portal = ({ children, type })=>{
    const [portalNode, setPortalNode] = (0, _react.useState)(null);
    (0, _react.useEffect)(()=>{
        const element = document.createElement(type);
        document.body.appendChild(element);
        setPortalNode(element);
        return ()=>{
            document.body.removeChild(element);
        };
    }, [
        type
    ]);
    return portalNode ? /*#__PURE__*/ (0, _reactdom.createPortal)(children, portalNode) : null;
};
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/set-attributes-from-props.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "setAttributesFromProps", {
    enumerable: true,
    get: function() {
        return setAttributesFromProps;
    }
});
const DOMAttributeNames = {
    acceptCharset: 'accept-charset',
    className: 'class',
    htmlFor: 'for',
    httpEquiv: 'http-equiv',
    noModule: 'noModule'
};
const ignoreProps = [
    'onLoad',
    'onReady',
    'dangerouslySetInnerHTML',
    'children',
    'onError',
    'strategy',
    'stylesheets'
];
function isBooleanScriptAttribute(attr) {
    return [
        'async',
        'defer',
        'noModule'
    ].includes(attr);
}
function setAttributesFromProps(el, props) {
    for (const [p, value] of Object.entries(props)){
        if (!props.hasOwnProperty(p)) continue;
        if (ignoreProps.includes(p)) continue;
        // we don't render undefined props to the DOM
        if (value === undefined) {
            continue;
        }
        const attr = DOMAttributeNames[p] || p.toLowerCase();
        if (el.tagName === 'SCRIPT' && isBooleanScriptAttribute(attr)) {
            // Correctly assign boolean script attributes
            // https://github.com/vercel/next.js/pull/20748
            ;
            el[attr] = !!value;
        } else {
            el.setAttribute(attr, String(value));
        }
        // Remove falsy non-zero boolean attributes so they are correctly interpreted
        // (e.g. if we set them to false, this coerces to the string "false", which the browser interprets as true)
        if (value === false || el.tagName === 'SCRIPT' && isBooleanScriptAttribute(attr) && (!value || value === 'false')) {
            // Call setAttribute before, as we need to set and unset the attribute to override force async:
            // https://html.spec.whatwg.org/multipage/scripting.html#script-force-async
            el.setAttribute(attr, '');
            el.removeAttribute(attr);
        }
    }
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/head-manager.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    default: null,
    isEqualNode: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    default: function() {
        return initHeadManager;
    },
    isEqualNode: function() {
        return isEqualNode;
    }
});
const _setattributesfromprops = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/set-attributes-from-props.js [client] (ecmascript)");
function reactElementToDOM({ type, props }) {
    const el = document.createElement(type);
    (0, _setattributesfromprops.setAttributesFromProps)(el, props);
    const { children, dangerouslySetInnerHTML } = props;
    if (dangerouslySetInnerHTML) {
        el.innerHTML = dangerouslySetInnerHTML.__html || '';
    } else if (children) {
        el.textContent = typeof children === 'string' ? children : Array.isArray(children) ? children.join('') : '';
    }
    return el;
}
function isEqualNode(oldTag, newTag) {
    if (oldTag instanceof HTMLElement && newTag instanceof HTMLElement) {
        const nonce = newTag.getAttribute('nonce');
        // Only strip the nonce if `oldTag` has had it stripped. An element's nonce attribute will not
        // be stripped if there is no content security policy response header that includes a nonce.
        if (nonce && !oldTag.getAttribute('nonce')) {
            const cloneTag = newTag.cloneNode(true);
            cloneTag.setAttribute('nonce', '');
            cloneTag.nonce = nonce;
            return nonce === oldTag.nonce && oldTag.isEqualNode(cloneTag);
        }
    }
    return oldTag.isEqualNode(newTag);
}
function updateElements(type, components) {
    const headEl = document.querySelector('head');
    if (!headEl) return;
    const oldTags = new Set(headEl.querySelectorAll(`${type}[data-next-head]`));
    if (type === 'meta') {
        const metaCharset = headEl.querySelector('meta[charset]');
        if (metaCharset !== null) {
            oldTags.add(metaCharset);
        }
    }
    const newTags = [];
    for(let i = 0; i < components.length; i++){
        const component = components[i];
        const newTag = reactElementToDOM(component);
        newTag.setAttribute('data-next-head', '');
        let isNew = true;
        for (const oldTag of oldTags){
            if (isEqualNode(oldTag, newTag)) {
                oldTags.delete(oldTag);
                isNew = false;
                break;
            }
        }
        if (isNew) {
            newTags.push(newTag);
        }
    }
    for (const oldTag of oldTags){
        oldTag.parentNode?.removeChild(oldTag);
    }
    for (const newTag of newTags){
        // meta[charset] must be first element so special case
        if (newTag.tagName.toLowerCase() === 'meta' && newTag.getAttribute('charset') !== null) {
            headEl.prepend(newTag);
        }
        headEl.appendChild(newTag);
    }
}
function initHeadManager() {
    return {
        mountedInstances: new Set(),
        updateHead: (head)=>{
            const tags = {};
            head.forEach((h)=>{
                if (// it won't be inlined. In this case revert to the original behavior
                h.type === 'link' && h.props['data-optimized-fonts']) {
                    if (document.querySelector(`style[data-href="${h.props['data-href']}"]`)) {
                        return;
                    } else {
                        h.props.href = h.props['data-href'];
                        h.props['data-href'] = undefined;
                    }
                }
                const components = tags[h.type] || [];
                components.push(h);
                tags[h.type] = components;
            });
            const titleComponent = tags.title ? tags.title[0] : null;
            let title = '';
            if (titleComponent) {
                const { children } = titleComponent.props;
                title = typeof children === 'string' ? children : Array.isArray(children) ? children.join('') : '';
            }
            if (title !== document.title) document.title = title;
            [
                'meta',
                'base',
                'link',
                'style',
                'script'
            ].forEach((type)=>{
                updateElements(type, tags[type] || []);
            });
        }
    };
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/normalize-trailing-slash.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "normalizePathTrailingSlash", {
    enumerable: true,
    get: function() {
        return normalizePathTrailingSlash;
    }
});
const _removetrailingslash = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/remove-trailing-slash.js [client] (ecmascript)");
const _parsepath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/parse-path.js [client] (ecmascript)");
const normalizePathTrailingSlash = (path)=>{
    if (!path.startsWith('/') || ("TURBOPACK compile-time value", void 0)) {
        return path;
    }
    const { pathname, query, hash } = (0, _parsepath.parsePath)(path);
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    return `${(0, _removetrailingslash.removeTrailingSlash)(pathname)}${query}${hash}`;
};
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/add-base-path.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "addBasePath", {
    enumerable: true,
    get: function() {
        return addBasePath;
    }
});
const _addpathprefix = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/add-path-prefix.js [client] (ecmascript)");
const _normalizetrailingslash = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/normalize-trailing-slash.js [client] (ecmascript)");
const basePath = ("TURBOPACK compile-time value", "") || '';
function addBasePath(path, required) {
    return (0, _normalizetrailingslash.normalizePathTrailingSlash)(("TURBOPACK compile-time falsy", 0) ? "TURBOPACK unreachable" : (0, _addpathprefix.addPathPrefix)(path, basePath));
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/add-locale.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "addLocale", {
    enumerable: true,
    get: function() {
        return addLocale;
    }
});
const _normalizetrailingslash = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/normalize-trailing-slash.js [client] (ecmascript)");
const addLocale = (path, ...args)=>{
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    return path;
};
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/trusted-types.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

/**
 * Stores the Trusted Types Policy. Starts as undefined and can be set to null
 * if Trusted Types is not supported in the browser.
 */ Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "__unsafeCreateTrustedScriptURL", {
    enumerable: true,
    get: function() {
        return __unsafeCreateTrustedScriptURL;
    }
});
let policy;
/**
 * Getter for the Trusted Types Policy. If it is undefined, it is instantiated
 * here or set to null if Trusted Types is not supported in the browser.
 */ function getPolicy() {
    if (typeof policy === 'undefined' && typeof window !== 'undefined') {
        policy = window.trustedTypes?.createPolicy('nextjs', {
            createHTML: (input)=>input,
            createScript: (input)=>input,
            createScriptURL: (input)=>input
        }) || null;
    }
    return policy;
}
function __unsafeCreateTrustedScriptURL(url) {
    return getPolicy()?.createScriptURL(url) || url;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/request-idle-callback.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    cancelIdleCallback: null,
    requestIdleCallback: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    cancelIdleCallback: function() {
        return cancelIdleCallback;
    },
    requestIdleCallback: function() {
        return requestIdleCallback;
    }
});
const requestIdleCallback = typeof self !== 'undefined' && self.requestIdleCallback && self.requestIdleCallback.bind(window) || function(cb) {
    let start = Date.now();
    return self.setTimeout(function() {
        cb({
            didTimeout: false,
            timeRemaining: function() {
                return Math.max(0, 50 - (Date.now() - start));
            }
        });
    }, 1);
};
const cancelIdleCallback = typeof self !== 'undefined' && self.cancelIdleCallback && self.cancelIdleCallback.bind(window) || function(id) {
    return clearTimeout(id);
};
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/lib/promise.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "resolvePromiseWithTimeout", {
    enumerable: true,
    get: function() {
        return resolvePromiseWithTimeout;
    }
});
const _requestidlecallback = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/request-idle-callback.js [client] (ecmascript)");
// 3.8s was arbitrarily chosen as it's what https://web.dev/interactive
// considers as "Good" time-to-interactive. We must assume something went
// wrong beyond this point, and then fall-back to a full page transition to
// show the user something of value.
const MS_MAX_IDLE_DELAY = 3800;
function resolvePromiseWithTimeout(p, err, devPromise) {
    return new Promise((resolve, reject)=>{
        let cancelled = false;
        p.then((r)=>{
            // Resolved, cancel the timeout
            cancelled = true;
            resolve(r);
        }).catch(reject);
        // We wrap these checks separately for better dead-code elimination in
        // production bundles.
        if ("TURBOPACK compile-time truthy", 1) {
            ;
            (devPromise || Promise.resolve()).then(()=>{
                (0, _requestidlecallback.requestIdleCallback)(()=>setTimeout(()=>{
                        if (!cancelled) {
                            reject(err);
                        }
                    }, MS_MAX_IDLE_DELAY));
            });
        }
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
    });
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/route-loader.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    createRouteLoader: null,
    getClientBuildManifest: null,
    isAssetError: null,
    markAssetError: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    createRouteLoader: function() {
        return createRouteLoader;
    },
    getClientBuildManifest: function() {
        return getClientBuildManifest;
    },
    isAssetError: function() {
        return isAssetError;
    },
    markAssetError: function() {
        return markAssetError;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [client] (ecmascript)");
const _getassetpathfromroute = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/get-asset-path-from-route.js [client] (ecmascript)"));
const _trustedtypes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/trusted-types.js [client] (ecmascript)");
const _requestidlecallback = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/request-idle-callback.js [client] (ecmascript)");
const _deploymentid = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/deployment-id.js [client] (ecmascript)");
const _encodeuripath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/encode-uri-path.js [client] (ecmascript)");
const _promise = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/lib/promise.js [client] (ecmascript)");
function withFuture(key, map, generator) {
    let entry = map.get(key);
    if (entry) {
        if ('future' in entry) {
            return entry.future;
        }
        return Promise.resolve(entry);
    }
    let resolver;
    const prom = new Promise((resolve)=>{
        resolver = resolve;
    });
    map.set(key, {
        resolve: resolver,
        future: prom
    });
    return generator ? generator().then((value)=>{
        resolver(value);
        return value;
    }).catch((err)=>{
        map.delete(key);
        throw err;
    }) : prom;
}
const ASSET_LOAD_ERROR = Symbol('ASSET_LOAD_ERROR');
function markAssetError(err) {
    return Object.defineProperty(err, ASSET_LOAD_ERROR, {});
}
function isAssetError(err) {
    return err && ASSET_LOAD_ERROR in err;
}
function hasPrefetch(link) {
    try {
        link = document.createElement('link');
        return(// with relList.support
        !!window.MSInputMethodContext && !!document.documentMode || link.relList.supports('prefetch'));
    } catch  {
        return false;
    }
}
const canPrefetch = hasPrefetch();
function prefetchViaDom(href, as, link) {
    return new Promise((resolve, reject)=>{
        const selector = `
      link[rel="prefetch"][href^="${href}"],
      link[rel="preload"][href^="${href}"],
      script[src^="${href}"]`;
        if (document.querySelector(selector)) {
            return resolve();
        }
        link = document.createElement('link');
        // The order of property assignment here is intentional:
        if (as) link.as = as;
        link.rel = `prefetch`;
        link.crossOrigin = ("TURBOPACK compile-time value", void 0);
        link.onload = resolve;
        link.onerror = ()=>reject(markAssetError(Object.defineProperty(new Error(`Failed to prefetch: ${href}`), "__NEXT_ERROR_CODE", {
                value: "E268",
                enumerable: false,
                configurable: true
            })));
        // `href` should always be last:
        link.href = href;
        document.head.appendChild(link);
    });
}
function appendScript(src, script) {
    return new Promise((resolve, reject)=>{
        script = document.createElement('script');
        // The order of property assignment here is intentional.
        // 1. Setup success/failure hooks in case the browser synchronously
        //    executes when `src` is set.
        script.onload = resolve;
        script.onerror = ()=>reject(markAssetError(Object.defineProperty(new Error(`Failed to load script: ${src}`), "__NEXT_ERROR_CODE", {
                value: "E74",
                enumerable: false,
                configurable: true
            })));
        // 2. Configure the cross-origin attribute before setting `src` in case the
        //    browser begins to fetch.
        script.crossOrigin = ("TURBOPACK compile-time value", void 0);
        // 3. Finally, set the source and inject into the DOM in case the child
        //    must be appended for fetching to start.
        script.src = src;
        document.body.appendChild(script);
    });
}
// We wait for pages to be built in dev before we start the route transition
// timeout to prevent an un-necessary hard navigation in development.
let devBuildPromise;
function getClientBuildManifest() {
    if (self.__BUILD_MANIFEST) {
        return Promise.resolve(self.__BUILD_MANIFEST);
    }
    const onBuildManifest = new Promise((resolve)=>{
        // Mandatory because this is not concurrent safe:
        const cb = self.__BUILD_MANIFEST_CB;
        self.__BUILD_MANIFEST_CB = ()=>{
            resolve(self.__BUILD_MANIFEST);
            cb && cb();
        };
    });
    return (0, _promise.resolvePromiseWithTimeout)(onBuildManifest, markAssetError(Object.defineProperty(new Error('Failed to load client build manifest'), "__NEXT_ERROR_CODE", {
        value: "E273",
        enumerable: false,
        configurable: true
    })), devBuildPromise);
}
function getFilesForRoute(assetPrefix, route) {
    if ("TURBOPACK compile-time truthy", 1) {
        const scriptUrl = assetPrefix + '/_next/static/chunks/pages' + (0, _encodeuripath.encodeURIPath)((0, _getassetpathfromroute.default)(route, '.js')) + (0, _deploymentid.getAssetTokenQuery)();
        return Promise.resolve({
            scripts: [
                (0, _trustedtypes.__unsafeCreateTrustedScriptURL)(scriptUrl)
            ],
            // Styles are handled by `style-loader` in development:
            css: []
        });
    }
    //TURBOPACK unreachable
    ;
}
function createRouteLoader(assetPrefix) {
    const entrypoints = new Map();
    const loadedScripts = new Map();
    const styleSheets = new Map();
    const routes = new Map();
    function maybeExecuteScript(src) {
        // With HMR we might need to "reload" scripts when they are
        // disposed and readded. Executing scripts twice has no functional
        // differences
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
        else {
            return appendScript(src);
        }
    }
    function fetchStyleSheet(href) {
        let prom = styleSheets.get(href);
        if (prom) {
            return prom;
        }
        styleSheets.set(href, prom = fetch(href, {
            credentials: 'same-origin'
        }).then((res)=>{
            if (!res.ok) {
                throw Object.defineProperty(new Error(`Failed to load stylesheet: ${href}`), "__NEXT_ERROR_CODE", {
                    value: "E189",
                    enumerable: false,
                    configurable: true
                });
            }
            return res.text().then((text)=>({
                    href: href,
                    content: text
                }));
        }).catch((err)=>{
            throw markAssetError(err);
        }));
        return prom;
    }
    return {
        whenEntrypoint (route) {
            return withFuture(route, entrypoints);
        },
        onEntrypoint (route, execute) {
            ;
            (execute ? Promise.resolve().then(()=>execute()).then((exports1)=>({
                    component: exports1 && exports1.default || exports1,
                    exports: exports1
                }), (err)=>({
                    error: err
                })) : Promise.resolve(undefined)).then((input)=>{
                const old = entrypoints.get(route);
                if (old && 'resolve' in old) {
                    if (input) {
                        entrypoints.set(route, input);
                        old.resolve(input);
                    }
                } else {
                    if (input) {
                        entrypoints.set(route, input);
                    } else {
                        entrypoints.delete(route);
                    }
                    // when this entrypoint has been resolved before
                    // the route is outdated and we want to invalidate
                    // this cache entry
                    routes.delete(route);
                }
            });
        },
        loadRoute (route, prefetch) {
            return withFuture(route, routes, ()=>{
                let devBuildPromiseResolve;
                if ("TURBOPACK compile-time truthy", 1) {
                    devBuildPromise = new Promise((resolve)=>{
                        devBuildPromiseResolve = resolve;
                    });
                }
                return (0, _promise.resolvePromiseWithTimeout)(getFilesForRoute(assetPrefix, route).then(({ scripts, css })=>{
                    return Promise.all([
                        entrypoints.has(route) ? [] : Promise.all(scripts.map(maybeExecuteScript)),
                        Promise.all(css.map(fetchStyleSheet))
                    ]);
                }).then((res)=>{
                    return this.whenEntrypoint(route).then((entrypoint)=>({
                            entrypoint,
                            styles: res[1]
                        }));
                }), markAssetError(Object.defineProperty(new Error(`Route did not complete loading: ${route}`), "__NEXT_ERROR_CODE", {
                    value: "E12",
                    enumerable: false,
                    configurable: true
                })), devBuildPromise).then(({ entrypoint, styles })=>{
                    const res = Object.assign({
                        styles: styles
                    }, entrypoint);
                    return 'error' in entrypoint ? entrypoint : res;
                }).catch((err)=>{
                    if (prefetch) {
                        // we don't want to cache errors during prefetch
                        throw err;
                    }
                    return {
                        error: err
                    };
                }).finally(()=>devBuildPromiseResolve?.());
            });
        },
        prefetch (route) {
            // https://github.com/GoogleChromeLabs/quicklink/blob/453a661fa1fa940e2d2e044452398e38c67a98fb/src/index.mjs#L115-L118
            // License: Apache 2.0
            let cn;
            if (cn = navigator.connection) {
                // Don't prefetch if using 2G or if Save-Data is enabled.
                if (cn.saveData || /2g/.test(cn.effectiveType)) return Promise.resolve();
            }
            return getFilesForRoute(assetPrefix, route).then((output)=>Promise.all(canPrefetch ? output.scripts.map((script)=>prefetchViaDom(script.toString(), 'script')) : [])).then(()=>{
                (0, _requestidlecallback.requestIdleCallback)(()=>this.loadRoute(route, true).catch(()=>{}));
            }).catch(()=>{});
        }
    };
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/page-loader.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "default", {
    enumerable: true,
    get: function() {
        return PageLoader;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [client] (ecmascript)");
const _addbasepath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/add-base-path.js [client] (ecmascript)");
const _interpolateas = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/interpolate-as.js [client] (ecmascript)");
const _getassetpathfromroute = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/get-asset-path-from-route.js [client] (ecmascript)"));
const _addlocale = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/add-locale.js [client] (ecmascript)");
const _isdynamic = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/is-dynamic.js [client] (ecmascript)");
const _parserelativeurl = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/parse-relative-url.js [client] (ecmascript)");
const _removetrailingslash = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/remove-trailing-slash.js [client] (ecmascript)");
const _routeloader = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/route-loader.js [client] (ecmascript)");
const _constants = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/constants.js [client] (ecmascript)");
const _promise = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/lib/promise.js [client] (ecmascript)");
class PageLoader {
    constructor(buildId, assetPrefix){
        this.routeLoader = (0, _routeloader.createRouteLoader)(assetPrefix);
        this.buildId = buildId;
        this.assetPrefix = assetPrefix;
        this.promisedSsgManifest = new Promise((resolve)=>{
            if (window.__SSG_MANIFEST) {
                resolve(window.__SSG_MANIFEST);
            } else {
                window.__SSG_MANIFEST_CB = ()=>{
                    resolve(window.__SSG_MANIFEST);
                };
            }
        });
    }
    getPageList() {
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
        else {
            if (window.__DEV_PAGES_MANIFEST) {
                return window.__DEV_PAGES_MANIFEST.pages;
            } else {
                this.promisedDevPagesManifest ||= fetch(`${this.assetPrefix}/_next/static/development/${_constants.DEV_CLIENT_PAGES_MANIFEST}`, {
                    credentials: 'same-origin'
                }).then((res)=>res.json()).then((manifest)=>{
                    window.__DEV_PAGES_MANIFEST = manifest;
                    return manifest.pages;
                }).catch((err)=>{
                    console.log(`Failed to fetch devPagesManifest:`, err);
                    throw Object.defineProperty(new Error(`Failed to fetch _devPagesManifest.json. Is something blocking that network request?\n` + 'Read more: https://nextjs.org/docs/messages/failed-to-fetch-devpagesmanifest'), "__NEXT_ERROR_CODE", {
                        value: "E423",
                        enumerable: false,
                        configurable: true
                    });
                });
                return this.promisedDevPagesManifest;
            }
        }
    }
    getMiddleware() {
        // Webpack production
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
        else if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
        else {
            if (window.__DEV_MIDDLEWARE_MATCHERS) {
                return window.__DEV_MIDDLEWARE_MATCHERS;
            } else {
                if (!this.promisedMiddlewareMatchers) {
                    // TODO: Decide what should happen when fetching fails instead of asserting
                    // @ts-ignore
                    this.promisedMiddlewareMatchers = fetch(`${this.assetPrefix}/_next/static/${this.buildId}/${_constants.DEV_CLIENT_MIDDLEWARE_MANIFEST}`, {
                        credentials: 'same-origin'
                    }).then((res)=>res.json()).then((matchers)=>{
                        window.__DEV_MIDDLEWARE_MATCHERS = matchers;
                        return matchers;
                    }).catch((err)=>{
                        console.log(`Failed to fetch _devMiddlewareManifest`, err);
                    });
                }
                // TODO Remove this assertion as this could be undefined
                return this.promisedMiddlewareMatchers;
            }
        }
    }
    getDataHref(params) {
        const { asPath, href, locale } = params;
        const { pathname: hrefPathname, query, search } = (0, _parserelativeurl.parseRelativeUrl)(href);
        const { pathname: asPathname } = (0, _parserelativeurl.parseRelativeUrl)(asPath);
        const route = (0, _removetrailingslash.removeTrailingSlash)(hrefPathname);
        if (route[0] !== '/') {
            throw Object.defineProperty(new Error(`Route name should start with a "/", got "${route}"`), "__NEXT_ERROR_CODE", {
                value: "E303",
                enumerable: false,
                configurable: true
            });
        }
        const getHrefForSlug = (path)=>{
            const dataRoute = (0, _getassetpathfromroute.default)((0, _removetrailingslash.removeTrailingSlash)((0, _addlocale.addLocale)(path, locale)), '.json');
            return (0, _addbasepath.addBasePath)(`/_next/data/${this.buildId}${dataRoute}${search}`, true);
        };
        return getHrefForSlug(params.skipInterpolation ? asPathname : (0, _isdynamic.isDynamicRoute)(route) ? (0, _interpolateas.interpolateAs)(hrefPathname, asPathname, query).result : route);
    }
    _isSsg(/** the route (file-system path) */ route) {
        return this.promisedSsgManifest.then((manifest)=>manifest.has(route));
    }
    loadPage(route) {
        return this.routeLoader.loadRoute(route).then((res)=>{
            if ('component' in res) {
                return {
                    page: res.component,
                    mod: res.exports,
                    styleSheets: res.styles.map((o)=>({
                            href: o.href,
                            text: o.content
                        }))
                };
            }
            throw res.error;
        });
    }
    prefetch(route) {
        return this.routeLoader.prefetch(route);
    }
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/script.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    default: null,
    handleClientScriptLoad: null,
    initScriptLoader: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    default: function() {
        return _default;
    },
    handleClientScriptLoad: function() {
        return handleClientScriptLoad;
    },
    initScriptLoader: function() {
        return initScriptLoader;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [client] (ecmascript)");
const _interop_require_wildcard = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_wildcard.cjs [client] (ecmascript)");
const _jsxruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/react@19.2.6/node_modules/react/jsx-runtime.js [client] (ecmascript)");
const _reactdom = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/react-dom@19.2.6_react@19.2.6/node_modules/react-dom/index.js [client] (ecmascript)"));
const _react = /*#__PURE__*/ _interop_require_wildcard._(__turbopack_context__.r("[project]/node_modules/.pnpm/react@19.2.6/node_modules/react/index.js [client] (ecmascript)"));
const _headmanagercontextsharedruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/head-manager-context.shared-runtime.js [client] (ecmascript)");
const _setattributesfromprops = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/set-attributes-from-props.js [client] (ecmascript)");
const _requestidlecallback = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/request-idle-callback.js [client] (ecmascript)");
const _htmlescape = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/htmlescape.js [client] (ecmascript)");
const ScriptCache = new Map();
const LoadCache = new Set();
const insertStylesheets = (stylesheets)=>{
    // Case 1: Styles for afterInteractive/lazyOnload with appDir injected via handleClientScriptLoad
    //
    // Using ReactDOM.preinit to feature detect appDir and inject styles
    // Stylesheets might have already been loaded if initialized with Script component
    // Re-inject styles here to handle scripts loaded via handleClientScriptLoad
    // ReactDOM.preinit handles dedup and ensures the styles are loaded only once
    if (_reactdom.default.preinit) {
        stylesheets.forEach((stylesheet)=>{
            _reactdom.default.preinit(stylesheet, {
                as: 'style'
            });
        });
        return;
    }
    // Case 2: Styles for afterInteractive/lazyOnload with pages injected via handleClientScriptLoad
    //
    // We use this function to load styles when appdir is not detected
    // TODO: Use React float APIs to load styles once available for pages dir
    if (typeof window !== 'undefined') {
        let head = document.head;
        stylesheets.forEach((stylesheet)=>{
            let link = document.createElement('link');
            link.type = 'text/css';
            link.rel = 'stylesheet';
            link.href = stylesheet;
            head.appendChild(link);
        });
    }
};
const loadScript = (props)=>{
    const { src, id, onLoad = ()=>{}, onReady = null, dangerouslySetInnerHTML, children = '', strategy = 'afterInteractive', onError, stylesheets } = props;
    const cacheKey = id || src;
    // Script has already loaded
    if (cacheKey && LoadCache.has(cacheKey)) {
        return;
    }
    // Contents of this script are already loading/loaded
    if (ScriptCache.has(src)) {
        LoadCache.add(cacheKey);
        // It is possible that multiple `next/script` components all have same "src", but has different "onLoad"
        // This is to make sure the same remote script will only load once, but "onLoad" are executed in order
        ScriptCache.get(src).then(onLoad, onError);
        return;
    }
    /** Execute after the script first loaded */ const afterLoad = ()=>{
        // Run onReady for the first time after load event
        if (onReady) {
            onReady();
        }
        // add cacheKey to LoadCache when load successfully
        LoadCache.add(cacheKey);
    };
    const el = document.createElement('script');
    const loadPromise = new Promise((resolve, reject)=>{
        el.addEventListener('load', function(e) {
            resolve();
            if (onLoad) {
                onLoad.call(this, e);
            }
            afterLoad();
        });
        el.addEventListener('error', function(e) {
            reject(e);
        });
    }).catch(function(e) {
        if (onError) {
            onError(e);
        }
    });
    if (dangerouslySetInnerHTML) {
        // Casting since lib.dom.d.ts doesn't have TrustedHTML yet.
        el.innerHTML = dangerouslySetInnerHTML.__html || '';
        afterLoad();
    } else if (children) {
        el.textContent = typeof children === 'string' ? children : Array.isArray(children) ? children.join('') : '';
        afterLoad();
    } else if (src) {
        el.src = src;
        // do not add cacheKey into LoadCache for remote script here
        // cacheKey will be added to LoadCache when it is actually loaded (see loadPromise above)
        ScriptCache.set(src, loadPromise);
    }
    (0, _setattributesfromprops.setAttributesFromProps)(el, props);
    if (strategy === 'worker') {
        el.setAttribute('type', 'text/partytown');
    }
    el.setAttribute('data-nscript', strategy);
    // Load styles associated with this script
    if (stylesheets) {
        insertStylesheets(stylesheets);
    }
    document.body.appendChild(el);
};
function handleClientScriptLoad(props) {
    const { strategy = 'afterInteractive' } = props;
    if (strategy === 'lazyOnload') {
        window.addEventListener('load', ()=>{
            (0, _requestidlecallback.requestIdleCallback)(()=>loadScript(props));
        });
    } else {
        loadScript(props);
    }
}
function loadLazyScript(props) {
    if (document.readyState === 'complete') {
        (0, _requestidlecallback.requestIdleCallback)(()=>loadScript(props));
    } else {
        window.addEventListener('load', ()=>{
            (0, _requestidlecallback.requestIdleCallback)(()=>loadScript(props));
        });
    }
}
function addBeforeInteractiveToCache() {
    const scripts = [
        ...document.querySelectorAll('[data-nscript="beforeInteractive"]'),
        ...document.querySelectorAll('[data-nscript="beforePageRender"]')
    ];
    scripts.forEach((script)=>{
        const cacheKey = script.id || script.getAttribute('src');
        LoadCache.add(cacheKey);
    });
}
function initScriptLoader(scriptLoaderItems) {
    scriptLoaderItems.forEach(handleClientScriptLoad);
    addBeforeInteractiveToCache();
}
/**
 * Load a third-party scripts in an optimized way.
 *
 * Read more: [Next.js Docs: `next/script`](https://nextjs.org/docs/app/api-reference/components/script)
 */ function Script(props) {
    const { id, src = '', onLoad = ()=>{}, onReady = null, strategy = 'afterInteractive', onError, stylesheets, ...restProps } = props;
    // Context is available only during SSR
    let { updateScripts, scripts, getIsSsr, appDir, nonce } = (0, _react.useContext)(_headmanagercontextsharedruntime.HeadManagerContext);
    // if a nonce is explicitly passed to the script tag, favor that over the automatic handling
    nonce = restProps.nonce || nonce;
    /**
   * - First mount:
   *   1. The useEffect for onReady executes
   *   2. hasOnReadyEffectCalled.current is false, but the script hasn't loaded yet (not in LoadCache)
   *      onReady is skipped, set hasOnReadyEffectCalled.current to true
   *   3. The useEffect for loadScript executes
   *   4. hasLoadScriptEffectCalled.current is false, loadScript executes
   *      Once the script is loaded, the onLoad and onReady will be called by then
   *   [If strict mode is enabled / is wrapped in <OffScreen /> component]
   *   5. The useEffect for onReady executes again
   *   6. hasOnReadyEffectCalled.current is true, so entire effect is skipped
   *   7. The useEffect for loadScript executes again
   *   8. hasLoadScriptEffectCalled.current is true, so entire effect is skipped
   *
   * - Second mount:
   *   1. The useEffect for onReady executes
   *   2. hasOnReadyEffectCalled.current is false, but the script has already loaded (found in LoadCache)
   *      onReady is called, set hasOnReadyEffectCalled.current to true
   *   3. The useEffect for loadScript executes
   *   4. The script is already loaded, loadScript bails out
   *   [If strict mode is enabled / is wrapped in <OffScreen /> component]
   *   5. The useEffect for onReady executes again
   *   6. hasOnReadyEffectCalled.current is true, so entire effect is skipped
   *   7. The useEffect for loadScript executes again
   *   8. hasLoadScriptEffectCalled.current is true, so entire effect is skipped
   */ const hasOnReadyEffectCalled = (0, _react.useRef)(false);
    (0, _react.useEffect)(()=>{
        const cacheKey = id || src;
        if (!hasOnReadyEffectCalled.current) {
            // Run onReady if script has loaded before but component is re-mounted
            if (onReady && cacheKey && LoadCache.has(cacheKey)) {
                onReady();
            }
            hasOnReadyEffectCalled.current = true;
        }
    }, [
        onReady,
        id,
        src
    ]);
    const hasLoadScriptEffectCalled = (0, _react.useRef)(false);
    (0, _react.useEffect)(()=>{
        if (!hasLoadScriptEffectCalled.current) {
            if (strategy === 'afterInteractive') {
                loadScript(props);
            } else if (strategy === 'lazyOnload') {
                loadLazyScript(props);
            }
            hasLoadScriptEffectCalled.current = true;
        }
    }, [
        props,
        strategy
    ]);
    if (strategy === 'beforeInteractive' || strategy === 'worker') {
        if (updateScripts) {
            scripts[strategy] = (scripts[strategy] || []).concat([
                {
                    id,
                    src,
                    onLoad,
                    onReady,
                    onError,
                    ...restProps,
                    nonce
                }
            ]);
            updateScripts(scripts);
        } else if (getIsSsr && getIsSsr()) {
            // Script has already loaded during SSR
            LoadCache.add(id || src);
        } else if (getIsSsr && !getIsSsr()) {
            loadScript({
                ...props,
                nonce
            });
        }
    }
    // For the app directory, we need React Float to preload these scripts.
    if (appDir) {
        // Injecting stylesheets here handles beforeInteractive and worker scripts correctly
        // For other strategies injecting here ensures correct stylesheet order
        // ReactDOM.preinit handles loading the styles in the correct order,
        // also ensures the stylesheet is loaded only once and in a consistent manner
        //
        // Case 1: Styles for beforeInteractive/worker with appDir - handled here
        // Case 2: Styles for beforeInteractive/worker with pages dir - Not handled yet
        // Case 3: Styles for afterInteractive/lazyOnload with appDir - handled here
        // Case 4: Styles for afterInteractive/lazyOnload with pages dir - handled in insertStylesheets function
        if (stylesheets) {
            stylesheets.forEach((styleSrc)=>{
                _reactdom.default.preinit(styleSrc, {
                    as: 'style'
                });
            });
        }
        // Before interactive scripts need to be loaded by Next.js' runtime instead
        // of native <script> tags, because they no longer have `defer`.
        if (strategy === 'beforeInteractive') {
            if (!src) {
                // For inlined scripts, we put the content in `children`.
                if (restProps.dangerouslySetInnerHTML) {
                    // Casting since lib.dom.d.ts doesn't have TrustedHTML yet.
                    restProps.children = restProps.dangerouslySetInnerHTML.__html;
                    delete restProps.dangerouslySetInnerHTML;
                }
                return /*#__PURE__*/ (0, _jsxruntime.jsx)("script", {
                    nonce: nonce,
                    dangerouslySetInnerHTML: {
                        __html: `(self.__next_s=self.__next_s||[]).push(${(0, _htmlescape.htmlEscapeJsonString)(JSON.stringify([
                            0,
                            {
                                ...restProps,
                                id
                            }
                        ]))})`
                    }
                });
            } else {
                // @ts-ignore
                _reactdom.default.preload(src, restProps.integrity ? {
                    as: 'script',
                    integrity: restProps.integrity,
                    nonce,
                    crossOrigin: restProps.crossOrigin
                } : {
                    as: 'script',
                    nonce,
                    crossOrigin: restProps.crossOrigin
                });
                return /*#__PURE__*/ (0, _jsxruntime.jsx)("script", {
                    nonce: nonce,
                    dangerouslySetInnerHTML: {
                        __html: `(self.__next_s=self.__next_s||[]).push(${(0, _htmlescape.htmlEscapeJsonString)(JSON.stringify([
                            src,
                            {
                                ...restProps,
                                id
                            }
                        ]))})`
                    }
                });
            }
        } else if (strategy === 'afterInteractive') {
            if (src) {
                // @ts-ignore
                _reactdom.default.preload(src, restProps.integrity ? {
                    as: 'script',
                    integrity: restProps.integrity,
                    nonce,
                    crossOrigin: restProps.crossOrigin
                } : {
                    as: 'script',
                    nonce,
                    crossOrigin: restProps.crossOrigin
                });
            }
        }
    }
    return null;
}
Object.defineProperty(Script, '__nextScript', {
    value: true
});
const _default = Script;
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/detect-domain-locale.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "detectDomainLocale", {
    enumerable: true,
    get: function() {
        return detectDomainLocale;
    }
});
const detectDomainLocale = (...args)=>{
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
};
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/remove-locale.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "removeLocale", {
    enumerable: true,
    get: function() {
        return removeLocale;
    }
});
const _parsepath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/parse-path.js [client] (ecmascript)");
function removeLocale(path, locale) {
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    return path;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/has-base-path.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "hasBasePath", {
    enumerable: true,
    get: function() {
        return hasBasePath;
    }
});
const _pathhasprefix = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/path-has-prefix.js [client] (ecmascript)");
const basePath = ("TURBOPACK compile-time value", "") || '';
function hasBasePath(path) {
    return (0, _pathhasprefix.pathHasPrefix)(path, basePath);
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/remove-base-path.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "removeBasePath", {
    enumerable: true,
    get: function() {
        return removeBasePath;
    }
});
const _hasbasepath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/has-base-path.js [client] (ecmascript)");
const basePath = ("TURBOPACK compile-time value", "") || '';
function removeBasePath(path) {
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    // Can't trim the basePath if it has zero length!
    if (basePath.length === 0) return path;
    path = path.slice(basePath.length);
    if (!path.startsWith('/')) path = `/${path}`;
    return path;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/resolve-href.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "resolveHref", {
    enumerable: true,
    get: function() {
        return resolveHref;
    }
});
const _querystring = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/querystring.js [client] (ecmascript)");
const _formaturl = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/format-url.js [client] (ecmascript)");
const _omit = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/omit.js [client] (ecmascript)");
const _utils = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/utils.js [client] (ecmascript)");
const _normalizetrailingslash = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/normalize-trailing-slash.js [client] (ecmascript)");
const _islocalurl = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/is-local-url.js [client] (ecmascript)");
const _utils1 = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/index.js [client] (ecmascript)");
const _interpolateas = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/interpolate-as.js [client] (ecmascript)");
const _routeregex = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/route-regex.js [client] (ecmascript)");
const _routematcher = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/route-matcher.js [client] (ecmascript)");
function resolveHref(router, href, resolveAs) {
    // we use a dummy base url for relative urls
    let base;
    let urlAsString = typeof href === 'string' ? href : (0, _formaturl.formatWithValidation)(href);
    // repeated slashes and backslashes in the URL are considered
    // invalid and will never match a Next.js page/file
    // https://www.rfc-editor.org/rfc/rfc3986.html#section-3.1
    const urlProtoMatch = urlAsString.match(/^[a-z][a-z0-9+.-]*:\/\//i);
    const urlAsStringNoProto = urlProtoMatch ? urlAsString.slice(urlProtoMatch[0].length) : urlAsString;
    const urlParts = urlAsStringNoProto.split('?', 1);
    if ((urlParts[0] || '').match(/(\/\/|\\)/)) {
        console.error(`Invalid href '${urlAsString}' passed to next/router in page: '${router.pathname}'. Repeated forward-slashes (//) or backslashes \\ are not valid in the href.`);
        const normalizedUrl = (0, _utils.normalizeRepeatedSlashes)(urlAsStringNoProto);
        urlAsString = (urlProtoMatch ? urlProtoMatch[0] : '') + normalizedUrl;
    }
    // Return because it cannot be routed by the Next.js router
    if (!(0, _islocalurl.isLocalURL)(urlAsString)) {
        return resolveAs ? [
            urlAsString
        ] : urlAsString;
    }
    try {
        let baseBase = urlAsString.startsWith('#') ? router.asPath : router.pathname;
        // If the provided href is only a query string, it is safer to use the asPath
        // considering rewrites.
        if (urlAsString.startsWith('?')) {
            baseBase = router.asPath;
            // However, if is a dynamic route, we need to use the pathname to preserve the
            // query interpolation and rewrites (router.pathname will look like "/[slug]").
            if ((0, _utils1.isDynamicRoute)(router.pathname)) {
                baseBase = router.pathname;
                const routeRegex = (0, _routeregex.getRouteRegex)(router.pathname);
                const match = (0, _routematcher.getRouteMatcher)(routeRegex)(router.asPath);
                // For dynamic routes, if asPath doesn't match the pathname regex, it is a rewritten path.
                // In this case, should use asPath to preserve the current URL.
                if (!match) {
                    baseBase = router.asPath;
                }
            // Note: There is an edge case where the pathname is dynamic, and also a rewrite path to the same segment.
            // E.g. in "/[slug]" path, rewrite "/foo" -> "/bar"
            // In this case, it will be treated as a non-rewritten path and possibly interpolate the query string.
            // E.g., "/any?slug=foo" will become the content of "/foo", not rewritten as "/bar"
            // This is currently a trade-off of not resolving rewrite paths on every Router/Link call,
            // but using a lighter route regex pattern check.
            }
        }
        base = new URL(baseBase, 'http://n');
    } catch (_) {
        // fallback to / for invalid asPath values e.g. //
        base = new URL('/', 'http://n');
    }
    try {
        const finalUrl = new URL(urlAsString, base);
        finalUrl.pathname = (0, _normalizetrailingslash.normalizePathTrailingSlash)(finalUrl.pathname);
        let interpolatedAs = '';
        if ((0, _utils1.isDynamicRoute)(finalUrl.pathname) && finalUrl.searchParams && resolveAs) {
            const query = (0, _querystring.searchParamsToUrlQuery)(finalUrl.searchParams);
            const { result, params } = (0, _interpolateas.interpolateAs)(finalUrl.pathname, finalUrl.pathname, query);
            if (result) {
                interpolatedAs = (0, _formaturl.formatWithValidation)({
                    pathname: result,
                    hash: finalUrl.hash,
                    query: (0, _omit.omit)(query, params)
                });
            }
        }
        // if the origin didn't change, it means we received a relative href
        const resolvedHref = finalUrl.origin === base.origin ? finalUrl.href.slice(finalUrl.origin.length) : finalUrl.href;
        return resolveAs ? [
            resolvedHref,
            interpolatedAs || resolvedHref
        ] : resolvedHref;
    } catch (_) {
        return resolveAs ? [
            urlAsString
        ] : urlAsString;
    }
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/lib/javascript-url.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

// Adapted from React's sanitizeURL function found here: https://github.com/facebook/react/blob/b565373afd0cc1988497e1107106e851e8cfb261/packages/react-dom-bindings/src/shared/sanitizeURL.js
// A javascript: URL can contain leading C0 control or \u0020 SPACE,
// and any newline or tab are filtered out as if they're not part of the URL.
// https://url.spec.whatwg.org/#url-parsing
// Tab or newline are defined as \r\n\t:
// https://infra.spec.whatwg.org/#ascii-tab-or-newline
// A C0 control is a code point in the range \u0000 NULL to \u001F
// INFORMATION SEPARATOR ONE, inclusive:
// https://infra.spec.whatwg.org/#c0-control-or-space
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "isJavaScriptURLString", {
    enumerable: true,
    get: function() {
        return isJavaScriptURLString;
    }
});
const isJavaScriptProtocol = /^[\u0000-\u001F ]*j[\r\n\t]*a[\r\n\t]*v[\r\n\t]*a[\r\n\t]*s[\r\n\t]*c[\r\n\t]*r[\r\n\t]*i[\r\n\t]*p[\r\n\t]*t[\r\n\t]*:/i;
function isJavaScriptURLString(url) {
    return isJavaScriptProtocol.test('' + url);
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/with-router.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "default", {
    enumerable: true,
    get: function() {
        return withRouter;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [client] (ecmascript)");
const _jsxruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/react@19.2.6/node_modules/react/jsx-runtime.js [client] (ecmascript)");
const _react = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/react@19.2.6/node_modules/react/index.js [client] (ecmascript)"));
const _router = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/router.js [client] (ecmascript)");
function withRouter(ComposedComponent) {
    function WithRouterWrapper(props) {
        return /*#__PURE__*/ (0, _jsxruntime.jsx)(ComposedComponent, {
            router: (0, _router.useRouter)(),
            ...props
        });
    }
    WithRouterWrapper.getInitialProps = ComposedComponent.getInitialProps;
    WithRouterWrapper.origGetInitialProps = ComposedComponent.origGetInitialProps;
    if ("TURBOPACK compile-time truthy", 1) {
        const name = ComposedComponent.displayName || ComposedComponent.name || 'Unknown';
        WithRouterWrapper.displayName = `withRouter(${name})`;
    }
    return WithRouterWrapper;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/router.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

/* global window */ Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    Router: null,
    createRouter: null,
    default: null,
    makePublicRouterInstance: null,
    useRouter: null,
    withRouter: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    Router: function() {
        return _router.default;
    },
    createRouter: function() {
        return createRouter;
    },
    // Export the singletonRouter and this is the public API.
    default: function() {
        return _default;
    },
    makePublicRouterInstance: function() {
        return makePublicRouterInstance;
    },
    useRouter: function() {
        return useRouter;
    },
    withRouter: function() {
        return _withrouter.default;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [client] (ecmascript)");
const _react = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/react@19.2.6/node_modules/react/index.js [client] (ecmascript)"));
const _router = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/router.js [client] (ecmascript)"));
const _routercontextsharedruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router-context.shared-runtime.js [client] (ecmascript)");
const _iserror = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/is-error.js [client] (ecmascript)"));
const _withrouter = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/with-router.js [client] (ecmascript)"));
const singletonRouter = {
    router: null,
    readyCallbacks: [],
    ready (callback) {
        if (this.router) return callback();
        if (typeof window !== 'undefined') {
            this.readyCallbacks.push(callback);
        }
    }
};
// Create public properties and methods of the router in the singletonRouter
const urlPropertyFields = [
    'pathname',
    'route',
    'query',
    'asPath',
    'components',
    'isFallback',
    'basePath',
    'locale',
    'locales',
    'defaultLocale',
    'isReady',
    'isPreview',
    'isLocaleDomain',
    'domainLocales'
];
const routerEvents = [
    'routeChangeStart',
    'beforeHistoryChange',
    'routeChangeComplete',
    'routeChangeError',
    'hashChangeStart',
    'hashChangeComplete'
];
const coreMethodFields = [
    'push',
    'replace',
    'reload',
    'back',
    'prefetch',
    'beforePopState'
];
// Events is a static property on the router, the router doesn't have to be initialized to use it
Object.defineProperty(singletonRouter, 'events', {
    get () {
        return _router.default.events;
    }
});
function getRouter() {
    if (!singletonRouter.router) {
        const message = 'No router instance found.\n' + 'You should only use "next/router" on the client side of your app.\n';
        throw Object.defineProperty(new Error(message), "__NEXT_ERROR_CODE", {
            value: "E1044",
            enumerable: false,
            configurable: true
        });
    }
    return singletonRouter.router;
}
urlPropertyFields.forEach((field)=>{
    // Here we need to use Object.defineProperty because we need to return
    // the property assigned to the actual router
    // The value might get changed as we change routes and this is the
    // proper way to access it
    Object.defineProperty(singletonRouter, field, {
        get () {
            const router = getRouter();
            return router[field];
        }
    });
});
coreMethodFields.forEach((field)=>{
    // We don't really know the types here, so we add them later instead
    ;
    singletonRouter[field] = (...args)=>{
        const router = getRouter();
        return router[field](...args);
    };
});
routerEvents.forEach((event)=>{
    singletonRouter.ready(()=>{
        _router.default.events.on(event, (...args)=>{
            const eventField = `on${event.charAt(0).toUpperCase()}${event.substring(1)}`;
            const _singletonRouter = singletonRouter;
            if (_singletonRouter[eventField]) {
                try {
                    _singletonRouter[eventField](...args);
                } catch (err) {
                    console.error(`Error when running the Router event: ${eventField}`);
                    console.error((0, _iserror.default)(err) ? `${err.message}\n${err.stack}` : err + '');
                }
            }
        });
    });
});
const _default = singletonRouter;
function useRouter() {
    const router = _react.default.useContext(_routercontextsharedruntime.RouterContext);
    if (!router) {
        throw Object.defineProperty(new Error('NextRouter was not mounted. https://nextjs.org/docs/messages/next-router-not-mounted'), "__NEXT_ERROR_CODE", {
            value: "E509",
            enumerable: false,
            configurable: true
        });
    }
    return router;
}
function createRouter(...args) {
    singletonRouter.router = new _router.default(...args);
    singletonRouter.readyCallbacks.forEach((cb)=>cb());
    singletonRouter.readyCallbacks = [];
    return singletonRouter.router;
}
function makePublicRouterInstance(router) {
    const scopedRouter = router;
    const instance = {};
    for (const property of urlPropertyFields){
        if (typeof scopedRouter[property] === 'object') {
            instance[property] = Object.assign(Array.isArray(scopedRouter[property]) ? [] : {}, scopedRouter[property]) // makes sure query is not stateful
            ;
            continue;
        }
        instance[property] = scopedRouter[property];
    }
    // Events is a static property on the router, the router doesn't have to be initialized to use it
    instance.events = _router.default.events;
    coreMethodFields.forEach((field)=>{
        instance[field] = (...args)=>{
            return scopedRouter[field](...args);
        };
    });
    return instance;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/route-announcer.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    RouteAnnouncer: null,
    default: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    RouteAnnouncer: function() {
        return RouteAnnouncer;
    },
    default: function() {
        return _default;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [client] (ecmascript)");
const _jsxruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/react@19.2.6/node_modules/react/jsx-runtime.js [client] (ecmascript)");
const _react = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/react@19.2.6/node_modules/react/index.js [client] (ecmascript)"));
const _router = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/router.js [client] (ecmascript)");
const nextjsRouteAnnouncerStyles = {
    border: 0,
    clip: 'rect(0 0 0 0)',
    height: '1px',
    margin: '-1px',
    overflow: 'hidden',
    padding: 0,
    position: 'absolute',
    top: 0,
    width: '1px',
    // https://medium.com/@jessebeach/beware-smushed-off-screen-accessible-text-5952a4c2cbfe
    whiteSpace: 'nowrap',
    wordWrap: 'normal'
};
const RouteAnnouncer = ()=>{
    const { asPath } = (0, _router.useRouter)();
    const [routeAnnouncement, setRouteAnnouncement] = _react.default.useState('');
    // Only announce the path change, but not for the first load because screen
    // reader will do that automatically.
    const previouslyLoadedPath = _react.default.useRef(asPath);
    // Every time the path changes, announce the new page’s title following this
    // priority: first the document title (from head), otherwise the first h1, or
    // if none of these exist, then the pathname from the URL. This methodology is
    // inspired by Marcy Sutton’s accessible client routing user testing. More
    // information can be found here:
    // https://www.gatsbyjs.com/blog/2019-07-11-user-testing-accessible-client-routing/
    _react.default.useEffect({
        "RouteAnnouncer.useEffect": ()=>{
            // If the path hasn't change, we do nothing.
            if (previouslyLoadedPath.current === asPath) return;
            previouslyLoadedPath.current = asPath;
            if (document.title) {
                setRouteAnnouncement(document.title);
            } else {
                const pageHeader = document.querySelector('h1');
                const content = pageHeader?.innerText ?? pageHeader?.textContent;
                setRouteAnnouncement(content || asPath);
            }
        }
    }["RouteAnnouncer.useEffect"], [
        asPath
    ]);
    return /*#__PURE__*/ (0, _jsxruntime.jsx)("p", {
        "aria-live": "assertive" // Make the announcement immediately.
        ,
        id: "__next-route-announcer__",
        role: "alert",
        style: nextjsRouteAnnouncerStyles,
        children: routeAnnouncement
    });
};
const _default = RouteAnnouncer;
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/readonly-url-search-params.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

/**
 * ReadonlyURLSearchParams implementation shared between client and server.
 * This file is intentionally not marked as 'use client' or 'use server'
 * so it can be imported by both environments.
 */ /** @internal */ Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "ReadonlyURLSearchParams", {
    enumerable: true,
    get: function() {
        return ReadonlyURLSearchParams;
    }
});
class ReadonlyURLSearchParamsError extends Error {
    constructor(){
        super('Method unavailable on `ReadonlyURLSearchParams`. Read more: https://nextjs.org/docs/app/api-reference/functions/use-search-params#updating-searchparams');
    }
}
class ReadonlyURLSearchParams extends URLSearchParams {
    /** @deprecated Method unavailable on `ReadonlyURLSearchParams`. Read more: https://nextjs.org/docs/app/api-reference/functions/use-search-params#updating-searchparams */ append() {
        throw new ReadonlyURLSearchParamsError();
    }
    /** @deprecated Method unavailable on `ReadonlyURLSearchParams`. Read more: https://nextjs.org/docs/app/api-reference/functions/use-search-params#updating-searchparams */ delete() {
        throw new ReadonlyURLSearchParamsError();
    }
    /** @deprecated Method unavailable on `ReadonlyURLSearchParams`. Read more: https://nextjs.org/docs/app/api-reference/functions/use-search-params#updating-searchparams */ set() {
        throw new ReadonlyURLSearchParamsError();
    }
    /** @deprecated Method unavailable on `ReadonlyURLSearchParams`. Read more: https://nextjs.org/docs/app/api-reference/functions/use-search-params#updating-searchparams */ sort() {
        throw new ReadonlyURLSearchParamsError();
    }
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/react-client-callbacks/report-global-error.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "reportGlobalError", {
    enumerable: true,
    get: function() {
        return reportGlobalError;
    }
});
const reportGlobalError = typeof reportError === 'function' ? reportError : (error)=>{
    // TODO: Dispatch error event
    globalThis.console.error(error);
};
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/react-client-callbacks/on-recoverable-error.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
// This module can be shared between both pages router and app router
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    isRecoverableError: null,
    onRecoverableError: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    isRecoverableError: function() {
        return isRecoverableError;
    },
    onRecoverableError: function() {
        return onRecoverableError;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [client] (ecmascript)");
const _bailouttocsr = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/lazy-dynamic/bailout-to-csr.js [client] (ecmascript)");
const _iserror = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/is-error.js [client] (ecmascript)"));
const _reportglobalerror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/react-client-callbacks/report-global-error.js [client] (ecmascript)");
const recoverableErrors = new WeakSet();
const isInstantTest = ("TURBOPACK compile-time value", true) && typeof self !== 'undefined' && !!self.__next_instant_test;
function isRecoverableError(error) {
    return recoverableErrors.has(error);
}
const onRecoverableError = (error)=>{
    // x-ref: https://github.com/facebook/react/pull/28736
    let cause = (0, _iserror.default)(error) && 'cause' in error ? error.cause : error;
    // Skip certain custom errors which are not expected to be reported on client
    if ((0, _bailouttocsr.isBailoutToCSRError)(cause)) return;
    // Instant Navigation Testing API: suppress "server could not finish this
    // Suspense boundary" errors (React error #419) during instant test mode.
    // The static shell intentionally has incomplete Suspense boundaries — React
    // correctly falls back to client rendering, which is expected.
    if (isInstantTest) {
        if ((0, _iserror.default)(cause)) {
            if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
            ;
            else {
                if (cause.message.includes('could not finish this Suspense boundary')) return;
            }
        }
    }
    if ("TURBOPACK compile-time truthy", 1) {
        const { decorateDevError } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/errors/stitched-error.js [client] (ecmascript)");
        const causeError = decorateDevError(cause);
        recoverableErrors.add(causeError);
        cause = causeError;
    }
    (0, _reportglobalerror.reportGlobalError)(cause);
};
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/tracing/tracer.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "default", {
    enumerable: true,
    get: function() {
        return _default;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [client] (ecmascript)");
const _mitt = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/mitt.js [client] (ecmascript)"));
class Span {
    constructor(name, options, onSpanEnd){
        this.name = name;
        this.attributes = options.attributes ?? {};
        this.startTime = options.startTime ?? Date.now();
        this.onSpanEnd = onSpanEnd;
        this.state = {
            state: 'inprogress'
        };
    }
    end(endTime) {
        if (this.state.state === 'ended') {
            throw Object.defineProperty(new Error('Span has already ended'), "__NEXT_ERROR_CODE", {
                value: "E17",
                enumerable: false,
                configurable: true
            });
        }
        this.state = {
            state: 'ended',
            endTime: endTime ?? Date.now()
        };
        this.onSpanEnd(this);
    }
}
class Tracer {
    startSpan(name, options) {
        return new Span(name, options, this.handleSpanEnd);
    }
    onSpanEnd(cb) {
        this._emitter.on('spanend', cb);
        return ()=>{
            this._emitter.off('spanend', cb);
        };
    }
    constructor(){
        this._emitter = (0, _mitt.default)();
        this.handleSpanEnd = (span)=>{
            this._emitter.emit('spanend', span);
        };
    }
}
const _default = new Tracer();
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/http-access-fallback/http-access-fallback.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    HTTPAccessErrorStatus: null,
    HTTP_ERROR_FALLBACK_ERROR_CODE: null,
    getAccessFallbackErrorTypeByStatus: null,
    getAccessFallbackHTTPStatus: null,
    isHTTPAccessFallbackError: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    HTTPAccessErrorStatus: function() {
        return HTTPAccessErrorStatus;
    },
    HTTP_ERROR_FALLBACK_ERROR_CODE: function() {
        return HTTP_ERROR_FALLBACK_ERROR_CODE;
    },
    getAccessFallbackErrorTypeByStatus: function() {
        return getAccessFallbackErrorTypeByStatus;
    },
    getAccessFallbackHTTPStatus: function() {
        return getAccessFallbackHTTPStatus;
    },
    isHTTPAccessFallbackError: function() {
        return isHTTPAccessFallbackError;
    }
});
const HTTPAccessErrorStatus = {
    NOT_FOUND: 404,
    FORBIDDEN: 403,
    UNAUTHORIZED: 401
};
const ALLOWED_CODES = new Set(Object.values(HTTPAccessErrorStatus));
const HTTP_ERROR_FALLBACK_ERROR_CODE = 'NEXT_HTTP_ERROR_FALLBACK';
function isHTTPAccessFallbackError(error) {
    if (typeof error !== 'object' || error === null || !('digest' in error) || typeof error.digest !== 'string') {
        return false;
    }
    const [prefix, httpStatus] = error.digest.split(';');
    return prefix === HTTP_ERROR_FALLBACK_ERROR_CODE && ALLOWED_CODES.has(Number(httpStatus));
}
function getAccessFallbackHTTPStatus(error) {
    const httpStatus = error.digest.split(';')[1];
    return Number(httpStatus);
}
function getAccessFallbackErrorTypeByStatus(status) {
    switch(status){
        case 401:
            return 'unauthorized';
        case 403:
            return 'forbidden';
        case 404:
            return 'not-found';
        default:
            return;
    }
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/redirect-status-code.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "RedirectStatusCode", {
    enumerable: true,
    get: function() {
        return RedirectStatusCode;
    }
});
var RedirectStatusCode = /*#__PURE__*/ function(RedirectStatusCode) {
    RedirectStatusCode[RedirectStatusCode["SeeOther"] = 303] = "SeeOther";
    RedirectStatusCode[RedirectStatusCode["TemporaryRedirect"] = 307] = "TemporaryRedirect";
    RedirectStatusCode[RedirectStatusCode["PermanentRedirect"] = 308] = "PermanentRedirect";
    return RedirectStatusCode;
}({});
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/redirect-error.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    REDIRECT_ERROR_CODE: null,
    isRedirectError: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    REDIRECT_ERROR_CODE: function() {
        return REDIRECT_ERROR_CODE;
    },
    isRedirectError: function() {
        return isRedirectError;
    }
});
const _redirectstatuscode = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/redirect-status-code.js [client] (ecmascript)");
const REDIRECT_ERROR_CODE = 'NEXT_REDIRECT';
function isRedirectError(error) {
    if (typeof error !== 'object' || error === null || !('digest' in error) || typeof error.digest !== 'string') {
        return false;
    }
    const digest = error.digest.split(';');
    const [errorCode, type] = digest;
    const destination = digest.slice(2, -2).join(';');
    const status = digest.at(-2);
    const statusCode = Number(status);
    return errorCode === REDIRECT_ERROR_CODE && (type === 'replace' || type === 'push') && typeof destination === 'string' && !isNaN(statusCode) && statusCode in _redirectstatuscode.RedirectStatusCode;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/is-next-router-error.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "isNextRouterError", {
    enumerable: true,
    get: function() {
        return isNextRouterError;
    }
});
const _httpaccessfallback = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/http-access-fallback/http-access-fallback.js [client] (ecmascript)");
const _redirecterror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/redirect-error.js [client] (ecmascript)");
function isNextRouterError(error) {
    return (0, _redirecterror.isRedirectError)(error) || (0, _httpaccessfallback.isHTTPAccessFallbackError)(error);
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/get-socket-url.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "getSocketUrl", {
    enumerable: true,
    get: function() {
        return getSocketUrl;
    }
});
const _normalizedassetprefix = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/normalized-asset-prefix.js [client] (ecmascript)");
function getSocketProtocol(assetPrefix) {
    let protocol = window.location.protocol;
    try {
        // assetPrefix is a url
        protocol = new URL(assetPrefix).protocol;
    } catch  {}
    return protocol === 'http:' ? 'ws:' : 'wss:';
}
function getSocketUrl(assetPrefix) {
    const prefix = (0, _normalizedassetprefix.normalizedAssetPrefix)(assetPrefix);
    const protocol = getSocketProtocol(assetPrefix || '');
    if (URL.canParse(prefix)) {
        // since normalized asset prefix is ensured to be a URL format,
        // we can safely replace the protocol
        return prefix.replace(/^http/, 'ws');
    }
    const { hostname, port } = window.location;
    return `${protocol}//${hostname}${port ? `:${port}` : ''}${prefix}`;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/pages/websocket.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    addMessageListener: null,
    connectHMR: null,
    sendMessage: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    addMessageListener: function() {
        return addMessageListener;
    },
    connectHMR: function() {
        return connectHMR;
    },
    sendMessage: function() {
        return sendMessage;
    }
});
const _forwardlogs = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/forward-logs.js [client] (ecmascript)");
const _hotreloadertypes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/server/dev/hot-reloader-types.js [client] (ecmascript)");
const _getsocketurl = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/get-socket-url.js [client] (ecmascript)");
const _constants = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/constants.js [client] (ecmascript)");
let source;
const messageCallbacks = [];
function addMessageListener(callback) {
    messageCallbacks.push(callback);
}
function sendMessage(data) {
    if (!source || source.readyState !== source.OPEN) return;
    return source.send(data);
}
let reconnections = 0;
let reloading = false;
let serverSessionId = null;
function connectHMR(options) {
    let timer;
    function init() {
        if (source) source.close();
        function handleOnline() {
            _forwardlogs.logQueue.onSocketReady(source);
            reconnections = 0;
            window.console.log('[HMR] connected');
        }
        function handleMessage(event) {
            // While the page is reloading, don't respond to any more messages.
            // On reconnect, the server may send an empty list of changes if it was restarted.
            if (reloading) {
                return;
            }
            const message = JSON.parse(event.data);
            if (message.type === _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.TURBOPACK_CONNECTED) {
                if (serverSessionId !== null && serverSessionId !== message.data.sessionId) {
                    // Either the server's session id has changed and it's a new server, or
                    // it's been too long since we disconnected and we should reload the page.
                    // There could be 1) unhandled server errors and/or 2) stale content.
                    // Perform a hard reload of the page.
                    window.location.reload();
                    reloading = true;
                    return;
                }
                serverSessionId = message.data.sessionId;
            }
            for (const messageCallback of messageCallbacks){
                messageCallback(message);
            }
        }
        function handleDisconnect() {
            source.onerror = null;
            source.onclose = null;
            source.close();
            reconnections++;
            // After 25 reconnects we'll want to reload the page as it indicates the dev server is no longer running.
            if (reconnections > _constants.WEB_SOCKET_MAX_RECONNECTIONS) {
                reloading = true;
                window.location.reload();
                return;
            }
            clearTimeout(timer);
            // Try again after 5 seconds
            timer = setTimeout(init, reconnections > 5 ? 5000 : 1000);
        }
        const url = (0, _getsocketurl.getSocketUrl)(options.assetPrefix);
        source = new window.WebSocket(`${url}${options.path}`);
        source.onopen = handleOnline;
        source.onerror = handleDisconnect;
        source.onclose = handleDisconnect;
        source.onmessage = handleMessage;
    }
    init();
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/shared.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    REACT_REFRESH_FULL_RELOAD: null,
    REACT_REFRESH_FULL_RELOAD_FROM_ERROR: null,
    reportInvalidHmrMessage: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    REACT_REFRESH_FULL_RELOAD: function() {
        return REACT_REFRESH_FULL_RELOAD;
    },
    REACT_REFRESH_FULL_RELOAD_FROM_ERROR: function() {
        return REACT_REFRESH_FULL_RELOAD_FROM_ERROR;
    },
    reportInvalidHmrMessage: function() {
        return reportInvalidHmrMessage;
    }
});
const REACT_REFRESH_FULL_RELOAD = '[Fast Refresh] performing full reload\n\n' + "Fast Refresh will perform a full reload when you edit a file that's imported by modules outside of the React rendering tree.\n" + 'You might have a file which exports a React component but also exports a value that is imported by a non-React component file.\n' + 'Consider migrating the non-React component export to a separate file and importing it into both files.\n\n' + 'It is also possible the parent component of the component you edited is a class component, which disables Fast Refresh.\n' + 'Fast Refresh requires at least one parent function component in your React tree.';
const REACT_REFRESH_FULL_RELOAD_FROM_ERROR = '[Fast Refresh] performing full reload because your application had an unrecoverable error';
function reportInvalidHmrMessage(message, err) {
    console.warn('[HMR] Invalid message: ' + JSON.stringify(message) + '\n' + (err instanceof Error && err?.stack || ''));
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/runtime-error-handler.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "RuntimeErrorHandler", {
    enumerable: true,
    get: function() {
        return RuntimeErrorHandler;
    }
});
const RuntimeErrorHandler = {
    hadRuntimeError: false
};
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/report-hmr-latency.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, /**
 * Logs information about a completed HMR to the console, the server (via a
 * `client-hmr-latency` event), and to `self.__NEXT_HMR_LATENCY_CB` (a debugging
 * hook).
 *
 * @param hasUpdate Set this to `false` to avoid reporting the HMR event via a
 *   `client-hmr-latency` event or to `self.__NEXT_HMR_LATENCY_CB`. Used by
 *   turbopack when we must report a message to the browser console (because we
 *   already logged a "rebuilding" message), but it's not a real HMR, so we
 *   don't want to impact our telemetry.
 */ "default", {
    enumerable: true,
    get: function() {
        return reportHmrLatency;
    }
});
function reportHmrLatency(sendMessage, updatedModules, startMsSinceEpoch, endMsSinceEpoch, hasUpdate = true) {
    const latencyMs = endMsSinceEpoch - startMsSinceEpoch;
    console.log(`[Fast Refresh] done in ${latencyMs}ms`);
    if (!hasUpdate) {
        return;
    }
    sendMessage(JSON.stringify({
        event: 'client-hmr-latency',
        id: window.__nextDevClientId,
        startTime: startMsSinceEpoch,
        endTime: endMsSinceEpoch,
        page: window.location.pathname,
        updatedModules,
        // Whether the page (tab) was hidden at the time the event occurred.
        // This can impact the accuracy of the event's timing.
        isPageHidden: document.visibilityState === 'hidden'
    }));
    if (self.__NEXT_HMR_LATENCY_CB) {
        self.__NEXT_HMR_LATENCY_CB(latencyMs);
    }
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/turbopack-hot-reloader-common.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "TurbopackHmr", {
    enumerable: true,
    get: function() {
        return TurbopackHmr;
    }
});
// How long to wait before reporting the HMR start, used to suppress irrelevant
// `BUILDING` events. Does not impact reported latency.
const TURBOPACK_HMR_START_DELAY_MS = 100;
class TurbopackHmr {
    #updatedModules;
    #startMsSinceEpoch;
    #lastUpdateMsSinceEpoch;
    #deferredReportHmrStartId;
    #reportedHmrStart;
    constructor(){
        this.#updatedModules = new Set();
        this.#reportedHmrStart = false;
    }
    // HACK: Turbopack tends to generate a lot of irrelevant "BUILDING" actions,
    // as it reports *any* compilation, including fully no-op/cached compilations
    // and those unrelated to HMR. Fixing this would require significant
    // architectural changes.
    //
    // Work around this by deferring any "rebuilding" message by 100ms. If we get
    // a BUILT event within that threshold and nothing has changed, just suppress
    // the message entirely.
    #runDeferredReportHmrStart() {
        if (this.#deferredReportHmrStartId != null) {
            console.log('[Fast Refresh] rebuilding');
            this.#reportedHmrStart = true;
            this.#cancelDeferredReportHmrStart();
        }
    }
    #cancelDeferredReportHmrStart() {
        clearTimeout(this.#deferredReportHmrStartId);
        this.#deferredReportHmrStartId = undefined;
    }
    onBuilding() {
        this.#lastUpdateMsSinceEpoch = undefined;
        this.#cancelDeferredReportHmrStart();
        this.#startMsSinceEpoch = Date.now();
        // report the HMR start after a short delay
        this.#deferredReportHmrStartId = setTimeout(()=>this.#runDeferredReportHmrStart(), self.__NEXT_HMR_TURBOPACK_REPORT_NOISY_NOOP_EVENTS ? 0 : TURBOPACK_HMR_START_DELAY_MS);
    }
    /** Helper for other `onEvent` methods. */ #onUpdate() {
        this.#runDeferredReportHmrStart();
        this.#lastUpdateMsSinceEpoch = Date.now();
    }
    onTurbopackMessage(msg) {
        this.#onUpdate();
        const updatedModules = extractModulesFromTurbopackMessage(msg.data);
        for (const module1 of updatedModules){
            this.#updatedModules.add(module1);
        }
    }
    onServerComponentChanges() {
        this.#onUpdate();
    }
    onReloadPage() {
        this.#onUpdate();
    }
    onPageAddRemove() {
        this.#onUpdate();
    }
    /**
   * @returns `null` if the caller should ignore the update entirely. Returns an
   *   object with `hasUpdates: false` if the caller should report the end of
   *   the HMR in the browser console, but the HMR was a no-op.
   */ onBuilt() {
        // Check that we got *any* `TurbopackMessage`, even if
        // `updatedModules` is empty (not everything gets recorded there).
        //
        // There's also a case where `onBuilt` gets called before `onBuilding`,
        // which can happen during initial page load. Ignore that too!
        const hasUpdates = this.#lastUpdateMsSinceEpoch != null && this.#startMsSinceEpoch != null;
        if (!hasUpdates && !this.#reportedHmrStart) {
            // suppress the update entirely
            this.#cancelDeferredReportHmrStart();
            return null;
        }
        this.#runDeferredReportHmrStart();
        const result = {
            hasUpdates,
            updatedModules: this.#updatedModules,
            startMsSinceEpoch: this.#startMsSinceEpoch,
            endMsSinceEpoch: this.#lastUpdateMsSinceEpoch ?? Date.now()
        };
        this.#updatedModules = new Set();
        this.#reportedHmrStart = false;
        return result;
    }
}
function extractModulesFromTurbopackMessage(data) {
    const updatedModules = new Set();
    const updates = Array.isArray(data) ? data : [
        data
    ];
    for (const update of updates){
        // TODO this won't capture changes to CSS since they don't result in a "merged" update
        if (update.type !== 'partial' || update.instruction.type !== 'ChunkListUpdate' || update.instruction.merged === undefined) {
            continue;
        }
        for (const mergedUpdate of update.instruction.merged){
            for (const name of Object.keys(mergedUpdate.entries)){
                const res = /(.*)\s+[([].*/.exec(name);
                if (res === null) {
                    continue;
                }
                updatedModules.add(res[1]);
            }
        }
    }
    return updatedModules;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/pages/hot-reloader-pages.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
// TODO: Remove use of `any` type.
/**
 * MIT License
 *
 * Copyright (c) 2013-present, Facebook, Inc.
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
 */ /// <reference types="webpack/module.d.ts" />
// This file is a modified version of the Create React App HMR dev client that
// can be found here:
// https://github.com/facebook/create-react-app/blob/v3.4.1/packages/react-dev-utils/webpackHotDevClient.js
/// <reference types="webpack/module.d.ts" />
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    default: null,
    handleStaticIndicator: null,
    performFullReload: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    default: function() {
        return connect;
    },
    handleStaticIndicator: function() {
        return handleStaticIndicator;
    },
    performFullReload: function() {
        return performFullReload;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [client] (ecmascript)");
const _nextdevtools = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/next-devtools/index.js (raw)");
const _pagesdevoverlaysetup = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/pages/pages-dev-overlay-setup.js [client] (ecmascript)");
const _stripansi = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/strip-ansi/index.js [client] (ecmascript)"));
const _websocket = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/pages/websocket.js [client] (ecmascript)");
const _formatwebpackmessages = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/format-webpack-messages.js [client] (ecmascript)"));
const _hotreloadertypes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/server/dev/hot-reloader-types.js [client] (ecmascript)");
const _shared = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/shared.js [client] (ecmascript)");
const _runtimeerrorhandler = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/runtime-error-handler.js [client] (ecmascript)");
const _reporthmrlatency = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/report-hmr-latency.js [client] (ecmascript)"));
const _turbopackhotreloadercommon = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/turbopack-hot-reloader-common.js [client] (ecmascript)");
window.__nextDevClientId = Math.round(Math.random() * 100 + Date.now());
let customHmrEventHandler;
let turbopackMessageListeners = [];
function connect() {
    (0, _pagesdevoverlaysetup.register)();
    (0, _websocket.addMessageListener)((message)=>{
        try {
            processMessage(message);
        } catch (err) {
            (0, _shared.reportInvalidHmrMessage)(message, err);
        }
    });
    return {
        subscribeToHmrEvent (handler) {
            customHmrEventHandler = handler;
        },
        onUnrecoverableError () {
            _runtimeerrorhandler.RuntimeErrorHandler.hadRuntimeError = true;
        },
        addTurbopackMessageListener (cb) {
            turbopackMessageListeners.push(cb);
        },
        sendTurbopackMessage (msg) {
            (0, _websocket.sendMessage)(msg);
        },
        handleUpdateError (err) {
            performFullReload(err);
        }
    };
}
// Remember some state related to hot module replacement.
var isFirstCompilation = true;
var mostRecentCompilationHash = null;
var hasCompileErrors = false;
function clearOutdatedErrors() {
    // Clean up outdated compile errors, if any.
    if (typeof console !== 'undefined' && typeof console.clear === 'function') {
        if (hasCompileErrors) {
            console.clear();
        }
    }
}
// Successful compilation.
function handleSuccess() {
    clearOutdatedErrors();
    hasCompileErrors = false;
    if ("TURBOPACK compile-time truthy", 1) {
        const hmrUpdate = turbopackHmr.onBuilt();
        if (hmrUpdate != null) {
            (0, _reporthmrlatency.default)(_websocket.sendMessage, [
                ...hmrUpdate.updatedModules
            ], hmrUpdate.startMsSinceEpoch, hmrUpdate.endMsSinceEpoch, hmrUpdate.hasUpdates);
        }
        _nextdevtools.dispatcher.onBuildOk();
    } else //TURBOPACK unreachable
    ;
    isFirstCompilation = false;
}
// Compilation with warnings (e.g. ESLint).
function handleWarnings(warnings) {
    clearOutdatedErrors();
    const isHotUpdate = !isFirstCompilation;
    isFirstCompilation = false;
    hasCompileErrors = false;
    function printWarnings() {
        // Print warnings to the console.
        const formatted = (0, _formatwebpackmessages.default)({
            warnings: warnings,
            errors: []
        });
        if (typeof console !== 'undefined' && typeof console.warn === 'function') {
            for(let i = 0; i < formatted.warnings?.length; i++){
                if (i === 5) {
                    console.warn('There were more warnings in other files.\n' + 'You can find a complete log in the terminal.');
                    break;
                }
                console.warn((0, _stripansi.default)(formatted.warnings[i]));
            }
        }
    }
    printWarnings();
    // Attempt to apply hot updates or reload.
    if (isHotUpdate) {
        tryApplyUpdatesWebpack();
    }
}
// Compilation with errors (e.g. syntax error or missing modules).
function handleErrors(errors) {
    clearOutdatedErrors();
    isFirstCompilation = false;
    hasCompileErrors = true;
    // "Massage" webpack messages.
    var formatted = (0, _formatwebpackmessages.default)({
        errors: errors,
        warnings: []
    });
    // Only show the first error.
    _nextdevtools.dispatcher.onBuildError(formatted.errors[0]);
    // Also log them to the console.
    if (typeof console !== 'undefined' && typeof console.error === 'function') {
        for(var i = 0; i < formatted.errors.length; i++){
            console.error((0, _stripansi.default)(formatted.errors[i]));
        }
    }
    // Do not attempt to reload now.
    // We will reload on next success instead.
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
}
let webpackStartMsSinceEpoch = null;
const turbopackHmr = ("TURBOPACK compile-time truthy", 1) ? new _turbopackhotreloadercommon.TurbopackHmr() : "TURBOPACK unreachable";
let isrManifest = {};
// There is a newer version of the code available.
function handleAvailableHash(hash) {
    // Update last known compilation hash.
    mostRecentCompilationHash = hash;
}
function handleStaticIndicator() {
    if ("TURBOPACK compile-time truthy", 1) {
        const routeInfo = window.next.router.components[window.next.router.pathname];
        const pageComponent = routeInfo?.Component;
        const appComponent = window.next.router.components['/_app']?.Component;
        const isDynamicPage = Boolean(pageComponent?.getInitialProps) || Boolean(routeInfo?.__N_SSP);
        const hasAppGetInitialProps = Boolean(appComponent?.getInitialProps) && appComponent?.getInitialProps !== appComponent?.origGetInitialProps;
        const isPageStatic = isrManifest[window.location.pathname] || !isDynamicPage && !hasAppGetInitialProps;
        _nextdevtools.dispatcher.onStaticIndicator(isPageStatic ? 'static' : 'dynamic');
    }
}
/** Handles messages from the server for the Pages Router. */ function processMessage(message) {
    switch(message.type){
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.ISR_MANIFEST:
            {
                isrManifest = message.data;
                handleStaticIndicator();
                break;
            }
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.BUILDING:
            {
                _nextdevtools.dispatcher.buildingIndicatorShow();
                if ("TURBOPACK compile-time truthy", 1) {
                    turbopackHmr.onBuilding();
                } else //TURBOPACK unreachable
                ;
                break;
            }
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.BUILT:
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.SYNC:
            {
                _nextdevtools.dispatcher.buildingIndicatorHide();
                if (message.hash) handleAvailableHash(message.hash);
                const { errors, warnings } = message;
                // Is undefined when it's a 'built' event
                if ('versionInfo' in message) _nextdevtools.dispatcher.onVersionInfo(message.versionInfo);
                if ('devIndicator' in message) _nextdevtools.dispatcher.onDevIndicator(message.devIndicator);
                if ('devToolsConfig' in message) _nextdevtools.dispatcher.onDevToolsConfig(message.devToolsConfig);
                const hasErrors = Boolean(errors && errors.length);
                if (hasErrors) {
                    (0, _websocket.sendMessage)(JSON.stringify({
                        event: 'client-error',
                        errorCount: errors.length,
                        clientId: window.__nextDevClientId
                    }));
                    return handleErrors(errors);
                }
                // NOTE: Turbopack does not currently send warnings
                const hasWarnings = Boolean(warnings && warnings.length);
                if (hasWarnings) {
                    (0, _websocket.sendMessage)(JSON.stringify({
                        event: 'client-warning',
                        warningCount: warnings.length,
                        clientId: window.__nextDevClientId
                    }));
                    return handleWarnings(warnings);
                }
                (0, _websocket.sendMessage)(JSON.stringify({
                    event: 'client-success',
                    clientId: window.__nextDevClientId
                }));
                return handleSuccess();
            }
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.SERVER_COMPONENT_CHANGES:
            {
                turbopackHmr?.onServerComponentChanges();
                if (hasCompileErrors || _runtimeerrorhandler.RuntimeErrorHandler.hadRuntimeError) {
                    window.location.reload();
                }
                return;
            }
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.SERVER_ERROR:
            {
                const { errorJSON } = message;
                if (errorJSON) {
                    const errorObject = JSON.parse(errorJSON);
                    const error = Object.defineProperty(new Error(errorObject.message), "__NEXT_ERROR_CODE", {
                        value: "E394",
                        enumerable: false,
                        configurable: true
                    });
                    error.stack = errorObject.stack;
                    handleErrors([
                        error
                    ]);
                }
                return;
            }
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.TURBOPACK_CONNECTED:
            {
                for (const listener of turbopackMessageListeners){
                    listener({
                        type: _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.TURBOPACK_CONNECTED,
                        data: message.data
                    });
                }
                break;
            }
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.TURBOPACK_MESSAGE:
            {
                turbopackHmr.onTurbopackMessage(message);
                _nextdevtools.dispatcher.onBeforeRefresh();
                for (const listener of turbopackMessageListeners){
                    listener({
                        type: _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.TURBOPACK_MESSAGE,
                        data: message.data
                    });
                }
                if (_runtimeerrorhandler.RuntimeErrorHandler.hadRuntimeError) {
                    console.warn(_shared.REACT_REFRESH_FULL_RELOAD_FROM_ERROR);
                    performFullReload(null);
                }
                _nextdevtools.dispatcher.onRefresh();
                break;
            }
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.ADDED_PAGE:
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.REMOVED_PAGE:
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.RELOAD_PAGE:
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.DEV_PAGES_MANIFEST_UPDATE:
            if (customHmrEventHandler) {
                customHmrEventHandler(message);
            }
            break;
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.DEVTOOLS_CONFIG:
            _nextdevtools.dispatcher.onDevToolsConfig(message.data);
            break;
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.CACHE_INDICATOR:
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.REACT_DEBUG_CHUNK:
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.ERRORS_TO_SHOW_IN_BROWSER:
            break;
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.MIDDLEWARE_CHANGES:
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.CLIENT_CHANGES:
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.SERVER_ONLY_CHANGES:
            break;
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.REQUEST_CURRENT_ERROR_STATE:
            {
                const errorState = (0, _nextdevtools.getSerializedOverlayState)();
                const response = {
                    event: _hotreloadertypes.HMR_MESSAGE_SENT_TO_SERVER.MCP_ERROR_STATE_RESPONSE,
                    requestId: message.requestId,
                    errorState,
                    url: window.location.href
                };
                (0, _websocket.sendMessage)(JSON.stringify(response));
                break;
            }
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.REQUEST_PAGE_METADATA:
            {
                const segmentTrieData = (0, _nextdevtools.getSegmentTrieData)();
                const response = {
                    event: _hotreloadertypes.HMR_MESSAGE_SENT_TO_SERVER.MCP_PAGE_METADATA_RESPONSE,
                    requestId: message.requestId,
                    segmentTrieData,
                    url: window.location.href
                };
                (0, _websocket.sendMessage)(JSON.stringify(response));
                return;
            }
        default:
            message;
    }
}
// Is there a newer version of this code available?
function isUpdateAvailable() {
    /* globals __webpack_hash__ */ // __webpack_hash__ is the hash of the current compilation.
    // It's a global variable injected by Webpack.
    return mostRecentCompilationHash !== __webpack_hash__;
}
// Webpack disallows updates in other states.
function canApplyUpdates() {
    return module.hot.status() === 'idle';
}
function afterApplyUpdates(fn) {
    if (canApplyUpdates()) {
        fn();
    } else {
        function handler(status) {
            if (status === 'idle') {
                module.hot.removeStatusHandler(handler);
                fn();
            }
        }
        module.hot.addStatusHandler(handler);
    }
}
// Attempt to update code on the fly, fall back to a hard reload.
function tryApplyUpdatesWebpack() {
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    if (!isUpdateAvailable() || !canApplyUpdates()) {
        _nextdevtools.dispatcher.onBuildOk();
        return;
    }
    function handleApplyUpdates(err, updatedModules) {
        if (err || _runtimeerrorhandler.RuntimeErrorHandler.hadRuntimeError || updatedModules == null) {
            if (err) {
                console.warn(_shared.REACT_REFRESH_FULL_RELOAD);
            } else if (_runtimeerrorhandler.RuntimeErrorHandler.hadRuntimeError) {
                console.warn(_shared.REACT_REFRESH_FULL_RELOAD_FROM_ERROR);
            }
            performFullReload(err);
            return;
        }
        _nextdevtools.dispatcher.onBuildOk();
        if (isUpdateAvailable()) {
            // While we were updating, there was a new update! Do it again.
            tryApplyUpdatesWebpack();
            return;
        }
        _nextdevtools.dispatcher.onRefresh();
        (0, _reporthmrlatency.default)(_websocket.sendMessage, updatedModules, webpackStartMsSinceEpoch, Date.now());
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
    }
    // https://webpack.js.org/api/hot-module-replacement/#check
    module.hot.check(/* autoApply */ false).then((updatedModules)=>{
        if (updatedModules == null) {
            return null;
        }
        // We should always handle an update, even if updatedModules is empty (but
        // non-null) for any reason. That's what webpack would normally do:
        // https://github.com/webpack/webpack/blob/3aa6b6bc3a64/lib/hmr/HotModuleReplacement.runtime.js#L296-L298
        _nextdevtools.dispatcher.onBeforeRefresh();
        // https://webpack.js.org/api/hot-module-replacement/#apply
        return module.hot.apply();
    }).then((updatedModules)=>{
        handleApplyUpdates(null, updatedModules);
    }, (err)=>{
        handleApplyUpdates(err, null);
    });
}
function performFullReload(err) {
    const stackTrace = err && (err.stack && err.stack.split('\n').slice(0, 5).join('\n') || err.message || err + '');
    (0, _websocket.sendMessage)(JSON.stringify({
        event: 'client-full-reload',
        stackTrace,
        hadRuntimeError: !!_runtimeerrorhandler.RuntimeErrorHandler.hadRuntimeError,
        dependencyChain: err ? err.dependencyChain : undefined
    }));
    window.location.reload();
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/tracing/report-to-socket.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "default", {
    enumerable: true,
    get: function() {
        return reportToSocket;
    }
});
const _websocket = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/pages/websocket.js [client] (ecmascript)");
function reportToSocket(span) {
    if (span.state.state !== 'ended') {
        throw Object.defineProperty(new Error('Expected span to be ended'), "__NEXT_ERROR_CODE", {
            value: "E302",
            enumerable: false,
            configurable: true
        });
    }
    (0, _websocket.sendMessage)(JSON.stringify({
        event: 'span-end',
        startTime: span.startTime,
        endTime: span.state.endTime,
        spanName: span.name,
        attributes: span.attributes
    }));
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/index.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
/* global location */ // imports polyfill from `@next/polyfill-module` after build.
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    emitter: null,
    hydrate: null,
    initialize: null,
    router: null,
    version: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    emitter: function() {
        return emitter;
    },
    hydrate: function() {
        return hydrate;
    },
    initialize: function() {
        return initialize;
    },
    router: function() {
        return router;
    },
    version: function() {
        return version;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [client] (ecmascript)");
const _jsxruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/react@19.2.6/node_modules/react/jsx-runtime.js [client] (ecmascript)");
__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/polyfill-module.js [client] (ecmascript)");
const _react = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/react@19.2.6/node_modules/react/index.js [client] (ecmascript)"));
const _client = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/react-dom@19.2.6_react@19.2.6/node_modules/react-dom/client.js [client] (ecmascript)"));
const _headmanagercontextsharedruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/head-manager-context.shared-runtime.js [client] (ecmascript)");
const _mitt = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/mitt.js [client] (ecmascript)"));
const _routercontextsharedruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router-context.shared-runtime.js [client] (ecmascript)");
const _disablesmoothscroll = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/disable-smooth-scroll.js [client] (ecmascript)");
const _isdynamic = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/is-dynamic.js [client] (ecmascript)");
const _querystring = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/querystring.js [client] (ecmascript)");
const _utils = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/utils.js [client] (ecmascript)");
const _portal = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/portal/index.js [client] (ecmascript)");
const _headmanager = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/head-manager.js [client] (ecmascript)"));
const _pageloader = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/page-loader.js [client] (ecmascript)"));
const _routeannouncer = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/route-announcer.js [client] (ecmascript)");
const _router = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/router.js [client] (ecmascript)");
const _iserror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/is-error.js [client] (ecmascript)");
const _imageconfigcontextsharedruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/image-config-context.shared-runtime.js [client] (ecmascript)");
const _removebasepath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/remove-base-path.js [client] (ecmascript)");
const _hasbasepath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/has-base-path.js [client] (ecmascript)");
const _approutercontextsharedruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/app-router-context.shared-runtime.js [client] (ecmascript)");
const _adapters = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/adapters.js [client] (ecmascript)");
const _hooksclientcontextsharedruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/hooks-client-context.shared-runtime.js [client] (ecmascript)");
const _onrecoverableerror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/react-client-callbacks/on-recoverable-error.js [client] (ecmascript)");
const _tracer = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/tracing/tracer.js [client] (ecmascript)"));
const _isnextroutererror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/is-next-router-error.js [client] (ecmascript)");
const version = "16.2.6";
let router;
const emitter = (0, _mitt.default)();
const looseToArray = (input)=>[].slice.call(input);
let initialData;
let defaultLocale = undefined;
let asPath;
let pageLoader;
let appElement;
let headManager;
let initialMatchesMiddleware = false;
let lastAppProps;
let lastRenderReject;
let devClient;
let CachedApp, onPerfEntry;
let CachedComponent;
class Container extends _react.default.Component {
    componentDidCatch(componentErr, info) {
        this.props.fn(componentErr, info);
    }
    componentDidMount() {
        this.scrollToHash();
        // We need to replace the router state if:
        // - the page was (auto) exported and has a query string or search (hash)
        // - it was auto exported and is a dynamic route (to provide params)
        // - if it is a client-side skeleton (fallback render)
        // - if middleware matches the current page (may have rewrite params)
        // - if rewrites in next.config.js match (may have rewrite params)
        if (router.isSsr && (initialData.isFallback || initialData.nextExport && ((0, _isdynamic.isDynamicRoute)(router.pathname) || location.search || ("TURBOPACK compile-time value", false) || initialMatchesMiddleware) || initialData.props && initialData.props.__N_SSG && (location.search || ("TURBOPACK compile-time value", false) || initialMatchesMiddleware))) {
            // update query on mount for exported pages
            router.replace(router.pathname + '?' + String((0, _querystring.assign)((0, _querystring.urlQueryToSearchParams)(router.query), new URLSearchParams(location.search))), asPath, {
                // @ts-ignore
                // WARNING: `_h` is an internal option for handing Next.js
                // client-side hydration. Your app should _never_ use this property.
                // It may change at any time without notice.
                _h: 1,
                // Fallback pages must trigger the data fetch, so the transition is
                // not shallow.
                // Other pages (strictly updating query) happens shallowly, as data
                // requirements would already be present.
                shallow: !initialData.isFallback && !initialMatchesMiddleware
            }).catch((err)=>{
                if (!err.cancelled) throw err;
            });
        }
    }
    componentDidUpdate() {
        this.scrollToHash();
    }
    scrollToHash() {
        let { hash } = location;
        hash = hash && hash.substring(1);
        if (!hash) return;
        const el = document.getElementById(hash);
        if (!el) return;
        // If we call scrollIntoView() in here without a setTimeout
        // it won't scroll properly.
        setTimeout(()=>el.scrollIntoView(), 0);
    }
    render() {
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
        else {
            const { PagesDevOverlayBridge } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/pages/pages-dev-overlay-setup.js [client] (ecmascript)");
            return /*#__PURE__*/ (0, _jsxruntime.jsx)(PagesDevOverlayBridge, {
                children: this.props.children
            });
        }
    }
}
async function initialize(opts = {}) {
    // This makes sure this specific lines are removed in production
    if ("TURBOPACK compile-time truthy", 1) {
        _tracer.default.onSpanEnd(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/tracing/report-to-socket.js [client] (ecmascript)").default);
        devClient = opts.devClient;
    }
    initialData = JSON.parse(document.getElementById('__NEXT_DATA__').textContent);
    window.__NEXT_DATA__ = initialData;
    defaultLocale = initialData.defaultLocale;
    const prefix = initialData.assetPrefix || '';
    self.__next_set_public_path__(`${prefix}/_next/`);
    asPath = (0, _utils.getURL)();
    // make sure not to attempt stripping basePath for 404s
    if ((0, _hasbasepath.hasBasePath)(asPath)) {
        asPath = (0, _removebasepath.removeBasePath)(asPath);
    }
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    if (initialData.scriptLoader) {
        const { initScriptLoader } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/script.js [client] (ecmascript)");
        initScriptLoader(initialData.scriptLoader);
    }
    pageLoader = new _pageloader.default(initialData.buildId, prefix);
    const register = ([r, f])=>pageLoader.routeLoader.onEntrypoint(r, f);
    if (window.__NEXT_P) {
        // Defer page registration for another tick. This will increase the overall
        // latency in hydrating the page, but reduce the total blocking time.
        window.__NEXT_P.map((p)=>setTimeout(()=>register(p), 0));
    }
    window.__NEXT_P = [];
    window.__NEXT_P.push = register;
    headManager = (0, _headmanager.default)();
    headManager.getIsSsr = ()=>{
        return router.isSsr;
    };
    appElement = document.getElementById('__next');
    return {
        assetPrefix: prefix
    };
}
function renderApp(App, appProps) {
    return /*#__PURE__*/ (0, _jsxruntime.jsx)(App, {
        ...appProps
    });
}
function AppContainer({ children }) {
    // Create a memoized value for next/navigation router context.
    const adaptedForAppRouter = _react.default.useMemo({
        "AppContainer.useMemo[adaptedForAppRouter]": ()=>{
            return (0, _adapters.adaptForAppRouterInstance)(router);
        }
    }["AppContainer.useMemo[adaptedForAppRouter]"], []);
    return /*#__PURE__*/ (0, _jsxruntime.jsx)(Container, {
        fn: (error)=>renderError({
                App: CachedApp,
                err: error
            }).catch((err)=>console.error('Error rendering page: ', err)),
        children: /*#__PURE__*/ (0, _jsxruntime.jsx)(_approutercontextsharedruntime.AppRouterContext.Provider, {
            value: adaptedForAppRouter,
            children: /*#__PURE__*/ (0, _jsxruntime.jsx)(_hooksclientcontextsharedruntime.SearchParamsContext.Provider, {
                value: (0, _adapters.adaptForSearchParams)(router),
                children: /*#__PURE__*/ (0, _jsxruntime.jsx)(_adapters.PathnameContextProviderAdapter, {
                    router: router,
                    isAutoExport: self.__NEXT_DATA__.autoExport ?? false,
                    children: /*#__PURE__*/ (0, _jsxruntime.jsx)(_hooksclientcontextsharedruntime.PathParamsContext.Provider, {
                        value: (0, _adapters.adaptForPathParams)(router),
                        children: /*#__PURE__*/ (0, _jsxruntime.jsx)(_routercontextsharedruntime.RouterContext.Provider, {
                            value: (0, _router.makePublicRouterInstance)(router),
                            children: /*#__PURE__*/ (0, _jsxruntime.jsx)(_headmanagercontextsharedruntime.HeadManagerContext.Provider, {
                                value: headManager,
                                children: /*#__PURE__*/ (0, _jsxruntime.jsx)(_imageconfigcontextsharedruntime.ImageConfigContext.Provider, {
                                    value: ("TURBOPACK compile-time value", {
                                        "deviceSizes": ("TURBOPACK compile-time value", [
                                            ("TURBOPACK compile-time value", 640),
                                            ("TURBOPACK compile-time value", 750),
                                            ("TURBOPACK compile-time value", 828),
                                            ("TURBOPACK compile-time value", 1080),
                                            ("TURBOPACK compile-time value", 1200),
                                            ("TURBOPACK compile-time value", 1920),
                                            ("TURBOPACK compile-time value", 2048),
                                            ("TURBOPACK compile-time value", 3840)
                                        ]),
                                        "imageSizes": ("TURBOPACK compile-time value", [
                                            ("TURBOPACK compile-time value", 32),
                                            ("TURBOPACK compile-time value", 48),
                                            ("TURBOPACK compile-time value", 64),
                                            ("TURBOPACK compile-time value", 96),
                                            ("TURBOPACK compile-time value", 128),
                                            ("TURBOPACK compile-time value", 256),
                                            ("TURBOPACK compile-time value", 384)
                                        ]),
                                        "qualities": ("TURBOPACK compile-time value", [
                                            ("TURBOPACK compile-time value", 75)
                                        ]),
                                        "path": ("TURBOPACK compile-time value", "/_next/image"),
                                        "loader": ("TURBOPACK compile-time value", "default"),
                                        "dangerouslyAllowSVG": ("TURBOPACK compile-time value", false),
                                        "unoptimized": ("TURBOPACK compile-time value", false),
                                        "domains": ("TURBOPACK compile-time value", []),
                                        "remotePatterns": ("TURBOPACK compile-time value", []),
                                        "localPatterns": ("TURBOPACK compile-time value", [
                                            ("TURBOPACK compile-time value", {
                                                "pathname": ("TURBOPACK compile-time value", "**"),
                                                "search": ("TURBOPACK compile-time value", "")
                                            })
                                        ])
                                    }),
                                    children: children
                                })
                            })
                        })
                    })
                })
            })
        })
    });
}
const wrapApp = (App)=>(wrappedAppProps)=>{
        const appProps = {
            ...wrappedAppProps,
            Component: CachedComponent,
            err: initialData.err,
            router
        };
        return /*#__PURE__*/ (0, _jsxruntime.jsx)(AppContainer, {
            children: renderApp(App, appProps)
        });
    };
// This method handles all runtime and debug errors.
// 404 and 500 errors are special kind of errors
// and they are still handle via the main render method.
function renderError(renderErrorProps) {
    let { App, err } = renderErrorProps;
    // In development runtime errors are caught by our overlay
    // In production we catch runtime errors using componentDidCatch which will trigger renderError
    if ("TURBOPACK compile-time truthy", 1) {
        // A Next.js rendering runtime error is always unrecoverable
        // FIXME: let's make this recoverable (error in GIP client-transition)
        devClient.onUnrecoverableError();
        // We need to render an empty <App> so that the `<ReactDevOverlay>` can
        // render itself.
        return doRender({
            App: ()=>null,
            props: {},
            Component: ()=>null,
            styleSheets: []
        });
    }
    //TURBOPACK unreachable
    ;
}
// Dummy component that we render as a child of Root so that we can
// toggle the correct styles before the page is rendered.
function Head({ callback }) {
    // We use `useLayoutEffect` to guarantee the callback is executed
    // as soon as React flushes the update.
    _react.default.useLayoutEffect({
        "Head.useLayoutEffect": ()=>callback()
    }["Head.useLayoutEffect"], [
        callback
    ]);
    return null;
}
const performanceMarks = {
    navigationStart: 'navigationStart',
    beforeRender: 'beforeRender',
    afterRender: 'afterRender',
    afterHydrate: 'afterHydrate',
    routeChange: 'routeChange'
};
const performanceMeasures = {
    hydration: 'Next.js-hydration',
    beforeHydration: 'Next.js-before-hydration',
    routeChangeToRender: 'Next.js-route-change-to-render',
    render: 'Next.js-render'
};
let reactRoot = null;
// On initial render a hydrate should always happen
let shouldHydrate = true;
function clearMarks() {
    ;
    [
        performanceMarks.beforeRender,
        performanceMarks.afterHydrate,
        performanceMarks.afterRender,
        performanceMarks.routeChange
    ].forEach((mark)=>performance.clearMarks(mark));
}
function markHydrateComplete() {
    if (!_utils.ST) return;
    performance.mark(performanceMarks.afterHydrate) // mark end of hydration
    ;
    const hasBeforeRenderMark = performance.getEntriesByName(performanceMarks.beforeRender, 'mark').length;
    if (hasBeforeRenderMark) {
        const beforeHydrationMeasure = performance.measure(performanceMeasures.beforeHydration, performanceMarks.navigationStart, performanceMarks.beforeRender);
        const hydrationMeasure = performance.measure(performanceMeasures.hydration, performanceMarks.beforeRender, performanceMarks.afterHydrate);
        if (("TURBOPACK compile-time value", "development") === 'development' && // Old versions of Safari don't return `PerformanceMeasure`s from `performance.measure()`
        beforeHydrationMeasure && hydrationMeasure) {
            _tracer.default.startSpan('navigation-to-hydration', {
                startTime: performance.timeOrigin + beforeHydrationMeasure.startTime,
                attributes: {
                    pathname: location.pathname,
                    query: location.search
                }
            }).end(performance.timeOrigin + hydrationMeasure.startTime + hydrationMeasure.duration);
        }
    }
    if (onPerfEntry) {
        performance.getEntriesByName(performanceMeasures.hydration).forEach(onPerfEntry);
    }
    clearMarks();
}
function markRenderComplete() {
    if (!_utils.ST) return;
    performance.mark(performanceMarks.afterRender) // mark end of render
    ;
    const navStartEntries = performance.getEntriesByName(performanceMarks.routeChange, 'mark');
    if (!navStartEntries.length) return;
    const hasBeforeRenderMark = performance.getEntriesByName(performanceMarks.beforeRender, 'mark').length;
    if (hasBeforeRenderMark) {
        performance.measure(performanceMeasures.routeChangeToRender, navStartEntries[0].name, performanceMarks.beforeRender);
        performance.measure(performanceMeasures.render, performanceMarks.beforeRender, performanceMarks.afterRender);
        if (onPerfEntry) {
            performance.getEntriesByName(performanceMeasures.render).forEach(onPerfEntry);
            performance.getEntriesByName(performanceMeasures.routeChangeToRender).forEach(onPerfEntry);
        }
    }
    clearMarks();
    [
        performanceMeasures.routeChangeToRender,
        performanceMeasures.render
    ].forEach((measure)=>performance.clearMeasures(measure));
}
function renderReactElement(domEl, fn) {
    // mark start of hydrate/render
    if (_utils.ST) {
        performance.mark(performanceMarks.beforeRender);
    }
    const reactEl = fn(shouldHydrate ? markHydrateComplete : markRenderComplete);
    if (!reactRoot) {
        // Unlike with createRoot, you don't need a separate root.render() call here
        reactRoot = _client.default.hydrateRoot(domEl, reactEl, {
            onRecoverableError: _onrecoverableerror.onRecoverableError
        });
        // TODO: Remove shouldHydrate variable when React 18 is stable as it can depend on `reactRoot` existing
        shouldHydrate = false;
    } else {
        const startTransition = _react.default.startTransition;
        startTransition(()=>{
            reactRoot.render(reactEl);
        });
    }
}
function Root({ callbacks, children }) {
    // We use `useLayoutEffect` to guarantee the callbacks are executed
    // as soon as React flushes the update
    _react.default.useLayoutEffect({
        "Root.useLayoutEffect": ()=>callbacks.forEach({
                "Root.useLayoutEffect": (callback)=>callback()
            }["Root.useLayoutEffect"])
    }["Root.useLayoutEffect"], [
        callbacks
    ]);
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    return children;
}
function doRender(input) {
    let { App, Component, props, err } = input;
    let styleSheets = 'initial' in input ? undefined : input.styleSheets;
    Component = Component || lastAppProps.Component;
    props = props || lastAppProps.props;
    const appProps = {
        ...props,
        Component,
        err,
        router
    };
    // lastAppProps has to be set before ReactDom.render to account for ReactDom throwing an error.
    lastAppProps = appProps;
    let canceled = false;
    let resolvePromise;
    const renderPromise = new Promise((resolve, reject)=>{
        if (lastRenderReject) {
            lastRenderReject();
        }
        resolvePromise = ()=>{
            lastRenderReject = null;
            resolve();
        };
        lastRenderReject = ()=>{
            canceled = true;
            lastRenderReject = null;
            const error = Object.defineProperty(new Error('Cancel rendering route'), "__NEXT_ERROR_CODE", {
                value: "E503",
                enumerable: false,
                configurable: true
            });
            error.cancelled = true;
            reject(error);
        };
    });
    // This function has a return type to ensure it doesn't start returning a
    // Promise. It should remain synchronous.
    function onStart() {
        if ("TURBOPACK compile-time truthy", 1) {
            return false;
        }
        //TURBOPACK unreachable
        ;
        const currentStyleTags = undefined;
        const currentHrefs = undefined;
        const noscript = undefined;
        const nonce = undefined;
    }
    function onHeadCommit() {
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
        if (input.scroll) {
            const { x, y } = input.scroll;
            (0, _disablesmoothscroll.disableSmoothScrollDuringRouteTransition)(()=>{
                window.scrollTo(x, y);
            });
        }
    }
    function onRootCommit() {
        resolvePromise();
    }
    onStart();
    const elem = /*#__PURE__*/ (0, _jsxruntime.jsxs)(_jsxruntime.Fragment, {
        children: [
            /*#__PURE__*/ (0, _jsxruntime.jsx)(Head, {
                callback: onHeadCommit
            }),
            /*#__PURE__*/ (0, _jsxruntime.jsxs)(AppContainer, {
                children: [
                    renderApp(App, appProps),
                    /*#__PURE__*/ (0, _jsxruntime.jsx)(_portal.Portal, {
                        type: "next-route-announcer",
                        children: /*#__PURE__*/ (0, _jsxruntime.jsx)(_routeannouncer.RouteAnnouncer, {})
                    })
                ]
            })
        ]
    });
    // We catch runtime errors using componentDidCatch which will trigger renderError
    renderReactElement(appElement, (callback)=>/*#__PURE__*/ (0, _jsxruntime.jsx)(Root, {
            callbacks: [
                callback,
                onRootCommit
            ],
            children: ("TURBOPACK compile-time falsy", 0) ? /*#__PURE__*/ "TURBOPACK unreachable" : elem
        }));
    return renderPromise;
}
async function render(renderingProps) {
    // if an error occurs in a server-side page (e.g. in getInitialProps),
    // skip re-rendering the error page client-side as data-fetching operations
    // will already have been done on the server and NEXT_DATA contains the correct
    // data for straight-forward hydration of the error page
    if (renderingProps.err && // renderingProps.Component might be undefined if there is a top/module-level error
    (typeof renderingProps.Component === 'undefined' || !renderingProps.isHydratePass)) {
        await renderError(renderingProps);
        return;
    }
    try {
        await doRender(renderingProps);
    } catch (err) {
        const renderErr = (0, _iserror.getProperError)(err);
        // bubble up cancelation errors
        if (renderErr.cancelled) {
            throw renderErr;
        }
        if ("TURBOPACK compile-time truthy", 1) {
            // Ensure this error is displayed in the overlay in development
            setTimeout(()=>{
                throw renderErr;
            });
        }
        await renderError({
            ...renderingProps,
            err: renderErr
        });
    }
}
async function hydrate(opts) {
    let initialErr = initialData.err;
    try {
        const appEntrypoint = await pageLoader.routeLoader.whenEntrypoint('/_app');
        if ('error' in appEntrypoint) {
            throw appEntrypoint.error;
        }
        const { component: app, exports: mod } = appEntrypoint;
        CachedApp = app;
        if (mod && mod.reportWebVitals) {
            onPerfEntry = ({ id, name, startTime, value, duration, entryType, entries, attribution })=>{
                // Combines timestamp with random number for unique ID
                const uniqueID = `${Date.now()}-${Math.floor(Math.random() * (9e12 - 1)) + 1e12}`;
                let perfStartEntry;
                if (entries && entries.length) {
                    perfStartEntry = entries[0].startTime;
                }
                const webVitals = {
                    id: id || uniqueID,
                    name,
                    startTime: startTime || perfStartEntry,
                    value: value == null ? duration : value,
                    label: entryType === 'mark' || entryType === 'measure' ? 'custom' : 'web-vital'
                };
                if (attribution) {
                    webVitals.attribution = attribution;
                }
                mod.reportWebVitals(webVitals);
            };
        }
        const pageEntrypoint = // error, so we need to skip waiting for the entrypoint.
        ("TURBOPACK compile-time value", "development") === 'development' && initialData.err ? {
            error: initialData.err
        } : await pageLoader.routeLoader.whenEntrypoint(initialData.page);
        if ('error' in pageEntrypoint) {
            throw pageEntrypoint.error;
        }
        CachedComponent = pageEntrypoint.component;
        if ("TURBOPACK compile-time truthy", 1) {
            const { isValidElementType } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-is/index.js [client] (ecmascript)");
            if (!isValidElementType(CachedComponent)) {
                throw Object.defineProperty(new Error(`The default export is not a React Component in page: "${initialData.page}"`), "__NEXT_ERROR_CODE", {
                    value: "E286",
                    enumerable: false,
                    configurable: true
                });
            }
        }
    } catch (error) {
        // This catches errors like throwing in the top level of a module
        initialErr = (0, _iserror.getProperError)(error);
    }
    if ("TURBOPACK compile-time truthy", 1) {
        const getServerError = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/server/dev/node-stack-frames.js [client] (ecmascript)").getServerError;
        // Server-side runtime errors need to be re-thrown on the client-side so
        // that the overlay is rendered.
        if (initialErr) {
            if (initialErr === initialData.err) {
                setTimeout(()=>{
                    let error;
                    try {
                        // Generate a new error object. We `throw` it because some browsers
                        // will set the `stack` when thrown, and we want to ensure ours is
                        // not overridden when we re-throw it below.
                        throw Object.defineProperty(new Error(initialErr.message), "__NEXT_ERROR_CODE", {
                            value: "E394",
                            enumerable: false,
                            configurable: true
                        });
                    } catch (e) {
                        error = e;
                    }
                    error.name = initialErr.name;
                    error.stack = initialErr.stack;
                    const errSource = initialErr.source;
                    // In development, error the navigation API usage in runtime,
                    // since it's not allowed to be used in pages router as it doesn't contain error boundary like app router.
                    if ((0, _isnextroutererror.isNextRouterError)(initialErr)) {
                        error.message = 'Next.js navigation API is not allowed to be used in Pages Router.';
                    }
                    throw getServerError(error, errSource);
                });
            } else {
                setTimeout(()=>{
                    throw initialErr;
                });
            }
        }
    }
    if (window.__NEXT_PRELOADREADY) {
        await window.__NEXT_PRELOADREADY(initialData.dynamicIds);
    }
    router = (0, _router.createRouter)(initialData.page, initialData.query, asPath, {
        initialProps: initialData.props,
        pageLoader,
        App: CachedApp,
        Component: CachedComponent,
        wrapApp,
        err: initialErr,
        isFallback: Boolean(initialData.isFallback),
        subscription: (info, App, scroll)=>render(Object.assign({}, info, {
                App,
                scroll
            })),
        locale: initialData.locale,
        locales: initialData.locales,
        defaultLocale,
        domainLocales: initialData.domainLocales,
        isPreview: initialData.isPreview
    });
    initialMatchesMiddleware = await router._initialMatchesMiddlewarePromise;
    const renderCtx = {
        App: CachedApp,
        initial: true,
        Component: CachedComponent,
        props: initialData.props,
        err: initialErr,
        isHydratePass: true
    };
    if (opts?.beforeRender) {
        await opts.beforeRender();
    }
    render(renderCtx);
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-middleware-client.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "default", {
    enumerable: true,
    get: function() {
        return _default;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [client] (ecmascript)");
const _hotreloadertypes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/server/dev/hot-reloader-types.js [client] (ecmascript)");
const _hotreloaderpages = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/pages/hot-reloader-pages.js [client] (ecmascript)"));
const _websocket = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/pages/websocket.js [client] (ecmascript)");
let reloading = false;
const _default = ()=>{
    const devClient = (0, _hotreloaderpages.default)();
    devClient.subscribeToHmrEvent((message)=>{
        if (reloading) return;
        // Retrieve the router if it's available
        const router = window.next?.router;
        // Determine if we're on an error page or the router is not initialized
        const isOnErrorPage = !router || router.pathname === '/404' || router.pathname === '/_error';
        switch(message.type){
            case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.RELOAD_PAGE:
                {
                    (0, _websocket.sendMessage)(JSON.stringify({
                        event: 'client-reload-page',
                        clientId: window.__nextDevClientId
                    }));
                    reloading = true;
                    return window.location.reload();
                }
            case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.REMOVED_PAGE:
                {
                    const [page] = message.data;
                    // Check if the removed page is the current page
                    const isCurrentPage = page === router?.pathname;
                    // We enter here if the removed page is currently being viewed
                    // or if we happen to be on an error page.
                    if (isCurrentPage || isOnErrorPage) {
                        (0, _websocket.sendMessage)(JSON.stringify({
                            event: 'client-removed-page',
                            clientId: window.__nextDevClientId,
                            page
                        }));
                        return window.location.reload();
                    }
                    return;
                }
            case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.ADDED_PAGE:
                {
                    const [page] = message.data;
                    // Check if the added page is the current page
                    const isCurrentPage = page === router?.pathname;
                    // Check if the page component is not yet loaded
                    const isPageNotLoaded = page !== null && typeof router?.components?.[page] === 'undefined';
                    // We enter this block if the newly added page is the one currently being viewed
                    // but hasn't been loaded yet, or if we're on an error page.
                    if (isCurrentPage && isPageNotLoaded || isOnErrorPage) {
                        (0, _websocket.sendMessage)(JSON.stringify({
                            event: 'client-added-page',
                            clientId: window.__nextDevClientId,
                            page
                        }));
                        return window.location.reload();
                    }
                    return;
                }
            case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.DEV_PAGES_MANIFEST_UPDATE:
                {
                    return;
                }
            default:
                {
                    message;
                }
        }
    });
    return devClient;
};
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/on-demand-entries-client.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "default", {
    enumerable: true,
    get: function() {
        return _default;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [client] (ecmascript)");
const _router = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/router.js [client] (ecmascript)"));
const _websocket = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/pages/websocket.js [client] (ecmascript)");
const _default = async ()=>{
    // Never send pings when using Turbopack as it's not used.
    // Pings were originally used to keep track of active routes in on-demand-entries with webpack.
    if ("TURBOPACK compile-time truthy", 1) {
        return;
    }
    //TURBOPACK unreachable
    ;
};
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/fouc.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

// This wrapper function is used to safely select the best available function
// to schedule removal of the no-FOUC styles workaround. requestAnimationFrame
// is the ideal choice, but when used in iframes, there are no guarantees that
// the callback will actually be called, which could stall the promise returned
// from displayContent.
//
// See: https://www.vector-logic.com/blog/posts/on-request-animation-frame-and-embedded-iframes
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "displayContent", {
    enumerable: true,
    get: function() {
        return displayContent;
    }
});
const safeCallbackQueue = (callback)=>{
    if (window.requestAnimationFrame && window.self === window.top) {
        window.requestAnimationFrame(callback);
    } else {
        window.setTimeout(callback);
    }
};
function displayContent() {
    return new Promise((resolve)=>{
        safeCallbackQueue(function() {
            for(var x = document.querySelectorAll('[data-next-hide-fouc]'), i = x.length; i--;){
                x[i].parentNode.removeChild(x[i]);
            }
            resolve();
        });
    });
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/page-bootstrap.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "pageBootstrap", {
    enumerable: true,
    get: function() {
        return pageBootstrap;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [client] (ecmascript)");
__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/require-instrumentation-client.js [client] (ecmascript)");
const _ = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/index.js [client] (ecmascript)");
const _ondemandentriesclient = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/on-demand-entries-client.js [client] (ecmascript)"));
const _fouc = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/fouc.js [client] (ecmascript)");
const _websocket = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/pages/websocket.js [client] (ecmascript)");
const _querystring = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/querystring.js [client] (ecmascript)");
const _hotreloadertypes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/server/dev/hot-reloader-types.js [client] (ecmascript)");
const _runtimeerrorhandler = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/runtime-error-handler.js [client] (ecmascript)");
const _shared = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/shared.js [client] (ecmascript)");
const _hotreloaderpages = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/pages/hot-reloader-pages.js [client] (ecmascript)");
const _nextdevtools = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/next-devtools/index.js (raw)");
function pageBootstrap(assetPrefix) {
    (0, _websocket.connectHMR)({
        assetPrefix,
        path: '/_next/webpack-hmr'
    });
    return (0, _.hydrate)({
        beforeRender: _fouc.displayContent
    }).then(()=>{
        (0, _ondemandentriesclient.default)();
        let reloading = false;
        (0, _websocket.addMessageListener)((message)=>{
            if (reloading) return;
            switch(message.type){
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.SERVER_ERROR:
                    {
                        const errorObject = JSON.parse(message.errorJSON);
                        const error = Object.defineProperty(new Error(errorObject.message), "__NEXT_ERROR_CODE", {
                            value: "E394",
                            enumerable: false,
                            configurable: true
                        });
                        error.stack = errorObject.stack;
                        throw error;
                    }
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.RELOAD_PAGE:
                    {
                        reloading = true;
                        window.location.reload();
                        break;
                    }
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.DEV_PAGES_MANIFEST_UPDATE:
                    {
                        fetch(`${assetPrefix}/_next/static/development/_devPagesManifest.json`).then((res)=>res.json()).then((manifest)=>{
                            window.__DEV_PAGES_MANIFEST = manifest;
                        }).catch((err)=>{
                            console.log(`Failed to fetch devPagesManifest`, err);
                        });
                        break;
                    }
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.MIDDLEWARE_CHANGES:
                    {
                        return window.location.reload();
                    }
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.CLIENT_CHANGES:
                    {
                        // This is used in `../server/dev/turbopack-utils.ts`.
                        const isOnErrorPage = window.next.router.pathname === '/_error';
                        // On the error page we want to reload the page when a page was changed
                        if (isOnErrorPage) {
                            if (_runtimeerrorhandler.RuntimeErrorHandler.hadRuntimeError) {
                                console.warn(_shared.REACT_REFRESH_FULL_RELOAD_FROM_ERROR);
                            }
                            reloading = true;
                            (0, _hotreloaderpages.performFullReload)(null);
                        }
                        break;
                    }
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.SERVER_ONLY_CHANGES:
                    {
                        if (_runtimeerrorhandler.RuntimeErrorHandler.hadRuntimeError) {
                            console.warn(_shared.REACT_REFRESH_FULL_RELOAD_FROM_ERROR);
                            (0, _hotreloaderpages.performFullReload)(null);
                        }
                        const { pages } = message;
                        // Make sure to reload when the dev-overlay is showing for an
                        // API route
                        // TODO: Fix `__NEXT_PAGE` type
                        if (pages.includes(_.router.query.__NEXT_PAGE)) {
                            return window.location.reload();
                        }
                        if (!_.router.clc && pages.includes(_.router.pathname)) {
                            console.log('Refreshing page data due to server-side change');
                            _nextdevtools.dispatcher.buildingIndicatorShow();
                            const clearIndicator = _nextdevtools.dispatcher.buildingIndicatorHide;
                            _.router.replace(_.router.pathname + '?' + String((0, _querystring.assign)((0, _querystring.urlQueryToSearchParams)(_.router.query), new URLSearchParams(location.search))), _.router.asPath, {
                                scroll: false
                            }).catch(()=>{
                                // trigger hard reload when failing to refresh data
                                // to show error overlay properly
                                location.reload();
                            }).finally(clearIndicator);
                        }
                        break;
                    }
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.ADDED_PAGE:
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.REMOVED_PAGE:
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.SERVER_COMPONENT_CHANGES:
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.SYNC:
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.BUILT:
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.BUILDING:
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.TURBOPACK_MESSAGE:
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.TURBOPACK_CONNECTED:
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.ISR_MANIFEST:
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.DEVTOOLS_CONFIG:
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.REACT_DEBUG_CHUNK:
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.REQUEST_CURRENT_ERROR_STATE:
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.REQUEST_PAGE_METADATA:
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.CACHE_INDICATOR:
                case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.ERRORS_TO_SHOW_IN_BROWSER:
                    break;
                default:
                    message;
            }
        });
    });
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/next-dev-turbopack.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

// TODO: Remove use of `any` type.
Object.defineProperty(exports, "__esModule", {
    value: true
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [client] (ecmascript)");
__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/register-deployment-id-global.js [client] (ecmascript)");
const _ = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/index.js [client] (ecmascript)");
const _hotmiddlewareclient = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-middleware-client.js [client] (ecmascript)"));
const _pagebootstrap = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/page-bootstrap.js [client] (ecmascript)");
const _hmrclientts = __turbopack_context__.r("[turbopack]/browser/dev/hmr-client/hmr-client.ts [client] (ecmascript)");
window.next = {
    version: _.version,
    turbopack: true,
    // router is initialized later so it has to be live-binded
    get router () {
        return _.router;
    },
    emitter: _.emitter
};
self.__next_set_public_path__ = ()=>{};
self.__webpack_hash__ = '';
const devClient = (0, _hotmiddlewareclient.default)();
(0, _.initialize)({
    devClient
}).then(({ assetPrefix })=>{
    // for the page loader
    ;
    self.__turbopack_load_page_chunks__ = (page, chunksData)=>{
        const chunkPromises = chunksData.map((c)=>/*TURBOPACK member replacement*/ __turbopack_context__.l(c));
        Promise.all(chunkPromises).catch((err)=>console.error('failed to load chunks for page ' + page, err));
    };
    (0, _hmrclientts.connect)({
        addMessageListener (cb) {
            devClient.addTurbopackMessageListener(cb);
        },
        sendMessage: devClient.sendTurbopackMessage,
        onUpdateError: devClient.handleUpdateError
    });
    return (0, _pagebootstrap.pageBootstrap)(assetPrefix);
}).catch((err)=>{
    console.error('Error was not caught', err);
});
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
]);

//# sourceMappingURL=08c5_next_dist_client_0yl.0ti._.js.map