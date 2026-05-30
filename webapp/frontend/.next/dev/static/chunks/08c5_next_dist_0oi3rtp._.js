(globalThis["TURBOPACK"] || (globalThis["TURBOPACK"] = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var _global_process, _global_process1;
module.exports = ((_global_process = /*TURBOPACK member replacement*/ __turbopack_context__.g.process) == null ? void 0 : _global_process.env) && typeof ((_global_process1 = /*TURBOPACK member replacement*/ __turbopack_context__.g.process) == null ? void 0 : _global_process1.env) === 'object' ? /*TURBOPACK member replacement*/ __turbopack_context__.g.process : __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/process/browser.js [client] (ecmascript)");
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/polyfill-module.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {

"trimStart" in String.prototype || (String.prototype.trimStart = String.prototype.trimLeft), "trimEnd" in String.prototype || (String.prototype.trimEnd = String.prototype.trimRight), "description" in Symbol.prototype || Object.defineProperty(Symbol.prototype, "description", {
    configurable: !0,
    get: function() {
        var t = /\((.*)\)/.exec(this.toString());
        return t ? t[1] : void 0;
    }
}), Array.prototype.flat || (Array.prototype.flat = function(t, r) {
    return r = this.concat.apply([], this), t > 1 && r.some(Array.isArray) ? r.flat(t - 1) : r;
}, Array.prototype.flatMap = function(t, r) {
    return this.map(t, r).flat();
}), Promise.prototype.finally || (Promise.prototype.finally = function(t) {
    if ("function" != typeof t) return this.then(t, t);
    var r = this.constructor || Promise;
    return this.then(function(n) {
        return r.resolve(t()).then(function() {
            return n;
        });
    }, function(n) {
        return r.resolve(t()).then(function() {
            throw n;
        });
    });
}), Object.fromEntries || (Object.fromEntries = function(t) {
    return Array.from(t).reduce(function(t, r) {
        return t[r[0]] = r[1], t;
    }, {});
}), Array.prototype.at || (Array.prototype.at = function(t) {
    var r = Math.trunc(t) || 0;
    if (r < 0 && (r += this.length), !(r < 0 || r >= this.length)) return this[r];
}), Object.hasOwn || (Object.hasOwn = function(t, r) {
    if (null == t) throw new TypeError("Cannot convert undefined or null to object");
    return Object.prototype.hasOwnProperty.call(Object(t), r);
}), "canParse" in URL || (URL.canParse = function(t, r) {
    try {
        return !!new URL(t, r);
    } catch (t) {
        return !1;
    }
});
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/route-pattern-normalizer.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    PARAM_SEPARATOR: null,
    hasAdjacentParameterIssues: null,
    normalizeAdjacentParameters: null,
    normalizeTokensForRegexp: null,
    stripNormalizedSeparators: null,
    stripParameterSeparators: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    PARAM_SEPARATOR: function() {
        return PARAM_SEPARATOR;
    },
    hasAdjacentParameterIssues: function() {
        return hasAdjacentParameterIssues;
    },
    normalizeAdjacentParameters: function() {
        return normalizeAdjacentParameters;
    },
    normalizeTokensForRegexp: function() {
        return normalizeTokensForRegexp;
    },
    stripNormalizedSeparators: function() {
        return stripNormalizedSeparators;
    },
    stripParameterSeparators: function() {
        return stripParameterSeparators;
    }
});
const PARAM_SEPARATOR = '_NEXTSEP_';
function hasAdjacentParameterIssues(route) {
    if (typeof route !== 'string') return false;
    // Check for interception route markers followed immediately by parameters
    // Pattern: /(.):param, /(..):param, /(...):param, /(.)(.):param etc.
    // These patterns cause "Must have text between two parameters" errors
    if (/\/\(\.{1,3}\):[^/\s]+/.test(route)) {
        return true;
    }
    // Check for basic adjacent parameters without separators
    // Pattern: :param1:param2 (but not :param* or other URL patterns)
    if (/:[a-zA-Z_][a-zA-Z0-9_]*:[a-zA-Z_][a-zA-Z0-9_]*/.test(route)) {
        return true;
    }
    return false;
}
function normalizeAdjacentParameters(route) {
    let normalized = route;
    // Handle interception route patterns: (.):param -> (.)_NEXTSEP_:param
    normalized = normalized.replace(/(\([^)]*\)):([^/\s]+)/g, `$1${PARAM_SEPARATOR}:$2`);
    // Handle other adjacent parameter patterns: :param1:param2 -> :param1_NEXTSEP_:param2
    normalized = normalized.replace(/:([^:/\s)]+)(?=:)/g, `:$1${PARAM_SEPARATOR}`);
    return normalized;
}
function normalizeTokensForRegexp(tokens) {
    return tokens.map((token)=>{
        // Token union type: Token = string | TokenObject
        // Literal path segments are strings, parameters/wildcards are objects
        if (typeof token === 'object' && token !== null && // Not all token objects have 'modifier' property (e.g., simple text tokens)
        'modifier' in token && // Only repeating modifiers (* or +) cause the validation error
        // Other modifiers like '?' (optional) are fine
        (token.modifier === '*' || token.modifier === '+') && // Token objects can have different shapes depending on route pattern
        'prefix' in token && 'suffix' in token && // Both prefix and suffix must be empty strings
        // This is what causes the validation error in path-to-regexp
        token.prefix === '' && token.suffix === '') {
            // Add minimal prefix to satisfy path-to-regexp validation
            // We use '/' as it's the most common path delimiter and won't break route matching
            // The prefix gets used in regex generation but doesn't affect parameter extraction
            return {
                ...token,
                prefix: '/'
            };
        }
        return token;
    });
}
function stripNormalizedSeparators(pathname) {
    // Remove separator after interception route markers
    // Pattern: (.)_NEXTSEP_ -> (.), (..)_NEXTSEP_ -> (..), etc.
    // The separator appears after the closing paren of interception markers
    return pathname.replace(new RegExp(`\\)${PARAM_SEPARATOR}`, 'g'), ')');
}
function stripParameterSeparators(params) {
    const cleaned = {};
    for (const [key, value] of Object.entries(params)){
        if (typeof value === 'string') {
            // Remove the separator if it appears at the start of parameter values
            cleaned[key] = value.replace(new RegExp(`^${PARAM_SEPARATOR}`), '');
        } else if (Array.isArray(value)) {
            // Handle array parameters (from repeated route segments)
            cleaned[key] = value.map((item)=>typeof item === 'string' ? item.replace(new RegExp(`^${PARAM_SEPARATOR}`), '') : item);
        } else {
            cleaned[key] = value;
        }
    }
    return cleaned;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/constants.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    ACTION_SUFFIX: null,
    APP_DIR_ALIAS: null,
    CACHE_ONE_YEAR_SECONDS: null,
    DOT_NEXT_ALIAS: null,
    ESLINT_DEFAULT_DIRS: null,
    GSP_NO_RETURNED_VALUE: null,
    GSSP_COMPONENT_MEMBER_ERROR: null,
    GSSP_NO_RETURNED_VALUE: null,
    HTML_CONTENT_TYPE_HEADER: null,
    INFINITE_CACHE: null,
    INSTRUMENTATION_HOOK_FILENAME: null,
    JSON_CONTENT_TYPE_HEADER: null,
    MATCHED_PATH_HEADER: null,
    MIDDLEWARE_FILENAME: null,
    MIDDLEWARE_LOCATION_REGEXP: null,
    NEXT_BODY_SUFFIX: null,
    NEXT_CACHE_IMPLICIT_TAG_ID: null,
    NEXT_CACHE_REVALIDATED_TAGS_HEADER: null,
    NEXT_CACHE_REVALIDATE_TAG_TOKEN_HEADER: null,
    NEXT_CACHE_ROOT_PARAM_TAG_ID: null,
    NEXT_CACHE_SOFT_TAG_MAX_LENGTH: null,
    NEXT_CACHE_TAGS_HEADER: null,
    NEXT_CACHE_TAG_MAX_ITEMS: null,
    NEXT_CACHE_TAG_MAX_LENGTH: null,
    NEXT_DATA_SUFFIX: null,
    NEXT_INTERCEPTION_MARKER_PREFIX: null,
    NEXT_META_SUFFIX: null,
    NEXT_NAV_DEPLOYMENT_ID_HEADER: null,
    NEXT_QUERY_PARAM_PREFIX: null,
    NEXT_RESUME_HEADER: null,
    NEXT_RESUME_STATE_LENGTH_HEADER: null,
    NON_STANDARD_NODE_ENV: null,
    PAGES_DIR_ALIAS: null,
    PRERENDER_REVALIDATE_HEADER: null,
    PRERENDER_REVALIDATE_ONLY_GENERATED_HEADER: null,
    PROXY_FILENAME: null,
    PROXY_LOCATION_REGEXP: null,
    PUBLIC_DIR_MIDDLEWARE_CONFLICT: null,
    ROOT_DIR_ALIAS: null,
    RSC_ACTION_CLIENT_WRAPPER_ALIAS: null,
    RSC_ACTION_ENCRYPTION_ALIAS: null,
    RSC_ACTION_PROXY_ALIAS: null,
    RSC_ACTION_VALIDATE_ALIAS: null,
    RSC_CACHE_WRAPPER_ALIAS: null,
    RSC_DYNAMIC_IMPORT_WRAPPER_ALIAS: null,
    RSC_MOD_REF_PROXY_ALIAS: null,
    RSC_SEGMENTS_DIR_SUFFIX: null,
    RSC_SEGMENT_SUFFIX: null,
    RSC_SUFFIX: null,
    SERVER_PROPS_EXPORT_ERROR: null,
    SERVER_PROPS_GET_INIT_PROPS_CONFLICT: null,
    SERVER_PROPS_SSG_CONFLICT: null,
    SERVER_RUNTIME: null,
    SSG_FALLBACK_EXPORT_ERROR: null,
    SSG_GET_INITIAL_PROPS_CONFLICT: null,
    STATIC_STATUS_PAGE_GET_INITIAL_PROPS_ERROR: null,
    TEXT_PLAIN_CONTENT_TYPE_HEADER: null,
    UNSTABLE_REVALIDATE_RENAME_ERROR: null,
    WEBPACK_LAYERS: null,
    WEBPACK_RESOURCE_QUERIES: null,
    WEB_SOCKET_MAX_RECONNECTIONS: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    ACTION_SUFFIX: function() {
        return ACTION_SUFFIX;
    },
    APP_DIR_ALIAS: function() {
        return APP_DIR_ALIAS;
    },
    CACHE_ONE_YEAR_SECONDS: function() {
        return CACHE_ONE_YEAR_SECONDS;
    },
    DOT_NEXT_ALIAS: function() {
        return DOT_NEXT_ALIAS;
    },
    ESLINT_DEFAULT_DIRS: function() {
        return ESLINT_DEFAULT_DIRS;
    },
    GSP_NO_RETURNED_VALUE: function() {
        return GSP_NO_RETURNED_VALUE;
    },
    GSSP_COMPONENT_MEMBER_ERROR: function() {
        return GSSP_COMPONENT_MEMBER_ERROR;
    },
    GSSP_NO_RETURNED_VALUE: function() {
        return GSSP_NO_RETURNED_VALUE;
    },
    HTML_CONTENT_TYPE_HEADER: function() {
        return HTML_CONTENT_TYPE_HEADER;
    },
    INFINITE_CACHE: function() {
        return INFINITE_CACHE;
    },
    INSTRUMENTATION_HOOK_FILENAME: function() {
        return INSTRUMENTATION_HOOK_FILENAME;
    },
    JSON_CONTENT_TYPE_HEADER: function() {
        return JSON_CONTENT_TYPE_HEADER;
    },
    MATCHED_PATH_HEADER: function() {
        return MATCHED_PATH_HEADER;
    },
    MIDDLEWARE_FILENAME: function() {
        return MIDDLEWARE_FILENAME;
    },
    MIDDLEWARE_LOCATION_REGEXP: function() {
        return MIDDLEWARE_LOCATION_REGEXP;
    },
    NEXT_BODY_SUFFIX: function() {
        return NEXT_BODY_SUFFIX;
    },
    NEXT_CACHE_IMPLICIT_TAG_ID: function() {
        return NEXT_CACHE_IMPLICIT_TAG_ID;
    },
    NEXT_CACHE_REVALIDATED_TAGS_HEADER: function() {
        return NEXT_CACHE_REVALIDATED_TAGS_HEADER;
    },
    NEXT_CACHE_REVALIDATE_TAG_TOKEN_HEADER: function() {
        return NEXT_CACHE_REVALIDATE_TAG_TOKEN_HEADER;
    },
    NEXT_CACHE_ROOT_PARAM_TAG_ID: function() {
        return NEXT_CACHE_ROOT_PARAM_TAG_ID;
    },
    NEXT_CACHE_SOFT_TAG_MAX_LENGTH: function() {
        return NEXT_CACHE_SOFT_TAG_MAX_LENGTH;
    },
    NEXT_CACHE_TAGS_HEADER: function() {
        return NEXT_CACHE_TAGS_HEADER;
    },
    NEXT_CACHE_TAG_MAX_ITEMS: function() {
        return NEXT_CACHE_TAG_MAX_ITEMS;
    },
    NEXT_CACHE_TAG_MAX_LENGTH: function() {
        return NEXT_CACHE_TAG_MAX_LENGTH;
    },
    NEXT_DATA_SUFFIX: function() {
        return NEXT_DATA_SUFFIX;
    },
    NEXT_INTERCEPTION_MARKER_PREFIX: function() {
        return NEXT_INTERCEPTION_MARKER_PREFIX;
    },
    NEXT_META_SUFFIX: function() {
        return NEXT_META_SUFFIX;
    },
    NEXT_NAV_DEPLOYMENT_ID_HEADER: function() {
        return NEXT_NAV_DEPLOYMENT_ID_HEADER;
    },
    NEXT_QUERY_PARAM_PREFIX: function() {
        return NEXT_QUERY_PARAM_PREFIX;
    },
    NEXT_RESUME_HEADER: function() {
        return NEXT_RESUME_HEADER;
    },
    NEXT_RESUME_STATE_LENGTH_HEADER: function() {
        return NEXT_RESUME_STATE_LENGTH_HEADER;
    },
    NON_STANDARD_NODE_ENV: function() {
        return NON_STANDARD_NODE_ENV;
    },
    PAGES_DIR_ALIAS: function() {
        return PAGES_DIR_ALIAS;
    },
    PRERENDER_REVALIDATE_HEADER: function() {
        return PRERENDER_REVALIDATE_HEADER;
    },
    PRERENDER_REVALIDATE_ONLY_GENERATED_HEADER: function() {
        return PRERENDER_REVALIDATE_ONLY_GENERATED_HEADER;
    },
    PROXY_FILENAME: function() {
        return PROXY_FILENAME;
    },
    PROXY_LOCATION_REGEXP: function() {
        return PROXY_LOCATION_REGEXP;
    },
    PUBLIC_DIR_MIDDLEWARE_CONFLICT: function() {
        return PUBLIC_DIR_MIDDLEWARE_CONFLICT;
    },
    ROOT_DIR_ALIAS: function() {
        return ROOT_DIR_ALIAS;
    },
    RSC_ACTION_CLIENT_WRAPPER_ALIAS: function() {
        return RSC_ACTION_CLIENT_WRAPPER_ALIAS;
    },
    RSC_ACTION_ENCRYPTION_ALIAS: function() {
        return RSC_ACTION_ENCRYPTION_ALIAS;
    },
    RSC_ACTION_PROXY_ALIAS: function() {
        return RSC_ACTION_PROXY_ALIAS;
    },
    RSC_ACTION_VALIDATE_ALIAS: function() {
        return RSC_ACTION_VALIDATE_ALIAS;
    },
    RSC_CACHE_WRAPPER_ALIAS: function() {
        return RSC_CACHE_WRAPPER_ALIAS;
    },
    RSC_DYNAMIC_IMPORT_WRAPPER_ALIAS: function() {
        return RSC_DYNAMIC_IMPORT_WRAPPER_ALIAS;
    },
    RSC_MOD_REF_PROXY_ALIAS: function() {
        return RSC_MOD_REF_PROXY_ALIAS;
    },
    RSC_SEGMENTS_DIR_SUFFIX: function() {
        return RSC_SEGMENTS_DIR_SUFFIX;
    },
    RSC_SEGMENT_SUFFIX: function() {
        return RSC_SEGMENT_SUFFIX;
    },
    RSC_SUFFIX: function() {
        return RSC_SUFFIX;
    },
    SERVER_PROPS_EXPORT_ERROR: function() {
        return SERVER_PROPS_EXPORT_ERROR;
    },
    SERVER_PROPS_GET_INIT_PROPS_CONFLICT: function() {
        return SERVER_PROPS_GET_INIT_PROPS_CONFLICT;
    },
    SERVER_PROPS_SSG_CONFLICT: function() {
        return SERVER_PROPS_SSG_CONFLICT;
    },
    SERVER_RUNTIME: function() {
        return SERVER_RUNTIME;
    },
    SSG_FALLBACK_EXPORT_ERROR: function() {
        return SSG_FALLBACK_EXPORT_ERROR;
    },
    SSG_GET_INITIAL_PROPS_CONFLICT: function() {
        return SSG_GET_INITIAL_PROPS_CONFLICT;
    },
    STATIC_STATUS_PAGE_GET_INITIAL_PROPS_ERROR: function() {
        return STATIC_STATUS_PAGE_GET_INITIAL_PROPS_ERROR;
    },
    TEXT_PLAIN_CONTENT_TYPE_HEADER: function() {
        return TEXT_PLAIN_CONTENT_TYPE_HEADER;
    },
    UNSTABLE_REVALIDATE_RENAME_ERROR: function() {
        return UNSTABLE_REVALIDATE_RENAME_ERROR;
    },
    WEBPACK_LAYERS: function() {
        return WEBPACK_LAYERS;
    },
    WEBPACK_RESOURCE_QUERIES: function() {
        return WEBPACK_RESOURCE_QUERIES;
    },
    WEB_SOCKET_MAX_RECONNECTIONS: function() {
        return WEB_SOCKET_MAX_RECONNECTIONS;
    }
});
const TEXT_PLAIN_CONTENT_TYPE_HEADER = 'text/plain';
const HTML_CONTENT_TYPE_HEADER = 'text/html; charset=utf-8';
const JSON_CONTENT_TYPE_HEADER = 'application/json; charset=utf-8';
const NEXT_QUERY_PARAM_PREFIX = 'nxtP';
const NEXT_INTERCEPTION_MARKER_PREFIX = 'nxtI';
const MATCHED_PATH_HEADER = 'x-matched-path';
const PRERENDER_REVALIDATE_HEADER = 'x-prerender-revalidate';
const PRERENDER_REVALIDATE_ONLY_GENERATED_HEADER = 'x-prerender-revalidate-if-generated';
const RSC_SEGMENTS_DIR_SUFFIX = '.segments';
const RSC_SEGMENT_SUFFIX = '.segment.rsc';
const RSC_SUFFIX = '.rsc';
const ACTION_SUFFIX = '.action';
const NEXT_DATA_SUFFIX = '.json';
const NEXT_META_SUFFIX = '.meta';
const NEXT_BODY_SUFFIX = '.body';
const NEXT_NAV_DEPLOYMENT_ID_HEADER = 'x-nextjs-deployment-id';
const NEXT_CACHE_TAGS_HEADER = 'x-next-cache-tags';
const NEXT_CACHE_REVALIDATED_TAGS_HEADER = 'x-next-revalidated-tags';
const NEXT_CACHE_REVALIDATE_TAG_TOKEN_HEADER = 'x-next-revalidate-tag-token';
const NEXT_RESUME_HEADER = 'next-resume';
const NEXT_RESUME_STATE_LENGTH_HEADER = 'x-next-resume-state-length';
const NEXT_CACHE_TAG_MAX_ITEMS = 128;
const NEXT_CACHE_TAG_MAX_LENGTH = 256;
const NEXT_CACHE_SOFT_TAG_MAX_LENGTH = 1024;
const NEXT_CACHE_IMPLICIT_TAG_ID = '_N_T_';
const NEXT_CACHE_ROOT_PARAM_TAG_ID = '_N_RP_';
const CACHE_ONE_YEAR_SECONDS = 31536000;
const INFINITE_CACHE = 0xfffffffe;
const MIDDLEWARE_FILENAME = 'middleware';
const MIDDLEWARE_LOCATION_REGEXP = `(?:src/)?${MIDDLEWARE_FILENAME}`;
const PROXY_FILENAME = 'proxy';
const PROXY_LOCATION_REGEXP = `(?:src/)?${PROXY_FILENAME}`;
const INSTRUMENTATION_HOOK_FILENAME = 'instrumentation';
const PAGES_DIR_ALIAS = 'private-next-pages';
const DOT_NEXT_ALIAS = 'private-dot-next';
const ROOT_DIR_ALIAS = 'private-next-root-dir';
const APP_DIR_ALIAS = 'private-next-app-dir';
const RSC_MOD_REF_PROXY_ALIAS = 'private-next-rsc-mod-ref-proxy';
const RSC_ACTION_VALIDATE_ALIAS = 'private-next-rsc-action-validate';
const RSC_ACTION_PROXY_ALIAS = 'private-next-rsc-server-reference';
const RSC_CACHE_WRAPPER_ALIAS = 'private-next-rsc-cache-wrapper';
const RSC_DYNAMIC_IMPORT_WRAPPER_ALIAS = 'private-next-rsc-track-dynamic-import';
const RSC_ACTION_ENCRYPTION_ALIAS = 'private-next-rsc-action-encryption';
const RSC_ACTION_CLIENT_WRAPPER_ALIAS = 'private-next-rsc-action-client-wrapper';
const PUBLIC_DIR_MIDDLEWARE_CONFLICT = `You can not have a '_next' folder inside of your public folder. This conflicts with the internal '/_next' route. https://nextjs.org/docs/messages/public-next-folder-conflict`;
const SSG_GET_INITIAL_PROPS_CONFLICT = `You can not use getInitialProps with getStaticProps. To use SSG, please remove your getInitialProps`;
const SERVER_PROPS_GET_INIT_PROPS_CONFLICT = `You can not use getInitialProps with getServerSideProps. Please remove getInitialProps.`;
const SERVER_PROPS_SSG_CONFLICT = `You can not use getStaticProps or getStaticPaths with getServerSideProps. To use SSG, please remove getServerSideProps`;
const STATIC_STATUS_PAGE_GET_INITIAL_PROPS_ERROR = `can not have getInitialProps/getServerSideProps, https://nextjs.org/docs/messages/404-get-initial-props`;
const SERVER_PROPS_EXPORT_ERROR = `pages with \`getServerSideProps\` can not be exported. See more info here: https://nextjs.org/docs/messages/gssp-export`;
const GSP_NO_RETURNED_VALUE = 'Your `getStaticProps` function did not return an object. Did you forget to add a `return`?';
const GSSP_NO_RETURNED_VALUE = 'Your `getServerSideProps` function did not return an object. Did you forget to add a `return`?';
const UNSTABLE_REVALIDATE_RENAME_ERROR = 'The `unstable_revalidate` property is available for general use.\n' + 'Please use `revalidate` instead.';
const GSSP_COMPONENT_MEMBER_ERROR = `can not be attached to a page's component and must be exported from the page. See more info here: https://nextjs.org/docs/messages/gssp-component-member`;
const NON_STANDARD_NODE_ENV = `You are using a non-standard "NODE_ENV" value in your environment. This creates inconsistencies in the project and is strongly advised against. Read more: https://nextjs.org/docs/messages/non-standard-node-env`;
const SSG_FALLBACK_EXPORT_ERROR = `Pages with \`fallback\` enabled in \`getStaticPaths\` can not be exported. See more info here: https://nextjs.org/docs/messages/ssg-fallback-true-export`;
const ESLINT_DEFAULT_DIRS = [
    'app',
    'pages',
    'components',
    'lib',
    'src'
];
const SERVER_RUNTIME = {
    edge: 'edge',
    experimentalEdge: 'experimental-edge',
    nodejs: 'nodejs'
};
const WEB_SOCKET_MAX_RECONNECTIONS = 12;
/**
 * The names of the webpack layers. These layers are the primitives for the
 * webpack chunks.
 */ const WEBPACK_LAYERS_NAMES = {
    /**
   * The layer for the shared code between the client and server bundles.
   */ shared: 'shared',
    /**
   * The layer for server-only runtime and picking up `react-server` export conditions.
   * Including app router RSC pages and app router custom routes and metadata routes.
   */ reactServerComponents: 'rsc',
    /**
   * Server Side Rendering layer for app (ssr).
   */ serverSideRendering: 'ssr',
    /**
   * The browser client bundle layer for actions.
   */ actionBrowser: 'action-browser',
    /**
   * The Node.js bundle layer for the API routes.
   */ apiNode: 'api-node',
    /**
   * The Edge Lite bundle layer for the API routes.
   */ apiEdge: 'api-edge',
    /**
   * The layer for the middleware code.
   */ middleware: 'middleware',
    /**
   * The layer for the instrumentation hooks.
   */ instrument: 'instrument',
    /**
   * The layer for assets on the edge.
   */ edgeAsset: 'edge-asset',
    /**
   * The browser client bundle layer for App directory.
   */ appPagesBrowser: 'app-pages-browser',
    /**
   * The browser client bundle layer for Pages directory.
   */ pagesDirBrowser: 'pages-dir-browser',
    /**
   * The Edge Lite bundle layer for Pages directory.
   */ pagesDirEdge: 'pages-dir-edge',
    /**
   * The Node.js bundle layer for Pages directory.
   */ pagesDirNode: 'pages-dir-node'
};
const WEBPACK_LAYERS = {
    ...WEBPACK_LAYERS_NAMES,
    GROUP: {
        builtinReact: [
            WEBPACK_LAYERS_NAMES.reactServerComponents,
            WEBPACK_LAYERS_NAMES.actionBrowser
        ],
        serverOnly: [
            WEBPACK_LAYERS_NAMES.reactServerComponents,
            WEBPACK_LAYERS_NAMES.actionBrowser,
            WEBPACK_LAYERS_NAMES.instrument,
            WEBPACK_LAYERS_NAMES.middleware
        ],
        neutralTarget: [
            // pages api
            WEBPACK_LAYERS_NAMES.apiNode,
            WEBPACK_LAYERS_NAMES.apiEdge
        ],
        clientOnly: [
            WEBPACK_LAYERS_NAMES.serverSideRendering,
            WEBPACK_LAYERS_NAMES.appPagesBrowser
        ],
        bundled: [
            WEBPACK_LAYERS_NAMES.reactServerComponents,
            WEBPACK_LAYERS_NAMES.actionBrowser,
            WEBPACK_LAYERS_NAMES.serverSideRendering,
            WEBPACK_LAYERS_NAMES.appPagesBrowser,
            WEBPACK_LAYERS_NAMES.shared,
            WEBPACK_LAYERS_NAMES.instrument,
            WEBPACK_LAYERS_NAMES.middleware
        ],
        appPages: [
            // app router pages and layouts
            WEBPACK_LAYERS_NAMES.reactServerComponents,
            WEBPACK_LAYERS_NAMES.serverSideRendering,
            WEBPACK_LAYERS_NAMES.appPagesBrowser,
            WEBPACK_LAYERS_NAMES.actionBrowser
        ]
    }
};
const WEBPACK_RESOURCE_QUERIES = {
    edgeSSREntry: '__next_edge_ssr_entry__',
    metadata: '__next_metadata__',
    metadataRoute: '__next_metadata_route__',
    metadataImageMeta: '__next_metadata_image_meta__'
};
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/is-error.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    default: null,
    getProperError: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    /**
 * Checks whether the given value is a NextError.
 * This can be used to print a more detailed error message with properties like `code` & `digest`.
 */ default: function() {
        return isError;
    },
    getProperError: function() {
        return getProperError;
    }
});
const _isplainobject = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/is-plain-object.js [client] (ecmascript)");
/**
 * This is a safe stringify function that handles circular references.
 * We're using a simpler version here to avoid introducing
 * the dependency `safe-stable-stringify` into production bundle.
 *
 * This helper is used both in development and production.
 */ function safeStringifyLite(obj) {
    const seen = new WeakSet();
    return JSON.stringify(obj, (_key, value)=>{
        // If value is an object and already seen, replace with "[Circular]"
        if (typeof value === 'object' && value !== null) {
            if (seen.has(value)) {
                return '[Circular]';
            }
            seen.add(value);
        }
        return value;
    });
}
function isError(err) {
    return typeof err === 'object' && err !== null && 'name' in err && 'message' in err;
}
function getProperError(err) {
    if (isError(err)) {
        return err;
    }
    if ("TURBOPACK compile-time truthy", 1) {
        // provide better error for case where `throw undefined`
        // is called in development
        if (typeof err === 'undefined') {
            return Object.defineProperty(new Error('An undefined error was thrown, ' + 'see here for more info: https://nextjs.org/docs/messages/threw-undefined'), "__NEXT_ERROR_CODE", {
                value: "E98",
                enumerable: false,
                configurable: true
            });
        }
        if (err === null) {
            return Object.defineProperty(new Error('A null error was thrown, ' + 'see here for more info: https://nextjs.org/docs/messages/threw-undefined'), "__NEXT_ERROR_CODE", {
                value: "E336",
                enumerable: false,
                configurable: true
            });
        }
    }
    return Object.defineProperty(new Error((0, _isplainobject.isPlainObject)(err) ? safeStringifyLite(err) : err + ''), "__NEXT_ERROR_CODE", {
        value: "E394",
        enumerable: false,
        configurable: true
    });
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/is-api-route.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "isAPIRoute", {
    enumerable: true,
    get: function() {
        return isAPIRoute;
    }
});
function isAPIRoute(value) {
    return value === '/api' || Boolean(value == null ? void 0 : value.startsWith('/api/'));
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/require-instrumentation-client.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
/**
 * This module imports the client instrumentation hook from the project root.
 *
 * The `private-next-instrumentation-client` module is automatically aliased to
 * the `instrumentation-client.ts` file in the project root by webpack or turbopack.
 */ "use strict";
if ("TURBOPACK compile-time truthy", 1) {
    const measureName = 'Client Instrumentation Hook';
    const startTime = performance.now();
    // eslint-disable-next-line @next/internal/typechecked-require -- Not a module.
    module.exports = {};
    const endTime = performance.now();
    const duration = endTime - startTime;
    // Using 16ms threshold as it represents one frame (1000ms/60fps)
    // This helps identify if the instrumentation hook initialization
    // could potentially cause frame drops during development.
    const THRESHOLD = 16;
    if (duration > THRESHOLD) {
        console.log(`[${measureName}] Slow execution detected: ${duration.toFixed(0)}ms (Note: Code download overhead is not included in this measurement)`);
    }
} else //TURBOPACK unreachable
;
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/errors/stitched-error.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    coerceError: null,
    decorateDevError: null,
    getOwnerStack: null,
    setOwnerStack: null,
    setOwnerStackIfAvailable: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    coerceError: function() {
        return coerceError;
    },
    decorateDevError: function() {
        return decorateDevError;
    },
    getOwnerStack: function() {
        return getOwnerStack;
    },
    setOwnerStack: function() {
        return setOwnerStack;
    },
    setOwnerStackIfAvailable: function() {
        return setOwnerStackIfAvailable;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [client] (ecmascript)");
const _react = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/react@19.2.6/node_modules/react/index.js [client] (ecmascript)"));
const _iserror = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/is-error.js [client] (ecmascript)"));
const ownerStacks = new WeakMap();
function getOwnerStack(error) {
    return ownerStacks.get(error);
}
function setOwnerStack(error, stack) {
    ownerStacks.set(error, stack);
}
function coerceError(value) {
    return (0, _iserror.default)(value) ? value : Object.defineProperty(new Error('' + value), "__NEXT_ERROR_CODE", {
        value: "E394",
        enumerable: false,
        configurable: true
    });
}
function setOwnerStackIfAvailable(error) {
    // React 18 and prod does not have `captureOwnerStack`
    if ('captureOwnerStack' in _react.default) {
        const ownerStack = _react.default.captureOwnerStack();
        // Only set if we captured a valid owner stack, or if none exists yet.
        // This prevents overwriting a valid owner stack captured earlier
        // (e.g., in onRecoverableError) with null captured later.
        if (ownerStack || !ownerStacks.has(error)) {
            setOwnerStack(error, ownerStack);
        }
    }
}
function decorateDevError(thrownValue) {
    const error = coerceError(thrownValue);
    setOwnerStackIfAvailable(error);
    return error;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/shared/react-18-hydration-error.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    getHydrationWarningType: null,
    isHydrationError: null,
    isHydrationWarning: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    getHydrationWarningType: function() {
        return getHydrationWarningType;
    },
    isHydrationError: function() {
        return isHydrationError;
    },
    isHydrationWarning: function() {
        return isHydrationWarning;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [client] (ecmascript)");
const _iserror = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/lib/is-error.js [client] (ecmascript)"));
function isHydrationError(error) {
    return (0, _iserror.default)(error) && (error.message === 'Hydration failed because the initial UI does not match what was rendered on the server.' || error.message === 'Text content does not match server-rendered HTML.');
}
function isHydrationWarning(message) {
    return isHtmlTagsWarning(message) || isTextInTagsMismatchWarning(message) || isTextWarning(message);
}
// https://github.com/facebook/react/blob/main/packages/react-dom/src/__tests__/ReactDOMHydrationDiff-test.js used as a reference
const htmlTagsWarnings = new Set([
    'Warning: Expected server HTML to contain a matching <%s> in <%s>.%s',
    'Warning: Did not expect server HTML to contain a <%s> in <%s>.%s'
]);
const textAndTagsMismatchWarnings = new Set([
    'Warning: Expected server HTML to contain a matching text node for "%s" in <%s>.%s',
    'Warning: Did not expect server HTML to contain the text node "%s" in <%s>.%s'
]);
const textWarnings = new Set([
    'Warning: Text content did not match. Server: "%s" Client: "%s"%s'
]);
const getHydrationWarningType = (message)=>{
    if (typeof message !== 'string') {
        // TODO: Doesn't make sense to treat no message as a hydration error message.
        // We should bail out somewhere earlier.
        return 'text';
    }
    const normalizedMessage = message.startsWith('Warning: ') ? message : `Warning: ${message}`;
    if (isHtmlTagsWarning(normalizedMessage)) return 'tag';
    if (isTextInTagsMismatchWarning(normalizedMessage)) return 'text-in-tag';
    return 'text';
};
const isHtmlTagsWarning = (message)=>typeof message === 'string' && htmlTagsWarnings.has(message);
const isTextInTagsMismatchWarning = (msg)=>typeof msg === 'string' && textAndTagsMismatchWarnings.has(msg);
const isTextWarning = (msg)=>typeof msg === 'string' && textWarnings.has(msg);
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/shared/react-19-hydration-error.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    NEXTJS_HYDRATION_ERROR_LINK: null,
    REACT_HYDRATION_ERROR_LINK: null,
    getHydrationErrorStackInfo: null,
    isErrorMessageWithComponentStackDiff: null,
    isHydrationError: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    NEXTJS_HYDRATION_ERROR_LINK: function() {
        return NEXTJS_HYDRATION_ERROR_LINK;
    },
    REACT_HYDRATION_ERROR_LINK: function() {
        return REACT_HYDRATION_ERROR_LINK;
    },
    getHydrationErrorStackInfo: function() {
        return getHydrationErrorStackInfo;
    },
    isErrorMessageWithComponentStackDiff: function() {
        return isErrorMessageWithComponentStackDiff;
    },
    isHydrationError: function() {
        return isHydrationError;
    }
});
const REACT_HYDRATION_ERROR_LINK = 'https://react.dev/link/hydration-mismatch';
const NEXTJS_HYDRATION_ERROR_LINK = 'https://nextjs.org/docs/messages/react-hydration-error';
/**
 * Only React 19+ contains component stack diff in the error message
 */ const errorMessagesWithComponentStackDiff = [
    /^In HTML, (.+?) cannot be a child of <(.+?)>\.(.*)\nThis will cause a hydration error\.(.*)/,
    /^In HTML, (.+?) cannot be a descendant of <(.+?)>\.\nThis will cause a hydration error\.(.*)/,
    /^In HTML, text nodes cannot be a child of <(.+?)>\.\nThis will cause a hydration error\./,
    /^In HTML, whitespace text nodes cannot be a child of <(.+?)>\. Make sure you don't have any extra whitespace between tags on each line of your source code\.\nThis will cause a hydration error\./
];
function isHydrationError(error) {
    return isErrorMessageWithComponentStackDiff(error.message) || /Hydration failed because the server rendered (text|HTML) didn't match the client\./.test(error.message) || /A tree hydrated but some attributes of the server rendered HTML didn't match the client properties./.test(error.message);
}
function isErrorMessageWithComponentStackDiff(msg) {
    return errorMessagesWithComponentStackDiff.some((regex)=>regex.test(msg));
}
function getHydrationErrorStackInfo(error) {
    const errorMessage = error.message;
    if (isErrorMessageWithComponentStackDiff(errorMessage)) {
        const [message, diffLog = ''] = errorMessage.split('\n\n');
        const diff = diffLog.trim();
        return {
            message: diff === '' ? errorMessage.trim() : message.trim(),
            diff,
            notes: null
        };
    }
    const [message, maybeComponentStackDiff] = errorMessage.split(`${REACT_HYDRATION_ERROR_LINK}`);
    const trimmedMessage = message.trim();
    // React built-in hydration diff starts with a newline
    if (maybeComponentStackDiff !== undefined && maybeComponentStackDiff.length > 1) {
        const diffs = [];
        maybeComponentStackDiff.split('\n').forEach((line)=>{
            if (line.trim() === '') return;
            if (!line.trim().startsWith('at ')) {
                diffs.push(line);
            }
        });
        const [displayedMessage, ...notes] = trimmedMessage.split('\n\n');
        return {
            message: displayedMessage,
            diff: diffs.join('\n'),
            notes: notes.join('\n\n') || null
        };
    } else {
        const [displayedMessage, ...notes] = trimmedMessage.split('\n\n');
        return {
            message: displayedMessage,
            diff: null,
            notes: notes.join('\n\n')
        };
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/pages/hydration-error-state.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    attachHydrationErrorState: null,
    getSquashedHydrationErrorDetails: null,
    storeHydrationErrorStateFromConsoleArgs: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    attachHydrationErrorState: function() {
        return attachHydrationErrorState;
    },
    getSquashedHydrationErrorDetails: function() {
        return getSquashedHydrationErrorDetails;
    },
    storeHydrationErrorStateFromConsoleArgs: function() {
        return storeHydrationErrorStateFromConsoleArgs;
    }
});
const _react18hydrationerror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/shared/react-18-hydration-error.js [client] (ecmascript)");
const _react19hydrationerror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/shared/react-19-hydration-error.js [client] (ecmascript)");
// We only need this for React 18 or hydration console errors in React 19.
// Once we surface console.error in the dev overlay in pages router, we should only
// use this for React 18.
let hydrationErrorState = {};
const squashedHydrationErrorDetails = new WeakMap();
function getSquashedHydrationErrorDetails(error) {
    return squashedHydrationErrorDetails.has(error) ? squashedHydrationErrorDetails.get(error) : null;
}
function attachHydrationErrorState(error) {
    if (!(0, _react18hydrationerror.isHydrationError)(error) && !(0, _react19hydrationerror.isHydrationError)(error)) {
        return;
    }
    let parsedHydrationErrorState = {};
    // If there's any extra information in the error message to display,
    // append it to the error message details property
    if (hydrationErrorState.warning) {
        // The patched console.error found hydration errors logged by React
        // Append the logged warning to the error message
        parsedHydrationErrorState = {
            // It contains the warning, component stack, server and client tag names
            ...hydrationErrorState
        };
        // Consume the cached hydration diff.
        // This is only required for now when we still squashed the hydration diff log into hydration error.
        // Once the all error is logged to dev overlay in order, this will go away.
        if (hydrationErrorState.reactOutputComponentDiff) {
            parsedHydrationErrorState.reactOutputComponentDiff = hydrationErrorState.reactOutputComponentDiff;
        }
        squashedHydrationErrorDetails.set(error, parsedHydrationErrorState);
    }
}
function storeHydrationErrorStateFromConsoleArgs(...args) {
    let [message, firstContent, secondContent, ...rest] = args;
    if ((0, _react18hydrationerror.isHydrationWarning)(message)) {
        // Some hydration warnings has 4 arguments, some has 3, fallback to the last argument
        // when the 3rd argument is not the component stack but an empty string
        // For some warnings, there's only 1 argument for template.
        // The second argument is the diff or component stack.
        if (args.length === 3) {
            secondContent = '';
        }
        const warning = message.replace(/Warning: /, '').replace('%s', firstContent).replace('%s', secondContent) // remove the last %s from the message
        .replace(/%s/g, '');
        const lastArg = (rest[rest.length - 1] || '').trim();
        hydrationErrorState.reactOutputComponentDiff = generateHydrationDiffReact18(message, firstContent, secondContent, lastArg);
        hydrationErrorState.warning = warning;
    } else if ((0, _react19hydrationerror.isErrorMessageWithComponentStackDiff)(message)) {
        // Some hydration warnings has 4 arguments, some has 3, fallback to the last argument
        // when the 3rd argument is not the component stack but an empty string
        // For some warnings, there's only 1 argument for template.
        // The second argument is the diff or component stack.
        if (args.length === 3) {
            secondContent = '';
        }
        const warning = message.replace('%s', firstContent).replace('%s', secondContent) // remove the last %s from the message
        .replace(/%s/g, '');
        const lastArg = (args[args.length - 1] || '').trim();
        hydrationErrorState.reactOutputComponentDiff = lastArg;
        hydrationErrorState.warning = warning;
    }
}
/*
 * Some hydration errors in React 18 does not have the diff in the error message.
 * Instead it has the error stack trace which is component stack that we can leverage.
 * Will parse the diff from the error stack trace
 *  e.g.
 *  Warning: Expected server HTML to contain a matching <div> in <p>.
 *    at div
 *    at p
 *    at div
 *    at div
 *    at Page
 *  output:
 *    <Page>
 *      <div>
 *        <p>
 *  >       <div>
 *
 */ function generateHydrationDiffReact18(message, firstContent, secondContent, lastArg) {
    const componentStack = lastArg;
    let firstIndex = -1;
    let secondIndex = -1;
    const hydrationWarningType = (0, _react18hydrationerror.getHydrationWarningType)(message);
    // at div\n at Foo\n at Bar (....)\n -> [div, Foo]
    const components = componentStack.split('\n') // .reverse()
    .map((line, index)=>{
        // `<space>at <component> (<location>)` -> `at <component> (<location>)`
        line = line.trim();
        // extract `<space>at <component>` to `<<component>>`
        // e.g. `  at Foo` -> `<Foo>`
        const [, component, location] = /at (\w+)( \((.*)\))?/.exec(line) || [];
        // If there's no location then it's user-land stack frame
        if (!location) {
            if (component === firstContent && firstIndex === -1) {
                firstIndex = index;
            } else if (component === secondContent && secondIndex === -1) {
                secondIndex = index;
            }
        }
        return location ? '' : component;
    }).filter(Boolean).reverse();
    let diff = '';
    for(let i = 0; i < components.length; i++){
        const component = components[i];
        const matchFirstContent = hydrationWarningType === 'tag' && i === components.length - firstIndex - 1;
        const matchSecondContent = hydrationWarningType === 'tag' && i === components.length - secondIndex - 1;
        if (matchFirstContent || matchSecondContent) {
            const spaces = ' '.repeat(Math.max(i * 2 - 2, 0) + 2);
            diff += `> ${spaces}<${component}>\n`;
        } else {
            const spaces = ' '.repeat(i * 2 + 2);
            diff += `${spaces}<${component}>\n`;
        }
    }
    if (hydrationWarningType === 'text') {
        const spaces = ' '.repeat(components.length * 2);
        diff += `+ ${spaces}"${firstContent}"\n`;
        diff += `- ${spaces}"${secondContent}"\n`;
    } else if (hydrationWarningType === 'text-in-tag') {
        const spaces = ' '.repeat(components.length * 2);
        diff += `> ${spaces}<${secondContent}>\n`;
        diff += `>   ${spaces}"${firstContent}"\n`;
    }
    return diff;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/pages/pages-dev-overlay-error-boundary.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "PagesDevOverlayErrorBoundary", {
    enumerable: true,
    get: function() {
        return PagesDevOverlayErrorBoundary;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [client] (ecmascript)");
const _react = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/react@19.2.6/node_modules/react/index.js [client] (ecmascript)"));
class PagesDevOverlayErrorBoundary extends _react.default.PureComponent {
    static getDerivedStateFromError(error) {
        return {
            error
        };
    }
    // Explicit type is needed to avoid the generated `.d.ts` having a wide return type that could be specific to the `@types/react` version.
    render() {
        // The component has to be unmounted or else it would continue to error
        return this.state.error ? null : this.props.children;
    }
    constructor(...args){
        super(...args), this.state = {
            error: null
        };
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
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/terminal-logging-config.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    getIsTerminalLoggingEnabled: null,
    getTerminalLoggingConfig: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    getIsTerminalLoggingEnabled: function() {
        return getIsTerminalLoggingEnabled;
    },
    getTerminalLoggingConfig: function() {
        return getTerminalLoggingConfig;
    }
});
function getTerminalLoggingConfig() {
    try {
        return JSON.parse(("TURBOPACK compile-time value", '"warn"') || 'false');
    } catch  {
        return false;
    }
}
function getIsTerminalLoggingEnabled() {
    const config = getTerminalLoggingConfig();
    return Boolean(config);
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/shared/forward-logs-shared.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    UNDEFINED_MARKER: null,
    patchConsoleMethod: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    UNDEFINED_MARKER: function() {
        return UNDEFINED_MARKER;
    },
    patchConsoleMethod: function() {
        return patchConsoleMethod;
    }
});
const UNDEFINED_MARKER = '__next_tagged_undefined';
function patchConsoleMethod(methodName, wrapper) {
    const descriptor = Object.getOwnPropertyDescriptor(console, methodName);
    if (descriptor && (descriptor.configurable || descriptor.writable) && typeof descriptor.value === 'function') {
        const originalMethod = descriptor.value;
        const originalName = Object.getOwnPropertyDescriptor(originalMethod, 'name');
        const wrapperMethod = function(...args) {
            wrapper(methodName, ...args);
            originalMethod.apply(this, args);
        };
        if (originalName) {
            Object.defineProperty(wrapperMethod, 'name', originalName);
        }
        Object.defineProperty(console, methodName, {
            value: wrapperMethod
        });
        return ()=>{
            Object.defineProperty(console, methodName, {
                value: originalMethod,
                writable: descriptor.writable,
                configurable: descriptor.configurable
            });
        };
    }
    return ()=>{};
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/forward-logs-utils.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    logStringify: null,
    preLogSerializationClone: null,
    safeStringifyWithDepth: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    logStringify: function() {
        return logStringify;
    },
    preLogSerializationClone: function() {
        return preLogSerializationClone;
    },
    safeStringifyWithDepth: function() {
        return safeStringifyWithDepth;
    }
});
const _safestablestringify = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/safe-stable-stringify/index.js [client] (ecmascript)");
const _terminalloggingconfig = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/terminal-logging-config.js [client] (ecmascript)");
const _forwardlogsshared = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/shared/forward-logs-shared.js [client] (ecmascript)");
const terminalLoggingConfig = (0, _terminalloggingconfig.getTerminalLoggingConfig)();
const PROMISE_MARKER = 'Promise {}';
const UNAVAILABLE_MARKER = '[Unable to view]';
const maximumDepth = typeof terminalLoggingConfig === 'object' && terminalLoggingConfig.depthLimit ? terminalLoggingConfig.depthLimit : 5;
const maximumBreadth = typeof terminalLoggingConfig === 'object' && terminalLoggingConfig.edgeLimit ? terminalLoggingConfig.edgeLimit : 100;
const safeStringifyWithDepth = (0, _safestablestringify.configure)({
    maximumDepth,
    maximumBreadth
});
function preLogSerializationClone(value, seen = new WeakMap()) {
    if (value === undefined) return _forwardlogsshared.UNDEFINED_MARKER;
    if (value === null || typeof value !== 'object') return value;
    if (seen.has(value)) return seen.get(value);
    try {
        Object.keys(value);
    } catch  {
        return UNAVAILABLE_MARKER;
    }
    try {
        if (typeof value.then === 'function') return PROMISE_MARKER;
    } catch  {
        return UNAVAILABLE_MARKER;
    }
    if (Array.isArray(value)) {
        const out = [];
        seen.set(value, out);
        for (const item of value){
            try {
                out.push(preLogSerializationClone(item, seen));
            } catch  {
                out.push(UNAVAILABLE_MARKER);
            }
        }
        return out;
    }
    const proto = Object.getPrototypeOf(value);
    if (proto === Object.prototype || proto === null) {
        const out = {};
        seen.set(value, out);
        for (const key of Object.keys(value)){
            try {
                out[key] = preLogSerializationClone(value[key], seen);
            } catch  {
                out[key] = UNAVAILABLE_MARKER;
            }
        }
        return out;
    }
    return Object.prototype.toString.call(value);
}
const logStringify = (data)=>{
    try {
        const result = safeStringifyWithDepth(data);
        return result ?? `"${UNAVAILABLE_MARKER}"`;
    } catch  {
        return `"${UNAVAILABLE_MARKER}"`;
    }
};
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/forward-logs.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    forwardErrorLog: null,
    forwardUnhandledError: null,
    initializeDebugLogForwarding: null,
    logQueue: null,
    logUnhandledRejection: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    forwardErrorLog: function() {
        return forwardErrorLog;
    },
    forwardUnhandledError: function() {
        return forwardUnhandledError;
    },
    initializeDebugLogForwarding: function() {
        return initializeDebugLogForwarding;
    },
    logQueue: function() {
        return logQueue;
    },
    logUnhandledRejection: function() {
        return logUnhandledRejection;
    }
});
const _errorsource = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/error-source.js [client] (ecmascript)");
const _terminalloggingconfig = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/terminal-logging-config.js [client] (ecmascript)");
const _forwardlogsshared = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/shared/forward-logs-shared.js [client] (ecmascript)");
const _forwardlogsutils = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/forward-logs-utils.js [client] (ecmascript)");
const _stitchederror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/errors/stitched-error.js [client] (ecmascript)");
// Client-side file logger for browser logs
class ClientFileLogger {
    formatTimestamp() {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        const seconds = now.getSeconds().toString().padStart(2, '0');
        const milliseconds = now.getMilliseconds().toString().padStart(3, '0');
        return `${hours}:${minutes}:${seconds}.${milliseconds}`;
    }
    log(level, args) {
        if (isReactServerReplayedLog(args)) {
            return;
        }
        // Format the args into a message string
        const message = args.map((arg)=>{
            if (typeof arg === 'string') return arg;
            if (typeof arg === 'number' || typeof arg === 'boolean') return String(arg);
            if (arg === null) return 'null';
            if (arg === undefined) return 'undefined';
            // Handle DOM nodes - only log the tag name to avoid React proxied elements
            if (arg instanceof Element) {
                return `<${arg.tagName.toLowerCase()}>`;
            }
            return (0, _forwardlogsutils.safeStringifyWithDepth)(arg);
        }).join(' ');
        const logEntry = {
            timestamp: this.formatTimestamp(),
            level: level.toUpperCase(),
            message
        };
        this.logEntries.push(logEntry);
        // Schedule flush when new log is added
        scheduleLogFlush();
    }
    getLogs() {
        return [
            ...this.logEntries
        ];
    }
    clear() {
        this.logEntries = [];
    }
    constructor(){
        this.logEntries = [];
    }
}
const clientFileLogger = new ClientFileLogger();
// Set up flush-based sending of client file logs
let logFlushTimeout = null;
let heartbeatInterval = null;
const scheduleLogFlush = ()=>{
    if (logFlushTimeout) {
        clearTimeout(logFlushTimeout);
    }
    logFlushTimeout = setTimeout(()=>{
        sendClientFileLogs();
        logFlushTimeout = null;
    }, 100) // Send after 100ms (much faster with debouncing)
    ;
};
const cancelLogFlush = ()=>{
    if (logFlushTimeout) {
        clearTimeout(logFlushTimeout);
        logFlushTimeout = null;
    }
};
const startHeartbeat = ()=>{
    if (heartbeatInterval) return;
    heartbeatInterval = setInterval(()=>{
        if (logQueue.socket && logQueue.socket.readyState === WebSocket.OPEN) {
            try {
                // Send a ping to keep the connection alive
                logQueue.socket.send(JSON.stringify({
                    event: 'ping'
                }));
            } catch (error) {
                // Connection might be closed, stop heartbeat
                stopHeartbeat();
            }
        } else {
            stopHeartbeat();
        }
    }, 5000) // Send ping every 5 seconds
    ;
};
const stopHeartbeat = ()=>{
    if (heartbeatInterval) {
        clearInterval(heartbeatInterval);
        heartbeatInterval = null;
    }
};
const isTerminalLoggingEnabled = (0, _terminalloggingconfig.getIsTerminalLoggingEnabled)();
const methods = [
    'log',
    'info',
    'warn',
    'debug',
    'table',
    'assert',
    'dir',
    'dirxml',
    'group',
    'groupCollapsed',
    'groupEnd',
    'trace'
];
const afterThisFrame = (cb)=>{
    let timeout;
    const rafId = requestAnimationFrame(()=>{
        timeout = setTimeout(()=>{
            cb();
        });
    });
    return ()=>{
        cancelAnimationFrame(rafId);
        clearTimeout(timeout);
    };
};
let isPatched = false;
const serializeEntries = (entries)=>entries.map((clientEntry)=>{
        switch(clientEntry.kind){
            case 'any-logged-error':
            case 'console':
                {
                    return {
                        ...clientEntry,
                        args: clientEntry.args.map(stringifyUserArg)
                    };
                }
            case 'formatted-error':
                {
                    return clientEntry;
                }
            default:
                {
                    return null;
                }
        }
    });
// Function to send client file logs to server
const sendClientFileLogs = ()=>{
    if (!logQueue.socket || logQueue.socket.readyState !== WebSocket.OPEN) {
        return;
    }
    const logs = clientFileLogger.getLogs();
    if (logs.length === 0) {
        return;
    }
    try {
        const payload = JSON.stringify({
            event: 'client-file-logs',
            logs: logs
        });
        logQueue.socket.send(payload);
    } catch (error) {
        console.error(error);
    } finally{
        // Clear logs regardless of send success to prevent memory leaks
        clientFileLogger.clear();
    }
};
const logQueue = {
    entries: [],
    flushScheduled: false,
    cancelFlush: null,
    socket: null,
    sourceType: undefined,
    router: null,
    scheduleLogSend: (entry)=>{
        logQueue.entries.push(entry);
        if (logQueue.flushScheduled) {
            return;
        }
        // safe to deref and use in setTimeout closure since we cancel on new socket
        const socket = logQueue.socket;
        if (!socket) {
            return;
        }
        // we probably dont need this
        logQueue.flushScheduled = true;
        // non blocking log flush, runs at most once per frame
        logQueue.cancelFlush = afterThisFrame(()=>{
            logQueue.flushScheduled = false;
            // just incase
            try {
                const payload = JSON.stringify({
                    event: 'browser-logs',
                    entries: serializeEntries(logQueue.entries),
                    router: logQueue.router,
                    // needed for source mapping, we just assign the sourceType from the last error for the whole batch
                    sourceType: logQueue.sourceType
                });
                socket.send(payload);
                logQueue.entries = [];
                logQueue.sourceType = undefined;
                // Also send client file logs
                sendClientFileLogs();
            } catch  {
            // error (make sure u don't infinite loop)
            /* noop */ }
        });
    },
    onSocketReady: (socket)=>{
        // When MCP or terminal logging is enabled, we enable the socket connection,
        // otherwise it will not proceed.
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
        if (socket.readyState !== WebSocket.OPEN) {
            // invariant
            return;
        }
        // incase an existing timeout was going to run with a stale socket
        logQueue.cancelFlush?.();
        logQueue.socket = socket;
        // Add socket event listeners to track connection state
        socket.addEventListener('close', ()=>{
            cancelLogFlush();
            stopHeartbeat();
        });
        // Only send terminal logs if enabled
        if (isTerminalLoggingEnabled) {
            try {
                const payload = JSON.stringify({
                    event: 'browser-logs',
                    entries: serializeEntries(logQueue.entries),
                    router: logQueue.router,
                    sourceType: logQueue.sourceType
                });
                socket.send(payload);
                logQueue.entries = [];
                logQueue.sourceType = undefined;
            } catch  {
            /** noop just incase */ }
        }
        // Always send client file logs when socket is ready
        sendClientFileLogs();
        // Start heartbeat to keep connection alive
        startHeartbeat();
    }
};
const stringifyUserArg = (arg)=>{
    if (arg.kind !== 'arg') {
        return arg;
    }
    return {
        ...arg,
        data: (0, _forwardlogsutils.logStringify)(arg.data)
    };
};
const createErrorArg = (error)=>{
    return {
        kind: 'formatted-error-arg',
        prefix: error.message ? `${error.name}: ${error.message}` : `${error.name}`,
        stack: getErrorStackWithOwnerStack(error)
    };
};
const createLogEntry = (level, args)=>{
    // Always log to client file logger with args (formatting done inside log method)
    clientFileLogger.log(level, args);
    // Only forward to terminal if enabled
    if (!isTerminalLoggingEnabled) {
        return;
    }
    // do not abstract this, it implicitly relies on which functions call it. forcing the inlined implementation makes you think about callers
    // error capture stack trace maybe
    const stack = getErrorStack(new Error());
    const stackLines = stack?.split('\n');
    const cleanStack = stackLines?.slice(3).join('\n') // this is probably ignored anyways
    ;
    const entry = {
        kind: 'console',
        consoleMethodStack: cleanStack ?? null,
        method: level,
        args: args.map((arg)=>{
            if (arg instanceof Error) {
                return createErrorArg(arg);
            }
            return {
                kind: 'arg',
                data: (0, _forwardlogsutils.preLogSerializationClone)(arg)
            };
        })
    };
    logQueue.scheduleLogSend(entry);
};
const forwardErrorLog = (args)=>{
    // Skip React server replayed logs - they were already logged on the server
    if (isReactServerReplayedLog(args)) {
        return;
    }
    // Always log to client file logger with args (formatting done inside log method)
    clientFileLogger.log('error', args);
    // Only forward to terminal if enabled
    if (!isTerminalLoggingEnabled) {
        return;
    }
    const errorObjects = args.filter((arg)=>arg instanceof Error);
    const first = errorObjects.at(0);
    if (first) {
        const source = (0, _errorsource.getErrorSource)(first);
        if (source) {
            logQueue.sourceType = source;
        }
    }
    /**
   * browser shows stack regardless of type of data passed to console.error, so we should do the same
   *
   * do not abstract this, it implicitly relies on which functions call it. forcing the inlined implementation makes you think about callers
   */ const stack = getErrorStack(new Error());
    const stackLines = stack?.split('\n');
    const cleanStack = stackLines?.slice(3).join('\n');
    const entry = {
        kind: 'any-logged-error',
        method: 'error',
        consoleErrorStack: cleanStack ?? '',
        args: args.map((arg)=>{
            if (arg instanceof Error) {
                return createErrorArg(arg);
            }
            return {
                kind: 'arg',
                data: (0, _forwardlogsutils.preLogSerializationClone)(arg)
            };
        })
    };
    logQueue.scheduleLogSend(entry);
};
const createUncaughtErrorEntry = (errorName, errorMessage, fullStack)=>{
    const entry = {
        kind: 'formatted-error',
        prefix: `Uncaught ${errorName}: ${errorMessage}`,
        stack: fullStack,
        method: 'error'
    };
    logQueue.scheduleLogSend(entry);
};
const getErrorStack = (error)=>{
    return error.stack || '';
};
// Get error stack with owner stack appended for source mapping on the server
const getErrorStackWithOwnerStack = (error)=>{
    const errorStack = getErrorStack(error);
    const ownerStack = (0, _stitchederror.getOwnerStack)(error);
    return ownerStack ? `${errorStack}\n${ownerStack}` : errorStack;
};
function logUnhandledRejection(reason) {
    // Always log to client file logger
    const message = reason instanceof Error ? `${reason.name}: ${reason.message}` : JSON.stringify(reason);
    clientFileLogger.log('error', [
        `unhandledRejection: ${message}`
    ]);
    // Only forward to terminal if enabled
    if (!isTerminalLoggingEnabled) {
        return;
    }
    if (reason instanceof Error) {
        createUnhandledRejectionErrorEntry(reason, getErrorStackWithOwnerStack(reason));
        return;
    }
    createUnhandledRejectionNonErrorEntry(reason);
}
const createUnhandledRejectionErrorEntry = (error, fullStack)=>{
    const source = (0, _errorsource.getErrorSource)(error);
    if (source) {
        logQueue.sourceType = source;
    }
    const entry = {
        kind: 'formatted-error',
        prefix: `⨯ unhandledRejection: ${error.name}: ${error.message}`,
        stack: fullStack,
        method: 'error'
    };
    logQueue.scheduleLogSend(entry);
};
const createUnhandledRejectionNonErrorEntry = (reason)=>{
    const entry = {
        kind: 'any-logged-error',
        // we can't access the stack since the event is dispatched async and creating an inline error would be meaningless
        consoleErrorStack: '',
        method: 'error',
        args: [
            {
                kind: 'arg',
                data: `⨯ unhandledRejection:`,
                isRejectionMessage: true
            },
            {
                kind: 'arg',
                data: (0, _forwardlogsutils.preLogSerializationClone)(reason)
            }
        ]
    };
    logQueue.scheduleLogSend(entry);
};
const isHMR = (args)=>{
    const firstArg = args[0];
    if (typeof firstArg !== 'string') {
        return false;
    }
    if (firstArg.startsWith('[Fast Refresh]')) {
        return true;
    }
    if (firstArg.startsWith('[HMR]')) {
        return true;
    }
    return false;
};
/**
 * Matches the format of logs arguments React replayed from the RSC.
 */ const isReactServerReplayedLog = (args)=>{
    if (args.length < 3) {
        return false;
    }
    const [format, styles, label] = args;
    if (typeof format !== 'string' || typeof styles !== 'string' || typeof label !== 'string') {
        return false;
    }
    return format.startsWith('%c%s%c') && styles.includes('background:');
};
function forwardUnhandledError(error) {
    // Always log to client file logger
    clientFileLogger.log('error', [
        `uncaughtError: ${error.name}: ${error.message}`
    ]);
    // Only forward to terminal if enabled
    if (!isTerminalLoggingEnabled) {
        return;
    }
    createUncaughtErrorEntry(error.name, error.message, getErrorStackWithOwnerStack(error));
}
const initializeDebugLogForwarding = (router)=>{
    // probably don't need this
    if (isPatched) {
        return;
    }
    // TODO(rob): why does this break rendering on server, important to know incase the same bug appears in browser
    if (typeof window === 'undefined') {
        return;
    }
    // better to be safe than sorry
    try {
        methods.forEach((method)=>(0, _forwardlogsshared.patchConsoleMethod)(method, (_, ...args)=>{
                if (isHMR(args)) {
                    return;
                }
                if (isReactServerReplayedLog(args)) {
                    return;
                }
                createLogEntry(method, args);
            }));
    } catch  {}
    logQueue.router = router;
    isPatched = true;
    // Cleanup on page unload
    window.addEventListener('beforeunload', ()=>{
        cancelLogFlush();
        stopHeartbeat();
        // Send any remaining logs before page unloads
        sendClientFileLogs();
    });
};
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/pages/pages-dev-overlay-setup.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$2$2e$6_react$2d$dom$40$19$2e$2$2e$6_react$40$19$2e$2$2e$6_$5f$react$40$19$2e$2$2e$6$2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/build/polyfills/process.js [client] (ecmascript)");
"use strict";
Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    PagesDevOverlayBridge: null,
    register: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    PagesDevOverlayBridge: function() {
        return PagesDevOverlayBridge;
    },
    register: function() {
        return register;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [client] (ecmascript)");
const _jsxruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/react@19.2.6/node_modules/react/jsx-runtime.js [client] (ecmascript)");
const _react = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/react@19.2.6/node_modules/react/index.js [client] (ecmascript)"));
const _nextdevtools = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/next-devtools/index.js (raw)");
const _hydrationerrorstate = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/pages/hydration-error-state.js [client] (ecmascript)");
const _router = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/router.js [client] (ecmascript)");
const _stitchederror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/errors/stitched-error.js [client] (ecmascript)");
const _onrecoverableerror = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/react-client-callbacks/on-recoverable-error.js [client] (ecmascript)");
const _pagesdevoverlayerrorboundary = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/pages/pages-dev-overlay-error-boundary.js [client] (ecmascript)");
const _forwardlogs = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/next-devtools/userspace/app/forward-logs.js [client] (ecmascript)");
const usePagesDevOverlayBridge = ()=>{
    _react.default.useInsertionEffect({
        "usePagesDevOverlayBridge.useInsertionEffect": ()=>{
            // NDT uses a different React instance so it's not technically a state update
            // scheduled from useInsertionEffect.
            (0, _nextdevtools.renderPagesDevOverlay)(_stitchederror.getOwnerStack, _hydrationerrorstate.getSquashedHydrationErrorDetails, _onrecoverableerror.isRecoverableError);
        }
    }["usePagesDevOverlayBridge.useInsertionEffect"], []);
    _react.default.useEffect({
        "usePagesDevOverlayBridge.useEffect": ()=>{
            const { handleStaticIndicator } = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/client/dev/hot-reloader/pages/hot-reloader-pages.js [client] (ecmascript)");
            _router.Router.events.on('routeChangeComplete', handleStaticIndicator);
            return ({
                "usePagesDevOverlayBridge.useEffect": function() {
                    _router.Router.events.off('routeChangeComplete', handleStaticIndicator);
                }
            })["usePagesDevOverlayBridge.useEffect"];
        }
    }["usePagesDevOverlayBridge.useEffect"], []);
};
function PagesDevOverlayBridge({ children }) {
    usePagesDevOverlayBridge();
    return /*#__PURE__*/ (0, _jsxruntime.jsx)(_pagesdevoverlayerrorboundary.PagesDevOverlayErrorBoundary, {
        children: children
    });
}
let isRegistered = false;
function handleError(error) {
    if (!error || !(error instanceof Error) || typeof error.stack !== 'string') {
        // A non-error was thrown, we don't have anything to show. :-(
        return;
    }
    (0, _hydrationerrorstate.attachHydrationErrorState)(error);
    // Skip ModuleBuildError and ModuleNotFoundError, as it will be sent through onBuildError callback.
    // This is to avoid same error as different type showing up on client to cause flashing.
    if (error.name !== 'ModuleBuildError' && error.name !== 'ModuleNotFoundError') {
        _nextdevtools.dispatcher.onUnhandledError(error);
    }
}
let origConsoleError = console.error;
function nextJsHandleConsoleError(...args) {
    // See https://github.com/facebook/react/blob/d50323eb845c5fde0d720cae888bf35dedd05506/packages/react-reconciler/src/ReactFiberErrorLogger.js#L78
    const maybeError = ("TURBOPACK compile-time truthy", 1) ? args[1] : "TURBOPACK unreachable";
    (0, _hydrationerrorstate.storeHydrationErrorStateFromConsoleArgs)(...args);
    // TODO: Surfaces non-errors logged via `console.error`.
    handleError(maybeError);
    (0, _forwardlogs.forwardErrorLog)(args);
    origConsoleError.apply(window.console, args);
}
function onUnhandledError(event) {
    const error = event?.error;
    handleError(error);
    if (error) {
        (0, _forwardlogs.forwardUnhandledError)(error);
    }
}
function onUnhandledRejection(ev) {
    const reason = ev?.reason;
    if (!reason || !(reason instanceof Error) || typeof reason.stack !== 'string') {
        // A non-error was thrown, we don't have anything to show. :-(
        return;
    }
    _nextdevtools.dispatcher.onUnhandledRejection(reason);
    (0, _forwardlogs.logUnhandledRejection)(reason);
}
function register() {
    if (isRegistered) {
        return;
    }
    isRegistered = true;
    try {
        Error.stackTraceLimit = 50;
    } catch  {}
    (0, _forwardlogs.initializeDebugLogForwarding)('pages');
    window.addEventListener('error', onUnhandledError);
    window.addEventListener('unhandledrejection', onUnhandledRejection);
    window.console.error = nextJsHandleConsoleError;
}
if ((typeof exports.default === 'function' || typeof exports.default === 'object' && exports.default !== null) && typeof exports.default.__esModule === 'undefined') {
    Object.defineProperty(exports.default, '__esModule', {
        value: true
    });
    Object.assign(exports.default, exports);
    module.exports = exports.default;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/server/dev/hot-reloader-types.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
0 && (module.exports = {
    HMR_MESSAGE_SENT_TO_BROWSER: null,
    HMR_MESSAGE_SENT_TO_SERVER: null
});
function _export(target, all) {
    for(var name in all)Object.defineProperty(target, name, {
        enumerable: true,
        get: all[name]
    });
}
_export(exports, {
    HMR_MESSAGE_SENT_TO_BROWSER: function() {
        return HMR_MESSAGE_SENT_TO_BROWSER;
    },
    HMR_MESSAGE_SENT_TO_SERVER: function() {
        return HMR_MESSAGE_SENT_TO_SERVER;
    }
});
var HMR_MESSAGE_SENT_TO_BROWSER = /*#__PURE__*/ function(HMR_MESSAGE_SENT_TO_BROWSER) {
    // JSON messages:
    HMR_MESSAGE_SENT_TO_BROWSER["ADDED_PAGE"] = "addedPage";
    HMR_MESSAGE_SENT_TO_BROWSER["REMOVED_PAGE"] = "removedPage";
    HMR_MESSAGE_SENT_TO_BROWSER["RELOAD_PAGE"] = "reloadPage";
    HMR_MESSAGE_SENT_TO_BROWSER["SERVER_COMPONENT_CHANGES"] = "serverComponentChanges";
    HMR_MESSAGE_SENT_TO_BROWSER["MIDDLEWARE_CHANGES"] = "middlewareChanges";
    HMR_MESSAGE_SENT_TO_BROWSER["CLIENT_CHANGES"] = "clientChanges";
    HMR_MESSAGE_SENT_TO_BROWSER["SERVER_ONLY_CHANGES"] = "serverOnlyChanges";
    HMR_MESSAGE_SENT_TO_BROWSER["SYNC"] = "sync";
    HMR_MESSAGE_SENT_TO_BROWSER["BUILT"] = "built";
    HMR_MESSAGE_SENT_TO_BROWSER["BUILDING"] = "building";
    HMR_MESSAGE_SENT_TO_BROWSER["DEV_PAGES_MANIFEST_UPDATE"] = "devPagesManifestUpdate";
    HMR_MESSAGE_SENT_TO_BROWSER["TURBOPACK_MESSAGE"] = "turbopack-message";
    HMR_MESSAGE_SENT_TO_BROWSER["SERVER_ERROR"] = "serverError";
    HMR_MESSAGE_SENT_TO_BROWSER["TURBOPACK_CONNECTED"] = "turbopack-connected";
    HMR_MESSAGE_SENT_TO_BROWSER["ISR_MANIFEST"] = "isrManifest";
    HMR_MESSAGE_SENT_TO_BROWSER["CACHE_INDICATOR"] = "cacheIndicator";
    HMR_MESSAGE_SENT_TO_BROWSER["DEV_INDICATOR"] = "devIndicator";
    HMR_MESSAGE_SENT_TO_BROWSER["DEVTOOLS_CONFIG"] = "devtoolsConfig";
    HMR_MESSAGE_SENT_TO_BROWSER["REQUEST_CURRENT_ERROR_STATE"] = "requestCurrentErrorState";
    HMR_MESSAGE_SENT_TO_BROWSER["REQUEST_PAGE_METADATA"] = "requestPageMetadata";
    // Binary messages:
    HMR_MESSAGE_SENT_TO_BROWSER[HMR_MESSAGE_SENT_TO_BROWSER["REACT_DEBUG_CHUNK"] = 0] = "REACT_DEBUG_CHUNK";
    HMR_MESSAGE_SENT_TO_BROWSER[HMR_MESSAGE_SENT_TO_BROWSER["ERRORS_TO_SHOW_IN_BROWSER"] = 1] = "ERRORS_TO_SHOW_IN_BROWSER";
    return HMR_MESSAGE_SENT_TO_BROWSER;
}({});
var HMR_MESSAGE_SENT_TO_SERVER = /*#__PURE__*/ function(HMR_MESSAGE_SENT_TO_SERVER) {
    // JSON messages:
    HMR_MESSAGE_SENT_TO_SERVER["MCP_ERROR_STATE_RESPONSE"] = "mcp-error-state-response";
    HMR_MESSAGE_SENT_TO_SERVER["MCP_PAGE_METADATA_RESPONSE"] = "mcp-page-metadata-response";
    HMR_MESSAGE_SENT_TO_SERVER["PING"] = "ping";
    return HMR_MESSAGE_SENT_TO_SERVER;
}({});
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/server/dev/node-stack-frames.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "getServerError", {
    enumerable: true,
    get: function() {
        return getServerError;
    }
});
const _stacktraceparser = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/stacktrace-parser/stack-trace-parser.cjs.js [client] (ecmascript)");
const _errorsource = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/error-source.js [client] (ecmascript)");
function getFilesystemFrame(frame) {
    const f = {
        ...frame
    };
    if (typeof f.file === 'string') {
        if (f.file.startsWith('/') || // Win32:
        /^[a-z]:\\/i.test(f.file) || // Win32 UNC:
        f.file.startsWith('\\\\')) {
            f.file = `file://${f.file}`;
        }
    }
    return f;
}
function getServerError(error, type) {
    if (error.name === 'TurbopackInternalError') {
        // If this is an internal Turbopack error we shouldn't show internal details
        // to the user. These are written to a log file instead.
        const turbopackInternalError = Object.defineProperty(new Error('An unexpected Turbopack error occurred. Please see the output of `next dev` for more details.'), "__NEXT_ERROR_CODE", {
            value: "E167",
            enumerable: false,
            configurable: true
        });
        (0, _errorsource.decorateServerError)(turbopackInternalError, type);
        return turbopackInternalError;
    }
    let n;
    try {
        throw Object.defineProperty(new Error(error.message), "__NEXT_ERROR_CODE", {
            value: "E394",
            enumerable: false,
            configurable: true
        });
    } catch (e) {
        n = e;
    }
    n.name = error.name;
    try {
        n.stack = `${n.toString()}\n${(0, _stacktraceparser.parse)(error.stack).map(getFilesystemFrame).map((f)=>{
            let str = `    at ${f.methodName}`;
            if (f.file) {
                let loc = f.file;
                if (f.lineNumber) {
                    loc += `:${f.lineNumber}`;
                    if (f.column) {
                        loc += `:${f.column}`;
                    }
                }
                str += ` (${loc})`;
            }
            return str;
        }).join('\n')}`;
    } catch  {
        n.stack = error.stack;
    }
    (0, _errorsource.decorateServerError)(n, type);
    return n;
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/pages/_app.js [client] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
Object.defineProperty(exports, "default", {
    enumerable: true,
    get: function() {
        return App;
    }
});
const _interop_require_default = __turbopack_context__.r("[project]/node_modules/.pnpm/@swc+helpers@0.5.15/node_modules/@swc/helpers/cjs/_interop_require_default.cjs [client] (ecmascript)");
const _jsxruntime = __turbopack_context__.r("[project]/node_modules/.pnpm/react@19.2.6/node_modules/react/jsx-runtime.js [client] (ecmascript)");
const _react = /*#__PURE__*/ _interop_require_default._(__turbopack_context__.r("[project]/node_modules/.pnpm/react@19.2.6/node_modules/react/index.js [client] (ecmascript)"));
const _utils = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/shared/lib/utils.js [client] (ecmascript)");
/**
 * `App` component is used for initialize of pages. It allows for overwriting and full control of the `page` initialization.
 * This allows for keeping state between navigation, custom error handling, injecting additional data.
 */ async function appGetInitialProps({ Component, ctx }) {
    const pageProps = await (0, _utils.loadGetInitialProps)(Component, ctx);
    return {
        pageProps
    };
}
class App extends _react.default.Component {
    static{
        this.origGetInitialProps = appGetInitialProps;
    }
    static{
        this.getInitialProps = appGetInitialProps;
    }
    render() {
        const { Component, pageProps } = this.props;
        return /*#__PURE__*/ (0, _jsxruntime.jsx)(Component, {
            ...pageProps
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
]);

//# sourceMappingURL=08c5_next_dist_0oi3rtp._.js.map