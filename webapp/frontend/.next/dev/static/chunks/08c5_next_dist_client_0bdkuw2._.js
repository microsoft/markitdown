(globalThis["TURBOPACK"] || (globalThis["TURBOPACK"] = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/register-deployment-id-global.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
const _deploymentid = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/deployment-id.js [app-client] (ecmascript)");
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/asset-prefix.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "getAssetPrefix", {
    enumerable: true,
    get: function() {
        return getAssetPrefix;
    }
});
const _invarianterror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/invariant-error.js [app-client] (ecmascript)");
function getAssetPrefix() {
    const currentScript = document.currentScript;
    if (!(currentScript instanceof HTMLScriptElement)) {
        throw Object.defineProperty(new _invarianterror.InvariantError(`Expected document.currentScript to be a <script> element. Received ${currentScript} instead.`), "__NEXT_ERROR_CODE", {
            value: "E783",
            enumerable: false,
            configurable: true
        });
    }
    const { pathname } = new URL(currentScript.src);
    const nextIndex = pathname.indexOf('/_next/');
    if (nextIndex === -1) {
        throw Object.defineProperty(new _invarianterror.InvariantError(`Expected document.currentScript src to contain '/_next/'. Received ${currentScript.src} instead.`), "__NEXT_ERROR_CODE", {
            value: "E784",
            enumerable: false,
            configurable: true
        });
    }
    return pathname.slice(0, nextIndex);
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/set-attributes-from-props.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/app-bootstrap.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
/**
 * Before starting the Next.js runtime and requiring any module, we need to make
 * sure the following scripts are executed in the correct order:
 * - Polyfills
 * - next/script with `beforeInteractive` strategy
 */ "use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "appBootstrap", {
    enumerable: true,
    get: function() {
        return appBootstrap;
    }
});
const _assetprefix = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/asset-prefix.js [app-client] (ecmascript)");
const _setattributesfromprops = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/set-attributes-from-props.js [app-client] (ecmascript)");
const version = "16.2.6";
window.next = {
    version,
    appDir: true
};
function loadScriptsInSequence(scripts, hydrate) {
    if (!scripts || !scripts.length) {
        return hydrate();
    }
    return scripts.reduce((promise, [src, props])=>{
        return promise.then(()=>{
            return new Promise((resolve, reject)=>{
                const el = document.createElement('script');
                if (props) {
                    (0, _setattributesfromprops.setAttributesFromProps)(el, props);
                }
                if (src) {
                    el.src = src;
                    el.onload = ()=>resolve();
                    el.onerror = reject;
                } else if (props) {
                    el.innerHTML = props.children;
                    setTimeout(resolve);
                }
                document.head.appendChild(el);
            });
        });
    }, Promise.resolve()).catch((err)=>{
        console.error(err);
    // Still try to hydrate even if there's an error.
    }).then(()=>{
        hydrate();
    });
}
function appBootstrap(hydrate) {
    const assetPrefix = (0, _assetprefix.getAssetPrefix)();
    loadScriptsInSequence(self.__next_s, ()=>{
        // If the static shell is being debugged, skip hydration if the
        // `__nextppronly` query is present. This is only enabled when the
        // environment variable `__NEXT_EXPERIMENTAL_STATIC_SHELL_DEBUGGING` is
        // set to `1`. Otherwise the following is optimized out.
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
        hydrate(assetPrefix);
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/react-client-callbacks/report-global-error.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/react-client-callbacks/on-recoverable-error.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
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
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [app-client] (ecmascript)");
const _bailouttocsr = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/lazy-dynamic/bailout-to-csr.js [app-client] (ecmascript)");
const _iserror = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/is-error.js [app-client] (ecmascript)"));
const _reportglobalerror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/react-client-callbacks/report-global-error.js [app-client] (ecmascript)");
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
        const { decorateDevError } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/errors/stitched-error.js [app-client] (ecmascript)");
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/http-access-fallback/http-access-fallback.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/redirect-status-code.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/redirect-error.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
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
const _redirectstatuscode = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/redirect-status-code.js [app-client] (ecmascript)");
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/is-next-router-error.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
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
const _httpaccessfallback = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/http-access-fallback/http-access-fallback.js [app-client] (ecmascript)");
const _redirecterror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/redirect-error.js [app-client] (ecmascript)");
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/lib/console.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    formatConsoleArgs: null,
    parseConsoleArgs: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    formatConsoleArgs: function() {
        return formatConsoleArgs;
    },
    parseConsoleArgs: function() {
        return parseConsoleArgs;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [app-client] (ecmascript)");
const _iserror = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/is-error.js [app-client] (ecmascript)"));
function formatObject(arg, depth) {
    switch(typeof arg){
        case 'object':
            if (arg === null) {
                return 'null';
            } else if (Array.isArray(arg)) {
                let result = '[';
                if (depth < 1) {
                    for(let i = 0; i < arg.length; i++){
                        if (result !== '[') {
                            result += ',';
                        }
                        if (Object.prototype.hasOwnProperty.call(arg, i)) {
                            result += formatObject(arg[i], depth + 1);
                        }
                    }
                } else {
                    result += arg.length > 0 ? '...' : '';
                }
                result += ']';
                return result;
            } else if (arg instanceof Error) {
                return arg + '';
            } else {
                const keys = Object.keys(arg);
                let result = '{';
                if (depth < 1) {
                    for(let i = 0; i < keys.length; i++){
                        const key = keys[i];
                        const desc = Object.getOwnPropertyDescriptor(arg, 'key');
                        if (desc && !desc.get && !desc.set) {
                            const jsonKey = JSON.stringify(key);
                            if (jsonKey !== '"' + key + '"') {
                                result += jsonKey + ': ';
                            } else {
                                result += key + ': ';
                            }
                            result += formatObject(desc.value, depth + 1);
                        }
                    }
                } else {
                    result += keys.length > 0 ? '...' : '';
                }
                result += '}';
                return result;
            }
        case 'string':
            return JSON.stringify(arg);
        case 'number':
        case 'bigint':
        case 'boolean':
        case 'symbol':
        case 'undefined':
        case 'function':
        default:
            return String(arg);
    }
}
function formatConsoleArgs(args) {
    let message;
    let idx;
    if (typeof args[0] === 'string') {
        message = args[0];
        idx = 1;
    } else {
        message = '';
        idx = 0;
    }
    let result = '';
    let startQuote = false;
    for(let i = 0; i < message.length; ++i){
        const char = message[i];
        if (char !== '%' || i === message.length - 1 || idx >= args.length) {
            result += char;
            continue;
        }
        const code = message[++i];
        switch(code){
            case 'c':
                {
                    // TODO: We should colorize with HTML instead of turning into a string.
                    // Ignore for now.
                    result = startQuote ? `${result}]` : `[${result}`;
                    startQuote = !startQuote;
                    idx++;
                    break;
                }
            case 'O':
            case 'o':
                {
                    result += formatObject(args[idx++], 0);
                    break;
                }
            case 'd':
            case 'i':
                {
                    result += parseInt(args[idx++], 10);
                    break;
                }
            case 'f':
                {
                    result += parseFloat(args[idx++]);
                    break;
                }
            case 's':
                {
                    result += String(args[idx++]);
                    break;
                }
            default:
                result += '%' + code;
        }
    }
    for(; idx < args.length; idx++){
        result += (idx > 0 ? ' ' : '') + formatObject(args[idx], 0);
    }
    return result;
}
function parseConsoleArgs(args) {
    // See
    // https://github.com/facebook/react/blob/65a56d0e99261481c721334a3ec4561d173594cd/packages/react-devtools-shared/src/backend/flight/renderer.js#L88-L93
    //
    // Logs replayed from the server look like this:
    // [
    //   "%c%s%c%o\n\n%s\n\n%s\n",
    //   "background: #e6e6e6; ...",
    //   " Server ", // can also be e.g. " Prerender "
    //   "",
    //   Error,
    //   "The above error occurred in the <Page> component.",
    //   ...
    // ]
    if (args.length > 3 && typeof args[0] === 'string' && args[0].startsWith('%c%s%c') && typeof args[1] === 'string' && typeof args[2] === 'string' && typeof args[3] === 'string') {
        const environmentName = args[2];
        const maybeError = args[4];
        return {
            environmentName: environmentName.trim(),
            error: (0, _iserror.default)(maybeError) ? maybeError : null
        };
    }
    return {
        environmentName: null,
        error: null
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-headers.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    ACTION_HEADER: null,
    FLIGHT_HEADERS: null,
    NEXT_ACTION_NOT_FOUND_HEADER: null,
    NEXT_ACTION_REVALIDATED_HEADER: null,
    NEXT_DID_POSTPONE_HEADER: null,
    NEXT_HMR_REFRESH_HASH_COOKIE: null,
    NEXT_HMR_REFRESH_HEADER: null,
    NEXT_HTML_REQUEST_ID_HEADER: null,
    NEXT_INSTANT_PREFETCH_HEADER: null,
    NEXT_INSTANT_TEST_COOKIE: null,
    NEXT_IS_PRERENDER_HEADER: null,
    NEXT_REQUEST_ID_HEADER: null,
    NEXT_REWRITTEN_PATH_HEADER: null,
    NEXT_REWRITTEN_QUERY_HEADER: null,
    NEXT_ROUTER_PREFETCH_HEADER: null,
    NEXT_ROUTER_SEGMENT_PREFETCH_HEADER: null,
    NEXT_ROUTER_STALE_TIME_HEADER: null,
    NEXT_ROUTER_STATE_TREE_HEADER: null,
    NEXT_RSC_UNION_QUERY: null,
    NEXT_URL: null,
    RSC_CONTENT_TYPE_HEADER: null,
    RSC_HEADER: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    ACTION_HEADER: function() {
        return ACTION_HEADER;
    },
    FLIGHT_HEADERS: function() {
        return FLIGHT_HEADERS;
    },
    NEXT_ACTION_NOT_FOUND_HEADER: function() {
        return NEXT_ACTION_NOT_FOUND_HEADER;
    },
    NEXT_ACTION_REVALIDATED_HEADER: function() {
        return NEXT_ACTION_REVALIDATED_HEADER;
    },
    NEXT_DID_POSTPONE_HEADER: function() {
        return NEXT_DID_POSTPONE_HEADER;
    },
    NEXT_HMR_REFRESH_HASH_COOKIE: function() {
        return NEXT_HMR_REFRESH_HASH_COOKIE;
    },
    NEXT_HMR_REFRESH_HEADER: function() {
        return NEXT_HMR_REFRESH_HEADER;
    },
    NEXT_HTML_REQUEST_ID_HEADER: function() {
        return NEXT_HTML_REQUEST_ID_HEADER;
    },
    NEXT_INSTANT_PREFETCH_HEADER: function() {
        return NEXT_INSTANT_PREFETCH_HEADER;
    },
    NEXT_INSTANT_TEST_COOKIE: function() {
        return NEXT_INSTANT_TEST_COOKIE;
    },
    NEXT_IS_PRERENDER_HEADER: function() {
        return NEXT_IS_PRERENDER_HEADER;
    },
    NEXT_REQUEST_ID_HEADER: function() {
        return NEXT_REQUEST_ID_HEADER;
    },
    NEXT_REWRITTEN_PATH_HEADER: function() {
        return NEXT_REWRITTEN_PATH_HEADER;
    },
    NEXT_REWRITTEN_QUERY_HEADER: function() {
        return NEXT_REWRITTEN_QUERY_HEADER;
    },
    NEXT_ROUTER_PREFETCH_HEADER: function() {
        return NEXT_ROUTER_PREFETCH_HEADER;
    },
    NEXT_ROUTER_SEGMENT_PREFETCH_HEADER: function() {
        return NEXT_ROUTER_SEGMENT_PREFETCH_HEADER;
    },
    NEXT_ROUTER_STALE_TIME_HEADER: function() {
        return NEXT_ROUTER_STALE_TIME_HEADER;
    },
    NEXT_ROUTER_STATE_TREE_HEADER: function() {
        return NEXT_ROUTER_STATE_TREE_HEADER;
    },
    NEXT_RSC_UNION_QUERY: function() {
        return NEXT_RSC_UNION_QUERY;
    },
    NEXT_URL: function() {
        return NEXT_URL;
    },
    RSC_CONTENT_TYPE_HEADER: function() {
        return RSC_CONTENT_TYPE_HEADER;
    },
    RSC_HEADER: function() {
        return RSC_HEADER;
    }
});
const RSC_HEADER = 'rsc';
const ACTION_HEADER = 'next-action';
const NEXT_ROUTER_STATE_TREE_HEADER = 'next-router-state-tree';
const NEXT_ROUTER_PREFETCH_HEADER = 'next-router-prefetch';
const NEXT_ROUTER_SEGMENT_PREFETCH_HEADER = 'next-router-segment-prefetch';
const NEXT_HMR_REFRESH_HEADER = 'next-hmr-refresh';
const NEXT_HMR_REFRESH_HASH_COOKIE = '__next_hmr_refresh_hash__';
const NEXT_URL = 'next-url';
const RSC_CONTENT_TYPE_HEADER = 'text/x-component';
const NEXT_INSTANT_PREFETCH_HEADER = 'next-instant-navigation-testing-prefetch';
const NEXT_INSTANT_TEST_COOKIE = 'next-instant-navigation-testing';
const FLIGHT_HEADERS = [
    RSC_HEADER,
    NEXT_ROUTER_STATE_TREE_HEADER,
    NEXT_ROUTER_PREFETCH_HEADER,
    NEXT_HMR_REFRESH_HEADER,
    NEXT_ROUTER_SEGMENT_PREFETCH_HEADER
];
const NEXT_RSC_UNION_QUERY = '_rsc';
const NEXT_ROUTER_STALE_TIME_HEADER = 'x-nextjs-stale-time';
const NEXT_DID_POSTPONE_HEADER = 'x-nextjs-postponed';
const NEXT_REWRITTEN_PATH_HEADER = 'x-nextjs-rewritten-path';
const NEXT_REWRITTEN_QUERY_HEADER = 'x-nextjs-rewritten-query';
const NEXT_IS_PRERENDER_HEADER = 'x-nextjs-prerender';
const NEXT_ACTION_NOT_FOUND_HEADER = 'x-nextjs-action-not-found';
const NEXT_REQUEST_ID_HEADER = 'x-nextjs-request-id';
const NEXT_HTML_REQUEST_ID_HEADER = 'x-nextjs-html-request-id';
const NEXT_ACTION_REVALIDATED_HEADER = 'x-action-revalidated';
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/router-reducer-types.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    ACTION_HMR_REFRESH: null,
    ACTION_NAVIGATE: null,
    ACTION_REFRESH: null,
    ACTION_RESTORE: null,
    ACTION_SERVER_ACTION: null,
    ACTION_SERVER_PATCH: null,
    PrefetchKind: null,
    ScrollBehavior: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    ACTION_HMR_REFRESH: function() {
        return ACTION_HMR_REFRESH;
    },
    ACTION_NAVIGATE: function() {
        return ACTION_NAVIGATE;
    },
    ACTION_REFRESH: function() {
        return ACTION_REFRESH;
    },
    ACTION_RESTORE: function() {
        return ACTION_RESTORE;
    },
    ACTION_SERVER_ACTION: function() {
        return ACTION_SERVER_ACTION;
    },
    ACTION_SERVER_PATCH: function() {
        return ACTION_SERVER_PATCH;
    },
    PrefetchKind: function() {
        return PrefetchKind;
    },
    ScrollBehavior: function() {
        return ScrollBehavior;
    }
});
const ACTION_REFRESH = 'refresh';
const ACTION_NAVIGATE = 'navigate';
const ACTION_RESTORE = 'restore';
const ACTION_SERVER_PATCH = 'server-patch';
const ACTION_HMR_REFRESH = 'hmr-refresh';
const ACTION_SERVER_ACTION = 'server-action';
var PrefetchKind = /*#__PURE__*/ function(PrefetchKind) {
    PrefetchKind["AUTO"] = "auto";
    PrefetchKind["FULL"] = "full";
    return PrefetchKind;
}({});
var ScrollBehavior = /*#__PURE__*/ function(ScrollBehavior) {
    /** Use per-node ScrollRef to decide whether to scroll. */ ScrollBehavior[ScrollBehavior["Default"] = 0] = "Default";
    /** Suppress scroll entirely (e.g. scroll={false} on Link or router.push). */ ScrollBehavior[ScrollBehavior["NoScroll"] = 1] = "NoScroll";
    return ScrollBehavior;
}({});
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/use-action-queue.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    dispatchAppRouterAction: null,
    dispatchGestureState: null,
    refreshOnInstantNavigationUnlock: null,
    useActionQueue: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    dispatchAppRouterAction: function() {
        return dispatchAppRouterAction;
    },
    dispatchGestureState: function() {
        return dispatchGestureState;
    },
    refreshOnInstantNavigationUnlock: function() {
        return refreshOnInstantNavigationUnlock;
    },
    useActionQueue: function() {
        return useActionQueue;
    }
});
const _interop_require_wildcard = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_wildcard.cjs [app-client] (ecmascript)");
const _react = /*#__PURE__*/ _interop_require_wildcard._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)"));
const _isthenable = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/is-thenable.js [app-client] (ecmascript)");
const _routerreducertypes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/router-reducer-types.js [app-client] (ecmascript)");
// The app router state lives outside of React, so we can import the dispatch
// method directly wherever we need it, rather than passing it around via props
// or context.
let dispatch = null;
function refreshOnInstantNavigationUnlock() {
    if ("TURBOPACK compile-time truthy", 1) {
        if (dispatch !== null) {
            dispatch({
                type: _routerreducertypes.ACTION_REFRESH,
                bypassCacheInvalidation: true
            });
        } else {
            window.location.reload();
        }
    }
}
function dispatchAppRouterAction(action) {
    if (dispatch === null) {
        throw Object.defineProperty(new Error('Internal Next.js error: Router action dispatched before initialization.'), "__NEXT_ERROR_CODE", {
            value: "E668",
            enumerable: false,
            configurable: true
        });
    }
    dispatch(action);
}
// Optimistic state setter for experimental_gesturePush. Only should be used
// during a gesture transition.
let setGestureRouterState = null;
function dispatchGestureState(state) {
    if (setGestureRouterState === null) {
        throw Object.defineProperty(new Error('Internal Next.js error: Router action dispatched before initialization.'), "__NEXT_ERROR_CODE", {
            value: "E668",
            enumerable: false,
            configurable: true
        });
    }
    setGestureRouterState(state);
}
const __DEV__ = ("TURBOPACK compile-time value", "development") !== 'production';
const promisesWithDebugInfo = ("TURBOPACK compile-time truthy", 1) ? new WeakMap() : "TURBOPACK unreachable";
function useActionQueue(actionQueue) {
    const [canonicalState, setState] = _react.default.useState(actionQueue.state);
    // Wrap the canonical state in useOptimistic to support
    // experimental_gesturePush. During a gesture transition, this returns a fork
    // of the router state that represents the eventual target if/when the gesture
    // completes. Otherwise it returns the canonical state.
    const [state, setGesture] = (0, _react.useOptimistic)(canonicalState);
    if (typeof window !== 'undefined') {
        setGestureRouterState = setGesture;
    }
    // Because of a known issue that requires to decode Flight streams inside the
    // render phase, we have to be a bit clever and assign the dispatch method to
    // a module-level variable upon initialization. The useState hook in this
    // module only exists to synchronize state that lives outside of React.
    // Ideally, what we'd do instead is pass the state as a prop to root.render;
    // this is conceptually how we're modeling the app router state, despite the
    // weird implementation details.
    let nextDispatch;
    if ("TURBOPACK compile-time truthy", 1) {
        const { useAppDevRenderingIndicator } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/use-app-dev-rendering-indicator.js [app-client] (ecmascript)");
        // eslint-disable-next-line react-hooks/rules-of-hooks
        const appDevRenderingIndicator = useAppDevRenderingIndicator();
        nextDispatch = (action)=>{
            appDevRenderingIndicator(()=>{
                actionQueue.dispatch(action, setState);
            });
        };
    } else //TURBOPACK unreachable
    ;
    if (typeof window !== 'undefined') {
        dispatch = nextDispatch;
    }
    // When navigating to a non-prefetched route, then App Router state will be
    // blocked until the server responds. We need to transfer the `_debugInfo`
    // from the underlying Flight response onto the top-level promise that is
    // passed to React (via `use`) so that the latency is accurately represented
    // in the React DevTools.
    const stateWithDebugInfo = (0, _react.useMemo)(()=>{
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
        if ((0, _isthenable.isThenable)(state)) {
            // useMemo can't be used to cache a Promise since the memoized value is thrown
            // away when we suspend. So we use a WeakMap to cache the Promise with debug info.
            let promiseWithDebugInfo = promisesWithDebugInfo.get(state);
            if (promiseWithDebugInfo === undefined) {
                const debugInfo = [];
                promiseWithDebugInfo = Promise.resolve(state).then((asyncState)=>{
                    if (asyncState.debugInfo !== null) {
                        debugInfo.push(...asyncState.debugInfo);
                    }
                    return asyncState;
                });
                promiseWithDebugInfo._debugInfo = debugInfo;
                promisesWithDebugInfo.set(state, promiseWithDebugInfo);
            }
            return promiseWithDebugInfo;
        }
        return state;
    }, [
        state
    ]);
    return (0, _isthenable.isThenable)(stateWithDebugInfo) ? (0, _react.use)(stateWithDebugInfo) : stateWithDebugInfo;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/navigation-testing-lock.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
/**
 * Navigation lock for the Instant Navigation Testing API.
 *
 * Manages the in-memory lock (a promise) that gates dynamic data writes
 * during instant navigation captures, and owns all cookie state
 * transitions (pending → captured-MPA, pending → captured-SPA).
 *
 * External actors (Playwright, devtools) set [0] to start a lock scope
 * and delete the cookie to end one. Next.js writes captured values.
 * The CookieStore handler distinguishes them by value: pending = external,
 * captured = self-write (ignored).
 */ "use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    isNavigationLocked: null,
    startListeningForInstantNavigationCookie: null,
    transitionToCapturedSPA: null,
    updateCapturedSPAToTree: null,
    waitForNavigationLockIfActive: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    isNavigationLocked: function() {
        return isNavigationLocked;
    },
    startListeningForInstantNavigationCookie: function() {
        return startListeningForInstantNavigationCookie;
    },
    transitionToCapturedSPA: function() {
        return transitionToCapturedSPA;
    },
    updateCapturedSPAToTree: function() {
        return updateCapturedSPAToTree;
    },
    waitForNavigationLockIfActive: function() {
        return waitForNavigationLockIfActive;
    }
});
const _approuterheaders = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-headers.js [app-client] (ecmascript)");
const _useactionqueue = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/use-action-queue.js [app-client] (ecmascript)");
function parseCookieValue(raw) {
    try {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed) && parsed.length >= 3) {
            const rawState = parsed[2];
            return rawState === null ? 'mpa' : 'spa';
        }
    } catch  {}
    return 'pending';
}
function writeCookieValue(value) {
    if (typeof cookieStore === 'undefined') {
        return;
    }
    // Read the existing cookie to preserve its attributes (domain, path),
    // then write back with the new value. This updates the same cookie
    // entry that the external actor created, regardless of how it was
    // scoped.
    cookieStore.get(_approuterheaders.NEXT_INSTANT_TEST_COOKIE).then((existing)=>{
        if (existing) {
            const options = {
                name: _approuterheaders.NEXT_INSTANT_TEST_COOKIE,
                value: JSON.stringify(value),
                path: existing.path ?? '/'
            };
            if (existing.domain) {
                options.domain = existing.domain;
            }
            cookieStore.set(options);
        }
    });
}
let lockState = null;
function acquireLock() {
    if (lockState !== null) {
        return;
    }
    let resolve;
    const promise = new Promise((r)=>{
        resolve = r;
    });
    lockState = {
        promise,
        resolve: resolve
    };
}
function releaseLock() {
    if (lockState !== null) {
        lockState.resolve();
        lockState = null;
    }
}
function startListeningForInstantNavigationCookie() {
    if ("TURBOPACK compile-time truthy", 1) {
        // If the server served a static shell, this is an MPA page load
        // while the lock is held. Transition to captured-MPA and acquire.
        if (self.__next_instant_test) {
            if (typeof cookieStore !== 'undefined') {
                // If the cookie was already cleared during the MPA page
                // transition, reload to get the full dynamic page.
                cookieStore.get(_approuterheaders.NEXT_INSTANT_TEST_COOKIE).then((cookie)=>{
                    if (!cookie) {
                        window.location.reload();
                    }
                });
            }
            writeCookieValue([
                1,
                `c${Math.random()}`,
                null
            ]);
            acquireLock();
        }
        if (typeof cookieStore === 'undefined') {
            return;
        }
        cookieStore.addEventListener('change', (event)=>{
            for (const cookie of event.changed){
                if (cookie.name === _approuterheaders.NEXT_INSTANT_TEST_COOKIE) {
                    const state = parseCookieValue(cookie.value ?? '');
                    if (state !== 'pending') {
                        // Captured value — our own transition. Ignore.
                        return;
                    }
                    // Pending value — external actor starting a new lock scope.
                    if (lockState !== null) {
                        releaseLock();
                    }
                    acquireLock();
                    return;
                }
            }
            for (const cookie of event.deleted){
                if (cookie.name === _approuterheaders.NEXT_INSTANT_TEST_COOKIE) {
                    releaseLock();
                    (0, _useactionqueue.refreshOnInstantNavigationUnlock)();
                    return;
                }
            }
        });
    }
}
function transitionToCapturedSPA(fromTree, toTree) {
    if ("TURBOPACK compile-time truthy", 1) {
        writeCookieValue([
            1,
            `c${Math.random()}`,
            {
                from: fromTree,
                to: toTree
            }
        ]);
    }
}
function updateCapturedSPAToTree(fromTree, toTree) {
    if ("TURBOPACK compile-time truthy", 1) {
        writeCookieValue([
            1,
            `c${Math.random()}`,
            {
                from: fromTree,
                to: toTree
            }
        ]);
    }
}
function isNavigationLocked() {
    if ("TURBOPACK compile-time truthy", 1) {
        return lockState !== null;
    }
    //TURBOPACK unreachable
    ;
}
async function waitForNavigationLockIfActive() {
    if ("TURBOPACK compile-time truthy", 1) {
        if (lockState !== null) {
            await lockState.promise;
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/app-globals.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
// imports polyfill from `@next/polyfill-module` after build.
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/polyfill-module.js [app-client] (ecmascript)");
// Only set up devtools for the dev server.
if ("TURBOPACK compile-time truthy", 1) {
    __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/app-dev-overlay-setup.js [app-client] (ecmascript)");
}
// Start listening for the instant navigation test cookie. The test framework
// (e.g. Playwright) sets/clears this cookie to control the navigation lock.
// Browser-only.
if (("TURBOPACK compile-time value", true) && typeof window !== 'undefined') {
    const { startListeningForInstantNavigationCookie } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/navigation-testing-lock.js [app-client] (ecmascript)");
    startListeningForInstantNavigationCookie();
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/readonly-url-search-params.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/navigation-untracked.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "useUntrackedPathname", {
    enumerable: true,
    get: function() {
        return useUntrackedPathname;
    }
});
const _react = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
const _hooksclientcontextsharedruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/hooks-client-context.shared-runtime.js [app-client] (ecmascript)");
/**
 * This checks to see if the current render has any unknown route parameters that
 * would cause the pathname to be dynamic. It's used to trigger a different
 * render path in the error boundary.
 *
 * @returns true if there are any unknown route parameters, false otherwise
 */ function hasFallbackRouteParams() {
    if (typeof window === 'undefined') {
        // AsyncLocalStorage should not be included in the client bundle.
        const { workUnitAsyncStorage } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/server/app-render/work-unit-async-storage.external.js [app-client] (ecmascript)");
        const workUnitStore = workUnitAsyncStorage.getStore();
        if (!workUnitStore) return false;
        switch(workUnitStore.type){
            case 'prerender':
            case 'prerender-client':
            case 'prerender-ppr':
            case 'validation-client':
                const fallbackParams = workUnitStore.fallbackRouteParams;
                return fallbackParams ? fallbackParams.size > 0 : false;
            case 'prerender-legacy':
            case 'request':
            case 'prerender-runtime':
            case 'cache':
            case 'private-cache':
            case 'unstable-cache':
            case 'generate-static-params':
                break;
            default:
                workUnitStore;
        }
        return false;
    }
    return false;
}
function useUntrackedPathname() {
    // If there are any unknown route parameters we would typically throw
    // an error, but this internal method allows us to return a null value instead
    // for components that do not propagate the pathname to the static shell (like
    // the error boundary).
    if (hasFallbackRouteParams()) {
        return null;
    }
    // This shouldn't cause any issues related to conditional rendering because
    // the environment will be consistent for the render.
    // eslint-disable-next-line react-hooks/rules-of-hooks
    return (0, _react.useContext)(_hooksclientcontextsharedruntime.PathnameContext);
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/create-href-from-url.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "createHrefFromUrl", {
    enumerable: true,
    get: function() {
        return createHrefFromUrl;
    }
});
function createHrefFromUrl(url, includeHash = true) {
    return url.pathname + url.search + (includeHash ? url.hash : '');
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/nav-failure-handler.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    handleHardNavError: null,
    useNavFailureHandler: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    handleHardNavError: function() {
        return handleHardNavError;
    },
    useNavFailureHandler: function() {
        return useNavFailureHandler;
    }
});
const _react = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
const _createhreffromurl = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/create-href-from-url.js [app-client] (ecmascript)");
function handleHardNavError(error) {
    if (error && typeof window !== 'undefined' && window.next.__pendingUrl && (0, _createhreffromurl.createHrefFromUrl)(new URL(window.location.href)) !== (0, _createhreffromurl.createHrefFromUrl)(window.next.__pendingUrl)) {
        console.error(`Error occurred during navigation, falling back to hard navigation`, error);
        window.location.href = window.next.__pendingUrl.toString();
        return true;
    }
    return false;
}
function useNavFailureHandler() {
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/handle-isr-error.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "handleISRError", {
    enumerable: true,
    get: function() {
        return handleISRError;
    }
});
const workAsyncStorage = typeof window === 'undefined' ? __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/server/app-render/work-async-storage.external.js [app-client] (ecmascript)").workAsyncStorage : undefined;
function handleISRError({ error }) {
    if (workAsyncStorage) {
        const store = workAsyncStorage.getStore();
        if (store?.isStaticGeneration) {
            if (error) {
                console.error(error);
            }
            throw error;
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/error-boundary.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
'use client';
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    ErrorBoundary: null,
    ErrorBoundaryHandler: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    ErrorBoundary: function() {
        return ErrorBoundary;
    },
    ErrorBoundaryHandler: function() {
        return ErrorBoundaryHandler;
    }
});
const _interop_require_wildcard = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_wildcard.cjs [app-client] (ecmascript)");
const _jsxruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/jsx-runtime.js [app-client] (ecmascript)");
const _react = /*#__PURE__*/ _interop_require_wildcard._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)"));
const _navigationuntracked = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/navigation-untracked.js [app-client] (ecmascript)");
const _isnextroutererror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/is-next-router-error.js [app-client] (ecmascript)");
const _navfailurehandler = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/nav-failure-handler.js [app-client] (ecmascript)");
const _handleisrerror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/handle-isr-error.js [app-client] (ecmascript)");
const _isbot = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/is-bot.js [app-client] (ecmascript)");
const _approutercontextsharedruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/app-router-context.shared-runtime.js [app-client] (ecmascript)");
const isBotUserAgent = typeof window !== 'undefined' && (0, _isbot.isBot)(window.navigator.userAgent);
class ErrorBoundaryHandler extends _react.default.Component {
    static{
        this.contextType = _approutercontextsharedruntime.AppRouterContext;
    }
    constructor(props){
        super(props), this.reset = ()=>{
            this.setState({
                error: null
            });
        }, this.unstable_retry = ()=>{
            (0, _react.startTransition)(()=>{
                this.context?.refresh();
                this.reset();
            });
        };
        this.state = {
            error: null,
            previousPathname: this.props.pathname
        };
    }
    static getDerivedStateFromError(error) {
        if ((0, _isnextroutererror.isNextRouterError)(error)) {
            // Re-throw if an expected internal Next.js router error occurs
            // this means it should be handled by a different boundary (such as a NotFound boundary in a parent segment)
            throw error;
        }
        return {
            error
        };
    }
    static getDerivedStateFromProps(props, state) {
        const { error } = state;
        // if we encounter an error while
        // a navigation is pending we shouldn't render
        // the error boundary and instead should fallback
        // to a hard navigation to attempt recovering
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
        /**
     * Handles reset of the error boundary when a navigation happens.
     * Ensures the error boundary does not stay enabled when navigating to a new page.
     * Approach of setState in render is safe as it checks the previous pathname and then overrides
     * it as outlined in https://react.dev/reference/react/useState#storing-information-from-previous-renders
     */ if (props.pathname !== state.previousPathname && state.error) {
            return {
                error: null,
                previousPathname: props.pathname
            };
        }
        return {
            error: state.error,
            previousPathname: props.pathname
        };
    }
    // Explicit type is needed to avoid the generated `.d.ts` having a wide return type that could be specific to the `@types/react` version.
    render() {
        //When it's bot request, segment level error boundary will keep rendering the children,
        // the final error will be caught by the root error boundary and determine wether need to apply graceful degrade.
        if (this.state.error && !isBotUserAgent) {
            (0, _handleisrerror.handleISRError)({
                error: this.state.error
            });
            return /*#__PURE__*/ (0, _jsxruntime.jsxs)(_jsxruntime.Fragment, {
                children: [
                    this.props.errorStyles,
                    this.props.errorScripts,
                    /*#__PURE__*/ (0, _jsxruntime.jsx)(this.props.errorComponent, {
                        error: this.state.error,
                        reset: this.reset,
                        unstable_retry: this.unstable_retry
                    })
                ]
            });
        }
        return this.props.children;
    }
}
function ErrorBoundary({ errorComponent, errorStyles, errorScripts, children }) {
    // When we're rendering the missing params shell, this will return null. This
    // is because we won't be rendering any not found boundaries or error
    // boundaries for the missing params shell. When this runs on the client
    // (where these errors can occur), we will get the correct pathname.
    const pathname = (0, _navigationuntracked.useUntrackedPathname)();
    if (errorComponent) {
        return /*#__PURE__*/ (0, _jsxruntime.jsx)(ErrorBoundaryHandler, {
            pathname: pathname,
            errorComponent: errorComponent,
            errorStyles: errorStyles,
            errorScripts: errorScripts,
            children: children
        });
    }
    return /*#__PURE__*/ (0, _jsxruntime.jsx)(_jsxruntime.Fragment, {
        children: children
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/builtin/error-styles.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    WarningIcon: null,
    errorStyles: null,
    errorThemeCss: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    WarningIcon: function() {
        return WarningIcon;
    },
    errorStyles: function() {
        return errorStyles;
    },
    errorThemeCss: function() {
        return errorThemeCss;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [app-client] (ecmascript)");
const _jsxruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/jsx-runtime.js [app-client] (ecmascript)");
const _react = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)"));
const errorStyles = {
    container: {
        fontFamily: 'system-ui,"Segoe UI",Roboto,Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji"',
        height: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
    },
    card: {
        marginTop: '-32px',
        maxWidth: '325px',
        padding: '32px 28px',
        textAlign: 'left'
    },
    icon: {
        marginBottom: '24px'
    },
    title: {
        fontSize: '24px',
        fontWeight: 500,
        letterSpacing: '-0.02em',
        lineHeight: '32px',
        margin: '0 0 12px 0',
        color: 'var(--next-error-title)'
    },
    message: {
        fontSize: '14px',
        fontWeight: 400,
        lineHeight: '21px',
        margin: '0 0 20px 0',
        color: 'var(--next-error-message)'
    },
    form: {
        margin: 0
    },
    buttonGroup: {
        display: 'flex',
        gap: '8px',
        alignItems: 'center'
    },
    button: {
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '32px',
        padding: '0 12px',
        fontSize: '14px',
        fontWeight: 500,
        lineHeight: '20px',
        borderRadius: '6px',
        cursor: 'pointer',
        color: 'var(--next-error-btn-text)',
        background: 'var(--next-error-btn-bg)',
        border: 'var(--next-error-btn-border)'
    },
    buttonSecondary: {
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '32px',
        padding: '0 12px',
        fontSize: '14px',
        fontWeight: 500,
        lineHeight: '20px',
        borderRadius: '6px',
        cursor: 'pointer',
        color: 'var(--next-error-btn-secondary-text)',
        background: 'var(--next-error-btn-secondary-bg)',
        border: 'var(--next-error-btn-secondary-border)'
    },
    digestFooter: {
        position: 'fixed',
        bottom: '32px',
        left: '0',
        right: '0',
        textAlign: 'center',
        fontFamily: 'ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace',
        fontSize: '12px',
        lineHeight: '18px',
        fontWeight: 400,
        margin: '0',
        color: 'var(--next-error-digest)'
    }
};
const errorThemeCss = `
:root {
  --next-error-bg: #fff;
  --next-error-text: #171717;
  --next-error-title: #171717;
  --next-error-message: #171717;
  --next-error-digest: #666666;
  --next-error-btn-text: #fff;
  --next-error-btn-bg: #171717;
  --next-error-btn-border: none;
  --next-error-btn-secondary-text: #171717;
  --next-error-btn-secondary-bg: transparent;
  --next-error-btn-secondary-border: 1px solid rgba(0,0,0,0.08);
}
@media (prefers-color-scheme: dark) {
  :root {
    --next-error-bg: #0a0a0a;
    --next-error-text: #ededed;
    --next-error-title: #ededed;
    --next-error-message: #ededed;
    --next-error-digest: #a0a0a0;
    --next-error-btn-text: #0a0a0a;
    --next-error-btn-bg: #ededed;
    --next-error-btn-border: none;
    --next-error-btn-secondary-text: #ededed;
    --next-error-btn-secondary-bg: transparent;
    --next-error-btn-secondary-border: 1px solid rgba(255,255,255,0.14);
  }
}
body { margin: 0; color: var(--next-error-text); background: var(--next-error-bg); }
`.replace(/\n\s*/g, '');
function WarningIcon() {
    return /*#__PURE__*/ (0, _jsxruntime.jsx)("svg", {
        width: "32",
        height: "32",
        viewBox: "-0.2 -1.5 32 32",
        fill: "none",
        style: errorStyles.icon,
        children: /*#__PURE__*/ (0, _jsxruntime.jsx)("path", {
            d: "M16.9328 0C18.0839 0.000116771 19.1334 0.658832 19.634 1.69531L31.4299 26.1309C32.0708 27.4588 31.1036 28.9999 29.6291 29H2.00215C0.527541 29 -0.439628 27.4588 0.201371 26.1309L11.9973 1.69531C12.4979 0.658823 13.5474 7.75066e-05 14.6984 0H16.9328ZM3.59493 26H28.0363L16.9328 3H14.6984L3.59493 26ZM15.8156 19C16.9202 19.0001 17.8156 19.8955 17.8156 21C17.8156 22.1045 16.9202 22.9999 15.8156 23C14.7111 23 13.8156 22.1046 13.8156 21C13.8156 19.8954 14.7111 19 15.8156 19ZM17.3156 16.5H14.3156V8.5H17.3156V16.5Z",
            fill: "var(--next-error-title)"
        })
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/builtin/global-error.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, // supplied custom global error signatures.
"default", {
    enumerable: true,
    get: function() {
        return _default;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [app-client] (ecmascript)");
const _jsxruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/jsx-runtime.js [app-client] (ecmascript)");
const _react = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)"));
const _handleisrerror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/handle-isr-error.js [app-client] (ecmascript)");
const _errorstyles = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/builtin/error-styles.js [app-client] (ecmascript)");
function DefaultGlobalError({ error }) {
    const digest = error?.digest;
    const isServerError = !!digest;
    const message = isServerError ? 'A server error occurred. Reload to try again.' : 'Reload to try again, or go back.';
    (0, _handleisrerror.handleISRError)({
        error
    });
    return /*#__PURE__*/ (0, _jsxruntime.jsxs)("html", {
        id: "__next_error__",
        children: [
            /*#__PURE__*/ (0, _jsxruntime.jsx)("head", {
                children: /*#__PURE__*/ (0, _jsxruntime.jsx)("style", {
                    dangerouslySetInnerHTML: {
                        __html: _errorstyles.errorThemeCss
                    }
                })
            }),
            /*#__PURE__*/ (0, _jsxruntime.jsxs)("body", {
                children: [
                    /*#__PURE__*/ (0, _jsxruntime.jsx)("div", {
                        style: _errorstyles.errorStyles.container,
                        children: /*#__PURE__*/ (0, _jsxruntime.jsxs)("div", {
                            style: _errorstyles.errorStyles.card,
                            children: [
                                /*#__PURE__*/ (0, _jsxruntime.jsx)(_errorstyles.WarningIcon, {}),
                                /*#__PURE__*/ (0, _jsxruntime.jsx)("h1", {
                                    style: _errorstyles.errorStyles.title,
                                    children: "This page couldn’t load"
                                }),
                                /*#__PURE__*/ (0, _jsxruntime.jsx)("p", {
                                    style: _errorstyles.errorStyles.message,
                                    children: message
                                }),
                                /*#__PURE__*/ (0, _jsxruntime.jsxs)("div", {
                                    style: _errorstyles.errorStyles.buttonGroup,
                                    children: [
                                        /*#__PURE__*/ (0, _jsxruntime.jsx)("form", {
                                            style: _errorstyles.errorStyles.form,
                                            children: /*#__PURE__*/ (0, _jsxruntime.jsx)("button", {
                                                type: "submit",
                                                style: _errorstyles.errorStyles.button,
                                                children: "Reload"
                                            })
                                        }),
                                        !isServerError && /*#__PURE__*/ (0, _jsxruntime.jsx)("button", {
                                            type: "button",
                                            style: _errorstyles.errorStyles.buttonSecondary,
                                            onClick: ()=>{
                                                if (window.history.length > 1) {
                                                    window.history.back();
                                                } else {
                                                    window.location.href = '/';
                                                }
                                            },
                                            children: "Back"
                                        })
                                    ]
                                })
                            ]
                        })
                    }),
                    digest && /*#__PURE__*/ (0, _jsxruntime.jsxs)("p", {
                        style: _errorstyles.errorStyles.digestFooter,
                        children: [
                            "ERROR ",
                            digest
                        ]
                    })
                ]
            })
        ]
    });
}
const _default = DefaultGlobalError;
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/runtime-error-handler.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/not-found.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "notFound", {
    enumerable: true,
    get: function() {
        return notFound;
    }
});
const _httpaccessfallback = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/http-access-fallback/http-access-fallback.js [app-client] (ecmascript)");
/**
 * This function allows you to render the [not-found.js file](https://nextjs.org/docs/app/api-reference/file-conventions/not-found)
 * within a route segment as well as inject a tag.
 *
 * `notFound()` can be used in
 * [Server Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components),
 * [Route Handlers](https://nextjs.org/docs/app/building-your-application/routing/route-handlers), and
 * [Server Actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations).
 *
 * - In a Server Component, this will insert a `<meta name="robots" content="noindex" />` meta tag and set the status code to 404.
 * - In a Route Handler or Server Action, it will serve a 404 to the caller.
 *
 * Read more: [Next.js Docs: `notFound`](https://nextjs.org/docs/app/api-reference/functions/not-found)
 */ const DIGEST = `${_httpaccessfallback.HTTP_ERROR_FALLBACK_ERROR_CODE};404`;
function notFound() {
    const error = Object.defineProperty(new Error(DIGEST), "__NEXT_ERROR_CODE", {
        value: "E1041",
        enumerable: false,
        configurable: true
    });
    error.digest = DIGEST;
    throw error;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/react-client-callbacks/error-boundary-callbacks.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
// This file is only used in app router due to the specific error state handling.
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    onCaughtError: null,
    onUncaughtError: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    onCaughtError: function() {
        return onCaughtError;
    },
    onUncaughtError: function() {
        return onUncaughtError;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [app-client] (ecmascript)");
const _isnextroutererror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/is-next-router-error.js [app-client] (ecmascript)");
const _bailouttocsr = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/lazy-dynamic/bailout-to-csr.js [app-client] (ecmascript)");
const _reportglobalerror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/react-client-callbacks/report-global-error.js [app-client] (ecmascript)");
const _errorboundary = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/error-boundary.js [app-client] (ecmascript)");
const _globalerror = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/builtin/global-error.js [app-client] (ecmascript)"));
const devToolErrorMod = ("TURBOPACK compile-time truthy", 1) ? __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/errors/index.js [app-client] (ecmascript)") : "TURBOPACK unreachable";
function onCaughtError(thrownValue, errorInfo) {
    const errorBoundaryComponent = errorInfo.errorBoundary?.constructor;
    let isImplicitErrorBoundary;
    if ("TURBOPACK compile-time truthy", 1) {
        const { AppDevOverlayErrorBoundary } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/app-dev-overlay-error-boundary.js [app-client] (ecmascript)");
        isImplicitErrorBoundary = errorBoundaryComponent === AppDevOverlayErrorBoundary;
    }
    isImplicitErrorBoundary = isImplicitErrorBoundary || errorBoundaryComponent === _errorboundary.ErrorBoundaryHandler && errorInfo.errorBoundary.props.errorComponent === _globalerror.default;
    // Skip the segment explorer triggered error
    if ("TURBOPACK compile-time truthy", 1) {
        const { SEGMENT_EXPLORER_SIMULATED_ERROR_MESSAGE } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/segment-explorer-node.js [app-client] (ecmascript)");
        if (thrownValue instanceof Error && thrownValue.message === SEGMENT_EXPLORER_SIMULATED_ERROR_MESSAGE) {
            return;
        }
    }
    if (isImplicitErrorBoundary) {
        // We don't consider errors caught unless they're caught by an explicit error
        // boundary. The built-in ones are considered implicit.
        // This mimics how the same app would behave without Next.js.
        return onUncaughtError(thrownValue);
    }
    // Skip certain custom errors which are not expected to be reported on client
    if ((0, _bailouttocsr.isBailoutToCSRError)(thrownValue) || (0, _isnextroutererror.isNextRouterError)(thrownValue)) return;
    if ("TURBOPACK compile-time truthy", 1) {
        const errorBoundaryName = errorBoundaryComponent?.displayName || errorBoundaryComponent?.name || 'Unknown';
        const componentThatErroredFrame = errorInfo?.componentStack?.split('\n')[1];
        // Match chrome or safari stack trace
        const matches = // example 1: at Page (http://localhost:3000/_next/static/chunks/pages/index.js?ts=1631600000000:2:1)
        // example 2: Page@http://localhost:3000/_next/static/chunks/pages/index.js?ts=1631600000000:2:1
        componentThatErroredFrame?.match(/\s+at (\w+)\s+|(\w+)@/) ?? [];
        const componentThatErroredName = matches[1] || matches[2] || 'Unknown';
        // Create error location with errored component and error boundary, to match the behavior of default React onCaughtError handler.
        const errorBoundaryMessage = `It was handled by the <${errorBoundaryName}> error boundary.`;
        const componentErrorMessage = ("TURBOPACK compile-time truthy", 1) ? `The above error occurred in the <${componentThatErroredName}> component.` : "TURBOPACK unreachable";
        const errorLocation = `${componentErrorMessage} ${errorBoundaryMessage}`;
        const error = devToolErrorMod.decorateDevError(thrownValue);
        // Log and report the error with location but without modifying the error stack
        devToolErrorMod.originConsoleError('%o\n\n%s', thrownValue, errorLocation);
        devToolErrorMod.handleClientError(error);
    } else //TURBOPACK unreachable
    ;
}
function onUncaughtError(thrownValue) {
    // Skip certain custom errors which are not expected to be reported on client
    if ((0, _bailouttocsr.isBailoutToCSRError)(thrownValue) || (0, _isnextroutererror.isNextRouterError)(thrownValue)) return;
    if ("TURBOPACK compile-time truthy", 1) {
        const error = devToolErrorMod.decorateDevError(thrownValue);
        // TODO: Add an adendum to the overlay telling people about custom error boundaries.
        (0, _reportglobalerror.reportGlobalError)(error);
    } else //TURBOPACK unreachable
    ;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/app-call-server.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "callServer", {
    enumerable: true,
    get: function() {
        return callServer;
    }
});
const _react = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
const _routerreducertypes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/router-reducer-types.js [app-client] (ecmascript)");
const _useactionqueue = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/use-action-queue.js [app-client] (ecmascript)");
async function callServer(actionId, actionArgs) {
    return new Promise((resolve, reject)=>{
        (0, _react.startTransition)(()=>{
            (0, _useactionqueue.dispatchAppRouterAction)({
                type: _routerreducertypes.ACTION_SERVER_ACTION,
                actionId,
                actionArgs,
                resolve,
                reject
            });
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/app-find-source-map-url.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "findSourceMapURL", {
    enumerable: true,
    get: function() {
        return findSourceMapURL;
    }
});
const basePath = ("TURBOPACK compile-time value", "") || '';
const pathname = `${basePath}/__nextjs_source-map`;
const findSourceMapURL = ("TURBOPACK compile-time truthy", 1) ? function findSourceMapURL(filename) {
    if (filename === '') {
        return null;
    }
    if (filename.startsWith(document.location.origin) && filename.includes('/_next/static')) {
        // This is a request for a client chunk. This can only happen when
        // using Turbopack. In this case, since we control how those source
        // maps are generated, we can safely assume that the sourceMappingURL
        // is relative to the filename, with an added `.map` extension. The
        // browser can just request this file, and it gets served through the
        // normal dev server, without the need to route this through
        // the `/__nextjs_source-map` dev middleware.
        return `${filename}.map`;
    }
    const url = new URL(pathname, document.location.origin);
    url.searchParams.set('filename', filename);
    return url.href;
} : "TURBOPACK unreachable";
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/route-params.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    doesStaticSegmentAppearInURL: null,
    getCacheKeyForDynamicParam: null,
    getParamValueFromCacheKey: null,
    getRenderedPathname: null,
    getRenderedSearch: null,
    parseDynamicParamFromURLPart: null,
    urlSearchParamsToParsedUrlQuery: null,
    urlToUrlWithoutFlightMarker: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    doesStaticSegmentAppearInURL: function() {
        return doesStaticSegmentAppearInURL;
    },
    getCacheKeyForDynamicParam: function() {
        return getCacheKeyForDynamicParam;
    },
    getParamValueFromCacheKey: function() {
        return getParamValueFromCacheKey;
    },
    getRenderedPathname: function() {
        return getRenderedPathname;
    },
    getRenderedSearch: function() {
        return getRenderedSearch;
    },
    parseDynamicParamFromURLPart: function() {
        return parseDynamicParamFromURLPart;
    },
    urlSearchParamsToParsedUrlQuery: function() {
        return urlSearchParamsToParsedUrlQuery;
    },
    urlToUrlWithoutFlightMarker: function() {
        return urlToUrlWithoutFlightMarker;
    }
});
const _segment = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/segment.js [app-client] (ecmascript)");
const _segmentvalueencoding = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/segment-cache/segment-value-encoding.js [app-client] (ecmascript)");
const _approuterheaders = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-headers.js [app-client] (ecmascript)");
function getRenderedSearch(response) {
    // If the server performed a rewrite, the search params used to render the
    // page will be different from the params in the request URL. In this case,
    // the response will include a header that gives the rewritten search query.
    const rewrittenQuery = response.headers.get(_approuterheaders.NEXT_REWRITTEN_QUERY_HEADER);
    if (rewrittenQuery !== null) {
        return rewrittenQuery === '' ? '' : '?' + rewrittenQuery;
    }
    // If the header is not present, there was no rewrite, so we use the search
    // query of the response URL.
    return urlToUrlWithoutFlightMarker(new URL(response.url)).search;
}
function getRenderedPathname(response) {
    // If the server performed a rewrite, the pathname used to render the
    // page will be different from the pathname in the request URL. In this case,
    // the response will include a header that gives the rewritten pathname.
    const rewrittenPath = response.headers.get(_approuterheaders.NEXT_REWRITTEN_PATH_HEADER);
    return rewrittenPath ?? urlToUrlWithoutFlightMarker(new URL(response.url)).pathname;
}
// Pathname parts come from `URL.pathname.split('/')`, so they are already
// in the encoded form the URL parser produces. The server-side equivalent
// (`get-dynamic-param.ts`) starts from a decoded param value and applies
// `encodeURIComponent` once. The two encodings are not the same — for
// example, the URL parser leaves `,` and `:` untouched while
// `encodeURIComponent` percent-encodes them. To produce the same canonical
// form on the client (and avoid double-encoding `%xx` sequences such as
// `%2F` → `%252F`), we decode the URL part first and re-encode it.
function canonicalizeURLPart(part) {
    try {
        return encodeURIComponent(decodeURIComponent(part));
    } catch  {
        // `decodeURIComponent` throws on malformed sequences. Fall back to the
        // already-encoded form rather than failing the navigation.
        return part;
    }
}
function parseDynamicParamFromURLPart(paramType, pathnameParts, partIndex) {
    // This needs to match the behavior in get-dynamic-param.ts.
    switch(paramType){
        // Catchalls
        case 'c':
            {
                // Catchalls receive all the remaining URL parts. If there are no
                // remaining pathname parts, return an empty array.
                return partIndex < pathnameParts.length ? pathnameParts.slice(partIndex).map((s)=>canonicalizeURLPart(s)) : [];
            }
        // Catchall intercepted
        case 'ci(..)(..)':
        case 'ci(.)':
        case 'ci(..)':
        case 'ci(...)':
            {
                const prefix = paramType.length - 2;
                return partIndex < pathnameParts.length ? pathnameParts.slice(partIndex).map((s, i)=>{
                    if (i === 0) {
                        return canonicalizeURLPart(s.slice(prefix));
                    }
                    return canonicalizeURLPart(s);
                }) : [];
            }
        // Optional catchalls
        case 'oc':
            {
                // Optional catchalls receive all the remaining URL parts, unless this is
                // the end of the pathname, in which case they return null.
                return partIndex < pathnameParts.length ? pathnameParts.slice(partIndex).map((s)=>canonicalizeURLPart(s)) : null;
            }
        // Dynamic
        case 'd':
            {
                if (partIndex >= pathnameParts.length) {
                    // The route tree expected there to be more parts in the URL than there
                    // actually are. This could happen if the x-nextjs-rewritten-path header
                    // is incorrectly set, or potentially due to bug in Next.js. TODO:
                    // Should this be a hard error? During a prefetch, we can just abort.
                    // During a client navigation, we could trigger a hard refresh. But if
                    // it happens during initial render, we don't really have any
                    // recovery options.
                    return '';
                }
                return canonicalizeURLPart(pathnameParts[partIndex]);
            }
        // Dynamic intercepted
        case 'di(..)(..)':
        case 'di(.)':
        case 'di(..)':
        case 'di(...)':
            {
                const prefix = paramType.length - 2;
                if (partIndex >= pathnameParts.length) {
                    // The route tree expected there to be more parts in the URL than there
                    // actually are. This could happen if the x-nextjs-rewritten-path header
                    // is incorrectly set, or potentially due to bug in Next.js. TODO:
                    // Should this be a hard error? During a prefetch, we can just abort.
                    // During a client navigation, we could trigger a hard refresh. But if
                    // it happens during initial render, we don't really have any
                    // recovery options.
                    return '';
                }
                return canonicalizeURLPart(pathnameParts[partIndex].slice(prefix));
            }
        default:
            paramType;
            return '';
    }
}
function doesStaticSegmentAppearInURL(segment) {
    // This is not a parameterized segment; however, we need to determine
    // whether or not this segment appears in the URL. For example, this route
    // groups do not appear in the URL, so they should be skipped. Any other
    // special cases must be handled here.
    // TODO: Consider encoding this directly into the router tree instead of
    // inferring it on the client based on the segment type. Something like
    // a `doesAppearInURL` flag in FlightRouterState.
    if (segment === _segmentvalueencoding.ROOT_SEGMENT_REQUEST_KEY || // For some reason, the loader tree sometimes includes extra __PAGE__
    // "layouts" when part of a parallel route. But it's not a leaf node.
    // Otherwise, we wouldn't need this special case because pages are
    // always leaf nodes.
    // TODO: Investigate why the loader produces these fake page segments.
    segment.startsWith(_segment.PAGE_SEGMENT_KEY) || // Route groups.
    segment[0] === '(' && segment.endsWith(')') || segment === _segment.DEFAULT_SEGMENT_KEY || segment === '/_not-found') {
        return false;
    } else {
        // All other segment types appear in the URL
        return true;
    }
}
function getCacheKeyForDynamicParam(paramValue, renderedSearch) {
    // This needs to match the logic in get-dynamic-param.ts, until we're able to
    // unify the various implementations so that these are always computed on
    // the client.
    if (typeof paramValue === 'string') {
        // TODO: Refactor or remove this helper function to accept a string rather
        // than the whole segment type. Also we can probably just append the
        // search string instead of turning it into JSON.
        const pageSegmentWithSearchParams = (0, _segment.addSearchParamsIfPageSegment)(paramValue, Object.fromEntries(new URLSearchParams(renderedSearch)));
        return pageSegmentWithSearchParams;
    } else if (paramValue === null) {
        return '';
    } else {
        return paramValue.join('/');
    }
}
function urlToUrlWithoutFlightMarker(url) {
    const urlWithoutFlightParameters = new URL(url);
    urlWithoutFlightParameters.searchParams.delete(_approuterheaders.NEXT_RSC_UNION_QUERY);
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    return urlWithoutFlightParameters;
}
function getParamValueFromCacheKey(paramCacheKey, paramType) {
    // Turn the cache key string sent by the server (as part of FlightRouterState)
    // into a value that can be passed to `useParams` and client components.
    const isCatchAll = paramType === 'c' || paramType === 'oc';
    if (isCatchAll) {
        // Catch-all param keys are a concatenation of the path segments.
        // See equivalent logic in `getSelectedParams`.
        // TODO: We should just pass the array directly, rather than concatenate
        // it to a string and then split it back to an array. It needs to be an
        // array in some places, like when passing a key React, but we can convert
        // it at runtime in those places.
        return paramCacheKey.split('/');
    }
    return paramCacheKey;
}
function urlSearchParamsToParsedUrlQuery(searchParams) {
    // Converts a URLSearchParams object to the same type used by the server when
    // creating search params props, i.e. the type returned by Node's
    // "querystring" module.
    const result = {};
    for (const [key, value] of searchParams.entries()){
        if (result[key] === undefined) {
            result[key] = value;
        } else if (Array.isArray(result[key])) {
            result[key].push(value);
        } else {
            result[key] = [
                result[key],
                value
            ];
        }
    }
    return result;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/flight-data-helpers.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    createInitialRSCPayloadFromFallbackPrerender: null,
    getFlightDataPartsFromPath: null,
    getNextFlightSegmentPath: null,
    normalizeFlightData: null,
    prepareFlightRouterStateForRequest: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    createInitialRSCPayloadFromFallbackPrerender: function() {
        return createInitialRSCPayloadFromFallbackPrerender;
    },
    getFlightDataPartsFromPath: function() {
        return getFlightDataPartsFromPath;
    },
    getNextFlightSegmentPath: function() {
        return getNextFlightSegmentPath;
    },
    normalizeFlightData: function() {
        return normalizeFlightData;
    },
    prepareFlightRouterStateForRequest: function() {
        return prepareFlightRouterStateForRequest;
    }
});
const _segment = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/segment.js [app-client] (ecmascript)");
const _routeparams = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/route-params.js [app-client] (ecmascript)");
const _createhreffromurl = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/create-href-from-url.js [app-client] (ecmascript)");
function getFlightDataPartsFromPath(flightDataPath) {
    // Pick the last 4 items from the `FlightDataPath` to get the [tree, seedData, viewport, isHeadPartial].
    const flightDataPathLength = 4;
    // tree, seedData, and head are *always* the last three items in the `FlightDataPath`.
    const [tree, seedData, head, isHeadPartial] = flightDataPath.slice(-flightDataPathLength);
    // The `FlightSegmentPath` is everything except the last three items. For a root render, it won't be present.
    const segmentPath = flightDataPath.slice(0, -flightDataPathLength);
    return {
        // TODO: Unify these two segment path helpers. We are inconsistently pushing an empty segment ("")
        // to the start of the segment path in some places which makes it hard to use solely the segment path.
        // Look for "// TODO-APP: remove ''" in the codebase.
        pathToSegment: segmentPath.slice(0, -1),
        segmentPath,
        // if the `FlightDataPath` corresponds with the root, there'll be no segment path,
        // in which case we default to ''.
        segment: segmentPath[segmentPath.length - 1] ?? '',
        tree,
        seedData,
        head,
        isHeadPartial,
        isRootRender: flightDataPath.length === flightDataPathLength
    };
}
function createInitialRSCPayloadFromFallbackPrerender(response, fallbackInitialRSCPayload) {
    // This is a static fallback page. In order to hydrate the page, we need to
    // parse the client params from the URL, but to account for the possibility
    // that the page was rewritten, we need to check the response headers
    // for x-nextjs-rewritten-path or x-nextjs-rewritten-query headers. Since
    // we can't access the headers of the initial document response, the client
    // performs a fetch request to the current location. Since it's possible that
    // the fetch request will be dynamically rewritten to a different path than
    // the initial document, this fetch request delivers _all_ the hydration data
    // for the page; it was not inlined into the document, like it normally
    // would be.
    //
    // TODO: Consider treating the case where fetch is rewritten to a different
    // path from the document as a special deopt case. We should optimistically
    // assume this won't happen, inline the data into the document, and perform
    // a minimal request (like a HEAD or range request) to verify that the
    // response matches. Tricky to get right because we need to account for
    // all the different deployment environments we support, like output:
    // "export" mode, where we currently don't assume that custom response
    // headers are present.
    // Patch the Flight data sent by the server with the correct params parsed
    // from the URL + response object.
    const renderedPathname = (0, _routeparams.getRenderedPathname)(response);
    const renderedSearch = (0, _routeparams.getRenderedSearch)(response);
    const canonicalUrl = (0, _createhreffromurl.createHrefFromUrl)(new URL(location.href));
    const originalFlightDataPath = fallbackInitialRSCPayload.f[0];
    const originalFlightRouterState = originalFlightDataPath[0];
    const payload = {
        c: canonicalUrl.split('/'),
        q: renderedSearch,
        i: fallbackInitialRSCPayload.i,
        f: [
            [
                fillInFallbackFlightRouterState(originalFlightRouterState, renderedPathname, renderedSearch),
                originalFlightDataPath[1],
                originalFlightDataPath[2],
                originalFlightDataPath[2]
            ]
        ],
        m: fallbackInitialRSCPayload.m,
        G: fallbackInitialRSCPayload.G,
        S: fallbackInitialRSCPayload.S,
        h: fallbackInitialRSCPayload.h
    };
    if (fallbackInitialRSCPayload.b) {
        payload.b = fallbackInitialRSCPayload.b;
    }
    return payload;
}
function fillInFallbackFlightRouterState(flightRouterState, renderedPathname, renderedSearch) {
    const pathnameParts = renderedPathname.split('/').filter((p)=>p !== '');
    const index = 0;
    return fillInFallbackFlightRouterStateImpl(flightRouterState, renderedSearch, pathnameParts, index);
}
function fillInFallbackFlightRouterStateImpl(flightRouterState, renderedSearch, pathnameParts, pathnamePartsIndex) {
    const originalSegment = flightRouterState[0];
    let newSegment;
    let doesAppearInURL;
    if (typeof originalSegment === 'string') {
        newSegment = originalSegment;
        doesAppearInURL = (0, _routeparams.doesStaticSegmentAppearInURL)(originalSegment);
    } else {
        const paramName = originalSegment[0];
        const paramType = originalSegment[2];
        const staticSiblings = originalSegment[3];
        const paramValue = (0, _routeparams.parseDynamicParamFromURLPart)(paramType, pathnameParts, pathnamePartsIndex);
        const cacheKey = (0, _routeparams.getCacheKeyForDynamicParam)(paramValue, renderedSearch);
        newSegment = [
            paramName,
            cacheKey,
            paramType,
            staticSiblings
        ];
        doesAppearInURL = true;
    }
    // Only increment the index if the segment appears in the URL. If it's a
    // "virtual" segment, like a route group, it remains the same.
    const childPathnamePartsIndex = doesAppearInURL ? pathnamePartsIndex + 1 : pathnamePartsIndex;
    const children = flightRouterState[1];
    const newChildren = {};
    for(let key in children){
        const childFlightRouterState = children[key];
        newChildren[key] = fillInFallbackFlightRouterStateImpl(childFlightRouterState, renderedSearch, pathnameParts, childPathnamePartsIndex);
    }
    const newState = [
        newSegment,
        newChildren,
        null,
        flightRouterState[3],
        flightRouterState[4]
    ];
    return newState;
}
function getNextFlightSegmentPath(flightSegmentPath) {
    // Since `FlightSegmentPath` is a repeated tuple of `Segment` and `ParallelRouteKey`, we slice off two items
    // to get the next segment path.
    return flightSegmentPath.slice(2);
}
function normalizeFlightData(flightData) {
    // FlightData can be a string when the server didn't respond with a proper flight response,
    // or when a redirect happens, to signal to the client that it needs to perform an MPA navigation.
    if (typeof flightData === 'string') {
        return flightData;
    }
    return flightData.map((flightDataPath)=>getFlightDataPartsFromPath(flightDataPath));
}
function prepareFlightRouterStateForRequest(flightRouterState, isHmrRefresh) {
    // HMR requests need the complete, unmodified state for proper functionality
    if (isHmrRefresh) {
        return encodeURIComponent(JSON.stringify(flightRouterState));
    }
    return encodeURIComponent(JSON.stringify(stripClientOnlyDataFromFlightRouterState(flightRouterState)));
}
/**
 * Recursively strips client-only data from FlightRouterState while preserving
 * server-needed information for proper rendering decisions.
 */ function stripClientOnlyDataFromFlightRouterState(flightRouterState) {
    const [segment, parallelRoutes, _refreshState, refreshMarker, prefetchHints] = flightRouterState;
    // Strip client-only data from the segment
    const cleanedSegment = stripClientOnlyDataFromSegment(segment);
    // Recursively process parallel routes
    const cleanedParallelRoutes = {};
    for (const [key, childState] of Object.entries(parallelRoutes)){
        cleanedParallelRoutes[key] = stripClientOnlyDataFromFlightRouterState(childState);
    }
    const result = [
        cleanedSegment,
        cleanedParallelRoutes
    ];
    if (refreshMarker) {
        result[2] = null // null slightly more compact than undefined
        ;
        result[3] = refreshMarker;
    }
    // Append optional fields if present
    if (prefetchHints !== undefined) {
        result[4] = prefetchHints;
    }
    // Everything else is used only by the client and is not needed for requests.
    return result;
}
/**
 * Strips client-only data from segments:
 * - Search parameters from __PAGE__ segments
 * - staticSiblings from dynamic segment tuples (only needed for client-side
 *   prefetch reuse decisions)
 */ function stripClientOnlyDataFromSegment(segment) {
    if (typeof segment === 'string') {
        // Strip search params from __PAGE__ segments
        if (segment.startsWith(_segment.PAGE_SEGMENT_KEY + '?')) {
            return _segment.PAGE_SEGMENT_KEY;
        }
        return segment;
    }
    // Dynamic segment tuple: [paramName, paramCacheKey, paramType, staticSiblings]
    // Strip staticSiblings (4th element) since server doesn't need it
    const [paramName, paramCacheKey, paramType] = segment;
    return [
        paramName,
        paramCacheKey,
        paramType,
        null
    ];
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/set-cache-busting-search-param.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    setCacheBustingSearchParam: null,
    setCacheBustingSearchParamWithHash: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    setCacheBustingSearchParam: function() {
        return setCacheBustingSearchParam;
    },
    setCacheBustingSearchParamWithHash: function() {
        return setCacheBustingSearchParamWithHash;
    }
});
const _cachebustingsearchparam = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/cache-busting-search-param.js [app-client] (ecmascript)");
const _approuterheaders = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-headers.js [app-client] (ecmascript)");
async function computeClientCacheBustingSearchParam(headers) {
    if (typeof globalThis.crypto?.subtle?.digest === 'function') {
        return (0, _cachebustingsearchparam.computeCacheBustingSearchParam)(headers[_approuterheaders.NEXT_ROUTER_PREFETCH_HEADER], headers[_approuterheaders.NEXT_ROUTER_SEGMENT_PREFETCH_HEADER], headers[_approuterheaders.NEXT_ROUTER_STATE_TREE_HEADER], headers[_approuterheaders.NEXT_URL]);
    }
    return (0, _cachebustingsearchparam.computeLegacyCacheBustingSearchParam)(headers[_approuterheaders.NEXT_ROUTER_PREFETCH_HEADER], headers[_approuterheaders.NEXT_ROUTER_SEGMENT_PREFETCH_HEADER], headers[_approuterheaders.NEXT_ROUTER_STATE_TREE_HEADER], headers[_approuterheaders.NEXT_URL]);
}
const setCacheBustingSearchParam = async (url, headers)=>{
    const uniqueCacheKey = await computeClientCacheBustingSearchParam(headers);
    setCacheBustingSearchParamWithHash(url, uniqueCacheKey);
};
const setCacheBustingSearchParamWithHash = (url, hash)=>{
    /**
   * Note that we intentionally do not use `url.searchParams.set` here:
   *
   * const url = new URL('https://example.com/search?q=custom%20spacing');
   * url.searchParams.set('_rsc', 'abc123');
   * console.log(url.toString()); // Outputs: https://example.com/search?q=custom+spacing&_rsc=abc123
   *                                                                             ^ <--- this is causing confusion
   * This is in fact intended based on https://url.spec.whatwg.org/#interface-urlsearchparams, but
   * we want to preserve the %20 as %20 if that's what the user passed in, hence the custom
   * logic below.
   */ const existingSearch = url.search;
    const rawQuery = existingSearch.startsWith('?') ? existingSearch.slice(1) : existingSearch;
    // Always remove any existing cache busting param and add a fresh one to ensure
    // we have the correct value based on current request headers
    const pairs = rawQuery.split('&').filter((pair)=>pair && !pair.startsWith(`${_approuterheaders.NEXT_RSC_UNION_QUERY}=`));
    if (hash.length > 0) {
        pairs.push(`${_approuterheaders.NEXT_RSC_UNION_QUERY}=${hash}`);
    } else {
        pairs.push(`${_approuterheaders.NEXT_RSC_UNION_QUERY}`);
    }
    url.search = pairs.length ? `?${pairs.join('&')}` : '';
};
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/navigation-build-id.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

// This gets assigned as a side-effect during app initialization. Because it
// represents the build used to create the JS bundle, it should never change
// after being set, so we store it in a global variable.
//
// When performing RSC requests, if the incoming data has a different build ID,
// we perform an MPA navigation/refresh to load the updated build and ensure
// that the client and server in sync.
//
// Starts as an empty string. In practice, because setNavigationBuildId is called during initialization
// before hydration starts, this will always get reassigned to the actual ID before it's ever needed
// by a navigation. If for some reasons it didn't, due to a bug or race condition, then on
// navigation the build comparision would fail and trigger an MPA navigation.
//
// Note that this can also be initialized with the deployment id instead (if available). So it's not
// the same as "the build id", but we are running out of alternative names for "build id or
// deployment id".
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    getNavigationBuildId: null,
    setNavigationBuildId: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    getNavigationBuildId: function() {
        return getNavigationBuildId;
    },
    setNavigationBuildId: function() {
        return setNavigationBuildId;
    }
});
let globalBuildId = '';
function setNavigationBuildId(buildId) {
    globalBuildId = buildId;
}
function getNavigationBuildId() {
    return globalBuildId;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/match-segments.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "matchSegment", {
    enumerable: true,
    get: function() {
        return matchSegment;
    }
});
const matchSegment = (existingSegment, segment)=>{
    // segment is either Array or string
    if (typeof existingSegment === 'string') {
        if (typeof segment === 'string') {
            // Common case: segment is just a string
            return existingSegment === segment;
        }
        return false;
    }
    if (typeof segment === 'string') {
        return false;
    }
    return existingSegment[0] === segment[0] && existingSegment[1] === segment[1];
};
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache-key.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

// TypeScript trick to simulate opaque types, like in Flow.
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "createCacheKey", {
    enumerable: true,
    get: function() {
        return createCacheKey;
    }
});
function createCacheKey(originalHref, nextUrl) {
    const originalUrl = new URL(originalHref);
    const cacheKey = {
        pathname: originalUrl.pathname,
        search: originalUrl.search,
        nextUrl: nextUrl
    };
    return cacheKey;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/types.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

/**
 * Shared types and constants for the Segment Cache.
 */ Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    FetchStrategy: null,
    NavigationResultTag: null,
    PrefetchPriority: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    FetchStrategy: function() {
        return FetchStrategy;
    },
    NavigationResultTag: function() {
        return NavigationResultTag;
    },
    PrefetchPriority: function() {
        return PrefetchPriority;
    }
});
var NavigationResultTag = /*#__PURE__*/ function(NavigationResultTag) {
    NavigationResultTag[NavigationResultTag["MPA"] = 0] = "MPA";
    NavigationResultTag[NavigationResultTag["Success"] = 1] = "Success";
    NavigationResultTag[NavigationResultTag["NoOp"] = 2] = "NoOp";
    NavigationResultTag[NavigationResultTag["Async"] = 3] = "Async";
    return NavigationResultTag;
}({});
var PrefetchPriority = /*#__PURE__*/ function(PrefetchPriority) {
    /**
   * Assigned to the most recently hovered/touched link. Special network
   * bandwidth is reserved for this task only. There's only ever one Intent-
   * priority task at a time; when a new Intent task is scheduled, the previous
   * one is bumped down to Default.
   */ PrefetchPriority[PrefetchPriority["Intent"] = 2] = "Intent";
    /**
   * The default priority for prefetch tasks.
   */ PrefetchPriority[PrefetchPriority["Default"] = 1] = "Default";
    /**
   * Assigned to tasks when they spawn non-blocking background work, like
   * revalidating a partially cached entry to see if more data is available.
   */ PrefetchPriority[PrefetchPriority["Background"] = 0] = "Background";
    return PrefetchPriority;
}({});
var FetchStrategy = /*#__PURE__*/ function(FetchStrategy) {
    // Deliberately ordered so we can easily compare two segments
    // and determine if one segment is "more specific" than another
    // (i.e. if it's likely that it contains more data)
    FetchStrategy[FetchStrategy["LoadingBoundary"] = 0] = "LoadingBoundary";
    FetchStrategy[FetchStrategy["PPR"] = 1] = "PPR";
    FetchStrategy[FetchStrategy["PPRRuntime"] = 2] = "PPRRuntime";
    FetchStrategy[FetchStrategy["Full"] = 3] = "Full";
    return FetchStrategy;
}({});
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache-map.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    Fallback: null,
    createCacheMap: null,
    deleteFromCacheMap: null,
    deleteMapEntry: null,
    getFromCacheMap: null,
    isValueExpired: null,
    setInCacheMap: null,
    setSizeInCacheMap: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    Fallback: function() {
        return Fallback;
    },
    createCacheMap: function() {
        return createCacheMap;
    },
    deleteFromCacheMap: function() {
        return deleteFromCacheMap;
    },
    deleteMapEntry: function() {
        return deleteMapEntry;
    },
    getFromCacheMap: function() {
        return getFromCacheMap;
    },
    isValueExpired: function() {
        return isValueExpired;
    },
    setInCacheMap: function() {
        return setInCacheMap;
    },
    setSizeInCacheMap: function() {
        return setSizeInCacheMap;
    }
});
const _lru = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/lru.js [app-client] (ecmascript)");
const Fallback = {};
// This is a special internal key that is used for "revalidation" entries. It's
// an implementation detail that shouldn't leak outside of this module.
const Revalidation = {};
function createCacheMap() {
    const cacheMap = {
        parent: null,
        key: null,
        value: null,
        map: null,
        // LRU-related fields
        prev: null,
        next: null,
        size: 0
    };
    return cacheMap;
}
function getOrInitialize(cacheMap, keys, isRevalidation) {
    // Go through each level of keys until we find the entry that matches, or
    // create a new entry if one doesn't exist.
    //
    // This function will only return entries that match the keypath _exactly_.
    // Unlike getWithFallback, it will not access fallback entries unless it's
    // explicitly part of the keypath.
    let entry = cacheMap;
    let remainingKeys = keys;
    let key = null;
    while(true){
        const previousKey = key;
        if (remainingKeys !== null) {
            key = remainingKeys.value;
            remainingKeys = remainingKeys.parent;
        } else if (isRevalidation && previousKey !== Revalidation) {
            // During a revalidation, we append an internal "Revalidation" key to
            // the end of the keypath. The "normal" entry is its parent.
            // However, if the parent entry is currently empty, we don't need to store
            // this as a revalidation entry. Just insert the revalidation into the
            // normal slot.
            if (entry.value === null) {
                return entry;
            }
            // Otheriwse, create a child entry.
            key = Revalidation;
        } else {
            break;
        }
        let map = entry.map;
        if (map !== null) {
            const existingEntry = map.get(key);
            if (existingEntry !== undefined) {
                // Found a match. Keep going.
                entry = existingEntry;
                continue;
            }
        } else {
            map = new Map();
            entry.map = map;
        }
        // No entry exists yet at this level. Create a new one.
        const newEntry = {
            parent: entry,
            key,
            value: null,
            map: null,
            // LRU-related fields
            prev: null,
            next: null,
            size: 0
        };
        map.set(key, newEntry);
        entry = newEntry;
    }
    return entry;
}
function getFromCacheMap(now, currentCacheVersion, rootEntry, keys, isRevalidation) {
    const entry = getEntryWithFallbackImpl(now, currentCacheVersion, rootEntry, keys, isRevalidation, 0);
    if (entry === null || entry.value === null) {
        return null;
    }
    // This is an LRU access. Move the entry to the front of the list.
    (0, _lru.lruPut)(entry);
    return entry.value;
}
function isValueExpired(now, currentCacheVersion, value) {
    return value.staleAt <= now || value.version < currentCacheVersion;
}
function lazilyEvictIfNeeded(now, currentCacheVersion, entry) {
    // We have a matching entry, but before we can return it, we need to check if
    // it's still fresh. Otherwise it should be treated the same as a cache miss.
    if (entry.value === null) {
        // This entry has no value, so there's nothing to evict.
        return entry;
    }
    const value = entry.value;
    if (isValueExpired(now, currentCacheVersion, value)) {
        // The value expired. Lazily evict it from the cache, and return null. This
        // is conceptually the same as a cache miss.
        deleteMapEntry(entry);
        return null;
    }
    // The matched entry has not expired. Return it.
    return entry;
}
function getEntryWithFallbackImpl(now, currentCacheVersion, entry, keys, isRevalidation, previousKey) {
    // This is similar to getExactEntry, but if an exact match is not found for
    // a key, it will return the fallback entry instead. This is recursive at
    // every level, e.g. an entry with keypath [a, Fallback, c, Fallback] is
    // valid match for [a, b, c, d].
    //
    // It will return the most specific match available.
    let key;
    let remainingKeys;
    if (keys !== null) {
        key = keys.value;
        remainingKeys = keys.parent;
    } else if (isRevalidation && previousKey !== Revalidation) {
        // During a revalidation, we append an internal "Revalidation" key to
        // the end of the keypath.
        key = Revalidation;
        remainingKeys = null;
    } else {
        // There are no more keys. This is the terminal entry.
        // TODO: When performing a lookup during a navigation, as opposed to a
        // prefetch, we may want to skip entries that are Pending if there's also
        // a Fulfilled fallback entry. Tricky to say, though, since if it's
        // already pending, it's likely to stream in soon. Maybe we could do this
        // just on slow connections and offline mode.
        return lazilyEvictIfNeeded(now, currentCacheVersion, entry);
    }
    const map = entry.map;
    if (map !== null) {
        const existingEntry = map.get(key);
        if (existingEntry !== undefined) {
            // Found an exact match for this key. Keep searching.
            const result = getEntryWithFallbackImpl(now, currentCacheVersion, existingEntry, remainingKeys, isRevalidation, key);
            if (result !== null) {
                return result;
            }
        }
        // No match found for this key. Check if there's a fallback.
        const fallbackEntry = map.get(Fallback);
        if (fallbackEntry !== undefined) {
            // Found a fallback for this key. Keep searching.
            return getEntryWithFallbackImpl(now, currentCacheVersion, fallbackEntry, remainingKeys, isRevalidation, key);
        }
    }
    return null;
}
function setInCacheMap(cacheMap, keys, value, isRevalidation) {
    // Add a value to the map at the given keypath. If the value is already
    // part of the map, it's removed from its previous keypath. (NOTE: This is
    // unlike a regular JS map, but the behavior is intentional.)
    const entry = getOrInitialize(cacheMap, keys, isRevalidation);
    setMapEntryValue(entry, value);
    // This is an LRU access. Move the entry to the front of the list.
    (0, _lru.lruPut)(entry);
    (0, _lru.updateLruSize)(entry, value.size);
}
function setMapEntryValue(entry, value) {
    if (entry.value !== null) {
        // There's already a value at the given keypath. Disconnect the old value
        // from the map. We're not calling `deleteMapEntry` here because the
        // entry itself is still in the map. We just want to overwrite its value.
        dropRef(entry.value);
        entry.value = null;
    }
    // This value may already be in the map at a different keypath.
    // Grab a reference before we overwrite it.
    const oldEntry = value.ref;
    entry.value = value;
    value.ref = entry;
    (0, _lru.updateLruSize)(entry, value.size);
    if (oldEntry !== null && oldEntry !== entry && oldEntry.value === value) {
        // This value is already in the map at a different keypath in the map.
        // Values only exist at a single keypath at a time. Remove it from the
        // previous keypath.
        //
        // Note that only the internal map entry is garbage collected; we don't
        // call `dropRef` here because it's still in the map, just
        // at a new keypath (the one we just set, above).
        deleteMapEntry(oldEntry);
    }
}
function deleteFromCacheMap(value) {
    const entry = value.ref;
    if (entry === null) {
        // This value is not a member of any map.
        return;
    }
    dropRef(value);
    deleteMapEntry(entry);
}
function dropRef(value) {
    // Drop the value from the map by setting its `ref` backpointer to
    // null. This is a separate operation from `deleteMapEntry` because when
    // re-keying a value we need to be able to delete the old, internal map
    // entry without garbage collecting the value itself.
    value.ref = null;
}
function deleteMapEntry(entry) {
    // Delete the entry from the cache.
    entry.value = null;
    (0, _lru.deleteFromLru)(entry);
    // Check if we can garbage collect the entry.
    const map = entry.map;
    if (map === null) {
        // Since this entry has no value, and also no child entries, we can
        // garbage collect it. Remove it from its parent, and keep garbage
        // collecting the parents until we reach a non-empty entry.
        let parent = entry.parent;
        let key = entry.key;
        while(parent !== null){
            const parentMap = parent.map;
            if (parentMap !== null) {
                parentMap.delete(key);
                if (parentMap.size === 0) {
                    // We just removed the last entry in the parent map.
                    parent.map = null;
                    if (parent.value === null) {
                        // The parent node has no child entries, nor does it have a value
                        // on itself. It can be garbage collected. Keep going.
                        key = parent.key;
                        parent = parent.parent;
                        continue;
                    }
                }
            }
            break;
        }
    } else {
        // Check if there's a revalidating entry. If so, promote it to a
        // "normal" entry, since the normal one was just deleted.
        const revalidatingEntry = map.get(Revalidation);
        if (revalidatingEntry !== undefined && revalidatingEntry.value !== null) {
            setMapEntryValue(entry, revalidatingEntry.value);
        }
    }
}
function setSizeInCacheMap(value, size) {
    const entry = value.ref;
    if (entry === null) {
        // This value is not a member of any map.
        return;
    }
    // Except during initialization (when the size is set to 0), this is the only
    // place the `size` field should be updated, to ensure it's in sync with the
    // the LRU.
    value.size = size;
    (0, _lru.updateLruSize)(entry, size);
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/lru.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    cleanup: null,
    deleteFromLru: null,
    lruPut: null,
    updateLruSize: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    cleanup: function() {
        return cleanup;
    },
    deleteFromLru: function() {
        return deleteFromLru;
    },
    lruPut: function() {
        return lruPut;
    },
    updateLruSize: function() {
        return updateLruSize;
    }
});
const _cachemap = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache-map.js [app-client] (ecmascript)");
const _scheduler = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/scheduler.js [app-client] (ecmascript)");
// We use an LRU for memory management. We must update this whenever we add or
// remove a new cache entry, or when an entry changes size.
let head = null;
let lruSize = 0;
// TODO: I chose the max size somewhat arbitrarily. Consider setting this based
// on navigator.deviceMemory, or some other heuristic. We should make this
// customizable via the Next.js config, too.
const maxLruSize = 50 * 1024 * 1024 // 50 MB
;
function lruPut(node) {
    if (head === node) {
        // Already at the head
        return;
    }
    const prev = node.prev;
    const next = node.next;
    if (next === null || prev === null) {
        // This is an insertion
        lruSize += node.size;
        // Whenever we add an entry, we need to check if we've exceeded the
        // max size. We don't evict entries immediately; they're evicted later in
        // an asynchronous task.
        ensureCleanupIsScheduled();
    } else {
        // This is a move. Remove from its current position.
        prev.next = next;
        next.prev = prev;
    }
    // Move to the front of the list
    if (head === null) {
        // This is the first entry
        node.prev = node;
        node.next = node;
    } else {
        // Add to the front of the list
        const tail = head.prev;
        node.prev = tail;
        // In practice, this is never null, but that isn't encoded in the type
        if (tail !== null) {
            tail.next = node;
        }
        node.next = head;
        head.prev = node;
    }
    head = node;
}
function updateLruSize(node, newNodeSize) {
    // This is a separate function from `put` so that we can resize the entry
    // regardless of whether it's currently being tracked by the LRU.
    const prevNodeSize = node.size;
    node.size = newNodeSize;
    if (node.next === null) {
        // This entry is not currently being tracked by the LRU.
        return;
    }
    // Update the total LRU size
    lruSize = lruSize - prevNodeSize + newNodeSize;
    ensureCleanupIsScheduled();
}
function deleteFromLru(deleted) {
    const next = deleted.next;
    const prev = deleted.prev;
    if (next !== null && prev !== null) {
        lruSize -= deleted.size;
        deleted.next = null;
        deleted.prev = null;
        // Remove from the list
        if (head === deleted) {
            // Update the head
            if (next === head) {
                // This was the last entry
                head = null;
            } else {
                head = next;
                prev.next = next;
                next.prev = prev;
            }
        } else {
            prev.next = next;
            next.prev = prev;
        }
    } else {
    // Already deleted
    }
}
function ensureCleanupIsScheduled() {
    if (lruSize <= maxLruSize) {
        return;
    }
    // To schedule cleanup, ping the prefetch scheduler. At the end of its work
    // loop, once there are no queued tasks and no in-progress requests, it will
    // call cleanup().
    (0, _scheduler.pingPrefetchScheduler)();
}
function cleanup() {
    if (lruSize <= maxLruSize) {
        return;
    }
    // Evict entries until we're at 90% capacity. We can assume this won't
    // infinite loop because even if `maxLruSize` were 0, eventually
    // `deleteFromLru` sets `head` to `null` when we run out entries.
    const ninetyPercentMax = maxLruSize * 0.9;
    while(lruSize > ninetyPercentMax && head !== null){
        const tail = head.prev;
        // In practice, this is never null, but that isn't encoded in the type
        if (tail !== null) {
            // Delete the entry from the map. In turn, this will remove it from
            // the LRU.
            (0, _cachemap.deleteMapEntry)(tail);
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/scheduler.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    cancelPrefetchTask: null,
    isPrefetchTaskDirty: null,
    pingPrefetchScheduler: null,
    pingPrefetchTask: null,
    reschedulePrefetchTask: null,
    schedulePrefetchTask: null,
    startRevalidationCooldown: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    cancelPrefetchTask: function() {
        return cancelPrefetchTask;
    },
    isPrefetchTaskDirty: function() {
        return isPrefetchTaskDirty;
    },
    pingPrefetchScheduler: function() {
        return pingPrefetchScheduler;
    },
    pingPrefetchTask: function() {
        return pingPrefetchTask;
    },
    reschedulePrefetchTask: function() {
        return reschedulePrefetchTask;
    },
    schedulePrefetchTask: function() {
        return schedulePrefetchTask;
    },
    startRevalidationCooldown: function() {
        return startRevalidationCooldown;
    }
});
const _approutertypes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/app-router-types.js [app-client] (ecmascript)");
const _matchsegments = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/match-segments.js [app-client] (ecmascript)");
const _cache = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache.js [app-client] (ecmascript)");
const _cachekey = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache-key.js [app-client] (ecmascript)");
const _types = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/types.js [app-client] (ecmascript)");
const _segment = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/segment.js [app-client] (ecmascript)");
const _lru = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/lru.js [app-client] (ecmascript)");
const scheduleMicrotask = typeof queueMicrotask === 'function' ? queueMicrotask : (fn)=>Promise.resolve().then(fn).catch((error)=>setTimeout(()=>{
            throw error;
        }));
const taskHeap = [];
let inProgressRequests = 0;
let sortIdCounter = 0;
let didScheduleMicrotask = false;
// The most recently hovered (or touched, etc) link, i.e. the most recent task
// scheduled at Intent priority. There's only ever a single task at Intent
// priority at a time. We reserve special network bandwidth for this task only.
let mostRecentlyHoveredLink = null;
// CDN cache propagation delay after revalidation (in milliseconds)
const REVALIDATION_COOLDOWN_MS = 300;
// Timeout handle for the revalidation cooldown. When non-null, prefetch
// requests are blocked to allow CDN cache propagation.
let revalidationCooldownTimeoutHandle = null;
function startRevalidationCooldown() {
    // Clear any existing timeout in case multiple revalidations happen
    // in quick succession.
    if (revalidationCooldownTimeoutHandle !== null) {
        clearTimeout(revalidationCooldownTimeoutHandle);
    }
    // Schedule the cooldown to expire after the delay.
    revalidationCooldownTimeoutHandle = setTimeout(()=>{
        revalidationCooldownTimeoutHandle = null;
        // Retry the prefetch queue now that the cooldown has expired.
        pingPrefetchScheduler();
    }, REVALIDATION_COOLDOWN_MS);
}
function schedulePrefetchTask(key, treeAtTimeOfPrefetch, fetchStrategy, priority, onInvalidate, _onComplete) {
    // Spawn a new prefetch task
    const task = {
        key,
        treeAtTimeOfPrefetch,
        routeCacheVersion: (0, _cache.getCurrentRouteCacheVersion)(),
        segmentCacheVersion: (0, _cache.getCurrentSegmentCacheVersion)(),
        priority,
        phase: 1,
        hasBackgroundWork: false,
        spawnedRuntimePrefetches: null,
        fetchStrategy,
        sortId: sortIdCounter++,
        isCanceled: false,
        onInvalidate,
        _heapIndex: -1
    };
    if ("TURBOPACK compile-time truthy", 1) {
        task._onComplete = _onComplete;
    }
    trackMostRecentlyHoveredLink(task);
    heapPush(taskHeap, task);
    // Schedule an async task to process the queue.
    //
    // The main reason we process the queue in an async task is for batching.
    // It's common for a single JS task/event to trigger multiple prefetches.
    // By deferring to a microtask, we only process the queue once per JS task.
    // If they have different priorities, it also ensures they are processed in
    // the optimal order.
    pingPrefetchScheduler();
    return task;
}
function cancelPrefetchTask(task) {
    // Remove the prefetch task from the queue. If the task already completed,
    // then this is a no-op.
    //
    // We must also explicitly mark the task as canceled so that a blocked task
    // does not get added back to the queue when it's pinged by the network.
    task.isCanceled = true;
    heapDelete(taskHeap, task);
    if ("TURBOPACK compile-time truthy", 1) {
        // Call completion callback. In practice this shouldn't be reached for
        // test-initiated prefetches since cancellation is only used by the Link
        // component when elements scroll out of viewport.
        const onComplete = task._onComplete;
        task._onComplete = undefined;
        onComplete?.();
    }
}
function reschedulePrefetchTask(task, treeAtTimeOfPrefetch, fetchStrategy, priority) {
    // Bump the prefetch task to the top of the queue, as if it were a fresh
    // task. This is essentially the same as canceling the task and scheduling
    // a new one, except it reuses the original object.
    //
    // The primary use case is to increase the priority of a Link-initated
    // prefetch on hover.
    //
    // Note: _onComplete is not reset here because it's preserved on the same
    // task object. When the rescheduled task completes, the original callback
    // will still be invoked.
    // Un-cancel the task, in case it was previously canceled.
    task.isCanceled = false;
    task.phase = 1;
    // Assign a new sort ID to move it ahead of all other tasks at the same
    // priority level. (Higher sort IDs are processed first.)
    task.sortId = sortIdCounter++;
    task.priority = // Intent priority, even if the rescheduled priority is lower.
    task === mostRecentlyHoveredLink ? _types.PrefetchPriority.Intent : priority;
    task.treeAtTimeOfPrefetch = treeAtTimeOfPrefetch;
    task.fetchStrategy = fetchStrategy;
    trackMostRecentlyHoveredLink(task);
    if (task._heapIndex !== -1) {
        // The task is already in the queue.
        heapResift(taskHeap, task);
    } else {
        heapPush(taskHeap, task);
    }
    pingPrefetchScheduler();
}
function isPrefetchTaskDirty(task, nextUrl, tree) {
    // This is used to quickly bail out of a prefetch task if the result is
    // guaranteed to not have changed since the task was initiated. This is
    // strictly an optimization — theoretically, if it always returned true, no
    // behavior should change because a full prefetch task will effectively
    // perform the same checks.
    return task.routeCacheVersion !== (0, _cache.getCurrentRouteCacheVersion)() || task.segmentCacheVersion !== (0, _cache.getCurrentSegmentCacheVersion)() || task.treeAtTimeOfPrefetch !== tree || task.key.nextUrl !== nextUrl;
}
function trackMostRecentlyHoveredLink(task) {
    // Track the mostly recently hovered link, i.e. the most recently scheduled
    // task at Intent priority. There must only be one such task at a time.
    if (task.priority === _types.PrefetchPriority.Intent && task !== mostRecentlyHoveredLink) {
        if (mostRecentlyHoveredLink !== null) {
            // Bump the previously hovered link's priority down to Default.
            if (mostRecentlyHoveredLink.priority !== _types.PrefetchPriority.Background) {
                mostRecentlyHoveredLink.priority = _types.PrefetchPriority.Default;
                heapResift(taskHeap, mostRecentlyHoveredLink);
            }
        }
        mostRecentlyHoveredLink = task;
    }
}
function pingPrefetchScheduler() {
    if (didScheduleMicrotask) {
        // Already scheduled a task to process the queue
        return;
    }
    didScheduleMicrotask = true;
    scheduleMicrotask(processQueueInMicrotask);
}
/**
 * Checks if we've exceeded the maximum number of concurrent prefetch requests,
 * to avoid saturating the browser's internal network queue. This is a
 * cooperative limit — prefetch tasks should check this before issuing
 * new requests.
 *
 * Also checks if we're within the revalidation cooldown window, during which
 * prefetch requests are delayed to allow CDN cache propagation.
 */ function hasNetworkBandwidth(task) {
    // Check if we're within the revalidation cooldown window
    if (revalidationCooldownTimeoutHandle !== null) {
        // We're within the cooldown window. Return false to prevent prefetching.
        // When the cooldown expires, the timeout will call ensureWorkIsScheduled()
        // to retry the queue.
        return false;
    }
    // TODO: Also check if there's an in-progress navigation. We should never
    // add prefetch requests to the network queue if an actual navigation is
    // taking place, to ensure there's sufficient bandwidth for render-blocking
    // data and resources.
    // TODO: Consider reserving some amount of bandwidth for static prefetches.
    if (task.priority === _types.PrefetchPriority.Intent) {
        // The most recently hovered link is allowed to exceed the default limit.
        //
        // The goal is to always have enough bandwidth to start a new prefetch
        // request when hovering over a link.
        //
        // However, because we don't abort in-progress requests, it's still possible
        // we'll run out of bandwidth. When links are hovered in quick succession,
        // there could be multiple hover requests running simultaneously.
        return inProgressRequests < 12;
    }
    // The default limit is lower than the limit for a hovered link.
    return inProgressRequests < 4;
}
function spawnPrefetchSubtask(prefetchSubtask) {
    // When the scheduler spawns an async task, we don't await its result.
    // Instead, the async task writes its result directly into the cache, then
    // pings the scheduler to continue.
    //
    // We process server responses streamingly, so the prefetch subtask will
    // likely resolve before we're finished receiving all the data. The subtask
    // result includes a promise that resolves once the network connection is
    // closed. The scheduler uses this to control network bandwidth by tracking
    // and limiting the number of concurrent requests.
    inProgressRequests++;
    return prefetchSubtask.then((result)=>{
        if (result === null) {
            // The prefetch task errored before it could start processing the
            // network stream. Assume the connection is closed.
            onPrefetchConnectionClosed();
            return null;
        }
        // Wait for the connection to close before freeing up more bandwidth.
        result.closed.then(onPrefetchConnectionClosed);
        return result.value;
    });
}
function onPrefetchConnectionClosed() {
    inProgressRequests--;
    // Notify the scheduler that we have more bandwidth, and can continue
    // processing tasks.
    pingPrefetchScheduler();
}
function pingPrefetchTask(task) {
    // "Ping" a prefetch that's already in progress to notify it of new data.
    if (task.isCanceled || // Check if prefetch is already queued.
    task._heapIndex !== -1) {
        return;
    }
    // Add the task back to the queue.
    heapPush(taskHeap, task);
    pingPrefetchScheduler();
}
function processQueueInMicrotask() {
    didScheduleMicrotask = false;
    // We aim to minimize how often we read the current time. Since nearly all
    // functions in the prefetch scheduler are synchronous, we can read the time
    // once and pass it as an argument wherever it's needed.
    const now = Date.now();
    // Process the task queue until we run out of network bandwidth.
    let task = heapPeek(taskHeap);
    while(task !== null && hasNetworkBandwidth(task)){
        task.routeCacheVersion = (0, _cache.getCurrentRouteCacheVersion)();
        task.segmentCacheVersion = (0, _cache.getCurrentSegmentCacheVersion)();
        const exitStatus = pingRoute(now, task);
        // These fields are only valid for a single attempt. Reset them after each
        // iteration of the task queue.
        const hasBackgroundWork = task.hasBackgroundWork;
        task.hasBackgroundWork = false;
        task.spawnedRuntimePrefetches = null;
        switch(exitStatus){
            case 0:
                // The task yielded because there are too many requests in progress.
                // Stop processing tasks until we have more bandwidth.
                return;
            case 1:
                // The task is blocked. It needs more data before it can proceed.
                // Keep the task out of the queue until the server responds.
                heapPop(taskHeap);
                // Continue to the next task
                task = heapPeek(taskHeap);
                continue;
            case 2:
                if (task.phase === 1) {
                    // Finished prefetching the route tree. Proceed to prefetching
                    // the segments.
                    task.phase = 0;
                    heapResift(taskHeap, task);
                } else if (hasBackgroundWork) {
                    // The task spawned additional background work. Reschedule the task
                    // at background priority.
                    task.priority = _types.PrefetchPriority.Background;
                    heapResift(taskHeap, task);
                } else {
                    // The prefetch is complete. Continue to the next task.
                    if ("TURBOPACK compile-time truthy", 1) {
                        // Notify the Instant Navigation Testing API that the prefetch has
                        // completed, so it can proceed with navigation.
                        const onComplete = task._onComplete;
                        task._onComplete = undefined;
                        onComplete?.();
                    }
                    heapPop(taskHeap);
                }
                task = heapPeek(taskHeap);
                continue;
            default:
                exitStatus;
        }
    }
    // Run LRU cleanup only when the scheduler is fully idle: no queued tasks and
    // no in-progress requests. At that point, all active prefetch tasks have
    // finished reading from the cache (moving recently used entries to the front
    // of the list), so only genuinely stale data gets evicted.
    if (task === null && inProgressRequests === 0) {
        (0, _lru.cleanup)();
    }
}
/**
 * Check this during a prefetch task to determine if background work can be
 * performed. If so, it evaluates to `true`. Otherwise, it returns `false`,
 * while also scheduling a background task to run later. Usage:
 *
 * @example
 * if (background(task)) {
 *   // Perform background-pri work
 * }
 */ function background(task) {
    if (task.priority === _types.PrefetchPriority.Background) {
        return true;
    }
    task.hasBackgroundWork = true;
    return false;
}
function pingRoute(now, task) {
    const key = task.key;
    const route = (0, _cache.readOrCreateRouteCacheEntry)(now, task, key);
    const exitStatus = pingRootRouteTree(now, task, route);
    if (exitStatus !== 0 && key.search !== '') {
        // If the URL has a non-empty search string, also prefetch the pathname
        // without the search string. We use the searchless route tree as a base for
        // optimistic routing; see requestOptimisticRouteCacheEntry for details.
        //
        // Note that we don't need to prefetch any of the segment data. Just the
        // route tree.
        //
        // TODO: This is a temporary solution; the plan is to replace this by adding
        // a wildcard lookup method to the TupleMap implementation. This is
        // non-trivial to implement because it needs to account for things like
        // fallback route entries, hence this temporary workaround.
        const url = new URL(key.pathname, location.origin);
        const keyWithoutSearch = (0, _cachekey.createCacheKey)(url.href, key.nextUrl);
        const routeWithoutSearch = (0, _cache.readOrCreateRouteCacheEntry)(now, task, keyWithoutSearch);
        switch(routeWithoutSearch.status){
            case _cache.EntryStatus.Empty:
                {
                    if (background(task)) {
                        routeWithoutSearch.status = _cache.EntryStatus.Pending;
                        spawnPrefetchSubtask((0, _cache.fetchRouteOnCacheMiss)(routeWithoutSearch, keyWithoutSearch));
                    }
                    break;
                }
            case _cache.EntryStatus.Pending:
            case _cache.EntryStatus.Fulfilled:
            case _cache.EntryStatus.Rejected:
                {
                    break;
                }
            default:
                routeWithoutSearch;
        }
    }
    return exitStatus;
}
function pingRootRouteTree(now, task, route) {
    switch(route.status){
        case _cache.EntryStatus.Empty:
            {
                // Route is not yet cached, and there's no request already in progress.
                // Spawn a task to request the route, load it into the cache, and ping
                // the task to continue.
                // TODO: There are multiple strategies in the <Link> API for prefetching
                // a route. Currently we've only implemented the main one: per-segment,
                // static-data only.
                //
                // There's also `<Link prefetch={true}>`
                // which prefetch both static *and* dynamic data.
                // Similarly, we need to fallback to the old, per-page
                // behavior if PPR is disabled for a route (via the incremental opt-in).
                //
                // Those cases will be handled here.
                spawnPrefetchSubtask((0, _cache.fetchRouteOnCacheMiss)(route, task.key));
                // If the request takes longer than a minute, a subsequent request should
                // retry instead of waiting for this one. When the response is received,
                // this value will be replaced by a new value based on the stale time sent
                // from the server.
                // TODO: We should probably also manually abort the fetch task, to reclaim
                // server bandwidth.
                route.staleAt = now + 60 * 1000;
                // Upgrade to Pending so we know there's already a request in progress
                route.status = _cache.EntryStatus.Pending;
            // Intentional fallthrough to the Pending branch
            }
        case _cache.EntryStatus.Pending:
            {
                // Still pending. We can't start prefetching the segments until the route
                // tree has loaded. Add the task to the set of blocked tasks so that it
                // is notified when the route tree is ready.
                const blockedTasks = route.blockedTasks;
                if (blockedTasks === null) {
                    route.blockedTasks = new Set([
                        task
                    ]);
                } else {
                    blockedTasks.add(task);
                }
                return 1;
            }
        case _cache.EntryStatus.Rejected:
            {
                // Route tree failed to load. Treat as a 404.
                return 2;
            }
        case _cache.EntryStatus.Fulfilled:
            {
                if (task.phase !== 0) {
                    // Do not prefetch segment data until we've entered the segment phase.
                    return 2;
                }
                // Recursively fill in the segment tree.
                if (!hasNetworkBandwidth(task)) {
                    // Stop prefetching segments until there's more bandwidth.
                    return 0;
                }
                const tree = route.tree;
                // A task's fetch strategy gets set to `PPR` for any "auto" prefetch.
                // If it turned out that the route isn't PPR-enabled, we need to use `LoadingBoundary` instead.
                // We don't need to do this for runtime prefetches, because those are only available in
                // `cacheComponents`, where every route is PPR.
                let fetchStrategy;
                if (tree.prefetchHints & _approutertypes.PrefetchHint.SubtreeHasInstant) {
                    // If `instant` is defined anywhere on the target route, ignore the
                    // fetch strategy and switch to unified strategy used by Cache
                    // Components (called `PPR` for now, will likely be renamed).
                    //
                    // In practice, this just means that a "full" prefetch (<Link
                    // prefetch={true}>) has no effect. You're meant to use Runtime
                    // Prefetching instead — that's the new pattern that replaces
                    // prefetch={true}.
                    //
                    // The reason we check for `instant` rather than the `cacheComponents`
                    // flag is to support incremental adoption. `prefetch={true}` will
                    // continue to work until you opt into `instant`.
                    fetchStrategy = _types.FetchStrategy.PPR;
                } else if (task.fetchStrategy === _types.FetchStrategy.PPR) {
                    fetchStrategy = route.supportsPerSegmentPrefetching ? _types.FetchStrategy.PPR : _types.FetchStrategy.LoadingBoundary;
                } else {
                    fetchStrategy = task.fetchStrategy;
                }
                switch(fetchStrategy){
                    case _types.FetchStrategy.PPR:
                        {
                            // For Cache Components pages, each segment may be prefetched
                            // statically or using a runtime request, based on various
                            // configurations and heuristics. We'll do this in two passes: first
                            // traverse the tree and perform all the static prefetches.
                            //
                            // Then, if there are any segments that need a runtime request,
                            // do another pass to perform a runtime prefetch.
                            pingStaticHead(now, task, route);
                            const exitStatus = pingSharedPartOfCacheComponentsTree(now, task, route, task.treeAtTimeOfPrefetch, tree);
                            if (exitStatus === 0) {
                                // Child yielded without finishing.
                                return 0;
                            }
                            const spawnedRuntimePrefetches = task.spawnedRuntimePrefetches;
                            if (spawnedRuntimePrefetches !== null) {
                                // During the first pass, we discovered segments that require a
                                // runtime prefetch. Do a second pass to construct a request tree.
                                const spawnedEntries = new Map();
                                pingRuntimeHead(now, task, route, spawnedEntries, _types.FetchStrategy.PPRRuntime);
                                const requestTree = pingRuntimePrefetches(now, task, route, tree, spawnedRuntimePrefetches, spawnedEntries);
                                let needsDynamicRequest = spawnedEntries.size > 0;
                                if (needsDynamicRequest) {
                                    // Perform a dynamic prefetch request and populate the cache with
                                    // the result.
                                    spawnPrefetchSubtask((0, _cache.fetchSegmentPrefetchesUsingDynamicRequest)(task, route, _types.FetchStrategy.PPRRuntime, requestTree, spawnedEntries));
                                }
                            }
                            return 2;
                        }
                    case _types.FetchStrategy.Full:
                    case _types.FetchStrategy.PPRRuntime:
                    case _types.FetchStrategy.LoadingBoundary:
                        {
                            // Prefetch multiple segments using a single dynamic request.
                            // TODO: We can consolidate this branch with previous one by modeling
                            // it as if the first segment in the new tree has runtime prefetching
                            // enabled. Will do this as a follow-up refactor. Might want to remove
                            // the special metatdata case below first. In the meantime, it's not
                            // really that much duplication, just would be nice to remove one of
                            // these codepaths.
                            const spawnedEntries = new Map();
                            pingRuntimeHead(now, task, route, spawnedEntries, fetchStrategy);
                            const dynamicRequestTree = diffRouteTreeAgainstCurrent(now, task, route, task.treeAtTimeOfPrefetch, tree, spawnedEntries, fetchStrategy);
                            let needsDynamicRequest = spawnedEntries.size > 0;
                            if (needsDynamicRequest) {
                                spawnPrefetchSubtask((0, _cache.fetchSegmentPrefetchesUsingDynamicRequest)(task, route, fetchStrategy, dynamicRequestTree, spawnedEntries));
                            }
                            return 2;
                        }
                    default:
                        fetchStrategy;
                }
                break;
            }
        default:
            {
                route;
            }
    }
    return 2;
}
function pingStaticHead(now, task, route) {
    // The Head data for a page (metadata, viewport) is not really a route
    // segment, in the sense that it doesn't appear in the route tree. But we
    // store it in the cache as if it were, using a special key.
    pingStaticSegmentData(now, task, route, (0, _cache.readOrCreateSegmentCacheEntry)(now, _types.FetchStrategy.PPR, route.metadata), task.key, route.metadata);
}
function pingRuntimeHead(now, task, route, spawnedEntries, fetchStrategy) {
    pingRouteTreeAndIncludeDynamicData(now, task, route, route.metadata, false, spawnedEntries, // and LoadingBoundary
    fetchStrategy === _types.FetchStrategy.LoadingBoundary ? _types.FetchStrategy.Full : fetchStrategy);
}
// TODO: Rename dynamic -> runtime throughout this module
function pingSharedPartOfCacheComponentsTree(now, task, route, oldTree, newTree) {
    // When Cache Components is enabled (or PPR, or a fully static route when PPR
    // is disabled; those cases are treated equivalently to Cache Components), we
    // start by prefetching each segment individually. Once we reach the "new"
    // part of the tree — the part that doesn't exist on the current page — we
    // may choose to switch to a runtime prefetch instead, based on the
    // information sent by the server in the route tree.
    //
    // The traversal starts in the "shared" part of the tree. Once we reach the
    // "new" part of the tree, we switch to a different traversal,
    // pingNewPartOfCacheComponentsTree.
    // Prefetch this segment's static data.
    const segment = (0, _cache.readOrCreateSegmentCacheEntry)(now, task.fetchStrategy, newTree);
    pingStaticSegmentData(now, task, route, segment, task.key, newTree);
    // Recursively ping the children.
    const oldTreeChildren = oldTree[1];
    const newTreeChildren = newTree.slots;
    if (newTreeChildren !== null) {
        for(const parallelRouteKey in newTreeChildren){
            if (!hasNetworkBandwidth(task)) {
                // Stop prefetching segments until there's more bandwidth.
                return 0;
            }
            const newTreeChild = newTreeChildren[parallelRouteKey];
            const newTreeChildSegment = newTreeChild.segment;
            const oldTreeChild = oldTreeChildren[parallelRouteKey];
            const oldTreeChildSegment = oldTreeChild?.[0];
            let childExitStatus;
            if (oldTreeChildSegment !== undefined && doesCurrentSegmentMatchCachedSegment(route, newTreeChildSegment, oldTreeChildSegment)) {
                // We're still in the "shared" part of the tree.
                childExitStatus = pingSharedPartOfCacheComponentsTree(now, task, route, oldTreeChild, newTreeChild);
            } else {
                // We've entered the "new" part of the tree. Switch
                // traversal functions.
                childExitStatus = pingNewPartOfCacheComponentsTree(now, task, route, newTreeChild);
            }
            if (childExitStatus === 0) {
                // Child yielded without finishing.
                return 0;
            }
        }
    }
    return 2;
}
function pingNewPartOfCacheComponentsTree(now, task, route, tree) {
    // We're now prefetching in the "new" part of the tree, the part that doesn't
    // exist on the current page. (In other words, we're deeper than the
    // shared layouts.) Segments in here default to being prefetched statically.
    // However, if the server instructs us to, we may switch to a runtime
    // prefetch instead. Traverse the tree and check at each segment.
    if (tree.prefetchHints & _approutertypes.PrefetchHint.HasRuntimePrefetch) {
        // This route has a runtime prefetch response. Since we're below the shared
        // layout, everything from this point should be prefetched using a single,
        // combined runtime request, rather than using per-segment static requests.
        // This is true even if some of the child segments are known to be fully
        // static — once we've decided to perform a runtime prefetch, we might as
        // well respond with the static segments in the same roundtrip. (That's how
        // regular navigations work, too.) We'll still skip over segments that are
        // already cached, though.
        //
        // It's the server's responsibility to set a reasonable value of
        // `hasRuntimePrefetch`. Currently it's user-defined, but eventually, the
        // server may send a value of `false` even if the user opts in, if it
        // determines during build that the route is always fully static. There are
        // more optimizations we can do once we implement fallback param
        // tracking, too.
        //
        // Use the task object to collect the segments that need a runtime prefetch.
        // This will signal to the outer task queue that a second traversal is
        // required to construct a request tree.
        if (task.spawnedRuntimePrefetches === null) {
            task.spawnedRuntimePrefetches = new Set([
                tree.requestKey
            ]);
        } else {
            task.spawnedRuntimePrefetches.add(tree.requestKey);
        }
        // Then exit the traversal without prefetching anything further.
        return 2;
    }
    // This segment should not be runtime prefetched. Prefetch its static data.
    const segment = (0, _cache.readOrCreateSegmentCacheEntry)(now, task.fetchStrategy, tree);
    pingStaticSegmentData(now, task, route, segment, task.key, tree);
    if (tree.slots !== null) {
        if (!hasNetworkBandwidth(task)) {
            // Stop prefetching segments until there's more bandwidth.
            return 0;
        }
        // Recursively ping the children.
        for(const parallelRouteKey in tree.slots){
            const childTree = tree.slots[parallelRouteKey];
            const childExitStatus = pingNewPartOfCacheComponentsTree(now, task, route, childTree);
            if (childExitStatus === 0) {
                // Child yielded without finishing.
                return 0;
            }
        }
    }
    // This segment and all its children have finished prefetching.
    return 2;
}
function diffRouteTreeAgainstCurrent(now, task, route, oldTree, newTree, spawnedEntries, fetchStrategy) {
    // This is a single recursive traversal that does multiple things:
    // - Finds the parts of the target route (newTree) that are not part of
    //   of the current page (oldTree) by diffing them, using the same algorithm
    //   as a real navigation.
    // - Constructs a request tree (FlightRouterState) that describes which
    //   segments need to be prefetched and which ones are already cached.
    // - Creates a set of pending cache entries for the segments that need to
    //   be prefetched, so that a subsequent prefetch task does not request the
    //   same segments again.
    const oldTreeChildren = oldTree[1];
    const newTreeChildren = newTree.slots;
    let requestTreeChildren = {};
    if (newTreeChildren !== null) {
        for(const parallelRouteKey in newTreeChildren){
            const newTreeChild = newTreeChildren[parallelRouteKey];
            const newTreeChildSegment = newTreeChild.segment;
            const oldTreeChild = oldTreeChildren[parallelRouteKey];
            const oldTreeChildSegment = oldTreeChild?.[0];
            if (oldTreeChildSegment !== undefined && doesCurrentSegmentMatchCachedSegment(route, newTreeChildSegment, oldTreeChildSegment)) {
                // This segment is already part of the current route. Keep traversing.
                const requestTreeChild = diffRouteTreeAgainstCurrent(now, task, route, oldTreeChild, newTreeChild, spawnedEntries, fetchStrategy);
                requestTreeChildren[parallelRouteKey] = requestTreeChild;
            } else {
                // This segment is not part of the current route. We're entering a
                // part of the tree that we need to prefetch (unless everything is
                // already cached).
                switch(fetchStrategy){
                    case _types.FetchStrategy.LoadingBoundary:
                        {
                            // When PPR is disabled, we can't prefetch per segment. We must
                            // fallback to the old prefetch behavior and send a dynamic request.
                            // Only routes that include a loading boundary can be prefetched in
                            // this way.
                            //
                            // This is simlar to a "full" prefetch, but we're much more
                            // conservative about which segments to include in the request.
                            //
                            // The server will only render up to the first loading boundary
                            // inside new part of the tree. If there's no loading boundary
                            // anywhere in the tree, the server will never return any data, so
                            // we can skip the request.
                            const subtreeHasLoadingBoundary = (newTreeChild.prefetchHints & (_approutertypes.PrefetchHint.SegmentHasLoadingBoundary | _approutertypes.PrefetchHint.SubtreeHasLoadingBoundary)) !== 0;
                            const requestTreeChild = subtreeHasLoadingBoundary ? pingPPRDisabledRouteTreeUpToLoadingBoundary(now, task, route, newTreeChild, null, spawnedEntries) : (0, _cache.convertRouteTreeToFlightRouterState)(newTreeChild);
                            requestTreeChildren[parallelRouteKey] = requestTreeChild;
                            break;
                        }
                    case _types.FetchStrategy.PPRRuntime:
                        {
                            // This is a runtime prefetch. Fetch all cacheable data in the tree,
                            // not just the static PPR shell.
                            const requestTreeChild = pingRouteTreeAndIncludeDynamicData(now, task, route, newTreeChild, false, spawnedEntries, fetchStrategy);
                            requestTreeChildren[parallelRouteKey] = requestTreeChild;
                            break;
                        }
                    case _types.FetchStrategy.Full:
                        {
                            // This is a "full" prefetch. Fetch all the data in the tree, both
                            // static and dynamic. We issue roughly the same request that we
                            // would during a real navigation. The goal is that once the
                            // navigation occurs, the router should not have to fetch any
                            // additional data.
                            //
                            // Although the response will include dynamic data, opting into a
                            // Full prefetch — via <Link prefetch={true}> — implicitly
                            // instructs the cache to treat the response as "static", or non-
                            // dynamic, since the whole point is to cache it for
                            // future navigations.
                            //
                            // Construct a tree (currently a FlightRouterState) that represents
                            // which segments need to be prefetched and which ones are already
                            // cached. If the tree is empty, then we can exit. Otherwise, we'll
                            // send the request tree to the server and use the response to
                            // populate the segment cache.
                            const requestTreeChild = pingRouteTreeAndIncludeDynamicData(now, task, route, newTreeChild, false, spawnedEntries, fetchStrategy);
                            requestTreeChildren[parallelRouteKey] = requestTreeChild;
                            break;
                        }
                    default:
                        fetchStrategy;
                }
            }
        }
    }
    const requestTree = [
        newTree.segment,
        requestTreeChildren,
        null,
        null
    ];
    return requestTree;
}
function pingPPRDisabledRouteTreeUpToLoadingBoundary(now, task, route, tree, refetchMarkerContext, spawnedEntries) {
    // This function is similar to pingRouteTreeAndIncludeDynamicData, except the
    // server is only going to return a minimal loading state — it will stop
    // rendering at the first loading boundary. Whereas a Full prefetch is
    // intentionally aggressive and tries to pretfetch all the data that will be
    // needed for a navigation, a LoadingBoundary prefetch is much more
    // conservative. For example, it will omit from the request tree any segment
    // that is already cached, regardles of whether it's partial or full. By
    // contrast, a Full prefetch will refetch partial segments.
    // "inside-shared-layout" tells the server where to start looking for a
    // loading boundary.
    let refetchMarker = refetchMarkerContext === null ? 'inside-shared-layout' : null;
    const segment = (0, _cache.readOrCreateSegmentCacheEntry)(now, task.fetchStrategy, tree);
    switch(segment.status){
        case _cache.EntryStatus.Empty:
            {
                // This segment is not cached. Add a refetch marker so the server knows
                // to start rendering here.
                // TODO: Instead of a "refetch" marker, we could just omit this subtree's
                // FlightRouterState from the request tree. I think this would probably
                // already work even without any updates to the server. For consistency,
                // though, I'll send the full tree and we'll look into this later as part
                // of a larger redesign of the request protocol.
                // Add the pending cache entry to the result map.
                spawnedEntries.set(tree.requestKey, (0, _cache.upgradeToPendingSegment)(segment, // might not include it in the pending response. If another route is able
                // to issue a per-segment request, we'll do that in the background.
                _types.FetchStrategy.LoadingBoundary));
                if (refetchMarkerContext !== 'refetch') {
                    refetchMarker = refetchMarkerContext = 'refetch';
                } else {
                // There's already a parent with a refetch marker, so we don't need
                // to add another one.
                }
                break;
            }
        case _cache.EntryStatus.Fulfilled:
            {
                // The segment is already cached.
                const segmentHasLoadingBoundary = (tree.prefetchHints & _approutertypes.PrefetchHint.SegmentHasLoadingBoundary) !== 0;
                if (segmentHasLoadingBoundary) {
                    // This segment has a loading boundary, which means the server won't
                    // render its children. So there's nothing left to prefetch along this
                    // path. We can bail out.
                    return (0, _cache.convertRouteTreeToFlightRouterState)(tree);
                }
                break;
            }
        case _cache.EntryStatus.Pending:
            {
                break;
            }
        case _cache.EntryStatus.Rejected:
            {
                break;
            }
        default:
            segment;
    }
    const requestTreeChildren = {};
    if (tree.slots !== null) {
        for(const parallelRouteKey in tree.slots){
            const childTree = tree.slots[parallelRouteKey];
            requestTreeChildren[parallelRouteKey] = pingPPRDisabledRouteTreeUpToLoadingBoundary(now, task, route, childTree, refetchMarkerContext, spawnedEntries);
        }
    }
    const requestTree = [
        tree.segment,
        requestTreeChildren,
        null,
        refetchMarker
    ];
    return requestTree;
}
function pingRouteTreeAndIncludeDynamicData(now, task, route, tree, isInsideRefetchingParent, spawnedEntries, fetchStrategy) {
    // The tree we're constructing is the same shape as the tree we're navigating
    // to. But even though this is a "new" tree, some of the individual segments
    // may be cached as a result of other route prefetches.
    //
    // So we need to find the first uncached segment along each path add an
    // explicit "refetch" marker so the server knows where to start rendering.
    // Once the server starts rendering along a path, it keeps rendering the
    // entire subtree.
    const segment = (0, _cache.readOrCreateSegmentCacheEntry)(now, // and we have to use the former here.
    // We can have a task with `FetchStrategy.PPR` where some of its segments are configured to
    // always use runtime prefetching (via `export const prefetch`), and those should check for
    // entries that include search params.
    fetchStrategy, tree);
    let spawnedSegment = null;
    switch(segment.status){
        case _cache.EntryStatus.Empty:
            {
                // This segment is not cached.
                if (fetchStrategy === _types.FetchStrategy.Full) {
                    // Check if there's a matching entry in the bfcache. If so, fulfill the
                    // segment using the bfcache entry instead of issuing a new request.
                    const fulfilled = (0, _cache.attemptToFulfillDynamicSegmentFromBFCache)(now, segment, tree);
                    if (fulfilled !== null) {
                        break;
                    }
                }
                // Include it in the request.
                spawnedSegment = (0, _cache.upgradeToPendingSegment)(segment, fetchStrategy);
                break;
            }
        case _cache.EntryStatus.Fulfilled:
            {
                // The segment is already cached.
                if (segment.isPartial && (0, _cache.canNewFetchStrategyProvideMoreContent)(segment.fetchStrategy, fetchStrategy)) {
                    // The cached segment contains dynamic holes, and was prefetched using a
                    // less specific strategy than the current one. This means we're in one
                    // of these cases:
                    //   - we have a static prefetch, and we're doing a runtime prefetch
                    //   - we have a static or runtime prefetch, and we're doing a Full
                    //     prefetch (or a navigation).
                    // In either case, we need to include it in the request to get a more
                    // specific (or full) version. However, if there's a non-stale bfcache
                    // entry from a previous navigation, prefer that over making a new
                    // request.
                    if (fetchStrategy === _types.FetchStrategy.Full) {
                        const fulfilled = (0, _cache.attemptToUpgradeSegmentFromBFCache)(now, tree);
                        if (fulfilled !== null) {
                            break;
                        }
                    }
                    spawnedSegment = pingFullSegmentRevalidation(now, tree, fetchStrategy);
                }
                break;
            }
        case _cache.EntryStatus.Pending:
        case _cache.EntryStatus.Rejected:
            {
                // There's either another prefetch currently in progress, or the previous
                // attempt failed. If the new strategy can provide more content, fetch it again.
                if ((0, _cache.canNewFetchStrategyProvideMoreContent)(segment.fetchStrategy, fetchStrategy)) {
                    spawnedSegment = pingFullSegmentRevalidation(now, tree, fetchStrategy);
                }
                break;
            }
        default:
            segment;
    }
    const requestTreeChildren = {};
    if (tree.slots !== null) {
        for(const parallelRouteKey in tree.slots){
            const childTree = tree.slots[parallelRouteKey];
            requestTreeChildren[parallelRouteKey] = pingRouteTreeAndIncludeDynamicData(now, task, route, childTree, isInsideRefetchingParent || spawnedSegment !== null, spawnedEntries, fetchStrategy);
        }
    }
    if (spawnedSegment !== null) {
        // Add the pending entry to the result map.
        spawnedEntries.set(tree.requestKey, spawnedSegment);
    }
    // Don't bother to add a refetch marker if one is already present in a parent.
    const refetchMarker = !isInsideRefetchingParent && spawnedSegment !== null ? 'refetch' : null;
    const requestTree = [
        tree.segment,
        requestTreeChildren,
        null,
        refetchMarker
    ];
    return requestTree;
}
function pingRuntimePrefetches(now, task, route, tree, spawnedRuntimePrefetches, spawnedEntries) {
    // Construct a request tree (FlightRouterState) for a runtime prefetch. If
    // a segment is part of the runtime prefetch, the tree is constructed by
    // diffing against what's already in the prefetch cache. Otherwise, we send
    // a regular FlightRouterState with no special markers.
    //
    // See pingRouteTreeAndIncludeDynamicData for details.
    if (spawnedRuntimePrefetches.has(tree.requestKey)) {
        // This segment needs a runtime prefetch.
        return pingRouteTreeAndIncludeDynamicData(now, task, route, tree, false, spawnedEntries, _types.FetchStrategy.PPRRuntime);
    }
    let requestTreeChildren = {};
    const slots = tree.slots;
    if (slots !== null) {
        for(const parallelRouteKey in slots){
            const childTree = slots[parallelRouteKey];
            requestTreeChildren[parallelRouteKey] = pingRuntimePrefetches(now, task, route, childTree, spawnedRuntimePrefetches, spawnedEntries);
        }
    }
    // This segment is not part of the runtime prefetch. Clone the base tree.
    const requestTree = [
        tree.segment,
        requestTreeChildren,
        null,
        null
    ];
    return requestTree;
}
function pingStaticSegmentData(now, task, route, segment, routeKey, tree) {
    switch(segment.status){
        case _cache.EntryStatus.Empty:
            if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
            ;
            // Upgrade to Pending so we know there's already a request in progress
            spawnPrefetchSubtask((0, _cache.fetchSegmentOnCacheMiss)(route, (0, _cache.upgradeToPendingSegment)(segment, _types.FetchStrategy.PPR), routeKey, tree));
            break;
        case _cache.EntryStatus.Pending:
            {
                // There's already a request in progress. Depending on what kind of
                // request it is, we may want to revalidate it.
                switch(segment.fetchStrategy){
                    case _types.FetchStrategy.PPR:
                    case _types.FetchStrategy.PPRRuntime:
                    case _types.FetchStrategy.Full:
                        break;
                    case _types.FetchStrategy.LoadingBoundary:
                        // There's a pending request, but because it's using the old
                        // prefetching strategy, we can't be sure if it will be fulfilled by
                        // the response — it might be inside the loading boundary. Perform
                        // a revalidation, but because it's speculative, wait to do it at
                        // background priority.
                        if (background(task)) {
                            // TODO: Instead of speculatively revalidating, consider including
                            // `hasLoading` in the route tree prefetch response.
                            pingPPRSegmentRevalidation(now, route, routeKey, tree);
                        }
                        break;
                    default:
                        segment.fetchStrategy;
                }
                break;
            }
        case _cache.EntryStatus.Rejected:
            {
                // The existing entry in the cache was rejected. Depending on how it
                // was originally fetched, we may or may not want to revalidate it.
                switch(segment.fetchStrategy){
                    case _types.FetchStrategy.PPR:
                    case _types.FetchStrategy.PPRRuntime:
                    case _types.FetchStrategy.Full:
                        break;
                    case _types.FetchStrategy.LoadingBoundary:
                        // There's a rejected entry, but it was fetched using the loading
                        // boundary strategy. So the reason it wasn't returned by the server
                        // might just be because it was inside a loading boundary. Or because
                        // there was a dynamic rewrite. Revalidate it using the per-
                        // segment strategy.
                        //
                        // Because a rejected segment will definitely prevent the segment (and
                        // all of its children) from rendering, we perform this revalidation
                        // immediately instead of deferring it to a background task.
                        pingPPRSegmentRevalidation(now, route, routeKey, tree);
                        break;
                    default:
                        segment.fetchStrategy;
                }
                break;
            }
        case _cache.EntryStatus.Fulfilled:
            break;
        default:
            segment;
    }
// Segments do not have dependent tasks, so once the prefetch is initiated,
// there's nothing else for us to do (except write the server data into the
// entry, which is handled by `fetchSegmentOnCacheMiss`).
}
/**
 * Walks the RouteTree (including the head metadata) and collects any segments
 * that are still Empty into a Map, upgrading them to Pending. These entries
 * will be fulfilled by the inlined prefetch response.
 */ function collectInlinedEntries(now, route) {
    const entries = new Map();
    collectInlinedEntriesImpl(now, route.tree, entries);
    // Also collect the head/metadata entry.
    const headEntry = (0, _cache.readOrCreateSegmentCacheEntry)(now, _types.FetchStrategy.PPR, route.metadata);
    if (headEntry.status === _cache.EntryStatus.Empty) {
        entries.set(route.metadata.requestKey, (0, _cache.upgradeToPendingSegment)(headEntry, _types.FetchStrategy.PPR));
    }
    return entries;
}
function collectInlinedEntriesImpl(now, tree, entries) {
    const entry = (0, _cache.readOrCreateSegmentCacheEntry)(now, _types.FetchStrategy.PPR, tree);
    if (entry.status === _cache.EntryStatus.Empty) {
        entries.set(tree.requestKey, (0, _cache.upgradeToPendingSegment)(entry, _types.FetchStrategy.PPR));
    }
    if (tree.slots !== null) {
        for(const parallelRouteKey in tree.slots){
            collectInlinedEntriesImpl(now, tree.slots[parallelRouteKey], entries);
        }
    }
}
function pingPPRSegmentRevalidation(now, route, routeKey, tree) {
    const revalidatingSegment = (0, _cache.readOrCreateRevalidatingSegmentEntry)(now, _types.FetchStrategy.PPR, tree);
    switch(revalidatingSegment.status){
        case _cache.EntryStatus.Empty:
            // Spawn a prefetch request. The fetch function handles upserting
            // the entry at the correct fulfilled vary path upon completion.
            spawnPrefetchSubtask((0, _cache.fetchSegmentOnCacheMiss)(route, (0, _cache.upgradeToPendingSegment)(revalidatingSegment, _types.FetchStrategy.PPR), routeKey, tree));
            break;
        case _cache.EntryStatus.Pending:
            break;
        case _cache.EntryStatus.Fulfilled:
        case _cache.EntryStatus.Rejected:
            break;
        default:
            revalidatingSegment;
    }
}
function pingFullSegmentRevalidation(now, tree, fetchStrategy) {
    const revalidatingSegment = (0, _cache.readOrCreateRevalidatingSegmentEntry)(now, fetchStrategy, tree);
    if (revalidatingSegment.status === _cache.EntryStatus.Empty) {
        // During a Full/PPRRuntime prefetch, a single dynamic request is made for all the
        // segments that we need. So we don't initiate a request here directly. By
        // returning a pending entry from this function, it signals to the caller
        // that this segment should be included in the request that's sent to
        // the server.
        const pendingSegment = (0, _cache.upgradeToPendingSegment)(revalidatingSegment, fetchStrategy);
        // The upsert is handled by fulfillEntrySpawnedByRuntimePrefetch
        // when the dynamic prefetch response is written into the cache.
        return pendingSegment;
    } else {
        // There's already a revalidation in progress.
        const nonEmptyRevalidatingSegment = revalidatingSegment;
        if ((0, _cache.canNewFetchStrategyProvideMoreContent)(nonEmptyRevalidatingSegment.fetchStrategy, fetchStrategy)) {
            // The existing revalidation was fetched using a less specific strategy.
            // Reset it and start a new revalidation.
            const emptySegment = (0, _cache.overwriteRevalidatingSegmentCacheEntry)(now, fetchStrategy, tree);
            const pendingSegment = (0, _cache.upgradeToPendingSegment)(emptySegment, fetchStrategy);
            // The upsert is handled by fulfillEntrySpawnedByRuntimePrefetch
            // when the dynamic prefetch response is written into the cache.
            return pendingSegment;
        }
        switch(nonEmptyRevalidatingSegment.status){
            case _cache.EntryStatus.Pending:
                // There's already an in-progress prefetch that includes this segment.
                return null;
            case _cache.EntryStatus.Fulfilled:
            case _cache.EntryStatus.Rejected:
                // A previous revalidation attempt finished, but we chose not to replace
                // the existing entry in the cache. Don't try again until or unless the
                // revalidation entry expires.
                return null;
            default:
                nonEmptyRevalidatingSegment;
                return null;
        }
    }
}
function doesCurrentSegmentMatchCachedSegment(route, currentSegment, cachedSegment) {
    if (cachedSegment === _segment.PAGE_SEGMENT_KEY) {
        // In the FlightRouterState stored by the router, the page segment has the
        // rendered search params appended to the name of the segment. In the
        // prefetch cache, however, this is stored separately. So, when comparing
        // the router's current FlightRouterState to the cached FlightRouterState,
        // we need to make sure we compare both parts of the segment.
        // TODO: This is not modeled clearly. We use the same type,
        // FlightRouterState, for both the CacheNode tree _and_ the prefetch cache
        // _and_ the server response format, when conceptually those are three
        // different things and treated in different ways. We should encode more of
        // this information into the type design so mistakes are less likely.
        return currentSegment === (0, _segment.addSearchParamsIfPageSegment)(_segment.PAGE_SEGMENT_KEY, Object.fromEntries(new URLSearchParams(route.renderedSearch)));
    }
    // Non-page segments are compared using the same function as the server
    return (0, _matchsegments.matchSegment)(cachedSegment, currentSegment);
}
// -----------------------------------------------------------------------------
// The remainder of the module is a MinHeap implementation. Try not to put any
// logic below here unless it's related to the heap algorithm. We can extract
// this to a separate module if/when we need multiple kinds of heaps.
// -----------------------------------------------------------------------------
function compareQueuePriority(a, b) {
    // Since the queue is a MinHeap, this should return a positive number if b is
    // higher priority than a, and a negative number if a is higher priority
    // than b.
    // `priority` is an integer, where higher numbers are higher priority.
    const priorityDiff = b.priority - a.priority;
    if (priorityDiff !== 0) {
        return priorityDiff;
    }
    // If the priority is the same, check which phase the prefetch is in — is it
    // prefetching the route tree, or the segments? Route trees are prioritized.
    const phaseDiff = b.phase - a.phase;
    if (phaseDiff !== 0) {
        return phaseDiff;
    }
    // Finally, check the insertion order. `sortId` is an incrementing counter
    // assigned to prefetches. We want to process the newest prefetches first.
    return b.sortId - a.sortId;
}
function heapPush(heap, node) {
    const index = heap.length;
    heap.push(node);
    node._heapIndex = index;
    heapSiftUp(heap, node, index);
}
function heapPeek(heap) {
    return heap.length === 0 ? null : heap[0];
}
function heapPop(heap) {
    if (heap.length === 0) {
        return null;
    }
    const first = heap[0];
    first._heapIndex = -1;
    const last = heap.pop();
    if (last !== first) {
        heap[0] = last;
        last._heapIndex = 0;
        heapSiftDown(heap, last, 0);
    }
    return first;
}
function heapDelete(heap, node) {
    const index = node._heapIndex;
    if (index !== -1) {
        node._heapIndex = -1;
        if (heap.length !== 0) {
            const last = heap.pop();
            if (last !== node) {
                heap[index] = last;
                last._heapIndex = index;
                heapSiftDown(heap, last, index);
            }
        }
    }
}
function heapResift(heap, node) {
    const index = node._heapIndex;
    if (index !== -1) {
        if (index === 0) {
            heapSiftDown(heap, node, 0);
        } else {
            const parentIndex = index - 1 >>> 1;
            const parent = heap[parentIndex];
            if (compareQueuePriority(parent, node) > 0) {
                // The parent is larger. Sift up.
                heapSiftUp(heap, node, index);
            } else {
                // The parent is smaller (or equal). Sift down.
                heapSiftDown(heap, node, index);
            }
        }
    }
}
function heapSiftUp(heap, node, i) {
    let index = i;
    while(index > 0){
        const parentIndex = index - 1 >>> 1;
        const parent = heap[parentIndex];
        if (compareQueuePriority(parent, node) > 0) {
            // The parent is larger. Swap positions.
            heap[parentIndex] = node;
            node._heapIndex = parentIndex;
            heap[index] = parent;
            parent._heapIndex = index;
            index = parentIndex;
        } else {
            // The parent is smaller. Exit.
            return;
        }
    }
}
function heapSiftDown(heap, node, i) {
    let index = i;
    const length = heap.length;
    const halfLength = length >>> 1;
    while(index < halfLength){
        const leftIndex = (index + 1) * 2 - 1;
        const left = heap[leftIndex];
        const rightIndex = leftIndex + 1;
        const right = heap[rightIndex];
        // If the left or right node is smaller, swap with the smaller of those.
        if (compareQueuePriority(left, node) < 0) {
            if (rightIndex < length && compareQueuePriority(right, left) < 0) {
                heap[index] = right;
                right._heapIndex = index;
                heap[rightIndex] = node;
                node._heapIndex = rightIndex;
                index = rightIndex;
            } else {
                heap[index] = left;
                left._heapIndex = index;
                heap[leftIndex] = node;
                node._heapIndex = leftIndex;
                index = leftIndex;
            }
        } else if (rightIndex < length && compareQueuePriority(right, node) < 0) {
            heap[index] = right;
            right._heapIndex = index;
            heap[rightIndex] = node;
            node._heapIndex = rightIndex;
            index = rightIndex;
        } else {
            // Neither child is smaller. Exit.
            return;
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/vary-path.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    appendLayoutVaryPath: null,
    clonePageVaryPathWithNewSearchParams: null,
    finalizeLayoutVaryPath: null,
    finalizeMetadataVaryPath: null,
    finalizePageVaryPath: null,
    getFulfilledRouteVaryPath: null,
    getFulfilledSegmentVaryPath: null,
    getPartialLayoutVaryPath: null,
    getPartialPageVaryPath: null,
    getRenderedSearchFromVaryPath: null,
    getRouteVaryPath: null,
    getSegmentVaryPathForRequest: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    appendLayoutVaryPath: function() {
        return appendLayoutVaryPath;
    },
    clonePageVaryPathWithNewSearchParams: function() {
        return clonePageVaryPathWithNewSearchParams;
    },
    finalizeLayoutVaryPath: function() {
        return finalizeLayoutVaryPath;
    },
    finalizeMetadataVaryPath: function() {
        return finalizeMetadataVaryPath;
    },
    finalizePageVaryPath: function() {
        return finalizePageVaryPath;
    },
    getFulfilledRouteVaryPath: function() {
        return getFulfilledRouteVaryPath;
    },
    getFulfilledSegmentVaryPath: function() {
        return getFulfilledSegmentVaryPath;
    },
    getPartialLayoutVaryPath: function() {
        return getPartialLayoutVaryPath;
    },
    getPartialPageVaryPath: function() {
        return getPartialPageVaryPath;
    },
    getRenderedSearchFromVaryPath: function() {
        return getRenderedSearchFromVaryPath;
    },
    getRouteVaryPath: function() {
        return getRouteVaryPath;
    },
    getSegmentVaryPathForRequest: function() {
        return getSegmentVaryPathForRequest;
    }
});
const _types = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/types.js [app-client] (ecmascript)");
const _cachemap = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache-map.js [app-client] (ecmascript)");
const _segmentvalueencoding = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/segment-cache/segment-value-encoding.js [app-client] (ecmascript)");
function getRouteVaryPath(pathname, search, nextUrl) {
    // requestKey -> searchParams -> nextUrl
    const varyPath = {
        id: null,
        value: pathname,
        parent: {
            id: '?',
            value: search,
            parent: {
                id: null,
                value: nextUrl,
                parent: null
            }
        }
    };
    return varyPath;
}
function getFulfilledRouteVaryPath(pathname, search, nextUrl, couldBeIntercepted) {
    // This is called when a route's data is fulfilled. The cache entry will be
    // re-keyed based on which inputs the response varies by.
    // requestKey -> searchParams -> nextUrl
    const varyPath = {
        id: null,
        value: pathname,
        parent: {
            id: '?',
            value: search,
            parent: {
                id: null,
                value: couldBeIntercepted ? nextUrl : _cachemap.Fallback,
                parent: null
            }
        }
    };
    return varyPath;
}
function appendLayoutVaryPath(parentPath, cacheKey, paramName) {
    const varyPathPart = {
        id: paramName,
        value: cacheKey,
        parent: parentPath
    };
    return varyPathPart;
}
function finalizeLayoutVaryPath(requestKey, varyPath) {
    const layoutVaryPath = {
        id: null,
        value: requestKey,
        parent: varyPath
    };
    return layoutVaryPath;
}
function getPartialLayoutVaryPath(finalizedVaryPath) {
    // This is the inverse of finalizeLayoutVaryPath.
    return finalizedVaryPath.parent;
}
function finalizePageVaryPath(requestKey, renderedSearch, varyPath) {
    // Unlike layouts, a page segment's vary path also includes the search string.
    // requestKey -> searchParams -> pathParams
    const pageVaryPath = {
        id: null,
        value: requestKey,
        parent: {
            id: '?',
            value: renderedSearch,
            parent: varyPath
        }
    };
    return pageVaryPath;
}
function getPartialPageVaryPath(finalizedVaryPath) {
    // This is the inverse of finalizePageVaryPath.
    return finalizedVaryPath.parent.parent;
}
function finalizeMetadataVaryPath(pageRequestKey, renderedSearch, varyPath) {
    // The metadata "segment" is not a real segment because it doesn't exist in
    // the normal structure of the route tree, but in terms of caching, it
    // behaves like a page segment because it varies by all the same params as
    // a page.
    //
    // To keep the protocol for querying the server simple, the request key for
    // the metadata does not include any path information. It's unnecessary from
    // the server's perspective, because unlike page segments, there's only one
    // metadata response per URL, i.e. there's no need to distinguish multiple
    // parallel pages.
    //
    // However, this means the metadata request key is insufficient for
    // caching the the metadata in the client cache, because on the client we
    // use the request key to distinguish the metadata entry from all other
    // page's metadata entries.
    //
    // So instead we create a simulated request key based on the page segment.
    // Conceptually this is equivalent to the request key the server would have
    // assigned the metadata segment if it treated it as part of the actual
    // route structure.
    // If there are multiple parallel pages, we use whichever is the first one.
    // This is fine because the only difference between request keys for
    // different parallel pages are things like route groups and parallel
    // route slots. As long as it's always the same one, it doesn't matter.
    const pageVaryPath = {
        id: null,
        // Append the actual metadata request key to the page request key. Note
        // that we're not using a separate vary path part; it's unnecessary because
        // these are not conceptually separate inputs.
        value: pageRequestKey + _segmentvalueencoding.HEAD_REQUEST_KEY,
        parent: {
            id: '?',
            value: renderedSearch,
            parent: varyPath
        }
    };
    return pageVaryPath;
}
function getSegmentVaryPathForRequest(fetchStrategy, tree) {
    // This is used for storing pending requests in the cache. We want to choose
    // the most generic vary path based on the strategy used to fetch it, i.e.
    // static/PPR versus runtime prefetching, so that it can be reused as much
    // as possible.
    //
    // We may be able to re-key the response to something even more generic once
    // we receive it — for example, if the server tells us that the response
    // doesn't vary on a particular param — but even before we send the request,
    // we know some params are reusable based on the fetch strategy alone. For
    // example, a static prefetch will never vary on search params.
    //
    // The original vary path with all the params filled in is stored on the
    // route tree object. We will clone this one to create a new vary path
    // where certain params are replaced with Fallback.
    //
    // This result of this function is not stored anywhere. It's only used to
    // access the cache a single time.
    //
    // TODO: Rather than create a new list object just to access the cache, the
    // plan is to add the concept of a "vary mask". This will represent all the
    // params that can be treated as Fallback. (Or perhaps the inverse.)
    const originalVaryPath = tree.varyPath;
    // Only page segments (and the special "metadata" segment, which is treated
    // like a page segment for the purposes of caching) may contain search
    // params. There's no reason to include them in the vary path otherwise.
    if (tree.isPage) {
        // Only a runtime prefetch will include search params in the vary path.
        // Static prefetches never include search params, so they can be reused
        // across all possible search param values.
        const doesVaryOnSearchParams = fetchStrategy === _types.FetchStrategy.Full || fetchStrategy === _types.FetchStrategy.PPRRuntime;
        if (!doesVaryOnSearchParams) {
            // The response from the the server will not vary on search params. Clone
            // the end of the original vary path to replace the search params
            // with Fallback.
            //
            // requestKey -> searchParams -> pathParams
            //               ^ This part gets replaced with Fallback
            const searchParamsVaryPath = originalVaryPath.parent;
            const pathParamsVaryPath = searchParamsVaryPath.parent;
            const patchedVaryPath = {
                id: null,
                value: originalVaryPath.value,
                parent: {
                    id: '?',
                    value: _cachemap.Fallback,
                    parent: pathParamsVaryPath
                }
            };
            return patchedVaryPath;
        }
    }
    // The request does vary on search params. We don't need to modify anything.
    return originalVaryPath;
}
function clonePageVaryPathWithNewSearchParams(originalVaryPath, newSearch) {
    // requestKey -> searchParams -> pathParams
    //               ^ This part gets replaced with newSearch
    const searchParamsVaryPath = originalVaryPath.parent;
    const clonedVaryPath = {
        id: null,
        value: originalVaryPath.value,
        parent: {
            id: '?',
            value: newSearch,
            parent: searchParamsVaryPath.parent
        }
    };
    return clonedVaryPath;
}
function getRenderedSearchFromVaryPath(varyPath) {
    const searchParams = varyPath.parent.value;
    return typeof searchParams === 'string' ? searchParams : null;
}
function getFulfilledSegmentVaryPath(original, varyParams) {
    // Re-keys a segment's vary path based on which params the segment actually
    // depends on. Params that are NOT in the varyParams set are replaced with
    // Fallback, allowing the cache entry to be reused across different values of
    // those params.
    // This is called when a segment is fulfilled with data from the server. The
    // varyParams set comes from the server and indicates which params were
    // accessed during rendering.
    const clone = {
        id: original.id,
        // If the id is null, this node is not a param (e.g., it's a request key).
        // If the id is in the varyParams set, keep the original value.
        // Otherwise, replace with Fallback to make it reusable.
        value: original.id === null || varyParams.has(original.id) ? original.value : _cachemap.Fallback,
        parent: original.parent === null ? null : getFulfilledSegmentVaryPath(original.parent, varyParams)
    };
    return clone;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/normalize-trailing-slash.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
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
const _removetrailingslash = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/remove-trailing-slash.js [app-client] (ecmascript)");
const _parsepath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/parse-path.js [app-client] (ecmascript)");
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/add-base-path.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
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
const _addpathprefix = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/add-path-prefix.js [app-client] (ecmascript)");
const _normalizetrailingslash = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/normalize-trailing-slash.js [app-client] (ecmascript)");
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-utils.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    createPrefetchURL: null,
    isExternalURL: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    createPrefetchURL: function() {
        return createPrefetchURL;
    },
    isExternalURL: function() {
        return isExternalURL;
    }
});
const _isbot = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/is-bot.js [app-client] (ecmascript)");
const _addbasepath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/add-base-path.js [app-client] (ecmascript)");
function isExternalURL(url) {
    return url.origin !== window.location.origin;
}
function createPrefetchURL(href) {
    // Don't prefetch for bots as they don't navigate.
    if ((0, _isbot.isBot)(window.navigator.userAgent)) {
        return null;
    }
    let url;
    try {
        url = new URL((0, _addbasepath.addBasePath)(href), window.location.href);
    } catch (_) {
        // TODO: Does this need to throw or can we just console.error instead? Does
        // anyone rely on this throwing? (Seems unlikely.)
        throw Object.defineProperty(new Error(`Cannot prefetch '${href}' because it cannot be converted to a URL.`), "__NEXT_ERROR_CODE", {
            value: "E234",
            enumerable: false,
            configurable: true
        });
    }
    // Don't prefetch during development (improves compilation performance)
    if ("TURBOPACK compile-time truthy", 1) {
        return null;
    }
    //TURBOPACK unreachable
    ;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/links.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    IDLE_LINK_STATUS: null,
    PENDING_LINK_STATUS: null,
    getLinkForCurrentNavigation: null,
    mountFormInstance: null,
    mountLinkInstance: null,
    onLinkVisibilityChanged: null,
    onNavigationIntent: null,
    pingVisibleLinks: null,
    setLinkForCurrentNavigation: null,
    unmountLinkForCurrentNavigation: null,
    unmountPrefetchableInstance: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    IDLE_LINK_STATUS: function() {
        return IDLE_LINK_STATUS;
    },
    PENDING_LINK_STATUS: function() {
        return PENDING_LINK_STATUS;
    },
    getLinkForCurrentNavigation: function() {
        return getLinkForCurrentNavigation;
    },
    mountFormInstance: function() {
        return mountFormInstance;
    },
    mountLinkInstance: function() {
        return mountLinkInstance;
    },
    onLinkVisibilityChanged: function() {
        return onLinkVisibilityChanged;
    },
    onNavigationIntent: function() {
        return onNavigationIntent;
    },
    pingVisibleLinks: function() {
        return pingVisibleLinks;
    },
    setLinkForCurrentNavigation: function() {
        return setLinkForCurrentNavigation;
    },
    unmountLinkForCurrentNavigation: function() {
        return unmountLinkForCurrentNavigation;
    },
    unmountPrefetchableInstance: function() {
        return unmountPrefetchableInstance;
    }
});
const _types = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/types.js [app-client] (ecmascript)");
const _cachekey = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache-key.js [app-client] (ecmascript)");
const _scheduler = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/scheduler.js [app-client] (ecmascript)");
const _react = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
// Tracks the most recently navigated link instance. When null, indicates
// the current navigation was not initiated by a link click.
let linkForMostRecentNavigation = null;
const PENDING_LINK_STATUS = {
    pending: true
};
const IDLE_LINK_STATUS = {
    pending: false
};
function setLinkForCurrentNavigation(link) {
    (0, _react.startTransition)(()=>{
        linkForMostRecentNavigation?.setOptimisticLinkStatus(IDLE_LINK_STATUS);
        link?.setOptimisticLinkStatus(PENDING_LINK_STATUS);
        linkForMostRecentNavigation = link;
    });
}
function unmountLinkForCurrentNavigation(link) {
    if (linkForMostRecentNavigation === link) {
        linkForMostRecentNavigation = null;
    }
}
function getLinkForCurrentNavigation() {
    return linkForMostRecentNavigation;
}
// Use a WeakMap to associate a Link instance with its DOM element. This is
// used by the IntersectionObserver to track the link's visibility.
const prefetchable = typeof WeakMap === 'function' ? new WeakMap() : new Map();
// A Set of the currently visible links. We re-prefetch visible links after a
// cache invalidation, or when the current URL changes. It's a separate data
// structure from the WeakMap above because only the visible links need to
// be enumerated.
const prefetchableAndVisible = new Set();
// A single IntersectionObserver instance shared by all <Link> components.
const observer = typeof IntersectionObserver === 'function' ? new IntersectionObserver(handleIntersect, {
    rootMargin: '200px'
}) : null;
function observeVisibility(element, instance) {
    const existingInstance = prefetchable.get(element);
    if (existingInstance !== undefined) {
        // This shouldn't happen because each <Link> component should have its own
        // anchor tag instance, but it's defensive coding to avoid a memory leak in
        // case there's a logical error somewhere else.
        unmountPrefetchableInstance(element);
    }
    // Only track prefetchable links that have a valid prefetch URL
    prefetchable.set(element, instance);
    if (observer !== null) {
        observer.observe(element);
    }
}
function coercePrefetchableUrl(href) {
    if (typeof window !== 'undefined') {
        const { createPrefetchURL } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-utils.js [app-client] (ecmascript)");
        try {
            return createPrefetchURL(href);
        } catch  {
            // createPrefetchURL sometimes throws an error if an invalid URL is
            // provided, though I'm not sure if it's actually necessary.
            // TODO: Consider removing the throw from the inner function, or change it
            // to reportError. Or maybe the error isn't even necessary for automatic
            // prefetches, just navigations.
            const reportErrorFn = typeof reportError === 'function' ? reportError : console.error;
            reportErrorFn(`Cannot prefetch '${href}' because it cannot be converted to a URL.`);
            return null;
        }
    } else {
        return null;
    }
}
function mountLinkInstance(element, href, router, fetchStrategy, prefetchEnabled, setOptimisticLinkStatus) {
    if (prefetchEnabled) {
        const prefetchURL = coercePrefetchableUrl(href);
        if (prefetchURL !== null) {
            const instance = {
                router,
                fetchStrategy,
                isVisible: false,
                prefetchTask: null,
                prefetchHref: prefetchURL.href,
                setOptimisticLinkStatus
            };
            // We only observe the link's visibility if it's prefetchable. For
            // example, this excludes links to external URLs.
            observeVisibility(element, instance);
            return instance;
        }
    }
    // If the link is not prefetchable, we still create an instance so we can
    // track its optimistic state (i.e. useLinkStatus).
    const instance = {
        router,
        fetchStrategy,
        isVisible: false,
        prefetchTask: null,
        prefetchHref: null,
        setOptimisticLinkStatus
    };
    return instance;
}
function mountFormInstance(element, href, router, fetchStrategy) {
    const prefetchURL = coercePrefetchableUrl(href);
    if (prefetchURL === null) {
        // This href is not prefetchable, so we don't track it.
        // TODO: We currently observe/unobserve a form every time its href changes.
        // For Links, this isn't a big deal because the href doesn't usually change,
        // but for forms it's extremely common. We should optimize this.
        return;
    }
    const instance = {
        router,
        fetchStrategy,
        isVisible: false,
        prefetchTask: null,
        prefetchHref: prefetchURL.href,
        setOptimisticLinkStatus: null
    };
    observeVisibility(element, instance);
}
function unmountPrefetchableInstance(element) {
    const instance = prefetchable.get(element);
    if (instance !== undefined) {
        prefetchable.delete(element);
        prefetchableAndVisible.delete(instance);
        const prefetchTask = instance.prefetchTask;
        if (prefetchTask !== null) {
            (0, _scheduler.cancelPrefetchTask)(prefetchTask);
        }
    }
    if (observer !== null) {
        observer.unobserve(element);
    }
}
function handleIntersect(entries) {
    for (const entry of entries){
        // Some extremely old browsers or polyfills don't reliably support
        // isIntersecting so we check intersectionRatio instead. (Do we care? Not
        // really. But whatever this is fine.)
        const isVisible = entry.intersectionRatio > 0;
        onLinkVisibilityChanged(entry.target, isVisible);
    }
}
function onLinkVisibilityChanged(element, isVisible) {
    if ("TURBOPACK compile-time truthy", 1) {
        // Prefetching on viewport is disabled in development for performance
        // reasons, because it requires compiling the target page.
        // TODO: Investigate re-enabling this.
        return;
    }
    //TURBOPACK unreachable
    ;
    const instance = undefined;
}
function onNavigationIntent(element, unstable_upgradeToDynamicPrefetch) {
    const instance = prefetchable.get(element);
    if (instance === undefined) {
        return;
    }
    // Prefetch the link on hover/touchstart.
    if (instance !== undefined) {
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
        rescheduleLinkPrefetch(instance, _types.PrefetchPriority.Intent);
    }
}
function rescheduleLinkPrefetch(instance, priority) {
    // Ensures that app-router-instance is not compiled in the server bundle
    if (typeof window !== 'undefined') {
        const existingPrefetchTask = instance.prefetchTask;
        if (!instance.isVisible) {
            // Cancel any in-progress prefetch task. (If it already finished then this
            // is a no-op.)
            if (existingPrefetchTask !== null) {
                (0, _scheduler.cancelPrefetchTask)(existingPrefetchTask);
            }
            // We don't need to reset the prefetchTask to null upon cancellation; an
            // old task object can be rescheduled with reschedulePrefetchTask. This is a
            // micro-optimization but also makes the code simpler (don't need to
            // worry about whether an old task object is stale).
            return;
        }
        const { getCurrentAppRouterState } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-instance.js [app-client] (ecmascript)");
        const appRouterState = getCurrentAppRouterState();
        if (appRouterState !== null) {
            const treeAtTimeOfPrefetch = appRouterState.tree;
            if (existingPrefetchTask === null) {
                // Initiate a prefetch task.
                const nextUrl = appRouterState.nextUrl;
                const cacheKey = (0, _cachekey.createCacheKey)(instance.prefetchHref, nextUrl);
                instance.prefetchTask = (0, _scheduler.schedulePrefetchTask)(cacheKey, treeAtTimeOfPrefetch, instance.fetchStrategy, priority, null);
            } else {
                // We already have an old task object that we can reschedule. This is
                // effectively the same as canceling the old task and creating a new one.
                (0, _scheduler.reschedulePrefetchTask)(existingPrefetchTask, treeAtTimeOfPrefetch, instance.fetchStrategy, priority);
            }
        }
    }
}
function pingVisibleLinks(nextUrl, tree) {
    // For each currently visible link, cancel the existing prefetch task (if it
    // exists) and schedule a new one. This is effectively the same as if all the
    // visible links left and then re-entered the viewport.
    //
    // This is called when the Next-Url or the base tree changes, since those
    // may affect the result of a prefetch task. It's also called after a
    // cache invalidation.
    for (const instance of prefetchableAndVisible){
        const task = instance.prefetchTask;
        if (task !== null && !(0, _scheduler.isPrefetchTaskDirty)(task, nextUrl, tree)) {
            continue;
        }
        // Something changed. Cancel the existing prefetch task and schedule a
        // new one.
        if (task !== null) {
            (0, _scheduler.cancelPrefetchTask)(task);
        }
        const cacheKey = (0, _cachekey.createCacheKey)(instance.prefetchHref, nextUrl);
        instance.prefetchTask = (0, _scheduler.schedulePrefetchTask)(cacheKey, tree, instance.fetchStrategy, _types.PrefetchPriority.Default, null);
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/bfcache.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    UnknownDynamicStaleTime: null,
    computeDynamicStaleAt: null,
    invalidateBfCache: null,
    readFromBFCache: null,
    readFromBFCacheDuringRegularNavigation: null,
    updateBFCacheEntryStaleAt: null,
    writeHeadToBFCache: null,
    writeToBFCache: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    UnknownDynamicStaleTime: function() {
        return UnknownDynamicStaleTime;
    },
    computeDynamicStaleAt: function() {
        return computeDynamicStaleAt;
    },
    invalidateBfCache: function() {
        return invalidateBfCache;
    },
    readFromBFCache: function() {
        return readFromBFCache;
    },
    readFromBFCacheDuringRegularNavigation: function() {
        return readFromBFCacheDuringRegularNavigation;
    },
    updateBFCacheEntryStaleAt: function() {
        return updateBFCacheEntryStaleAt;
    },
    writeHeadToBFCache: function() {
        return writeHeadToBFCache;
    },
    writeToBFCache: function() {
        return writeToBFCache;
    }
});
const _navigatereducer = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/navigate-reducer.js [app-client] (ecmascript)");
const _cachemap = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache-map.js [app-client] (ecmascript)");
const UnknownDynamicStaleTime = -1;
function computeDynamicStaleAt(now, dynamicStaleTimeSeconds) {
    return dynamicStaleTimeSeconds !== UnknownDynamicStaleTime ? now + dynamicStaleTimeSeconds * 1000 : now + _navigatereducer.DYNAMIC_STALETIME_MS;
}
const bfcacheMap = (0, _cachemap.createCacheMap)();
let currentBfCacheVersion = 0;
function invalidateBfCache() {
    if (typeof window === 'undefined') {
        return;
    }
    currentBfCacheVersion++;
}
function writeToBFCache(now, varyPath, rsc, prefetchRsc, head, prefetchHead, dynamicStaleAt) {
    if (typeof window === 'undefined') {
        return;
    }
    const entry = {
        rsc,
        prefetchRsc,
        // TODO: These fields will be removed from both BFCacheEntry and
        // SegmentCacheEntry. The head has its own separate cache entry.
        head,
        prefetchHead,
        ref: null,
        // TODO: This is just a heuristic. Getting the actual size of the segment
        // isn't feasible because it's part of a larger streaming response. The
        // LRU will still evict it, we just won't have a fully accurate total
        // LRU size. However, we'll probably remove the size tracking from the LRU
        // entirely and use memory pressure events instead.
        size: 100,
        navigatedAt: now,
        // A back/forward navigation will disregard the stale time. This field is
        // only relevant when staleTimes.dynamic is enabled or unstable_dynamicStaleTime
        // is exported by a page.
        staleAt: dynamicStaleAt,
        version: currentBfCacheVersion
    };
    const isRevalidation = false;
    (0, _cachemap.setInCacheMap)(bfcacheMap, varyPath, entry, isRevalidation);
}
function writeHeadToBFCache(now, varyPath, head, prefetchHead, dynamicStaleAt) {
    // Read the special "segment" that represents the head data.
    writeToBFCache(now, varyPath, head, prefetchHead, null, null, dynamicStaleAt);
}
function updateBFCacheEntryStaleAt(varyPath, newStaleAt) {
    if (typeof window === 'undefined') {
        return;
    }
    const isRevalidation = false;
    // Read with staleness bypass (-1) so we can update even stale entries
    const entry = (0, _cachemap.getFromCacheMap)(-1, currentBfCacheVersion, bfcacheMap, varyPath, isRevalidation);
    if (entry !== null) {
        entry.staleAt = newStaleAt;
    }
}
function readFromBFCache(varyPath) {
    if (typeof window === 'undefined') {
        return null;
    }
    const isRevalidation = false;
    return (0, _cachemap.getFromCacheMap)(// might be. Pass -1 instead of the actual current time to bypass
    // staleness checks.
    -1, currentBfCacheVersion, bfcacheMap, varyPath, isRevalidation);
}
function readFromBFCacheDuringRegularNavigation(now, varyPath) {
    if (typeof window === 'undefined') {
        return null;
    }
    const isRevalidation = false;
    return (0, _cachemap.getFromCacheMap)(now, currentBfCacheVersion, bfcacheMap, varyPath, isRevalidation);
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/optimistic-routes.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

/**
 * Optimistic Routing (Known Routes)
 *
 * This module enables the client to predict route structure for URLs that
 * haven't been prefetched yet, based on previously learned route patterns.
 * When successful, this allows skipping the route tree prefetch request
 * entirely.
 *
 * The core idea is that many URLs map to the same route structure. For example,
 * /blog/post-1 and /blog/post-2 both resolve to /blog/[slug]. Once we've
 * prefetched one, we can predict the structure of the other.
 *
 * However, we can't always make this prediction. Static siblings (like
 * /blog/featured alongside /blog/[slug]) have different route structures.
 * When we learn a dynamic route, we also learn its static siblings so we
 * know when NOT to apply the prediction.
 *
 * Main entry points:
 *
 * 1. discoverKnownRoute: Called after receiving a route tree from the server.
 *    Traverses the route tree, compares URL parts to segments, and populates
 *    the known route tree if they match. Routes are always inserted into the
 *    cache.
 *
 * 2. matchKnownRoute: Called when looking up a route with no cache entry.
 *    Matches the candidate URL against learned patterns. Returns a synthetic
 *    cache entry if successful, or null to fall back to server resolution.
 *
 * Rewrite detection happens during traversal: if a URL path part doesn't match
 * the corresponding route segment, we stop populating the known route tree
 * (since the mapping is incorrect) but still insert the route into the cache.
 *
 * The known route tree is append-only with no eviction. Route patterns are
 * derived from the filesystem, so they don't become stale within a session.
 * Cache invalidation on deploy clears everything anyway.
 *
 * Current limitations (deopt to server resolution):
 * - Rewrites: Detected during traversal (tree not populated, but route cached)
 * - Intercepted routes: The route tree varies by referrer (Next-Url header),
 *   so we can't predict the correct structure from the URL alone. Patterns are
 *   still stored during discovery (so the trie stays populated for non-
 *   intercepted siblings), but matching bails out when the pattern is marked
 *   as interceptable.
 */ Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    discoverKnownRoute: null,
    matchKnownRoute: null,
    resetKnownRoutes: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    discoverKnownRoute: function() {
        return discoverKnownRoute;
    },
    matchKnownRoute: function() {
        return matchKnownRoute;
    },
    resetKnownRoutes: function() {
        return resetKnownRoutes;
    }
});
const _cache = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache.js [app-client] (ecmascript)");
const _routeparams = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/route-params.js [app-client] (ecmascript)");
const _varypath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/vary-path.js [app-client] (ecmascript)");
function createEmptyPart() {
    return {
        staticChildren: null,
        dynamicChild: null,
        dynamicChildParamName: null,
        dynamicChildParamType: null,
        pattern: null
    };
}
// The root of the known route tree.
let knownRouteTreeRoot = createEmptyPart();
function discoverKnownRoute(now, pathname, nextUrl, pendingEntry, routeTree, metadataVaryPath, couldBeIntercepted, canonicalUrl, supportsPerSegmentPrefetching, hasDynamicRewrite) {
    const tree = routeTree;
    const pathnameParts = pathname.split('/').filter((p)=>p !== '');
    const firstPart = pathnameParts.length > 0 ? pathnameParts[0] : null;
    const remainingParts = pathnameParts.length > 0 ? pathnameParts.slice(1) : [];
    if (pendingEntry !== null) {
        // Fulfill the pending entry first
        const fulfilledEntry = (0, _cache.fulfillRouteCacheEntry)(now, pendingEntry, tree, metadataVaryPath, couldBeIntercepted, canonicalUrl, supportsPerSegmentPrefetching);
        if (hasDynamicRewrite) {
            fulfilledEntry.hasDynamicRewrite = true;
        }
        // Populate the known route tree (handles rewrite detection internally).
        // The entry is already in the cache; this just stores it as a pattern
        // if the URL matches the route structure.
        discoverKnownRoutePart(knownRouteTreeRoot, tree, firstPart, remainingParts, fulfilledEntry, now, pathname, nextUrl, tree, metadataVaryPath, couldBeIntercepted, canonicalUrl, supportsPerSegmentPrefetching, hasDynamicRewrite);
        return fulfilledEntry;
    }
    // No pending entry - discoverKnownRoutePart will create one and insert it
    // into the cache, or return an existing pattern if one exists.
    return discoverKnownRoutePart(knownRouteTreeRoot, tree, firstPart, remainingParts, null, now, pathname, nextUrl, tree, metadataVaryPath, couldBeIntercepted, canonicalUrl, supportsPerSegmentPrefetching, hasDynamicRewrite);
}
/**
 * Gets or creates the dynamic child node for a KnownRoutePart.
 * A node can have at most one dynamic child (you can't have both [slug] and
 * [id] at the same route level), so we either return existing or create new.
 */ function discoverDynamicChild(part, paramName, paramType) {
    if (part.dynamicChild !== null) {
        return part.dynamicChild;
    }
    const newChild = createEmptyPart();
    // Type assertion needed because we're converting from "without" to "with"
    // dynamic child variant.
    const mutablePart = part;
    mutablePart.dynamicChild = newChild;
    mutablePart.dynamicChildParamName = paramName;
    mutablePart.dynamicChildParamType = paramType;
    return newChild;
}
/**
 * Recursive workhorse for discoverKnownRoute.
 *
 * Walks the route tree and URL parts in parallel, building out the known
 * route tree as it goes. At each step:
 * 1. Determines if the current segment appears in the URL (dynamic/static)
 * 2. Validates URL matches route structure (detects rewrites)
 * 3. Creates/updates the corresponding KnownRoutePart node
 * 4. Records static siblings for future matching
 * 5. Recurses into child slots (parallel routes)
 *
 * If a URL/route mismatch is detected (rewrite), we stop building the known
 * route tree but still cache the route entry for direct lookup.
 */ function discoverKnownRoutePart(parentKnownRoutePart, routeTree, urlPart, remainingParts, existingEntry, now, pathname, nextUrl, fullTree, metadataVaryPath, couldBeIntercepted, canonicalUrl, supportsPerSegmentPrefetching, hasDynamicRewrite) {
    const segment = routeTree.segment;
    let segmentAppearsInURL;
    let paramName = null;
    let paramType = null;
    let staticSiblings = null;
    if (typeof segment === 'string') {
        segmentAppearsInURL = (0, _routeparams.doesStaticSegmentAppearInURL)(segment);
    } else {
        // Dynamic segment tuple: [paramName, paramCacheKey, paramType, staticSiblings]
        paramName = segment[0];
        paramType = segment[2];
        staticSiblings = segment[3];
        segmentAppearsInURL = true;
    }
    let knownRoutePart = parentKnownRoutePart;
    let nextUrlPart = urlPart;
    let nextRemainingParts = remainingParts;
    if (segmentAppearsInURL) {
        // Check for mismatch: if this is a static segment, the URL part must match
        if (paramName === null && urlPart !== segment) {
            // URL doesn't match route structure (likely a rewrite).
            // Don't populate the known route tree, just write the route into the
            // cache and return immediately.
            if (existingEntry !== null) {
                return existingEntry;
            }
            return (0, _cache.writeRouteIntoCache)(now, pathname, nextUrl, fullTree, metadataVaryPath, couldBeIntercepted, canonicalUrl, supportsPerSegmentPrefetching);
        }
        // URL matches route structure. Build the known route tree.
        if (paramName !== null && paramType !== null) {
            // Dynamic segment
            knownRoutePart = discoverDynamicChild(parentKnownRoutePart, paramName, paramType);
            // Record static siblings as placeholder parts.
            // IMPORTANT: We use the null vs Map distinction to track whether
            // siblings are known at this level:
            // - staticChildren: null = siblings unknown (can't safely match dynamic)
            // - staticChildren: Map = siblings known (even if empty)
            // This matters in dev mode where webpack may not know all siblings yet.
            if (staticSiblings !== null) {
                // Siblings are known - ensure we have a Map (even if empty)
                if (parentKnownRoutePart.staticChildren === null) {
                    parentKnownRoutePart.staticChildren = new Map();
                }
                for (const sibling of staticSiblings){
                    if (!parentKnownRoutePart.staticChildren.has(sibling)) {
                        parentKnownRoutePart.staticChildren.set(sibling, createEmptyPart());
                    }
                }
            }
        } else {
            // Static segment
            if (parentKnownRoutePart.staticChildren === null) {
                parentKnownRoutePart.staticChildren = new Map();
            }
            let existingChild = parentKnownRoutePart.staticChildren.get(urlPart);
            if (existingChild === undefined) {
                existingChild = createEmptyPart();
                parentKnownRoutePart.staticChildren.set(urlPart, existingChild);
            }
            knownRoutePart = existingChild;
        }
        // Advance to next URL part
        nextUrlPart = remainingParts.length > 0 ? remainingParts[0] : null;
        nextRemainingParts = remainingParts.length > 0 ? remainingParts.slice(1) : [];
    }
    // else: Transparent segment (route group, __PAGE__, etc.)
    // Stay at the same known route part, don't advance URL parts
    // Recurse into child routes. A route tree can have multiple parallel routes
    // (e.g., @modal alongside children). Each parallel route is a separate
    // branch, but they all share the same URL - we just need to traverse all
    // branches to build out the known route tree.
    const slots = routeTree.slots;
    let resultFromChildren = null;
    if (slots !== null) {
        for(const parallelRouteKey in slots){
            const childRouteTree = slots[parallelRouteKey];
            // Skip branches with refreshState set - these were reused from a
            // different route (e.g., a "default" parallel slot) and don't represent
            // the actual route structure for this URL.
            if (childRouteTree.refreshState !== null) {
                continue;
            }
            const result = discoverKnownRoutePart(knownRoutePart, childRouteTree, nextUrlPart, nextRemainingParts, existingEntry, now, pathname, nextUrl, fullTree, metadataVaryPath, couldBeIntercepted, canonicalUrl, supportsPerSegmentPrefetching, hasDynamicRewrite);
            // All parallel route branches share the same URL, so they should all
            // reach compatible leaf nodes. We capture any result.
            resultFromChildren = result;
        }
        if (resultFromChildren !== null) {
            return resultFromChildren;
        }
        // Defensive fallback: no children returned a result. This shouldn't happen
        // for valid route trees, but handle it gracefully.
        if (existingEntry !== null) {
            return existingEntry;
        }
        return (0, _cache.writeRouteIntoCache)(now, pathname, nextUrl, fullTree, metadataVaryPath, couldBeIntercepted, canonicalUrl, supportsPerSegmentPrefetching);
    }
    // Reached a page node. Create/get the route cache entry and store as a
    // pattern. First, check if there's already a pattern for this route.
    if (knownRoutePart.pattern !== null) {
        // If this route has a dynamic rewrite, mark the existing pattern.
        if (hasDynamicRewrite) {
            knownRoutePart.pattern.hasDynamicRewrite = true;
        }
        return knownRoutePart.pattern;
    }
    // Get or create the entry
    let entry;
    if (existingEntry !== null) {
        // Already have a fulfilled entry, use it directly. It's already in the
        // route cache map.
        entry = existingEntry;
    } else {
        // Create the entry and insert it into the route cache map.
        entry = (0, _cache.writeRouteIntoCache)(now, pathname, nextUrl, fullTree, metadataVaryPath, couldBeIntercepted, canonicalUrl, supportsPerSegmentPrefetching);
    }
    if (hasDynamicRewrite) {
        entry.hasDynamicRewrite = true;
    }
    // Store as pattern
    knownRoutePart.pattern = entry;
    return entry;
}
function matchKnownRoute(pathname, search) {
    const pathnameParts = pathname.split('/').filter((p)=>p !== '');
    const resolvedParams = new Map();
    const match = matchKnownRoutePart(knownRouteTreeRoot, pathnameParts, 0, resolvedParams);
    if (match === null) {
        return null;
    }
    const matchedPart = match.part;
    const pattern = match.pattern;
    // If the pattern could be intercepted, we can't safely use it for prediction.
    // Interception routes resolve to different route trees depending on the
    // referrer (the Next-Url header), which means the same URL can map to
    // different page components depending on where the navigation originated.
    // Since the known route tree only stores a single pattern per URL shape, we
    // can't distinguish between the intercepted and non-intercepted cases, so we
    // bail out to server resolution.
    //
    // TODO: We could store interception behavior in the known route tree itself
    // (e.g., which segments use interception markers and what they resolve to).
    // With enough information embedded in the trie, we could match interception
    // routes entirely on the client without a server round-trip.
    if (pattern.couldBeIntercepted) {
        return null;
    }
    // "Reify" the pattern: clone the template tree with concrete param values.
    // This substitutes resolved params (e.g., slug: "hello") into dynamic
    // segments and recomputes vary paths for correct segment cache keying.
    const acc = {
        metadataVaryPath: null
    };
    const reifiedTree = reifyRouteTree(pattern.tree, resolvedParams, search, null, acc);
    // The metadata tree is a flat page node without the intermediate layout
    // structure. Clone it with the updated metadata vary path collected during
    // the main tree traversal.
    const metadataVaryPath = acc.metadataVaryPath;
    if (metadataVaryPath === null) {
        // This shouldn't be reachable for a valid route tree.
        return null;
    }
    const reifiedMetadata = (0, _cache.createMetadataRouteTree)(metadataVaryPath);
    // Create a synthetic (predicted) entry and store it as the new pattern.
    //
    // Why replace the pattern? We intentionally update the pattern with this
    // synthetic entry so that if our prediction was wrong (server returns a
    // different pathname due to dynamic rewrite), the entry gets marked with
    // hasDynamicRewrite. Future predictions for this route will see the flag
    // and bail out to server resolution instead of making the same mistake.
    const syntheticEntry = {
        canonicalUrl: pathname + search,
        status: _cache.EntryStatus.Fulfilled,
        blockedTasks: null,
        tree: reifiedTree,
        metadata: reifiedMetadata,
        couldBeIntercepted: pattern.couldBeIntercepted,
        supportsPerSegmentPrefetching: pattern.supportsPerSegmentPrefetching,
        hasDynamicRewrite: false,
        renderedSearch: search,
        ref: null,
        size: pattern.size,
        staleAt: pattern.staleAt,
        version: pattern.version
    };
    matchedPart.pattern = syntheticEntry;
    return syntheticEntry;
}
/**
 * Recursively matches a URL against the known route tree.
 *
 * Matching priority (most specific first):
 * 1. Static children - exact path segment match
 * 2. Dynamic child - [param], [...param], [[...param]]
 * 3. Direct pattern - when no more URL parts remain
 *
 * Collects resolved param values in resolvedParams as it traverses.
 * Returns null if no match found (caller should fall back to server).
 */ function matchKnownRoutePart(part, pathnameParts, partIndex, resolvedParams) {
    const urlPart = partIndex < pathnameParts.length ? pathnameParts[partIndex] : null;
    // If staticChildren is null, we don't know what static routes exist at this
    // level. This happens in webpack dev mode where routes are compiled
    // on-demand. We can't safely match a dynamicChild because the URL part might
    // be a static sibling we haven't discovered yet. Example: We know
    // /blog/[slug] exists, but haven't compiled /blog/featured. A request for
    // /blog/featured would incorrectly match /blog/[slug].
    if (part.staticChildren === null) {
        // The only safe match is a direct pattern when no URL parts remain.
        if (urlPart === null) {
            const pattern = part.pattern;
            if (pattern !== null && !pattern.hasDynamicRewrite) {
                return {
                    part,
                    pattern
                };
            }
        }
        return null;
    }
    // Static children take priority over dynamic. This ensures /blog/featured
    // matches its own route rather than /blog/[slug].
    if (urlPart !== null) {
        const staticChild = part.staticChildren.get(urlPart);
        if (staticChild !== undefined) {
            // Check if this is an "unknown" placeholder part. These are created when
            // we learn about static siblings (from the route tree's staticSiblings
            // field) but haven't prefetched them yet. We know the path exists but
            // don't know its structure, so we can't predict it.
            if (staticChild.pattern === null && staticChild.dynamicChild === null && staticChild.staticChildren === null) {
                // Bail out - server must resolve this route.
                return null;
            }
            const match = matchKnownRoutePart(staticChild, pathnameParts, partIndex + 1, resolvedParams);
            if (match !== null) {
                return match;
            }
            // Static child is a real node (not a placeholder) but its subtree
            // didn't match the remaining URL parts. This means the route exists
            // in the static subtree but hasn't been fully discovered yet. Do not
            // fall through to try the dynamic child — the static match is
            // authoritative. Bail out to server resolution.
            return null;
        }
    }
    // Try dynamic child
    if (part.dynamicChild !== null) {
        const dynamicPart = part.dynamicChild;
        const paramName = part.dynamicChildParamName;
        const paramType = part.dynamicChildParamType;
        const dynamicPattern = dynamicPart.pattern;
        switch(paramType){
            case 'c':
                // Required catch-all [...param]: consumes 1+ URL parts
                if (dynamicPattern !== null && !dynamicPattern.hasDynamicRewrite && urlPart !== null) {
                    resolvedParams.set(paramName, pathnameParts.slice(partIndex));
                    return {
                        part: dynamicPart,
                        pattern: dynamicPattern
                    };
                }
                break;
            case 'oc':
                // Optional catch-all [[...param]]: consumes 0+ URL parts
                if (dynamicPattern !== null && !dynamicPattern.hasDynamicRewrite) {
                    if (urlPart !== null) {
                        resolvedParams.set(paramName, pathnameParts.slice(partIndex));
                        return {
                            part: dynamicPart,
                            pattern: dynamicPattern
                        };
                    }
                    // urlPart is null - can match with zero parts, but a direct pattern
                    // (e.g., page.tsx alongside [[...param]]) takes precedence.
                    if (part.pattern === null || part.pattern.hasDynamicRewrite) {
                        resolvedParams.set(paramName, []);
                        return {
                            part: dynamicPart,
                            pattern: dynamicPattern
                        };
                    }
                }
                break;
            case 'd':
                // Regular dynamic [param]: consumes exactly 1 URL part.
                // Unlike catch-all which terminates here, regular dynamic must
                // continue recursing to find the leaf pattern.
                if (urlPart !== null) {
                    resolvedParams.set(paramName, urlPart);
                    return matchKnownRoutePart(dynamicPart, pathnameParts, partIndex + 1, resolvedParams);
                }
                break;
            // Intercepted routes use relative path markers like (.), (..), (...)
            // Their behavior depends on navigation context (soft vs hard nav),
            // so we can't predict them client-side. Defer to server.
            case 'ci(..)(..)':
            case 'ci(.)':
            case 'ci(..)':
            case 'ci(...)':
            case 'di(..)(..)':
            case 'di(.)':
            case 'di(..)':
            case 'di(...)':
                return null;
            default:
                paramType;
        }
    }
    // No children matched. If we've consumed all URL parts, check for a direct
    // pattern at this node (the route terminates here).
    if (urlPart === null) {
        const pattern = part.pattern;
        if (pattern !== null && !pattern.hasDynamicRewrite) {
            return {
                part,
                pattern
            };
        }
    }
    return null;
}
/**
 * "Reify" means to make concrete - we take an abstract pattern (the template
 * route tree) and produce a concrete instance with actual param values.
 *
 * This function clones a RouteTree, substituting dynamic segment values from
 * resolvedParams and computing new vary paths. The vary path encodes param
 * values so segment cache entries can be correctly keyed.
 *
 * Example: Pattern for /blog/[slug] with resolvedParams { slug: "hello" }
 * produces a tree where segment [slug] has cacheKey "hello".
 */ function reifyRouteTree(pattern, resolvedParams, search, parentPartialVaryPath, acc) {
    const originalSegment = pattern.segment;
    let newSegment = originalSegment;
    let partialVaryPath;
    if (typeof originalSegment !== 'string') {
        // Dynamic segment: compute new cache key and append to partial vary path
        const paramName = originalSegment[0];
        const paramType = originalSegment[2];
        const staticSiblings = originalSegment[3];
        const newValue = resolvedParams.get(paramName);
        if (newValue !== undefined) {
            const newCacheKey = Array.isArray(newValue) ? newValue.join('/') : newValue;
            newSegment = [
                paramName,
                newCacheKey,
                paramType,
                staticSiblings
            ];
            partialVaryPath = (0, _varypath.appendLayoutVaryPath)(parentPartialVaryPath, newCacheKey, paramName);
        } else {
            // Param not found in resolvedParams - keep original and inherit partial
            // TODO: This should never happen. Bail out with null.
            partialVaryPath = parentPartialVaryPath;
        }
    } else {
        // Static segment: inherit partial vary path from parent
        partialVaryPath = parentPartialVaryPath;
    }
    // Recurse into children with the (possibly updated) partial vary path
    let newSlots = null;
    if (pattern.slots !== null) {
        newSlots = {};
        for(const key in pattern.slots){
            newSlots[key] = reifyRouteTree(pattern.slots[key], resolvedParams, search, partialVaryPath, acc);
        }
    }
    if (pattern.isPage) {
        // Page segment: finalize with search params
        const newVaryPath = (0, _varypath.finalizePageVaryPath)(pattern.requestKey, search, partialVaryPath);
        // Collect metadata vary path (first page wins, same as original algorithm)
        if (acc.metadataVaryPath === null) {
            acc.metadataVaryPath = (0, _varypath.finalizeMetadataVaryPath)(pattern.requestKey, search, partialVaryPath);
        }
        return {
            requestKey: pattern.requestKey,
            segment: newSegment,
            refreshState: pattern.refreshState,
            slots: newSlots,
            prefetchHints: pattern.prefetchHints,
            isPage: true,
            varyPath: newVaryPath
        };
    } else {
        // Layout segment: finalize without search params
        const newVaryPath = (0, _varypath.finalizeLayoutVaryPath)(pattern.requestKey, partialVaryPath);
        return {
            requestKey: pattern.requestKey,
            segment: newSegment,
            refreshState: pattern.refreshState,
            slots: newSlots,
            prefetchHints: pattern.prefetchHints,
            isPage: false,
            varyPath: newVaryPath
        };
    }
}
function resetKnownRoutes() {
    knownRouteTreeRoot = createEmptyPart();
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    EntryStatus: null,
    attemptToFulfillDynamicSegmentFromBFCache: null,
    attemptToUpgradeSegmentFromBFCache: null,
    canNewFetchStrategyProvideMoreContent: null,
    convertReusedFlightRouterStateToRouteTree: null,
    convertRootFlightRouterStateToRouteTree: null,
    convertRouteTreeToFlightRouterState: null,
    createDetachedSegmentCacheEntry: null,
    createMetadataRouteTree: null,
    deprecated_requestOptimisticRouteCacheEntry: null,
    fetchInlinedSegmentsOnCacheMiss: null,
    fetchRouteOnCacheMiss: null,
    fetchSegmentOnCacheMiss: null,
    fetchSegmentPrefetchesUsingDynamicRequest: null,
    fulfillRouteCacheEntry: null,
    getCurrentRouteCacheVersion: null,
    getCurrentSegmentCacheVersion: null,
    getStaleAt: null,
    getStaleTimeMs: null,
    invalidateEntirePrefetchCache: null,
    invalidateRouteCacheEntries: null,
    invalidateSegmentCacheEntries: null,
    markRouteEntryAsDynamicRewrite: null,
    overwriteRevalidatingSegmentCacheEntry: null,
    pingInvalidationListeners: null,
    processRuntimePrefetchStream: null,
    readOrCreateRevalidatingSegmentEntry: null,
    readOrCreateRouteCacheEntry: null,
    readOrCreateSegmentCacheEntry: null,
    readRouteCacheEntry: null,
    readSegmentCacheEntry: null,
    stripIsPartialByte: null,
    upgradeToPendingSegment: null,
    upsertSegmentEntry: null,
    waitForSegmentCacheEntry: null,
    writeDynamicRenderResponseIntoCache: null,
    writeRouteIntoCache: null,
    writeStaticStageResponseIntoCache: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    EntryStatus: function() {
        return EntryStatus;
    },
    attemptToFulfillDynamicSegmentFromBFCache: function() {
        return attemptToFulfillDynamicSegmentFromBFCache;
    },
    attemptToUpgradeSegmentFromBFCache: function() {
        return attemptToUpgradeSegmentFromBFCache;
    },
    canNewFetchStrategyProvideMoreContent: function() {
        return canNewFetchStrategyProvideMoreContent;
    },
    convertReusedFlightRouterStateToRouteTree: function() {
        return convertReusedFlightRouterStateToRouteTree;
    },
    convertRootFlightRouterStateToRouteTree: function() {
        return convertRootFlightRouterStateToRouteTree;
    },
    convertRouteTreeToFlightRouterState: function() {
        return convertRouteTreeToFlightRouterState;
    },
    createDetachedSegmentCacheEntry: function() {
        return createDetachedSegmentCacheEntry;
    },
    createMetadataRouteTree: function() {
        return createMetadataRouteTree;
    },
    deprecated_requestOptimisticRouteCacheEntry: function() {
        return deprecated_requestOptimisticRouteCacheEntry;
    },
    fetchInlinedSegmentsOnCacheMiss: function() {
        return fetchInlinedSegmentsOnCacheMiss;
    },
    fetchRouteOnCacheMiss: function() {
        return fetchRouteOnCacheMiss;
    },
    fetchSegmentOnCacheMiss: function() {
        return fetchSegmentOnCacheMiss;
    },
    fetchSegmentPrefetchesUsingDynamicRequest: function() {
        return fetchSegmentPrefetchesUsingDynamicRequest;
    },
    fulfillRouteCacheEntry: function() {
        return fulfillRouteCacheEntry;
    },
    getCurrentRouteCacheVersion: function() {
        return getCurrentRouteCacheVersion;
    },
    getCurrentSegmentCacheVersion: function() {
        return getCurrentSegmentCacheVersion;
    },
    getStaleAt: function() {
        return getStaleAt;
    },
    getStaleTimeMs: function() {
        return getStaleTimeMs;
    },
    invalidateEntirePrefetchCache: function() {
        return invalidateEntirePrefetchCache;
    },
    invalidateRouteCacheEntries: function() {
        return invalidateRouteCacheEntries;
    },
    invalidateSegmentCacheEntries: function() {
        return invalidateSegmentCacheEntries;
    },
    markRouteEntryAsDynamicRewrite: function() {
        return markRouteEntryAsDynamicRewrite;
    },
    overwriteRevalidatingSegmentCacheEntry: function() {
        return overwriteRevalidatingSegmentCacheEntry;
    },
    pingInvalidationListeners: function() {
        return pingInvalidationListeners;
    },
    processRuntimePrefetchStream: function() {
        return processRuntimePrefetchStream;
    },
    readOrCreateRevalidatingSegmentEntry: function() {
        return readOrCreateRevalidatingSegmentEntry;
    },
    readOrCreateRouteCacheEntry: function() {
        return readOrCreateRouteCacheEntry;
    },
    readOrCreateSegmentCacheEntry: function() {
        return readOrCreateSegmentCacheEntry;
    },
    readRouteCacheEntry: function() {
        return readRouteCacheEntry;
    },
    readSegmentCacheEntry: function() {
        return readSegmentCacheEntry;
    },
    stripIsPartialByte: function() {
        return stripIsPartialByte;
    },
    upgradeToPendingSegment: function() {
        return upgradeToPendingSegment;
    },
    upsertSegmentEntry: function() {
        return upsertSegmentEntry;
    },
    waitForSegmentCacheEntry: function() {
        return waitForSegmentCacheEntry;
    },
    writeDynamicRenderResponseIntoCache: function() {
        return writeDynamicRenderResponseIntoCache;
    },
    writeRouteIntoCache: function() {
        return writeRouteIntoCache;
    },
    writeStaticStageResponseIntoCache: function() {
        return writeStaticStageResponseIntoCache;
    }
});
const _varyparamsdecoding = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/segment-cache/vary-params-decoding.js [app-client] (ecmascript)");
const _approuterheaders = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-headers.js [app-client] (ecmascript)");
const _fetchserverresponse = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/fetch-server-response.js [app-client] (ecmascript)");
const _scheduler = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/scheduler.js [app-client] (ecmascript)");
const _varypath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/vary-path.js [app-client] (ecmascript)");
const _createhreffromurl = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/create-href-from-url.js [app-client] (ecmascript)");
const _cachekey = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache-key.js [app-client] (ecmascript)");
const _routeparams = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/route-params.js [app-client] (ecmascript)");
const _cachemap = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache-map.js [app-client] (ecmascript)");
const _segmentvalueencoding = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/segment-cache/segment-value-encoding.js [app-client] (ecmascript)");
const _flightdatahelpers = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/flight-data-helpers.js [app-client] (ecmascript)");
const _navigatereducer = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/navigate-reducer.js [app-client] (ecmascript)");
const _links = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/links.js [app-client] (ecmascript)");
const _segment = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/segment.js [app-client] (ecmascript)");
const _types = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/types.js [app-client] (ecmascript)");
const _promisewithresolvers = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/promise-with-resolvers.js [app-client] (ecmascript)");
const _bfcache = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/bfcache.js [app-client] (ecmascript)");
const _optimisticroutes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/optimistic-routes.js [app-client] (ecmascript)");
const _navigation = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/navigation.js [app-client] (ecmascript)");
const _navigationbuildid = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/navigation-build-id.js [app-client] (ecmascript)");
const _constants = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/constants.js [app-client] (ecmascript)");
function getStaleTimeMs(staleTimeSeconds) {
    return Math.max(staleTimeSeconds, 30) * 1000;
}
var EntryStatus = /*#__PURE__*/ function(EntryStatus) {
    EntryStatus[EntryStatus["Empty"] = 0] = "Empty";
    EntryStatus[EntryStatus["Pending"] = 1] = "Pending";
    EntryStatus[EntryStatus["Fulfilled"] = 2] = "Fulfilled";
    EntryStatus[EntryStatus["Rejected"] = 3] = "Rejected";
    return EntryStatus;
}({});
const isOutputExportMode = ("TURBOPACK compile-time value", "development") === 'production' && ("TURBOPACK compile-time value", void 0) === 'export';
const MetadataOnlyRequestTree = [
    '',
    {},
    null,
    'metadata-only'
];
let routeCacheMap = (0, _cachemap.createCacheMap)();
let segmentCacheMap = (0, _cachemap.createCacheMap)();
// All invalidation listeners for the whole cache are tracked in single set.
// Since we don't yet support tag or path-based invalidation, there's no point
// tracking them any more granularly than this. Once we add granular
// invalidation, that may change, though generally the model is to just notify
// the listeners and allow the caller to poll the prefetch cache with a new
// prefetch task if desired.
let invalidationListeners = null;
// Incrementing counters used to track cache invalidations. Route and segment
// caches have separate versions so they can be invalidated independently.
// Invalidation does not eagerly evict anything from the cache; entries are
// lazily evicted when read.
let currentRouteCacheVersion = 0;
let currentSegmentCacheVersion = 0;
function getCurrentRouteCacheVersion() {
    return currentRouteCacheVersion;
}
function getCurrentSegmentCacheVersion() {
    return currentSegmentCacheVersion;
}
function invalidateEntirePrefetchCache(nextUrl, tree) {
    currentRouteCacheVersion++;
    currentSegmentCacheVersion++;
    (0, _links.pingVisibleLinks)(nextUrl, tree);
    pingInvalidationListeners(nextUrl, tree);
}
function invalidateRouteCacheEntries(nextUrl, tree) {
    currentRouteCacheVersion++;
    (0, _links.pingVisibleLinks)(nextUrl, tree);
    pingInvalidationListeners(nextUrl, tree);
}
function invalidateSegmentCacheEntries(nextUrl, tree) {
    currentSegmentCacheVersion++;
    (0, _links.pingVisibleLinks)(nextUrl, tree);
    pingInvalidationListeners(nextUrl, tree);
}
function attachInvalidationListener(task) {
    // This function is called whenever a prefetch task reads a cache entry. If
    // the task has an onInvalidate function associated with it — i.e. the one
    // optionally passed to router.prefetch(onInvalidate) — then we attach that
    // listener to the every cache entry that the task reads. Then, if an entry
    // is invalidated, we call the function.
    if (task.onInvalidate !== null) {
        if (invalidationListeners === null) {
            invalidationListeners = new Set([
                task
            ]);
        } else {
            invalidationListeners.add(task);
        }
    }
}
function notifyInvalidationListener(task) {
    const onInvalidate = task.onInvalidate;
    if (onInvalidate !== null) {
        // Clear the callback from the task object to guarantee it's not called more
        // than once.
        task.onInvalidate = null;
        // This is a user-space function, so we must wrap in try/catch.
        try {
            onInvalidate();
        } catch (error) {
            if (typeof reportError === 'function') {
                reportError(error);
            } else {
                console.error(error);
            }
        }
    }
}
function pingInvalidationListeners(nextUrl, tree) {
    // The rough equivalent of pingVisibleLinks, but for onInvalidate callbacks.
    // This is called when the Next-Url or the base tree changes, since those
    // may affect the result of a prefetch task. It's also called after a
    // cache invalidation.
    if (invalidationListeners !== null) {
        const tasks = invalidationListeners;
        invalidationListeners = null;
        for (const task of tasks){
            if ((0, _scheduler.isPrefetchTaskDirty)(task, nextUrl, tree)) {
                notifyInvalidationListener(task);
            }
        }
    }
}
function readRouteCacheEntry(now, key) {
    const varyPath = (0, _varypath.getRouteVaryPath)(key.pathname, key.search, key.nextUrl);
    const isRevalidation = false;
    const existingEntry = (0, _cachemap.getFromCacheMap)(now, getCurrentRouteCacheVersion(), routeCacheMap, varyPath, isRevalidation);
    if (existingEntry !== null) {
        return existingEntry;
    }
    // No cache hit. Attempt to construct from template using the new
    // optimistic routing mechanism (pattern-based matching).
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    return null;
}
function readSegmentCacheEntry(now, varyPath) {
    const isRevalidation = false;
    return (0, _cachemap.getFromCacheMap)(now, getCurrentSegmentCacheVersion(), segmentCacheMap, varyPath, isRevalidation);
}
function readRevalidatingSegmentCacheEntry(now, varyPath) {
    const isRevalidation = true;
    return (0, _cachemap.getFromCacheMap)(now, getCurrentSegmentCacheVersion(), segmentCacheMap, varyPath, isRevalidation);
}
function waitForSegmentCacheEntry(pendingEntry) {
    // Because the entry is pending, there's already a in-progress request.
    // Attach a promise to the entry that will resolve when the server responds.
    let promiseWithResolvers = pendingEntry.promise;
    if (promiseWithResolvers === null) {
        promiseWithResolvers = pendingEntry.promise = (0, _promisewithresolvers.createPromiseWithResolvers)();
    } else {
    // There's already a promise we can use
    }
    return promiseWithResolvers.promise;
}
function createDetachedRouteCacheEntry() {
    return {
        canonicalUrl: null,
        status: 0,
        blockedTasks: null,
        tree: null,
        metadata: null,
        // This is initialized to true because we don't know yet whether the route
        // could be intercepted. It's only set to false once we receive a response
        // from the server.
        couldBeIntercepted: true,
        // Similarly, we don't yet know if the route supports PPR.
        supportsPerSegmentPrefetching: false,
        renderedSearch: null,
        // Map-related fields
        ref: null,
        size: 0,
        // Since this is an empty entry, there's no reason to ever evict it. It will
        // be updated when the data is populated.
        staleAt: Infinity,
        version: getCurrentRouteCacheVersion()
    };
}
function readOrCreateRouteCacheEntry(now, task, key) {
    attachInvalidationListener(task);
    const existingEntry = readRouteCacheEntry(now, key);
    if (existingEntry !== null) {
        return existingEntry;
    }
    // Create a pending entry and add it to the cache.
    const pendingEntry = createDetachedRouteCacheEntry();
    const varyPath = (0, _varypath.getRouteVaryPath)(key.pathname, key.search, key.nextUrl);
    const isRevalidation = false;
    (0, _cachemap.setInCacheMap)(routeCacheMap, varyPath, pendingEntry, isRevalidation);
    return pendingEntry;
}
function deprecated_requestOptimisticRouteCacheEntry(now, requestedUrl, nextUrl) {
    // This function is called during a navigation when there was no matching
    // route tree in the prefetch cache. Before de-opting to a blocking,
    // unprefetched navigation, we will first attempt to construct an "optimistic"
    // route tree by checking the cache for similar routes.
    //
    // Check if there's a route with the same pathname, but with different
    // search params. We can then base our optimistic route tree on this entry.
    //
    // Conceptually, we are simulating what would happen if we did perform a
    // prefetch the requested URL, under the assumption that the server will
    // not redirect or rewrite the request in a different manner than the
    // base route tree. This assumption might not hold, in which case we'll have
    // to recover when we perform the dynamic navigation request. However, this
    // is what would happen if a route were dynamically rewritten/redirected
    // in between the prefetch and the navigation. So the logic needs to exist
    // to handle this case regardless.
    // Look for a route with the same pathname, but with an empty search string.
    // TODO: There's nothing inherently special about the empty search string;
    // it's chosen somewhat arbitrarily, with the rationale that it's the most
    // likely one to exist. But we should update this to match _any_ search
    // string. The plan is to generalize this logic alongside other improvements
    // related to "fallback" cache entries.
    const requestedSearch = requestedUrl.search;
    if (requestedSearch === '') {
        // The caller would have already checked if a route with an empty search
        // string is in the cache. So we can bail out here.
        return null;
    }
    const urlWithoutSearchParams = new URL(requestedUrl);
    urlWithoutSearchParams.search = '';
    const routeWithNoSearchParams = readRouteCacheEntry(now, (0, _cachekey.createCacheKey)(urlWithoutSearchParams.href, nextUrl));
    if (routeWithNoSearchParams === null || routeWithNoSearchParams.status !== 2) {
        // Bail out of constructing an optimistic route tree. This will result in
        // a blocking, unprefetched navigation.
        return null;
    }
    // Now we have a base route tree we can "patch" with our optimistic values.
    // Optimistically assume that redirects for the requested pathname do
    // not vary on the search string. Therefore, if the base route was
    // redirected to a different search string, then the optimistic route
    // should be redirected to the same search string. Otherwise, we use
    // the requested search string.
    const canonicalUrlForRouteWithNoSearchParams = new URL(routeWithNoSearchParams.canonicalUrl, requestedUrl.origin);
    const optimisticCanonicalSearch = canonicalUrlForRouteWithNoSearchParams.search !== '' ? canonicalUrlForRouteWithNoSearchParams.search : requestedSearch;
    // Similarly, optimistically assume that rewrites for the requested
    // pathname do not vary on the search string. Therefore, if the base
    // route was rewritten to a different search string, then the optimistic
    // route should be rewritten to the same search string. Otherwise, we use
    // the requested search string.
    const optimisticRenderedSearch = routeWithNoSearchParams.renderedSearch !== '' ? routeWithNoSearchParams.renderedSearch : requestedSearch;
    const optimisticUrl = new URL(routeWithNoSearchParams.canonicalUrl, location.origin);
    optimisticUrl.search = optimisticCanonicalSearch;
    const optimisticCanonicalUrl = (0, _createhreffromurl.createHrefFromUrl)(optimisticUrl);
    const optimisticRouteTree = deprecated_createOptimisticRouteTree(routeWithNoSearchParams.tree, optimisticRenderedSearch);
    const optimisticMetadataTree = deprecated_createOptimisticRouteTree(routeWithNoSearchParams.metadata, optimisticRenderedSearch);
    // Clone the base route tree, and override the relevant fields with our
    // optimistic values.
    const optimisticEntry = {
        canonicalUrl: optimisticCanonicalUrl,
        status: 2,
        // This isn't cloned because it's instance-specific
        blockedTasks: null,
        tree: optimisticRouteTree,
        metadata: optimisticMetadataTree,
        couldBeIntercepted: routeWithNoSearchParams.couldBeIntercepted,
        supportsPerSegmentPrefetching: routeWithNoSearchParams.supportsPerSegmentPrefetching,
        hasDynamicRewrite: routeWithNoSearchParams.hasDynamicRewrite,
        // Override the rendered search with the optimistic value.
        renderedSearch: optimisticRenderedSearch,
        // Map-related fields
        ref: null,
        size: 0,
        staleAt: routeWithNoSearchParams.staleAt,
        version: routeWithNoSearchParams.version
    };
    // Do not insert this entry into the cache. It only exists so we can
    // perform the current navigation. Just return it to the caller.
    return optimisticEntry;
}
function deprecated_createOptimisticRouteTree(tree, newRenderedSearch) {
    // Create a new route tree that identical to the original one except for
    // the rendered search string, which is contained in the vary path.
    let clonedSlots = null;
    const originalSlots = tree.slots;
    if (originalSlots !== null) {
        clonedSlots = {};
        for(const parallelRouteKey in originalSlots){
            const childTree = originalSlots[parallelRouteKey];
            clonedSlots[parallelRouteKey] = deprecated_createOptimisticRouteTree(childTree, newRenderedSearch);
        }
    }
    // We only need to clone the vary path if the route is a page.
    if (tree.isPage) {
        return {
            requestKey: tree.requestKey,
            segment: tree.segment,
            refreshState: tree.refreshState,
            varyPath: (0, _varypath.clonePageVaryPathWithNewSearchParams)(tree.varyPath, newRenderedSearch),
            isPage: true,
            slots: clonedSlots,
            prefetchHints: tree.prefetchHints
        };
    }
    return {
        requestKey: tree.requestKey,
        segment: tree.segment,
        refreshState: tree.refreshState,
        varyPath: tree.varyPath,
        isPage: false,
        slots: clonedSlots,
        prefetchHints: tree.prefetchHints
    };
}
function readOrCreateSegmentCacheEntry(now, fetchStrategy, tree) {
    const existingEntry = readSegmentCacheEntry(now, tree.varyPath);
    if (existingEntry !== null) {
        return existingEntry;
    }
    // Create a pending entry and add it to the cache. The stale time is set to a
    // default value; the actual stale time will be set when the entry is
    // fulfilled with data from the server response.
    const varyPathForRequest = (0, _varypath.getSegmentVaryPathForRequest)(fetchStrategy, tree);
    const pendingEntry = createDetachedSegmentCacheEntry(now);
    const isRevalidation = false;
    (0, _cachemap.setInCacheMap)(segmentCacheMap, varyPathForRequest, pendingEntry, isRevalidation);
    return pendingEntry;
}
function readOrCreateRevalidatingSegmentEntry(now, fetchStrategy, tree) {
    // This function is called when we've already confirmed that a particular
    // segment is cached, but we want to perform another request anyway in case it
    // returns more complete and/or fresher data than we already have. The logic
    // for deciding whether to replace the existing entry is handled elsewhere;
    // this function just handles retrieving a cache entry that we can use to
    // track the revalidation.
    //
    // The reason revalidations are stored in the cache is because we need to be
    // able to dedupe multiple revalidation requests. The reason they have to be
    // handled specially is because we shouldn't overwrite a "normal" entry if
    // one exists at the same keypath. So, for each internal cache location, there
    // is a special "revalidation" slot that is used solely for this purpose.
    //
    // You can think of it as if all the revalidation entries were stored in a
    // separate cache map from the canonical entries, and then transfered to the
    // canonical cache map once the request is complete — this isn't how it's
    // actually implemented, since it's more efficient to store them in the same
    // data structure as the normal entries, but that's how it's modeled
    // conceptually.
    // TODO: Once we implement Fallback behavior for params, where an entry is
    // re-keyed based on response information, we'll need to account for the
    // possibility that the keypath of the previous entry is more generic than
    // the keypath of the revalidating entry. In other words, the server could
    // return a less generic entry upon revalidation. For now, though, this isn't
    // a concern because the keypath is based solely on the prefetch strategy,
    // not on data contained in the response.
    const existingEntry = readRevalidatingSegmentCacheEntry(now, tree.varyPath);
    if (existingEntry !== null) {
        return existingEntry;
    }
    // Create a pending entry and add it to the cache. The stale time is set to a
    // default value; the actual stale time will be set when the entry is
    // fulfilled with data from the server response.
    const varyPathForRequest = (0, _varypath.getSegmentVaryPathForRequest)(fetchStrategy, tree);
    const pendingEntry = createDetachedSegmentCacheEntry(now);
    const isRevalidation = true;
    (0, _cachemap.setInCacheMap)(segmentCacheMap, varyPathForRequest, pendingEntry, isRevalidation);
    return pendingEntry;
}
function overwriteRevalidatingSegmentCacheEntry(now, fetchStrategy, tree) {
    // This function is called when we've already decided to replace an existing
    // revalidation entry. Create a new entry and write it into the cache,
    // overwriting the previous value. The stale time is set to a default value;
    // the actual stale time will be set when the entry is fulfilled with data
    // from the server response.
    const varyPathForRequest = (0, _varypath.getSegmentVaryPathForRequest)(fetchStrategy, tree);
    const pendingEntry = createDetachedSegmentCacheEntry(now);
    const isRevalidation = true;
    (0, _cachemap.setInCacheMap)(segmentCacheMap, varyPathForRequest, pendingEntry, isRevalidation);
    return pendingEntry;
}
function upsertSegmentEntry(now, varyPath, candidateEntry) {
    // We have a new entry that has not yet been inserted into the cache. Before
    // we do so, we need to confirm whether it takes precedence over the existing
    // entry (if one exists).
    // TODO: We should not upsert an entry if its key was invalidated in the time
    // since the request was made. We can do that by passing the "owner" entry to
    // this function and confirming it's the same as `existingEntry`.
    if ((0, _cachemap.isValueExpired)(now, getCurrentSegmentCacheVersion(), candidateEntry)) {
        // The entry is expired. We cannot upsert it.
        return null;
    }
    const existingEntry = readSegmentCacheEntry(now, varyPath);
    if (existingEntry !== null) {
        // Don't replace a more specific segment with a less-specific one. A case where this
        // might happen is if the existing segment was fetched via
        // `<Link prefetch={true}>`.
        if (// than the segment we already have in the cache, so it can't have more content.
        candidateEntry.fetchStrategy !== existingEntry.fetchStrategy && !canNewFetchStrategyProvideMoreContent(existingEntry.fetchStrategy, candidateEntry.fetchStrategy) || // The existing entry isn't partial, but the new one is.
        // (TODO: can this be true if `candidateEntry.fetchStrategy >= existingEntry.fetchStrategy`?)
        !existingEntry.isPartial && candidateEntry.isPartial) {
            // We're going to leave revalidating entry in the cache so that it doesn't
            // get revalidated again unnecessarily. Downgrade the Fulfilled entry to
            // Rejected and null out the data so it can be garbage collected. We leave
            // `staleAt` intact to prevent subsequent revalidation attempts only until
            // the entry expires.
            const rejectedEntry = candidateEntry;
            rejectedEntry.status = 3;
            rejectedEntry.rsc = null;
            return null;
        }
        // Evict the existing entry from the cache.
        (0, _cachemap.deleteFromCacheMap)(existingEntry);
    }
    const isRevalidation = false;
    (0, _cachemap.setInCacheMap)(segmentCacheMap, varyPath, candidateEntry, isRevalidation);
    return candidateEntry;
}
function createDetachedSegmentCacheEntry(now) {
    // Default stale time for pending segment cache entries. The actual stale time
    // is set when the entry is fulfilled with data from the server response.
    const staleAt = now + 30 * 1000;
    const emptyEntry = {
        status: 0,
        // Default to assuming the fetch strategy will be PPR. This will be updated
        // when a fetch is actually initiated.
        fetchStrategy: _types.FetchStrategy.PPR,
        rsc: null,
        isPartial: true,
        promise: null,
        // Map-related fields
        ref: null,
        size: 0,
        staleAt,
        version: 0
    };
    return emptyEntry;
}
function upgradeToPendingSegment(emptyEntry, fetchStrategy) {
    const pendingEntry = emptyEntry;
    pendingEntry.status = 1;
    pendingEntry.fetchStrategy = fetchStrategy;
    if (fetchStrategy === _types.FetchStrategy.Full) {
        // We can assume the response will contain the full segment data. Set this
        // to false so we know it's OK to omit this segment from any navigation
        // requests that may happen while the data is still pending.
        pendingEntry.isPartial = false;
    }
    // Set the version here, since this is right before the request is initiated.
    // The next time the segment cache version is incremented, the entry will
    // effectively be evicted. This happens before initiating the request, rather
    // than when receiving the response, because it's guaranteed to happen
    // before the data is read on the server.
    pendingEntry.version = getCurrentSegmentCacheVersion();
    return pendingEntry;
}
function attemptToFulfillDynamicSegmentFromBFCache(now, segment, tree) {
    // Attempts to fulfill an empty segment cache entry using data from the
    // bfcache. This is only valid during a Full prefetch (i.e. one that includes
    // dynamic data), because the bfcache stores data from navigations which
    // always include dynamic data.
    // We always use the canonical vary path when checking the bfcache. This is
    // the same operation we'd use to access the cache during a
    // regular navigation.
    const varyPath = tree.varyPath;
    // Read from the BFCache without expiring it (pass -1). We check freshness
    // ourselves using navigatedAt, because the BFCache's staleAt may have been
    // overridden by a per-page unstable_dynamicStaleTime and can't be used to
    // derive the original request time.
    const bfcacheEntry = (0, _bfcache.readFromBFCache)(varyPath);
    if (bfcacheEntry !== null) {
        // The stale time for dynamic prefetches (default: 5 mins) is different
        // from the stale time for regular navigations (default: 0 secs). Use
        // navigatedAt to compute the correct expiry for prefetch purposes.
        const dynamicPrefetchStaleAt = bfcacheEntry.navigatedAt + _navigatereducer.STATIC_STALETIME_MS;
        if (now > dynamicPrefetchStaleAt) {
            return null;
        }
        const pendingSegment = upgradeToPendingSegment(segment, _types.FetchStrategy.Full);
        const isPartial = false;
        return fulfillSegmentCacheEntry(pendingSegment, bfcacheEntry.rsc, dynamicPrefetchStaleAt, isPartial);
    }
    return null;
}
function attemptToUpgradeSegmentFromBFCache(now, tree) {
    const varyPath = tree.varyPath;
    const bfcacheEntry = (0, _bfcache.readFromBFCache)(varyPath);
    if (bfcacheEntry !== null) {
        const dynamicPrefetchStaleAt = bfcacheEntry.navigatedAt + _navigatereducer.STATIC_STALETIME_MS;
        if (now > dynamicPrefetchStaleAt) {
            return null;
        }
        const pendingSegment = upgradeToPendingSegment(createDetachedSegmentCacheEntry(now), _types.FetchStrategy.Full);
        const isPartial = false;
        const newEntry = fulfillSegmentCacheEntry(pendingSegment, bfcacheEntry.rsc, dynamicPrefetchStaleAt, isPartial);
        const segmentVaryPath = (0, _varypath.getSegmentVaryPathForRequest)(_types.FetchStrategy.Full, tree);
        const upserted = upsertSegmentEntry(now, segmentVaryPath, newEntry);
        if (upserted !== null && upserted.status === 2) {
            return upserted;
        }
    }
    return null;
}
function pingBlockedTasks(entry) {
    const blockedTasks = entry.blockedTasks;
    if (blockedTasks !== null) {
        for (const task of blockedTasks){
            (0, _scheduler.pingPrefetchTask)(task);
        }
        entry.blockedTasks = null;
    }
}
function createMetadataRouteTree(metadataVaryPath) {
    // The Head is not actually part of the route tree, but other than that, it's
    // fetched and cached like a segment. Some functions expect a RouteTree
    // object, so rather than fork the logic in all those places, we use this
    // "fake" one.
    const metadata = {
        requestKey: _segmentvalueencoding.HEAD_REQUEST_KEY,
        segment: _segmentvalueencoding.HEAD_REQUEST_KEY,
        refreshState: null,
        varyPath: metadataVaryPath,
        // The metadata isn't really a "page" (though it isn't really a "segment"
        // either) but for the purposes of how this field is used, it behaves like
        // one. If this logic ever gets more complex we can change this to an enum.
        isPage: true,
        slots: null,
        prefetchHints: 0
    };
    return metadata;
}
function fulfillRouteCacheEntry(now, entry, tree, metadataVaryPath, couldBeIntercepted, canonicalUrl, supportsPerSegmentPrefetching) {
    // Get the rendered search from the vary path
    const renderedSearch = (0, _varypath.getRenderedSearchFromVaryPath)(metadataVaryPath) ?? '';
    const fulfilledEntry = entry;
    fulfilledEntry.status = 2;
    fulfilledEntry.tree = tree;
    fulfilledEntry.metadata = createMetadataRouteTree(metadataVaryPath);
    // Route structure is essentially static — it only changes on deploy.
    // Always use the static stale time.
    // NOTE: An exception is rewrites/redirects in middleware or proxy, which can
    // change routes dynamically. We have other strategies for handling those.
    fulfilledEntry.staleAt = now + _navigatereducer.STATIC_STALETIME_MS;
    fulfilledEntry.couldBeIntercepted = couldBeIntercepted;
    fulfilledEntry.canonicalUrl = canonicalUrl;
    fulfilledEntry.renderedSearch = renderedSearch;
    fulfilledEntry.supportsPerSegmentPrefetching = supportsPerSegmentPrefetching;
    fulfilledEntry.hasDynamicRewrite = false;
    pingBlockedTasks(entry);
    return fulfilledEntry;
}
function writeRouteIntoCache(now, pathname, nextUrl, tree, metadataVaryPath, couldBeIntercepted, canonicalUrl, supportsPerSegmentPrefetching) {
    const pendingEntry = createDetachedRouteCacheEntry();
    const fulfilledEntry = fulfillRouteCacheEntry(now, pendingEntry, tree, metadataVaryPath, couldBeIntercepted, canonicalUrl, supportsPerSegmentPrefetching);
    const renderedSearch = fulfilledEntry.renderedSearch;
    const varyPath = (0, _varypath.getFulfilledRouteVaryPath)(pathname, renderedSearch, nextUrl, couldBeIntercepted);
    const isRevalidation = false;
    (0, _cachemap.setInCacheMap)(routeCacheMap, varyPath, fulfilledEntry, isRevalidation);
    return fulfilledEntry;
}
function markRouteEntryAsDynamicRewrite(entry) {
    entry.hasDynamicRewrite = true;
// Note: The caller is responsible for also calling invalidateRouteCacheEntries
// to invalidate other entries that may have been derived from this template
// before we knew it had a dynamic rewrite.
}
function fulfillSegmentCacheEntry(segmentCacheEntry, rsc, staleAt, isPartial) {
    const fulfilledEntry = segmentCacheEntry;
    fulfilledEntry.status = 2;
    fulfilledEntry.rsc = rsc;
    fulfilledEntry.staleAt = staleAt;
    fulfilledEntry.isPartial = isPartial;
    // Resolve any listeners that were waiting for this data.
    if (segmentCacheEntry.promise !== null) {
        segmentCacheEntry.promise.resolve(fulfilledEntry);
        // Free the promise for garbage collection.
        fulfilledEntry.promise = null;
    }
    return fulfilledEntry;
}
function rejectRouteCacheEntry(entry, staleAt) {
    const rejectedEntry = entry;
    rejectedEntry.status = 3;
    rejectedEntry.staleAt = staleAt;
    pingBlockedTasks(entry);
}
function rejectSegmentCacheEntry(entry, staleAt) {
    const rejectedEntry = entry;
    rejectedEntry.status = 3;
    rejectedEntry.staleAt = staleAt;
    if (entry.promise !== null) {
        // NOTE: We don't currently propagate the reason the prefetch was canceled
        // but we could by accepting a `reason` argument.
        entry.promise.resolve(null);
        entry.promise = null;
    }
}
function convertRootTreePrefetchToRouteTree(rootTree, renderedPathname, renderedSearch, acc) {
    // Remove trailing and leading slashes
    const pathnameParts = renderedPathname.split('/').filter((p)=>p !== '');
    const index = 0;
    const rootSegment = _segmentvalueencoding.ROOT_SEGMENT_REQUEST_KEY;
    return convertTreePrefetchToRouteTree(rootTree.tree, rootSegment, null, _segmentvalueencoding.ROOT_SEGMENT_REQUEST_KEY, pathnameParts, index, renderedSearch, acc);
}
function convertTreePrefetchToRouteTree(prefetch, segment, partialVaryPath, requestKey, pathnameParts, pathnamePartsIndex, renderedSearch, acc) {
    // Converts the route tree sent by the server into the format used by the
    // cache. The cached version of the tree includes additional fields, such as a
    // cache key for each segment. Since this is frequently accessed, we compute
    // it once instead of on every access. This same cache key is also used to
    // request the segment from the server.
    let slots = null;
    let isPage;
    let varyPath;
    const prefetchSlots = prefetch.slots;
    if (prefetchSlots !== null) {
        isPage = false;
        varyPath = (0, _varypath.finalizeLayoutVaryPath)(requestKey, partialVaryPath);
        slots = {};
        for(let parallelRouteKey in prefetchSlots){
            const childPrefetch = prefetchSlots[parallelRouteKey];
            const childSegmentName = childPrefetch.name;
            const childParam = childPrefetch.param;
            let childDoesAppearInURL;
            let childSegment;
            let childPartialVaryPath;
            if (childParam !== null) {
                // This segment is parameterized. Get the param from the pathname.
                const childParamValue = (0, _routeparams.parseDynamicParamFromURLPart)(childParam.type, pathnameParts, pathnamePartsIndex);
                // Assign a cache key to the segment, based on the param value. In the
                // pre-Segment Cache implementation, the server computes this and sends
                // it in the body of the response. In the Segment Cache implementation,
                // the server sends an empty string and we fill it in here.
                // TODO: We're intentionally not adding the search param to page
                // segments here; it's tracked separately and added back during a read.
                // This would clearer if we waited to construct the segment until it's
                // read from the cache, since that's effectively what we're
                // doing anyway.
                const childParamKey = // cacheComponents is enabled.
                childParam.key !== null ? childParam.key : (0, _routeparams.getCacheKeyForDynamicParam)(childParamValue, '');
                childPartialVaryPath = (0, _varypath.appendLayoutVaryPath)(partialVaryPath, childParamKey, childSegmentName);
                childSegment = [
                    childSegmentName,
                    childParamKey,
                    childParam.type,
                    childParam.siblings
                ];
                childDoesAppearInURL = true;
            } else {
                // This segment does not have a param. Inherit the partial vary path of
                // the parent.
                childPartialVaryPath = partialVaryPath;
                childSegment = childSegmentName;
                childDoesAppearInURL = (0, _routeparams.doesStaticSegmentAppearInURL)(childSegmentName);
            }
            // Only increment the index if the segment appears in the URL. If it's a
            // "virtual" segment, like a route group, it remains the same.
            const childPathnamePartsIndex = childDoesAppearInURL ? pathnamePartsIndex + 1 : pathnamePartsIndex;
            const childRequestKeyPart = (0, _segmentvalueencoding.createSegmentRequestKeyPart)(childSegment);
            const childRequestKey = (0, _segmentvalueencoding.appendSegmentRequestKeyPart)(requestKey, parallelRouteKey, childRequestKeyPart);
            slots[parallelRouteKey] = convertTreePrefetchToRouteTree(childPrefetch, childSegment, childPartialVaryPath, childRequestKey, pathnameParts, childPathnamePartsIndex, renderedSearch, acc);
        }
    } else {
        if (requestKey.endsWith(_segment.PAGE_SEGMENT_KEY)) {
            // This is a page segment.
            isPage = true;
            varyPath = (0, _varypath.finalizePageVaryPath)(requestKey, renderedSearch, partialVaryPath);
            // The metadata "segment" is not part the route tree, but it has the same
            // conceptual params as a page segment. Write the vary path into the
            // accumulator object. If there are multiple parallel pages, we use the
            // first one. Which page we choose is arbitrary as long as it's
            // consistently the same one every time every time. See
            // finalizeMetadataVaryPath for more details.
            if (acc.metadataVaryPath === null) {
                acc.metadataVaryPath = (0, _varypath.finalizeMetadataVaryPath)(requestKey, renderedSearch, partialVaryPath);
            }
        } else {
            // This is a layout segment.
            isPage = false;
            varyPath = (0, _varypath.finalizeLayoutVaryPath)(requestKey, partialVaryPath);
        }
    }
    return {
        requestKey,
        segment,
        refreshState: null,
        // TODO: Cheating the type system here a bit because TypeScript can't tell
        // that the type of isPage and varyPath are consistent. The fix would be to
        // create separate constructors and call the appropriate one from each of
        // the branches above. Just seems a bit overkill only for one field so I'll
        // leave it as-is for now. If isPage were wrong it would break the behavior
        // and we'd catch it quickly, anyway.
        varyPath: varyPath,
        isPage: isPage,
        slots,
        prefetchHints: prefetch.prefetchHints
    };
}
function convertRootFlightRouterStateToRouteTree(flightRouterState, renderedSearch, acc) {
    return convertFlightRouterStateToRouteTree(flightRouterState, _segmentvalueencoding.ROOT_SEGMENT_REQUEST_KEY, null, renderedSearch, acc);
}
function convertReusedFlightRouterStateToRouteTree(parentRouteTree, parallelRouteKey, flightRouterState, renderedSearch, acc) {
    // Create a RouteTree for a FlightRouterState that was reused from an older
    // route. This happens during a navigation when a parallel route slot does not
    // match the target route; we reuse whatever slot was already active.
    // Unlike a FlightRouterState, the RouteTree type contains backreferences to
    // the parent segments. Append the vary path to the parent's vary path.
    const parentPartialVaryPath = parentRouteTree.isPage ? (0, _varypath.getPartialPageVaryPath)(parentRouteTree.varyPath) : (0, _varypath.getPartialLayoutVaryPath)(parentRouteTree.varyPath);
    const segment = flightRouterState[0];
    // And the request key.
    const parentRequestKey = parentRouteTree.requestKey;
    const requestKeyPart = (0, _segmentvalueencoding.createSegmentRequestKeyPart)(segment);
    const requestKey = (0, _segmentvalueencoding.appendSegmentRequestKeyPart)(parentRequestKey, parallelRouteKey, requestKeyPart);
    return convertFlightRouterStateToRouteTree(flightRouterState, requestKey, parentPartialVaryPath, renderedSearch, acc);
}
function convertFlightRouterStateToRouteTree(flightRouterState, requestKey, parentPartialVaryPath, parentRenderedSearch, acc) {
    const originalSegment = flightRouterState[0];
    // If the FlightRouterState has a refresh state, then this segment is part of
    // an inactive parallel route. It has a different rendered search query than
    // the outer parent route. In order to construct the inactive route correctly,
    // we must restore the query that was originally used to render it.
    const compressedRefreshState = flightRouterState[2] ?? null;
    const refreshState = compressedRefreshState !== null ? {
        canonicalUrl: compressedRefreshState[0],
        renderedSearch: compressedRefreshState[1]
    } : null;
    const renderedSearch = refreshState !== null ? refreshState.renderedSearch : parentRenderedSearch;
    let segment;
    let partialVaryPath;
    let isPage;
    let varyPath;
    if (Array.isArray(originalSegment)) {
        isPage = false;
        const paramCacheKey = originalSegment[1];
        const paramName = originalSegment[0];
        partialVaryPath = (0, _varypath.appendLayoutVaryPath)(parentPartialVaryPath, paramCacheKey, paramName);
        varyPath = (0, _varypath.finalizeLayoutVaryPath)(requestKey, partialVaryPath);
        segment = originalSegment;
    } else {
        // This segment does not have a param. Inherit the partial vary path of
        // the parent.
        partialVaryPath = parentPartialVaryPath;
        if (requestKey.endsWith(_segment.PAGE_SEGMENT_KEY)) {
            // This is a page segment.
            isPage = true;
            // The navigation implementation expects the search params to be included
            // in the segment. However, in the case of a static response, the search
            // params are omitted. So the client needs to add them back in when reading
            // from the Segment Cache.
            //
            // For consistency, we'll do this for dynamic responses, too.
            //
            // TODO: We should move search params out of FlightRouterState and handle
            // them entirely on the client, similar to our plan for dynamic params.
            segment = _segment.PAGE_SEGMENT_KEY;
            varyPath = (0, _varypath.finalizePageVaryPath)(requestKey, renderedSearch, partialVaryPath);
            // The metadata "segment" is not part the route tree, but it has the same
            // conceptual params as a page segment. Write the vary path into the
            // accumulator object. If there are multiple parallel pages, we use the
            // first one. Which page we choose is arbitrary as long as it's
            // consistently the same one every time every time. See
            // finalizeMetadataVaryPath for more details.
            if (acc.metadataVaryPath === null) {
                acc.metadataVaryPath = (0, _varypath.finalizeMetadataVaryPath)(requestKey, renderedSearch, partialVaryPath);
            }
        } else {
            // This is a layout segment.
            isPage = false;
            segment = originalSegment;
            varyPath = (0, _varypath.finalizeLayoutVaryPath)(requestKey, partialVaryPath);
        }
    }
    let slots = null;
    const parallelRoutes = flightRouterState[1];
    for(let parallelRouteKey in parallelRoutes){
        const childRouterState = parallelRoutes[parallelRouteKey];
        const childSegment = childRouterState[0];
        // TODO: Eventually, the param values will not be included in the response
        // from the server. We'll instead fill them in on the client by parsing
        // the URL. This is where we'll do that.
        const childRequestKeyPart = (0, _segmentvalueencoding.createSegmentRequestKeyPart)(childSegment);
        const childRequestKey = (0, _segmentvalueencoding.appendSegmentRequestKeyPart)(requestKey, parallelRouteKey, childRequestKeyPart);
        const childTree = convertFlightRouterStateToRouteTree(childRouterState, childRequestKey, partialVaryPath, renderedSearch, acc);
        if (slots === null) {
            slots = {
                [parallelRouteKey]: childTree
            };
        } else {
            slots[parallelRouteKey] = childTree;
        }
    }
    return {
        requestKey,
        segment,
        refreshState,
        // TODO: Cheating the type system here a bit because TypeScript can't tell
        // that the type of isPage and varyPath are consistent. The fix would be to
        // create separate constructors and call the appropriate one from each of
        // the branches above. Just seems a bit overkill only for one field so I'll
        // leave it as-is for now. If isPage were wrong it would break the behavior
        // and we'd catch it quickly, anyway.
        varyPath: varyPath,
        isPage: isPage,
        slots,
        prefetchHints: flightRouterState[4] ?? 0
    };
}
function convertRouteTreeToFlightRouterState(routeTree) {
    const parallelRoutes = {};
    if (routeTree.slots !== null) {
        for(const parallelRouteKey in routeTree.slots){
            parallelRoutes[parallelRouteKey] = convertRouteTreeToFlightRouterState(routeTree.slots[parallelRouteKey]);
        }
    }
    const flightRouterState = [
        routeTree.segment,
        parallelRoutes,
        null,
        null
    ];
    return flightRouterState;
}
async function fetchRouteOnCacheMiss(entry, key) {
    // This function is allowed to use async/await because it contains the actual
    // fetch that gets issued on a cache miss. Notice it writes the result to the
    // cache entry directly, rather than return data that is then written by
    // the caller.
    const pathname = key.pathname;
    const search = key.search;
    const nextUrl = key.nextUrl;
    const segmentPath = '/_tree';
    const headers = {
        [_approuterheaders.RSC_HEADER]: '1',
        [_approuterheaders.NEXT_ROUTER_PREFETCH_HEADER]: '1',
        [_approuterheaders.NEXT_ROUTER_SEGMENT_PREFETCH_HEADER]: segmentPath
    };
    if (nextUrl !== null) {
        headers[_approuterheaders.NEXT_URL] = nextUrl;
    }
    // Tell the server to perform a static pre-render for the Instant Navigation
    // Testing API. Static pre-renders don't normally happen during development.
    addInstantPrefetchHeaderIfLocked(headers);
    try {
        const url = new URL(pathname + search, location.origin);
        let response;
        let urlAfterRedirects;
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
        else {
            // "Server" mode. We can use request headers instead of the pathname.
            // TODO: The eventual plan is to get rid of our custom request headers and
            // encode everything into the URL, using a similar strategy to the
            // "output: export" block above.
            response = await fetchPrefetchResponse(url, headers);
            urlAfterRedirects = response !== null && response.redirected ? new URL(response.url) : url;
        }
        if (!response || !response.ok || // 204 is a Cache miss. Though theoretically this shouldn't happen when
        // PPR is enabled, because we always respond to route tree requests, even
        // if it needs to be blockingly generated on demand.
        response.status === 204 || !response.body) {
            // Server responded with an error, or with a miss. We should still cache
            // the response, but we can try again after 10 seconds.
            rejectRouteCacheEntry(entry, Date.now() + 10 * 1000);
            return null;
        }
        // TODO: The canonical URL is the href without the origin. I think
        // historically the reason for this is because the initial canonical URL
        // gets passed as a prop to the top-level React component, which means it
        // needs to be computed during SSR. If it were to include the origin, it
        // would need to always be same as location.origin on the client, to prevent
        // a hydration mismatch. To sidestep this complexity, we omit the origin.
        //
        // However, since this is neither a native URL object nor a fully qualified
        // URL string, we need to be careful about how we use it. To prevent subtle
        // mistakes, we should create a special type for it, instead of just string.
        // Or, we should just use a (readonly) URL object instead. The type of the
        // prop that we pass to seed the initial state does not need to be the same
        // type as the state itself.
        const canonicalUrl = (0, _createhreffromurl.createHrefFromUrl)(urlAfterRedirects);
        // Check whether the response varies based on the Next-Url header.
        const varyHeader = response.headers.get('vary');
        const couldBeIntercepted = varyHeader !== null && varyHeader.includes(_approuterheaders.NEXT_URL);
        // TODO: The `closed` promise was originally used to track when a streaming
        // network connection closes, so the scheduler could limit concurrent
        // connections. Now that prefetch responses are buffered, `closed` is
        // resolved immediately after buffering — before the outer function even
        // returns. This mechanism is only still meaningful for dynamic (Full)
        // prefetches, which use incremental streaming. Consider removing the
        // `closed` plumbing for buffered prefetch paths.
        const closed = (0, _promisewithresolvers.createPromiseWithResolvers)();
        // This checks whether the response was served from the per-segment cache,
        // rather than the old prefetching flow. If it fails, it implies that PPR
        // is disabled on this route.
        const routeIsPPREnabled = response.headers.get(_approuterheaders.NEXT_DID_POSTPONE_HEADER) === '2' || // In output: "export" mode, we can't rely on response headers. But if we
        // receive a well-formed response, we can assume it's a static response,
        // because all data is static in this mode.
        isOutputExportMode;
        if (routeIsPPREnabled) {
            const { stream: prefetchStream, size: responseSize } = await createNonTaskyPrefetchResponseStream(response.body);
            closed.resolve();
            (0, _cachemap.setSizeInCacheMap)(entry, responseSize);
            const serverData = await (0, _fetchserverresponse.createFromNextReadableStream)(prefetchStream, headers, {
                allowPartialStream: true
            });
            if ((response.headers.get(_constants.NEXT_NAV_DEPLOYMENT_ID_HEADER) ?? serverData.buildId) !== (0, _navigationbuildid.getNavigationBuildId)()) {
                // The server build does not match the client. Treat as a 404. During
                // an actual navigation, the router will trigger an MPA navigation.
                // TODO: We should cache the fact that this is an MPA navigation.
                rejectRouteCacheEntry(entry, Date.now() + 10 * 1000);
                return null;
            }
            // Get the params that were used to render the target page. These may
            // be different from the params in the request URL, if the page
            // was rewritten.
            const renderedPathname = (0, _routeparams.getRenderedPathname)(response);
            const renderedSearch = (0, _routeparams.getRenderedSearch)(response);
            // Convert the server-sent data into the RouteTree format used by the
            // client cache.
            //
            // During this traversal, we accumulate additional data into this
            // "accumulator" object.
            const acc = {
                metadataVaryPath: null
            };
            const routeTree = convertRootTreePrefetchToRouteTree(serverData, renderedPathname, renderedSearch, acc);
            const metadataVaryPath = acc.metadataVaryPath;
            if (metadataVaryPath === null) {
                rejectRouteCacheEntry(entry, Date.now() + 10 * 1000);
                return null;
            }
            (0, _optimisticroutes.discoverKnownRoute)(Date.now(), pathname, nextUrl, entry, routeTree, metadataVaryPath, couldBeIntercepted, canonicalUrl, routeIsPPREnabled, false // hasDynamicRewrite
            );
        } else {
            // PPR is not enabled for this route. The server responds with a
            // different format (FlightRouterState) that we need to convert.
            // TODO: We will unify the responses eventually. I'm keeping the types
            // separate for now because FlightRouterState has so many
            // overloaded concerns.
            const { stream: prefetchStream, size: responseSize } = await createNonTaskyPrefetchResponseStream(response.body);
            closed.resolve();
            (0, _cachemap.setSizeInCacheMap)(entry, responseSize);
            const serverData = await (0, _fetchserverresponse.createFromNextReadableStream)(prefetchStream, headers, {
                allowPartialStream: true
            });
            if ((response.headers.get(_constants.NEXT_NAV_DEPLOYMENT_ID_HEADER) ?? serverData.b) !== (0, _navigationbuildid.getNavigationBuildId)()) {
                // The server build does not match the client. Treat as a 404. During
                // an actual navigation, the router will trigger an MPA navigation.
                // TODO: We should cache the fact that this is an MPA navigation.
                rejectRouteCacheEntry(entry, Date.now() + 10 * 1000);
                return null;
            }
            // Read head vary params synchronously. Individual segments carry their
            // own thenables in CacheNodeSeedData.
            const headVaryParamsThenable = serverData.h;
            const headVaryParams = headVaryParamsThenable !== null ? (0, _varyparamsdecoding.readVaryParams)(headVaryParamsThenable) : null;
            writeDynamicTreeResponseIntoCache(Date.now(), // using the LoadingBoundary fetch strategy, so mark their cache entries accordingly.
            _types.FetchStrategy.LoadingBoundary, response, serverData, entry, couldBeIntercepted, canonicalUrl, routeIsPPREnabled, headVaryParams, pathname, nextUrl);
        }
        if (!couldBeIntercepted) {
            // This route will never be intercepted. So we can use this entry for all
            // requests to this route, regardless of the Next-Url header. This works
            // because when reading the cache we always check for a valid
            // non-intercepted entry first.
            // Re-key the entry. The `set` implementation handles removing it from
            // its previous position in the cache. We don't need to do anything to
            // update the LRU, because the entry is already in it.
            // TODO: Treat this as an upsert — should check if an entry already
            // exists at the new keypath, and if so, whether we should keep that
            // one instead.
            const fulfilledVaryPath = (0, _varypath.getFulfilledRouteVaryPath)(pathname, search, nextUrl, couldBeIntercepted);
            const isRevalidation = false;
            (0, _cachemap.setInCacheMap)(routeCacheMap, fulfilledVaryPath, entry, isRevalidation);
        }
        // Return a promise that resolves when the network connection closes, so
        // the scheduler can track the number of concurrent network connections.
        return {
            value: null,
            closed: closed.promise
        };
    } catch (error) {
        // Either the connection itself failed, or something bad happened while
        // decoding the response.
        rejectRouteCacheEntry(entry, Date.now() + 10 * 1000);
        return null;
    }
}
async function fetchSegmentOnCacheMiss(route, segmentCacheEntry, routeKey, tree) {
    // This function is allowed to use async/await because it contains the actual
    // fetch that gets issued on a cache miss. Notice it writes the result to the
    // cache entry directly, rather than return data that is then written by
    // the caller.
    //
    // Segment fetches are non-blocking so we don't need to ping the scheduler
    // on completion.
    // Use the canonical URL to request the segment, not the original URL. These
    // are usually the same, but the canonical URL will be different if the route
    // tree response was redirected. To avoid an extra waterfall on every segment
    // request, we pass the redirected URL instead of the original one.
    const url = new URL(route.canonicalUrl, location.origin);
    const nextUrl = routeKey.nextUrl;
    const requestKey = tree.requestKey;
    const normalizedRequestKey = requestKey === _segmentvalueencoding.ROOT_SEGMENT_REQUEST_KEY ? // `_index` instead of as an empty string. This should be treated as
    // an implementation detail and not as a stable part of the protocol.
    // It just needs to match the equivalent logic that happens when
    // prerendering the responses. It should not leak outside of Next.js.
    '/_index' : requestKey;
    const headers = {
        [_approuterheaders.RSC_HEADER]: '1',
        [_approuterheaders.NEXT_ROUTER_PREFETCH_HEADER]: '1',
        [_approuterheaders.NEXT_ROUTER_SEGMENT_PREFETCH_HEADER]: normalizedRequestKey
    };
    if (nextUrl !== null) {
        headers[_approuterheaders.NEXT_URL] = nextUrl;
    }
    // Tell the server to perform a static pre-render for the Instant Navigation
    // Testing API. Static pre-renders don't normally happen during development.
    addInstantPrefetchHeaderIfLocked(headers);
    const requestUrl = ("TURBOPACK compile-time falsy", 0) ? "TURBOPACK unreachable" : url;
    try {
        const response = await fetchPrefetchResponse(requestUrl, headers);
        if (!response || !response.ok || response.status === 204 || // Cache miss
        // This checks whether the response was served from the per-segment cache,
        // rather than the old prefetching flow. If it fails, it implies that PPR
        // is disabled on this route. Theoretically this should never happen
        // because we only issue requests for segments once we've verified that
        // the route supports PPR.
        response.headers.get(_approuterheaders.NEXT_DID_POSTPONE_HEADER) !== '2' && // In output: "export" mode, we can't rely on response headers. But if
        // we receive a well-formed response, we can assume it's a static
        // response, because all data is static in this mode.
        !isOutputExportMode || !response.body) {
            // Server responded with an error, or with a miss. We should still cache
            // the response, but we can try again after 10 seconds.
            rejectSegmentCacheEntry(segmentCacheEntry, Date.now() + 10 * 1000);
            return null;
        }
        // See TODO in fetchRouteOnCacheMiss about removing `closed` for
        // buffered prefetch paths.
        const closed = (0, _promisewithresolvers.createPromiseWithResolvers)();
        const { stream: prefetchStream, size: responseSize } = await createNonTaskyPrefetchResponseStream(response.body);
        closed.resolve();
        (0, _cachemap.setSizeInCacheMap)(segmentCacheEntry, responseSize);
        const serverData = await (0, _fetchserverresponse.createFromNextReadableStream)(prefetchStream, headers, {
            allowPartialStream: true
        });
        if ((response.headers.get(_constants.NEXT_NAV_DEPLOYMENT_ID_HEADER) ?? serverData.buildId) !== (0, _navigationbuildid.getNavigationBuildId)()) {
            // The server build does not match the client. Treat as a 404. During
            // an actual navigation, the router will trigger an MPA navigation.
            rejectSegmentCacheEntry(segmentCacheEntry, Date.now() + 10 * 1000);
            return null;
        }
        const now = Date.now();
        const staleAt = now + getStaleTimeMs(serverData.staleTime);
        const fulfilledEntry = fulfillSegmentCacheEntry(segmentCacheEntry, serverData.rsc, staleAt, serverData.isPartial);
        // If the server tells us which params the segment varies by, we can re-key
        // the entry to a more generic vary path. This allows the entry to be reused
        // across different param values for params that the segment doesn't
        // actually depend on.
        const varyParams = serverData.varyParams;
        const fulfilledVaryPath = ("TURBOPACK compile-time falsy", 0) ? "TURBOPACK unreachable" : (0, _varypath.getSegmentVaryPathForRequest)(segmentCacheEntry.fetchStrategy, tree);
        // Re-key and upsert the entry at the fulfilled vary path. This ensures
        // the entry is stored at the most generic path possible based on which
        // params the segment actually depends on.
        upsertSegmentEntry(now, fulfilledVaryPath, fulfilledEntry);
        return {
            value: fulfilledEntry,
            // Return a promise that resolves when the network connection closes, so
            // the scheduler can track the number of concurrent network connections.
            closed: closed.promise
        };
    } catch (error) {
        // Either the connection itself failed, or something bad happened while
        // decoding the response.
        rejectSegmentCacheEntry(segmentCacheEntry, Date.now() + 10 * 1000);
        return null;
    }
}
async function fetchInlinedSegmentsOnCacheMiss(route, routeKey, tree, spawnedEntries) {
    // When prefetch inlining is enabled, all segment data for a route is bundled
    // into a single /_inlined response instead of individual per-segment
    // requests. This function fetches that response and walks the tree to fill
    // all segment cache entries at once.
    const url = new URL(route.canonicalUrl, location.origin);
    const nextUrl = routeKey.nextUrl;
    const headers = {
        [_approuterheaders.RSC_HEADER]: '1',
        [_approuterheaders.NEXT_ROUTER_PREFETCH_HEADER]: '1',
        [_approuterheaders.NEXT_ROUTER_SEGMENT_PREFETCH_HEADER]: '/' + _segment.PAGE_SEGMENT_KEY
    };
    if (nextUrl !== null) {
        headers[_approuterheaders.NEXT_URL] = nextUrl;
    }
    addInstantPrefetchHeaderIfLocked(headers);
    try {
        const response = await fetchPrefetchResponse(url, headers);
        if (!response || !response.ok || response.status === 204 || response.headers.get(_approuterheaders.NEXT_DID_POSTPONE_HEADER) !== '2' && !isOutputExportMode || !response.body) {
            rejectSegmentEntriesIfStillPending(spawnedEntries, Date.now() + 10 * 1000);
            return null;
        }
        // See TODO in fetchRouteOnCacheMiss about removing `closed` for
        // buffered prefetch paths.
        const closed = (0, _promisewithresolvers.createPromiseWithResolvers)();
        const { stream: prefetchStream } = await createNonTaskyPrefetchResponseStream(response.body);
        closed.resolve();
        const serverData = await (0, _fetchserverresponse.createFromNextReadableStream)(prefetchStream, headers, {
            allowPartialStream: true
        });
        if ((response.headers.get(_constants.NEXT_NAV_DEPLOYMENT_ID_HEADER) ?? serverData.tree.segment.buildId) !== (0, _navigationbuildid.getNavigationBuildId)()) {
            rejectSegmentEntriesIfStillPending(spawnedEntries, Date.now() + 10 * 1000);
            return null;
        }
        const now = Date.now();
        // Walk the inlined tree in parallel with the RouteTree and fill
        // segment cache entries.
        fillInlinedSegmentEntries(now, route, tree, serverData.tree, spawnedEntries);
        // Fill the head entry.
        const headStaleAt = now + getStaleTimeMs(serverData.head.staleTime);
        const headKey = route.metadata.requestKey;
        const ownedHeadEntry = spawnedEntries.get(headKey);
        if (ownedHeadEntry !== undefined) {
            fulfillSegmentCacheEntry(ownedHeadEntry, serverData.head.rsc, headStaleAt, serverData.head.isPartial);
        } else {
            // The head was already cached. Try to upsert if the entry is empty.
            const existingEntry = readOrCreateSegmentCacheEntry(now, _types.FetchStrategy.PPR, route.metadata);
            if (existingEntry.status === 0) {
                fulfillSegmentCacheEntry(upgradeToPendingSegment(existingEntry, _types.FetchStrategy.PPR), serverData.head.rsc, headStaleAt, serverData.head.isPartial);
            }
        }
        // Reject any remaining entries that were not fulfilled by the response.
        rejectSegmentEntriesIfStillPending(spawnedEntries, Date.now() + 10 * 1000);
        return {
            value: null,
            closed: closed.promise
        };
    } catch (error) {
        rejectSegmentEntriesIfStillPending(spawnedEntries, Date.now() + 10 * 1000);
        return null;
    }
}
function fillInlinedSegmentEntries(now, route, tree, inlinedNode, spawnedEntries) {
    // Check if the spawned entries map has an entry for this segment's key.
    const segment = inlinedNode.segment;
    const staleAt = now + getStaleTimeMs(segment.staleTime);
    const ownedEntry = spawnedEntries.get(tree.requestKey);
    if (ownedEntry !== undefined) {
        // We own this entry. Fulfill it directly.
        fulfillSegmentCacheEntry(ownedEntry, segment.rsc, staleAt, segment.isPartial);
    } else {
        // Not owned by us — this is extra data from the inlined response for a
        // segment that was already cached. Try to upsert if the entry is empty.
        const existingEntry = readOrCreateSegmentCacheEntry(now, _types.FetchStrategy.PPR, tree);
        if (existingEntry.status === 0) {
            fulfillSegmentCacheEntry(upgradeToPendingSegment(existingEntry, _types.FetchStrategy.PPR), segment.rsc, staleAt, segment.isPartial);
        }
    }
    // Recurse into children.
    if (tree.slots !== null && inlinedNode.slots !== null) {
        for(const parallelRouteKey in tree.slots){
            const childTree = tree.slots[parallelRouteKey];
            const childInlinedNode = inlinedNode.slots[parallelRouteKey];
            if (childInlinedNode !== undefined) {
                fillInlinedSegmentEntries(now, route, childTree, childInlinedNode, spawnedEntries);
            }
        }
    }
}
async function fetchSegmentPrefetchesUsingDynamicRequest(task, route, fetchStrategy, dynamicRequestTree, spawnedEntries) {
    const key = task.key;
    const url = new URL(route.canonicalUrl, location.origin);
    const nextUrl = key.nextUrl;
    if (spawnedEntries.size === 1 && spawnedEntries.has(route.metadata.requestKey)) {
        // The only thing pending is the head. Instruct the server to
        // skip over everything else.
        dynamicRequestTree = MetadataOnlyRequestTree;
    }
    const headers = {
        [_approuterheaders.RSC_HEADER]: '1',
        [_approuterheaders.NEXT_ROUTER_STATE_TREE_HEADER]: (0, _flightdatahelpers.prepareFlightRouterStateForRequest)(dynamicRequestTree)
    };
    if (nextUrl !== null) {
        headers[_approuterheaders.NEXT_URL] = nextUrl;
    }
    switch(fetchStrategy){
        case _types.FetchStrategy.Full:
            {
                break;
            }
        case _types.FetchStrategy.PPRRuntime:
            {
                headers[_approuterheaders.NEXT_ROUTER_PREFETCH_HEADER] = '2';
                break;
            }
        case _types.FetchStrategy.LoadingBoundary:
            {
                headers[_approuterheaders.NEXT_ROUTER_PREFETCH_HEADER] = '1';
                break;
            }
        default:
            {
                fetchStrategy;
            }
    }
    try {
        const response = await fetchPrefetchResponse(url, headers);
        if (!response || !response.ok || !response.body) {
            // Server responded with an error, or with a miss. We should still cache
            // the response, but we can try again after 10 seconds.
            rejectSegmentEntriesIfStillPending(spawnedEntries, Date.now() + 10 * 1000);
            return null;
        }
        const renderedSearch = (0, _routeparams.getRenderedSearch)(response);
        if (renderedSearch !== route.renderedSearch) {
            // The search params that were used to render the target page are
            // different from the search params in the request URL. This only happens
            // when there's a dynamic rewrite in between the tree prefetch and the
            // data prefetch.
            // TODO: For now, since this is an edge case, we reject the prefetch, but
            // the proper way to handle this is to evict the stale route tree entry
            // then fill the cache with the new response.
            rejectSegmentEntriesIfStillPending(spawnedEntries, Date.now() + 10 * 1000);
            return null;
        }
        // Track when the network connection closes. Only meaningful for Full
        // (dynamic) prefetches which use incremental streaming. For buffered
        // paths, this is resolved immediately — see TODO in fetchRouteOnCacheMiss.
        const closed = (0, _promisewithresolvers.createPromiseWithResolvers)();
        let fulfilledEntries = null;
        let prefetchStream;
        let bufferedResponseSize = null;
        if (fetchStrategy === _types.FetchStrategy.Full) {
            // Full prefetches are dynamic responses stored in the prefetch cache.
            // They don't carry vary params or other cache metadata, so there's no
            // need to buffer them. Use the incremental version to allow data to be
            // processed as it arrives.
            prefetchStream = createIncrementalPrefetchResponseStream(response.body, closed.resolve, function onResponseSizeUpdate(totalBytesReceivedSoFar) {
                // When processing a dynamic response, we don't know how large each
                // individual segment is, so approximate by assigning each segment
                // the average of the total response size.
                if (fulfilledEntries === null) {
                    // Haven't received enough data yet to know which segments
                    // were included.
                    return;
                }
                const averageSize = totalBytesReceivedSoFar / fulfilledEntries.length;
                for (const entry of fulfilledEntries){
                    (0, _cachemap.setSizeInCacheMap)(entry, averageSize);
                }
            });
        } else {
            const { stream, size } = await createNonTaskyPrefetchResponseStream(response.body);
            closed.resolve();
            prefetchStream = stream;
            bufferedResponseSize = size;
        }
        const [serverData, cacheData] = await Promise.all([
            (0, _fetchserverresponse.createFromNextReadableStream)(prefetchStream, headers, {
                allowPartialStream: true
            }),
            response.cacheData
        ]);
        // Read head vary params synchronously. Individual segments carry their
        // own thenables in CacheNodeSeedData.
        const headVaryParamsThenable = serverData.h;
        const headVaryParams = headVaryParamsThenable !== null ? (0, _varyparamsdecoding.readVaryParams)(headVaryParamsThenable) : null;
        const now = Date.now();
        const staleAt = await getStaleAt(now, serverData.s, response);
        // PPRRuntime prefetches are partial when the server marks the response
        // as '~' (Partial). Full/LoadingBoundary prefetches are always complete.
        const isResponsePartial = fetchStrategy === _types.FetchStrategy.PPRRuntime && (cacheData?.isResponsePartial ?? false);
        // Aside from writing the data into the cache, this function also returns
        // the entries that were fulfilled, so we can streamingly update their sizes
        // in the LRU as more data comes in.
        const buildId = response.headers.get(_constants.NEXT_NAV_DEPLOYMENT_ID_HEADER) ?? serverData.b;
        const flightDatas = (0, _flightdatahelpers.normalizeFlightData)(serverData.f);
        if (typeof flightDatas === 'string') {
            rejectSegmentEntriesIfStillPending(spawnedEntries, Date.now() + 10 * 1000);
            return null;
        }
        const navigationSeed = (0, _navigation.convertServerPatchToFullTree)(now, dynamicRequestTree, flightDatas, renderedSearch, _bfcache.UnknownDynamicStaleTime);
        fulfilledEntries = writeDynamicRenderResponseIntoCache(now, fetchStrategy, flightDatas, buildId, isResponsePartial, headVaryParams, staleAt, navigationSeed, spawnedEntries);
        // For buffered responses, update LRU sizes now that we know which
        // entries were fulfilled.
        if (bufferedResponseSize !== null && fulfilledEntries !== null && fulfilledEntries.length > 0) {
            const averageSize = bufferedResponseSize / fulfilledEntries.length;
            for (const entry of fulfilledEntries){
                (0, _cachemap.setSizeInCacheMap)(entry, averageSize);
            }
        }
        // Return a promise that resolves when the network connection closes, so
        // the scheduler can track the number of concurrent network connections.
        return {
            value: null,
            closed: closed.promise
        };
    } catch (error) {
        rejectSegmentEntriesIfStillPending(spawnedEntries, Date.now() + 10 * 1000);
        return null;
    }
}
function writeDynamicTreeResponseIntoCache(now, fetchStrategy, response, serverData, entry, couldBeIntercepted, canonicalUrl, routeIsPPREnabled, headVaryParams, originalPathname, nextUrl) {
    const renderedSearch = (0, _routeparams.getRenderedSearch)(response);
    const normalizedFlightDataResult = (0, _flightdatahelpers.normalizeFlightData)(serverData.f);
    if (// MPA navigation.
    typeof normalizedFlightDataResult === 'string' || normalizedFlightDataResult.length !== 1) {
        rejectRouteCacheEntry(entry, now + 10 * 1000);
        return;
    }
    const flightData = normalizedFlightDataResult[0];
    if (!flightData.isRootRender) {
        // Unexpected response format.
        rejectRouteCacheEntry(entry, now + 10 * 1000);
        return;
    }
    const flightRouterState = flightData.tree;
    // If the response was postponed, segments may contain dynamic holes.
    // The head has its own partiality flag (flightDataEntry.isHeadPartial)
    // which is handled separately in writeDynamicRenderResponseIntoCache.
    const isResponsePartial = response.headers.get(_approuterheaders.NEXT_DID_POSTPONE_HEADER) === '1';
    // Convert the server-sent data into the RouteTree format used by the
    // client cache.
    //
    // During this traversal, we accumulate additional data into this
    // "accumulator" object.
    const acc = {
        metadataVaryPath: null
    };
    const routeTree = convertRootFlightRouterStateToRouteTree(flightRouterState, renderedSearch, acc);
    const metadataVaryPath = acc.metadataVaryPath;
    if (metadataVaryPath === null) {
        rejectRouteCacheEntry(entry, now + 10 * 1000);
        return;
    }
    (0, _optimisticroutes.discoverKnownRoute)(now, originalPathname, nextUrl, entry, routeTree, metadataVaryPath, couldBeIntercepted, canonicalUrl, routeIsPPREnabled, false // hasDynamicRewrite
    );
    // If the server sent segment data as part of the response, we should write
    // it into the cache to prevent a second, redundant prefetch request.
    // TODO: This is a leftover branch from before Client Segment Cache was
    // enabled everywhere. Tree prefetches should never include segment data.  We
    // can delete it. Leaving for a subsequent PR.
    const navigationSeed = (0, _navigation.convertServerPatchToFullTree)(now, flightRouterState, normalizedFlightDataResult, renderedSearch, _bfcache.UnknownDynamicStaleTime);
    const buildId = response.headers.get(_constants.NEXT_NAV_DEPLOYMENT_ID_HEADER) ?? serverData.b;
    writeDynamicRenderResponseIntoCache(now, fetchStrategy, normalizedFlightDataResult, buildId, isResponsePartial, headVaryParams, getStaleAtFromHeader(now, response), navigationSeed, null);
}
function rejectSegmentEntriesIfStillPending(entries, staleAt) {
    const fulfilledEntries = [];
    for (const entry of entries.values()){
        if (entry.status === 1) {
            rejectSegmentCacheEntry(entry, staleAt);
        } else if (entry.status === 2) {
            fulfilledEntries.push(entry);
        }
    }
    return fulfilledEntries;
}
function writeDynamicRenderResponseIntoCache(now, fetchStrategy, flightDatas, buildId, isResponsePartial, headVaryParams, staleAt, navigationSeed, spawnedEntries) {
    if (buildId && buildId !== (0, _navigationbuildid.getNavigationBuildId)()) {
        // The server build does not match the client. Treat as a 404. During
        // an actual navigation, the router will trigger an MPA navigation.
        if (spawnedEntries !== null) {
            rejectSegmentEntriesIfStillPending(spawnedEntries, now + 10 * 1000);
        }
        return null;
    }
    const routeTree = navigationSeed.routeTree;
    const metadataTree = navigationSeed.metadataVaryPath !== null ? createMetadataRouteTree(navigationSeed.metadataVaryPath) : null;
    for (const flightDataEntry of flightDatas){
        const seedData = flightDataEntry.seedData;
        if (seedData !== null) {
            // The data sent by the server represents only a subtree of the app. We
            // need to find the part of the task tree that matches the response.
            //
            // segmentPath represents the parent path of subtree. It's a repeating
            // pattern of parallel route key and segment:
            //
            //   [string, Segment, string, Segment, string, Segment, ...]
            const segmentPath = flightDataEntry.segmentPath;
            let tree = routeTree;
            for(let i = 0; i < segmentPath.length; i += 2){
                const parallelRouteKey = segmentPath[i];
                if (tree?.slots?.[parallelRouteKey] !== undefined) {
                    tree = tree.slots[parallelRouteKey];
                } else {
                    if (spawnedEntries !== null) {
                        rejectSegmentEntriesIfStillPending(spawnedEntries, now + 10 * 1000);
                    }
                    return null;
                }
            }
            writeSeedDataIntoCache(now, fetchStrategy, tree, staleAt, seedData, isResponsePartial, spawnedEntries);
        }
        const head = flightDataEntry.head;
        if (head !== null && metadataTree !== null) {
            // When Cache Components is enabled, the server conservatively marks
            // the head as partial during static generation (isPossiblyPartialHead
            // in app-render.tsx), even for fully static pages where the head is
            // actually complete. When the response is non-partial, we override
            // this since the server confirmed no dynamic content exists.
            //
            // Without Cache Components, the server always sends the correct
            // isHeadPartial value, so no override is needed.
            const isHeadPartial = ("TURBOPACK compile-time falsy", 0) ? "TURBOPACK unreachable" : flightDataEntry.isHeadPartial;
            fulfillEntrySpawnedByRuntimePrefetch(now, fetchStrategy, head, isHeadPartial, staleAt, // parameter.
            headVaryParams, metadataTree, spawnedEntries);
        }
    }
    // Any entry that's still pending was intentionally not rendered by the
    // server, because it was inside the loading boundary. Mark them as rejected
    // so we know not to fetch them again.
    // TODO: If PPR is enabled on some routes but not others, then it's possible
    // that a different page is able to do a per-segment prefetch of one of the
    // segments we're marking as rejected here. We should mark on the segment
    // somehow that the reason for the rejection is because of a non-PPR prefetch.
    // That way a per-segment prefetch knows to disregard the rejection.
    if (spawnedEntries !== null) {
        const fulfilledEntries = rejectSegmentEntriesIfStillPending(spawnedEntries, now + 10 * 1000);
        return fulfilledEntries;
    }
    return null;
}
function writeSeedDataIntoCache(now, fetchStrategy, tree, staleAt, seedData, isResponsePartial, entriesOwnedByCurrentTask) {
    // This function is used to write the result of a runtime server request
    // (CacheNodeSeedData) into the prefetch cache.
    const rsc = seedData[0];
    const isPartial = rsc === null || isResponsePartial;
    const varyParamsThenable = seedData[4];
    // Each segment carries its own vary params thenable in the seed data. The
    // thenable resolves to the set of params the segment accessed during render.
    // A null thenable means tracking was not enabled (not a prerender).
    const varyParams = varyParamsThenable !== null ? (0, _varyparamsdecoding.readVaryParams)(varyParamsThenable) : null;
    fulfillEntrySpawnedByRuntimePrefetch(now, fetchStrategy, rsc, isPartial, staleAt, varyParams, tree, entriesOwnedByCurrentTask);
    // Recursively write the child data into the cache.
    const slots = tree.slots;
    if (slots !== null) {
        const seedDataChildren = seedData[1];
        for(const parallelRouteKey in slots){
            const childTree = slots[parallelRouteKey];
            const childSeedData = seedDataChildren[parallelRouteKey];
            if (childSeedData !== null && childSeedData !== undefined) {
                writeSeedDataIntoCache(now, fetchStrategy, childTree, staleAt, childSeedData, isResponsePartial, entriesOwnedByCurrentTask);
            }
        }
    }
}
function fulfillEntrySpawnedByRuntimePrefetch(now, fetchStrategy, rsc, isPartial, staleAt, segmentVaryParams, tree, entriesOwnedByCurrentTask) {
    // We should only write into cache entries that are owned by us. Or create
    // a new one and write into that. We must never write over an entry that was
    // created by a different task, because that causes data races.
    const ownedEntry = entriesOwnedByCurrentTask !== null ? entriesOwnedByCurrentTask.get(tree.requestKey) : undefined;
    if (ownedEntry !== undefined) {
        const fulfilledEntry = fulfillSegmentCacheEntry(ownedEntry, rsc, staleAt, isPartial);
        // Re-key the entry based on which params the segment actually depends on.
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
    } else {
        // There's no matching entry. Attempt to create a new one.
        const possiblyNewEntry = readOrCreateSegmentCacheEntry(now, fetchStrategy, tree);
        if (possiblyNewEntry.status === 0) {
            // Confirmed this is a new entry. We can fulfill it.
            const newEntry = possiblyNewEntry;
            const fulfilledEntry = fulfillSegmentCacheEntry(upgradeToPendingSegment(newEntry, fetchStrategy), rsc, staleAt, isPartial);
            // Re-key the entry based on which params the segment actually depends on.
            if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
            ;
        } else {
            // There was already an entry in the cache. But we may be able to
            // replace it with the new one from the server.
            const newEntry = fulfillSegmentCacheEntry(upgradeToPendingSegment(createDetachedSegmentCacheEntry(now), fetchStrategy), rsc, staleAt, isPartial);
            // Use the fulfilled vary path if available, otherwise fall back to
            // the request vary path.
            const varyPath = ("TURBOPACK compile-time falsy", 0) ? "TURBOPACK unreachable" : (0, _varypath.getSegmentVaryPathForRequest)(fetchStrategy, tree);
            upsertSegmentEntry(now, varyPath, newEntry);
        }
    }
}
async function fetchPrefetchResponse(url, headers) {
    const fetchPriority = 'low';
    // When issuing a prefetch request, don't immediately decode the response; we
    // use the lower level `createFromResponse` API instead because we need to do
    // some extra processing of the response stream. See
    // `createNonTaskyPrefetchResponseStream` for more details.
    const shouldImmediatelyDecode = false;
    const response = await (0, _fetchserverresponse.createFetch)(url, headers, fetchPriority, shouldImmediatelyDecode);
    if (!response.ok) {
        return null;
    }
    // Check the content type
    if ("TURBOPACK compile-time falsy", 0) {
    // In output: "export" mode, we relaxed about the content type, since it's
    // not Next.js that's serving the response. If the status is OK, assume the
    // response is valid. If it's not a valid response, the Flight client won't
    // be able to decode it, and we'll treat it as a miss.
    } else {
        const contentType = response.headers.get('content-type');
        const isFlightResponse = contentType && contentType.startsWith(_approuterheaders.RSC_CONTENT_TYPE_HEADER);
        if (!isFlightResponse) {
            return null;
        }
    }
    return response;
}
async function createNonTaskyPrefetchResponseStream(body) {
    // Buffer the entire response before passing it to the Flight client. This
    // ensures that when Flight processes the stream, all model data is available
    // synchronously. This is important for readVaryParams, which synchronously
    // checks the thenable status — if data arrived in multiple network chunks,
    // the thenables might not yet be fulfilled.
    //
    // TODO: There are too many intermediate stream transformations in the
    // prefetch response pipeline (e.g. stripIsPartialByte, this function).
    // These could all be consolidated into a single transformation. Refactor
    // once the cached navigations experiment lands.
    //
    // Read the entire response from the network.
    const reader = body.getReader();
    const chunks = [];
    let size = 0;
    while(true){
        const { done, value } = await reader.read();
        if (done) break;
        chunks.push(value);
        size += value.byteLength;
    }
    // Concatenate into a single chunk so that Flight's processBinaryChunk
    // processes all rows synchronously in one call. Multiple chunks would not
    // be sufficient: even though reader.read() resolves as a microtask for
    // already-enqueued data, the `await` continuation from
    // createFromReadableStream can interleave between chunks. If the root
    // model row isn't the first row (e.g. outlined values come first), the
    // PromiseResolveThenableJob from `await` can cause the root to initialize
    // eagerly, scheduling the continuation before remaining chunks (including
    // promise value rows) are processed. A single chunk avoids this.
    let buffer;
    if (chunks.length === 1) {
        buffer = chunks[0];
    } else if (chunks.length > 1) {
        buffer = new Uint8Array(size);
        let offset = 0;
        for (const chunk of chunks){
            buffer.set(chunk, offset);
            offset += chunk.byteLength;
        }
    } else {
        buffer = new Uint8Array(0);
    }
    const stream = new ReadableStream({
        start (controller) {
            controller.enqueue(buffer);
            controller.close();
        }
    });
    return {
        stream,
        size
    };
}
/**
 * Creates a streaming (non-buffered) prefetch response stream for dynamic/Full
 * prefetches. These are essentially dynamic responses that get stored in the
 * prefetch cache — they don't carry vary params or other cache metadata that
 * requires synchronous thenable resolution, so there's no need to buffer them.
 * They should continue to stream so consumers can process data as it arrives.
 */ function createIncrementalPrefetchResponseStream(originalFlightStream, onStreamClose, onResponseSizeUpdate) {
    // While processing the original stream, we incrementally update the size
    // of the cache entry in the LRU.
    let totalByteLength = 0;
    const reader = originalFlightStream.getReader();
    return new ReadableStream({
        async pull (controller) {
            while(true){
                const { done, value } = await reader.read();
                if (!done) {
                    // Pass to the target stream and keep consuming the Flight response
                    // from the server.
                    controller.enqueue(value);
                    // Incrementally update the size of the cache entry in the LRU.
                    totalByteLength += value.byteLength;
                    onResponseSizeUpdate(totalByteLength);
                    continue;
                }
                controller.close();
                onStreamClose();
                return;
            }
        }
    });
}
function addSegmentPathToUrlInOutputExportMode(url, segmentPath) {
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    return url;
}
function canNewFetchStrategyProvideMoreContent(currentStrategy, newStrategy) {
    return currentStrategy < newStrategy;
}
/**
 * Adds the instant prefetch header if the navigation lock is active.
 * Uses a lazy require to ensure dead code elimination.
 */ function addInstantPrefetchHeaderIfLocked(headers) {
    if ("TURBOPACK compile-time truthy", 1) {
        const { isNavigationLocked } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/navigation-testing-lock.js [app-client] (ecmascript)");
        if (isNavigationLocked()) {
            headers[_approuterheaders.NEXT_INSTANT_PREFETCH_HEADER] = '1';
        }
    }
}
function getStaleAtFromHeader(now, response) {
    const staleTimeSeconds = parseInt(response.headers.get(_approuterheaders.NEXT_ROUTER_STALE_TIME_HEADER) ?? '', 10);
    const staleTimeMs = !isNaN(staleTimeSeconds) ? getStaleTimeMs(staleTimeSeconds) : _navigatereducer.STATIC_STALETIME_MS;
    return now + staleTimeMs;
}
async function getStaleAt(now, staleTimeIterable, response) {
    if (staleTimeIterable !== undefined) {
        // Iterate the async iterable and take the last yielded value. The server
        // yields updated staleTime values during the render; the last one is the
        // final staleTime.
        let staleTimeSeconds;
        for await (const value of staleTimeIterable){
            staleTimeSeconds = value;
        }
        if (staleTimeSeconds !== undefined) {
            const staleTimeMs = isNaN(staleTimeSeconds) ? _navigatereducer.STATIC_STALETIME_MS : getStaleTimeMs(staleTimeSeconds);
            return now + staleTimeMs;
        }
    }
    if (response !== undefined) {
        return getStaleAtFromHeader(now, response);
    }
    return now + _navigatereducer.STATIC_STALETIME_MS;
}
function writeStaticStageResponseIntoCache(now, flightData, buildId, headVaryParamsThenable, staleAt, baseTree, renderedSearch, isResponsePartial) {
    const fetchStrategy = isResponsePartial ? _types.FetchStrategy.PPR : _types.FetchStrategy.Full;
    const headVaryParams = headVaryParamsThenable !== null ? (0, _varyparamsdecoding.readVaryParams)(headVaryParamsThenable) : null;
    const flightDatas = (0, _flightdatahelpers.normalizeFlightData)(flightData);
    if (typeof flightDatas === 'string') {
        return;
    }
    const navigationSeed = (0, _navigation.convertServerPatchToFullTree)(now, baseTree, flightDatas, renderedSearch, _bfcache.UnknownDynamicStaleTime);
    writeDynamicRenderResponseIntoCache(now, fetchStrategy, flightDatas, buildId, isResponsePartial, headVaryParams, staleAt, navigationSeed, null // spawnedEntries — no pre-created entries; will create or upsert
    );
}
async function processRuntimePrefetchStream(now, runtimePrefetchStream, baseTree, renderedSearch) {
    const { stream, isPartial } = await stripIsPartialByte(runtimePrefetchStream);
    const serverData = await (0, _fetchserverresponse.createFromNextReadableStream)(stream, undefined, {
        allowPartialStream: true
    });
    const headVaryParamsThenable = serverData.h;
    const headVaryParams = headVaryParamsThenable !== null ? (0, _varyparamsdecoding.readVaryParams)(headVaryParamsThenable) : null;
    const staleAt = await getStaleAt(now, serverData.s);
    const flightDatas = (0, _flightdatahelpers.normalizeFlightData)(serverData.f);
    if (typeof flightDatas === 'string') {
        return null;
    }
    const navigationSeed = (0, _navigation.convertServerPatchToFullTree)(now, baseTree, flightDatas, renderedSearch, _bfcache.UnknownDynamicStaleTime);
    return {
        flightDatas,
        navigationSeed,
        buildId: serverData.b,
        isResponsePartial: isPartial,
        headVaryParams,
        staleAt
    };
}
async function stripIsPartialByte(stream) {
    // When there is no recognized marker byte, the fallback depends on whether
    // Cached Navigations is enabled. When enabled, dynamic navigation responses
    // don't have a marker but may contain dynamic holes, so they are treated as
    // partial. When disabled, unmarked responses are treated as non-partial.
    const defaultIsPartial = !!("TURBOPACK compile-time value", false);
    const reader = stream.getReader();
    const { done, value } = await reader.read();
    if (done || !value || value.byteLength === 0) {
        return {
            stream: new ReadableStream({
                start: (c)=>c.close()
            }),
            isPartial: defaultIsPartial
        };
    }
    const firstByte = value[0];
    const hasMarker = firstByte === 0x23 || firstByte === 0x7e;
    const isPartial = hasMarker ? firstByte === 0x7e : defaultIsPartial;
    const remainder = hasMarker ? value.byteLength > 1 ? value.subarray(1) : null : value;
    return {
        isPartial,
        stream: new ReadableStream({
            start (controller) {
                if (remainder) {
                    controller.enqueue(remainder);
                }
            },
            async pull (controller) {
                const result = await reader.read();
                if (result.done) {
                    controller.close();
                } else {
                    controller.enqueue(result.value);
                }
            }
        })
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/debug-channel.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    createDebugChannel: null,
    getOrCreateDebugChannelReadableWriterPair: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    createDebugChannel: function() {
        return createDebugChannel;
    },
    getOrCreateDebugChannelReadableWriterPair: function() {
        return getOrCreateDebugChannelReadableWriterPair;
    }
});
const _approuterheaders = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-headers.js [app-client] (ecmascript)");
const _invarianterror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/invariant-error.js [app-client] (ecmascript)");
const pairs = new Map();
function getOrCreateDebugChannelReadableWriterPair(requestId) {
    let pair = pairs.get(requestId);
    if (!pair) {
        const { readable, writable } = new TransformStream();
        pair = {
            readable,
            writer: writable.getWriter()
        };
        pairs.set(requestId, pair);
        pair.writer.closed.finally(()=>pairs.delete(requestId));
    }
    return pair;
}
function createDebugChannel(requestHeaders) {
    let requestId;
    if (requestHeaders) {
        requestId = requestHeaders[_approuterheaders.NEXT_REQUEST_ID_HEADER] ?? undefined;
        if (!requestId) {
            throw Object.defineProperty(new _invarianterror.InvariantError(`Expected a ${JSON.stringify(_approuterheaders.NEXT_REQUEST_ID_HEADER)} request header.`), "__NEXT_ERROR_CODE", {
                value: "E854",
                enumerable: false,
                configurable: true
            });
        }
    } else {
        requestId = self.__next_r;
        if (!requestId) {
            throw Object.defineProperty(new _invarianterror.InvariantError(`Expected a request ID to be defined for the document via self.__next_r.`), "__NEXT_ERROR_CODE", {
                value: "E806",
                enumerable: false,
                configurable: true
            });
        }
    }
    const { readable } = getOrCreateDebugChannelReadableWriterPair(requestId);
    return {
        readable
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/fetch-server-response.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
'use client';
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    createFetch: null,
    createFromNextReadableStream: null,
    decodeStaticStage: null,
    fetchServerResponse: null,
    processFetch: null,
    resolveStaticStageData: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    createFetch: function() {
        return createFetch;
    },
    createFromNextReadableStream: function() {
        return createFromNextReadableStream;
    },
    decodeStaticStage: function() {
        return decodeStaticStage;
    },
    fetchServerResponse: function() {
        return fetchServerResponse;
    },
    processFetch: function() {
        return processFetch;
    },
    resolveStaticStageData: function() {
        return resolveStaticStageData;
    }
});
const _client = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-server-dom-turbopack/client.js [app-client] (ecmascript)");
const _invarianterror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/invariant-error.js [app-client] (ecmascript)");
const _approuterheaders = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-headers.js [app-client] (ecmascript)");
const _appcallserver = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/app-call-server.js [app-client] (ecmascript)");
const _appfindsourcemapurl = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/app-find-source-map-url.js [app-client] (ecmascript)");
const _flightdatahelpers = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/flight-data-helpers.js [app-client] (ecmascript)");
const _setcachebustingsearchparam = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/set-cache-busting-search-param.js [app-client] (ecmascript)");
const _routeparams = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/route-params.js [app-client] (ecmascript)");
const _deploymentid = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/deployment-id.js [app-client] (ecmascript)");
const _navigationbuildid = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/navigation-build-id.js [app-client] (ecmascript)");
const _constants = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/constants.js [app-client] (ecmascript)");
const _cache = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache.js [app-client] (ecmascript)");
const _bfcache = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/bfcache.js [app-client] (ecmascript)");
const createFromReadableStream = _client.createFromReadableStream;
const createFromFetch = _client.createFromFetch;
let createDebugChannel;
if ("TURBOPACK compile-time truthy", 1) {
    createDebugChannel = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/debug-channel.js [app-client] (ecmascript)").createDebugChannel;
}
function doMpaNavigation(url) {
    return (0, _routeparams.urlToUrlWithoutFlightMarker)(new URL(url, location.origin)).toString();
}
let isPageUnloading = false;
if (typeof window !== 'undefined') {
    // Track when the page is unloading, e.g. due to reloading the page or
    // performing hard navigations. This allows us to suppress error logging when
    // the browser cancels in-flight requests during page unload.
    window.addEventListener('pagehide', ()=>{
        isPageUnloading = true;
    });
    // Reset the flag on pageshow, e.g. when navigating back and the JavaScript
    // execution context is restored by the browser.
    window.addEventListener('pageshow', ()=>{
        isPageUnloading = false;
    });
}
async function fetchServerResponse(url, options) {
    const { flightRouterState, nextUrl } = options;
    const headers = {
        // Enable flight response
        [_approuterheaders.RSC_HEADER]: '1',
        // Provide the current router state
        [_approuterheaders.NEXT_ROUTER_STATE_TREE_HEADER]: (0, _flightdatahelpers.prepareFlightRouterStateForRequest)(flightRouterState, options.isHmrRefresh)
    };
    if (("TURBOPACK compile-time value", "development") === 'development' && options.isHmrRefresh) {
        headers[_approuterheaders.NEXT_HMR_REFRESH_HEADER] = '1';
    }
    if (nextUrl) {
        headers[_approuterheaders.NEXT_URL] = nextUrl;
    }
    // In static export mode, we need to modify the URL to request the .txt file,
    // but we should preserve the original URL for the canonical URL and error handling.
    const originalUrl = url;
    try {
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
        // Typically, during a navigation, we decode the response using Flight's
        // `createFromFetch` API, which accepts a `fetch` promise.
        // TODO: Remove this check once the old PPR flag is removed
        const isLegacyPPR = ("TURBOPACK compile-time value", false) && !("TURBOPACK compile-time value", false);
        const shouldImmediatelyDecode = !isLegacyPPR;
        const res = await createFetch(url, headers, 'auto', shouldImmediatelyDecode);
        const responseUrl = (0, _routeparams.urlToUrlWithoutFlightMarker)(new URL(res.url));
        const canonicalUrl = res.redirected ? responseUrl : originalUrl;
        const contentType = res.headers.get('content-type') || '';
        const interception = !!res.headers.get('vary')?.includes(_approuterheaders.NEXT_URL);
        const postponed = !!res.headers.get(_approuterheaders.NEXT_DID_POSTPONE_HEADER);
        let isFlightResponse = contentType.startsWith(_approuterheaders.RSC_CONTENT_TYPE_HEADER);
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
        // If fetch returns something different than flight response handle it like a mpa navigation
        // If the fetch was not 200, we also handle it like a mpa navigation
        if (!isFlightResponse || !res.ok || !res.body) {
            // in case the original URL came with a hash, preserve it before redirecting to the new URL
            if (url.hash) {
                responseUrl.hash = url.hash;
            }
            return doMpaNavigation(responseUrl.toString());
        }
        // We may navigate to a page that requires a different Webpack runtime.
        // In prod, every page will have the same Webpack runtime.
        // In dev, the Webpack runtime is minimal for each page.
        // We need to ensure the Webpack runtime is updated before executing client-side JS of the new page.
        // TODO: This needs to happen in the Flight Client.
        // Or Webpack needs to include the runtime update in the Flight response as
        // a blocking script.
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
        let flightResponsePromise = res.flightResponsePromise;
        if (flightResponsePromise === null) {
            // Typically, `createFetch` would have already started decoding the
            // Flight response. If it hasn't, though, we need to decode it now.
            // TODO: This should only be reachable if legacy PPR is enabled (i.e. PPR
            // without Cache Components). Remove this branch once legacy PPR
            // is deleted.
            flightResponsePromise = createFromNextReadableStream(res.body, headers, {
                allowPartialStream: postponed
            });
        }
        const [flightResponse, cacheData] = await Promise.all([
            flightResponsePromise,
            res.cacheData
        ]);
        if ((res.headers.get(_constants.NEXT_NAV_DEPLOYMENT_ID_HEADER) ?? flightResponse.b) !== (0, _navigationbuildid.getNavigationBuildId)()) {
            // The server build does not match the client build.
            return doMpaNavigation(res.url);
        }
        const normalizedFlightData = (0, _flightdatahelpers.normalizeFlightData)(flightResponse.f);
        if (typeof normalizedFlightData === 'string') {
            return doMpaNavigation(normalizedFlightData);
        }
        const staticStageData = cacheData !== null ? await resolveStaticStageData(cacheData, flightResponse, headers) : null;
        return {
            flightData: normalizedFlightData,
            canonicalUrl: canonicalUrl,
            // TODO: We should be able to read this from the rewrite header, not the
            // Flight response. Theoretically they should always agree, but there are
            // currently some cases where it's incorrect for interception routes. We
            // can always trust the value in the response body. However, per-segment
            // prefetch responses don't embed the value in the body; they rely on the
            // header alone. So we need to investigate why the header is sometimes
            // wrong for interception routes.
            renderedSearch: flightResponse.q,
            couldBeIntercepted: interception,
            supportsPerSegmentPrefetching: flightResponse.S,
            postponed,
            // The dynamicStaleTime is only present in the response body when
            // a page exports unstable_dynamicStaleTime and this is a dynamic render.
            // When absent (UnknownDynamicStaleTime), the client falls back to the
            // global DYNAMIC_STALETIME_MS. The value is in seconds.
            dynamicStaleTime: flightResponse.d ?? _bfcache.UnknownDynamicStaleTime,
            staticStageData,
            runtimePrefetchStream: flightResponse.p ?? null,
            responseHeaders: res.headers,
            debugInfo: flightResponsePromise._debugInfo ?? null
        };
    } catch (err) {
        if (!isPageUnloading) {
            console.error(`Failed to fetch RSC payload for ${originalUrl}. Falling back to browser navigation.`, err);
        }
        // If fetch fails handle it like a mpa navigation
        // TODO-APP: Add a test for the case where a CORS request fails, e.g. external url redirect coming from the response.
        // See https://github.com/vercel/next.js/issues/43605#issuecomment-1451617521 for a reproduction.
        return originalUrl.toString();
    }
}
async function processFetch(response) {
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    return {
        response,
        cacheData: null
    };
}
async function resolveStaticStageData(cacheData, flightResponse, headers) {
    const { isResponsePartial, responseBodyClone } = cacheData;
    if (responseBodyClone) {
        if (!isResponsePartial) {
            // Fully static — cache the entire decoded response as-is.
            responseBodyClone.cancel();
            return {
                response: flightResponse,
                isResponsePartial: false
            };
        }
        if (flightResponse.l !== undefined) {
            // Partially static — truncate the body clone at the byte boundary and
            // decode it.
            const response = await decodeStaticStage(responseBodyClone, flightResponse.l, headers);
            return {
                response,
                isResponsePartial: true
            };
        }
        // No caching — cancel the unused clone.
        responseBodyClone.cancel();
    }
    return null;
}
async function decodeStaticStage(responseBodyClone, staticStageByteLengthPromise, headers) {
    const staticStageByteLength = await staticStageByteLengthPromise;
    const truncatedStream = truncateStream(responseBodyClone, staticStageByteLength);
    return createFromNextReadableStream(truncatedStream, headers, {
        allowPartialStream: true
    });
}
async function createFetch(url, headers, fetchPriority, shouldImmediatelyDecode, signal) {
    // TODO: In output: "export" mode, the headers do nothing. Omit them (and the
    // cache busting search param) from the request so they're
    // maximally cacheable.
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    const deploymentId = (0, _deploymentid.getDeploymentId)();
    if (deploymentId) {
        headers['x-deployment-id'] = deploymentId;
    }
    if ("TURBOPACK compile-time truthy", 1) {
        if (self.__next_r) {
            headers[_approuterheaders.NEXT_HTML_REQUEST_ID_HEADER] = self.__next_r;
        }
        // Create a new request ID for the server action request. The server uses
        // this to tag debug information sent via WebSocket to the client, which
        // then routes those chunks to the debug channel associated with this ID.
        headers[_approuterheaders.NEXT_REQUEST_ID_HEADER] = crypto.getRandomValues(new Uint32Array(1))[0].toString(16);
    }
    const fetchOptions = {
        // Backwards compat for older browsers. `same-origin` is the default in modern browsers.
        credentials: 'same-origin',
        headers,
        priority: fetchPriority || undefined,
        signal
    };
    // `fetchUrl` is slightly different from `url` because we add a cache-busting
    // search param to it. This should not leak outside of this function, so we
    // track them separately.
    let fetchUrl = new URL(url);
    await (0, _setcachebustingsearchparam.setCacheBustingSearchParam)(fetchUrl, headers);
    let processed = fetch(fetchUrl, fetchOptions).then(processFetch);
    let fetchPromise = processed.then(({ response })=>response);
    // Immediately pass the fetch promise to the Flight client so that the debug
    // info includes the latency from the client to the server. The internal timer
    // in React starts as soon as `createFromFetch` is called.
    //
    // The only case where we don't do this is during a prefetch, because a
    // top-level prefetch response never blocks a navigation; if it hasn't already
    // been written into the cache by the time the navigation happens, the router
    // will go straight to a dynamic request.
    let flightResponsePromise = shouldImmediatelyDecode ? createFromNextFetch(fetchPromise, headers) : null;
    let browserResponse = await fetchPromise;
    // If the server responds with a redirect (e.g. 307), and the redirected
    // location does not contain the cache busting search param set in the
    // original request, the response is likely invalid — when following the
    // redirect, the browser forwards the request headers, but since the cache
    // busting search param is missing, the server will reject the request due to
    // a mismatch.
    //
    // Ideally, we would be able to intercept the redirect response and perform it
    // manually, instead of letting the browser automatically follow it, but this
    // is not allowed by the fetch API.
    //
    // So instead, we must "replay" the redirect by fetching the new location
    // again, but this time we'll append the cache busting search param to prevent
    // a mismatch.
    //
    // TODO: We can optimize Next.js's built-in middleware APIs by returning a
    // custom status code, to prevent the browser from automatically following it.
    //
    // This does not affect Server Action-based redirects; those are encoded
    // differently, as part of the Flight body. It only affects redirects that
    // occur in a middleware or a third-party proxy.
    let redirected = browserResponse.redirected;
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    // Remove the cache busting search param from the response URL, to prevent it
    // from leaking outside of this function.
    const responseUrl = new URL(browserResponse.url, fetchUrl);
    responseUrl.searchParams.delete(_approuterheaders.NEXT_RSC_UNION_QUERY);
    const rscResponse = {
        url: responseUrl.href,
        // This is true if any redirects occurred, either automatically by the
        // browser, or manually by us. So it's different from
        // `browserResponse.redirected`, which only tells us whether the browser
        // followed a redirect, and only for the last response in the chain.
        redirected,
        // These can be copied from the last browser response we received. We
        // intentionally only expose the subset of fields that are actually used
        // elsewhere in the codebase.
        ok: browserResponse.ok,
        headers: browserResponse.headers,
        body: browserResponse.body,
        status: browserResponse.status,
        // This is the exact promise returned by `createFromFetch`. It contains
        // debug information that we need to transfer to any derived promises that
        // are later rendered by React.
        flightResponsePromise: flightResponsePromise,
        cacheData: processed.then(({ cacheData })=>cacheData)
    };
    return rscResponse;
}
function createFromNextReadableStream(flightStream, requestHeaders, options) {
    return createFromReadableStream(flightStream, {
        callServer: _appcallserver.callServer,
        findSourceMapURL: _appfindsourcemapurl.findSourceMapURL,
        debugChannel: createDebugChannel && createDebugChannel(requestHeaders),
        unstable_allowPartialStream: options?.allowPartialStream
    });
}
function createFromNextFetch(promiseForResponse, requestHeaders) {
    return createFromFetch(promiseForResponse, {
        callServer: _appcallserver.callServer,
        findSourceMapURL: _appfindsourcemapurl.findSourceMapURL,
        debugChannel: createDebugChannel && createDebugChannel(requestHeaders)
    });
}
function truncateStream(stream, byteLength) {
    const reader = stream.getReader();
    let remaining = byteLength;
    return new ReadableStream({
        async pull (controller) {
            if (remaining <= 0) {
                reader.cancel();
                controller.close();
                return;
            }
            const { done, value } = await reader.read();
            if (done) {
                controller.close();
                return;
            }
            if (value.byteLength <= remaining) {
                controller.enqueue(value);
                remaining -= value.byteLength;
            } else {
                controller.enqueue(value.subarray(0, remaining));
                remaining = 0;
                reader.cancel();
                controller.close();
            }
        },
        cancel () {
            reader.cancel();
        }
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/is-navigating-to-new-root-layout.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "isNavigatingToNewRootLayout", {
    enumerable: true,
    get: function() {
        return isNavigatingToNewRootLayout;
    }
});
const _approutertypes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/app-router-types.js [app-client] (ecmascript)");
function isNavigatingToNewRootLayout(currentTree, nextTree) {
    // Compare segments
    const currentTreeSegment = currentTree[0];
    const nextTreeSegment = nextTree.segment;
    // If any segment is different before we find the root layout, the root layout has changed.
    // E.g. /same/(group1)/layout.js -> /same/(group2)/layout.js
    // First segment is 'same' for both, keep looking. (group1) changed to (group2) before the root layout was found, it must have changed.
    if (Array.isArray(currentTreeSegment) && Array.isArray(nextTreeSegment)) {
        // Compare dynamic param name and type but ignore the value, different values would not affect the current root layout
        // /[name] - /slug1 and /slug2, both values (slug1 & slug2) still has the same layout /[name]/layout.js
        if (currentTreeSegment[0] !== nextTreeSegment[0] || currentTreeSegment[2] !== nextTreeSegment[2]) {
            return true;
        }
    } else if (currentTreeSegment !== nextTreeSegment) {
        return true;
    }
    // Current tree root layout found
    const currentIsRootLayout = ((currentTree[4] ?? 0) & _approutertypes.PrefetchHint.IsRootLayout) !== 0;
    const nextIsRootLayout = (nextTree.prefetchHints & _approutertypes.PrefetchHint.IsRootLayout) !== 0;
    if (currentIsRootLayout) {
        // If the next tree doesn't have the root layout flag, it must have changed.
        return !nextIsRootLayout;
    }
    // Current tree didn't have its root layout here, must have changed.
    if (nextIsRootLayout) {
        return true;
    }
    const slots = nextTree.slots;
    const currentTreeChildren = currentTree[1];
    if (slots !== null) {
        for(const slot in slots){
            const nextTreeChild = slots[slot];
            const currentTreeChild = currentTreeChildren[slot];
            if (currentTreeChild === undefined || isNavigatingToNewRootLayout(currentTreeChild, nextTreeChild)) {
                return true;
            }
        }
    }
    return false;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/committed-state.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    getLastCommittedTree: null,
    setLastCommittedTree: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    getLastCommittedTree: function() {
        return getLastCommittedTree;
    },
    setLastCommittedTree: function() {
        return setLastCommittedTree;
    }
});
// The tree from the last state that was committed to the browser history
// (i.e., the last state for which HistoryUpdater's useInsertionEffect ran).
// This lets the server-patch reducer distinguish between retrying a
// navigation that already pushed a history entry vs one whose transition
// suspended and never committed.
//
// Currently only used by the server-patch retry logic, but this module is a
// stepping stone toward a broader refactor of the navigation queue. The
// existing AppRouter action queue will eventually be replaced by a more
// reactive model that explicitly tracks pending vs committed navigation
// state. This file will likely evolve into (or be subsumed by) that new
// implementation.
let lastCommittedTree = null;
function getLastCommittedTree() {
    return lastCommittedTree;
}
function setLastCommittedTree(tree) {
    lastCommittedTree = tree;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/ppr-navigations.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    FreshnessPolicy: null,
    createInitialCacheNodeForHydration: null,
    isDeferredRsc: null,
    spawnDynamicRequests: null,
    startPPRNavigation: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    FreshnessPolicy: function() {
        return FreshnessPolicy;
    },
    createInitialCacheNodeForHydration: function() {
        return createInitialCacheNodeForHydration;
    },
    isDeferredRsc: function() {
        return isDeferredRsc;
    },
    spawnDynamicRequests: function() {
        return spawnDynamicRequests;
    },
    startPPRNavigation: function() {
        return startPPRNavigation;
    }
});
const _approutertypes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/app-router-types.js [app-client] (ecmascript)");
const _segment = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/segment.js [app-client] (ecmascript)");
const _matchsegments = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/match-segments.js [app-client] (ecmascript)");
const _createhreffromurl = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/create-href-from-url.js [app-client] (ecmascript)");
const _fetchserverresponse = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/fetch-server-response.js [app-client] (ecmascript)");
const _useactionqueue = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/use-action-queue.js [app-client] (ecmascript)");
const _routerreducertypes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/router-reducer-types.js [app-client] (ecmascript)");
const _isnavigatingtonewrootlayout = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/is-navigating-to-new-root-layout.js [app-client] (ecmascript)");
const _committedstate = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/committed-state.js [app-client] (ecmascript)");
const _navigation = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/navigation.js [app-client] (ecmascript)");
const _cache = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache.js [app-client] (ecmascript)");
const _types = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/types.js [app-client] (ecmascript)");
const _optimisticroutes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/optimistic-routes.js [app-client] (ecmascript)");
const _constants = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/constants.js [app-client] (ecmascript)");
const _varypath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/vary-path.js [app-client] (ecmascript)");
const _bfcache = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/bfcache.js [app-client] (ecmascript)");
var FreshnessPolicy = /*#__PURE__*/ function(FreshnessPolicy) {
    FreshnessPolicy[FreshnessPolicy["Default"] = 0] = "Default";
    FreshnessPolicy[FreshnessPolicy["Hydration"] = 1] = "Hydration";
    FreshnessPolicy[FreshnessPolicy["HistoryTraversal"] = 2] = "HistoryTraversal";
    FreshnessPolicy[FreshnessPolicy["RefreshAll"] = 3] = "RefreshAll";
    FreshnessPolicy[FreshnessPolicy["HMRRefresh"] = 4] = "HMRRefresh";
    FreshnessPolicy[FreshnessPolicy["Gesture"] = 5] = "Gesture";
    return FreshnessPolicy;
}({});
const noop = ()=>{};
function createInitialCacheNodeForHydration(navigatedAt, initialTree, seedData, seedHead, seedDynamicStaleAt) {
    // Create the initial cache node tree, using the data embedded into the
    // HTML document.
    const accumulation = {
        separateRefreshUrls: null,
        scrollRef: null
    };
    const task = createCacheNodeOnNavigation(navigatedAt, initialTree, null, 1, seedData, seedHead, seedDynamicStaleAt, false, accumulation);
    return task;
}
function startPPRNavigation(navigatedAt, oldUrl, oldRenderedSearch, oldCacheNode, oldRouterState, newRouteTree, newMetadataVaryPath, freshness, seedData, seedHead, seedDynamicStaleAt, isSamePageNavigation, accumulation) {
    const didFindRootLayout = false;
    const parentNeedsDynamicRequest = false;
    const parentRefreshState = null;
    const oldRootRefreshState = {
        canonicalUrl: (0, _createhreffromurl.createHrefFromUrl)(oldUrl),
        renderedSearch: oldRenderedSearch
    };
    return updateCacheNodeOnNavigation(navigatedAt, oldUrl, oldCacheNode !== null ? oldCacheNode : undefined, oldRouterState, newRouteTree, newMetadataVaryPath, freshness, didFindRootLayout, seedData, seedHead, seedDynamicStaleAt, isSamePageNavigation, parentNeedsDynamicRequest, oldRootRefreshState, parentRefreshState, accumulation);
}
function updateCacheNodeOnNavigation(navigatedAt, oldUrl, oldCacheNode, oldRouterState, newRouteTree, newMetadataVaryPath, freshness, didFindRootLayout, seedData, seedHead, seedDynamicStaleAt, isSamePageNavigation, parentNeedsDynamicRequest, oldRootRefreshState, parentRefreshState, accumulation) {
    // Check if this segment matches the one in the previous route.
    const oldSegment = oldRouterState[0];
    const newSegment = createSegmentFromRouteTree(newRouteTree);
    if (!(0, _matchsegments.matchSegment)(newSegment, oldSegment)) {
        // This segment does not match the previous route. We're now entering the
        // new part of the target route. Switch to the "create" path.
        if (// highest-level layout in a route tree is referred to as the "root"
        // layout.) This could mean that we're navigating between two different
        // root layouts. When this happens, we perform a full-page (MPA-style)
        // navigation.
        //
        // However, the algorithm for deciding where to start rendering a route
        // (i.e. the one performed in order to reach this function) is stricter
        // than the one used to detect a change in the root layout. So just
        // because we're re-rendering a segment outside of the root layout does
        // not mean we should trigger a full-page navigation.
        //
        // Specifically, we handle dynamic parameters differently: two segments
        // are considered the same even if their parameter values are different.
        //
        // Refer to isNavigatingToNewRootLayout for details.
        //
        // Note that we only have to perform this extra traversal if we didn't
        // already discover a root layout in the part of the tree that is
        // unchanged. We also only need to compare the subtree that is not
        // shared. In the common case, this branch is skipped completely.
        !didFindRootLayout && (0, _isnavigatingtonewrootlayout.isNavigatingToNewRootLayout)(oldRouterState, newRouteTree) || // The global Not Found route (app/global-not-found.tsx) is a special
        // case, because it acts like a root layout, but in the router tree, it
        // is rendered in the same position as app/layout.tsx.
        //
        // Any navigation to the global Not Found route should trigger a
        // full-page navigation.
        //
        // TODO: We should probably model this by changing the key of the root
        // segment when this happens. Then the root layout check would work
        // as expected, without a special case.
        newSegment === _segment.NOT_FOUND_SEGMENT_KEY) {
            return null;
        }
        return createCacheNodeOnNavigation(navigatedAt, newRouteTree, newMetadataVaryPath, freshness, seedData, seedHead, seedDynamicStaleAt, parentNeedsDynamicRequest, accumulation);
    }
    const newSlots = newRouteTree.slots;
    const oldRouterStateChildren = oldRouterState[1];
    const seedDataChildren = seedData !== null ? seedData[1] : null;
    // We're currently traversing the part of the tree that was also part of
    // the previous route. If we discover a root layout, then we don't need to
    // trigger an MPA navigation.
    const childDidFindRootLayout = didFindRootLayout || (newRouteTree.prefetchHints & _approutertypes.PrefetchHint.IsRootLayout) !== 0;
    let shouldRefreshDynamicData = false;
    switch(freshness){
        case 0:
        case 2:
        case 1:
        case 5:
            shouldRefreshDynamicData = false;
            break;
        case 3:
        case 4:
            shouldRefreshDynamicData = true;
            break;
        default:
            freshness;
            break;
    }
    // TODO: We're not consistent about how we do this check. Some places
    // check if the segment starts with PAGE_SEGMENT_KEY, but most seem to
    // check if there any any children, which is why I'm doing it here. We
    // should probably encode an empty children set as `null` though. Either
    // way, we should update all the checks to be consistent.
    const isLeafSegment = newSlots === null;
    // Get the data for this segment. Since it was part of the previous route,
    // usually we just clone the data from the old CacheNode. However, during a
    // refresh or a revalidation, there won't be any existing CacheNode. So we
    // may need to consult the prefetch cache, like we would for a new segment.
    let newCacheNode;
    let needsDynamicRequest;
    if (oldCacheNode !== undefined && !shouldRefreshDynamicData && // During a same-page navigation, we always refetch the page segments
    !(isLeafSegment && isSamePageNavigation)) {
        // Reuse the existing CacheNode
        const dropPrefetchRsc = false;
        newCacheNode = reuseSharedCacheNode(dropPrefetchRsc, oldCacheNode);
        needsDynamicRequest = false;
    } else {
        // If this is part of a refresh, ignore the existing CacheNode and create a
        // new one.
        const seedRsc = seedData !== null ? seedData[0] : null;
        const result = createCacheNodeForSegment(navigatedAt, newRouteTree, seedRsc, newMetadataVaryPath, seedHead, freshness, seedDynamicStaleAt);
        newCacheNode = result.cacheNode;
        needsDynamicRequest = result.needsDynamicRequest;
        // Carry forward the old node's scrollRef. This preserves scroll
        // intent when a prior navigation's cache node is replaced by a
        // refresh before the scroll handler has had a chance to fire —
        // e.g. when router.push() and router.refresh() are called in the
        // same startTransition batch.
        if (oldCacheNode !== undefined) {
            newCacheNode.scrollRef = oldCacheNode.scrollRef;
        }
    }
    // During a refresh navigation, there's a special case that happens when
    // entering a "default" slot. The default slot may not be part of the
    // current route; it may have been reused from an older route. If so,
    // we need to fetch its data from the old route's URL rather than current
    // route's URL. Keep track of this as we traverse the tree.
    const maybeRefreshState = newRouteTree.refreshState;
    const refreshState = maybeRefreshState !== undefined && maybeRefreshState !== null ? maybeRefreshState : parentRefreshState;
    // If this segment itself needs to fetch new data from the server, then by
    // definition it is being refreshed. Track its refresh URL so we know which
    // URL to request the data from.
    if (needsDynamicRequest && refreshState !== null) {
        accumulateRefreshUrl(accumulation, refreshState);
    }
    // As we diff the trees, we may sometimes modify (copy-on-write, not mutate)
    // the Route Tree that was returned by the server — for example, in the case
    // of default parallel routes, we preserve the currently active segment. To
    // avoid mutating the original tree, we clone the router state children along
    // the return path.
    let patchedRouterStateChildren = {};
    let taskChildren = null;
    // Most navigations require a request to fetch additional data from the
    // server, either because the data was not already prefetched, or because the
    // target route contains dynamic data that cannot be prefetched.
    //
    // However, if the target route is fully static, and it's already completely
    // loaded into the segment cache, then we can skip the server request.
    //
    // This starts off as `false`, and is set to `true` if any of the child
    // routes requires a dynamic request.
    let childNeedsDynamicRequest = false;
    // As we traverse the children, we'll construct a FlightRouterState that can
    // be sent to the server to request the dynamic data. If it turns out that
    // nothing in the subtree is dynamic (i.e. childNeedsDynamicRequest is false
    // at the end), then this will be discarded.
    // TODO: We can probably optimize the format of this data structure to only
    // include paths that are dynamic. Instead of reusing the
    // FlightRouterState type.
    let dynamicRequestTreeChildren = {};
    let newCacheNodeSlots = null;
    if (newSlots !== null) {
        const oldCacheNodeSlots = oldCacheNode !== undefined ? oldCacheNode.slots : null;
        newCacheNode.slots = newCacheNodeSlots = {};
        taskChildren = new Map();
        for(let parallelRouteKey in newSlots){
            let newRouteTreeChild = newSlots[parallelRouteKey];
            const oldRouterStateChild = oldRouterStateChildren[parallelRouteKey];
            if (oldRouterStateChild === undefined) {
                // This should never happen, but if it does, it suggests a malformed
                // server response. Trigger a full-page navigation.
                return null;
            }
            let seedDataChild = seedDataChildren !== null ? seedDataChildren[parallelRouteKey] : null;
            const oldSegmentChild = oldRouterStateChild[0];
            let newSegmentChild = createSegmentFromRouteTree(newRouteTreeChild);
            let seedHeadChild = seedHead;
            if (// was stashed in the history entry as-is.
            freshness !== 2 && newSegmentChild === _segment.DEFAULT_SEGMENT_KEY && oldSegmentChild !== _segment.DEFAULT_SEGMENT_KEY) {
                // This is a "default" segment. These are never sent by the server during
                // a soft navigation; instead, the client reuses whatever segment was
                // already active in that slot on the previous route.
                newRouteTreeChild = reuseActiveSegmentInDefaultSlot(newRouteTree, parallelRouteKey, oldRootRefreshState, oldRouterStateChild);
                newSegmentChild = createSegmentFromRouteTree(newRouteTreeChild);
                // Since we're switching to a different route tree, these are no
                // longer valid, because they correspond to the outer tree.
                seedDataChild = null;
                seedHeadChild = null;
            }
            const oldCacheNodeChild = oldCacheNodeSlots !== null ? oldCacheNodeSlots[parallelRouteKey] : undefined;
            const taskChild = updateCacheNodeOnNavigation(navigatedAt, oldUrl, oldCacheNodeChild, oldRouterStateChild, newRouteTreeChild, newMetadataVaryPath, freshness, childDidFindRootLayout, seedDataChild ?? null, seedHeadChild, seedDynamicStaleAt, isSamePageNavigation, parentNeedsDynamicRequest || needsDynamicRequest, oldRootRefreshState, refreshState, accumulation);
            if (taskChild === null) {
                // One of the child tasks discovered a change to the root layout.
                // Immediately unwind from this recursive traversal. This will trigger a
                // full-page navigation.
                return null;
            }
            // Recursively propagate up the child tasks.
            taskChildren.set(parallelRouteKey, taskChild);
            newCacheNodeSlots[parallelRouteKey] = taskChild.node;
            // The child tree's route state may be different from the prefetched
            // route sent by the server. We need to clone it as we traverse back up
            // the tree.
            const taskChildRoute = taskChild.route;
            patchedRouterStateChildren[parallelRouteKey] = taskChildRoute;
            const dynamicRequestTreeChild = taskChild.dynamicRequestTree;
            if (dynamicRequestTreeChild !== null) {
                // Something in the child tree is dynamic.
                childNeedsDynamicRequest = true;
                dynamicRequestTreeChildren[parallelRouteKey] = dynamicRequestTreeChild;
            } else {
                dynamicRequestTreeChildren[parallelRouteKey] = taskChildRoute;
            }
        }
    }
    const newFlightRouterState = [
        createSegmentFromRouteTree(newRouteTree),
        patchedRouterStateChildren,
        refreshState !== null ? [
            refreshState.canonicalUrl,
            refreshState.renderedSearch
        ] : null,
        null,
        newRouteTree.prefetchHints
    ];
    return {
        status: needsDynamicRequest ? 0 : 1,
        route: newFlightRouterState,
        node: newCacheNode,
        dynamicRequestTree: createDynamicRequestTree(newFlightRouterState, dynamicRequestTreeChildren, needsDynamicRequest, childNeedsDynamicRequest, parentNeedsDynamicRequest),
        refreshState,
        children: taskChildren
    };
}
/**
 * Assigns a ScrollRef to a new leaf CacheNode so the scroll handler
 * knows to scroll to it after navigation. All leaves in the same
 * navigation share the same ScrollRef — the first segment to scroll
 * consumes it, preventing others from also scrolling.
 *
 * This is only called inside `createCacheNodeOnNavigation`, which only
 * runs when segments diverge from the previous route. So for a refresh
 * where the route structure stays the same, segments match, the update
 * path is taken, and this function is never called — no scroll ref is
 * assigned. A scroll ref is only assigned when the route actually
 * changed (e.g. a redirect, or a dynamic condition on the server that
 * produces a different route).
 *
 * Skipped during hydration (initial render should not scroll) and
 * history traversal (scroll restoration is handled separately).
 */ function accumulateScrollRef(freshness, cacheNode, accumulation) {
    switch(freshness){
        case 0:
        case 5:
        case 3:
        case 4:
            if (accumulation.scrollRef === null) {
                accumulation.scrollRef = {
                    current: true
                };
            }
            cacheNode.scrollRef = accumulation.scrollRef;
            break;
        case 1:
            break;
        case 2:
            break;
        default:
            freshness;
            break;
    }
}
function createCacheNodeOnNavigation(navigatedAt, newRouteTree, newMetadataVaryPath, freshness, seedData, seedHead, seedDynamicStaleAt, parentNeedsDynamicRequest, accumulation) {
    // Same traversal as updateCacheNodeNavigation, but simpler. We switch to this
    // path once we reach the part of the tree that was not in the previous route.
    // We don't need to diff against the old tree, we just need to create a new
    // one. We also don't need to worry about any refresh-related logic.
    //
    // For the most part, this is a subset of updateCacheNodeOnNavigation, so any
    // change that happens in this function likely needs to be applied to that
    // one, too. However there are some places where the behavior intentionally
    // diverges, which is why we keep them separate.
    const newSegment = createSegmentFromRouteTree(newRouteTree);
    const newSlots = newRouteTree.slots;
    const seedDataChildren = seedData !== null ? seedData[1] : null;
    const seedRsc = seedData !== null ? seedData[0] : null;
    const result = createCacheNodeForSegment(navigatedAt, newRouteTree, seedRsc, newMetadataVaryPath, seedHead, freshness, seedDynamicStaleAt);
    const newCacheNode = result.cacheNode;
    const needsDynamicRequest = result.needsDynamicRequest;
    const isLeafSegment = newSlots === null;
    if (isLeafSegment) {
        accumulateScrollRef(freshness, newCacheNode, accumulation);
    }
    let patchedRouterStateChildren = {};
    let taskChildren = null;
    let childNeedsDynamicRequest = false;
    let dynamicRequestTreeChildren = {};
    let newCacheNodeSlots = null;
    if (newSlots !== null) {
        newCacheNode.slots = newCacheNodeSlots = {};
        taskChildren = new Map();
        for(let parallelRouteKey in newSlots){
            const newRouteTreeChild = newSlots[parallelRouteKey];
            const seedDataChild = seedDataChildren !== null ? seedDataChildren[parallelRouteKey] : null;
            const taskChild = createCacheNodeOnNavigation(navigatedAt, newRouteTreeChild, newMetadataVaryPath, freshness, seedDataChild ?? null, seedHead, seedDynamicStaleAt, parentNeedsDynamicRequest || needsDynamicRequest, accumulation);
            taskChildren.set(parallelRouteKey, taskChild);
            newCacheNodeSlots[parallelRouteKey] = taskChild.node;
            const taskChildRoute = taskChild.route;
            patchedRouterStateChildren[parallelRouteKey] = taskChildRoute;
            const dynamicRequestTreeChild = taskChild.dynamicRequestTree;
            if (dynamicRequestTreeChild !== null) {
                childNeedsDynamicRequest = true;
                dynamicRequestTreeChildren[parallelRouteKey] = dynamicRequestTreeChild;
            } else {
                dynamicRequestTreeChildren[parallelRouteKey] = taskChildRoute;
            }
        }
    }
    const newFlightRouterState = [
        newSegment,
        patchedRouterStateChildren,
        null,
        null,
        newRouteTree.prefetchHints
    ];
    return {
        status: needsDynamicRequest ? 0 : 1,
        route: newFlightRouterState,
        node: newCacheNode,
        dynamicRequestTree: createDynamicRequestTree(newFlightRouterState, dynamicRequestTreeChildren, needsDynamicRequest, childNeedsDynamicRequest, parentNeedsDynamicRequest),
        // This route is not part of the current tree, so there's no reason to
        // track the refresh URL.
        refreshState: null,
        children: taskChildren
    };
}
function createSegmentFromRouteTree(newRouteTree) {
    if (newRouteTree.isPage) {
        // In a dynamic server response, the server embeds the search params into
        // the segment key, but in a static one it's omitted. The client handles
        // this inconsistency by adding the search params back right at the end.
        //
        // TODO: The only thing this is used for is to create a cache key for
        // ChildSegmentMap. But we already track the `renderedSearch` everywhere as
        // part of the varyPath. The plan is get rid of ChildSegmentMap and
        // store the page data in a CacheMap using the varyPath, like we do
        // for prefetches. Then we can remove it from the segment key.
        //
        // As an incremental step, we can grab the search params from the varyPath.
        const renderedSearch = (0, _varypath.getRenderedSearchFromVaryPath)(newRouteTree.varyPath);
        if (renderedSearch === null) {
            return _segment.PAGE_SEGMENT_KEY;
        }
        // This is based on equivalent logic in addSearchParamsIfPageSegment, used
        // on the server.
        const stringifiedQuery = JSON.stringify(Object.fromEntries(new URLSearchParams(renderedSearch)));
        return stringifiedQuery !== '{}' ? _segment.PAGE_SEGMENT_KEY + '?' + stringifiedQuery : _segment.PAGE_SEGMENT_KEY;
    }
    return newRouteTree.segment;
}
function patchRouterStateWithNewChildren(baseRouterState, newChildren) {
    const clone = [
        baseRouterState[0],
        newChildren
    ];
    // Based on equivalent logic in apply-router-state-patch-to-tree, but should
    // confirm whether we need to copy all of these fields. Not sure the server
    // ever sends, e.g. the refetch marker.
    if (2 in baseRouterState) {
        clone[2] = baseRouterState[2];
    }
    if (3 in baseRouterState) {
        clone[3] = baseRouterState[3];
    }
    if (4 in baseRouterState) {
        clone[4] = baseRouterState[4];
    }
    return clone;
}
function createDynamicRequestTree(newRouterState, dynamicRequestTreeChildren, needsDynamicRequest, childNeedsDynamicRequest, parentNeedsDynamicRequest) {
    // Create a FlightRouterState that instructs the server how to render the
    // requested segment.
    //
    // Or, if neither this segment nor any of the children require a new data,
    // then we return `null` to skip the request.
    let dynamicRequestTree = null;
    if (needsDynamicRequest) {
        dynamicRequestTree = patchRouterStateWithNewChildren(newRouterState, dynamicRequestTreeChildren);
        // The "refetch" marker is set on the top-most segment that requires new
        // data. We can omit it if a parent was already marked.
        if (!parentNeedsDynamicRequest) {
            dynamicRequestTree[3] = 'refetch';
        }
    } else if (childNeedsDynamicRequest) {
        // This segment does not request new data, but at least one of its
        // children does.
        dynamicRequestTree = patchRouterStateWithNewChildren(newRouterState, dynamicRequestTreeChildren);
    } else {
        dynamicRequestTree = null;
    }
    return dynamicRequestTree;
}
function accumulateRefreshUrl(accumulation, refreshState) {
    // This is a refresh navigation, and we're inside a "default" slot that's
    // not part of the current route; it was reused from an older route. In
    // order to get fresh data for this reused route, we need to issue a
    // separate request using the old route's URL.
    //
    // Track these extra URLs in the accumulated result. Later, we'll construct
    // an appropriate request for each unique URL in the final set. The reason
    // we don't do it immediately here is so we can deduplicate multiple
    // instances of the same URL into a single request. See
    // listenForDynamicRequest for more details.
    const refreshUrl = refreshState.canonicalUrl;
    const separateRefreshUrls = accumulation.separateRefreshUrls;
    if (separateRefreshUrls === null) {
        accumulation.separateRefreshUrls = new Set([
            refreshUrl
        ]);
    } else {
        separateRefreshUrls.add(refreshUrl);
    }
}
function reuseActiveSegmentInDefaultSlot(parentRouteTree, parallelRouteKey, oldRootRefreshState, oldRouterState) {
    // This is a "default" segment. These are never sent by the server during a
    // soft navigation; instead, the client reuses whatever segment was already
    // active in that slot on the previous route. This means if we later need to
    // refresh the segment, it will have to be refetched from the previous route's
    // URL. We store it in the Flight Router State.
    let reusedUrl;
    let reusedRenderedSearch;
    const oldRefreshState = oldRouterState[2];
    if (oldRefreshState !== undefined && oldRefreshState !== null) {
        // This segment was already reused from an even older route. Keep its
        // existing URL and refresh state.
        reusedUrl = oldRefreshState[0];
        reusedRenderedSearch = oldRefreshState[1];
    } else {
        // Since this route didn't already have a refresh state, it must have been
        // reachable from the root of the old route. So we use the refresh state
        // that represents the old route.
        reusedUrl = oldRootRefreshState.canonicalUrl;
        reusedRenderedSearch = oldRootRefreshState.renderedSearch;
    }
    const acc = {
        metadataVaryPath: null
    };
    const reusedRouteTree = (0, _cache.convertReusedFlightRouterStateToRouteTree)(parentRouteTree, parallelRouteKey, oldRouterState, reusedRenderedSearch, acc);
    reusedRouteTree.refreshState = {
        canonicalUrl: reusedUrl,
        renderedSearch: reusedRenderedSearch
    };
    return reusedRouteTree;
}
function reuseSharedCacheNode(dropPrefetchRsc, existingCacheNode) {
    // Clone the CacheNode that was already present in the previous tree.
    // Carry forward the scrollRef so scroll intent from a prior navigation
    // survives tree rebuilds (e.g. push + refresh in the same batch).
    return createCacheNode(existingCacheNode.rsc, dropPrefetchRsc ? null : existingCacheNode.prefetchRsc, existingCacheNode.head, dropPrefetchRsc ? null : existingCacheNode.prefetchHead, existingCacheNode.scrollRef);
}
function createCacheNodeForSegment(now, tree, seedRsc, metadataVaryPath, seedHead, freshness, dynamicStaleAt) {
    // Construct a new CacheNode using data from the BFCache, the client's
    // Segment Cache, or seeded from a server response.
    //
    // If there's a cache miss, or if we only have a partial hit, we'll render
    // the partial state immediately, and spawn a request to the server to fill
    // in the missing data.
    //
    // If the segment is fully cached on the client already, we can omit this
    // segment from the server request.
    //
    // If we already have a dynamic data response associated with this navigation,
    // as in the case of a Server Action-initiated redirect or refresh, we may
    // also be able to use that data without spawning a new request. (This is
    // referred to as the "seed" data.)
    const isPage = tree.isPage;
    // During certain kinds of navigations, we may be able to render from
    // the BFCache.
    switch(freshness){
        case 0:
            {
                // Check BFCache during regular navigations. The entry's staleAt
                // determines whether it's still fresh. This is used when
                // staleTimes.dynamic is configured globally or when a page exports
                // unstable_dynamicStaleTime for per-page control.
                const bfcacheEntry = (0, _bfcache.readFromBFCacheDuringRegularNavigation)(now, tree.varyPath);
                if (bfcacheEntry !== null) {
                    return {
                        cacheNode: createCacheNode(bfcacheEntry.rsc, bfcacheEntry.prefetchRsc, bfcacheEntry.head, bfcacheEntry.prefetchHead),
                        needsDynamicRequest: false
                    };
                }
                break;
            }
        case 1:
            {
                // This is not related to the BFCache but it is a special case.
                //
                // We should never spawn network requests during hydration. We must treat
                // the initial payload as authoritative, because the initial page load is
                // used as a last-ditch mechanism for recovering the app.
                //
                // This is also an important safety check because if this leaks into the
                // server rendering path (which theoretically it never should because the
                // server payload should be consistent), the server would hang because these
                // promises would never resolve.
                //
                // TODO: There is an existing case where the global "not found" boundary
                // triggers this path. But it does render correctly despite that. That's an
                // unusual render path so it's not surprising, but we should look into
                // modeling it in a more consistent way. See also the /_notFound special
                // case in updateCacheNodeOnNavigation.
                const rsc = seedRsc;
                const prefetchRsc = null;
                const head = isPage ? seedHead : null;
                const prefetchHead = null;
                (0, _bfcache.writeToBFCache)(now, tree.varyPath, rsc, prefetchRsc, head, prefetchHead, dynamicStaleAt);
                if (isPage && metadataVaryPath !== null) {
                    (0, _bfcache.writeHeadToBFCache)(now, metadataVaryPath, head, prefetchHead, dynamicStaleAt);
                }
                return {
                    cacheNode: createCacheNode(rsc, prefetchRsc, head, prefetchHead),
                    needsDynamicRequest: false
                };
            }
        case 2:
            const bfcacheEntry = (0, _bfcache.readFromBFCache)(tree.varyPath);
            if (bfcacheEntry !== null) {
                // Only show prefetched data if the dynamic data is still pending. This
                // avoids a flash back to the prefetch state in a case where it's highly
                // likely to have already streamed in.
                //
                // Tehnically, what we're actually checking is whether the dynamic
                // network response was received. But since it's a streaming response,
                // this does not mean that all the dynamic data has fully streamed in.
                // It just means that _some_ of the dynamic data was received. But as a
                // heuristic, we assume that the rest dynamic data will stream in
                // quickly, so it's still better to skip the prefetch state.
                const oldRsc = bfcacheEntry.rsc;
                const oldRscDidResolve = !isDeferredRsc(oldRsc) || oldRsc.status !== 'pending';
                const dropPrefetchRsc = oldRscDidResolve;
                return {
                    cacheNode: createCacheNode(bfcacheEntry.rsc, dropPrefetchRsc ? null : bfcacheEntry.prefetchRsc, bfcacheEntry.head, dropPrefetchRsc ? null : bfcacheEntry.prefetchHead),
                    needsDynamicRequest: false
                };
            }
            break;
        case 3:
        case 4:
        case 5:
            break;
        default:
            freshness;
            break;
    }
    let cachedRsc = null;
    let isCachedRscPartial = true;
    const segmentEntry = (0, _cache.readSegmentCacheEntry)(now, tree.varyPath);
    if (segmentEntry !== null) {
        switch(segmentEntry.status){
            case _cache.EntryStatus.Fulfilled:
                {
                    // Happy path: a cache hit
                    cachedRsc = segmentEntry.rsc;
                    isCachedRscPartial = segmentEntry.isPartial;
                    break;
                }
            case _cache.EntryStatus.Pending:
                {
                    // We haven't received data for this segment yet, but there's already
                    // an in-progress request. Since it's extremely likely to arrive
                    // before the dynamic data response, we might as well use it.
                    const promiseForFulfilledEntry = (0, _cache.waitForSegmentCacheEntry)(segmentEntry);
                    cachedRsc = promiseForFulfilledEntry.then((entry)=>entry !== null ? entry.rsc : null);
                    // Because the request is still pending, we typically don't know yet
                    // whether the response will be partial. We shouldn't skip this segment
                    // during the dynamic navigation request. Otherwise, we might need to
                    // do yet another request to fill in the remaining data, creating
                    // a waterfall.
                    //
                    // The one exception is if this segment is being fetched with via
                    // prefetch={true} (i.e. the "force stale" or "full" strategy). If so,
                    // we can assume the response will be full. This field is set to `false`
                    // for such segments.
                    isCachedRscPartial = segmentEntry.isPartial;
                    break;
                }
            case _cache.EntryStatus.Empty:
            case _cache.EntryStatus.Rejected:
                {
                    break;
                }
            default:
                {
                    segmentEntry;
                    break;
                }
        }
    }
    // Now combine the cached data with the seed data to determine what we can
    // render immediately, versus what needs to stream in later.
    // A partial state to show immediately while we wait for the final data to
    // arrive. If `rsc` is already a complete value (not partial), or if we
    // don't have any useful partial state, this will be `null`.
    let prefetchRsc;
    // The final, resolved segment data. If the data is missing, this will be a
    // promise that resolves to the eventual data. A resolved value of `null`
    // means the data failed to load; the LayoutRouter will suspend indefinitely
    // until the router updates again (refer to finishNavigationTask).
    let rsc;
    let doesSegmentNeedDynamicRequest;
    if (seedRsc !== null) {
        // We already have a dynamic server response for this segment.
        if (isCachedRscPartial) {
            // The seed data may still be streaming in, so it's worth showing the
            // partial cached state in the meantime.
            prefetchRsc = cachedRsc;
            rsc = seedRsc;
        } else {
            // We already have a completely cached segment. Ignore the seed data,
            // which may still be streaming in. This shouldn't happen in the normal
            // case because the client will inform the server which segments are
            // already fully cached, and the server will skip rendering them.
            prefetchRsc = null;
            rsc = cachedRsc;
        }
        doesSegmentNeedDynamicRequest = false;
    } else {
        if (isCachedRscPartial) {
            // The cached data contains dynamic holes, or it's missing entirely. We'll
            // show the partial state immediately (if available), and stream in the
            // final data.
            //
            // Create a pending promise that we can later write to when the
            // data arrives from the server.
            prefetchRsc = cachedRsc;
            rsc = createDeferredRsc();
        } else {
            // The data is fully cached.
            prefetchRsc = null;
            rsc = cachedRsc;
        }
        doesSegmentNeedDynamicRequest = isCachedRscPartial;
    }
    // If this is a page segment, we need to do the same for the head. This
    // follows analogous logic to the segment data above.
    // TODO: We don't need to store the head on the page segment's CacheNode; we
    // can lift it to the main state object. Then we can also delete
    // findHeadCache.
    let prefetchHead = null;
    let head = null;
    let doesHeadNeedDynamicRequest = isPage;
    if (isPage) {
        let cachedHead = null;
        let isCachedHeadPartial = true;
        if (metadataVaryPath !== null) {
            const metadataEntry = (0, _cache.readSegmentCacheEntry)(now, metadataVaryPath);
            if (metadataEntry !== null) {
                switch(metadataEntry.status){
                    case _cache.EntryStatus.Fulfilled:
                        {
                            cachedHead = metadataEntry.rsc;
                            isCachedHeadPartial = metadataEntry.isPartial;
                            break;
                        }
                    case _cache.EntryStatus.Pending:
                        {
                            cachedHead = (0, _cache.waitForSegmentCacheEntry)(metadataEntry).then((entry)=>entry !== null ? entry.rsc : null);
                            isCachedHeadPartial = metadataEntry.isPartial;
                            break;
                        }
                    case _cache.EntryStatus.Empty:
                    case _cache.EntryStatus.Rejected:
                        {
                            break;
                        }
                    default:
                        {
                            metadataEntry;
                            break;
                        }
                }
            }
        }
        if (("TURBOPACK compile-time value", false) && isCachedHeadPartial) {
            // TODO: When optimistic routing is enabled, don't block on waiting for
            // the viewport to resolve. This is a temporary workaround until Vary
            // Params are tracked when rendering the metadata. We'll fix it before
            // this feature is stable. However, it's not a critical issue because 1)
            // it will stream in eventually anyway 2) metadata is wrapped in an
            // internal Suspense boundary, so is always non-blocking; this only
            // affects the viewport node, which is meant to blocking, however... 3)
            // before Segment Cache landed this wasn't always the case, anyway, so
            // it's unlikely that many people are relying on this behavior. Still,
            // will be fixed before stable. It's the very next step in the sequence of
            // work on this project.
            //
            // This line of code works because the App Router treats `null` as
            // "no renderable head available", rather than an empty head. React treats
            // an empty string as empty.
            cachedHead = '';
        }
        if (seedHead !== null) {
            if (isCachedHeadPartial) {
                prefetchHead = cachedHead;
                head = seedHead;
            } else {
                prefetchHead = null;
                head = cachedHead;
            }
            doesHeadNeedDynamicRequest = false;
        } else {
            if (isCachedHeadPartial) {
                prefetchHead = cachedHead;
                head = createDeferredRsc();
            } else {
                prefetchHead = null;
                head = cachedHead;
            }
            doesHeadNeedDynamicRequest = isCachedHeadPartial;
        }
    }
    // Now that we're creating a new segment, write its data to the BFCache. A
    // subsequent back/forward navigation will reuse this same data, until or
    // unless it's cleared by a refresh/revalidation.
    //
    // Skip BFCache writes for optimistic navigations since they are transient
    // and will be replaced by the canonical navigation.
    if (freshness !== 5) {
        (0, _bfcache.writeToBFCache)(now, tree.varyPath, rsc, prefetchRsc, head, prefetchHead, dynamicStaleAt);
        if (isPage && metadataVaryPath !== null) {
            (0, _bfcache.writeHeadToBFCache)(now, metadataVaryPath, head, prefetchHead, dynamicStaleAt);
        }
    }
    return {
        cacheNode: createCacheNode(rsc, prefetchRsc, head, prefetchHead),
        // TODO: We should store this field on the CacheNode itself. I think we can
        // probably unify NavigationTask, CacheNode, and DeferredRsc into a
        // single type. Or at least CacheNode and DeferredRsc.
        needsDynamicRequest: doesSegmentNeedDynamicRequest || doesHeadNeedDynamicRequest
    };
}
function createCacheNode(rsc, prefetchRsc, head, prefetchHead, scrollRef = null) {
    return {
        rsc,
        prefetchRsc,
        head,
        prefetchHead,
        slots: null,
        scrollRef
    };
}
// Represents whether the previuos navigation resulted in a route tree mismatch.
// A mismatch results in a refresh of the page. If there are two successive
// mismatches, we will fall back to an MPA navigation, to prevent a retry loop.
let previousNavigationDidMismatch = false;
function spawnDynamicRequests(task, primaryUrl, nextUrl, freshnessPolicy, accumulation, // prediction. Passed through so it can be marked as having a dynamic rewrite
// if the server returns a different pathname than expected (indicating
// dynamic rewrite behavior that varies by param value).
routeCacheEntry, // server-patch retry logic so it can inherit the intent if the original
// transition hasn't committed yet.
navigateType) {
    const dynamicRequestTree = task.dynamicRequestTree;
    if (dynamicRequestTree === null) {
        // This navigation was fully cached. There are no dynamic requests to spawn.
        previousNavigationDidMismatch = false;
        return;
    }
    // This is intentionally not an async function to discourage the caller from
    // awaiting the result. Any subsequent async operations spawned by this
    // function should result in a separate navigation task, rather than
    // block the original one.
    //
    // In this function we spawn (but do not await) all the network requests that
    // block the navigation, and collect the promises. The next function,
    // `finishNavigationTask`, can await the promises in any order without
    // accidentally introducing a network waterfall.
    const primaryRequestPromise = fetchMissingDynamicData(task, dynamicRequestTree, primaryUrl, nextUrl, freshnessPolicy, routeCacheEntry);
    const separateRefreshUrls = accumulation.separateRefreshUrls;
    let refreshRequestPromises = null;
    if (separateRefreshUrls !== null) {
        // There are multiple URLs that we need to request the data from. This
        // happens when a "default" parallel route slot is present in the tree, and
        // its data cannot be fetched from the current route. We need to split the
        // combined dynamic request tree into separate requests per URL.
        // TODO: Create a scoped dynamic request tree that omits anything that
        // is not relevant to the given URL. Without doing this, the server may
        // sometimes render more data than necessary; this is not a regression
        // compared to the pre-Segment Cache implementation, though, just an
        // optimization we can make in the future.
        // Construct a request tree for each additional refresh URL. This will
        // prune away everything except the parts of the tree that match the
        // given refresh URL.
        refreshRequestPromises = [];
        const canonicalUrl = (0, _createhreffromurl.createHrefFromUrl)(primaryUrl);
        for (const refreshUrl of separateRefreshUrls){
            if (refreshUrl === canonicalUrl) {
                continue;
            }
            // TODO: Create a scoped dynamic request tree that omits anything that
            // is not relevant to the given URL. Without doing this, the server may
            // sometimes render more data than necessary; this is not a regression
            // compared to the pre-Segment Cache implementation, though, just an
            // optimization we can make in the future.
            // const scopedDynamicRequestTree = splitTaskByURL(task, refreshUrl)
            const scopedDynamicRequestTree = dynamicRequestTree;
            if (scopedDynamicRequestTree !== null) {
                refreshRequestPromises.push(fetchMissingDynamicData(task, scopedDynamicRequestTree, new URL(refreshUrl, location.origin), // time the refresh URL was set, not the current Next-Url. Need to
                // start tracking this alongside the refresh URL. In the meantime,
                // if a refresh fails due to a mismatch, it will trigger a
                // hard refresh.
                nextUrl, freshnessPolicy, routeCacheEntry));
            }
        }
    }
    // Further async operations are moved into this separate function to
    // discourage sequential network requests.
    const voidPromise = finishNavigationTask(task, nextUrl, primaryRequestPromise, refreshRequestPromises, routeCacheEntry, navigateType);
    // `finishNavigationTask` is responsible for error handling, so we can attach
    // noop callbacks to this promise.
    voidPromise.then(noop, noop);
}
async function finishNavigationTask(task, nextUrl, primaryRequestPromise, refreshRequestPromises, routeCacheEntry, navigateType) {
    // Wait for all the requests to finish, or for the first one to fail.
    let exitStatus = await waitForRequestsToFinish(primaryRequestPromise, refreshRequestPromises);
    // Once the all the requests have finished, check the tree for any remaining
    // pending tasks. If anything is still pending, it means the server response
    // does not match the client, and we must refresh to get back to a consistent
    // state. We can skip this step if we already detected a mismatch during the
    // first phase; it doesn't matter in that case because we're going to refresh
    // the whole tree regardless.
    if (exitStatus === 0) {
        exitStatus = abortRemainingPendingTasks(task, null, null);
    }
    switch(exitStatus){
        case 0:
            {
                // The task has completely finished. There's no missing data. Exit.
                previousNavigationDidMismatch = false;
                return;
            }
        case 1:
            {
                // Some data failed to finish loading. Trigger a soft retry.
                // TODO: As an extra precaution against soft retry loops, consider
                // tracking whether a navigation was itself triggered by a retry. If two
                // happen in a row, fall back to a hard retry.
                const isHardRetry = false;
                const primaryRequestResult = await primaryRequestPromise;
                dispatchRetryDueToTreeMismatch(isHardRetry, primaryRequestResult.url, nextUrl, primaryRequestResult.seed, task.route, routeCacheEntry, navigateType);
                return;
            }
        case 2:
            {
                // Some data failed to finish loading in a non-recoverable way, such as a
                // network error. Trigger an MPA navigation.
                //
                // Hard navigating/refreshing is how we prevent an infinite retry loop
                // caused by a network error — when the network fails, we fall back to the
                // browser behavior for offline navigations. In the future, Next.js may
                // introduce its own custom handling of offline navigations, but that
                // doesn't exist yet.
                const isHardRetry = true;
                const primaryRequestResult = await primaryRequestPromise;
                dispatchRetryDueToTreeMismatch(isHardRetry, primaryRequestResult.url, nextUrl, primaryRequestResult.seed, task.route, routeCacheEntry, navigateType);
                return;
            }
        default:
            {
                return exitStatus;
            }
    }
}
function waitForRequestsToFinish(primaryRequestPromise, refreshRequestPromises) {
    // Custom async combinator logic. This could be replaced by Promise.any but
    // we don't assume that's available.
    //
    // Each promise resolves once the server responsds and the data is written
    // into the CacheNode tree. Resolve the combined promise once all the
    // requests finish.
    //
    // Or, resolve as soon as one of the requests fails, without waiting for the
    // others to finish.
    return new Promise((resolve)=>{
        const onFulfill = (result)=>{
            if (result.exitStatus === 0) {
                remainingCount--;
                if (remainingCount === 0) {
                    // All the requests finished successfully.
                    resolve(0);
                }
            } else {
                // One of the requests failed. Exit with a failing status.
                // NOTE: It's possible for one of the requests to fail with SoftRetry
                // and a later one to fail with HardRetry. In this case, we choose to
                // retry immediately, rather than delay the retry until all the requests
                // finish. If it fails again, we will hard retry on the next
                // attempt, anyway.
                resolve(result.exitStatus);
            }
        };
        // onReject shouldn't ever be called because fetchMissingDynamicData's
        // entire body is wrapped in a try/catch. This is just defensive.
        const onReject = ()=>resolve(2);
        // Attach the listeners to the promises.
        let remainingCount = 1;
        primaryRequestPromise.then(onFulfill, onReject);
        if (refreshRequestPromises !== null) {
            remainingCount += refreshRequestPromises.length;
            refreshRequestPromises.forEach((refreshRequestPromise)=>refreshRequestPromise.then(onFulfill, onReject));
        }
    });
}
function dispatchRetryDueToTreeMismatch(isHardRetry, retryUrl, retryNextUrl, seed, baseTree, // prediction. If the navigation results in a mismatch, we mark it as having
// a dynamic rewrite so future predictions bail out.
routeCacheEntry, originalNavigateType) {
    // If the navigation used a route prediction, mark it as having a dynamic
    // rewrite since it resulted in a mismatch.
    if (routeCacheEntry !== null) {
        (0, _cache.markRouteEntryAsDynamicRewrite)(routeCacheEntry);
    } else if (seed !== null) {
        // Even without a direct reference to the route cache entry, we can still
        // mark the route as having a dynamic rewrite by traversing the known route
        // tree. This handles cases where the navigation didn't originate from a
        // route prediction, but still needs to mark the pattern.
        const metadataVaryPath = seed.metadataVaryPath;
        if (metadataVaryPath !== null) {
            const now = Date.now();
            (0, _optimisticroutes.discoverKnownRoute)(now, retryUrl.pathname, retryNextUrl, null, seed.routeTree, metadataVaryPath, false, (0, _createhreffromurl.createHrefFromUrl)(retryUrl), false, true // hasDynamicRewrite
            );
        }
    }
    // Invalidate all route cache entries. Other entries may have been derived
    // from the template before we knew it had a dynamic rewrite. This also
    // triggers re-prefetching of visible links.
    (0, _cache.invalidateRouteCacheEntries)(retryNextUrl, baseTree);
    // If this is the second time in a row that a navigation resulted in a
    // mismatch, fall back to a hard (MPA) refresh.
    isHardRetry = isHardRetry || previousNavigationDidMismatch;
    previousNavigationDidMismatch = true;
    // If the original navigation hasn't committed to the browser history yet
    // (the transition suspended before React committed), inherit its push/replace
    // intent. Otherwise, the pushState already ran, so use 'replace' to avoid
    // creating a duplicate history entry.
    //
    // This works because React entangles the retry's state update with the
    // original pending transition — they commit together as a single batch,
    // so the navigate type from the retry is what HistoryUpdater ultimately sees.
    //
    // TODO: Ideally this check would happen right before we schedule the React
    // update (i.e., closer to where the action is dispatched into the queue),
    // not here where the action is constructed. But the current action queue
    // doesn't provide a natural place for that. Revisit when we refactor the
    // action queue into a more reactive navigation model.
    const lastCommitted = (0, _committedstate.getLastCommittedTree)();
    const retryNavigateType = lastCommitted !== null && baseTree !== lastCommitted ? originalNavigateType : 'replace';
    const retryAction = {
        type: _routerreducertypes.ACTION_SERVER_PATCH,
        previousTree: baseTree,
        url: retryUrl,
        nextUrl: retryNextUrl,
        seed,
        mpa: isHardRetry,
        navigateType: retryNavigateType
    };
    (0, _useactionqueue.dispatchAppRouterAction)(retryAction);
}
async function fetchMissingDynamicData(task, dynamicRequestTree, url, nextUrl, freshnessPolicy, routeCacheEntry) {
    try {
        const result = await (0, _fetchserverresponse.fetchServerResponse)(url, {
            flightRouterState: dynamicRequestTree,
            nextUrl,
            isHmrRefresh: freshnessPolicy === 4
        });
        if (typeof result === 'string') {
            // fetchServerResponse will return an href to indicate that the SPA
            // navigation failed. For example, if the server triggered a hard
            // redirect, or the fetch request errored. Initiate an MPA navigation
            // to the given href.
            return {
                exitStatus: 2,
                url: new URL(result, location.origin),
                seed: null
            };
        }
        const now = Date.now();
        const seed = (0, _navigation.convertServerPatchToFullTree)(now, task.route, result.flightData, result.renderedSearch, result.dynamicStaleTime);
        // If the navigation lock is active, wait for it to be released before
        // writing the dynamic data. This allows tests to assert on the prefetched
        // UI state.
        if ("TURBOPACK compile-time truthy", 1) {
            await waitForNavigationLock();
        }
        if (routeCacheEntry !== null && result.staticStageData !== null) {
            const { response: staticStageResponse, isResponsePartial } = result.staticStageData;
            (0, _cache.getStaleAt)(now, staticStageResponse.s).then((staleAt)=>{
                const buildId = result.responseHeaders.get(_constants.NEXT_NAV_DEPLOYMENT_ID_HEADER) ?? staticStageResponse.b;
                (0, _cache.writeStaticStageResponseIntoCache)(now, staticStageResponse.f, buildId, staticStageResponse.h, staleAt, dynamicRequestTree, result.renderedSearch, isResponsePartial);
            }).catch(()=>{
            // The static stage processing failed. Not fatal — the navigation
            // completed normally, we just won't write into the cache.
            });
        }
        if (routeCacheEntry !== null && result.runtimePrefetchStream !== null) {
            (0, _cache.processRuntimePrefetchStream)(now, result.runtimePrefetchStream, dynamicRequestTree, result.renderedSearch).then((processed)=>{
                if (processed !== null) {
                    (0, _cache.writeDynamicRenderResponseIntoCache)(now, _types.FetchStrategy.PPRRuntime, processed.flightDatas, processed.buildId, processed.isResponsePartial, processed.headVaryParams, processed.staleAt, processed.navigationSeed, null);
                }
            }).catch(()=>{
            // The runtime prefetch cache write failed. Not fatal — the
            // navigation completed normally, we just won't cache runtime data.
            });
        }
        // result.dynamicStaleTime is in seconds (from the server's `d` field).
        // Convert to an absolute timestamp using the centralized helper.
        const dynamicStaleAt = (0, _bfcache.computeDynamicStaleAt)(now, result.dynamicStaleTime);
        const didReceiveUnknownParallelRoute = writeDynamicDataIntoNavigationTask(task, seed.routeTree, seed.data, seed.head, dynamicStaleAt, result.debugInfo);
        return {
            exitStatus: didReceiveUnknownParallelRoute ? 1 : 0,
            url: new URL(result.canonicalUrl, location.origin),
            seed
        };
    } catch  {
        // This shouldn't happen because fetchServerResponse's entire body is
        // wrapped in a try/catch. If it does, though, it implies the server failed
        // to respond with any tree at all. So we must fall back to a hard retry.
        return {
            exitStatus: 2,
            url: url,
            seed: null
        };
    }
}
function writeDynamicDataIntoNavigationTask(task, serverRouteTree, dynamicData, dynamicHead, dynamicStaleAt, debugInfo) {
    if (task.status === 0 && dynamicData !== null) {
        task.status = 1;
        finishPendingCacheNode(task.node, dynamicData, dynamicHead, debugInfo);
        // Update the BFCache entry's staleAt for this segment with the value
        // from the dynamic response. This applies the per-page
        // unstable_dynamicStaleTime if set, or the default DYNAMIC_STALETIME_MS.
        // We only update segments that received dynamic data — static segments
        // are unaffected.
        (0, _bfcache.updateBFCacheEntryStaleAt)(serverRouteTree.varyPath, dynamicStaleAt);
    }
    const taskChildren = task.children;
    const serverChildren = serverRouteTree.slots;
    const dynamicDataChildren = dynamicData !== null ? dynamicData[1] : null;
    // Detect whether the server sends a parallel route slot that the client
    // doesn't know about.
    let didReceiveUnknownParallelRoute = false;
    if (taskChildren !== null) {
        if (serverChildren !== null) {
            for(const parallelRouteKey in serverChildren){
                const serverRouteTreeChild = serverChildren[parallelRouteKey];
                const dynamicDataChild = dynamicDataChildren !== null ? dynamicDataChildren[parallelRouteKey] : null;
                const taskChild = taskChildren.get(parallelRouteKey);
                if (taskChild === undefined) {
                    // The server sent a child segment that the client doesn't know about.
                    //
                    // When we receive an unknown parallel route, we must consider it a
                    // mismatch. This is unlike the case where the segment itself
                    // mismatches, because multiple routes can be active simultaneously.
                    // But a given layout should never have a mismatching set of
                    // child slots.
                    //
                    // Theoretically, this should only happen in development during an HMR
                    // refresh, because the set of parallel routes for a layout does not
                    // change over the lifetime of a build/deployment. In production, we
                    // should have already mismatched on either the build id or the segment
                    // path. But as an extra precaution, we validate in prod, too.
                    didReceiveUnknownParallelRoute = true;
                } else {
                    const taskSegment = taskChild.route[0];
                    const serverSegment = createSegmentFromRouteTree(serverRouteTreeChild);
                    if ((0, _matchsegments.matchSegment)(serverSegment, taskSegment) && dynamicDataChild !== null && dynamicDataChild !== undefined) {
                        // Found a match for this task. Keep traversing down the task tree.
                        const childDidReceiveUnknownParallelRoute = writeDynamicDataIntoNavigationTask(taskChild, serverRouteTreeChild, dynamicDataChild, dynamicHead, dynamicStaleAt, debugInfo);
                        if (childDidReceiveUnknownParallelRoute) {
                            didReceiveUnknownParallelRoute = true;
                        }
                    }
                }
            }
        } else {
            if (serverChildren !== null) {
                // The server sent a child segment that the client doesn't know about.
                didReceiveUnknownParallelRoute = true;
            }
        }
    }
    return didReceiveUnknownParallelRoute;
}
function finishPendingCacheNode(cacheNode, dynamicData, dynamicHead, debugInfo) {
    // Writes a dynamic response into an existing Cache Node tree. This does _not_
    // create a new tree, it updates the existing tree in-place. So it must follow
    // the Suspense rules of cache safety — it can resolve pending promises, but
    // it cannot overwrite existing data. It can add segments to the tree (because
    // a missing segment will cause the layout router to suspend).
    // but it cannot delete them.
    //
    // We must resolve every promise in the tree, or else it will suspend
    // indefinitely. If we did not receive data for a segment, we will resolve its
    // data promise to `null` to trigger a lazy fetch during render.
    // Use the dynamic data from the server to fulfill the deferred RSC promise
    // on the Cache Node.
    const rsc = cacheNode.rsc;
    const dynamicSegmentData = dynamicData[0];
    if (dynamicSegmentData === null) {
        // This is an empty CacheNode; this particular server request did not
        // render this segment. There may be a separate pending request that will,
        // though, so we won't abort the task until all pending requests finish.
        return;
    }
    if (rsc === null) {
        // This is a lazy cache node. We can overwrite it. This is only safe
        // because we know that the LayoutRouter suspends if `rsc` is `null`.
        cacheNode.rsc = dynamicSegmentData;
    } else if (isDeferredRsc(rsc)) {
        // This is a deferred RSC promise. We can fulfill it with the data we just
        // received from the server. If it was already resolved by a different
        // navigation, then this does nothing because we can't overwrite data.
        rsc.resolve(dynamicSegmentData, debugInfo);
    } else {
    // This is not a deferred RSC promise, nor is it empty, so it must have
    // been populated by a different navigation. We must not overwrite it.
    }
    // Check if this is a leaf segment. If so, it will have a `head` property with
    // a pending promise that needs to be resolved with the dynamic head from
    // the server.
    const head = cacheNode.head;
    if (isDeferredRsc(head)) {
        head.resolve(dynamicHead, debugInfo);
    }
}
function abortRemainingPendingTasks(task, error, debugInfo) {
    let exitStatus;
    if (task.status === 0) {
        // The data for this segment is still missing.
        task.status = 2;
        abortPendingCacheNode(task.node, error, debugInfo);
        // If the server failed to fulfill the data for this segment, it implies
        // that the route tree received from the server mismatched the tree that
        // was previously prefetched.
        //
        // In an app with fully static routes and no proxy-driven redirects or
        // rewrites, this should never happen, because the route for a URL would
        // always be the same across multiple requests. So, this implies that some
        // runtime routing condition changed, likely in a proxy, without being
        // pushed to the client.
        //
        // When this happens, we treat this the same as a refresh(). The entire
        // tree will be re-rendered from the root.
        if (task.refreshState === null) {
            // Trigger a "soft" refresh. Essentially the same as calling `refresh()`
            // in a Server Action.
            exitStatus = 1;
        } else {
            // The mismatch was discovered inside an inactive parallel route. This
            // implies the inactive parallel route is no longer reachable at the URL
            // that originally rendered it. Fall back to an MPA refresh.
            // TODO: An alternative could be to trigger a soft refresh but to _not_
            // re-use the inactive parallel routes this time. Similar to what would
            // happen if were to do a hard refrehs, but without the HTML page.
            exitStatus = 2;
        }
    } else {
        // This segment finished. (An error here is treated as Done because they are
        // surfaced to the application during render.)
        exitStatus = 0;
    }
    const taskChildren = task.children;
    if (taskChildren !== null) {
        for (const [, taskChild] of taskChildren){
            const childExitStatus = abortRemainingPendingTasks(taskChild, error, debugInfo);
            // Propagate the exit status up the tree. The statuses are ordered by
            // their precedence.
            if (childExitStatus > exitStatus) {
                exitStatus = childExitStatus;
            }
        }
    }
    return exitStatus;
}
function abortPendingCacheNode(cacheNode, error, debugInfo) {
    const rsc = cacheNode.rsc;
    if (isDeferredRsc(rsc)) {
        if (error === null) {
            // This will trigger a lazy fetch during render.
            rsc.resolve(null, debugInfo);
        } else {
            // This will trigger an error during rendering.
            rsc.reject(error, debugInfo);
        }
    }
    // Check if this is a leaf segment. If so, it will have a `head` property with
    // a pending promise that needs to be resolved. If an error was provided, we
    // will not resolve it with an error, since this is rendered at the root of
    // the app. We want the segment to error, not the entire app.
    const head = cacheNode.head;
    if (isDeferredRsc(head)) {
        head.resolve(null, debugInfo);
    }
}
const DEFERRED = Symbol();
function isDeferredRsc(value) {
    return value && typeof value === 'object' && value.tag === DEFERRED;
}
function createDeferredRsc() {
    // Create an unresolved promise that represents data derived from a Flight
    // response. The promise will be resolved later as soon as we start receiving
    // data from the server, i.e. as soon as the Flight client decodes and returns
    // the top-level response object.
    // The `_debugInfo` field contains profiling information. Promises that are
    // created by Flight already have this info added by React; for any derived
    // promise created by the router, we need to transfer the Flight debug info
    // onto the derived promise.
    //
    // The debug info represents the latency between the start of the navigation
    // and the start of rendering. (It does not represent the time it takes for
    // whole stream to finish.)
    const debugInfo = [];
    let resolve;
    let reject;
    const pendingRsc = new Promise((res, rej)=>{
        resolve = res;
        reject = rej;
    });
    pendingRsc.status = 'pending';
    pendingRsc.resolve = (value, responseDebugInfo)=>{
        if (pendingRsc.status === 'pending') {
            const fulfilledRsc = pendingRsc;
            fulfilledRsc.status = 'fulfilled';
            fulfilledRsc.value = value;
            if (responseDebugInfo !== null) {
                // Transfer the debug info to the derived promise.
                debugInfo.push.apply(debugInfo, responseDebugInfo);
            }
            resolve(value);
        }
    };
    pendingRsc.reject = (error, responseDebugInfo)=>{
        if (pendingRsc.status === 'pending') {
            const rejectedRsc = pendingRsc;
            rejectedRsc.status = 'rejected';
            rejectedRsc.reason = error;
            if (responseDebugInfo !== null) {
                // Transfer the debug info to the derived promise.
                debugInfo.push.apply(debugInfo, responseDebugInfo);
            }
            reject(error);
        }
    };
    pendingRsc.tag = DEFERRED;
    pendingRsc._debugInfo = debugInfo;
    return pendingRsc;
}
/**
 * Helper for the Instant Navigation Testing API. Waits for the navigation lock
 * to be released before returning. The network request has already completed by
 * the time this is called, so this only delays writing the dynamic data.
 *
 * Not exposed in production builds by default.
 */ async function waitForNavigationLock() {
    if ("TURBOPACK compile-time truthy", 1) {
        const { waitForNavigationLockIfActive } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/navigation-testing-lock.js [app-client] (ecmascript)");
        await waitForNavigationLockIfActive();
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/compute-changed-path.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    computeChangedPath: null,
    extractPathFromFlightRouterState: null,
    extractSourcePageFromFlightRouterState: null,
    getSelectedParams: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    computeChangedPath: function() {
        return computeChangedPath;
    },
    extractPathFromFlightRouterState: function() {
        return extractPathFromFlightRouterState;
    },
    extractSourcePageFromFlightRouterState: function() {
        return extractSourcePageFromFlightRouterState;
    },
    getSelectedParams: function() {
        return getSelectedParams;
    }
});
const _interceptionroutes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/interception-routes.js [app-client] (ecmascript)");
const _segment = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/segment.js [app-client] (ecmascript)");
const _matchsegments = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/match-segments.js [app-client] (ecmascript)");
const removeLeadingSlash = (segment)=>{
    return segment[0] === '/' ? segment.slice(1) : segment;
};
const segmentToPathname = (segment)=>{
    if (typeof segment === 'string') {
        // 'children' is not a valid path -- it's technically a parallel route that corresponds with the current segment's page
        // if we don't skip it, then the computed pathname might be something like `/children` which doesn't make sense.
        if (segment === 'children') return '';
        return segment;
    }
    return segment[1];
};
const segmentToSourcePagePathname = (segment)=>{
    if (typeof segment === 'string') {
        if (segment === 'children') return '';
        if (segment.startsWith(_segment.PAGE_SEGMENT_KEY)) return 'page';
        return segment;
    }
    const [paramName, , dynamicParamType] = segment;
    switch(dynamicParamType){
        case 'c':
            return `[...${paramName}]`;
        case 'ci(..)(..)':
            return `(..)(..)[...${paramName}]`;
        case 'ci(.)':
            return `(.)[...${paramName}]`;
        case 'ci(..)':
            return `(..)[...${paramName}]`;
        case 'ci(...)':
            return `(...)[...${paramName}]`;
        case 'oc':
            return `[[...${paramName}]]`;
        case 'd':
            return `[${paramName}]`;
        case 'di(..)(..)':
            return `(..)(..)[${paramName}]`;
        case 'di(.)':
            return `(.)[${paramName}]`;
        case 'di(..)':
            return `(..)[${paramName}]`;
        case 'di(...)':
            return `(...)[${paramName}]`;
        default:
            dynamicParamType;
            return `[${paramName}]`;
    }
};
function normalizeSegments(segments) {
    return segments.reduce((acc, segment)=>{
        segment = removeLeadingSlash(segment);
        if (segment === '' || (0, _segment.isGroupSegment)(segment)) {
            return acc;
        }
        return `${acc}/${segment}`;
    }, '') || '/';
}
function extractPathFromFlightRouterState(flightRouterState) {
    const segment = Array.isArray(flightRouterState[0]) ? flightRouterState[0][1] : flightRouterState[0];
    if (segment === _segment.DEFAULT_SEGMENT_KEY || _interceptionroutes.INTERCEPTION_ROUTE_MARKERS.some((m)=>segment.startsWith(m))) return undefined;
    if (segment.startsWith(_segment.PAGE_SEGMENT_KEY)) return '';
    const segments = [
        segmentToPathname(segment)
    ];
    const parallelRoutes = flightRouterState[1] ?? {};
    const childrenPath = parallelRoutes.children ? extractPathFromFlightRouterState(parallelRoutes.children) : undefined;
    if (childrenPath !== undefined) {
        segments.push(childrenPath);
    } else {
        for (const [key, value] of Object.entries(parallelRoutes)){
            if (key === 'children') continue;
            const childPath = extractPathFromFlightRouterState(value);
            if (childPath !== undefined) {
                segments.push(childPath);
            }
        }
    }
    return normalizeSegments(segments);
}
function extractSourcePageSegmentsFromFlightRouterState(flightRouterState) {
    const segment = segmentToSourcePagePathname(flightRouterState[0]);
    if (segment === _segment.DEFAULT_SEGMENT_KEY) {
        return undefined;
    }
    if (segment === 'page') {
        return [
            segment
        ];
    }
    const parallelRoutes = flightRouterState[1] ?? {};
    const childrenPath = parallelRoutes.children ? extractSourcePageSegmentsFromFlightRouterState(parallelRoutes.children) : undefined;
    if (childrenPath !== undefined) {
        return segment === '' ? childrenPath : [
            removeLeadingSlash(segment),
            ...childrenPath
        ];
    }
    for (const [key, value] of Object.entries(parallelRoutes)){
        if (key === 'children') continue;
        const childPath = extractSourcePageSegmentsFromFlightRouterState(value);
        if (childPath !== undefined) {
            return segment === '' ? childPath : [
                removeLeadingSlash(segment),
                ...childPath
            ];
        }
    }
    return undefined;
}
function extractSourcePageFromFlightRouterState(flightRouterState) {
    const sourcePageSegments = extractSourcePageSegmentsFromFlightRouterState(flightRouterState);
    return sourcePageSegments ? `/${sourcePageSegments.join('/')}` : undefined;
}
function computeChangedPathImpl(treeA, treeB) {
    const [segmentA, parallelRoutesA] = treeA;
    const [segmentB, parallelRoutesB] = treeB;
    const normalizedSegmentA = segmentToPathname(segmentA);
    const normalizedSegmentB = segmentToPathname(segmentB);
    if (_interceptionroutes.INTERCEPTION_ROUTE_MARKERS.some((m)=>normalizedSegmentA.startsWith(m) || normalizedSegmentB.startsWith(m))) {
        return '';
    }
    if (!(0, _matchsegments.matchSegment)(segmentA, segmentB)) {
        // once we find where the tree changed, we compute the rest of the path by traversing the tree
        return extractPathFromFlightRouterState(treeB) ?? '';
    }
    for(const parallelRouterKey in parallelRoutesA){
        if (parallelRoutesB[parallelRouterKey]) {
            const changedPath = computeChangedPathImpl(parallelRoutesA[parallelRouterKey], parallelRoutesB[parallelRouterKey]);
            if (changedPath !== null) {
                return `${segmentToPathname(segmentB)}/${changedPath}`;
            }
        }
    }
    return null;
}
function computeChangedPath(treeA, treeB) {
    const changedPath = computeChangedPathImpl(treeA, treeB);
    if (changedPath == null || changedPath === '/') {
        return changedPath;
    }
    // lightweight normalization to remove route groups
    return normalizeSegments(changedPath.split('/'));
}
function getSelectedParams(currentTree, params = {}) {
    const parallelRoutes = currentTree[1];
    for (const parallelRoute of Object.values(parallelRoutes)){
        const segment = parallelRoute[0];
        const isDynamicParameter = Array.isArray(segment);
        const segmentValue = isDynamicParameter ? segment[1] : segment;
        if (!segmentValue || segmentValue.startsWith(_segment.PAGE_SEGMENT_KEY)) continue;
        // Ensure catchAll and optional catchall are turned into an array
        const isCatchAll = isDynamicParameter && (segment[2] === 'c' || segment[2] === 'oc');
        if (isCatchAll) {
            params[segment[0]] = segment[1].split('/');
        } else if (isDynamicParameter) {
            params[segment[0]] = segment[1];
        }
        params = getSelectedParams(parallelRoute, params);
    }
    return params;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/lib/javascript-url.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/navigation.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    completeHardNavigation: null,
    completeSoftNavigation: null,
    completeTraverseNavigation: null,
    convertServerPatchToFullTree: null,
    navigate: null,
    navigateToKnownRoute: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    completeHardNavigation: function() {
        return completeHardNavigation;
    },
    completeSoftNavigation: function() {
        return completeSoftNavigation;
    },
    completeTraverseNavigation: function() {
        return completeTraverseNavigation;
    },
    convertServerPatchToFullTree: function() {
        return convertServerPatchToFullTree;
    },
    navigate: function() {
        return navigate;
    },
    navigateToKnownRoute: function() {
        return navigateToKnownRoute;
    }
});
const _fetchserverresponse = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/fetch-server-response.js [app-client] (ecmascript)");
const _pprnavigations = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/ppr-navigations.js [app-client] (ecmascript)");
const _createhreffromurl = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/create-href-from-url.js [app-client] (ecmascript)");
const _constants = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/constants.js [app-client] (ecmascript)");
const _cache = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache.js [app-client] (ecmascript)");
const _optimisticroutes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/optimistic-routes.js [app-client] (ecmascript)");
const _cachekey = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache-key.js [app-client] (ecmascript)");
const _scheduler = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/scheduler.js [app-client] (ecmascript)");
const _types = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/types.js [app-client] (ecmascript)");
const _links = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/links.js [app-client] (ecmascript)");
const _routerreducertypes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/router-reducer-types.js [app-client] (ecmascript)");
const _computechangedpath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/compute-changed-path.js [app-client] (ecmascript)");
const _javascripturl = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/lib/javascript-url.js [app-client] (ecmascript)");
const _bfcache = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/bfcache.js [app-client] (ecmascript)");
function navigate(state, url, currentUrl, currentRenderedSearch, currentCacheNode, currentFlightRouterState, nextUrl, freshnessPolicy, scrollBehavior, navigateType) {
    // Instant Navigation Testing API: when the lock is active, ensure a
    // prefetch task has been initiated before proceeding with the navigation.
    // This guarantees that segment data requests are at least pending, even
    // for routes that already have a cached route tree. Without this, the
    // static shell might be incomplete because some segments were never
    // requested.
    if ("TURBOPACK compile-time truthy", 1) {
        const { isNavigationLocked } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/navigation-testing-lock.js [app-client] (ecmascript)");
        if (isNavigationLocked()) {
            return ensurePrefetchThenNavigate(state, url, currentUrl, currentRenderedSearch, currentCacheNode, currentFlightRouterState, nextUrl, freshnessPolicy, scrollBehavior, navigateType);
        }
    }
    return navigateImpl(state, url, currentUrl, currentRenderedSearch, currentCacheNode, currentFlightRouterState, nextUrl, freshnessPolicy, scrollBehavior, navigateType);
}
function navigateImpl(state, url, currentUrl, currentRenderedSearch, currentCacheNode, currentFlightRouterState, nextUrl, freshnessPolicy, scrollBehavior, navigateType) {
    const now = Date.now();
    const href = url.href;
    const cacheKey = (0, _cachekey.createCacheKey)(href, nextUrl);
    const route = (0, _cache.readRouteCacheEntry)(now, cacheKey);
    if (route !== null && route.status === _cache.EntryStatus.Fulfilled) {
        // We have a matching prefetch.
        return navigateUsingPrefetchedRouteTree(now, state, url, currentUrl, currentRenderedSearch, nextUrl, currentCacheNode, currentFlightRouterState, freshnessPolicy, scrollBehavior, navigateType, route);
    }
    // There was no matching route tree in the cache. Let's see if we can
    // construct an "optimistic" route tree using the deprecated search-params
    // based matching. This is only used when the new optimisticRouting flag is
    // disabled.
    //
    // Do not construct an optimistic route tree if there was a cache hit, but
    // the entry has a rejected status, since it may have been rejected due to a
    // rewrite or redirect based on the search params.
    //
    // TODO: There are multiple reasons a prefetch might be rejected; we should
    // track them explicitly and choose what to do here based on that.
    if ("TURBOPACK compile-time truthy", 1) {
        if (route === null || route.status !== _cache.EntryStatus.Rejected) {
            const optimisticRoute = (0, _cache.deprecated_requestOptimisticRouteCacheEntry)(now, url, nextUrl);
            if (optimisticRoute !== null) {
                // We have an optimistic route tree. Proceed with the normal flow.
                return navigateUsingPrefetchedRouteTree(now, state, url, currentUrl, currentRenderedSearch, nextUrl, currentCacheNode, currentFlightRouterState, freshnessPolicy, scrollBehavior, navigateType, optimisticRoute);
            }
        }
    }
    // There's no matching prefetch for this route in the cache. We must lazily
    // fetch it from the server before we can perform the navigation.
    //
    // TODO: If this is a gesture navigation, instead of performing a
    // dynamic request, we should do a runtime prefetch.
    return navigateToUnknownRoute(now, state, url, currentUrl, currentRenderedSearch, nextUrl, currentCacheNode, currentFlightRouterState, freshnessPolicy, scrollBehavior, navigateType).catch(()=>{
        // If the navigation fails, return the current state
        return state;
    });
}
function navigateToKnownRoute(now, state, url, canonicalUrl, navigationSeed, currentUrl, currentRenderedSearch, currentCacheNode, currentFlightRouterState, freshnessPolicy, nextUrl, scrollBehavior, navigateType, debugInfo, // prediction. Passed through so it can be marked as having a dynamic rewrite
// if the server returns a different pathname (indicating dynamic rewrite
// behavior).
//
// When null, the navigation did not use route prediction - either because
// the route was already fully cached, or it's a navigation that doesn't
// involve prediction (refresh, history traversal, server action, etc.).
// In these cases, if a mismatch occurs, we still mark the route as having a
// dynamic rewrite by traversing the known route tree (see
// dispatchRetryDueToTreeMismatch).
routeCacheEntry) {
    // A version of navigate() that accepts the target route tree as an argument
    // rather than reading it from the prefetch cache.
    const accumulation = {
        separateRefreshUrls: null,
        scrollRef: null
    };
    // We special case navigations to the exact same URL as the current location.
    // It's a common UI pattern for apps to refresh when you click a link to the
    // current page. So when this happens, we refresh the dynamic data in the page
    // segments.
    //
    // Note that this does not apply if the any part of the hash or search query
    // has changed. This might feel a bit weird but it makes more sense when you
    // consider that the way to trigger this behavior is to click the same link
    // multiple times.
    //
    // TODO: We should probably refresh the *entire* route when this case occurs,
    // not just the page segments. Essentially treating it the same as a refresh()
    // triggered by an action, which is the more explicit way of modeling the UI
    // pattern described above.
    //
    // Also note that this only refreshes the dynamic data, not static/ cached
    // data. If the page segment is fully static and prefetched, the request is
    // skipped. (This is also how refresh() works.)
    const isSamePageNavigation = url.href === currentUrl.href;
    const task = (0, _pprnavigations.startPPRNavigation)(now, currentUrl, currentRenderedSearch, currentCacheNode, currentFlightRouterState, navigationSeed.routeTree, navigationSeed.metadataVaryPath, freshnessPolicy, navigationSeed.data, navigationSeed.head, navigationSeed.dynamicStaleAt, isSamePageNavigation, accumulation);
    if (task !== null) {
        if (freshnessPolicy !== _pprnavigations.FreshnessPolicy.Gesture) {
            (0, _pprnavigations.spawnDynamicRequests)(task, url, nextUrl, freshnessPolicy, accumulation, routeCacheEntry, navigateType);
        }
        return completeSoftNavigation(state, url, nextUrl, task.route, task.node, navigationSeed.renderedSearch, canonicalUrl, navigateType, scrollBehavior, accumulation.scrollRef, debugInfo);
    }
    // Could not perform a SPA navigation. Revert to a full-page (MPA) navigation.
    return completeHardNavigation(state, url, navigateType);
}
function navigateUsingPrefetchedRouteTree(now, state, url, currentUrl, currentRenderedSearch, nextUrl, currentCacheNode, currentFlightRouterState, freshnessPolicy, scrollBehavior, navigateType, route) {
    const routeTree = route.tree;
    const canonicalUrl = route.canonicalUrl + url.hash;
    const renderedSearch = route.renderedSearch;
    const prefetchSeed = {
        renderedSearch,
        routeTree,
        metadataVaryPath: route.metadata.varyPath,
        data: null,
        head: null,
        dynamicStaleAt: (0, _bfcache.computeDynamicStaleAt)(now, _bfcache.UnknownDynamicStaleTime)
    };
    return navigateToKnownRoute(now, state, url, canonicalUrl, prefetchSeed, currentUrl, currentRenderedSearch, currentCacheNode, currentFlightRouterState, freshnessPolicy, nextUrl, scrollBehavior, navigateType, null, route);
}
// Used to request all the dynamic data for a route, rather than just a subset,
// e.g. during a refresh or a revalidation. Typically this gets constructed
// during the normal flow when diffing the route tree, but for an unprefetched
// navigation, where we don't know the structure of the target route, we use
// this instead.
const DynamicRequestTreeForEntireRoute = [
    '',
    {},
    null,
    'refetch'
];
async function navigateToUnknownRoute(now, state, url, currentUrl, currentRenderedSearch, nextUrl, currentCacheNode, currentFlightRouterState, freshnessPolicy, scrollBehavior, navigateType) {
    // Runs when a navigation happens but there's no cached prefetch we can use.
    // Don't bother to wait for a prefetch response; go straight to a full
    // navigation that contains both static and dynamic data in a single stream.
    // (This is unlike the old navigation implementation, which instead blocks
    // the dynamic request until a prefetch request is received.)
    //
    // To avoid duplication of logic, we're going to pretend that the tree
    // returned by the dynamic request is, in fact, a prefetch tree. Then we can
    // use the same server response to write the actual data into the CacheNode
    // tree. So it's the same flow as the "happy path" (prefetch, then
    // navigation), except we use a single server response for both stages.
    let dynamicRequestTree;
    switch(freshnessPolicy){
        case _pprnavigations.FreshnessPolicy.Default:
        case _pprnavigations.FreshnessPolicy.HistoryTraversal:
        case _pprnavigations.FreshnessPolicy.Gesture:
            dynamicRequestTree = currentFlightRouterState;
            break;
        case _pprnavigations.FreshnessPolicy.Hydration:
        case _pprnavigations.FreshnessPolicy.RefreshAll:
        case _pprnavigations.FreshnessPolicy.HMRRefresh:
            dynamicRequestTree = DynamicRequestTreeForEntireRoute;
            break;
        default:
            freshnessPolicy;
            dynamicRequestTree = currentFlightRouterState;
            break;
    }
    const promiseForDynamicServerResponse = (0, _fetchserverresponse.fetchServerResponse)(url, {
        flightRouterState: dynamicRequestTree,
        nextUrl
    });
    const result = await promiseForDynamicServerResponse;
    if (typeof result === 'string') {
        // This is an MPA navigation.
        const redirectUrl = new URL(result, location.origin);
        return completeHardNavigation(state, redirectUrl, navigateType);
    }
    const { flightData, canonicalUrl, renderedSearch, couldBeIntercepted, supportsPerSegmentPrefetching, dynamicStaleTime, staticStageData, runtimePrefetchStream, responseHeaders, debugInfo } = result;
    // Since the response format of dynamic requests and prefetches is slightly
    // different, we'll need to massage the data a bit. Create FlightRouterState
    // tree that simulates what we'd receive as the result of a prefetch.
    const navigationSeed = convertServerPatchToFullTree(now, currentFlightRouterState, flightData, renderedSearch, dynamicStaleTime);
    // Learn the route pattern so we can predict it for future navigations.
    // hasDynamicRewrite is false because this is a fresh navigation to an
    // unknown route - any rewrite detection happens during the traversal inside
    // discoverKnownRoute. The hasDynamicRewrite param is only set to true when
    // retrying after a tree mismatch (see dispatchRetryDueToTreeMismatch).
    const metadataVaryPath = navigationSeed.metadataVaryPath;
    if (metadataVaryPath !== null) {
        (0, _optimisticroutes.discoverKnownRoute)(now, url.pathname, nextUrl, null, navigationSeed.routeTree, metadataVaryPath, couldBeIntercepted, (0, _createhreffromurl.createHrefFromUrl)(canonicalUrl), supportsPerSegmentPrefetching, false // hasDynamicRewrite - not a retry, rewrite detection happens during traversal
        );
        if (staticStageData !== null) {
            const { response: staticStageResponse, isResponsePartial } = staticStageData;
            // Write the static stage of the response into the segment cache so that
            // subsequent navigations can serve cached static segments instantly.
            (0, _cache.getStaleAt)(now, staticStageResponse.s).then((staleAt)=>{
                const buildId = responseHeaders.get(_constants.NEXT_NAV_DEPLOYMENT_ID_HEADER) ?? staticStageResponse.b;
                (0, _cache.writeStaticStageResponseIntoCache)(now, staticStageResponse.f, buildId, staticStageResponse.h, staleAt, currentFlightRouterState, renderedSearch, isResponsePartial);
            }).catch(()=>{
            // The static stage processing failed. Not fatal — the navigation
            // completed normally, we just won't write into the cache.
            });
        }
        if (runtimePrefetchStream !== null) {
            (0, _cache.processRuntimePrefetchStream)(now, runtimePrefetchStream, currentFlightRouterState, renderedSearch).then((processed)=>{
                if (processed !== null) {
                    (0, _cache.writeDynamicRenderResponseIntoCache)(now, _types.FetchStrategy.PPRRuntime, processed.flightDatas, processed.buildId, processed.isResponsePartial, processed.headVaryParams, processed.staleAt, processed.navigationSeed, null);
                }
            }).catch(()=>{
            // The runtime prefetch cache write failed. Not fatal — the
            // navigation completed normally, we just won't cache runtime data.
            });
        }
    }
    return navigateToKnownRoute(now, state, url, (0, _createhreffromurl.createHrefFromUrl)(canonicalUrl), navigationSeed, currentUrl, currentRenderedSearch, currentCacheNode, currentFlightRouterState, freshnessPolicy, nextUrl, scrollBehavior, navigateType, debugInfo, // came directly from the server. If a mismatch occurs during dynamic data
    // fetch, the retry handler will traverse the known route tree to mark the
    // entry as having a dynamic rewrite.
    null);
}
function completeHardNavigation(state, url, navigateType) {
    if ((0, _javascripturl.isJavaScriptURLString)(url.href)) {
        console.error('Next.js has blocked a javascript: URL as a security precaution.');
        return state;
    }
    const newState = {
        canonicalUrl: url.origin === location.origin ? (0, _createhreffromurl.createHrefFromUrl)(url) : url.href,
        pushRef: {
            pendingPush: navigateType === 'push',
            mpaNavigation: true,
            preserveCustomHistoryState: false
        },
        // TODO: None of the rest of these values are consistent with the incoming
        // navigation. We rely on the fact that AppRouter will suspend and trigger
        // a hard navigation before it accesses any of these values. But instead
        // we should trigger the hard navigation and blocking any subsequent
        // router updates without updating React.
        renderedSearch: state.renderedSearch,
        focusAndScrollRef: state.focusAndScrollRef,
        cache: state.cache,
        tree: state.tree,
        nextUrl: state.nextUrl,
        previousNextUrl: state.previousNextUrl,
        debugInfo: null
    };
    return newState;
}
function completeSoftNavigation(oldState, url, referringNextUrl, tree, cache, renderedSearch, canonicalUrl, navigateType, scrollBehavior, scrollRef, collectedDebugInfo) {
    // The "Next-Url" is a special representation of the URL that Next.js
    // uses to implement interception routes.
    // TODO: Get rid of this extra traversal by computing this during the
    // same traversal that computes the tree itself. We should also figure out
    // what is the minimum information needed for the server to correctly
    // intercept the route.
    const changedPath = (0, _computechangedpath.computeChangedPath)(oldState.tree, tree);
    const nextUrlForNewRoute = changedPath ? changedPath : oldState.nextUrl;
    // This value is stored on the state as `previousNextUrl`; the naming is
    // confusing. What it represents is the "Next-Url" header that was used to
    // fetch the incoming route. It's essentially the refererer URL, but in a
    // Next.js specific format. During refreshes, this is sent back to the server
    // instead of the current route's "Next-Url" so that the same interception
    // logic is applied as during the original navigation.
    const previousNextUrl = referringNextUrl;
    // Check if the only thing that changed was the hash fragment.
    const oldUrl = new URL(oldState.canonicalUrl, url);
    const onlyHashChange = // navigations are always same-origin.
    url.pathname === oldUrl.pathname && url.search === oldUrl.search && url.hash !== oldUrl.hash;
    // Determine whether and how the page should scroll after this
    // navigation.
    //
    // By default, we scroll to the segments that were navigated to — i.e.
    // segments in the new part of the route, as opposed to shared segments
    // that were already part of the previous route. All newly navigated
    // segments share a single ScrollRef. When they mount, the first one
    // to mount initiates the scroll. They share a ref so that only one
    // scroll happens per navigation.
    //
    // If a subsequent navigation produces new segments, those supersede
    // any pending scroll from the previous navigation by invalidating its
    // ScrollRef. If a navigation doesn't produce any new segments (e.g.
    // a refresh where the route structure didn't change), any pending
    // scrolls from previous navigations are unaffected.
    //
    // The branches below handle special cases layered on top of this
    // default model.
    let activeScrollRef;
    let forceScroll;
    if (scrollBehavior === _routerreducertypes.ScrollBehavior.NoScroll) {
        // The user explicitly opted out of scrolling (e.g. scroll={false}
        // on a Link or router.push).
        //
        // If this navigation created new scroll targets (scrollRef !== null),
        // neutralize them. If it didn't, any prior scroll targets carried
        // forward on the cache nodes via reuseSharedCacheNode remain active.
        if (scrollRef !== null) {
            scrollRef.current = false;
        }
        activeScrollRef = oldState.focusAndScrollRef.scrollRef;
        forceScroll = false;
    } else if (onlyHashChange) {
        // Hash-only navigations should scroll regardless of per-node state.
        // Create a fresh ref so the first segment to scroll consumes it.
        //
        // Invalidate any scroll ref from a prior navigation that hasn't
        // been consumed yet.
        const oldScrollRef = oldState.focusAndScrollRef.scrollRef;
        if (oldScrollRef !== null) {
            oldScrollRef.current = false;
        }
        // Also invalidate any per-node refs that were accumulated during
        // this navigation's tree construction — the hash-only ref
        // supersedes them.
        if (scrollRef !== null) {
            scrollRef.current = false;
        }
        activeScrollRef = {
            current: true
        };
        forceScroll = true;
    } else {
        // Default case. Use the accumulated scrollRef (may be null if no
        // new segments were created). The handler checks per-node refs, so
        // unchanged parallel route slots won't scroll.
        activeScrollRef = scrollRef;
        // If this navigation created new scroll targets, invalidate any
        // pending scroll from a previous navigation.
        if (scrollRef !== null) {
            const oldScrollRef = oldState.focusAndScrollRef.scrollRef;
            if (oldScrollRef !== null) {
                oldScrollRef.current = false;
            }
        }
        forceScroll = false;
    }
    const newState = {
        canonicalUrl,
        renderedSearch,
        pushRef: {
            pendingPush: navigateType === 'push',
            mpaNavigation: false,
            preserveCustomHistoryState: false
        },
        focusAndScrollRef: {
            scrollRef: activeScrollRef,
            forceScroll,
            onlyHashChange,
            hashFragment: //
            // Empty hash should trigger default behavior of scrolling layout into
            // view. #top is handled in layout-router.
            //
            // Refer to `ScrollAndFocusHandler` for details on how this is used.
            scrollBehavior !== _routerreducertypes.ScrollBehavior.NoScroll && url.hash !== '' ? decodeURIComponent(url.hash.slice(1)) : oldState.focusAndScrollRef.hashFragment
        },
        cache,
        tree,
        nextUrl: nextUrlForNewRoute,
        previousNextUrl,
        debugInfo: collectedDebugInfo
    };
    return newState;
}
function completeTraverseNavigation(state, url, renderedSearch, cache, tree, nextUrl) {
    return {
        // Set canonical url
        canonicalUrl: (0, _createhreffromurl.createHrefFromUrl)(url),
        renderedSearch,
        pushRef: {
            pendingPush: false,
            mpaNavigation: false,
            // Ensures that the custom history state that was set is preserved when applying this update.
            preserveCustomHistoryState: true
        },
        focusAndScrollRef: state.focusAndScrollRef,
        cache,
        // Restore provided tree
        tree,
        nextUrl,
        // TODO: We need to restore previousNextUrl, too, which represents the
        // Next-Url that was used to fetch the data. Anywhere we fetch using the
        // canonical URL, there should be a corresponding Next-Url.
        previousNextUrl: null,
        debugInfo: null
    };
}
function convertServerPatchToFullTree(now, currentTree, flightData, renderedSearch, dynamicStaleTimeSeconds) {
    // During a client navigation or prefetch, the server sends back only a patch
    // for the parts of the tree that have changed.
    //
    // This applies the patch to the base tree to create a full representation of
    // the resulting tree.
    //
    // The return type includes a full FlightRouterState tree and a full
    // CacheNodeSeedData tree. (Conceptually these are the same tree, and should
    // eventually be unified, but there's still lots of existing code that
    // operates on FlightRouterState trees alone without the CacheNodeSeedData.)
    //
    // TODO: This similar to what apply-router-state-patch-to-tree does. It
    // will eventually fully replace it. We should get rid of all the remaining
    // places where we iterate over the server patch format. This should also
    // eventually replace normalizeFlightData.
    let baseTree = currentTree;
    let baseData = null;
    let head = null;
    if (flightData !== null) {
        for (const { segmentPath, tree: treePatch, seedData: dataPatch, head: headPatch } of flightData){
            const result = convertServerPatchToFullTreeImpl(baseTree, baseData, treePatch, dataPatch, segmentPath, renderedSearch, 0);
            baseTree = result.tree;
            baseData = result.data;
            // This is the same for all patches per response, so just pick an
            // arbitrary one
            head = headPatch;
        }
    }
    const finalFlightRouterState = baseTree;
    // Convert the final FlightRouterState into a RouteTree type.
    //
    // TODO: Eventually, FlightRouterState will evolve to being a transport format
    // only. The RouteTree type will become the main type used for dealing with
    // routes on the client, and we'll store it in the state directly.
    const acc = {
        metadataVaryPath: null
    };
    const routeTree = (0, _cache.convertRootFlightRouterStateToRouteTree)(finalFlightRouterState, renderedSearch, acc);
    return {
        routeTree,
        metadataVaryPath: acc.metadataVaryPath,
        data: baseData,
        renderedSearch,
        head,
        dynamicStaleAt: (0, _bfcache.computeDynamicStaleAt)(now, dynamicStaleTimeSeconds)
    };
}
function convertServerPatchToFullTreeImpl(baseRouterState, baseData, treePatch, dataPatch, segmentPath, renderedSearch, index) {
    if (index === segmentPath.length) {
        // We reached the part of the tree that we need to patch.
        return {
            tree: treePatch,
            data: dataPatch
        };
    }
    // segmentPath represents the parent path of subtree. It's a repeating
    // pattern of parallel route key and segment:
    //
    //   [string, Segment, string, Segment, string, Segment, ...]
    //
    // This path tells us which part of the base tree to apply the tree patch.
    //
    // NOTE: We receive the FlightRouterState patch in the same request as the
    // seed data patch. Therefore we don't need to worry about diffing the segment
    // values; we can assume the server sent us a correct result.
    const updatedParallelRouteKey = segmentPath[index];
    // const segment: Segment = segmentPath[index + 1] <-- Not used, see note above
    const baseTreeChildren = baseRouterState[1];
    const baseSeedDataChildren = baseData !== null ? baseData[1] : null;
    const newTreeChildren = {};
    const newSeedDataChildren = {};
    for(const parallelRouteKey in baseTreeChildren){
        const childBaseRouterState = baseTreeChildren[parallelRouteKey];
        const childBaseSeedData = baseSeedDataChildren !== null ? baseSeedDataChildren[parallelRouteKey] ?? null : null;
        if (parallelRouteKey === updatedParallelRouteKey) {
            const result = convertServerPatchToFullTreeImpl(childBaseRouterState, childBaseSeedData, treePatch, dataPatch, segmentPath, renderedSearch, // the end of the segment path.
            index + 2);
            newTreeChildren[parallelRouteKey] = result.tree;
            newSeedDataChildren[parallelRouteKey] = result.data;
        } else {
            // This child is not being patched. Copy it over as-is.
            newTreeChildren[parallelRouteKey] = childBaseRouterState;
            newSeedDataChildren[parallelRouteKey] = childBaseSeedData;
        }
    }
    let clonedTree;
    let clonedSeedData;
    // Clone all the fields except the children.
    // Clone the FlightRouterState tree. Based on equivalent logic in
    // apply-router-state-patch-to-tree, but should confirm whether we need to
    // copy all of these fields. Not sure the server ever sends, e.g. the
    // refetch marker.
    clonedTree = [
        baseRouterState[0],
        newTreeChildren
    ];
    if (2 in baseRouterState) {
        const compressedRefreshState = baseRouterState[2];
        if (compressedRefreshState !== undefined && compressedRefreshState !== null) {
            // Since this part of the tree was patched with new data, any parent
            // refresh states should be updated to reflect the new rendered search
            // value. (The refresh state acts like a "context provider".) All pages
            // within the same server response share the same renderedSearch value,
            // but the same RouteTree could be composed from multiple different
            // routes, and multiple responses.
            clonedTree[2] = [
                compressedRefreshState[0],
                renderedSearch
            ];
        }
    }
    if (3 in baseRouterState) {
        clonedTree[3] = baseRouterState[3];
    }
    if (4 in baseRouterState) {
        clonedTree[4] = baseRouterState[4];
    }
    // Clone the CacheNodeSeedData tree.
    const isEmptySeedDataPartial = true;
    clonedSeedData = [
        null,
        newSeedDataChildren,
        null,
        isEmptySeedDataPartial,
        null
    ];
    return {
        tree: clonedTree,
        data: clonedSeedData
    };
}
/**
 * Instant Navigation Testing API: ensures a prefetch task has been initiated
 * and completed before proceeding with the navigation. This guarantees that
 * segment data requests are at least pending, even for routes whose route
 * tree is already cached.
 *
 * After the prefetch completes, delegates to the normal navigation flow.
 */ async function ensurePrefetchThenNavigate(state, url, currentUrl, currentRenderedSearch, currentCacheNode, currentFlightRouterState, nextUrl, freshnessPolicy, scrollBehavior, navigateType) {
    const link = (0, _links.getLinkForCurrentNavigation)();
    const fetchStrategy = link !== null ? link.fetchStrategy : _types.FetchStrategy.PPR;
    // Transition the cookie to captured-SPA immediately, before waiting
    // for the prefetch. This ensures the devtools panel can update its UI
    // right away, even if the prefetch takes time (e.g. dev compilation).
    // The "to" tree starts as null and is filled in after the prefetch
    // resolves and the navigation produces a new router state.
    const { transitionToCapturedSPA, updateCapturedSPAToTree } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/navigation-testing-lock.js [app-client] (ecmascript)");
    transitionToCapturedSPA(currentFlightRouterState, null);
    const cacheKey = (0, _cachekey.createCacheKey)(url.href, nextUrl);
    await new Promise((resolve)=>{
        (0, _scheduler.schedulePrefetchTask)(cacheKey, currentFlightRouterState, fetchStrategy, _types.PrefetchPriority.Default, null, resolve // _onComplete callback
        );
    });
    // Prefetch is complete. Proceed with the normal navigation flow, which
    // will now find the route in the cache.
    const result = await navigateImpl(state, url, currentUrl, currentRenderedSearch, currentCacheNode, currentFlightRouterState, nextUrl, freshnessPolicy, scrollBehavior, navigateType);
    // Update the cookie with the resolved "to" tree so the devtools
    // panel can display both routes immediately.
    updateCapturedSPAToTree(currentFlightRouterState, result.tree);
    return result;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/navigate-reducer.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    DYNAMIC_STALETIME_MS: null,
    STATIC_STALETIME_MS: null,
    navigateReducer: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    DYNAMIC_STALETIME_MS: function() {
        return DYNAMIC_STALETIME_MS;
    },
    STATIC_STALETIME_MS: function() {
        return STATIC_STALETIME_MS;
    },
    navigateReducer: function() {
        return navigateReducer;
    }
});
const _navigation = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/navigation.js [app-client] (ecmascript)");
const _cache = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache.js [app-client] (ecmascript)");
const _pprnavigations = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/ppr-navigations.js [app-client] (ecmascript)");
const DYNAMIC_STALETIME_MS = Number(("TURBOPACK compile-time value", "0")) * 1000;
const STATIC_STALETIME_MS = (0, _cache.getStaleTimeMs)(Number(("TURBOPACK compile-time value", "300")));
function navigateReducer(state, action) {
    const { url, isExternalUrl, navigateType, scrollBehavior } = action;
    if (isExternalUrl) {
        return (0, _navigation.completeHardNavigation)(state, url, navigateType);
    }
    // Handles case where `<meta http-equiv="refresh">` tag is present,
    // which will trigger an MPA navigation.
    if (document.getElementById('__next-page-redirect')) {
        return (0, _navigation.completeHardNavigation)(state, url, navigateType);
    }
    // Temporary glue code between the router reducer and the new navigation
    // implementation. Eventually we'll rewrite the router reducer to a
    // state machine.
    const currentUrl = new URL(state.canonicalUrl, location.origin);
    const currentRenderedSearch = state.renderedSearch;
    return (0, _navigation.navigate)(state, url, currentUrl, currentRenderedSearch, state.cache, state.tree, state.nextUrl, _pprnavigations.FreshnessPolicy.Default, scrollBehavior, navigateType);
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/has-interception-route-in-current-tree.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "hasInterceptionRouteInCurrentTree", {
    enumerable: true,
    get: function() {
        return hasInterceptionRouteInCurrentTree;
    }
});
const _interceptionroutes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/interception-routes.js [app-client] (ecmascript)");
function hasInterceptionRouteInCurrentTree([segment, parallelRoutes]) {
    // If we have a dynamic segment, it's marked as an interception route by the presence of the `i` suffix.
    if (Array.isArray(segment) && (segment[2] === 'di(..)(..)' || segment[2] === 'ci(..)(..)' || segment[2] === 'di(.)' || segment[2] === 'ci(.)' || segment[2] === 'di(..)' || segment[2] === 'ci(..)' || segment[2] === 'di(...)' || segment[2] === 'ci(...)')) {
        return true;
    }
    // If segment is not an array, apply the existing string-based check
    if (typeof segment === 'string' && (0, _interceptionroutes.isInterceptionRouteAppPath)(segment)) {
        return true;
    }
    // Iterate through parallelRoutes if they exist
    if (parallelRoutes) {
        for(const key in parallelRoutes){
            if (hasInterceptionRouteInCurrentTree(parallelRoutes[key])) {
                return true;
            }
        }
    }
    return false;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/refresh-reducer.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    refreshDynamicData: null,
    refreshReducer: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    refreshDynamicData: function() {
        return refreshDynamicData;
    },
    refreshReducer: function() {
        return refreshReducer;
    }
});
const _routerreducertypes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/router-reducer-types.js [app-client] (ecmascript)");
const _navigation = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/navigation.js [app-client] (ecmascript)");
const _cache = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache.js [app-client] (ecmascript)");
const _hasinterceptionrouteincurrenttree = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/has-interception-route-in-current-tree.js [app-client] (ecmascript)");
const _pprnavigations = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/ppr-navigations.js [app-client] (ecmascript)");
const _bfcache = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/bfcache.js [app-client] (ecmascript)");
function refreshReducer(state, action) {
    // During a refresh, we invalidate the segment cache but not the route cache.
    // The route cache contains the tree structure (which segments exist at a
    // given URL) which doesn't change during a refresh. The segment cache
    // contains the actual RSC data which needs to be re-fetched.
    //
    // The Instant Navigation Testing API can bypass cache invalidation to
    // preserve prefetched data when refreshing after an MPA navigation. This is
    // only used for testing and is not exposed in production builds by default.
    const bypassCacheInvalidation = ("TURBOPACK compile-time value", true) && action.bypassCacheInvalidation;
    if (!bypassCacheInvalidation) {
        const currentNextUrl = state.nextUrl;
        const currentRouterState = state.tree;
        (0, _cache.invalidateSegmentCacheEntries)(currentNextUrl, currentRouterState);
    }
    return refreshDynamicData(state, _pprnavigations.FreshnessPolicy.RefreshAll);
}
function refreshDynamicData(state, freshnessPolicy) {
    // During a refresh, invalidate the BFCache, which may contain dynamic data.
    (0, _bfcache.invalidateBfCache)();
    const currentNextUrl = state.nextUrl;
    // We always send the last next-url, not the current when performing a dynamic
    // request. This is because we update the next-url after a navigation, but we
    // want the same interception route to be matched that used the last next-url.
    const nextUrlForRefresh = (0, _hasinterceptionrouteincurrenttree.hasInterceptionRouteInCurrentTree)(state.tree) ? state.previousNextUrl || currentNextUrl : null;
    // A refresh is modeled as a navigation to the current URL, but where any
    // existing dynamic data (including in shared layouts) is re-fetched.
    const currentCanonicalUrl = state.canonicalUrl;
    const currentUrl = new URL(currentCanonicalUrl, location.origin);
    const currentRenderedSearch = state.renderedSearch;
    const currentFlightRouterState = state.tree;
    const scrollBehavior = _routerreducertypes.ScrollBehavior.NoScroll;
    // Create a NavigationSeed from the current FlightRouterState.
    // TODO: Eventually we will store this type directly on the state object
    // instead of reconstructing it on demand. Part of a larger series of
    // refactors to unify the various tree types that the client deals with.
    const now = Date.now();
    // TODO: Store the dynamic stale time on the top-level state so it's known
    // during restores and refreshes.
    const refreshSeed = (0, _navigation.convertServerPatchToFullTree)(now, currentFlightRouterState, null, currentRenderedSearch, _bfcache.UnknownDynamicStaleTime);
    const navigateType = 'replace';
    return (0, _navigation.navigateToKnownRoute)(now, state, currentUrl, currentCanonicalUrl, refreshSeed, currentUrl, currentRenderedSearch, state.cache, currentFlightRouterState, freshnessPolicy, nextUrlForRefresh, scrollBehavior, navigateType, null, // cache entry to mark as having a dynamic rewrite on mismatch. If a
    // mismatch occurs, the retry handler will traverse the known route tree
    // to find and mark the entry.
    null);
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/server-patch-reducer.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "serverPatchReducer", {
    enumerable: true,
    get: function() {
        return serverPatchReducer;
    }
});
const _createhreffromurl = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/create-href-from-url.js [app-client] (ecmascript)");
const _routerreducertypes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/router-reducer-types.js [app-client] (ecmascript)");
const _navigation = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/navigation.js [app-client] (ecmascript)");
const _refreshreducer = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/refresh-reducer.js [app-client] (ecmascript)");
const _pprnavigations = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/ppr-navigations.js [app-client] (ecmascript)");
function serverPatchReducer(state, action) {
    // A "retry" is a navigation that happens due to a route mismatch. It's
    // similar to a refresh, because we will omit any existing dynamic data on
    // the page. But we seed the retry navigation with the exact tree that the
    // server just responded with.
    const retryMpa = action.mpa;
    const retryUrl = new URL(action.url, location.origin);
    const retrySeed = action.seed;
    const navigateType = action.navigateType;
    if (retryMpa || retrySeed === null) {
        // If the server did not send back data during the mismatch, fall back to
        // an MPA navigation.
        return (0, _navigation.completeHardNavigation)(state, retryUrl, navigateType);
    }
    const currentUrl = new URL(state.canonicalUrl, location.origin);
    const currentRenderedSearch = state.renderedSearch;
    if (action.previousTree !== state.tree) {
        // There was another, more recent navigation since the once that
        // mismatched. We can abort the retry, but we still need to refresh the
        // page to evict any stale dynamic data.
        return (0, _refreshreducer.refreshReducer)(state, {
            type: _routerreducertypes.ACTION_REFRESH
        });
    }
    // There have been no new navigations since the mismatched one. Refresh,
    // using the tree we just received from the server.
    const retryCanonicalUrl = (0, _createhreffromurl.createHrefFromUrl)(retryUrl);
    const retryNextUrl = action.nextUrl;
    const scrollBehavior = _routerreducertypes.ScrollBehavior.Default;
    const now = Date.now();
    return (0, _navigation.navigateToKnownRoute)(now, state, retryUrl, retryCanonicalUrl, retrySeed, currentUrl, currentRenderedSearch, state.cache, state.tree, _pprnavigations.FreshnessPolicy.RefreshAll, retryNextUrl, scrollBehavior, navigateType, null, // typically a retry after a previous mismatch, so the route was already
    // marked as having a dynamic rewrite when the mismatch was detected.
    null);
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/restore-reducer.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "restoreReducer", {
    enumerable: true,
    get: function() {
        return restoreReducer;
    }
});
const _computechangedpath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/compute-changed-path.js [app-client] (ecmascript)");
const _pprnavigations = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/ppr-navigations.js [app-client] (ecmascript)");
const _navigation = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/navigation.js [app-client] (ecmascript)");
const _bfcache = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/bfcache.js [app-client] (ecmascript)");
function restoreReducer(state, action) {
    // This action is used to restore the router state from the history state.
    // However, it's possible that the history state no longer contains the `FlightRouterState`.
    // We will copy over the internal state on pushState/replaceState events, but if a history entry
    // occurred before hydration, or if the user navigated to a hash using a regular anchor link,
    // the history state will not contain the `FlightRouterState`.
    // In this case, we'll continue to use the existing tree so the router doesn't get into an invalid state.
    let treeToRestore;
    let renderedSearch;
    const historyState = action.historyState;
    if (historyState) {
        treeToRestore = historyState.tree;
        renderedSearch = historyState.renderedSearch;
    } else {
        treeToRestore = state.tree;
        renderedSearch = state.renderedSearch;
    }
    const currentUrl = new URL(state.canonicalUrl, location.origin);
    const restoredUrl = action.url;
    const restoredNextUrl = (0, _computechangedpath.extractPathFromFlightRouterState)(treeToRestore) ?? restoredUrl.pathname;
    const now = Date.now();
    // TODO: Store the dynamic stale time on the top-level state so it's known
    // during restores and refreshes.
    const accumulation = {
        separateRefreshUrls: null,
        scrollRef: null
    };
    const restoreSeed = (0, _navigation.convertServerPatchToFullTree)(now, treeToRestore, null, renderedSearch, _bfcache.UnknownDynamicStaleTime);
    const task = (0, _pprnavigations.startPPRNavigation)(now, currentUrl, state.renderedSearch, state.cache, state.tree, restoreSeed.routeTree, restoreSeed.metadataVaryPath, _pprnavigations.FreshnessPolicy.HistoryTraversal, null, null, restoreSeed.dynamicStaleAt, false, accumulation);
    if (task === null) {
        return (0, _navigation.completeHardNavigation)(state, restoredUrl, 'replace');
    }
    (0, _pprnavigations.spawnDynamicRequests)(task, restoredUrl, restoredNextUrl, _pprnavigations.FreshnessPolicy.HistoryTraversal, accumulation, // cache entry to mark as having a dynamic rewrite on mismatch. If a
    // mismatch occurs, the retry handler will traverse the known route tree
    // to find and mark the entry.
    null, 'replace');
    return (0, _navigation.completeTraverseNavigation)(state, restoredUrl, renderedSearch, task.node, task.route, restoredNextUrl);
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/hmr-refresh-reducer.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "hmrRefreshReducer", {
    enumerable: true,
    get: function() {
        return hmrRefreshReducer;
    }
});
const _refreshreducer = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/refresh-reducer.js [app-client] (ecmascript)");
const _pprnavigations = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/ppr-navigations.js [app-client] (ecmascript)");
function hmrRefreshReducer(state) {
    return (0, _refreshreducer.refreshDynamicData)(state, _pprnavigations.FreshnessPolicy.HMRRefresh);
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/unrecognized-action-error.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    UnrecognizedActionError: null,
    unstable_isUnrecognizedActionError: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    UnrecognizedActionError: function() {
        return UnrecognizedActionError;
    },
    unstable_isUnrecognizedActionError: function() {
        return unstable_isUnrecognizedActionError;
    }
});
class UnrecognizedActionError extends Error {
    constructor(...args){
        super(...args);
        this.name = 'UnrecognizedActionError';
    }
}
function unstable_isUnrecognizedActionError(error) {
    return !!(error && typeof error === 'object' && error instanceof UnrecognizedActionError);
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/assign-location.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "assignLocation", {
    enumerable: true,
    get: function() {
        return assignLocation;
    }
});
const _addbasepath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/add-base-path.js [app-client] (ecmascript)");
function assignLocation(location, url) {
    if (location.startsWith('.')) {
        const urlBase = url.origin + url.pathname;
        return new URL(// new URL('./relative', 'https://example.com/subdir').href -> 'https://example.com/relative'
        // new URL('./relative', 'https://example.com/subdir/').href -> 'https://example.com/subdir/relative'
        (urlBase.endsWith('/') ? urlBase : urlBase + '/') + location);
    }
    return new URL((0, _addbasepath.addBasePath)(location), url.href);
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/redirect.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    getRedirectError: null,
    getRedirectStatusCodeFromError: null,
    getRedirectTypeFromError: null,
    getURLFromRedirectError: null,
    permanentRedirect: null,
    redirect: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    getRedirectError: function() {
        return getRedirectError;
    },
    getRedirectStatusCodeFromError: function() {
        return getRedirectStatusCodeFromError;
    },
    getRedirectTypeFromError: function() {
        return getRedirectTypeFromError;
    },
    getURLFromRedirectError: function() {
        return getURLFromRedirectError;
    },
    permanentRedirect: function() {
        return permanentRedirect;
    },
    redirect: function() {
        return redirect;
    }
});
const _redirectstatuscode = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/redirect-status-code.js [app-client] (ecmascript)");
const _redirecterror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/redirect-error.js [app-client] (ecmascript)");
const actionAsyncStorage = typeof window === 'undefined' ? __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/server/app-render/action-async-storage.external.js [app-client] (ecmascript)").actionAsyncStorage : undefined;
function getRedirectError(url, type, statusCode = _redirectstatuscode.RedirectStatusCode.TemporaryRedirect) {
    const error = Object.defineProperty(new Error(_redirecterror.REDIRECT_ERROR_CODE), "__NEXT_ERROR_CODE", {
        value: "E394",
        enumerable: false,
        configurable: true
    });
    error.digest = `${_redirecterror.REDIRECT_ERROR_CODE};${type};${url};${statusCode};`;
    return error;
}
function redirect(/** The URL to redirect to */ url, type) {
    type ??= actionAsyncStorage?.getStore()?.isAction ? 'push' : 'replace';
    throw getRedirectError(url, type, _redirectstatuscode.RedirectStatusCode.TemporaryRedirect);
}
function permanentRedirect(/** The URL to redirect to */ url, type = 'replace') {
    throw getRedirectError(url, type, _redirectstatuscode.RedirectStatusCode.PermanentRedirect);
}
function getURLFromRedirectError(error) {
    if (!(0, _redirecterror.isRedirectError)(error)) return null;
    // Slices off the beginning of the digest that contains the code and the
    // separating ';'.
    return error.digest.split(';').slice(2, -2).join(';');
}
function getRedirectTypeFromError(error) {
    if (!(0, _redirecterror.isRedirectError)(error)) {
        throw Object.defineProperty(new Error('Not a redirect error'), "__NEXT_ERROR_CODE", {
            value: "E260",
            enumerable: false,
            configurable: true
        });
    }
    return error.digest.split(';', 2)[1];
}
function getRedirectStatusCodeFromError(error) {
    if (!(0, _redirecterror.isRedirectError)(error)) {
        throw Object.defineProperty(new Error('Not a redirect error'), "__NEXT_ERROR_CODE", {
            value: "E260",
            enumerable: false,
            configurable: true
        });
    }
    return Number(error.digest.split(';').at(-2));
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/has-base-path.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
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
const _pathhasprefix = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/path-has-prefix.js [app-client] (ecmascript)");
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/remove-base-path.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
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
const _hasbasepath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/has-base-path.js [app-client] (ecmascript)");
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/server-action-reducer.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "serverActionReducer", {
    enumerable: true,
    get: function() {
        return serverActionReducer;
    }
});
const _appcallserver = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/app-call-server.js [app-client] (ecmascript)");
const _appfindsourcemapurl = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/app-find-source-map-url.js [app-client] (ecmascript)");
const _approuterheaders = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-headers.js [app-client] (ecmascript)");
const _unrecognizedactionerror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/unrecognized-action-error.js [app-client] (ecmascript)");
const _client = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-server-dom-turbopack/client.js [app-client] (ecmascript)");
const _routerreducertypes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/router-reducer-types.js [app-client] (ecmascript)");
const _assignlocation = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/assign-location.js [app-client] (ecmascript)");
const _createhreffromurl = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/create-href-from-url.js [app-client] (ecmascript)");
const _hasinterceptionrouteincurrenttree = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/has-interception-route-in-current-tree.js [app-client] (ecmascript)");
const _flightdatahelpers = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/flight-data-helpers.js [app-client] (ecmascript)");
const _redirect = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/redirect.js [app-client] (ecmascript)");
const _removebasepath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/remove-base-path.js [app-client] (ecmascript)");
const _hasbasepath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/has-base-path.js [app-client] (ecmascript)");
const _serverreferenceinfo = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/server-reference-info.js [app-client] (ecmascript)");
const _cache = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache.js [app-client] (ecmascript)");
const _scheduler = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/scheduler.js [app-client] (ecmascript)");
const _deploymentid = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/deployment-id.js [app-client] (ecmascript)");
const _navigationbuildid = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/navigation-build-id.js [app-client] (ecmascript)");
const _constants = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/constants.js [app-client] (ecmascript)");
const _navigation = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/navigation.js [app-client] (ecmascript)");
const _optimisticroutes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/optimistic-routes.js [app-client] (ecmascript)");
const _actionrevalidationkind = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/action-revalidation-kind.js [app-client] (ecmascript)");
const _approuterutils = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-utils.js [app-client] (ecmascript)");
const _pprnavigations = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/ppr-navigations.js [app-client] (ecmascript)");
const _fetchserverresponse = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/fetch-server-response.js [app-client] (ecmascript)");
const _bfcache = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/bfcache.js [app-client] (ecmascript)");
const createFromFetch = _client.createFromFetch;
let createDebugChannel;
if ("TURBOPACK compile-time truthy", 1) {
    createDebugChannel = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/debug-channel.js [app-client] (ecmascript)").createDebugChannel;
}
async function fetchServerAction(state, nextUrl, { actionId, actionArgs }) {
    const temporaryReferences = (0, _client.createTemporaryReferenceSet)();
    const info = (0, _serverreferenceinfo.extractInfoFromServerReferenceId)(actionId);
    const usedArgs = (0, _serverreferenceinfo.omitUnusedArgs)(actionArgs, info);
    const body = await (0, _client.encodeReply)(usedArgs, {
        temporaryReferences
    });
    const headers = {
        Accept: _approuterheaders.RSC_CONTENT_TYPE_HEADER,
        [_approuterheaders.ACTION_HEADER]: actionId,
        [_approuterheaders.NEXT_ROUTER_STATE_TREE_HEADER]: (0, _flightdatahelpers.prepareFlightRouterStateForRequest)(state.tree)
    };
    const deploymentId = (0, _deploymentid.getDeploymentId)();
    if (deploymentId) {
        headers['x-deployment-id'] = deploymentId;
    }
    if (nextUrl) {
        headers[_approuterheaders.NEXT_URL] = nextUrl;
    }
    if ("TURBOPACK compile-time truthy", 1) {
        if (self.__next_r) {
            headers[_approuterheaders.NEXT_HTML_REQUEST_ID_HEADER] = self.__next_r;
        }
        // Create a new request ID for the server action request. The server uses
        // this to tag debug information sent via WebSocket to the client, which
        // then routes those chunks to the debug channel associated with this ID.
        headers[_approuterheaders.NEXT_REQUEST_ID_HEADER] = crypto.getRandomValues(new Uint32Array(1))[0].toString(16);
    }
    const res = await fetch(state.canonicalUrl, {
        method: 'POST',
        headers,
        body
    });
    // Handle server actions that the server didn't recognize.
    const unrecognizedActionHeader = res.headers.get(_approuterheaders.NEXT_ACTION_NOT_FOUND_HEADER);
    if (unrecognizedActionHeader === '1') {
        throw Object.defineProperty(new _unrecognizedactionerror.UnrecognizedActionError(`Server Action "${actionId}" was not found on the server. \nRead more: https://nextjs.org/docs/messages/failed-to-find-server-action`), "__NEXT_ERROR_CODE", {
            value: "E715",
            enumerable: false,
            configurable: true
        });
    }
    const redirectHeader = res.headers.get('x-action-redirect');
    const [location1, _redirectType] = redirectHeader?.split(';') || [];
    let redirectType;
    switch(_redirectType){
        case 'push':
            redirectType = 'push';
            break;
        case 'replace':
            redirectType = 'replace';
            break;
        default:
            redirectType = undefined;
    }
    const isPrerender = !!res.headers.get(_approuterheaders.NEXT_IS_PRERENDER_HEADER);
    let revalidationKind = _actionrevalidationkind.ActionDidNotRevalidate;
    try {
        const revalidationHeader = res.headers.get('x-action-revalidated');
        if (revalidationHeader) {
            const parsedKind = JSON.parse(revalidationHeader);
            if (parsedKind === _actionrevalidationkind.ActionDidRevalidateStaticAndDynamic || parsedKind === _actionrevalidationkind.ActionDidRevalidateDynamicOnly) {
                revalidationKind = parsedKind;
            }
        }
    } catch  {}
    const redirectLocation = location1 ? (0, _assignlocation.assignLocation)(location1, new URL(state.canonicalUrl, window.location.href)) : undefined;
    const contentType = res.headers.get('content-type');
    const isRscResponse = !!(contentType && contentType.startsWith(_approuterheaders.RSC_CONTENT_TYPE_HEADER));
    // Handle invalid server action responses.
    // A valid response must have `content-type: text/x-component`, unless it's an external redirect.
    // (external redirects have an 'x-action-redirect' header, but the body is an empty 'text/plain')
    if (!isRscResponse && !redirectLocation) {
        // The server can respond with a text/plain error message, but we'll fallback to something generic
        // if there isn't one.
        const message = res.status >= 400 && contentType === 'text/plain' ? await res.text() : 'An unexpected response was received from the server.';
        throw Object.defineProperty(new Error(message), "__NEXT_ERROR_CODE", {
            value: "E394",
            enumerable: false,
            configurable: true
        });
    }
    let actionResult;
    let actionFlightData;
    let actionFlightDataRenderedSearch;
    let couldBeIntercepted = false;
    if (isRscResponse) {
        // Server action redirect responses carry the Flight data of the redirect
        // target, which may be prerendered with a completeness marker byte
        // prepended. Strip it before passing to Flight.
        const responsePromise = redirectLocation ? (0, _fetchserverresponse.processFetch)(res).then(({ response: r })=>r) : Promise.resolve(res);
        const response = await createFromFetch(responsePromise, {
            callServer: _appcallserver.callServer,
            findSourceMapURL: _appfindsourcemapurl.findSourceMapURL,
            temporaryReferences,
            debugChannel: createDebugChannel && createDebugChannel(headers)
        });
        // An internal redirect can send an RSC response, but does not have a useful `actionResult`.
        actionResult = redirectLocation ? undefined : response.a;
        couldBeIntercepted = response.i;
        // Check if the response build ID matches the client build ID.
        // In a multi-zone setup, when a server action triggers a redirect,
        // the server pre-fetches the redirect target as RSC. If the redirect
        // target is served by a different Next.js zone (different build), the
        // pre-fetched RSC data will have a foreign build ID. We must discard
        // the flight data in that case so the redirect triggers an MPA
        // navigation (full page load) instead of trying to apply the foreign
        // RSC payload — which would result in a blank page.
        const responseBuildId = res.headers.get(_constants.NEXT_NAV_DEPLOYMENT_ID_HEADER) ?? response.b;
        if (responseBuildId !== undefined && responseBuildId !== (0, _navigationbuildid.getNavigationBuildId)()) {
        // Build ID mismatch — discard the flight data. The redirect will
        // still be processed, and the absence of flight data will cause an
        // MPA navigation via completeHardNavigation().
        } else {
            const maybeFlightData = (0, _flightdatahelpers.normalizeFlightData)(response.f);
            if (maybeFlightData !== '') {
                actionFlightData = maybeFlightData;
                actionFlightDataRenderedSearch = response.q;
            }
        }
    } else {
        // An external redirect doesn't contain RSC data.
        actionResult = undefined;
        actionFlightData = undefined;
        actionFlightDataRenderedSearch = undefined;
    }
    return {
        actionResult,
        actionFlightData,
        actionFlightDataRenderedSearch,
        redirectLocation,
        redirectType,
        revalidationKind,
        isPrerender,
        couldBeIntercepted
    };
}
function serverActionReducer(state, action) {
    const { resolve, reject } = action;
    // only pass along the `nextUrl` param (used for interception routes) if the current route was intercepted.
    // If the route has been intercepted, the action should be as well.
    // Otherwise the server action might be intercepted with the wrong action id
    // (ie, one that corresponds with the intercepted route)
    const nextUrl = // performing a dynamic request. This is because we update
    // the next-url after a navigation, but we want the same
    // interception route to be matched that used the last
    // next-url.
    (state.previousNextUrl || state.nextUrl) && (0, _hasinterceptionrouteincurrenttree.hasInterceptionRouteInCurrentTree)(state.tree) ? state.previousNextUrl || state.nextUrl : null;
    return fetchServerAction(state, nextUrl, action).then(async ({ revalidationKind, actionResult, actionFlightData: flightData, actionFlightDataRenderedSearch: flightDataRenderedSearch, redirectLocation, redirectType, isPrerender, couldBeIntercepted })=>{
        if (revalidationKind !== _actionrevalidationkind.ActionDidNotRevalidate) {
            // There was either a revalidation or a refresh, or maybe both.
            // Evict the BFCache, which may contain dynamic data.
            (0, _bfcache.invalidateBfCache)();
            // Store whether this action triggered any revalidation
            // The action queue will use this information to potentially
            // trigger a refresh action if the action was discarded
            // (ie, due to a navigation, before the action completed)
            action.didRevalidate = true;
            // If there was a revalidation, evict the prefetch cache.
            // TODO: Evict only segments with matching tags and/or paths.
            // TODO: We should only invalidate the route cache if cookies were
            // mutated, since route trees may vary based on cookies. For now we
            // invalidate both caches until we have a way to detect cookie
            // mutations on the client.
            if (revalidationKind === _actionrevalidationkind.ActionDidRevalidateStaticAndDynamic) {
                (0, _cache.invalidateEntirePrefetchCache)(nextUrl, state.tree);
            }
            // Start a cooldown before re-prefetching to allow CDN cache
            // propagation.
            (0, _scheduler.startRevalidationCooldown)();
        }
        const navigateType = redirectType || 'push';
        if (redirectLocation !== undefined) {
            // If the action triggered a redirect, the action promise will be rejected with
            // a redirect so that it's handled by RedirectBoundary as we won't have a valid
            // action result to resolve the promise with. This will effectively reset the state of
            // the component that called the action as the error boundary will remount the tree.
            // The status code doesn't matter here as the action handler will have already sent
            // a response with the correct status code.
            if ((0, _approuterutils.isExternalURL)(redirectLocation)) {
                // External redirect. Triggers an MPA navigation.
                const redirectHref = redirectLocation.href;
                const redirectError = createRedirectErrorForAction(redirectHref, navigateType);
                reject(redirectError);
                return (0, _navigation.completeHardNavigation)(state, redirectLocation, navigateType);
            } else {
                // Internal redirect. Triggers an SPA navigation.
                const redirectWithBasepath = (0, _createhreffromurl.createHrefFromUrl)(redirectLocation, false);
                const redirectHref = (0, _hasbasepath.hasBasePath)(redirectWithBasepath) ? (0, _removebasepath.removeBasePath)(redirectWithBasepath) : redirectWithBasepath;
                const redirectError = createRedirectErrorForAction(redirectHref, navigateType);
                reject(redirectError);
            }
        } else {
            // If there's no redirect, resolve the action with the result.
            resolve(actionResult);
        }
        // Check if we can bail out without updating any state.
        if (redirectLocation === undefined && // Did the action revalidate any data?
        revalidationKind === _actionrevalidationkind.ActionDidNotRevalidate && // Did the server render new data?
        flightData === undefined) {
            // The action did not trigger any revalidations or redirects. No
            // navigation is required.
            return state;
        }
        if (flightData === undefined && redirectLocation !== undefined) {
            // The server redirected, but did not send any Flight data. This implies
            // an external redirect.
            // TODO: We should refactor the action response type to be more explicit
            // about the various response types.
            return (0, _navigation.completeHardNavigation)(state, redirectLocation, navigateType);
        }
        if (typeof flightData === 'string') {
            // If the flight data is just a string, something earlier in the
            // response handling triggered an external redirect.
            return (0, _navigation.completeHardNavigation)(state, new URL(flightData, location.origin), navigateType);
        }
        // The action triggered a navigation — either a redirect, a revalidation,
        // or both.
        // If there was no redirect, then the target URL is the same as the
        // current URL.
        const currentUrl = new URL(state.canonicalUrl, location.origin);
        const currentRenderedSearch = state.renderedSearch;
        const redirectUrl = redirectLocation !== undefined ? redirectLocation : currentUrl;
        const currentFlightRouterState = state.tree;
        const scrollBehavior = _routerreducertypes.ScrollBehavior.Default;
        // If the action triggered a revalidation of the cache, we should also
        // refresh all the dynamic data.
        const freshnessPolicy = revalidationKind === _actionrevalidationkind.ActionDidNotRevalidate ? _pprnavigations.FreshnessPolicy.Default : _pprnavigations.FreshnessPolicy.RefreshAll;
        // The server may have sent back new data. If so, we will perform a
        // "seeded" navigation that uses the data from the response.
        // TODO: Currently the server always renders from the root in
        // response to a Server Action. In the case of a normal redirect
        // with no revalidation, it should skip over the shared layouts.
        if (flightData !== undefined && flightDataRenderedSearch !== undefined) {
            // The server sent back new route data as part of the response. We
            // will use this to render the new page. If this happens to be only a
            // subset of the data needed to render the new page, we'll initiate a
            // new fetch, like we would for a normal navigation.
            const redirectCanonicalUrl = (0, _createhreffromurl.createHrefFromUrl)(redirectUrl);
            const now = Date.now();
            // TODO: Store the dynamic stale time on the top-level state so it's
            // known during restores and refreshes.
            const redirectSeed = (0, _navigation.convertServerPatchToFullTree)(now, currentFlightRouterState, flightData, flightDataRenderedSearch, _bfcache.UnknownDynamicStaleTime);
            // Learn the route pattern so we can predict it for future navigations.
            const metadataVaryPath = redirectSeed.metadataVaryPath;
            if (metadataVaryPath !== null) {
                (0, _optimisticroutes.discoverKnownRoute)(now, redirectUrl.pathname, nextUrl, null, redirectSeed.routeTree, metadataVaryPath, couldBeIntercepted, redirectCanonicalUrl, isPrerender, false // hasDynamicRewrite
                );
            }
            return (0, _navigation.navigateToKnownRoute)(now, state, redirectUrl, redirectCanonicalUrl, redirectSeed, currentUrl, currentRenderedSearch, state.cache, currentFlightRouterState, freshnessPolicy, nextUrl, scrollBehavior, navigateType, null, // have the route tree from the server response. If a mismatch occurs
            // during dynamic data fetch, the retry handler will traverse the
            // known route tree to mark the entry as having a dynamic rewrite.
            null);
        }
        // The server did not send back new data. We'll perform a regular, non-
        // seeded navigation — effectively the same as <Link> or router.push().
        return (0, _navigation.navigate)(state, redirectUrl, currentUrl, currentRenderedSearch, state.cache, currentFlightRouterState, nextUrl, freshnessPolicy, scrollBehavior, navigateType);
    }, (e)=>{
        // When the server action is rejected we don't update the state and instead call the reject handler of the promise.
        reject(e);
        return state;
    });
}
function createRedirectErrorForAction(redirectHref, resolvedRedirectType) {
    const redirectError = (0, _redirect.getRedirectError)(redirectHref, resolvedRedirectType);
    redirectError.handled = true;
    return redirectError;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/router-reducer.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "reducer", {
    enumerable: true,
    get: function() {
        return reducer;
    }
});
const _routerreducertypes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/router-reducer-types.js [app-client] (ecmascript)");
const _navigatereducer = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/navigate-reducer.js [app-client] (ecmascript)");
const _serverpatchreducer = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/server-patch-reducer.js [app-client] (ecmascript)");
const _restorereducer = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/restore-reducer.js [app-client] (ecmascript)");
const _refreshreducer = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/refresh-reducer.js [app-client] (ecmascript)");
const _hmrrefreshreducer = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/hmr-refresh-reducer.js [app-client] (ecmascript)");
const _serveractionreducer = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/server-action-reducer.js [app-client] (ecmascript)");
/**
 * Reducer that handles the app-router state updates.
 */ function clientReducer(state, action) {
    switch(action.type){
        case _routerreducertypes.ACTION_NAVIGATE:
            {
                return (0, _navigatereducer.navigateReducer)(state, action);
            }
        case _routerreducertypes.ACTION_SERVER_PATCH:
            {
                return (0, _serverpatchreducer.serverPatchReducer)(state, action);
            }
        case _routerreducertypes.ACTION_RESTORE:
            {
                return (0, _restorereducer.restoreReducer)(state, action);
            }
        case _routerreducertypes.ACTION_REFRESH:
            {
                return (0, _refreshreducer.refreshReducer)(state, action);
            }
        case _routerreducertypes.ACTION_HMR_REFRESH:
            {
                return (0, _hmrrefreshreducer.hmrRefreshReducer)(state);
            }
        case _routerreducertypes.ACTION_SERVER_ACTION:
            {
                return (0, _serveractionreducer.serverActionReducer)(state, action);
            }
        // This case should never be hit as dispatch is strongly typed.
        default:
            throw Object.defineProperty(new Error('Unknown action'), "__NEXT_ERROR_CODE", {
                value: "E295",
                enumerable: false,
                configurable: true
            });
    }
}
function serverReducer(state, _action) {
    return state;
}
const reducer = typeof window === 'undefined' ? serverReducer : clientReducer;
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/prefetch.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "prefetch", {
    enumerable: true,
    get: function() {
        return prefetch;
    }
});
const _approuterutils = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-utils.js [app-client] (ecmascript)");
const _cachekey = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache-key.js [app-client] (ecmascript)");
const _scheduler = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/scheduler.js [app-client] (ecmascript)");
const _types = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/types.js [app-client] (ecmascript)");
function prefetch(href, nextUrl, treeAtTimeOfPrefetch, fetchStrategy, onInvalidate) {
    const url = (0, _approuterutils.createPrefetchURL)(href);
    if (url === null) {
        // This href should not be prefetched.
        return;
    }
    const cacheKey = (0, _cachekey.createCacheKey)(url.href, nextUrl);
    (0, _scheduler.schedulePrefetchTask)(cacheKey, treeAtTimeOfPrefetch, fetchStrategy, _types.PrefetchPriority.Default, onInvalidate);
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-instance.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    createMutableActionQueue: null,
    dispatchNavigateAction: null,
    dispatchTraverseAction: null,
    getCurrentAppRouterState: null,
    publicAppRouterInstance: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    createMutableActionQueue: function() {
        return createMutableActionQueue;
    },
    dispatchNavigateAction: function() {
        return dispatchNavigateAction;
    },
    dispatchTraverseAction: function() {
        return dispatchTraverseAction;
    },
    getCurrentAppRouterState: function() {
        return getCurrentAppRouterState;
    },
    publicAppRouterInstance: function() {
        return publicAppRouterInstance;
    }
});
const _routerreducertypes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/router-reducer-types.js [app-client] (ecmascript)");
const _routerreducer = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/router-reducer.js [app-client] (ecmascript)");
const _react = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
const _isthenable = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/is-thenable.js [app-client] (ecmascript)");
const _types = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/types.js [app-client] (ecmascript)");
const _prefetch = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/prefetch.js [app-client] (ecmascript)");
const _navigation = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/navigation.js [app-client] (ecmascript)");
const _useactionqueue = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/use-action-queue.js [app-client] (ecmascript)");
const _optimisticroutes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/optimistic-routes.js [app-client] (ecmascript)");
const _pprnavigations = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/ppr-navigations.js [app-client] (ecmascript)");
const _addbasepath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/add-base-path.js [app-client] (ecmascript)");
const _approuterutils = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-utils.js [app-client] (ecmascript)");
const _links = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/links.js [app-client] (ecmascript)");
const _javascripturl = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/lib/javascript-url.js [app-client] (ecmascript)");
function runRemainingActions(actionQueue, setState) {
    if (actionQueue.pending !== null) {
        actionQueue.pending = actionQueue.pending.next;
        if (actionQueue.pending !== null) {
            runAction({
                actionQueue,
                action: actionQueue.pending,
                setState
            });
        }
    } else {
        // Check for refresh when pending is already null
        // This handles the case where a discarded server action completes
        // after the navigation has already finished and the queue is empty
        if (actionQueue.needsRefresh) {
            actionQueue.needsRefresh = false;
            actionQueue.dispatch({
                type: _routerreducertypes.ACTION_REFRESH
            }, setState);
        }
    }
}
async function runAction({ actionQueue, action, setState }) {
    const prevState = actionQueue.state;
    actionQueue.pending = action;
    const payload = action.payload;
    const actionResult = actionQueue.action(prevState, payload);
    function handleResult(nextState) {
        // if we discarded this action, the state should also be discarded
        if (action.discarded) {
            // Check if the discarded server action revalidated data
            if (action.payload.type === _routerreducertypes.ACTION_SERVER_ACTION && action.payload.didRevalidate) {
                // The server action was discarded but it revalidated data,
                // mark that we need to refresh after all actions complete
                actionQueue.needsRefresh = true;
            }
            // Still need to run remaining actions even for discarded actions
            // to potentially trigger the refresh
            runRemainingActions(actionQueue, setState);
            return;
        }
        actionQueue.state = nextState;
        runRemainingActions(actionQueue, setState);
        action.resolve(nextState);
    }
    // if the action is a promise, set up a callback to resolve it
    if ((0, _isthenable.isThenable)(actionResult)) {
        actionResult.then(handleResult, (err)=>{
            runRemainingActions(actionQueue, setState);
            action.reject(err);
        });
    } else {
        handleResult(actionResult);
    }
}
function dispatchAction(actionQueue, payload, setState) {
    let resolvers = {
        resolve: setState,
        reject: ()=>{}
    };
    // most of the action types are async with the exception of restore
    // it's important that restore is handled quickly since it's fired on the popstate event
    // and we don't want to add any delay on a back/forward nav
    // this only creates a promise for the async actions
    if (payload.type !== _routerreducertypes.ACTION_RESTORE) {
        // Create the promise and assign the resolvers to the object.
        const deferredPromise = new Promise((resolve, reject)=>{
            resolvers = {
                resolve,
                reject
            };
        });
        (0, _react.startTransition)(()=>{
            // we immediately notify React of the pending promise -- the resolver is attached to the action node
            // and will be called when the associated action promise resolves
            setState(deferredPromise);
        });
    }
    const newAction = {
        payload,
        next: null,
        resolve: resolvers.resolve,
        reject: resolvers.reject
    };
    // Check if the queue is empty
    if (actionQueue.pending === null) {
        // The queue is empty, so add the action and start it immediately
        // Mark this action as the last in the queue
        actionQueue.last = newAction;
        runAction({
            actionQueue,
            action: newAction,
            setState
        });
    } else if (payload.type === _routerreducertypes.ACTION_NAVIGATE || payload.type === _routerreducertypes.ACTION_RESTORE) {
        // Navigations (including back/forward) take priority over any pending actions.
        // Mark the pending action as discarded (so the state is never applied) and start the navigation action immediately.
        actionQueue.pending.discarded = true;
        // The rest of the current queue should still execute after this navigation.
        // (Note that it can't contain any earlier navigations, because we always put those into `actionQueue.pending` by calling `runAction`)
        newAction.next = actionQueue.pending.next;
        runAction({
            actionQueue,
            action: newAction,
            setState
        });
    } else {
        // The queue is not empty, so add the action to the end of the queue
        // It will be started by runRemainingActions after the previous action finishes
        if (actionQueue.last !== null) {
            actionQueue.last.next = newAction;
        }
        actionQueue.last = newAction;
    }
}
let globalActionQueue = null;
function createMutableActionQueue(initialState, instrumentationHooks) {
    const actionQueue = {
        state: initialState,
        dispatch: (payload, setState)=>dispatchAction(actionQueue, payload, setState),
        action: async (state, action)=>{
            const result = (0, _routerreducer.reducer)(state, action);
            return result;
        },
        pending: null,
        last: null,
        onRouterTransitionStart: instrumentationHooks !== null && typeof instrumentationHooks.onRouterTransitionStart === 'function' ? instrumentationHooks.onRouterTransitionStart : null
    };
    if (typeof window !== 'undefined') {
        // The action queue is lazily created on hydration, but after that point
        // it doesn't change. So we can store it in a global rather than pass
        // it around everywhere via props/context.
        if (globalActionQueue !== null) {
            throw Object.defineProperty(new Error('Internal Next.js Error: createMutableActionQueue was called more ' + 'than once'), "__NEXT_ERROR_CODE", {
                value: "E624",
                enumerable: false,
                configurable: true
            });
        }
        globalActionQueue = actionQueue;
    }
    return actionQueue;
}
function getCurrentAppRouterState() {
    return globalActionQueue !== null ? globalActionQueue.state : null;
}
function getAppRouterActionQueue() {
    if (globalActionQueue === null) {
        throw Object.defineProperty(new Error('Internal Next.js error: Router action dispatched before initialization.'), "__NEXT_ERROR_CODE", {
            value: "E668",
            enumerable: false,
            configurable: true
        });
    }
    return globalActionQueue;
}
function getProfilingHookForOnNavigationStart() {
    if (globalActionQueue !== null) {
        return globalActionQueue.onRouterTransitionStart;
    }
    return null;
}
function dispatchNavigateAction(href, navigateType, scrollBehavior, linkInstanceRef, transitionTypes) {
    // TODO: This stuff could just go into the reducer. Leaving as-is for now
    // since we're about to rewrite all the router reducer stuff anyway.
    if (transitionTypes) {
        for (const type of transitionTypes){
            (0, _react.addTransitionType)(type);
        }
    }
    const url = new URL((0, _addbasepath.addBasePath)(href), location.href);
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    (0, _links.setLinkForCurrentNavigation)(linkInstanceRef);
    const onRouterTransitionStart = getProfilingHookForOnNavigationStart();
    if (onRouterTransitionStart !== null) {
        onRouterTransitionStart(href, navigateType);
    }
    (0, _useactionqueue.dispatchAppRouterAction)({
        type: _routerreducertypes.ACTION_NAVIGATE,
        url,
        isExternalUrl: (0, _approuterutils.isExternalURL)(url),
        locationSearch: location.search,
        scrollBehavior,
        navigateType
    });
}
function dispatchTraverseAction(href, historyState) {
    const onRouterTransitionStart = getProfilingHookForOnNavigationStart();
    if (onRouterTransitionStart !== null) {
        onRouterTransitionStart(href, 'traverse');
    }
    (0, _useactionqueue.dispatchAppRouterAction)({
        type: _routerreducertypes.ACTION_RESTORE,
        url: new URL(href),
        historyState
    });
}
/**
 * (Experimental) Perform a gesture navigation. This dispatches through React's
 * useOptimistic instead of the main action queue, allowing the state to be
 * shown during a gesture transition and discarded when the canonical navigation
 * completes.
 *
 * Only available when experimental.gestureTransition is enabled.
 */ function gesturePush(href, options) {
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
}
const publicAppRouterInstance = {
    back: ()=>window.history.back(),
    forward: ()=>window.history.forward(),
    prefetch: // data in the router reducer state; it writes into a global mutable
    // cache. So we don't need to dispatch an action.
    (href, options)=>{
        if ((0, _javascripturl.isJavaScriptURLString)(href)) {
            throw Object.defineProperty(new Error('Next.js has blocked a javascript: URL as a security precaution.'), "__NEXT_ERROR_CODE", {
                value: "E978",
                enumerable: false,
                configurable: true
            });
        }
        const actionQueue = getAppRouterActionQueue();
        const prefetchKind = options?.kind ?? _routerreducertypes.PrefetchKind.AUTO;
        // We don't currently offer a way to issue a runtime prefetch via `router.prefetch()`.
        // This will be possible when we update its API to not take a PrefetchKind.
        let fetchStrategy;
        switch(prefetchKind){
            case _routerreducertypes.PrefetchKind.AUTO:
                {
                    // We default to PPR. We'll discover whether or not the route supports it with the initial prefetch.
                    fetchStrategy = _types.FetchStrategy.PPR;
                    break;
                }
            case _routerreducertypes.PrefetchKind.FULL:
                {
                    fetchStrategy = _types.FetchStrategy.Full;
                    break;
                }
            default:
                {
                    prefetchKind;
                    // Despite typescript thinking that this can't happen,
                    // we might get an unexpected value from user code.
                    // We don't know what they want, but we know they want a prefetch,
                    // so use the default.
                    fetchStrategy = _types.FetchStrategy.PPR;
                }
        }
        (0, _prefetch.prefetch)(href, actionQueue.state.nextUrl, actionQueue.state.tree, fetchStrategy, options?.onInvalidate ?? null);
    },
    replace: (href, options)=>{
        if ((0, _javascripturl.isJavaScriptURLString)(href)) {
            throw Object.defineProperty(new Error('Next.js has blocked a javascript: URL as a security precaution.'), "__NEXT_ERROR_CODE", {
                value: "E978",
                enumerable: false,
                configurable: true
            });
        }
        (0, _react.startTransition)(()=>{
            dispatchNavigateAction(href, 'replace', options?.scroll === false ? _routerreducertypes.ScrollBehavior.NoScroll : _routerreducertypes.ScrollBehavior.Default, null, options?.transitionTypes);
        });
    },
    push: (href, options)=>{
        if ((0, _javascripturl.isJavaScriptURLString)(href)) {
            throw Object.defineProperty(new Error('Next.js has blocked a javascript: URL as a security precaution.'), "__NEXT_ERROR_CODE", {
                value: "E978",
                enumerable: false,
                configurable: true
            });
        }
        (0, _react.startTransition)(()=>{
            dispatchNavigateAction(href, 'push', options?.scroll === false ? _routerreducertypes.ScrollBehavior.NoScroll : _routerreducertypes.ScrollBehavior.Default, null, options?.transitionTypes);
        });
    },
    refresh: ()=>{
        (0, _react.startTransition)(()=>{
            (0, _useactionqueue.dispatchAppRouterAction)({
                type: _routerreducertypes.ACTION_REFRESH
            });
        });
    },
    hmrRefresh: ()=>{
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
        else {
            // Reset the known routes table so that route predictions are cleared
            // when routes change during development.
            (0, _optimisticroutes.resetKnownRoutes)();
            (0, _react.startTransition)(()=>{
                (0, _useactionqueue.dispatchAppRouterAction)({
                    type: _routerreducertypes.ACTION_HMR_REFRESH
                });
            });
        }
    }
};
// Conditionally add experimental_gesturePush when gestureTransition is enabled
if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
;
// Exists for debugging purposes. Don't use in application code.
if (typeof window !== 'undefined' && window.next) {
    window.next.router = publicAppRouterInstance;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-announcer.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "AppRouterAnnouncer", {
    enumerable: true,
    get: function() {
        return AppRouterAnnouncer;
    }
});
const _react = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
const _reactdom = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-dom/index.js [app-client] (ecmascript)");
const ANNOUNCER_TYPE = 'next-route-announcer';
const ANNOUNCER_ID = '__next-route-announcer__';
function getAnnouncerNode() {
    const existingAnnouncer = document.getElementsByName(ANNOUNCER_TYPE)[0];
    if (existingAnnouncer?.shadowRoot?.childNodes[0]) {
        return existingAnnouncer.shadowRoot.childNodes[0];
    } else {
        const container = document.createElement(ANNOUNCER_TYPE);
        container.style.cssText = 'position:absolute';
        const announcer = document.createElement('div');
        announcer.ariaLive = 'assertive';
        announcer.id = ANNOUNCER_ID;
        announcer.role = 'alert';
        announcer.style.cssText = 'position:absolute;border:0;height:1px;margin:-1px;padding:0;width:1px;clip:rect(0 0 0 0);overflow:hidden;white-space:nowrap;word-wrap:normal';
        // Use shadow DOM here to avoid any potential CSS bleed
        const shadow = container.attachShadow({
            mode: 'open'
        });
        shadow.appendChild(announcer);
        document.body.appendChild(container);
        return announcer;
    }
}
function AppRouterAnnouncer({ tree }) {
    const [portalNode, setPortalNode] = (0, _react.useState)(null);
    (0, _react.useEffect)(()=>{
        const announcer = getAnnouncerNode();
        setPortalNode(announcer);
        return ()=>{
            const container = document.getElementsByTagName(ANNOUNCER_TYPE)[0];
            if (container?.isConnected) {
                document.body.removeChild(container);
            }
        };
    }, []);
    const [routeAnnouncement, setRouteAnnouncement] = (0, _react.useState)('');
    const previousTitle = (0, _react.useRef)(undefined);
    (0, _react.useEffect)(()=>{
        let currentTitle = '';
        if (document.title) {
            currentTitle = document.title;
        } else {
            const pageHeader = document.querySelector('h1');
            if (pageHeader) {
                currentTitle = pageHeader.innerText || pageHeader.textContent || '';
            }
        }
        // Only announce the title change, but not for the first load because screen
        // readers do that automatically.
        if (previousTitle.current !== undefined && previousTitle.current !== currentTitle) {
            setRouteAnnouncement(currentTitle);
        }
        previousTitle.current = currentTitle;
    }, [
        tree
    ]);
    return portalNode ? /*#__PURE__*/ (0, _reactdom.createPortal)(routeAnnouncement, portalNode) : null;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/forbidden.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "forbidden", {
    enumerable: true,
    get: function() {
        return forbidden;
    }
});
const _httpaccessfallback = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/http-access-fallback/http-access-fallback.js [app-client] (ecmascript)");
// TODO: Add `forbidden` docs
/**
 * @experimental
 * This function allows you to render the [forbidden.js file](https://nextjs.org/docs/app/api-reference/file-conventions/forbidden)
 * within a route segment as well as inject a tag.
 *
 * `forbidden()` can be used in
 * [Server Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components),
 * [Route Handlers](https://nextjs.org/docs/app/building-your-application/routing/route-handlers), and
 * [Server Actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations).
 *
 * Read more: [Next.js Docs: `forbidden`](https://nextjs.org/docs/app/api-reference/functions/forbidden)
 */ const DIGEST = `${_httpaccessfallback.HTTP_ERROR_FALLBACK_ERROR_CODE};403`;
function forbidden() {
    if ("TURBOPACK compile-time truthy", 1) {
        throw Object.defineProperty(new Error(`\`forbidden()\` is experimental and only allowed to be enabled when \`experimental.authInterrupts\` is enabled.`), "__NEXT_ERROR_CODE", {
            value: "E488",
            enumerable: false,
            configurable: true
        });
    }
    const error = Object.defineProperty(new Error(DIGEST), "__NEXT_ERROR_CODE", {
        value: "E1019",
        enumerable: false,
        configurable: true
    });
    error.digest = DIGEST;
    throw error;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/unauthorized.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "unauthorized", {
    enumerable: true,
    get: function() {
        return unauthorized;
    }
});
const _httpaccessfallback = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/http-access-fallback/http-access-fallback.js [app-client] (ecmascript)");
// TODO: Add `unauthorized` docs
/**
 * @experimental
 * This function allows you to render the [unauthorized.js file](https://nextjs.org/docs/app/api-reference/file-conventions/unauthorized)
 * within a route segment as well as inject a tag.
 *
 * `unauthorized()` can be used in
 * [Server Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components),
 * [Route Handlers](https://nextjs.org/docs/app/building-your-application/routing/route-handlers), and
 * [Server Actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations).
 *
 *
 * Read more: [Next.js Docs: `unauthorized`](https://nextjs.org/docs/app/api-reference/functions/unauthorized)
 */ const DIGEST = `${_httpaccessfallback.HTTP_ERROR_FALLBACK_ERROR_CODE};401`;
function unauthorized() {
    if ("TURBOPACK compile-time truthy", 1) {
        throw Object.defineProperty(new Error(`\`unauthorized()\` is experimental and only allowed to be used when \`experimental.authInterrupts\` is enabled.`), "__NEXT_ERROR_CODE", {
            value: "E411",
            enumerable: false,
            configurable: true
        });
    }
    const error = Object.defineProperty(new Error(DIGEST), "__NEXT_ERROR_CODE", {
        value: "E1002",
        enumerable: false,
        configurable: true
    });
    error.digest = DIGEST;
    throw error;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/unstable-rethrow.browser.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "unstable_rethrow", {
    enumerable: true,
    get: function() {
        return unstable_rethrow;
    }
});
const _bailouttocsr = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/lazy-dynamic/bailout-to-csr.js [app-client] (ecmascript)");
const _isnextroutererror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/is-next-router-error.js [app-client] (ecmascript)");
function unstable_rethrow(error) {
    if ((0, _isnextroutererror.isNextRouterError)(error) || (0, _bailouttocsr.isBailoutToCSRError)(error)) {
        throw error;
    }
    if (error instanceof Error && 'cause' in error) {
        unstable_rethrow(error.cause);
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/hooks-server-context.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    DynamicServerError: null,
    isDynamicServerError: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    DynamicServerError: function() {
        return DynamicServerError;
    },
    isDynamicServerError: function() {
        return isDynamicServerError;
    }
});
const DYNAMIC_ERROR_CODE = 'DYNAMIC_SERVER_USAGE';
class DynamicServerError extends Error {
    constructor(description){
        super(`Dynamic server usage: ${description}`), this.description = description, this.digest = DYNAMIC_ERROR_CODE;
    }
}
function isDynamicServerError(err) {
    if (typeof err !== 'object' || err === null || !('digest' in err) || typeof err.digest !== 'string') {
        return false;
    }
    return err.digest === DYNAMIC_ERROR_CODE;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/static-generation-bailout.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    StaticGenBailoutError: null,
    isStaticGenBailoutError: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    StaticGenBailoutError: function() {
        return StaticGenBailoutError;
    },
    isStaticGenBailoutError: function() {
        return isStaticGenBailoutError;
    }
});
const NEXT_STATIC_GEN_BAILOUT = 'NEXT_STATIC_GEN_BAILOUT';
class StaticGenBailoutError extends Error {
    constructor(...args){
        super(...args), this.code = NEXT_STATIC_GEN_BAILOUT;
    }
}
function isStaticGenBailoutError(error) {
    if (typeof error !== 'object' || error === null || !('code' in error)) {
        return false;
    }
    return error.code === NEXT_STATIC_GEN_BAILOUT;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/unstable-rethrow.server.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "unstable_rethrow", {
    enumerable: true,
    get: function() {
        return unstable_rethrow;
    }
});
const _dynamicrenderingutils = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/server/dynamic-rendering-utils.js [app-client] (ecmascript)");
const _ispostpone = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/server/lib/router-utils/is-postpone.js [app-client] (ecmascript)");
const _bailouttocsr = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/lazy-dynamic/bailout-to-csr.js [app-client] (ecmascript)");
const _isnextroutererror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/is-next-router-error.js [app-client] (ecmascript)");
const _dynamicrendering = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/server/app-render/dynamic-rendering.js [app-client] (ecmascript)");
const _hooksservercontext = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/hooks-server-context.js [app-client] (ecmascript)");
function unstable_rethrow(error) {
    if ((0, _isnextroutererror.isNextRouterError)(error) || (0, _bailouttocsr.isBailoutToCSRError)(error) || (0, _hooksservercontext.isDynamicServerError)(error) || (0, _dynamicrendering.isDynamicPostpone)(error) || (0, _ispostpone.isPostpone)(error) || (0, _dynamicrenderingutils.isHangingPromiseRejectionError)(error) || (0, _dynamicrendering.isPrerenderInterruptedError)(error)) {
        throw error;
    }
    if (error instanceof Error && 'cause' in error) {
        unstable_rethrow(error.cause);
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/unstable-rethrow.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

/**
 * This function should be used to rethrow internal Next.js errors so that they can be handled by the framework.
 * When wrapping an API that uses errors to interrupt control flow, you should use this function before you do any error handling.
 * This function will rethrow the error if it is a Next.js error so it can be handled, otherwise it will do nothing.
 *
 * Read more: [Next.js Docs: `unstable_rethrow`](https://nextjs.org/docs/app/api-reference/functions/unstable_rethrow)
 */ Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "unstable_rethrow", {
    enumerable: true,
    get: function() {
        return unstable_rethrow;
    }
});
const unstable_rethrow = typeof window === 'undefined' ? __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/unstable-rethrow.server.js [app-client] (ecmascript)").unstable_rethrow : __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/unstable-rethrow.browser.js [app-client] (ecmascript)").unstable_rethrow;
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/navigation.react-server.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    ReadonlyURLSearchParams: null,
    RedirectType: null,
    forbidden: null,
    notFound: null,
    permanentRedirect: null,
    redirect: null,
    unauthorized: null,
    unstable_isUnrecognizedActionError: null,
    unstable_rethrow: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    ReadonlyURLSearchParams: function() {
        return _readonlyurlsearchparams.ReadonlyURLSearchParams;
    },
    RedirectType: function() {
        return RedirectType;
    },
    forbidden: function() {
        return _forbidden.forbidden;
    },
    notFound: function() {
        return _notfound.notFound;
    },
    permanentRedirect: function() {
        return _redirect.permanentRedirect;
    },
    redirect: function() {
        return _redirect.redirect;
    },
    unauthorized: function() {
        return _unauthorized.unauthorized;
    },
    unstable_isUnrecognizedActionError: function() {
        return unstable_isUnrecognizedActionError;
    },
    unstable_rethrow: function() {
        return _unstablerethrow.unstable_rethrow;
    }
});
const _readonlyurlsearchparams = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/readonly-url-search-params.js [app-client] (ecmascript)");
const _redirect = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/redirect.js [app-client] (ecmascript)");
const _notfound = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/not-found.js [app-client] (ecmascript)");
const _forbidden = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/forbidden.js [app-client] (ecmascript)");
const _unauthorized = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/unauthorized.js [app-client] (ecmascript)");
const _unstablerethrow = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/unstable-rethrow.js [app-client] (ecmascript)");
function unstable_isUnrecognizedActionError() {
    throw Object.defineProperty(new Error('`unstable_isUnrecognizedActionError` can only be used on the client.'), "__NEXT_ERROR_CODE", {
        value: "E776",
        enumerable: false,
        configurable: true
    });
}
const RedirectType = {
    push: 'push',
    replace: 'replace'
};
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/navigation.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    ReadonlyURLSearchParams: null,
    RedirectType: null,
    ServerInsertedHTMLContext: null,
    forbidden: null,
    notFound: null,
    permanentRedirect: null,
    redirect: null,
    unauthorized: null,
    unstable_isUnrecognizedActionError: null,
    unstable_rethrow: null,
    useParams: null,
    usePathname: null,
    useRouter: null,
    useSearchParams: null,
    useSelectedLayoutSegment: null,
    useSelectedLayoutSegments: null,
    useServerInsertedHTML: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    // We need the same class that was used to instantiate the context value
    // Otherwise instanceof checks will fail in usercode
    ReadonlyURLSearchParams: function() {
        return _hooksclientcontextsharedruntime.ReadonlyURLSearchParams;
    },
    RedirectType: function() {
        return _navigationreactserver.RedirectType;
    },
    ServerInsertedHTMLContext: function() {
        return _serverinsertedhtmlsharedruntime.ServerInsertedHTMLContext;
    },
    forbidden: function() {
        return _navigationreactserver.forbidden;
    },
    notFound: function() {
        return _navigationreactserver.notFound;
    },
    permanentRedirect: function() {
        return _navigationreactserver.permanentRedirect;
    },
    redirect: function() {
        return _navigationreactserver.redirect;
    },
    unauthorized: function() {
        return _navigationreactserver.unauthorized;
    },
    unstable_isUnrecognizedActionError: function() {
        return _unrecognizedactionerror.unstable_isUnrecognizedActionError;
    },
    unstable_rethrow: function() {
        return _navigationreactserver.unstable_rethrow;
    },
    useParams: function() {
        return useParams;
    },
    usePathname: function() {
        return usePathname;
    },
    useRouter: function() {
        return useRouter;
    },
    useSearchParams: function() {
        return useSearchParams;
    },
    useSelectedLayoutSegment: function() {
        return useSelectedLayoutSegment;
    },
    useSelectedLayoutSegments: function() {
        return useSelectedLayoutSegments;
    },
    useServerInsertedHTML: function() {
        return _serverinsertedhtmlsharedruntime.useServerInsertedHTML;
    }
});
const _interop_require_wildcard = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_wildcard.cjs [app-client] (ecmascript)");
const _react = /*#__PURE__*/ _interop_require_wildcard._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)"));
const _approutercontextsharedruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/app-router-context.shared-runtime.js [app-client] (ecmascript)");
const _hooksclientcontextsharedruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/hooks-client-context.shared-runtime.js [app-client] (ecmascript)");
const _segment = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/segment.js [app-client] (ecmascript)");
const _serverinsertedhtmlsharedruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/server-inserted-html.shared-runtime.js [app-client] (ecmascript)");
const _unrecognizedactionerror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/unrecognized-action-error.js [app-client] (ecmascript)");
const _navigationreactserver = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/navigation.react-server.js [app-client] (ecmascript)");
const useDynamicRouteParams = typeof window === 'undefined' ? __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/server/app-render/dynamic-rendering.js [app-client] (ecmascript)").useDynamicRouteParams : undefined;
const useDynamicSearchParams = typeof window === 'undefined' ? __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/server/app-render/dynamic-rendering.js [app-client] (ecmascript)").useDynamicSearchParams : undefined;
const { instrumentParamsForClientValidation, instrumentSearchParamsForClientValidation, expectCompleteParamsInClientValidation } = ("TURBOPACK compile-time falsy", 0) ? "TURBOPACK unreachable" : {};
function useSearchParams() {
    useDynamicSearchParams?.('useSearchParams()');
    const searchParams = (0, _react.useContext)(_hooksclientcontextsharedruntime.SearchParamsContext);
    // In the case where this is `null`, the compat types added in
    // `next-env.d.ts` will add a new overload that changes the return type to
    // include `null`.
    const readonlySearchParams = (0, _react.useMemo)(()=>{
        if (!searchParams) {
            // When the router is not ready in pages, we won't have the search params
            // available.
            return null;
        }
        return new _hooksclientcontextsharedruntime.ReadonlyURLSearchParams(searchParams);
    }, [
        searchParams
    ]);
    // During build-time instant validation, wrap with an proxy
    // so that accessing undeclared search params throws an error.
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    // Instrument with Suspense DevTools (dev-only)
    if (("TURBOPACK compile-time value", "development") !== 'production' && 'use' in _react.default) {
        const navigationPromises = (0, _react.use)(_hooksclientcontextsharedruntime.NavigationPromisesContext);
        if (navigationPromises) {
            return (0, _react.use)(navigationPromises.searchParams);
        }
    }
    return readonlySearchParams;
}
function usePathname() {
    useDynamicRouteParams?.('usePathname()');
    // In the case where this is `null`, the compat types added in `next-env.d.ts`
    // will add a new overload that changes the return type to include `null`.
    const pathname = (0, _react.useContext)(_hooksclientcontextsharedruntime.PathnameContext);
    // During build-time instant validation, error if fallback params exist
    // because usePathname() can't return a sensible value without all params.
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    // Instrument with Suspense DevTools (dev-only)
    if (("TURBOPACK compile-time value", "development") !== 'production' && 'use' in _react.default) {
        const navigationPromises = (0, _react.use)(_hooksclientcontextsharedruntime.NavigationPromisesContext);
        if (navigationPromises) {
            return (0, _react.use)(navigationPromises.pathname);
        }
    }
    return pathname;
}
function useRouter() {
    const router = (0, _react.useContext)(_approutercontextsharedruntime.AppRouterContext);
    if (router === null) {
        throw Object.defineProperty(new Error('invariant expected app router to be mounted'), "__NEXT_ERROR_CODE", {
            value: "E238",
            enumerable: false,
            configurable: true
        });
    }
    return router;
}
function useParams() {
    useDynamicRouteParams?.('useParams()');
    const params = (0, _react.useContext)(_hooksclientcontextsharedruntime.PathParamsContext);
    // During build-time instant validation, wrap with a proxy
    // so that accessing undeclared params throws an error.
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    // Instrument with Suspense DevTools (dev-only)
    if (("TURBOPACK compile-time value", "development") !== 'production' && 'use' in _react.default) {
        const navigationPromises = (0, _react.use)(_hooksclientcontextsharedruntime.NavigationPromisesContext);
        if (navigationPromises) {
            return (0, _react.use)(navigationPromises.params);
        }
    }
    return params;
}
function useSelectedLayoutSegments(parallelRouteKey = 'children') {
    useDynamicRouteParams?.('useSelectedLayoutSegments()');
    const context = (0, _react.useContext)(_approutercontextsharedruntime.LayoutRouterContext);
    // @ts-expect-error This only happens in `pages`. Type is overwritten in navigation.d.ts
    if (!context) return null;
    // During build-time instant validation, error if fallback params exist
    // because useSelectedLayoutSegments() can't return a sensible value without all params.
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    // Instrument with Suspense DevTools (dev-only)
    if (("TURBOPACK compile-time value", "development") !== 'production' && 'use' in _react.default) {
        const navigationPromises = (0, _react.use)(_hooksclientcontextsharedruntime.NavigationPromisesContext);
        if (navigationPromises) {
            const promise = navigationPromises.selectedLayoutSegmentsPromises?.get(parallelRouteKey);
            if (promise) {
                // We should always have a promise here, but if we don't, it's not worth erroring over.
                // We just won't be able to instrument it, but can still provide the value.
                return (0, _react.use)(promise);
            }
        }
    }
    return (0, _segment.getSelectedLayoutSegmentPath)(context.parentTree, parallelRouteKey);
}
function useSelectedLayoutSegment(parallelRouteKey = 'children') {
    useDynamicRouteParams?.('useSelectedLayoutSegment()');
    const navigationPromises = (0, _react.useContext)(_hooksclientcontextsharedruntime.NavigationPromisesContext);
    const selectedLayoutSegments = useSelectedLayoutSegments(parallelRouteKey);
    // During build-time instant validation, error if fallback params exist
    // because useSelectedLayoutSegment() can't return a sensible value without all params.
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    // Instrument with Suspense DevTools (dev-only)
    if (("TURBOPACK compile-time value", "development") !== 'production' && navigationPromises && 'use' in _react.default) {
        const promise = navigationPromises.selectedLayoutSegmentPromises?.get(parallelRouteKey);
        if (promise) {
            // We should always have a promise here, but if we don't, it's not worth erroring over.
            // We just won't be able to instrument it, but can still provide the value.
            return (0, _react.use)(promise);
        }
    }
    return (0, _segment.computeSelectedLayoutSegment)(selectedLayoutSegments, parallelRouteKey);
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/redirect-boundary.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    RedirectBoundary: null,
    RedirectErrorBoundary: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    RedirectBoundary: function() {
        return RedirectBoundary;
    },
    RedirectErrorBoundary: function() {
        return RedirectErrorBoundary;
    }
});
const _interop_require_wildcard = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_wildcard.cjs [app-client] (ecmascript)");
const _jsxruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/jsx-runtime.js [app-client] (ecmascript)");
const _react = /*#__PURE__*/ _interop_require_wildcard._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)"));
const _navigation = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/navigation.js [app-client] (ecmascript)");
const _redirect = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/redirect.js [app-client] (ecmascript)");
const _redirecterror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/redirect-error.js [app-client] (ecmascript)");
function HandleRedirect({ redirect, reset, redirectType }) {
    const router = (0, _navigation.useRouter)();
    (0, _react.useEffect)(()=>{
        _react.default.startTransition(()=>{
            if (redirectType === 'push') {
                router.push(redirect, {});
            } else {
                router.replace(redirect, {});
            }
            reset();
        });
    }, [
        redirect,
        redirectType,
        reset,
        router
    ]);
    return null;
}
class RedirectErrorBoundary extends _react.default.Component {
    constructor(props){
        super(props);
        this.state = {
            redirect: null,
            redirectType: null
        };
    }
    static getDerivedStateFromError(error) {
        if ((0, _redirecterror.isRedirectError)(error)) {
            const url = (0, _redirect.getURLFromRedirectError)(error);
            const redirectType = (0, _redirect.getRedirectTypeFromError)(error);
            if ('handled' in error) {
                // The redirect was already handled. We'll still catch the redirect error
                // so that we can remount the subtree, but we don't actually need to trigger the
                // router.push.
                return {
                    redirect: null,
                    redirectType: null
                };
            }
            return {
                redirect: url,
                redirectType
            };
        }
        // Re-throw if error is not for redirect
        throw error;
    }
    // Explicit type is needed to avoid the generated `.d.ts` having a wide return type that could be specific to the `@types/react` version.
    render() {
        const { redirect, redirectType } = this.state;
        if (redirect !== null && redirectType !== null) {
            return /*#__PURE__*/ (0, _jsxruntime.jsx)(HandleRedirect, {
                redirect: redirect,
                redirectType: redirectType,
                reset: ()=>this.setState({
                        redirect: null
                    })
            });
        }
        return this.props.children;
    }
}
function RedirectBoundary({ children }) {
    const router = (0, _navigation.useRouter)();
    return /*#__PURE__*/ (0, _jsxruntime.jsx)(RedirectErrorBoundary, {
        router: router,
        children: children
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/create-router-cache-key.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "createRouterCacheKey", {
    enumerable: true,
    get: function() {
        return createRouterCacheKey;
    }
});
const _segment = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/segment.js [app-client] (ecmascript)");
function createRouterCacheKey(segment, withoutSearchParameters = false) {
    // if the segment is an array, it means it's a dynamic segment
    // for example, ['lang', 'en', 'd']. We need to convert it to a string to store it as a cache node key.
    if (Array.isArray(segment)) {
        return `${segment[0]}|${segment[1]}|${segment[2]}`;
    }
    // Page segments might have search parameters, ie __PAGE__?foo=bar
    // When `withoutSearchParameters` is true, we only want to return the page segment
    if (withoutSearchParameters && segment.startsWith(_segment.PAGE_SEGMENT_KEY)) {
        return _segment.PAGE_SEGMENT_KEY;
    }
    return segment;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/find-head-in-cache.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "findHeadInCache", {
    enumerable: true,
    get: function() {
        return findHeadInCache;
    }
});
const _segment = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/segment.js [app-client] (ecmascript)");
const _createroutercachekey = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/create-router-cache-key.js [app-client] (ecmascript)");
function findHeadInCache(cache, parallelRoutes) {
    return findHeadInCacheImpl(cache, parallelRoutes, '', '');
}
function findHeadInCacheImpl(cache, parallelRoutes, keyPrefix, keyPrefixWithoutSearchParams) {
    const isLastItem = Object.keys(parallelRoutes).length === 0;
    if (isLastItem) {
        // Returns the entire Cache Node of the segment whose head we will render.
        return [
            cache,
            keyPrefix,
            keyPrefixWithoutSearchParams
        ];
    }
    // First try the 'children' parallel route if it exists
    // when starting from the "root", this corresponds with the main page component
    const parallelRoutesKeys = Object.keys(parallelRoutes).filter((key)=>key !== 'children');
    // if we are at the root, we need to check the children slot first
    if ('children' in parallelRoutes) {
        parallelRoutesKeys.unshift('children');
    }
    const slots = cache.slots;
    if (slots !== null) {
        for (const key of parallelRoutesKeys){
            const [segment, childParallelRoutes] = parallelRoutes[key];
            // If the parallel is not matched and using the default segment,
            // skip searching the head from it.
            if (segment === _segment.DEFAULT_SEGMENT_KEY) {
                continue;
            }
            const childCacheNode = slots[key];
            if (!childCacheNode) {
                continue;
            }
            const cacheKey = (0, _createroutercachekey.createRouterCacheKey)(segment);
            const cacheKeyWithoutSearchParams = (0, _createroutercachekey.createRouterCacheKey)(segment, true);
            const item = findHeadInCacheImpl(childCacheNode, childParallelRoutes, keyPrefix + '/' + cacheKey, keyPrefix + '/' + cacheKeyWithoutSearchParams);
            if (item) {
                return item;
            }
        }
    }
    return null;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/unresolved-thenable.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

/**
 * Create a "Thenable" that does not resolve. This is used to suspend indefinitely when data is not available yet.
 */ Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "unresolvedThenable", {
    enumerable: true,
    get: function() {
        return unresolvedThenable;
    }
});
const unresolvedThenable = {
    then: ()=>{}
};
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/errors/graceful-degrade-boundary.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    GracefulDegradeBoundary: null,
    default: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    GracefulDegradeBoundary: function() {
        return GracefulDegradeBoundary;
    },
    default: function() {
        return _default;
    }
});
const _jsxruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/jsx-runtime.js [app-client] (ecmascript)");
const _react = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
function getDomNodeAttributes(node) {
    const result = {};
    for(let i = 0; i < node.attributes.length; i++){
        const attr = node.attributes[i];
        result[attr.name] = attr.value;
    }
    return result;
}
class GracefulDegradeBoundary extends _react.Component {
    constructor(props){
        super(props);
        this.state = {
            hasError: false
        };
        this.rootHtml = '';
        this.htmlAttributes = {};
        this.htmlRef = /*#__PURE__*/ (0, _react.createRef)();
    }
    static getDerivedStateFromError(_) {
        return {
            hasError: true
        };
    }
    componentDidMount() {
        const htmlNode = this.htmlRef.current;
        if (this.state.hasError && htmlNode) {
            // Reapply the cached HTML attributes to the root element
            Object.entries(this.htmlAttributes).forEach(([key, value])=>{
                htmlNode.setAttribute(key, value);
            });
        }
    }
    render() {
        const { hasError } = this.state;
        // Cache the root HTML content on the first render
        if (typeof window !== 'undefined' && !this.rootHtml) {
            this.rootHtml = document.documentElement.innerHTML;
            this.htmlAttributes = getDomNodeAttributes(document.documentElement);
        }
        if (hasError) {
            // Render the current HTML content without hydration
            return /*#__PURE__*/ (0, _jsxruntime.jsx)("html", {
                ref: this.htmlRef,
                suppressHydrationWarning: true,
                dangerouslySetInnerHTML: {
                    __html: this.rootHtml
                }
            });
        }
        return this.props.children;
    }
}
const _default = GracefulDegradeBoundary;
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/errors/root-error-boundary.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "default", {
    enumerable: true,
    get: function() {
        return RootErrorBoundary;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [app-client] (ecmascript)");
const _jsxruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/jsx-runtime.js [app-client] (ecmascript)");
const _react = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)"));
const _gracefuldegradeboundary = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/errors/graceful-degrade-boundary.js [app-client] (ecmascript)"));
const _errorboundary = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/error-boundary.js [app-client] (ecmascript)");
const _isbot = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/router/utils/is-bot.js [app-client] (ecmascript)");
const isBotUserAgent = typeof window !== 'undefined' && (0, _isbot.isBot)(window.navigator.userAgent);
function RootErrorBoundary({ children, errorComponent, errorStyles, errorScripts }) {
    if (isBotUserAgent) {
        // Preserve existing DOM/HTML for bots to avoid replacing content with an error UI
        // and to keep the original SSR output intact.
        return /*#__PURE__*/ (0, _jsxruntime.jsx)(_gracefuldegradeboundary.default, {
            children: children
        });
    }
    return /*#__PURE__*/ (0, _jsxruntime.jsx)(_errorboundary.ErrorBoundary, {
        errorComponent: errorComponent,
        errorStyles: errorStyles,
        errorScripts: errorScripts,
        children: children
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/navigation-devtools.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    createNestedLayoutNavigationPromises: null,
    createRootNavigationPromises: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    createNestedLayoutNavigationPromises: function() {
        return createNestedLayoutNavigationPromises;
    },
    createRootNavigationPromises: function() {
        return createRootNavigationPromises;
    }
});
const _hooksclientcontextsharedruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/hooks-client-context.shared-runtime.js [app-client] (ecmascript)");
const _segment = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/segment.js [app-client] (ecmascript)");
const layoutSegmentPromisesCache = new WeakMap();
/**
 * Creates instrumented promises for layout segment hooks at a given tree level.
 * This is dev-only code for React Suspense DevTools instrumentation.
 */ function createLayoutSegmentPromises(tree) {
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    // Check if we already have cached promises for this tree
    const cached = layoutSegmentPromisesCache.get(tree);
    if (cached) {
        return cached;
    }
    // Create new promises and cache them
    const segmentPromises = new Map();
    const segmentsPromises = new Map();
    const parallelRoutes = tree[1];
    for (const parallelRouteKey of Object.keys(parallelRoutes)){
        const segments = (0, _segment.getSelectedLayoutSegmentPath)(tree, parallelRouteKey);
        // Use the shared logic to compute the segment value
        const segment = (0, _segment.computeSelectedLayoutSegment)(segments, parallelRouteKey);
        segmentPromises.set(parallelRouteKey, (0, _hooksclientcontextsharedruntime.createDevToolsInstrumentedPromise)('useSelectedLayoutSegment', segment));
        segmentsPromises.set(parallelRouteKey, (0, _hooksclientcontextsharedruntime.createDevToolsInstrumentedPromise)('useSelectedLayoutSegments', segments));
    }
    const result = {
        selectedLayoutSegmentPromises: segmentPromises,
        selectedLayoutSegmentsPromises: segmentsPromises
    };
    // Cache the result for future renders
    layoutSegmentPromisesCache.set(tree, result);
    return result;
}
const rootNavigationPromisesCache = new WeakMap();
function createRootNavigationPromises(tree, pathname, searchParams, pathParams) {
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    // Create stable cache keys from the values
    const searchParamsString = searchParams.toString();
    const pathParamsString = JSON.stringify(pathParams);
    const cacheKey = `${pathname}:${searchParamsString}:${pathParamsString}`;
    // Get or create the cache for this tree
    let treeCache = rootNavigationPromisesCache.get(tree);
    if (!treeCache) {
        treeCache = new Map();
        rootNavigationPromisesCache.set(tree, treeCache);
    }
    // Check if we have cached promises for this combination
    const cached = treeCache.get(cacheKey);
    if (cached) {
        return cached;
    }
    const readonlySearchParams = new _hooksclientcontextsharedruntime.ReadonlyURLSearchParams(searchParams);
    const layoutSegmentPromises = createLayoutSegmentPromises(tree);
    const promises = {
        pathname: (0, _hooksclientcontextsharedruntime.createDevToolsInstrumentedPromise)('usePathname', pathname),
        searchParams: (0, _hooksclientcontextsharedruntime.createDevToolsInstrumentedPromise)('useSearchParams', readonlySearchParams),
        params: (0, _hooksclientcontextsharedruntime.createDevToolsInstrumentedPromise)('useParams', pathParams),
        ...layoutSegmentPromises
    };
    treeCache.set(cacheKey, promises);
    return promises;
}
const nestedLayoutPromisesCache = new WeakMap();
function createNestedLayoutNavigationPromises(tree, parentNavPromises) {
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    const parallelRoutes = tree[1];
    const parallelRouteKeys = Object.keys(parallelRoutes);
    // Only create promises if there are parallel routes at this level
    if (parallelRouteKeys.length === 0) {
        return null;
    }
    // Get or create the cache for this tree
    let treeCache = nestedLayoutPromisesCache.get(tree);
    if (!treeCache) {
        treeCache = new Map();
        nestedLayoutPromisesCache.set(tree, treeCache);
    }
    // Check if we have cached promises for this parent combination
    const cached = treeCache.get(parentNavPromises);
    if (cached) {
        return cached;
    }
    // Create merged promises
    const layoutSegmentPromises = createLayoutSegmentPromises(tree);
    const promises = {
        ...parentNavPromises,
        ...layoutSegmentPromises
    };
    treeCache.set(parentNavPromises, promises);
    return promises;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/http-access-fallback/error-boundary.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
'use client';
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "HTTPAccessFallbackBoundary", {
    enumerable: true,
    get: function() {
        return HTTPAccessFallbackBoundary;
    }
});
const _interop_require_wildcard = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_wildcard.cjs [app-client] (ecmascript)");
const _jsxruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/jsx-runtime.js [app-client] (ecmascript)");
const _react = /*#__PURE__*/ _interop_require_wildcard._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)"));
const _navigationuntracked = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/navigation-untracked.js [app-client] (ecmascript)");
const _httpaccessfallback = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/http-access-fallback/http-access-fallback.js [app-client] (ecmascript)");
const _warnonce = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/utils/warn-once.js [app-client] (ecmascript)");
const _approutercontextsharedruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/app-router-context.shared-runtime.js [app-client] (ecmascript)");
class HTTPAccessFallbackErrorBoundary extends _react.default.Component {
    constructor(props){
        super(props);
        this.state = {
            triggeredStatus: undefined,
            previousPathname: props.pathname
        };
    }
    componentDidCatch() {
        if (("TURBOPACK compile-time value", "development") === 'development' && this.props.missingSlots && this.props.missingSlots.size > 0 && // A missing children slot is the typical not-found case, so no need to warn
        !this.props.missingSlots.has('children')) {
            let warningMessage = 'No default component was found for a parallel route rendered on this page. Falling back to nearest NotFound boundary.\n' + 'Learn more: https://nextjs.org/docs/app/building-your-application/routing/parallel-routes#defaultjs\n\n';
            const formattedSlots = Array.from(this.props.missingSlots).sort((a, b)=>a.localeCompare(b)).map((slot)=>`@${slot}`).join(', ');
            warningMessage += 'Missing slots: ' + formattedSlots;
            (0, _warnonce.warnOnce)(warningMessage);
        }
    }
    static getDerivedStateFromError(error) {
        if ((0, _httpaccessfallback.isHTTPAccessFallbackError)(error)) {
            const httpStatus = (0, _httpaccessfallback.getAccessFallbackHTTPStatus)(error);
            return {
                triggeredStatus: httpStatus
            };
        }
        // Re-throw if error is not for 404
        throw error;
    }
    static getDerivedStateFromProps(props, state) {
        /**
     * Handles reset of the error boundary when a navigation happens.
     * Ensures the error boundary does not stay enabled when navigating to a new page.
     * Approach of setState in render is safe as it checks the previous pathname and then overrides
     * it as outlined in https://react.dev/reference/react/useState#storing-information-from-previous-renders
     */ if (props.pathname !== state.previousPathname && state.triggeredStatus) {
            return {
                triggeredStatus: undefined,
                previousPathname: props.pathname
            };
        }
        return {
            triggeredStatus: state.triggeredStatus,
            previousPathname: props.pathname
        };
    }
    render() {
        const { notFound, forbidden, unauthorized, children } = this.props;
        const { triggeredStatus } = this.state;
        const errorComponents = {
            [_httpaccessfallback.HTTPAccessErrorStatus.NOT_FOUND]: notFound,
            [_httpaccessfallback.HTTPAccessErrorStatus.FORBIDDEN]: forbidden,
            [_httpaccessfallback.HTTPAccessErrorStatus.UNAUTHORIZED]: unauthorized
        };
        if (triggeredStatus) {
            const isNotFound = triggeredStatus === _httpaccessfallback.HTTPAccessErrorStatus.NOT_FOUND && notFound;
            const isForbidden = triggeredStatus === _httpaccessfallback.HTTPAccessErrorStatus.FORBIDDEN && forbidden;
            const isUnauthorized = triggeredStatus === _httpaccessfallback.HTTPAccessErrorStatus.UNAUTHORIZED && unauthorized;
            // If there's no matched boundary in this layer, keep throwing the error by rendering the children
            if (!(isNotFound || isForbidden || isUnauthorized)) {
                return children;
            }
            return /*#__PURE__*/ (0, _jsxruntime.jsxs)(_jsxruntime.Fragment, {
                children: [
                    /*#__PURE__*/ (0, _jsxruntime.jsx)("meta", {
                        name: "robots",
                        content: "noindex"
                    }),
                    ("TURBOPACK compile-time value", "development") === 'development' && /*#__PURE__*/ (0, _jsxruntime.jsx)("meta", {
                        name: "boundary-next-error",
                        content: (0, _httpaccessfallback.getAccessFallbackErrorTypeByStatus)(triggeredStatus)
                    }),
                    errorComponents[triggeredStatus]
                ]
            });
        }
        return children;
    }
}
function HTTPAccessFallbackBoundary({ notFound, forbidden, unauthorized, children }) {
    // When we're rendering the missing params shell, this will return null. This
    // is because we won't be rendering any not found boundaries or error
    // boundaries for the missing params shell. When this runs on the client
    // (where these error can occur), we will get the correct pathname.
    const pathname = (0, _navigationuntracked.useUntrackedPathname)();
    const missingSlots = (0, _react.useContext)(_approutercontextsharedruntime.MissingSlotContext);
    const hasErrorFallback = !!(notFound || forbidden || unauthorized);
    if (hasErrorFallback) {
        return /*#__PURE__*/ (0, _jsxruntime.jsx)(HTTPAccessFallbackErrorBoundary, {
            pathname: pathname,
            notFound: notFound,
            forbidden: forbidden,
            unauthorized: unauthorized,
            missingSlots: missingSlots,
            children: children
        });
    }
    return /*#__PURE__*/ (0, _jsxruntime.jsx)(_jsxruntime.Fragment, {
        children: children
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/dev-root-http-access-fallback-boundary.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    DevRootHTTPAccessFallbackBoundary: null,
    bailOnRootNotFound: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    DevRootHTTPAccessFallbackBoundary: function() {
        return DevRootHTTPAccessFallbackBoundary;
    },
    bailOnRootNotFound: function() {
        return bailOnRootNotFound;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [app-client] (ecmascript)");
const _jsxruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/jsx-runtime.js [app-client] (ecmascript)");
const _react = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)"));
const _errorboundary = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/http-access-fallback/error-boundary.js [app-client] (ecmascript)");
function bailOnRootNotFound() {
    throw Object.defineProperty(new Error('notFound() is not allowed to use in root layout'), "__NEXT_ERROR_CODE", {
        value: "E192",
        enumerable: false,
        configurable: true
    });
}
function NotAllowedRootHTTPFallbackError() {
    bailOnRootNotFound();
    return null;
}
function DevRootHTTPAccessFallbackBoundary({ children }) {
    return /*#__PURE__*/ (0, _jsxruntime.jsx)(_errorboundary.HTTPAccessFallbackBoundary, {
        notFound: /*#__PURE__*/ (0, _jsxruntime.jsx)(NotAllowedRootHTTPFallbackError, {}),
        children: children
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/shared.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/get-socket-url.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
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
const _normalizedassetprefix = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/normalized-asset-prefix.js [app-client] (ecmascript)");
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/app/web-socket.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    createProcessTurbopackMessage: null,
    createWebSocket: null,
    useWebSocketPing: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    createProcessTurbopackMessage: function() {
        return createProcessTurbopackMessage;
    },
    createWebSocket: function() {
        return createWebSocket;
    },
    useWebSocketPing: function() {
        return useWebSocketPing;
    }
});
const _react = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
const _approutercontextsharedruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/app-router-context.shared-runtime.js [app-client] (ecmascript)");
const _getsocketurl = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/get-socket-url.js [app-client] (ecmascript)");
const _hotreloadertypes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/server/dev/hot-reloader-types.js [app-client] (ecmascript)");
const _shared = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/shared.js [app-client] (ecmascript)");
const _hotreloaderapp = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/app/hot-reloader-app.js [app-client] (ecmascript)");
const _forwardlogs = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/forward-logs.js [app-client] (ecmascript)");
const _invarianterror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/invariant-error.js [app-client] (ecmascript)");
const _constants = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/constants.js [app-client] (ecmascript)");
let reconnections = 0;
let reloading = false;
let serverSessionId = null;
let mostRecentCompilationHash = null;
function createWebSocket(assetPrefix, staticIndicatorState) {
    if (!self.__next_r) {
        throw Object.defineProperty(new _invarianterror.InvariantError(`Expected a request ID to be defined for the document via self.__next_r.`), "__NEXT_ERROR_CODE", {
            value: "E806",
            enumerable: false,
            configurable: true
        });
    }
    let webSocket;
    let timer;
    const sendMessage = (data)=>{
        if (webSocket && webSocket.readyState === webSocket.OPEN) {
            webSocket.send(data);
        }
    };
    const processTurbopackMessage = createProcessTurbopackMessage(sendMessage);
    function init() {
        if (webSocket) {
            webSocket.close();
        }
        const newWebSocket = new window.WebSocket(`${(0, _getsocketurl.getSocketUrl)(assetPrefix)}/_next/webpack-hmr?id=${self.__next_r}`);
        newWebSocket.binaryType = 'arraybuffer';
        function handleOnline() {
            _forwardlogs.logQueue.onSocketReady(newWebSocket);
            reconnections = 0;
            window.console.log('[HMR] connected');
        }
        function handleMessage(event) {
            // While the page is reloading, don't respond to any more messages.
            if (reloading) {
                return;
            }
            try {
                const message = event.data instanceof ArrayBuffer ? parseBinaryMessage(event.data) : JSON.parse(event.data);
                // Check for server restart in Turbopack mode
                if (message.type === _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.TURBOPACK_CONNECTED) {
                    if (serverSessionId !== null && serverSessionId !== message.data.sessionId) {
                        // Either the server's session id has changed and it's a new server, or
                        // it's been too long since we disconnected and we should reload the page.
                        window.location.reload();
                        reloading = true;
                        return;
                    }
                    serverSessionId = message.data.sessionId;
                }
                // Track webpack compilation hash for server restart detection
                if (message.type === _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.SYNC && 'hash' in message) {
                    // If we had previously reconnected and the hash changed, the server may have restarted
                    if (mostRecentCompilationHash !== null && mostRecentCompilationHash !== message.hash) {
                        window.location.reload();
                        reloading = true;
                        return;
                    }
                    mostRecentCompilationHash = message.hash;
                }
                (0, _hotreloaderapp.processMessage)(message, sendMessage, processTurbopackMessage, staticIndicatorState);
            } catch (err) {
                (0, _shared.reportInvalidHmrMessage)(event, err);
            }
        }
        function handleDisconnect() {
            newWebSocket.onerror = null;
            newWebSocket.onclose = null;
            newWebSocket.close();
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
        newWebSocket.onopen = handleOnline;
        newWebSocket.onerror = handleDisconnect;
        newWebSocket.onclose = handleDisconnect;
        newWebSocket.onmessage = handleMessage;
        webSocket = newWebSocket;
        return newWebSocket;
    }
    return init();
}
function createProcessTurbopackMessage(sendMessage) {
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    let queue = [];
    let callback;
    const processTurbopackMessage = (msg)=>{
        if (callback) {
            callback(msg);
        } else {
            queue.push(msg);
        }
    };
    __turbopack_context__.A("[turbopack]/browser/dev/hmr-client/hmr-client.ts [app-client] (ecmascript, async loader)").then(({ connect })=>{
        connect({
            addMessageListener (cb) {
                callback = cb;
                // Replay all Turbopack messages before we were able to establish the HMR client.
                for (const msg of queue){
                    cb(msg);
                }
                queue.length = 0;
            },
            sendMessage,
            onUpdateError: (err)=>(0, _hotreloaderapp.performFullReload)(err, sendMessage)
        });
    });
    return processTurbopackMessage;
}
function useWebSocketPing(webSocket) {
    const { tree } = (0, _react.useContext)(_approutercontextsharedruntime.GlobalLayoutRouterContext);
    (0, _react.useEffect)(()=>{
        if (!webSocket) {
            throw Object.defineProperty(new _invarianterror.InvariantError('Expected webSocket to be defined in dev mode.'), "__NEXT_ERROR_CODE", {
                value: "E785",
                enumerable: false,
                configurable: true
            });
        }
        // Never send pings when using Turbopack as it's not used.
        // Pings were originally used to keep track of active routes in on-demand-entries with webpack.
        if ("TURBOPACK compile-time truthy", 1) {
            return;
        }
        //TURBOPACK unreachable
        ;
        // Taken from on-demand-entries-client.js
        const interval = undefined;
    }, [
        tree,
        webSocket
    ]);
}
const textDecoder = new TextDecoder();
function parseBinaryMessage(data) {
    assertByteLength(data, 1);
    const view = new DataView(data);
    const messageType = view.getUint8(0);
    switch(messageType){
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.ERRORS_TO_SHOW_IN_BROWSER:
            {
                const serializedErrors = new Uint8Array(data, 1);
                return {
                    type: _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.ERRORS_TO_SHOW_IN_BROWSER,
                    serializedErrors
                };
            }
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.REACT_DEBUG_CHUNK:
            {
                assertByteLength(data, 2);
                const requestIdLength = view.getUint8(1);
                assertByteLength(data, 2 + requestIdLength);
                const requestId = textDecoder.decode(new Uint8Array(data, 2, requestIdLength));
                const chunk = data.byteLength > 2 + requestIdLength ? new Uint8Array(data, 2 + requestIdLength) : null;
                return {
                    type: _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.REACT_DEBUG_CHUNK,
                    requestId,
                    chunk
                };
            }
        default:
            {
                throw Object.defineProperty(new _invarianterror.InvariantError(`Invalid binary HMR message of type ${messageType}`), "__NEXT_ERROR_CODE", {
                    value: "E809",
                    enumerable: false,
                    configurable: true
                });
            }
    }
}
function assertByteLength(data, expectedLength) {
    if (data.byteLength < expectedLength) {
        throw Object.defineProperty(new _invarianterror.InvariantError(`Invalid binary HMR message: insufficient data (expected ${expectedLength} bytes, got ${data.byteLength})`), "__NEXT_ERROR_CODE", {
            value: "E808",
            enumerable: false,
            configurable: true
        });
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/report-hmr-latency.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/turbopack-hot-reloader-common.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/app/hot-reloader-app.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
/// <reference types="webpack/module.d.ts" />
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    default: null,
    performFullReload: null,
    processMessage: null,
    waitForWebpackRuntimeHotUpdate: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    default: function() {
        return HotReload;
    },
    performFullReload: function() {
        return performFullReload;
    },
    processMessage: function() {
        return processMessage;
    },
    waitForWebpackRuntimeHotUpdate: function() {
        return waitForWebpackRuntimeHotUpdate;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [app-client] (ecmascript)");
const _jsxruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/jsx-runtime.js [app-client] (ecmascript)");
const _react = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
const _stripansi = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/strip-ansi/index.js [app-client] (ecmascript)"));
const _formatwebpackmessages = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/format-webpack-messages.js [app-client] (ecmascript)"));
const _shared = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/shared.js [app-client] (ecmascript)");
const _nextdevtools = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/next-devtools/index.js (raw)");
const _replayssronlyerrors = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/errors/replay-ssr-only-errors.js [app-client] (ecmascript)");
const _appdevoverlayerrorboundary = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/app-dev-overlay-error-boundary.js [app-client] (ecmascript)");
const _useerrorhandler = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/errors/use-error-handler.js [app-client] (ecmascript)");
const _runtimeerrorhandler = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/runtime-error-handler.js [app-client] (ecmascript)");
const _websocket = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/app/web-socket.js [app-client] (ecmascript)");
const _hotreloadertypes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/server/dev/hot-reloader-types.js [app-client] (ecmascript)");
const _navigationuntracked = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/navigation-untracked.js [app-client] (ecmascript)");
const _reporthmrlatency = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/report-hmr-latency.js [app-client] (ecmascript)"));
const _turbopackhotreloadercommon = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/turbopack-hot-reloader-common.js [app-client] (ecmascript)");
const _approuterheaders = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-headers.js [app-client] (ecmascript)");
const _approuterinstance = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-instance.js [app-client] (ecmascript)");
const _invarianterror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/invariant-error.js [app-client] (ecmascript)");
const _debugchannel = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/debug-channel.js [app-client] (ecmascript)");
const _client = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-server-dom-turbopack/client.js [app-client] (ecmascript)");
const _appfindsourcemapurl = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/app-find-source-map-url.js [app-client] (ecmascript)");
const createFromReadableStream = _client.createFromReadableStream;
let mostRecentCompilationHash = null;
let __nextDevClientId = Math.round(Math.random() * 100 + Date.now());
let reloading = false;
let webpackStartMsSinceEpoch = null;
const turbopackHmr = ("TURBOPACK compile-time truthy", 1) ? new _turbopackhotreloadercommon.TurbopackHmr() : "TURBOPACK unreachable";
let pendingHotUpdateWebpack = Promise.resolve();
let resolvePendingHotUpdateWebpack = ()=>{};
function setPendingHotUpdateWebpack() {
    pendingHotUpdateWebpack = new Promise((resolve)=>{
        resolvePendingHotUpdateWebpack = ()=>{
            resolve();
        };
    });
}
function waitForWebpackRuntimeHotUpdate() {
    return pendingHotUpdateWebpack;
}
// There is a newer version of the code available.
function handleAvailableHash(hash) {
    // Update last known compilation hash.
    mostRecentCompilationHash = hash;
}
/**
 * Is there a newer version of this code available?
 * For webpack: Check if the hash changed compared to __webpack_hash__
 * For Turbopack: Always true because it doesn't have __webpack_hash__
 */ function isUpdateAvailable() {
    if ("TURBOPACK compile-time truthy", 1) {
        return true;
    }
    //TURBOPACK unreachable
    ;
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
function performFullReload(err, sendMessage) {
    const stackTrace = err && (err.stack && err.stack.split('\n').slice(0, 5).join('\n') || err.message || err + '');
    sendMessage(JSON.stringify({
        event: 'client-full-reload',
        stackTrace,
        hadRuntimeError: !!_runtimeerrorhandler.RuntimeErrorHandler.hadRuntimeError,
        dependencyChain: err ? err.dependencyChain : undefined
    }));
    if (reloading) return;
    reloading = true;
    window.location.reload();
}
// Attempt to update code on the fly, fall back to a hard reload.
function tryApplyUpdatesWebpack(sendMessage) {
    if (!isUpdateAvailable() || !canApplyUpdates()) {
        resolvePendingHotUpdateWebpack();
        _nextdevtools.dispatcher.onBuildOk();
        (0, _reporthmrlatency.default)(sendMessage, [], webpackStartMsSinceEpoch, Date.now());
        return;
    }
    function handleApplyUpdates(err, updatedModules) {
        if (err || _runtimeerrorhandler.RuntimeErrorHandler.hadRuntimeError || updatedModules == null) {
            if (err) {
                console.warn(_shared.REACT_REFRESH_FULL_RELOAD);
            } else if (_runtimeerrorhandler.RuntimeErrorHandler.hadRuntimeError) {
                console.warn(_shared.REACT_REFRESH_FULL_RELOAD_FROM_ERROR);
            }
            performFullReload(err, sendMessage);
            return;
        }
        _nextdevtools.dispatcher.onBuildOk();
        if (isUpdateAvailable()) {
            // While we were updating, there was a new update! Do it again.
            tryApplyUpdatesWebpack(sendMessage);
            return;
        }
        _nextdevtools.dispatcher.onRefresh();
        resolvePendingHotUpdateWebpack();
        (0, _reporthmrlatency.default)(sendMessage, updatedModules, webpackStartMsSinceEpoch, Date.now());
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
function processMessage(message, sendMessage, processTurbopackMessage, staticIndicatorState) {
    function handleErrors(errors) {
        // "Massage" webpack messages.
        const formatted = (0, _formatwebpackmessages.default)({
            errors: errors,
            warnings: []
        });
        // Only show the first error.
        _nextdevtools.dispatcher.onBuildError(formatted.errors[0]);
        // Also log them to the console.
        for(let i = 0; i < formatted.errors.length; i++){
            console.error((0, _stripansi.default)(formatted.errors[i]));
        }
        // Do not attempt to reload now.
        // We will reload on next success instead.
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
    }
    function handleHotUpdate() {
        if ("TURBOPACK compile-time truthy", 1) {
            const hmrUpdate = turbopackHmr.onBuilt();
            if (hmrUpdate != null) {
                (0, _reporthmrlatency.default)(sendMessage, [
                    ...hmrUpdate.updatedModules
                ], hmrUpdate.startMsSinceEpoch, hmrUpdate.endMsSinceEpoch, hmrUpdate.hasUpdates);
            }
            _nextdevtools.dispatcher.onBuildOk();
        } else //TURBOPACK unreachable
        ;
    }
    switch(message.type){
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.ISR_MANIFEST:
            {
                if ("TURBOPACK compile-time truthy", 1) {
                    staticIndicatorState.appIsrManifest = message.data;
                    // Handle the initial static indicator status on receiving the ISR
                    // manifest. Navigation is handled in an effect inside HotReload for
                    // pathname changes as we'll receive the updated manifest before
                    // usePathname triggers for a new value.
                    const isStatic = staticIndicatorState.pathname ? message.data[staticIndicatorState.pathname] : undefined;
                    _nextdevtools.dispatcher.onStaticIndicator(isStatic === undefined ? 'pending' : isStatic ? 'static' : 'dynamic');
                }
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
                if (message.hash) {
                    handleAvailableHash(message.hash);
                }
                const { errors, warnings } = message;
                // Is undefined when it's a 'built' event
                if ('versionInfo' in message) _nextdevtools.dispatcher.onVersionInfo(message.versionInfo);
                if ('debug' in message && message.debug) _nextdevtools.dispatcher.onDebugInfo(message.debug);
                if ('devIndicator' in message) _nextdevtools.dispatcher.onDevIndicator(message.devIndicator);
                if ('devToolsConfig' in message) _nextdevtools.dispatcher.onDevToolsConfig(message.devToolsConfig);
                const hasErrors = Boolean(errors && errors.length);
                // Compilation with errors (e.g. syntax error or missing modules).
                if (hasErrors) {
                    sendMessage(JSON.stringify({
                        event: 'client-error',
                        errorCount: errors.length,
                        clientId: __nextDevClientId
                    }));
                    handleErrors(errors);
                    return;
                }
                const hasWarnings = Boolean(warnings && warnings.length);
                if (hasWarnings) {
                    sendMessage(JSON.stringify({
                        event: 'client-warning',
                        warningCount: warnings.length,
                        clientId: __nextDevClientId
                    }));
                    // Print warnings to the console.
                    const formattedMessages = (0, _formatwebpackmessages.default)({
                        warnings: warnings,
                        errors: []
                    });
                    for(let i = 0; i < formattedMessages.warnings.length; i++){
                        if (i === 5) {
                            console.warn('There were more warnings in other files.\n' + 'You can find a complete log in the terminal.');
                            break;
                        }
                        console.warn((0, _stripansi.default)(formattedMessages.warnings[i]));
                    }
                // No early return here as we need to apply modules in the same way between warnings only and compiles without warnings
                }
                sendMessage(JSON.stringify({
                    event: 'client-success',
                    clientId: __nextDevClientId
                }));
                if (message.type === _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.BUILT) {
                    handleHotUpdate();
                }
                return;
            }
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.TURBOPACK_CONNECTED:
            {
                processTurbopackMessage({
                    type: _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.TURBOPACK_CONNECTED,
                    data: {
                        sessionId: message.data.sessionId
                    }
                });
                break;
            }
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.TURBOPACK_MESSAGE:
            {
                turbopackHmr.onTurbopackMessage(message);
                _nextdevtools.dispatcher.onBeforeRefresh();
                processTurbopackMessage({
                    type: _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.TURBOPACK_MESSAGE,
                    data: message.data
                });
                if (_runtimeerrorhandler.RuntimeErrorHandler.hadRuntimeError) {
                    console.warn(_shared.REACT_REFRESH_FULL_RELOAD_FROM_ERROR);
                    performFullReload(null, sendMessage);
                }
                _nextdevtools.dispatcher.onRefresh();
                break;
            }
        // TODO-APP: make server component change more granular
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.SERVER_COMPONENT_CHANGES:
            {
                turbopackHmr?.onServerComponentChanges();
                sendMessage(JSON.stringify({
                    event: 'server-component-reload-page',
                    clientId: __nextDevClientId,
                    hash: message.hash
                }));
                // Store the latest hash in a session cookie so that it's sent back to the
                // server with any subsequent requests.
                document.cookie = `${_approuterheaders.NEXT_HMR_REFRESH_HASH_COOKIE}=${message.hash};path=/`;
                if (_runtimeerrorhandler.RuntimeErrorHandler.hadRuntimeError || document.documentElement.id === '__next_error__') {
                    if (reloading) return;
                    reloading = true;
                    return window.location.reload();
                }
                (0, _react.startTransition)(()=>{
                    _approuterinstance.publicAppRouterInstance.hmrRefresh();
                    _nextdevtools.dispatcher.onRefresh();
                });
                if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
                ;
                return;
            }
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.RELOAD_PAGE:
            {
                turbopackHmr?.onReloadPage();
                sendMessage(JSON.stringify({
                    event: 'client-reload-page',
                    clientId: __nextDevClientId
                }));
                if (reloading) return;
                reloading = true;
                return window.location.reload();
            }
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.ADDED_PAGE:
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.REMOVED_PAGE:
            {
                turbopackHmr?.onPageAddRemove();
                // TODO-APP: potentially only refresh if the currently viewed page was added/removed.
                return _approuterinstance.publicAppRouterInstance.hmrRefresh();
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
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.DEV_PAGES_MANIFEST_UPDATE:
            {
                return;
            }
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.DEVTOOLS_CONFIG:
            {
                _nextdevtools.dispatcher.onDevToolsConfig(message.data);
                return;
            }
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.REACT_DEBUG_CHUNK:
            {
                const { requestId, chunk } = message;
                const { writer } = (0, _debugchannel.getOrCreateDebugChannelReadableWriterPair)(requestId);
                if (chunk) {
                    writer.ready.then(()=>writer.write(chunk)).catch(console.error);
                } else {
                    // A null chunk signals that no more chunks will be sent, which allows
                    // us to close the writer.
                    // TODO: Revisit this cleanup logic when we integrate the return channel
                    // that keeps the connection open to be able to lazily retrieve debug
                    // objects.
                    writer.ready.then(()=>writer.close()).catch(console.error);
                }
                return;
            }
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.REQUEST_CURRENT_ERROR_STATE:
            {
                const errorState = (0, _nextdevtools.getSerializedOverlayState)();
                const response = {
                    event: _hotreloadertypes.HMR_MESSAGE_SENT_TO_SERVER.MCP_ERROR_STATE_RESPONSE,
                    requestId: message.requestId,
                    errorState,
                    url: window.location.href
                };
                sendMessage(JSON.stringify(response));
                return;
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
                sendMessage(JSON.stringify(response));
                return;
            }
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.CACHE_INDICATOR:
            {
                _nextdevtools.dispatcher.onCacheIndicator(message.state);
                return;
            }
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.ERRORS_TO_SHOW_IN_BROWSER:
            {
                createFromReadableStream(new ReadableStream({
                    start (controller) {
                        controller.enqueue(message.serializedErrors);
                        controller.close();
                    }
                }), {
                    findSourceMapURL: _appfindsourcemapurl.findSourceMapURL
                }).then(({ errors, errorCodes })=>{
                    for (const error of errors){
                        const code = errorCodes.get(error);
                        if (code !== undefined) {
                            Object.defineProperty(error, '__NEXT_ERROR_CODE', {
                                value: code,
                                enumerable: false,
                                configurable: true
                            });
                        }
                        console.error(error);
                    }
                }, (err)=>{
                    console.error(Object.defineProperty(new Error('Failed to deserialize errors.', {
                        cause: err
                    }), "__NEXT_ERROR_CODE", {
                        value: "E946",
                        enumerable: false,
                        configurable: true
                    }));
                });
                return;
            }
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.MIDDLEWARE_CHANGES:
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.CLIENT_CHANGES:
        case _hotreloadertypes.HMR_MESSAGE_SENT_TO_BROWSER.SERVER_ONLY_CHANGES:
            break;
        default:
            {
                message;
            }
    }
}
function HotReload({ children, globalError, webSocket, staticIndicatorState }) {
    (0, _useerrorhandler.useErrorHandler)(_nextdevtools.dispatcher.onUnhandledError, _nextdevtools.dispatcher.onUnhandledRejection);
    (0, _websocket.useWebSocketPing)(webSocket);
    // We don't want access of the pathname for the dev tools to trigger a dynamic
    // access (as the dev overlay will never be present in production).
    const pathname = (0, _navigationuntracked.useUntrackedPathname)();
    if ("TURBOPACK compile-time truthy", 1) {
        // this conditional is only for dead-code elimination which
        // isn't a runtime conditional only build-time so ignore hooks rule
        // eslint-disable-next-line react-hooks/rules-of-hooks
        (0, _react.useEffect)(()=>{
            if (!staticIndicatorState) {
                throw Object.defineProperty(new _invarianterror.InvariantError('Expected staticIndicatorState to be defined in dev mode.'), "__NEXT_ERROR_CODE", {
                    value: "E786",
                    enumerable: false,
                    configurable: true
                });
            }
            staticIndicatorState.pathname = pathname;
            if (staticIndicatorState.appIsrManifest) {
                const isStatic = pathname ? staticIndicatorState.appIsrManifest[pathname] : undefined;
                _nextdevtools.dispatcher.onStaticIndicator(isStatic === undefined ? 'pending' : isStatic ? 'static' : 'dynamic');
            }
        }, [
            pathname,
            staticIndicatorState
        ]);
    }
    return /*#__PURE__*/ (0, _jsxruntime.jsxs)(_appdevoverlayerrorboundary.AppDevOverlayErrorBoundary, {
        globalError: globalError,
        children: [
            /*#__PURE__*/ (0, _jsxruntime.jsx)(_replayssronlyerrors.ReplaySsrOnlyErrors, {
                onBlockingError: _nextdevtools.dispatcher.openErrorOverlay
            }),
            children
        ]
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "default", {
    enumerable: true,
    get: function() {
        return AppRouter;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [app-client] (ecmascript)");
const _interop_require_wildcard = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_wildcard.cjs [app-client] (ecmascript)");
const _jsxruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/jsx-runtime.js [app-client] (ecmascript)");
const _react = /*#__PURE__*/ _interop_require_wildcard._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)"));
const _approutercontextsharedruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/app-router-context.shared-runtime.js [app-client] (ecmascript)");
const _routerreducertypes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/router-reducer-types.js [app-client] (ecmascript)");
const _createhreffromurl = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/create-href-from-url.js [app-client] (ecmascript)");
const _hooksclientcontextsharedruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/hooks-client-context.shared-runtime.js [app-client] (ecmascript)");
const _useactionqueue = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/use-action-queue.js [app-client] (ecmascript)");
const _committedstate = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/committed-state.js [app-client] (ecmascript)");
const _approuterannouncer = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-announcer.js [app-client] (ecmascript)");
const _redirectboundary = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/redirect-boundary.js [app-client] (ecmascript)");
const _findheadincache = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/reducers/find-head-in-cache.js [app-client] (ecmascript)");
const _unresolvedthenable = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/unresolved-thenable.js [app-client] (ecmascript)");
const _removebasepath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/remove-base-path.js [app-client] (ecmascript)");
const _hasbasepath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/has-base-path.js [app-client] (ecmascript)");
const _computechangedpath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/compute-changed-path.js [app-client] (ecmascript)");
const _navfailurehandler = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/nav-failure-handler.js [app-client] (ecmascript)");
const _approuterinstance = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-instance.js [app-client] (ecmascript)");
const _redirect = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/redirect.js [app-client] (ecmascript)");
const _redirecterror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/redirect-error.js [app-client] (ecmascript)");
const _links = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/links.js [app-client] (ecmascript)");
const _rooterrorboundary = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/errors/root-error-boundary.js [app-client] (ecmascript)"));
const _globalerror = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/builtin/global-error.js [app-client] (ecmascript)"));
const _boundarycomponents = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/framework/boundary-components.js [app-client] (ecmascript)");
const _deploymentid = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/deployment-id.js [app-client] (ecmascript)");
const globalMutable = {};
function HistoryUpdater({ appRouterState }) {
    (0, _react.useInsertionEffect)(()=>{
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
        const { tree, pushRef, canonicalUrl, renderedSearch } = appRouterState;
        const appHistoryState = {
            tree,
            renderedSearch
        };
        // TODO: Use Navigation API if available
        const historyState = {
            ...pushRef.preserveCustomHistoryState ? window.history.state : {},
            // Identifier is shortened intentionally.
            // __NA is used to identify if the history entry can be handled by the app-router.
            // __N is used to identify if the history entry can be handled by the old router.
            __NA: true,
            __PRIVATE_NEXTJS_INTERNALS_TREE: appHistoryState
        };
        if (pushRef.pendingPush && // Skip pushing an additional history entry if the canonicalUrl is the same as the current url.
        // This mirrors the browser behavior for normal navigation.
        (0, _createhreffromurl.createHrefFromUrl)(new URL(window.location.href)) !== canonicalUrl) {
            // This intentionally mutates React state, pushRef is overwritten to ensure additional push/replace calls do not trigger an additional history entry.
            pushRef.pendingPush = false;
            window.history.pushState(historyState, '', canonicalUrl);
        } else {
            window.history.replaceState(historyState, '', canonicalUrl);
        }
        (0, _committedstate.setLastCommittedTree)(tree);
    }, [
        appRouterState
    ]);
    (0, _react.useEffect)(()=>{
        // The Next-Url and the base tree may affect the result of a prefetch
        // task. Re-prefetch all visible links with the updated values. In most
        // cases, this will not result in any new network requests, only if
        // the prefetch result actually varies on one of these inputs.
        (0, _links.pingVisibleLinks)(appRouterState.nextUrl, appRouterState.tree);
    }, [
        appRouterState.nextUrl,
        appRouterState.tree
    ]);
    return null;
}
function copyNextJsInternalHistoryState(data) {
    if (data == null) data = {};
    const currentState = window.history.state;
    const __NA = currentState?.__NA;
    if (__NA) {
        data.__NA = __NA;
    }
    const __PRIVATE_NEXTJS_INTERNALS_TREE = currentState?.__PRIVATE_NEXTJS_INTERNALS_TREE;
    if (__PRIVATE_NEXTJS_INTERNALS_TREE) {
        data.__PRIVATE_NEXTJS_INTERNALS_TREE = __PRIVATE_NEXTJS_INTERNALS_TREE;
    }
    return data;
}
function Head({ headCacheNode }) {
    // If this segment has a `prefetchHead`, it's the statically prefetched data.
    // We should use that on initial render instead of `head`. Then we'll switch
    // to `head` when the dynamic response streams in.
    const head = headCacheNode !== null ? headCacheNode.head : null;
    const prefetchHead = headCacheNode !== null ? headCacheNode.prefetchHead : null;
    // If no prefetch data is available, then we go straight to rendering `head`.
    const resolvedPrefetchRsc = prefetchHead !== null ? prefetchHead : head;
    // We use `useDeferredValue` to handle switching between the prefetched and
    // final values. The second argument is returned on initial render, then it
    // re-renders with the first argument.
    return (0, _react.useDeferredValue)(head, resolvedPrefetchRsc);
}
/**
 * The global router that wraps the application components.
 */ function Router({ actionQueue, globalError, webSocket, staticIndicatorState }) {
    const state = (0, _useactionqueue.useActionQueue)(actionQueue);
    const { canonicalUrl } = state;
    // Add memoized pathname/query for useSearchParams and usePathname.
    const { searchParams, pathname } = (0, _react.useMemo)(()=>{
        const url = new URL(canonicalUrl, typeof window === 'undefined' ? 'http://n' : window.location.href);
        return {
            // This is turned into a readonly class in `useSearchParams`
            searchParams: url.searchParams,
            pathname: (0, _hasbasepath.hasBasePath)(url.pathname) ? (0, _removebasepath.removeBasePath)(url.pathname) : url.pathname
        };
    }, [
        canonicalUrl
    ]);
    if ("TURBOPACK compile-time truthy", 1) {
        const { cache, tree } = state;
        // This hook is in a conditional but that is ok because `process.env.NODE_ENV` never changes
        // eslint-disable-next-line react-hooks/rules-of-hooks
        (0, _react.useEffect)(()=>{
            // Add `window.nd` for debugging purposes.
            // This is not meant for use in applications as concurrent rendering will affect the cache/tree/router.
            // @ts-ignore this is for debugging
            window.nd = {
                router: _approuterinstance.publicAppRouterInstance,
                cache,
                tree
            };
        }, [
            cache,
            tree
        ]);
    }
    (0, _react.useEffect)(()=>{
        const sourcePage = (0, _computechangedpath.extractSourcePageFromFlightRouterState)(state.tree);
        if (sourcePage !== undefined) {
            window.next.__internal_src_page = sourcePage;
        } else {
            delete window.next.__internal_src_page;
        }
    }, [
        state.tree
    ]);
    (0, _react.useEffect)(()=>{
        // If the app is restored from bfcache, it's possible that
        // pushRef.mpaNavigation is true, which would mean that any re-render of this component
        // would trigger the mpa navigation logic again from the lines below.
        // This will restore the router to the initial state in the event that the app is restored from bfcache.
        function handlePageShow(event) {
            if (!event.persisted || !window.history.state?.__PRIVATE_NEXTJS_INTERNALS_TREE) {
                return;
            }
            // Clear the pendingMpaPath value so that a subsequent MPA navigation to the same URL can be triggered.
            // This is necessary because if the browser restored from bfcache, the pendingMpaPath would still be set to the value
            // of the last MPA navigation.
            globalMutable.pendingMpaPath = undefined;
            (0, _useactionqueue.dispatchAppRouterAction)({
                type: _routerreducertypes.ACTION_RESTORE,
                url: new URL(window.location.href),
                historyState: window.history.state.__PRIVATE_NEXTJS_INTERNALS_TREE
            });
        }
        window.addEventListener('pageshow', handlePageShow);
        return ()=>{
            window.removeEventListener('pageshow', handlePageShow);
        };
    }, []);
    (0, _react.useEffect)(()=>{
        // Ensure that any redirect errors that bubble up outside of the RedirectBoundary
        // are caught and handled by the router.
        function handleUnhandledRedirect(event) {
            const error = 'reason' in event ? event.reason : event.error;
            if ((0, _redirecterror.isRedirectError)(error)) {
                event.preventDefault();
                const url = (0, _redirect.getURLFromRedirectError)(error);
                const redirectType = (0, _redirect.getRedirectTypeFromError)(error);
                // TODO: This should access the router methods directly, rather than
                // go through the public interface.
                if (redirectType === 'push') {
                    _approuterinstance.publicAppRouterInstance.push(url, {});
                } else {
                    _approuterinstance.publicAppRouterInstance.replace(url, {});
                }
            }
        }
        window.addEventListener('error', handleUnhandledRedirect);
        window.addEventListener('unhandledrejection', handleUnhandledRedirect);
        return ()=>{
            window.removeEventListener('error', handleUnhandledRedirect);
            window.removeEventListener('unhandledrejection', handleUnhandledRedirect);
        };
    }, []);
    // When mpaNavigation flag is set do a hard navigation to the new url.
    // Infinitely suspend because we don't actually want to rerender any child
    // components with the new URL and any entangled state updates shouldn't
    // commit either (eg: useTransition isPending should stay true until the page
    // unloads).
    //
    // This is a side effect in render. Don't try this at home, kids. It's
    // probably safe because we know this is a singleton component and it's never
    // in <Offscreen>. At least I hope so. (It will run twice in dev strict mode,
    // but that's... fine?)
    const { pushRef } = state;
    if (pushRef.mpaNavigation) {
        // if there's a re-render, we don't want to trigger another redirect if one is already in flight to the same URL
        if (globalMutable.pendingMpaPath !== canonicalUrl) {
            const location = window.location;
            if (pushRef.pendingPush) {
                location.assign(canonicalUrl);
            } else {
                location.replace(canonicalUrl);
            }
            globalMutable.pendingMpaPath = canonicalUrl;
        }
        // TODO-APP: Should we listen to navigateerror here to catch failed
        // navigations somehow? And should we call window.stop() if a SPA navigation
        // should interrupt an MPA one?
        // NOTE: This is intentionally using `throw` instead of `use` because we're
        // inside an externally mutable condition (pushRef.mpaNavigation), which
        // violates the rules of hooks.
        throw _unresolvedthenable.unresolvedThenable;
    }
    (0, _react.useEffect)(()=>{
        const originalPushState = window.history.pushState.bind(window.history);
        const originalReplaceState = window.history.replaceState.bind(window.history);
        // Ensure the canonical URL in the Next.js Router is updated when the URL is changed so that `usePathname` and `useSearchParams` hold the pushed values.
        const applyUrlFromHistoryPushReplace = (url)=>{
            const href = window.location.href;
            const appHistoryState = window.history.state?.__PRIVATE_NEXTJS_INTERNALS_TREE;
            (0, _react.startTransition)(()=>{
                (0, _useactionqueue.dispatchAppRouterAction)({
                    type: _routerreducertypes.ACTION_RESTORE,
                    url: new URL(url ?? href, href),
                    historyState: appHistoryState
                });
            });
        };
        /**
     * Patch pushState to ensure external changes to the history are reflected in the Next.js Router.
     * Ensures Next.js internal history state is copied to the new history entry.
     * Ensures usePathname and useSearchParams hold the newly provided url.
     */ window.history.pushState = function pushState(data, _unused, url) {
            // TODO: Warn when Navigation API is available (navigation.navigate() should be used)
            // Avoid a loop when Next.js internals trigger pushState/replaceState
            if (data?.__NA || data?._N) {
                return originalPushState(data, _unused, url);
            }
            data = copyNextJsInternalHistoryState(data);
            if (url) {
                applyUrlFromHistoryPushReplace(url);
            }
            return originalPushState(data, _unused, url);
        };
        /**
     * Patch replaceState to ensure external changes to the history are reflected in the Next.js Router.
     * Ensures Next.js internal history state is copied to the new history entry.
     * Ensures usePathname and useSearchParams hold the newly provided url.
     */ window.history.replaceState = function replaceState(data, _unused, url) {
            // TODO: Warn when Navigation API is available (navigation.navigate() should be used)
            // Avoid a loop when Next.js internals trigger pushState/replaceState
            if (data?.__NA || data?._N) {
                return originalReplaceState(data, _unused, url);
            }
            data = copyNextJsInternalHistoryState(data);
            if (url) {
                applyUrlFromHistoryPushReplace(url);
            }
            return originalReplaceState(data, _unused, url);
        };
        /**
     * Handle popstate event, this is used to handle back/forward in the browser.
     * By default dispatches ACTION_RESTORE, however if the history entry was not pushed/replaced by app-router it will reload the page.
     * That case can happen when the old router injected the history entry.
     */ const onPopState = (event)=>{
            if (!event.state) {
                // TODO-APP: this case only happens when pushState/replaceState was called outside of Next.js. It should probably reload the page in this case.
                return;
            }
            // This case happens when the history entry was pushed by the `pages` router.
            if (!event.state.__NA) {
                window.location.reload();
                return;
            }
            // TODO-APP: Ideally the back button should not use startTransition as it should apply the updates synchronously
            // Without startTransition works if the cache is there for this path
            (0, _react.startTransition)(()=>{
                (0, _approuterinstance.dispatchTraverseAction)(window.location.href, event.state.__PRIVATE_NEXTJS_INTERNALS_TREE);
            });
        };
        // Register popstate event to call onPopstate.
        window.addEventListener('popstate', onPopState);
        return ()=>{
            window.history.pushState = originalPushState;
            window.history.replaceState = originalReplaceState;
            window.removeEventListener('popstate', onPopState);
        };
    }, []);
    const { cache, tree, nextUrl, focusAndScrollRef, previousNextUrl } = state;
    const matchingHead = (0, _react.useMemo)(()=>{
        return (0, _findheadincache.findHeadInCache)(cache, tree[1]);
    }, [
        cache,
        tree
    ]);
    // Add memoized pathParams for useParams.
    const pathParams = (0, _react.useMemo)(()=>{
        return (0, _computechangedpath.getSelectedParams)(tree);
    }, [
        tree
    ]);
    // Create instrumented promises for navigation hooks (dev-only)
    // These are specially instrumented promises to show in the Suspense DevTools
    // Promises are cached outside of render to survive suspense retries.
    let instrumentedNavigationPromises = null;
    if ("TURBOPACK compile-time truthy", 1) {
        const { createRootNavigationPromises } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/navigation-devtools.js [app-client] (ecmascript)");
        instrumentedNavigationPromises = createRootNavigationPromises(tree, pathname, searchParams, pathParams);
    }
    const layoutRouterContext = (0, _react.useMemo)(()=>{
        return {
            parentTree: tree,
            parentCacheNode: cache,
            parentSegmentPath: null,
            parentParams: {},
            parentLoadingData: null,
            // This is the <Activity> "name" that shows up in the Suspense DevTools.
            // It represents the root of the app.
            debugNameContext: '/',
            // Root node always has `url`
            // Provided in AppTreeContext to ensure it can be overwritten in layout-router
            url: canonicalUrl,
            // Root segment is always active
            isActive: true
        };
    }, [
        tree,
        cache,
        canonicalUrl
    ]);
    const globalLayoutRouterContext = (0, _react.useMemo)(()=>{
        return {
            tree,
            focusAndScrollRef,
            nextUrl,
            previousNextUrl
        };
    }, [
        tree,
        focusAndScrollRef,
        nextUrl,
        previousNextUrl
    ]);
    let head;
    if (matchingHead !== null) {
        // The head is wrapped in an extra component so we can use
        // `useDeferredValue` to swap between the prefetched and final versions of
        // the head. (This is what LayoutRouter does for segment data, too.)
        //
        // The `key` is used to remount the component whenever the head moves to
        // a different segment.
        const [headCacheNode, headKey, headKeyWithoutSearchParams] = matchingHead;
        head = /*#__PURE__*/ (0, _jsxruntime.jsx)(Head, {
            headCacheNode: headCacheNode
        }, typeof window === 'undefined' ? headKeyWithoutSearchParams : headKey);
    } else {
        head = null;
    }
    let content = /*#__PURE__*/ (0, _jsxruntime.jsxs)(_redirectboundary.RedirectBoundary, {
        children: [
            head,
            /*#__PURE__*/ (0, _jsxruntime.jsx)(_boundarycomponents.RootLayoutBoundary, {
                children: cache.rsc
            }),
            /*#__PURE__*/ (0, _jsxruntime.jsx)(_approuterannouncer.AppRouterAnnouncer, {
                tree: tree
            })
        ]
    });
    if ("TURBOPACK compile-time truthy", 1) {
        // In development, we apply few error boundaries and hot-reloader:
        // - DevRootHTTPAccessFallbackBoundary: avoid using navigation API like notFound() in root layout
        // - HotReloader:
        //  - hot-reload the app when the code changes
        //  - render dev overlay
        //  - catch runtime errors and display global-error when necessary
        if (typeof window !== 'undefined') {
            const { DevRootHTTPAccessFallbackBoundary } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/dev-root-http-access-fallback-boundary.js [app-client] (ecmascript)");
            content = /*#__PURE__*/ (0, _jsxruntime.jsx)(DevRootHTTPAccessFallbackBoundary, {
                children: content
            });
        }
        const HotReloader = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/app/hot-reloader-app.js [app-client] (ecmascript)").default;
        content = /*#__PURE__*/ (0, _jsxruntime.jsx)(HotReloader, {
            globalError: globalError,
            webSocket: webSocket,
            staticIndicatorState: staticIndicatorState,
            children: content
        });
    } else //TURBOPACK unreachable
    ;
    return /*#__PURE__*/ (0, _jsxruntime.jsxs)(_jsxruntime.Fragment, {
        children: [
            /*#__PURE__*/ (0, _jsxruntime.jsx)(HistoryUpdater, {
                appRouterState: state
            }),
            ("TURBOPACK compile-time truthy", 1) ? null : /*#__PURE__*/ "TURBOPACK unreachable",
            /*#__PURE__*/ (0, _jsxruntime.jsx)(_hooksclientcontextsharedruntime.NavigationPromisesContext.Provider, {
                value: instrumentedNavigationPromises,
                children: /*#__PURE__*/ (0, _jsxruntime.jsx)(_hooksclientcontextsharedruntime.PathParamsContext.Provider, {
                    value: pathParams,
                    children: /*#__PURE__*/ (0, _jsxruntime.jsx)(_hooksclientcontextsharedruntime.PathnameContext.Provider, {
                        value: pathname,
                        children: /*#__PURE__*/ (0, _jsxruntime.jsx)(_hooksclientcontextsharedruntime.SearchParamsContext.Provider, {
                            value: searchParams,
                            children: /*#__PURE__*/ (0, _jsxruntime.jsx)(_approutercontextsharedruntime.GlobalLayoutRouterContext.Provider, {
                                value: globalLayoutRouterContext,
                                children: /*#__PURE__*/ (0, _jsxruntime.jsx)(_approutercontextsharedruntime.AppRouterContext.Provider, {
                                    value: _approuterinstance.publicAppRouterInstance,
                                    children: /*#__PURE__*/ (0, _jsxruntime.jsx)(_approutercontextsharedruntime.LayoutRouterContext.Provider, {
                                        value: layoutRouterContext,
                                        children: content
                                    })
                                })
                            })
                        })
                    })
                })
            })
        ]
    });
}
function AppRouter({ actionQueue, globalErrorState, webSocket, staticIndicatorState }) {
    (0, _navfailurehandler.useNavFailureHandler)();
    const router = /*#__PURE__*/ (0, _jsxruntime.jsx)(Router, {
        actionQueue: actionQueue,
        globalError: globalErrorState,
        webSocket: webSocket,
        staticIndicatorState: staticIndicatorState
    });
    // At the very top level, use the default GlobalError component as the final fallback.
    // When the app router itself fails, which means the framework itself fails, we show the default error.
    return /*#__PURE__*/ (0, _jsxruntime.jsx)(_rooterrorboundary.default, {
        errorComponent: _globalerror.default,
        children: router
    });
}
let runtimeStyles;
let runtimeStyleChanged;
if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
;
function RuntimeStylesForWebpack() {
    const [, forceUpdate] = _react.default.useState(0);
    const renderedStylesSize = runtimeStyles?.size ?? 0;
    (0, _react.useEffect)(()=>{
        if (!runtimeStyles || !runtimeStyleChanged) return;
        const changed = ()=>forceUpdate((c)=>c + 1);
        runtimeStyleChanged.add(changed);
        if (renderedStylesSize !== runtimeStyles.size) {
            changed();
        }
        return ()=>{
            runtimeStyleChanged.delete(changed);
        };
    }, [
        renderedStylesSize,
        forceUpdate
    ]);
    const query = (0, _deploymentid.getAssetTokenQuery)();
    return [
        ...runtimeStyles || []
    ].map((href, i)=>/*#__PURE__*/ (0, _jsxruntime.jsx)("link", {
            rel: "stylesheet",
            href: `${href}${query}`,
            // @ts-ignore
            precedence: "next"
        }, i));
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/create-initial-router-state.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "createInitialRouterState", {
    enumerable: true,
    get: function() {
        return createInitialRouterState;
    }
});
const _createhreffromurl = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/create-href-from-url.js [app-client] (ecmascript)");
const _computechangedpath = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/compute-changed-path.js [app-client] (ecmascript)");
const _flightdatahelpers = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/flight-data-helpers.js [app-client] (ecmascript)");
const _pprnavigations = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/ppr-navigations.js [app-client] (ecmascript)");
const _cache = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/cache.js [app-client] (ecmascript)");
const _types = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/types.js [app-client] (ecmascript)");
const _bfcache = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/bfcache.js [app-client] (ecmascript)");
const _fetchserverresponse = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/fetch-server-response.js [app-client] (ecmascript)");
const _optimisticroutes = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/segment-cache/optimistic-routes.js [app-client] (ecmascript)");
function createInitialRouterState({ navigatedAt, initialRSCPayload, initialFlightStreamForCache, location }) {
    const { c: initialCanonicalUrlParts, f: initialFlightData, q: initialRenderedSearch, i: initialCouldBeIntercepted, S: initialSupportsPerSegmentPrefetching, s: initialStaleTime, l: initialStaticStageByteLength, h: initialHeadVaryParams, p: initialRuntimePrefetchStream, d: initialDynamicStaleTimeSeconds } = initialRSCPayload;
    // When initialized on the server, the canonical URL is provided as an array of parts.
    // This is to ensure that when the RSC payload streamed to the client, crawlers don't interpret it
    // as a URL that should be crawled.
    const initialCanonicalUrl = initialCanonicalUrlParts.join('/');
    const normalizedFlightData = (0, _flightdatahelpers.getFlightDataPartsFromPath)(initialFlightData[0]);
    const { tree: initialTree, seedData: initialSeedData, head: initialHead } = normalizedFlightData;
    // For the SSR render, seed data should always be available (we only send back a `null` response
    // in the case of a `loading` segment, pre-PPR.)
    const canonicalUrl = // This is safe to do as canonicalUrl can't be rendered, it's only used to control the history updates in the useEffect further down in this file.
    location ? (0, _createhreffromurl.createHrefFromUrl)(location) : initialCanonicalUrl;
    // Convert the initial FlightRouterState into the RouteTree type.
    // NOTE: The metadataVaryPath isn't used for anything currently because the
    // head is embedded into the CacheNode tree, but eventually we'll lift it out
    // and store it on the top-level state object.
    //
    // TODO: For statically-generated-at-build-time HTML pages, the
    // FlightRouterState baked into the initial RSC payload won't have the
    // correct segment inlining hints (ParentInlinedIntoSelf, InlinedIntoChild)
    // because those are computed after the pre-render. The client will need to
    // fetch the correct hints from the route tree prefetch (/_tree) response
    // before acting on inlining decisions.
    const acc = {
        metadataVaryPath: null
    };
    const initialRouteTree = (0, _cache.convertRootFlightRouterStateToRouteTree)(initialTree, initialRenderedSearch, acc);
    const metadataVaryPath = acc.metadataVaryPath;
    const initialTask = (0, _pprnavigations.createInitialCacheNodeForHydration)(navigatedAt, initialRouteTree, initialSeedData, initialHead, (0, _bfcache.computeDynamicStaleAt)(navigatedAt, initialDynamicStaleTimeSeconds ?? _bfcache.UnknownDynamicStaleTime));
    // The following only applies in the browser (location !== null) since neither
    // route learning nor segment cache state persists from SSR to client.
    if (location !== null && metadataVaryPath !== null) {
        // Learn the route pattern so we can predict it for future navigations.
        (0, _optimisticroutes.discoverKnownRoute)(Date.now(), location.pathname, null, null, initialRouteTree, metadataVaryPath, initialCouldBeIntercepted, canonicalUrl, initialSupportsPerSegmentPrefetching, false // hasDynamicRewrite
        );
        // Write the initial seed data into the segment cache so subsequent
        // navigations to the initial page can serve cached segments instantly.
        if (initialSeedData !== null && initialStaleTime !== undefined) {
            if (initialStaticStageByteLength !== undefined && initialFlightStreamForCache != null) {
                // Partially static page — truncate the cloned Flight stream at the
                // static stage byte boundary, decode, and cache the static subset.
                (0, _fetchserverresponse.decodeStaticStage)(initialFlightStreamForCache, initialStaticStageByteLength, undefined).then(async (staticStageResponse)=>{
                    const now = Date.now();
                    const staleAt = await (0, _cache.getStaleAt)(now, staticStageResponse.s);
                    (0, _cache.writeStaticStageResponseIntoCache)(now, staticStageResponse.f, undefined, staticStageResponse.h, staleAt, initialTree, initialRenderedSearch, true // isResponsePartial
                    );
                }).catch(()=>{
                // The static stage processing failed. Not fatal — the page
                // rendered normally, we just won't write into the cache.
                });
            } else {
                // Fully static page — cache the entire decoded seed data as-is. We're
                // not using the initial response here (which would allow us to combine
                // the two branches) to avoid unnecessary decoding of the Flight data,
                // since we can just take the seed data that we already decoded during
                // hydration and write it into the cache directly.
                const now = Date.now();
                (0, _cache.getStaleAt)(now, initialStaleTime).then((staleAt)=>{
                    (0, _cache.writeStaticStageResponseIntoCache)(now, initialFlightData, undefined, initialHeadVaryParams, staleAt, initialTree, initialRenderedSearch, false // isResponsePartial
                    );
                }).catch(()=>{
                // The static stage processing failed. Not fatal — the page
                // rendered normally, we just won't write into the cache.
                });
                // Cancel the stream clone — fully static path doesn't need it.
                initialFlightStreamForCache?.cancel();
            }
        } else {
            // No caching — cancel the unused stream clone.
            initialFlightStreamForCache?.cancel();
        }
        // If the initial RSC payload includes an embedded runtime prefetch stream,
        // decode it and write the runtime data into the segment cache. This allows
        // subsequent navigations to serve runtime-prefetchable content from cache
        // without a separate prefetch request.
        if (initialRuntimePrefetchStream != null) {
            (0, _cache.processRuntimePrefetchStream)(Date.now(), initialRuntimePrefetchStream, initialTree, initialRenderedSearch).then((processed)=>{
                if (processed !== null) {
                    (0, _cache.writeDynamicRenderResponseIntoCache)(Date.now(), _types.FetchStrategy.PPRRuntime, processed.flightDatas, processed.buildId, processed.isResponsePartial, processed.headVaryParams, processed.staleAt, processed.navigationSeed, null);
                }
            }).catch(()=>{
            // Runtime prefetch cache write failed. Not fatal — the page rendered
            // normally, we just won't cache runtime data.
            });
        }
    }
    // NOTE: We intentionally don't check if any data needs to be fetched from the
    // server. We assume the initial hydration payload is sufficient to render
    // the page.
    //
    // The completeness of the initial data is an important property that we rely
    // on as a last-ditch mechanism for recovering the app; we must always be able
    // to reload a fresh HTML document to get to a consistent state.
    //
    // In the future, there may be cases where the server intentionally sends
    // partial data and expects the client to fill in the rest, in which case this
    // logic may change. (There already is a similar case where the server sends
    // _no_ hydration data in the HTML document at all, and the client fetches it
    // separately, but that's different because we still end up hydrating with a
    // complete tree.)
    const initialState = {
        tree: initialTask.route,
        cache: initialTask.node,
        pushRef: {
            pendingPush: false,
            mpaNavigation: false,
            // First render needs to preserve the previous window.history.state
            // to avoid it being overwritten on navigation back/forward with MPA Navigation.
            preserveCustomHistoryState: true
        },
        focusAndScrollRef: {
            scrollRef: null,
            forceScroll: false,
            onlyHashChange: false,
            hashFragment: null
        },
        canonicalUrl,
        renderedSearch: initialRenderedSearch,
        // the || operator is intentional, the pathname can be an empty string
        nextUrl: ((0, _computechangedpath.extractPathFromFlightRouterState)(initialTree) || location?.pathname) ?? null,
        previousNextUrl: null,
        debugInfo: null
    };
    return initialState;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/app-link-gc.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "linkGc", {
    enumerable: true,
    get: function() {
        return linkGc;
    }
});
function linkGc() {
    // TODO-APP: Remove this logic when Float has GC built-in in development.
    if ("TURBOPACK compile-time truthy", 1) {
        const callback = (mutationList)=>{
            for (const mutation of mutationList){
                if (mutation.type === 'childList') {
                    for (const node of mutation.addedNodes){
                        if ('tagName' in node && node.tagName === 'LINK') {
                            const link = node;
                            if (link.dataset.precedence?.startsWith('next')) {
                                const href = link.getAttribute('href');
                                if (href) {
                                    const [resource, version] = href.split('?v=', 2);
                                    if (version) {
                                        const currentOrigin = window.location.origin;
                                        const allLinks = [
                                            ...document.querySelectorAll('link[href^="' + resource + '"]'),
                                            // It's possible that the resource is a full URL or only pathname,
                                            // so we need to remove the alternative href as well.
                                            ...document.querySelectorAll('link[href^="' + (resource.startsWith(currentOrigin) ? resource.slice(currentOrigin.length) : currentOrigin + resource) + '"]')
                                        ];
                                        for (const otherLink of allLinks){
                                            if (otherLink.dataset.precedence?.startsWith('next')) {
                                                const otherHref = otherLink.getAttribute('href');
                                                if (otherHref) {
                                                    const [, otherVersion] = otherHref.split('?v=', 2);
                                                    if (!otherVersion || +otherVersion < +version) {
                                                        // Delay the removal of the stylesheet to avoid FOUC
                                                        // caused by `@font-face` rules, as they seem to be
                                                        // a couple of ticks delayed between the old and new
                                                        // styles being swapped even if the font is cached.
                                                        setTimeout(()=>{
                                                            otherLink.remove();
                                                        }, 5);
                                                        const preloadLink = document.querySelector(`link[rel="preload"][as="style"][href="${otherHref}"]`);
                                                        if (preloadLink) {
                                                            preloadLink.remove();
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        };
        // Create an observer instance linked to the callback function
        const observer = new MutationObserver(callback);
        observer.observe(document.head, {
            childList: true
        });
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/app-index.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "hydrate", {
    enumerable: true,
    get: function() {
        return hydrate;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [app-client] (ecmascript)");
const _jsxruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/jsx-runtime.js [app-client] (ecmascript)");
__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/app-globals.js [app-client] (ecmascript)");
const _client = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-dom/client.js [app-client] (ecmascript)"));
const _react = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)"));
const _client1 = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-server-dom-turbopack/client.js [app-client] (ecmascript)");
const _headmanagercontextsharedruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/head-manager-context.shared-runtime.js [app-client] (ecmascript)");
const _onrecoverableerror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/react-client-callbacks/on-recoverable-error.js [app-client] (ecmascript)");
const _errorboundarycallbacks = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/react-client-callbacks/error-boundary-callbacks.js [app-client] (ecmascript)");
const _appcallserver = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/app-call-server.js [app-client] (ecmascript)");
const _appfindsourcemapurl = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/app-find-source-map-url.js [app-client] (ecmascript)");
const _approuterinstance = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router-instance.js [app-client] (ecmascript)");
const _approuter = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/app-router.js [app-client] (ecmascript)"));
const _createinitialrouterstate = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/components/router-reducer/create-initial-router-state.js [app-client] (ecmascript)");
const _approutercontextsharedruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/app-router-context.shared-runtime.js [app-client] (ecmascript)");
const _flightdatahelpers = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/flight-data-helpers.js [app-client] (ecmascript)");
const _deploymentid = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/deployment-id.js [app-client] (ecmascript)");
const _navigationbuildid = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/navigation-build-id.js [app-client] (ecmascript)");
/// <reference types="react-dom/experimental" />
const createFromReadableStream = _client1.createFromReadableStream;
const createFromFetch = _client1.createFromFetch;
const appElement = document;
// Instant Navigation Testing API: captured once at module init. When truthy,
// this is the fetch promise for the static RSC payload (set by an injected
// <script> tag in the static shell HTML).
const instantTestStaticFetch = self.__next_instant_test ? self.__next_instant_test : undefined;
const encoder = new TextEncoder();
let initialServerDataBuffer = undefined;
let initialServerDataWriter = undefined;
let initialServerDataLoaded = false;
let initialServerDataFlushed = false;
let initialFormStateData = null;
function nextServerDataCallback(seg) {
    if (seg[0] === 0) {
        initialServerDataBuffer = [];
    } else if (seg[0] === 1) {
        if (!initialServerDataBuffer) throw Object.defineProperty(new Error('Unexpected server data: missing bootstrap script.'), "__NEXT_ERROR_CODE", {
            value: "E18",
            enumerable: false,
            configurable: true
        });
        if (initialServerDataWriter) {
            initialServerDataWriter.enqueue(encoder.encode(seg[1]));
        } else {
            initialServerDataBuffer.push(seg[1]);
        }
    } else if (seg[0] === 2) {
        initialFormStateData = seg[1];
    } else if (seg[0] === 3) {
        if (!initialServerDataBuffer) throw Object.defineProperty(new Error('Unexpected server data: missing bootstrap script.'), "__NEXT_ERROR_CODE", {
            value: "E18",
            enumerable: false,
            configurable: true
        });
        // Decode the base64 string back to binary data.
        const binaryString = atob(seg[1]);
        const decodedChunk = new Uint8Array(binaryString.length);
        for(var i = 0; i < binaryString.length; i++){
            decodedChunk[i] = binaryString.charCodeAt(i);
        }
        if (initialServerDataWriter) {
            initialServerDataWriter.enqueue(decodedChunk);
        } else {
            initialServerDataBuffer.push(decodedChunk);
        }
    }
}
function isStreamErrorOrUnfinished(ctr) {
    // If `desiredSize` is null, it means the stream is closed or errored. If it is lower than 0, the stream is still unfinished.
    return ctr.desiredSize === null || ctr.desiredSize < 0;
}
// There might be race conditions between `nextServerDataRegisterWriter` and
// `DOMContentLoaded`. The former will be called when React starts to hydrate
// the root, the latter will be called when the DOM is fully loaded.
// For streaming, the former is called first due to partial hydration.
// For non-streaming, the latter can be called first.
// Hence, we use two variables `initialServerDataLoaded` and
// `initialServerDataFlushed` to make sure the writer will be closed and
// `initialServerDataBuffer` will be cleared in the right time.
function nextServerDataRegisterWriter(ctr) {
    if (initialServerDataBuffer) {
        initialServerDataBuffer.forEach((val)=>{
            ctr.enqueue(typeof val === 'string' ? encoder.encode(val) : val);
        });
        if (initialServerDataLoaded && !initialServerDataFlushed) {
            // Instant Navigation Testing API: don't close or error the inline
            // Flight stream. The static shell has no inline Flight data, so the
            // stream is empty. Closing it would cause React to log an error about
            // missing data. Leaving it open lets React treat any holes as
            // "still suspended." Hydration uses the separately fetched RSC payload
            // (self.__next_instant_test), not this stream.
            if (isStreamErrorOrUnfinished(ctr)) {
                if (!instantTestStaticFetch) {
                    ctr.error(Object.defineProperty(new Error('The connection to the page was unexpectedly closed, possibly due to the stop button being clicked, loss of Wi-Fi, or an unstable internet connection.'), "__NEXT_ERROR_CODE", {
                        value: "E117",
                        enumerable: false,
                        configurable: true
                    }));
                }
            } else {
                ctr.close();
            }
            initialServerDataFlushed = true;
            initialServerDataBuffer = undefined;
        }
    }
    initialServerDataWriter = ctr;
}
// When `DOMContentLoaded`, we can close all pending writers to finish hydration.
const DOMContentLoaded = function() {
    if (initialServerDataWriter && !initialServerDataFlushed) {
        initialServerDataWriter.close();
        initialServerDataFlushed = true;
        initialServerDataBuffer = undefined;
    }
    initialServerDataLoaded = true;
};
// It's possible that the DOM is already loaded.
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', DOMContentLoaded, false);
} else {
    // Delayed in marco task to ensure it's executed later than hydration
    setTimeout(DOMContentLoaded);
}
const nextServerDataLoadingGlobal = self.__next_f = self.__next_f || [];
// Consume all buffered chunks and clear the global data array right after to release memory.
// Otherwise it will be retained indefinitely.
nextServerDataLoadingGlobal.forEach(nextServerDataCallback);
nextServerDataLoadingGlobal.length = 0;
// Patch its push method so subsequent chunks are handled (but not actually pushed to the array).
nextServerDataLoadingGlobal.push = nextServerDataCallback;
let readable = new ReadableStream({
    start (controller) {
        nextServerDataRegisterWriter(controller);
    }
});
if ("TURBOPACK compile-time truthy", 1) {
    // @ts-expect-error
    readable.name = 'hydration';
}
// When Cache Components is enabled, tee the inlined Flight stream so we can
// truncate a clone at the static stage byte boundary and cache it. We don't
// know if `l` is present until React decodes the payload, so always tee and
// cancel the clone if not needed.
let initialFlightStreamForCache = null;
if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
;
let debugChannel;
if (("TURBOPACK compile-time value", "1") && ("TURBOPACK compile-time value", true) && typeof window !== 'undefined') {
    const { createDebugChannel } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/debug-channel.js [app-client] (ecmascript)");
    debugChannel = createDebugChannel(undefined);
}
let initialServerResponse;
if (instantTestStaticFetch) {
    // Instant Navigation Testing API: hydrate from the static RSC payload
    // fetch kicked off by an injected <script> tag, instead of the inline
    // Flight data (which is not present in the static shell).
    initialServerResponse = Promise.resolve(createFromFetch(instantTestStaticFetch, {
        callServer: _appcallserver.callServer,
        findSourceMapURL: _appfindsourcemapurl.findSourceMapURL,
        debugChannel,
        // The static fetch response is a partial stream (static-only Flight
        // data with no dynamic content). Allow it to close without error so
        // React treats dynamic holes as still-suspended rather than
        // triggering error recovery.
        unstable_allowPartialStream: true
    })).then(async (initialRSCPayload)=>{
        return (0, _flightdatahelpers.createInitialRSCPayloadFromFallbackPrerender)(await instantTestStaticFetch, initialRSCPayload);
    });
} else if (window.__NEXT_CLIENT_RESUME) {
    const clientResumeFetch = window.__NEXT_CLIENT_RESUME;
    initialServerResponse = Promise.resolve(createFromFetch(clientResumeFetch, {
        callServer: _appcallserver.callServer,
        findSourceMapURL: _appfindsourcemapurl.findSourceMapURL,
        debugChannel
    })).then(async (fallbackInitialRSCPayload)=>(0, _flightdatahelpers.createInitialRSCPayloadFromFallbackPrerender)(await clientResumeFetch, fallbackInitialRSCPayload));
} else {
    initialServerResponse = createFromReadableStream(readable, {
        callServer: _appcallserver.callServer,
        findSourceMapURL: _appfindsourcemapurl.findSourceMapURL,
        debugChannel,
        startTime: 0
    });
}
function ServerRoot({ initialRSCPayload, actionQueue, webSocket, staticIndicatorState }) {
    const router = /*#__PURE__*/ (0, _jsxruntime.jsx)(_approuter.default, {
        actionQueue: actionQueue,
        globalErrorState: initialRSCPayload.G,
        webSocket: webSocket,
        staticIndicatorState: staticIndicatorState
    });
    if (("TURBOPACK compile-time value", "development") === 'development' && initialRSCPayload.m) {
        // We provide missing slot information in a context provider only during development
        // as we log some additional information about the missing slots in the console.
        return /*#__PURE__*/ (0, _jsxruntime.jsx)(_approutercontextsharedruntime.MissingSlotContext, {
            value: initialRSCPayload.m,
            children: router
        });
    }
    return router;
}
const StrictModeIfEnabled = ("TURBOPACK compile-time truthy", 1) ? _react.default.StrictMode : "TURBOPACK unreachable";
function Root({ children }) {
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    return children;
}
const enableTransitionIndicator = ("TURBOPACK compile-time value", false);
function noDefaultTransitionIndicator() {
    return ()=>{};
}
const reactRootOptions = {
    onDefaultTransitionIndicator: ("TURBOPACK compile-time falsy", 0) ? "TURBOPACK unreachable" : noDefaultTransitionIndicator,
    onRecoverableError: _onrecoverableerror.onRecoverableError,
    onCaughtError: _errorboundarycallbacks.onCaughtError,
    onUncaughtError: _errorboundarycallbacks.onUncaughtError
};
async function hydrate(instrumentationHooks, assetPrefix) {
    let staticIndicatorState;
    let webSocket;
    if ("TURBOPACK compile-time truthy", 1) {
        const { createWebSocket } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/app/web-socket.js [app-client] (ecmascript)");
        staticIndicatorState = {
            pathname: null,
            appIsrManifest: null
        };
        webSocket = createWebSocket(assetPrefix, staticIndicatorState);
    }
    const initialRSCPayload = await initialServerResponse;
    // setNavigationBuildId should be called only once, during JS initialization
    // and before any components have hydrated.
    if (initialRSCPayload.b) {
        (0, _navigationbuildid.setNavigationBuildId)(initialRSCPayload.b);
    } else {
        (0, _navigationbuildid.setNavigationBuildId)((0, _deploymentid.getDeploymentId)());
    }
    const initialTimestamp = Date.now();
    const actionQueue = (0, _approuterinstance.createMutableActionQueue)((0, _createinitialrouterstate.createInitialRouterState)({
        navigatedAt: initialTimestamp,
        initialRSCPayload,
        initialFlightStreamForCache,
        location: window.location
    }), instrumentationHooks);
    const reactEl = /*#__PURE__*/ (0, _jsxruntime.jsx)(StrictModeIfEnabled, {
        children: /*#__PURE__*/ (0, _jsxruntime.jsx)(_headmanagercontextsharedruntime.HeadManagerContext.Provider, {
            value: {
                appDir: true
            },
            children: /*#__PURE__*/ (0, _jsxruntime.jsx)(Root, {
                children: /*#__PURE__*/ (0, _jsxruntime.jsx)(ServerRoot, {
                    initialRSCPayload: initialRSCPayload,
                    actionQueue: actionQueue,
                    webSocket: webSocket,
                    staticIndicatorState: staticIndicatorState
                })
            })
        })
    });
    if (document.documentElement.id === '__next_error__') {
        let element = reactEl;
        // Server rendering failed, fall back to client-side rendering
        if ("TURBOPACK compile-time truthy", 1) {
            const { RootLevelDevOverlayElement } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/client-entry.js [app-client] (ecmascript)");
            // Note this won't cause hydration mismatch because we are doing CSR w/o hydration
            element = /*#__PURE__*/ (0, _jsxruntime.jsx)(RootLevelDevOverlayElement, {
                children: element
            });
        }
        _client.default.createRoot(appElement, reactRootOptions).render(element);
    } else {
        _react.default.startTransition(()=>{
            _client.default.hydrateRoot(appElement, reactEl, {
                ...reactRootOptions,
                formState: initialFormStateData
            });
        });
    }
    // TODO-APP: Remove this logic when Float has GC built-in in development.
    if ("TURBOPACK compile-time truthy", 1) {
        const { linkGc } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/app-link-gc.js [app-client] (ecmascript)");
        linkGc();
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/app-next-turbopack.js [app-client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/register-deployment-id-global.js [app-client] (ecmascript)");
const _appbootstrap = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/app-bootstrap.js [app-client] (ecmascript)");
const _onrecoverableerror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/react-client-callbacks/on-recoverable-error.js [app-client] (ecmascript)");
window.next.turbopack = true;
self.__webpack_hash__ = '';
// eslint-disable-next-line @next/internal/typechecked-require
const instrumentationHooks = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/require-instrumentation-client.js [app-client] (ecmascript)");
(0, _appbootstrap.appBootstrap)((assetPrefix)=>{
    const { hydrate } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/app-index.js [app-client] (ecmascript)");
    try {
        hydrate(instrumentationHooks, assetPrefix);
    } finally{
        if ("TURBOPACK compile-time truthy", 1) {
            const enableCacheIndicator = ("TURBOPACK compile-time value", false);
            const { getOwnerStack } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/errors/stitched-error.js [app-client] (ecmascript)");
            const { renderAppDevOverlay } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/next-devtools/index.js (raw)");
            renderAppDevOverlay(getOwnerStack, _onrecoverableerror.isRecoverableError, enableCacheIndicator);
        }
    }
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

//# sourceMappingURL=08c5_next_dist_client_0bdkuw2._.js.map