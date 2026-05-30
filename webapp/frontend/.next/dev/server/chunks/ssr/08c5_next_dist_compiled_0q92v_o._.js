module.exports = [
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/@opentelemetry/api/index.js [app-rsc] (ecmascript)", ((__turbopack_context__, module, exports) => {

(()=>{
    "use strict";
    var e = {
        491: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.ContextAPI = void 0;
            const n = r(223);
            const a = r(172);
            const o = r(930);
            const i = "context";
            const c = new n.NoopContextManager;
            class ContextAPI {
                constructor(){}
                static getInstance() {
                    if (!this._instance) {
                        this._instance = new ContextAPI;
                    }
                    return this._instance;
                }
                setGlobalContextManager(e) {
                    return (0, a.registerGlobal)(i, e, o.DiagAPI.instance());
                }
                active() {
                    return this._getContextManager().active();
                }
                with(e, t, r, ...n) {
                    return this._getContextManager().with(e, t, r, ...n);
                }
                bind(e, t) {
                    return this._getContextManager().bind(e, t);
                }
                _getContextManager() {
                    return (0, a.getGlobal)(i) || c;
                }
                disable() {
                    this._getContextManager().disable();
                    (0, a.unregisterGlobal)(i, o.DiagAPI.instance());
                }
            }
            t.ContextAPI = ContextAPI;
        },
        930: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.DiagAPI = void 0;
            const n = r(56);
            const a = r(912);
            const o = r(957);
            const i = r(172);
            const c = "diag";
            class DiagAPI {
                constructor(){
                    function _logProxy(e) {
                        return function(...t) {
                            const r = (0, i.getGlobal)("diag");
                            if (!r) return;
                            return r[e](...t);
                        };
                    }
                    const e = this;
                    const setLogger = (t, r = {
                        logLevel: o.DiagLogLevel.INFO
                    })=>{
                        var n, c, s;
                        if (t === e) {
                            const t = new Error("Cannot use diag as the logger for itself. Please use a DiagLogger implementation like ConsoleDiagLogger or a custom implementation");
                            e.error((n = t.stack) !== null && n !== void 0 ? n : t.message);
                            return false;
                        }
                        if (typeof r === "number") {
                            r = {
                                logLevel: r
                            };
                        }
                        const u = (0, i.getGlobal)("diag");
                        const l = (0, a.createLogLevelDiagLogger)((c = r.logLevel) !== null && c !== void 0 ? c : o.DiagLogLevel.INFO, t);
                        if (u && !r.suppressOverrideMessage) {
                            const e = (s = (new Error).stack) !== null && s !== void 0 ? s : "<failed to generate stacktrace>";
                            u.warn(`Current logger will be overwritten from ${e}`);
                            l.warn(`Current logger will overwrite one already registered from ${e}`);
                        }
                        return (0, i.registerGlobal)("diag", l, e, true);
                    };
                    e.setLogger = setLogger;
                    e.disable = ()=>{
                        (0, i.unregisterGlobal)(c, e);
                    };
                    e.createComponentLogger = (e)=>new n.DiagComponentLogger(e);
                    e.verbose = _logProxy("verbose");
                    e.debug = _logProxy("debug");
                    e.info = _logProxy("info");
                    e.warn = _logProxy("warn");
                    e.error = _logProxy("error");
                }
                static instance() {
                    if (!this._instance) {
                        this._instance = new DiagAPI;
                    }
                    return this._instance;
                }
            }
            t.DiagAPI = DiagAPI;
        },
        653: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.MetricsAPI = void 0;
            const n = r(660);
            const a = r(172);
            const o = r(930);
            const i = "metrics";
            class MetricsAPI {
                constructor(){}
                static getInstance() {
                    if (!this._instance) {
                        this._instance = new MetricsAPI;
                    }
                    return this._instance;
                }
                setGlobalMeterProvider(e) {
                    return (0, a.registerGlobal)(i, e, o.DiagAPI.instance());
                }
                getMeterProvider() {
                    return (0, a.getGlobal)(i) || n.NOOP_METER_PROVIDER;
                }
                getMeter(e, t, r) {
                    return this.getMeterProvider().getMeter(e, t, r);
                }
                disable() {
                    (0, a.unregisterGlobal)(i, o.DiagAPI.instance());
                }
            }
            t.MetricsAPI = MetricsAPI;
        },
        181: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.PropagationAPI = void 0;
            const n = r(172);
            const a = r(874);
            const o = r(194);
            const i = r(277);
            const c = r(369);
            const s = r(930);
            const u = "propagation";
            const l = new a.NoopTextMapPropagator;
            class PropagationAPI {
                constructor(){
                    this.createBaggage = c.createBaggage;
                    this.getBaggage = i.getBaggage;
                    this.getActiveBaggage = i.getActiveBaggage;
                    this.setBaggage = i.setBaggage;
                    this.deleteBaggage = i.deleteBaggage;
                }
                static getInstance() {
                    if (!this._instance) {
                        this._instance = new PropagationAPI;
                    }
                    return this._instance;
                }
                setGlobalPropagator(e) {
                    return (0, n.registerGlobal)(u, e, s.DiagAPI.instance());
                }
                inject(e, t, r = o.defaultTextMapSetter) {
                    return this._getGlobalPropagator().inject(e, t, r);
                }
                extract(e, t, r = o.defaultTextMapGetter) {
                    return this._getGlobalPropagator().extract(e, t, r);
                }
                fields() {
                    return this._getGlobalPropagator().fields();
                }
                disable() {
                    (0, n.unregisterGlobal)(u, s.DiagAPI.instance());
                }
                _getGlobalPropagator() {
                    return (0, n.getGlobal)(u) || l;
                }
            }
            t.PropagationAPI = PropagationAPI;
        },
        997: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.TraceAPI = void 0;
            const n = r(172);
            const a = r(846);
            const o = r(139);
            const i = r(607);
            const c = r(930);
            const s = "trace";
            class TraceAPI {
                constructor(){
                    this._proxyTracerProvider = new a.ProxyTracerProvider;
                    this.wrapSpanContext = o.wrapSpanContext;
                    this.isSpanContextValid = o.isSpanContextValid;
                    this.deleteSpan = i.deleteSpan;
                    this.getSpan = i.getSpan;
                    this.getActiveSpan = i.getActiveSpan;
                    this.getSpanContext = i.getSpanContext;
                    this.setSpan = i.setSpan;
                    this.setSpanContext = i.setSpanContext;
                }
                static getInstance() {
                    if (!this._instance) {
                        this._instance = new TraceAPI;
                    }
                    return this._instance;
                }
                setGlobalTracerProvider(e) {
                    const t = (0, n.registerGlobal)(s, this._proxyTracerProvider, c.DiagAPI.instance());
                    if (t) {
                        this._proxyTracerProvider.setDelegate(e);
                    }
                    return t;
                }
                getTracerProvider() {
                    return (0, n.getGlobal)(s) || this._proxyTracerProvider;
                }
                getTracer(e, t) {
                    return this.getTracerProvider().getTracer(e, t);
                }
                disable() {
                    (0, n.unregisterGlobal)(s, c.DiagAPI.instance());
                    this._proxyTracerProvider = new a.ProxyTracerProvider;
                }
            }
            t.TraceAPI = TraceAPI;
        },
        277: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.deleteBaggage = t.setBaggage = t.getActiveBaggage = t.getBaggage = void 0;
            const n = r(491);
            const a = r(780);
            const o = (0, a.createContextKey)("OpenTelemetry Baggage Key");
            function getBaggage(e) {
                return e.getValue(o) || undefined;
            }
            t.getBaggage = getBaggage;
            function getActiveBaggage() {
                return getBaggage(n.ContextAPI.getInstance().active());
            }
            t.getActiveBaggage = getActiveBaggage;
            function setBaggage(e, t) {
                return e.setValue(o, t);
            }
            t.setBaggage = setBaggage;
            function deleteBaggage(e) {
                return e.deleteValue(o);
            }
            t.deleteBaggage = deleteBaggage;
        },
        993: (e, t)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.BaggageImpl = void 0;
            class BaggageImpl {
                constructor(e){
                    this._entries = e ? new Map(e) : new Map;
                }
                getEntry(e) {
                    const t = this._entries.get(e);
                    if (!t) {
                        return undefined;
                    }
                    return Object.assign({}, t);
                }
                getAllEntries() {
                    return Array.from(this._entries.entries()).map(([e, t])=>[
                            e,
                            t
                        ]);
                }
                setEntry(e, t) {
                    const r = new BaggageImpl(this._entries);
                    r._entries.set(e, t);
                    return r;
                }
                removeEntry(e) {
                    const t = new BaggageImpl(this._entries);
                    t._entries.delete(e);
                    return t;
                }
                removeEntries(...e) {
                    const t = new BaggageImpl(this._entries);
                    for (const r of e){
                        t._entries.delete(r);
                    }
                    return t;
                }
                clear() {
                    return new BaggageImpl;
                }
            }
            t.BaggageImpl = BaggageImpl;
        },
        830: (e, t)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.baggageEntryMetadataSymbol = void 0;
            t.baggageEntryMetadataSymbol = Symbol("BaggageEntryMetadata");
        },
        369: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.baggageEntryMetadataFromString = t.createBaggage = void 0;
            const n = r(930);
            const a = r(993);
            const o = r(830);
            const i = n.DiagAPI.instance();
            function createBaggage(e = {}) {
                return new a.BaggageImpl(new Map(Object.entries(e)));
            }
            t.createBaggage = createBaggage;
            function baggageEntryMetadataFromString(e) {
                if (typeof e !== "string") {
                    i.error(`Cannot create baggage metadata from unknown type: ${typeof e}`);
                    e = "";
                }
                return {
                    __TYPE__: o.baggageEntryMetadataSymbol,
                    toString () {
                        return e;
                    }
                };
            }
            t.baggageEntryMetadataFromString = baggageEntryMetadataFromString;
        },
        67: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.context = void 0;
            const n = r(491);
            t.context = n.ContextAPI.getInstance();
        },
        223: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.NoopContextManager = void 0;
            const n = r(780);
            class NoopContextManager {
                active() {
                    return n.ROOT_CONTEXT;
                }
                with(e, t, r, ...n) {
                    return t.call(r, ...n);
                }
                bind(e, t) {
                    return t;
                }
                enable() {
                    return this;
                }
                disable() {
                    return this;
                }
            }
            t.NoopContextManager = NoopContextManager;
        },
        780: (e, t)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.ROOT_CONTEXT = t.createContextKey = void 0;
            function createContextKey(e) {
                return Symbol.for(e);
            }
            t.createContextKey = createContextKey;
            class BaseContext {
                constructor(e){
                    const t = this;
                    t._currentContext = e ? new Map(e) : new Map;
                    t.getValue = (e)=>t._currentContext.get(e);
                    t.setValue = (e, r)=>{
                        const n = new BaseContext(t._currentContext);
                        n._currentContext.set(e, r);
                        return n;
                    };
                    t.deleteValue = (e)=>{
                        const r = new BaseContext(t._currentContext);
                        r._currentContext.delete(e);
                        return r;
                    };
                }
            }
            t.ROOT_CONTEXT = new BaseContext;
        },
        506: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.diag = void 0;
            const n = r(930);
            t.diag = n.DiagAPI.instance();
        },
        56: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.DiagComponentLogger = void 0;
            const n = r(172);
            class DiagComponentLogger {
                constructor(e){
                    this._namespace = e.namespace || "DiagComponentLogger";
                }
                debug(...e) {
                    return logProxy("debug", this._namespace, e);
                }
                error(...e) {
                    return logProxy("error", this._namespace, e);
                }
                info(...e) {
                    return logProxy("info", this._namespace, e);
                }
                warn(...e) {
                    return logProxy("warn", this._namespace, e);
                }
                verbose(...e) {
                    return logProxy("verbose", this._namespace, e);
                }
            }
            t.DiagComponentLogger = DiagComponentLogger;
            function logProxy(e, t, r) {
                const a = (0, n.getGlobal)("diag");
                if (!a) {
                    return;
                }
                r.unshift(t);
                return a[e](...r);
            }
        },
        972: (e, t)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.DiagConsoleLogger = void 0;
            const r = [
                {
                    n: "error",
                    c: "error"
                },
                {
                    n: "warn",
                    c: "warn"
                },
                {
                    n: "info",
                    c: "info"
                },
                {
                    n: "debug",
                    c: "debug"
                },
                {
                    n: "verbose",
                    c: "trace"
                }
            ];
            class DiagConsoleLogger {
                constructor(){
                    function _consoleFunc(e) {
                        return function(...t) {
                            if (console) {
                                let r = console[e];
                                if (typeof r !== "function") {
                                    r = console.log;
                                }
                                if (typeof r === "function") {
                                    return r.apply(console, t);
                                }
                            }
                        };
                    }
                    for(let e = 0; e < r.length; e++){
                        this[r[e].n] = _consoleFunc(r[e].c);
                    }
                }
            }
            t.DiagConsoleLogger = DiagConsoleLogger;
        },
        912: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.createLogLevelDiagLogger = void 0;
            const n = r(957);
            function createLogLevelDiagLogger(e, t) {
                if (e < n.DiagLogLevel.NONE) {
                    e = n.DiagLogLevel.NONE;
                } else if (e > n.DiagLogLevel.ALL) {
                    e = n.DiagLogLevel.ALL;
                }
                t = t || {};
                function _filterFunc(r, n) {
                    const a = t[r];
                    if (typeof a === "function" && e >= n) {
                        return a.bind(t);
                    }
                    return function() {};
                }
                return {
                    error: _filterFunc("error", n.DiagLogLevel.ERROR),
                    warn: _filterFunc("warn", n.DiagLogLevel.WARN),
                    info: _filterFunc("info", n.DiagLogLevel.INFO),
                    debug: _filterFunc("debug", n.DiagLogLevel.DEBUG),
                    verbose: _filterFunc("verbose", n.DiagLogLevel.VERBOSE)
                };
            }
            t.createLogLevelDiagLogger = createLogLevelDiagLogger;
        },
        957: (e, t)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.DiagLogLevel = void 0;
            var r;
            (function(e) {
                e[e["NONE"] = 0] = "NONE";
                e[e["ERROR"] = 30] = "ERROR";
                e[e["WARN"] = 50] = "WARN";
                e[e["INFO"] = 60] = "INFO";
                e[e["DEBUG"] = 70] = "DEBUG";
                e[e["VERBOSE"] = 80] = "VERBOSE";
                e[e["ALL"] = 9999] = "ALL";
            })(r = t.DiagLogLevel || (t.DiagLogLevel = {}));
        },
        172: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.unregisterGlobal = t.getGlobal = t.registerGlobal = void 0;
            const n = r(200);
            const a = r(521);
            const o = r(130);
            const i = a.VERSION.split(".")[0];
            const c = Symbol.for(`opentelemetry.js.api.${i}`);
            const s = n._globalThis;
            function registerGlobal(e, t, r, n = false) {
                var o;
                const i = s[c] = (o = s[c]) !== null && o !== void 0 ? o : {
                    version: a.VERSION
                };
                if (!n && i[e]) {
                    const t = new Error(`@opentelemetry/api: Attempted duplicate registration of API: ${e}`);
                    r.error(t.stack || t.message);
                    return false;
                }
                if (i.version !== a.VERSION) {
                    const t = new Error(`@opentelemetry/api: Registration of version v${i.version} for ${e} does not match previously registered API v${a.VERSION}`);
                    r.error(t.stack || t.message);
                    return false;
                }
                i[e] = t;
                r.debug(`@opentelemetry/api: Registered a global for ${e} v${a.VERSION}.`);
                return true;
            }
            t.registerGlobal = registerGlobal;
            function getGlobal(e) {
                var t, r;
                const n = (t = s[c]) === null || t === void 0 ? void 0 : t.version;
                if (!n || !(0, o.isCompatible)(n)) {
                    return;
                }
                return (r = s[c]) === null || r === void 0 ? void 0 : r[e];
            }
            t.getGlobal = getGlobal;
            function unregisterGlobal(e, t) {
                t.debug(`@opentelemetry/api: Unregistering a global for ${e} v${a.VERSION}.`);
                const r = s[c];
                if (r) {
                    delete r[e];
                }
            }
            t.unregisterGlobal = unregisterGlobal;
        },
        130: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.isCompatible = t._makeCompatibilityCheck = void 0;
            const n = r(521);
            const a = /^(\d+)\.(\d+)\.(\d+)(-(.+))?$/;
            function _makeCompatibilityCheck(e) {
                const t = new Set([
                    e
                ]);
                const r = new Set;
                const n = e.match(a);
                if (!n) {
                    return ()=>false;
                }
                const o = {
                    major: +n[1],
                    minor: +n[2],
                    patch: +n[3],
                    prerelease: n[4]
                };
                if (o.prerelease != null) {
                    return function isExactmatch(t) {
                        return t === e;
                    };
                }
                function _reject(e) {
                    r.add(e);
                    return false;
                }
                function _accept(e) {
                    t.add(e);
                    return true;
                }
                return function isCompatible(e) {
                    if (t.has(e)) {
                        return true;
                    }
                    if (r.has(e)) {
                        return false;
                    }
                    const n = e.match(a);
                    if (!n) {
                        return _reject(e);
                    }
                    const i = {
                        major: +n[1],
                        minor: +n[2],
                        patch: +n[3],
                        prerelease: n[4]
                    };
                    if (i.prerelease != null) {
                        return _reject(e);
                    }
                    if (o.major !== i.major) {
                        return _reject(e);
                    }
                    if (o.major === 0) {
                        if (o.minor === i.minor && o.patch <= i.patch) {
                            return _accept(e);
                        }
                        return _reject(e);
                    }
                    if (o.minor <= i.minor) {
                        return _accept(e);
                    }
                    return _reject(e);
                };
            }
            t._makeCompatibilityCheck = _makeCompatibilityCheck;
            t.isCompatible = _makeCompatibilityCheck(n.VERSION);
        },
        886: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.metrics = void 0;
            const n = r(653);
            t.metrics = n.MetricsAPI.getInstance();
        },
        901: (e, t)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.ValueType = void 0;
            var r;
            (function(e) {
                e[e["INT"] = 0] = "INT";
                e[e["DOUBLE"] = 1] = "DOUBLE";
            })(r = t.ValueType || (t.ValueType = {}));
        },
        102: (e, t)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.createNoopMeter = t.NOOP_OBSERVABLE_UP_DOWN_COUNTER_METRIC = t.NOOP_OBSERVABLE_GAUGE_METRIC = t.NOOP_OBSERVABLE_COUNTER_METRIC = t.NOOP_UP_DOWN_COUNTER_METRIC = t.NOOP_HISTOGRAM_METRIC = t.NOOP_COUNTER_METRIC = t.NOOP_METER = t.NoopObservableUpDownCounterMetric = t.NoopObservableGaugeMetric = t.NoopObservableCounterMetric = t.NoopObservableMetric = t.NoopHistogramMetric = t.NoopUpDownCounterMetric = t.NoopCounterMetric = t.NoopMetric = t.NoopMeter = void 0;
            class NoopMeter {
                constructor(){}
                createHistogram(e, r) {
                    return t.NOOP_HISTOGRAM_METRIC;
                }
                createCounter(e, r) {
                    return t.NOOP_COUNTER_METRIC;
                }
                createUpDownCounter(e, r) {
                    return t.NOOP_UP_DOWN_COUNTER_METRIC;
                }
                createObservableGauge(e, r) {
                    return t.NOOP_OBSERVABLE_GAUGE_METRIC;
                }
                createObservableCounter(e, r) {
                    return t.NOOP_OBSERVABLE_COUNTER_METRIC;
                }
                createObservableUpDownCounter(e, r) {
                    return t.NOOP_OBSERVABLE_UP_DOWN_COUNTER_METRIC;
                }
                addBatchObservableCallback(e, t) {}
                removeBatchObservableCallback(e) {}
            }
            t.NoopMeter = NoopMeter;
            class NoopMetric {
            }
            t.NoopMetric = NoopMetric;
            class NoopCounterMetric extends NoopMetric {
                add(e, t) {}
            }
            t.NoopCounterMetric = NoopCounterMetric;
            class NoopUpDownCounterMetric extends NoopMetric {
                add(e, t) {}
            }
            t.NoopUpDownCounterMetric = NoopUpDownCounterMetric;
            class NoopHistogramMetric extends NoopMetric {
                record(e, t) {}
            }
            t.NoopHistogramMetric = NoopHistogramMetric;
            class NoopObservableMetric {
                addCallback(e) {}
                removeCallback(e) {}
            }
            t.NoopObservableMetric = NoopObservableMetric;
            class NoopObservableCounterMetric extends NoopObservableMetric {
            }
            t.NoopObservableCounterMetric = NoopObservableCounterMetric;
            class NoopObservableGaugeMetric extends NoopObservableMetric {
            }
            t.NoopObservableGaugeMetric = NoopObservableGaugeMetric;
            class NoopObservableUpDownCounterMetric extends NoopObservableMetric {
            }
            t.NoopObservableUpDownCounterMetric = NoopObservableUpDownCounterMetric;
            t.NOOP_METER = new NoopMeter;
            t.NOOP_COUNTER_METRIC = new NoopCounterMetric;
            t.NOOP_HISTOGRAM_METRIC = new NoopHistogramMetric;
            t.NOOP_UP_DOWN_COUNTER_METRIC = new NoopUpDownCounterMetric;
            t.NOOP_OBSERVABLE_COUNTER_METRIC = new NoopObservableCounterMetric;
            t.NOOP_OBSERVABLE_GAUGE_METRIC = new NoopObservableGaugeMetric;
            t.NOOP_OBSERVABLE_UP_DOWN_COUNTER_METRIC = new NoopObservableUpDownCounterMetric;
            function createNoopMeter() {
                return t.NOOP_METER;
            }
            t.createNoopMeter = createNoopMeter;
        },
        660: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.NOOP_METER_PROVIDER = t.NoopMeterProvider = void 0;
            const n = r(102);
            class NoopMeterProvider {
                getMeter(e, t, r) {
                    return n.NOOP_METER;
                }
            }
            t.NoopMeterProvider = NoopMeterProvider;
            t.NOOP_METER_PROVIDER = new NoopMeterProvider;
        },
        200: function(e, t, r) {
            var n = this && this.__createBinding || (Object.create ? function(e, t, r, n) {
                if (n === undefined) n = r;
                Object.defineProperty(e, n, {
                    enumerable: true,
                    get: function() {
                        return t[r];
                    }
                });
            } : function(e, t, r, n) {
                if (n === undefined) n = r;
                e[n] = t[r];
            });
            var a = this && this.__exportStar || function(e, t) {
                for(var r in e)if (r !== "default" && !Object.prototype.hasOwnProperty.call(t, r)) n(t, e, r);
            };
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            a(r(46), t);
        },
        651: (e, t)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t._globalThis = void 0;
            t._globalThis = typeof globalThis === "object" ? globalThis : /*TURBOPACK member replacement*/ __turbopack_context__.g;
        },
        46: function(e, t, r) {
            var n = this && this.__createBinding || (Object.create ? function(e, t, r, n) {
                if (n === undefined) n = r;
                Object.defineProperty(e, n, {
                    enumerable: true,
                    get: function() {
                        return t[r];
                    }
                });
            } : function(e, t, r, n) {
                if (n === undefined) n = r;
                e[n] = t[r];
            });
            var a = this && this.__exportStar || function(e, t) {
                for(var r in e)if (r !== "default" && !Object.prototype.hasOwnProperty.call(t, r)) n(t, e, r);
            };
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            a(r(651), t);
        },
        939: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.propagation = void 0;
            const n = r(181);
            t.propagation = n.PropagationAPI.getInstance();
        },
        874: (e, t)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.NoopTextMapPropagator = void 0;
            class NoopTextMapPropagator {
                inject(e, t) {}
                extract(e, t) {
                    return e;
                }
                fields() {
                    return [];
                }
            }
            t.NoopTextMapPropagator = NoopTextMapPropagator;
        },
        194: (e, t)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.defaultTextMapSetter = t.defaultTextMapGetter = void 0;
            t.defaultTextMapGetter = {
                get (e, t) {
                    if (e == null) {
                        return undefined;
                    }
                    return e[t];
                },
                keys (e) {
                    if (e == null) {
                        return [];
                    }
                    return Object.keys(e);
                }
            };
            t.defaultTextMapSetter = {
                set (e, t, r) {
                    if (e == null) {
                        return;
                    }
                    e[t] = r;
                }
            };
        },
        845: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.trace = void 0;
            const n = r(997);
            t.trace = n.TraceAPI.getInstance();
        },
        403: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.NonRecordingSpan = void 0;
            const n = r(476);
            class NonRecordingSpan {
                constructor(e = n.INVALID_SPAN_CONTEXT){
                    this._spanContext = e;
                }
                spanContext() {
                    return this._spanContext;
                }
                setAttribute(e, t) {
                    return this;
                }
                setAttributes(e) {
                    return this;
                }
                addEvent(e, t) {
                    return this;
                }
                setStatus(e) {
                    return this;
                }
                updateName(e) {
                    return this;
                }
                end(e) {}
                isRecording() {
                    return false;
                }
                recordException(e, t) {}
            }
            t.NonRecordingSpan = NonRecordingSpan;
        },
        614: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.NoopTracer = void 0;
            const n = r(491);
            const a = r(607);
            const o = r(403);
            const i = r(139);
            const c = n.ContextAPI.getInstance();
            class NoopTracer {
                startSpan(e, t, r = c.active()) {
                    const n = Boolean(t === null || t === void 0 ? void 0 : t.root);
                    if (n) {
                        return new o.NonRecordingSpan;
                    }
                    const s = r && (0, a.getSpanContext)(r);
                    if (isSpanContext(s) && (0, i.isSpanContextValid)(s)) {
                        return new o.NonRecordingSpan(s);
                    } else {
                        return new o.NonRecordingSpan;
                    }
                }
                startActiveSpan(e, t, r, n) {
                    let o;
                    let i;
                    let s;
                    if (arguments.length < 2) {
                        return;
                    } else if (arguments.length === 2) {
                        s = t;
                    } else if (arguments.length === 3) {
                        o = t;
                        s = r;
                    } else {
                        o = t;
                        i = r;
                        s = n;
                    }
                    const u = i !== null && i !== void 0 ? i : c.active();
                    const l = this.startSpan(e, o, u);
                    const g = (0, a.setSpan)(u, l);
                    return c.with(g, s, undefined, l);
                }
            }
            t.NoopTracer = NoopTracer;
            function isSpanContext(e) {
                return typeof e === "object" && typeof e["spanId"] === "string" && typeof e["traceId"] === "string" && typeof e["traceFlags"] === "number";
            }
        },
        124: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.NoopTracerProvider = void 0;
            const n = r(614);
            class NoopTracerProvider {
                getTracer(e, t, r) {
                    return new n.NoopTracer;
                }
            }
            t.NoopTracerProvider = NoopTracerProvider;
        },
        125: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.ProxyTracer = void 0;
            const n = r(614);
            const a = new n.NoopTracer;
            class ProxyTracer {
                constructor(e, t, r, n){
                    this._provider = e;
                    this.name = t;
                    this.version = r;
                    this.options = n;
                }
                startSpan(e, t, r) {
                    return this._getTracer().startSpan(e, t, r);
                }
                startActiveSpan(e, t, r, n) {
                    const a = this._getTracer();
                    return Reflect.apply(a.startActiveSpan, a, arguments);
                }
                _getTracer() {
                    if (this._delegate) {
                        return this._delegate;
                    }
                    const e = this._provider.getDelegateTracer(this.name, this.version, this.options);
                    if (!e) {
                        return a;
                    }
                    this._delegate = e;
                    return this._delegate;
                }
            }
            t.ProxyTracer = ProxyTracer;
        },
        846: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.ProxyTracerProvider = void 0;
            const n = r(125);
            const a = r(124);
            const o = new a.NoopTracerProvider;
            class ProxyTracerProvider {
                getTracer(e, t, r) {
                    var a;
                    return (a = this.getDelegateTracer(e, t, r)) !== null && a !== void 0 ? a : new n.ProxyTracer(this, e, t, r);
                }
                getDelegate() {
                    var e;
                    return (e = this._delegate) !== null && e !== void 0 ? e : o;
                }
                setDelegate(e) {
                    this._delegate = e;
                }
                getDelegateTracer(e, t, r) {
                    var n;
                    return (n = this._delegate) === null || n === void 0 ? void 0 : n.getTracer(e, t, r);
                }
            }
            t.ProxyTracerProvider = ProxyTracerProvider;
        },
        996: (e, t)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.SamplingDecision = void 0;
            var r;
            (function(e) {
                e[e["NOT_RECORD"] = 0] = "NOT_RECORD";
                e[e["RECORD"] = 1] = "RECORD";
                e[e["RECORD_AND_SAMPLED"] = 2] = "RECORD_AND_SAMPLED";
            })(r = t.SamplingDecision || (t.SamplingDecision = {}));
        },
        607: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.getSpanContext = t.setSpanContext = t.deleteSpan = t.setSpan = t.getActiveSpan = t.getSpan = void 0;
            const n = r(780);
            const a = r(403);
            const o = r(491);
            const i = (0, n.createContextKey)("OpenTelemetry Context Key SPAN");
            function getSpan(e) {
                return e.getValue(i) || undefined;
            }
            t.getSpan = getSpan;
            function getActiveSpan() {
                return getSpan(o.ContextAPI.getInstance().active());
            }
            t.getActiveSpan = getActiveSpan;
            function setSpan(e, t) {
                return e.setValue(i, t);
            }
            t.setSpan = setSpan;
            function deleteSpan(e) {
                return e.deleteValue(i);
            }
            t.deleteSpan = deleteSpan;
            function setSpanContext(e, t) {
                return setSpan(e, new a.NonRecordingSpan(t));
            }
            t.setSpanContext = setSpanContext;
            function getSpanContext(e) {
                var t;
                return (t = getSpan(e)) === null || t === void 0 ? void 0 : t.spanContext();
            }
            t.getSpanContext = getSpanContext;
        },
        325: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.TraceStateImpl = void 0;
            const n = r(564);
            const a = 32;
            const o = 512;
            const i = ",";
            const c = "=";
            class TraceStateImpl {
                constructor(e){
                    this._internalState = new Map;
                    if (e) this._parse(e);
                }
                set(e, t) {
                    const r = this._clone();
                    if (r._internalState.has(e)) {
                        r._internalState.delete(e);
                    }
                    r._internalState.set(e, t);
                    return r;
                }
                unset(e) {
                    const t = this._clone();
                    t._internalState.delete(e);
                    return t;
                }
                get(e) {
                    return this._internalState.get(e);
                }
                serialize() {
                    return this._keys().reduce((e, t)=>{
                        e.push(t + c + this.get(t));
                        return e;
                    }, []).join(i);
                }
                _parse(e) {
                    if (e.length > o) return;
                    this._internalState = e.split(i).reverse().reduce((e, t)=>{
                        const r = t.trim();
                        const a = r.indexOf(c);
                        if (a !== -1) {
                            const o = r.slice(0, a);
                            const i = r.slice(a + 1, t.length);
                            if ((0, n.validateKey)(o) && (0, n.validateValue)(i)) {
                                e.set(o, i);
                            } else {}
                        }
                        return e;
                    }, new Map);
                    if (this._internalState.size > a) {
                        this._internalState = new Map(Array.from(this._internalState.entries()).reverse().slice(0, a));
                    }
                }
                _keys() {
                    return Array.from(this._internalState.keys()).reverse();
                }
                _clone() {
                    const e = new TraceStateImpl;
                    e._internalState = new Map(this._internalState);
                    return e;
                }
            }
            t.TraceStateImpl = TraceStateImpl;
        },
        564: (e, t)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.validateValue = t.validateKey = void 0;
            const r = "[_0-9a-z-*/]";
            const n = `[a-z]${r}{0,255}`;
            const a = `[a-z0-9]${r}{0,240}@[a-z]${r}{0,13}`;
            const o = new RegExp(`^(?:${n}|${a})$`);
            const i = /^[ -~]{0,255}[!-~]$/;
            const c = /,|=/;
            function validateKey(e) {
                return o.test(e);
            }
            t.validateKey = validateKey;
            function validateValue(e) {
                return i.test(e) && !c.test(e);
            }
            t.validateValue = validateValue;
        },
        98: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.createTraceState = void 0;
            const n = r(325);
            function createTraceState(e) {
                return new n.TraceStateImpl(e);
            }
            t.createTraceState = createTraceState;
        },
        476: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.INVALID_SPAN_CONTEXT = t.INVALID_TRACEID = t.INVALID_SPANID = void 0;
            const n = r(475);
            t.INVALID_SPANID = "0000000000000000";
            t.INVALID_TRACEID = "00000000000000000000000000000000";
            t.INVALID_SPAN_CONTEXT = {
                traceId: t.INVALID_TRACEID,
                spanId: t.INVALID_SPANID,
                traceFlags: n.TraceFlags.NONE
            };
        },
        357: (e, t)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.SpanKind = void 0;
            var r;
            (function(e) {
                e[e["INTERNAL"] = 0] = "INTERNAL";
                e[e["SERVER"] = 1] = "SERVER";
                e[e["CLIENT"] = 2] = "CLIENT";
                e[e["PRODUCER"] = 3] = "PRODUCER";
                e[e["CONSUMER"] = 4] = "CONSUMER";
            })(r = t.SpanKind || (t.SpanKind = {}));
        },
        139: (e, t, r)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.wrapSpanContext = t.isSpanContextValid = t.isValidSpanId = t.isValidTraceId = void 0;
            const n = r(476);
            const a = r(403);
            const o = /^([0-9a-f]{32})$/i;
            const i = /^[0-9a-f]{16}$/i;
            function isValidTraceId(e) {
                return o.test(e) && e !== n.INVALID_TRACEID;
            }
            t.isValidTraceId = isValidTraceId;
            function isValidSpanId(e) {
                return i.test(e) && e !== n.INVALID_SPANID;
            }
            t.isValidSpanId = isValidSpanId;
            function isSpanContextValid(e) {
                return isValidTraceId(e.traceId) && isValidSpanId(e.spanId);
            }
            t.isSpanContextValid = isSpanContextValid;
            function wrapSpanContext(e) {
                return new a.NonRecordingSpan(e);
            }
            t.wrapSpanContext = wrapSpanContext;
        },
        847: (e, t)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.SpanStatusCode = void 0;
            var r;
            (function(e) {
                e[e["UNSET"] = 0] = "UNSET";
                e[e["OK"] = 1] = "OK";
                e[e["ERROR"] = 2] = "ERROR";
            })(r = t.SpanStatusCode || (t.SpanStatusCode = {}));
        },
        475: (e, t)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.TraceFlags = void 0;
            var r;
            (function(e) {
                e[e["NONE"] = 0] = "NONE";
                e[e["SAMPLED"] = 1] = "SAMPLED";
            })(r = t.TraceFlags || (t.TraceFlags = {}));
        },
        521: (e, t)=>{
            Object.defineProperty(t, "__esModule", {
                value: true
            });
            t.VERSION = void 0;
            t.VERSION = "1.6.0";
        }
    };
    var t = {};
    function __nccwpck_require__(r) {
        var n = t[r];
        if (n !== undefined) {
            return n.exports;
        }
        var a = t[r] = {
            exports: {}
        };
        var o = true;
        try {
            e[r].call(a.exports, a, a.exports, __nccwpck_require__);
            o = false;
        } finally{
            if (o) delete t[r];
        }
        return a.exports;
    }
    if (typeof __nccwpck_require__ !== "undefined") __nccwpck_require__.ab = ("TURBOPACK compile-time value", "/ROOT/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/@opentelemetry/api") + "/";
    var r = {};
    (()=>{
        var e = r;
        Object.defineProperty(e, "__esModule", {
            value: true
        });
        e.trace = e.propagation = e.metrics = e.diag = e.context = e.INVALID_SPAN_CONTEXT = e.INVALID_TRACEID = e.INVALID_SPANID = e.isValidSpanId = e.isValidTraceId = e.isSpanContextValid = e.createTraceState = e.TraceFlags = e.SpanStatusCode = e.SpanKind = e.SamplingDecision = e.ProxyTracerProvider = e.ProxyTracer = e.defaultTextMapSetter = e.defaultTextMapGetter = e.ValueType = e.createNoopMeter = e.DiagLogLevel = e.DiagConsoleLogger = e.ROOT_CONTEXT = e.createContextKey = e.baggageEntryMetadataFromString = void 0;
        var t = __nccwpck_require__(369);
        Object.defineProperty(e, "baggageEntryMetadataFromString", {
            enumerable: true,
            get: function() {
                return t.baggageEntryMetadataFromString;
            }
        });
        var n = __nccwpck_require__(780);
        Object.defineProperty(e, "createContextKey", {
            enumerable: true,
            get: function() {
                return n.createContextKey;
            }
        });
        Object.defineProperty(e, "ROOT_CONTEXT", {
            enumerable: true,
            get: function() {
                return n.ROOT_CONTEXT;
            }
        });
        var a = __nccwpck_require__(972);
        Object.defineProperty(e, "DiagConsoleLogger", {
            enumerable: true,
            get: function() {
                return a.DiagConsoleLogger;
            }
        });
        var o = __nccwpck_require__(957);
        Object.defineProperty(e, "DiagLogLevel", {
            enumerable: true,
            get: function() {
                return o.DiagLogLevel;
            }
        });
        var i = __nccwpck_require__(102);
        Object.defineProperty(e, "createNoopMeter", {
            enumerable: true,
            get: function() {
                return i.createNoopMeter;
            }
        });
        var c = __nccwpck_require__(901);
        Object.defineProperty(e, "ValueType", {
            enumerable: true,
            get: function() {
                return c.ValueType;
            }
        });
        var s = __nccwpck_require__(194);
        Object.defineProperty(e, "defaultTextMapGetter", {
            enumerable: true,
            get: function() {
                return s.defaultTextMapGetter;
            }
        });
        Object.defineProperty(e, "defaultTextMapSetter", {
            enumerable: true,
            get: function() {
                return s.defaultTextMapSetter;
            }
        });
        var u = __nccwpck_require__(125);
        Object.defineProperty(e, "ProxyTracer", {
            enumerable: true,
            get: function() {
                return u.ProxyTracer;
            }
        });
        var l = __nccwpck_require__(846);
        Object.defineProperty(e, "ProxyTracerProvider", {
            enumerable: true,
            get: function() {
                return l.ProxyTracerProvider;
            }
        });
        var g = __nccwpck_require__(996);
        Object.defineProperty(e, "SamplingDecision", {
            enumerable: true,
            get: function() {
                return g.SamplingDecision;
            }
        });
        var p = __nccwpck_require__(357);
        Object.defineProperty(e, "SpanKind", {
            enumerable: true,
            get: function() {
                return p.SpanKind;
            }
        });
        var d = __nccwpck_require__(847);
        Object.defineProperty(e, "SpanStatusCode", {
            enumerable: true,
            get: function() {
                return d.SpanStatusCode;
            }
        });
        var _ = __nccwpck_require__(475);
        Object.defineProperty(e, "TraceFlags", {
            enumerable: true,
            get: function() {
                return _.TraceFlags;
            }
        });
        var f = __nccwpck_require__(98);
        Object.defineProperty(e, "createTraceState", {
            enumerable: true,
            get: function() {
                return f.createTraceState;
            }
        });
        var b = __nccwpck_require__(139);
        Object.defineProperty(e, "isSpanContextValid", {
            enumerable: true,
            get: function() {
                return b.isSpanContextValid;
            }
        });
        Object.defineProperty(e, "isValidTraceId", {
            enumerable: true,
            get: function() {
                return b.isValidTraceId;
            }
        });
        Object.defineProperty(e, "isValidSpanId", {
            enumerable: true,
            get: function() {
                return b.isValidSpanId;
            }
        });
        var v = __nccwpck_require__(476);
        Object.defineProperty(e, "INVALID_SPANID", {
            enumerable: true,
            get: function() {
                return v.INVALID_SPANID;
            }
        });
        Object.defineProperty(e, "INVALID_TRACEID", {
            enumerable: true,
            get: function() {
                return v.INVALID_TRACEID;
            }
        });
        Object.defineProperty(e, "INVALID_SPAN_CONTEXT", {
            enumerable: true,
            get: function() {
                return v.INVALID_SPAN_CONTEXT;
            }
        });
        const O = __nccwpck_require__(67);
        Object.defineProperty(e, "context", {
            enumerable: true,
            get: function() {
                return O.context;
            }
        });
        const P = __nccwpck_require__(506);
        Object.defineProperty(e, "diag", {
            enumerable: true,
            get: function() {
                return P.diag;
            }
        });
        const N = __nccwpck_require__(886);
        Object.defineProperty(e, "metrics", {
            enumerable: true,
            get: function() {
                return N.metrics;
            }
        });
        const S = __nccwpck_require__(939);
        Object.defineProperty(e, "propagation", {
            enumerable: true,
            get: function() {
                return S.propagation;
            }
        });
        const C = __nccwpck_require__(845);
        Object.defineProperty(e, "trace", {
            enumerable: true,
            get: function() {
                return C.trace;
            }
        });
        e["default"] = {
            context: O.context,
            diag: P.diag,
            metrics: N.metrics,
            propagation: S.propagation,
            trace: C.trace
        };
    })();
    module.exports = r;
})();
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/cookie/index.js [app-rsc] (ecmascript)", ((__turbopack_context__, module, exports) => {

(()=>{
    "use strict";
    if (typeof __nccwpck_require__ !== "undefined") __nccwpck_require__.ab = ("TURBOPACK compile-time value", "/ROOT/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/cookie") + "/";
    var e = {};
    (()=>{
        var r = e;
        /*!
 * cookie
 * Copyright(c) 2012-2014 Roman Shtylman
 * Copyright(c) 2015 Douglas Christopher Wilson
 * MIT Licensed
 */ r.parse = parse;
        r.serialize = serialize;
        var i = decodeURIComponent;
        var t = encodeURIComponent;
        var a = /; */;
        var n = /^[\u0009\u0020-\u007e\u0080-\u00ff]+$/;
        function parse(e, r) {
            if (typeof e !== "string") {
                throw new TypeError("argument str must be a string");
            }
            var t = {};
            var n = r || {};
            var o = e.split(a);
            var s = n.decode || i;
            for(var p = 0; p < o.length; p++){
                var f = o[p];
                var u = f.indexOf("=");
                if (u < 0) {
                    continue;
                }
                var v = f.substr(0, u).trim();
                var c = f.substr(++u, f.length).trim();
                if ('"' == c[0]) {
                    c = c.slice(1, -1);
                }
                if (undefined == t[v]) {
                    t[v] = tryDecode(c, s);
                }
            }
            return t;
        }
        function serialize(e, r, i) {
            var a = i || {};
            var o = a.encode || t;
            if (typeof o !== "function") {
                throw new TypeError("option encode is invalid");
            }
            if (!n.test(e)) {
                throw new TypeError("argument name is invalid");
            }
            var s = o(r);
            if (s && !n.test(s)) {
                throw new TypeError("argument val is invalid");
            }
            var p = e + "=" + s;
            if (null != a.maxAge) {
                var f = a.maxAge - 0;
                if (isNaN(f) || !isFinite(f)) {
                    throw new TypeError("option maxAge is invalid");
                }
                p += "; Max-Age=" + Math.floor(f);
            }
            if (a.domain) {
                if (!n.test(a.domain)) {
                    throw new TypeError("option domain is invalid");
                }
                p += "; Domain=" + a.domain;
            }
            if (a.path) {
                if (!n.test(a.path)) {
                    throw new TypeError("option path is invalid");
                }
                p += "; Path=" + a.path;
            }
            if (a.expires) {
                if (typeof a.expires.toUTCString !== "function") {
                    throw new TypeError("option expires is invalid");
                }
                p += "; Expires=" + a.expires.toUTCString();
            }
            if (a.httpOnly) {
                p += "; HttpOnly";
            }
            if (a.secure) {
                p += "; Secure";
            }
            if (a.sameSite) {
                var u = typeof a.sameSite === "string" ? a.sameSite.toLowerCase() : a.sameSite;
                switch(u){
                    case true:
                        p += "; SameSite=Strict";
                        break;
                    case "lax":
                        p += "; SameSite=Lax";
                        break;
                    case "strict":
                        p += "; SameSite=Strict";
                        break;
                    case "none":
                        p += "; SameSite=None";
                        break;
                    default:
                        throw new TypeError("option sameSite is invalid");
                }
            }
            return p;
        }
        function tryDecode(e, r) {
            try {
                return r(e);
            } catch (r) {
                return e;
            }
        }
    })();
    module.exports = e;
})();
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/@edge-runtime/cookies/index.js [app-rsc] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all)=>{
    for(var name in all)__defProp(target, name, {
        get: all[name],
        enumerable: true
    });
};
var __copyProps = (to, from, except, desc)=>{
    if (from && typeof from === "object" || typeof from === "function") {
        for (let key of __getOwnPropNames(from))if (!__hasOwnProp.call(to, key) && key !== except) __defProp(to, key, {
            get: ()=>from[key],
            enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable
        });
    }
    return to;
};
var __toCommonJS = (mod)=>__copyProps(__defProp({}, "__esModule", {
        value: true
    }), mod);
// src/index.ts
var src_exports = {};
__export(src_exports, {
    RequestCookies: ()=>RequestCookies,
    ResponseCookies: ()=>ResponseCookies,
    parseCookie: ()=>parseCookie,
    parseSetCookie: ()=>parseSetCookie,
    stringifyCookie: ()=>stringifyCookie
});
module.exports = __toCommonJS(src_exports);
// src/serialize.ts
function stringifyCookie(c) {
    var _a;
    const attrs = [
        "path" in c && c.path && `Path=${c.path}`,
        "expires" in c && (c.expires || c.expires === 0) && `Expires=${(typeof c.expires === "number" ? new Date(c.expires) : c.expires).toUTCString()}`,
        "maxAge" in c && typeof c.maxAge === "number" && `Max-Age=${c.maxAge}`,
        "domain" in c && c.domain && `Domain=${c.domain}`,
        "secure" in c && c.secure && "Secure",
        "httpOnly" in c && c.httpOnly && "HttpOnly",
        "sameSite" in c && c.sameSite && `SameSite=${c.sameSite}`,
        "partitioned" in c && c.partitioned && "Partitioned",
        "priority" in c && c.priority && `Priority=${c.priority}`
    ].filter(Boolean);
    const stringified = `${c.name}=${encodeURIComponent((_a = c.value) != null ? _a : "")}`;
    return attrs.length === 0 ? stringified : `${stringified}; ${attrs.join("; ")}`;
}
function parseCookie(cookie) {
    const map = /* @__PURE__ */ new Map();
    for (const pair of cookie.split(/; */)){
        if (!pair) continue;
        const splitAt = pair.indexOf("=");
        if (splitAt === -1) {
            map.set(pair, "true");
            continue;
        }
        const [key, value] = [
            pair.slice(0, splitAt),
            pair.slice(splitAt + 1)
        ];
        try {
            map.set(key, decodeURIComponent(value != null ? value : "true"));
        } catch  {}
    }
    return map;
}
function parseSetCookie(setCookie) {
    if (!setCookie) {
        return void 0;
    }
    const [[name, value], ...attributes] = parseCookie(setCookie);
    const { domain, expires, httponly, maxage, path, samesite, secure, partitioned, priority } = Object.fromEntries(attributes.map(([key, value2])=>[
            key.toLowerCase().replace(/-/g, ""),
            value2
        ]));
    const cookie = {
        name,
        value: decodeURIComponent(value),
        domain,
        ...expires && {
            expires: new Date(expires)
        },
        ...httponly && {
            httpOnly: true
        },
        ...typeof maxage === "string" && {
            maxAge: Number(maxage)
        },
        path,
        ...samesite && {
            sameSite: parseSameSite(samesite)
        },
        ...secure && {
            secure: true
        },
        ...priority && {
            priority: parsePriority(priority)
        },
        ...partitioned && {
            partitioned: true
        }
    };
    return compact(cookie);
}
function compact(t) {
    const newT = {};
    for(const key in t){
        if (t[key]) {
            newT[key] = t[key];
        }
    }
    return newT;
}
var SAME_SITE = [
    "strict",
    "lax",
    "none"
];
function parseSameSite(string) {
    string = string.toLowerCase();
    return SAME_SITE.includes(string) ? string : void 0;
}
var PRIORITY = [
    "low",
    "medium",
    "high"
];
function parsePriority(string) {
    string = string.toLowerCase();
    return PRIORITY.includes(string) ? string : void 0;
}
function splitCookiesString(cookiesString) {
    if (!cookiesString) return [];
    var cookiesStrings = [];
    var pos = 0;
    var start;
    var ch;
    var lastComma;
    var nextStart;
    var cookiesSeparatorFound;
    function skipWhitespace() {
        while(pos < cookiesString.length && /\s/.test(cookiesString.charAt(pos))){
            pos += 1;
        }
        return pos < cookiesString.length;
    }
    function notSpecialChar() {
        ch = cookiesString.charAt(pos);
        return ch !== "=" && ch !== ";" && ch !== ",";
    }
    while(pos < cookiesString.length){
        start = pos;
        cookiesSeparatorFound = false;
        while(skipWhitespace()){
            ch = cookiesString.charAt(pos);
            if (ch === ",") {
                lastComma = pos;
                pos += 1;
                skipWhitespace();
                nextStart = pos;
                while(pos < cookiesString.length && notSpecialChar()){
                    pos += 1;
                }
                if (pos < cookiesString.length && cookiesString.charAt(pos) === "=") {
                    cookiesSeparatorFound = true;
                    pos = nextStart;
                    cookiesStrings.push(cookiesString.substring(start, lastComma));
                    start = pos;
                } else {
                    pos = lastComma + 1;
                }
            } else {
                pos += 1;
            }
        }
        if (!cookiesSeparatorFound || pos >= cookiesString.length) {
            cookiesStrings.push(cookiesString.substring(start, cookiesString.length));
        }
    }
    return cookiesStrings;
}
// src/request-cookies.ts
var RequestCookies = class {
    constructor(requestHeaders){
        /** @internal */ this._parsed = /* @__PURE__ */ new Map();
        this._headers = requestHeaders;
        const header = requestHeaders.get("cookie");
        if (header) {
            const parsed = parseCookie(header);
            for (const [name, value] of parsed){
                this._parsed.set(name, {
                    name,
                    value
                });
            }
        }
    }
    [Symbol.iterator]() {
        return this._parsed[Symbol.iterator]();
    }
    /**
   * The amount of cookies received from the client
   */ get size() {
        return this._parsed.size;
    }
    get(...args) {
        const name = typeof args[0] === "string" ? args[0] : args[0].name;
        return this._parsed.get(name);
    }
    getAll(...args) {
        var _a;
        const all = Array.from(this._parsed);
        if (!args.length) {
            return all.map(([_, value])=>value);
        }
        const name = typeof args[0] === "string" ? args[0] : (_a = args[0]) == null ? void 0 : _a.name;
        return all.filter(([n])=>n === name).map(([_, value])=>value);
    }
    has(name) {
        return this._parsed.has(name);
    }
    set(...args) {
        const [name, value] = args.length === 1 ? [
            args[0].name,
            args[0].value
        ] : args;
        const map = this._parsed;
        map.set(name, {
            name,
            value
        });
        this._headers.set("cookie", Array.from(map).map(([_, value2])=>stringifyCookie(value2)).join("; "));
        return this;
    }
    /**
   * Delete the cookies matching the passed name or names in the request.
   */ delete(names) {
        const map = this._parsed;
        const result = !Array.isArray(names) ? map.delete(names) : names.map((name)=>map.delete(name));
        this._headers.set("cookie", Array.from(map).map(([_, value])=>stringifyCookie(value)).join("; "));
        return result;
    }
    /**
   * Delete all the cookies in the cookies in the request.
   */ clear() {
        this.delete(Array.from(this._parsed.keys()));
        return this;
    }
    /**
   * Format the cookies in the request as a string for logging
   */ [Symbol.for("edge-runtime.inspect.custom")]() {
        return `RequestCookies ${JSON.stringify(Object.fromEntries(this._parsed))}`;
    }
    toString() {
        return [
            ...this._parsed.values()
        ].map((v)=>`${v.name}=${encodeURIComponent(v.value)}`).join("; ");
    }
};
// src/response-cookies.ts
var ResponseCookies = class {
    constructor(responseHeaders){
        /** @internal */ this._parsed = /* @__PURE__ */ new Map();
        var _a, _b, _c;
        this._headers = responseHeaders;
        const setCookie = (_c = (_b = (_a = responseHeaders.getSetCookie) == null ? void 0 : _a.call(responseHeaders)) != null ? _b : responseHeaders.get("set-cookie")) != null ? _c : [];
        const cookieStrings = Array.isArray(setCookie) ? setCookie : splitCookiesString(setCookie);
        for (const cookieString of cookieStrings){
            const parsed = parseSetCookie(cookieString);
            if (parsed) this._parsed.set(parsed.name, parsed);
        }
    }
    /**
   * {@link https://wicg.github.io/cookie-store/#CookieStore-get CookieStore#get} without the Promise.
   */ get(...args) {
        const key = typeof args[0] === "string" ? args[0] : args[0].name;
        return this._parsed.get(key);
    }
    /**
   * {@link https://wicg.github.io/cookie-store/#CookieStore-getAll CookieStore#getAll} without the Promise.
   */ getAll(...args) {
        var _a;
        const all = Array.from(this._parsed.values());
        if (!args.length) {
            return all;
        }
        const key = typeof args[0] === "string" ? args[0] : (_a = args[0]) == null ? void 0 : _a.name;
        return all.filter((c)=>c.name === key);
    }
    has(name) {
        return this._parsed.has(name);
    }
    /**
   * {@link https://wicg.github.io/cookie-store/#CookieStore-set CookieStore#set} without the Promise.
   */ set(...args) {
        const [name, value, cookie] = args.length === 1 ? [
            args[0].name,
            args[0].value,
            args[0]
        ] : args;
        const map = this._parsed;
        map.set(name, normalizeCookie({
            name,
            value,
            ...cookie
        }));
        replace(map, this._headers);
        return this;
    }
    /**
   * {@link https://wicg.github.io/cookie-store/#CookieStore-delete CookieStore#delete} without the Promise.
   */ delete(...args) {
        const [name, options] = typeof args[0] === "string" ? [
            args[0]
        ] : [
            args[0].name,
            args[0]
        ];
        return this.set({
            ...options,
            name,
            value: "",
            expires: /* @__PURE__ */ new Date(0)
        });
    }
    [Symbol.for("edge-runtime.inspect.custom")]() {
        return `ResponseCookies ${JSON.stringify(Object.fromEntries(this._parsed))}`;
    }
    toString() {
        return [
            ...this._parsed.values()
        ].map(stringifyCookie).join("; ");
    }
};
function replace(bag, headers) {
    headers.delete("set-cookie");
    for (const [, value] of bag){
        const serialized = stringifyCookie(value);
        headers.append("set-cookie", serialized);
    }
}
function normalizeCookie(cookie = {
    name: "",
    value: ""
}) {
    if (typeof cookie.expires === "number") {
        cookie.expires = new Date(cookie.expires);
    }
    if (cookie.maxAge) {
        cookie.expires = new Date(Date.now() + cookie.maxAge * 1e3);
    }
    if (cookie.path === null || cookie.path === void 0) {
        cookie.path = "/";
    }
    return cookie;
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
    RequestCookies,
    ResponseCookies,
    parseCookie,
    parseSetCookie,
    stringifyCookie
});
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/fresh/index.js [app-rsc] (ecmascript)", ((__turbopack_context__, module, exports) => {

(()=>{
    "use strict";
    var e = {
        695: (e)=>{
            /*!
 * fresh
 * Copyright(c) 2012 TJ Holowaychuk
 * Copyright(c) 2016-2017 Douglas Christopher Wilson
 * MIT Licensed
 */ var r = /(?:^|,)\s*?no-cache\s*?(?:,|$)/;
            e.exports = fresh;
            function fresh(e, a) {
                var t = e["if-modified-since"];
                var s = e["if-none-match"];
                if (!t && !s) {
                    return false;
                }
                var i = e["cache-control"];
                if (i && r.test(i)) {
                    return false;
                }
                if (s && s !== "*") {
                    var f = a["etag"];
                    if (!f) {
                        return false;
                    }
                    var n = true;
                    var u = parseTokenList(s);
                    for(var _ = 0; _ < u.length; _++){
                        var o = u[_];
                        if (o === f || o === "W/" + f || "W/" + o === f) {
                            n = false;
                            break;
                        }
                    }
                    if (n) {
                        return false;
                    }
                }
                if (t) {
                    var p = a["last-modified"];
                    var v = !p || !(parseHttpDate(p) <= parseHttpDate(t));
                    if (v) {
                        return false;
                    }
                }
                return true;
            }
            function parseHttpDate(e) {
                var r = e && Date.parse(e);
                return typeof r === "number" ? r : NaN;
            }
            function parseTokenList(e) {
                var r = 0;
                var a = [];
                var t = 0;
                for(var s = 0, i = e.length; s < i; s++){
                    switch(e.charCodeAt(s)){
                        case 32:
                            if (t === r) {
                                t = r = s + 1;
                            }
                            break;
                        case 44:
                            a.push(e.substring(t, r));
                            t = r = s + 1;
                            break;
                        default:
                            r = s + 1;
                            break;
                    }
                }
                a.push(e.substring(t, r));
                return a;
            }
        }
    };
    var r = {};
    function __nccwpck_require__(a) {
        var t = r[a];
        if (t !== undefined) {
            return t.exports;
        }
        var s = r[a] = {
            exports: {}
        };
        var i = true;
        try {
            e[a](s, s.exports, __nccwpck_require__);
            i = false;
        } finally{
            if (i) delete r[a];
        }
        return s.exports;
    }
    if (typeof __nccwpck_require__ !== "undefined") __nccwpck_require__.ab = ("TURBOPACK compile-time value", "/ROOT/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/fresh") + "/";
    var a = __nccwpck_require__(695);
    module.exports = a;
})();
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/bytes/index.js [app-rsc] (ecmascript)", ((__turbopack_context__, module, exports) => {

(()=>{
    "use strict";
    var e = {
        56: (e)=>{
            /*!
 * bytes
 * Copyright(c) 2012-2014 TJ Holowaychuk
 * Copyright(c) 2015 Jed Watson
 * MIT Licensed
 */ e.exports = bytes;
            e.exports.format = format;
            e.exports.parse = parse;
            var r = /\B(?=(\d{3})+(?!\d))/g;
            var a = /(?:\.0*|(\.[^0]+)0+)$/;
            var t = {
                b: 1,
                kb: 1 << 10,
                mb: 1 << 20,
                gb: 1 << 30,
                tb: Math.pow(1024, 4),
                pb: Math.pow(1024, 5)
            };
            var i = /^((-|\+)?(\d+(?:\.\d+)?)) *(kb|mb|gb|tb|pb)$/i;
            function bytes(e, r) {
                if (typeof e === "string") {
                    return parse(e);
                }
                if (typeof e === "number") {
                    return format(e, r);
                }
                return null;
            }
            function format(e, i) {
                if (!Number.isFinite(e)) {
                    return null;
                }
                var n = Math.abs(e);
                var o = i && i.thousandsSeparator || "";
                var s = i && i.unitSeparator || "";
                var f = i && i.decimalPlaces !== undefined ? i.decimalPlaces : 2;
                var u = Boolean(i && i.fixedDecimals);
                var p = i && i.unit || "";
                if (!p || !t[p.toLowerCase()]) {
                    if (n >= t.pb) {
                        p = "PB";
                    } else if (n >= t.tb) {
                        p = "TB";
                    } else if (n >= t.gb) {
                        p = "GB";
                    } else if (n >= t.mb) {
                        p = "MB";
                    } else if (n >= t.kb) {
                        p = "KB";
                    } else {
                        p = "B";
                    }
                }
                var b = e / t[p.toLowerCase()];
                var l = b.toFixed(f);
                if (!u) {
                    l = l.replace(a, "$1");
                }
                if (o) {
                    l = l.split(".").map(function(e, a) {
                        return a === 0 ? e.replace(r, o) : e;
                    }).join(".");
                }
                return l + s + p;
            }
            function parse(e) {
                if (typeof e === "number" && !isNaN(e)) {
                    return e;
                }
                if (typeof e !== "string") {
                    return null;
                }
                var r = i.exec(e);
                var a;
                var n = "b";
                if (!r) {
                    a = parseInt(e, 10);
                    n = "b";
                } else {
                    a = parseFloat(r[1]);
                    n = r[4].toLowerCase();
                }
                return Math.floor(t[n] * a);
            }
        }
    };
    var r = {};
    function __nccwpck_require__(a) {
        var t = r[a];
        if (t !== undefined) {
            return t.exports;
        }
        var i = r[a] = {
            exports: {}
        };
        var n = true;
        try {
            e[a](i, i.exports, __nccwpck_require__);
            n = false;
        } finally{
            if (n) delete r[a];
        }
        return i.exports;
    }
    if (typeof __nccwpck_require__ !== "undefined") __nccwpck_require__.ab = ("TURBOPACK compile-time value", "/ROOT/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/bytes") + "/";
    var a = __nccwpck_require__(56);
    module.exports = a;
})();
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-server-dom-turbopack/cjs/react-server-dom-turbopack-client.node.development.js [app-rsc] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

/**
 * @license React
 * react-server-dom-turbopack-client.node.development.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */ "production" !== ("TURBOPACK compile-time value", "development") && function() {
    function checkEvalAvailabilityOnceDev() {
        if (!hasConfirmedEval) {
            hasConfirmedEval = !0;
            try {
                (0, eval)("null");
            } catch ($jscomp$unused$catch) {
                console.error("eval() is not supported in this environment. This can happen if you started the Node.js process with --disallow-code-generation-from-strings, or if `eval` was patched by other means. React requires eval() in development mode for various debugging features like reconstructing callstacks from a different environment.\nReact will never use eval() in production mode");
            }
        }
    }
    function resolveClientReference(bundlerConfig, metadata) {
        if (bundlerConfig) {
            var moduleExports = bundlerConfig[metadata[0]];
            if (bundlerConfig = moduleExports && moduleExports[metadata[2]]) moduleExports = bundlerConfig.name;
            else {
                bundlerConfig = moduleExports && moduleExports["*"];
                if (!bundlerConfig) throw Error('Could not find the module "' + metadata[0] + '" in the React Server Consumer Manifest. This is probably a bug in the React Server Components bundler.');
                moduleExports = metadata[2];
            }
            return 4 === metadata.length ? [
                bundlerConfig.id,
                bundlerConfig.chunks,
                moduleExports,
                1
            ] : [
                bundlerConfig.id,
                bundlerConfig.chunks,
                moduleExports
            ];
        }
        return metadata;
    }
    function resolveServerReference(bundlerConfig, id) {
        var name = "", resolvedModuleData = bundlerConfig[id];
        if (resolvedModuleData) name = resolvedModuleData.name;
        else {
            var idx = id.lastIndexOf("#");
            -1 !== idx && (name = id.slice(idx + 1), resolvedModuleData = bundlerConfig[id.slice(0, idx)]);
            if (!resolvedModuleData) throw Error('Could not find the module "' + id + '" in the React Server Manifest. This is probably a bug in the React Server Components bundler.');
        }
        return resolvedModuleData.async ? [
            resolvedModuleData.id,
            resolvedModuleData.chunks,
            name,
            1
        ] : [
            resolvedModuleData.id,
            resolvedModuleData.chunks,
            name
        ];
    }
    function requireAsyncModule(id) {
        var promise = globalThis.__next_require__(id);
        if ("function" !== typeof promise.then || "fulfilled" === promise.status) return null;
        promise.then(function(value) {
            promise.status = "fulfilled";
            promise.value = value;
        }, function(reason) {
            promise.status = "rejected";
            promise.reason = reason;
        });
        return promise;
    }
    function ignoreReject() {}
    function preloadModule(metadata) {
        for(var chunks = metadata[1], promises = [], i = 0; i < chunks.length; i++){
            var thenable = globalThis.__next_chunk_load__(chunks[i]);
            loadedChunks.has(thenable) || promises.push(thenable);
            if (!instrumentedChunks.has(thenable)) {
                var resolve = loadedChunks.add.bind(loadedChunks, thenable);
                thenable.then(resolve, ignoreReject);
                instrumentedChunks.add(thenable);
            }
        }
        return 4 === metadata.length ? 0 === promises.length ? requireAsyncModule(metadata[0]) : Promise.all(promises).then(function() {
            return requireAsyncModule(metadata[0]);
        }) : 0 < promises.length ? Promise.all(promises) : null;
    }
    function requireModule(metadata) {
        var moduleExports = globalThis.__next_require__(metadata[0]);
        if (4 === metadata.length && "function" === typeof moduleExports.then) if ("fulfilled" === moduleExports.status) moduleExports = moduleExports.value;
        else throw moduleExports.reason;
        if ("*" === metadata[2]) return moduleExports;
        if ("" === metadata[2]) return moduleExports.__esModule ? moduleExports.default : moduleExports;
        if (hasOwnProperty.call(moduleExports, metadata[2])) return moduleExports[metadata[2]];
    }
    function prepareDestinationWithChunks(moduleLoading, chunks, nonce$jscomp$0) {
        if (null !== moduleLoading) for(var i = 0; i < chunks.length; i++){
            var nonce = nonce$jscomp$0, JSCompiler_temp_const = ReactDOMSharedInternals.d, JSCompiler_temp_const$jscomp$0 = JSCompiler_temp_const.X, JSCompiler_temp_const$jscomp$1 = moduleLoading.prefix + chunks[i];
            var JSCompiler_inline_result = moduleLoading.crossOrigin;
            JSCompiler_inline_result = "string" === typeof JSCompiler_inline_result ? "use-credentials" === JSCompiler_inline_result ? JSCompiler_inline_result : "" : void 0;
            JSCompiler_temp_const$jscomp$0.call(JSCompiler_temp_const, JSCompiler_temp_const$jscomp$1, {
                crossOrigin: JSCompiler_inline_result,
                nonce: nonce
            });
        }
    }
    function getIteratorFn(maybeIterable) {
        if (null === maybeIterable || "object" !== typeof maybeIterable) return null;
        maybeIterable = MAYBE_ITERATOR_SYMBOL && maybeIterable[MAYBE_ITERATOR_SYMBOL] || maybeIterable["@@iterator"];
        return "function" === typeof maybeIterable ? maybeIterable : null;
    }
    function isObjectPrototype(object) {
        if (!object) return !1;
        var ObjectPrototype = Object.prototype;
        if (object === ObjectPrototype) return !0;
        if (getPrototypeOf(object)) return !1;
        object = Object.getOwnPropertyNames(object);
        for(var i = 0; i < object.length; i++)if (!(object[i] in ObjectPrototype)) return !1;
        return !0;
    }
    function isSimpleObject(object) {
        if (!isObjectPrototype(getPrototypeOf(object))) return !1;
        for(var names = Object.getOwnPropertyNames(object), i = 0; i < names.length; i++){
            var descriptor = Object.getOwnPropertyDescriptor(object, names[i]);
            if (!descriptor || !descriptor.enumerable && ("key" !== names[i] && "ref" !== names[i] || "function" !== typeof descriptor.get)) return !1;
        }
        return !0;
    }
    function objectName(object) {
        object = Object.prototype.toString.call(object);
        return object.slice(8, object.length - 1);
    }
    function describeKeyForErrorMessage(key) {
        var encodedKey = JSON.stringify(key);
        return '"' + key + '"' === encodedKey ? key : encodedKey;
    }
    function describeValueForErrorMessage(value) {
        switch(typeof value){
            case "string":
                return JSON.stringify(10 >= value.length ? value : value.slice(0, 10) + "...");
            case "object":
                if (isArrayImpl(value)) return "[...]";
                if (null !== value && value.$$typeof === CLIENT_REFERENCE_TAG) return "client";
                value = objectName(value);
                return "Object" === value ? "{...}" : value;
            case "function":
                return value.$$typeof === CLIENT_REFERENCE_TAG ? "client" : (value = value.displayName || value.name) ? "function " + value : "function";
            default:
                return String(value);
        }
    }
    function describeElementType(type) {
        if ("string" === typeof type) return type;
        switch(type){
            case REACT_SUSPENSE_TYPE:
                return "Suspense";
            case REACT_SUSPENSE_LIST_TYPE:
                return "SuspenseList";
            case REACT_VIEW_TRANSITION_TYPE:
                return "ViewTransition";
        }
        if ("object" === typeof type) switch(type.$$typeof){
            case REACT_FORWARD_REF_TYPE:
                return describeElementType(type.render);
            case REACT_MEMO_TYPE:
                return describeElementType(type.type);
            case REACT_LAZY_TYPE:
                var payload = type._payload;
                type = type._init;
                try {
                    return describeElementType(type(payload));
                } catch (x) {}
        }
        return "";
    }
    function describeObjectForErrorMessage(objectOrArray, expandedName) {
        var objKind = objectName(objectOrArray);
        if ("Object" !== objKind && "Array" !== objKind) return objKind;
        var start = -1, length = 0;
        if (isArrayImpl(objectOrArray)) if (jsxChildrenParents.has(objectOrArray)) {
            var type = jsxChildrenParents.get(objectOrArray);
            objKind = "<" + describeElementType(type) + ">";
            for(var i = 0; i < objectOrArray.length; i++){
                var value = objectOrArray[i];
                value = "string" === typeof value ? value : "object" === typeof value && null !== value ? "{" + describeObjectForErrorMessage(value) + "}" : "{" + describeValueForErrorMessage(value) + "}";
                "" + i === expandedName ? (start = objKind.length, length = value.length, objKind += value) : objKind = 15 > value.length && 40 > objKind.length + value.length ? objKind + value : objKind + "{...}";
            }
            objKind += "</" + describeElementType(type) + ">";
        } else {
            objKind = "[";
            for(type = 0; type < objectOrArray.length; type++)0 < type && (objKind += ", "), i = objectOrArray[type], i = "object" === typeof i && null !== i ? describeObjectForErrorMessage(i) : describeValueForErrorMessage(i), "" + type === expandedName ? (start = objKind.length, length = i.length, objKind += i) : objKind = 10 > i.length && 40 > objKind.length + i.length ? objKind + i : objKind + "...";
            objKind += "]";
        }
        else if (objectOrArray.$$typeof === REACT_ELEMENT_TYPE) objKind = "<" + describeElementType(objectOrArray.type) + "/>";
        else {
            if (objectOrArray.$$typeof === CLIENT_REFERENCE_TAG) return "client";
            if (jsxPropsParents.has(objectOrArray)) {
                objKind = jsxPropsParents.get(objectOrArray);
                objKind = "<" + (describeElementType(objKind) || "...");
                type = Object.keys(objectOrArray);
                for(i = 0; i < type.length; i++){
                    objKind += " ";
                    value = type[i];
                    objKind += describeKeyForErrorMessage(value) + "=";
                    var _value2 = objectOrArray[value];
                    var _substr2 = value === expandedName && "object" === typeof _value2 && null !== _value2 ? describeObjectForErrorMessage(_value2) : describeValueForErrorMessage(_value2);
                    "string" !== typeof _value2 && (_substr2 = "{" + _substr2 + "}");
                    value === expandedName ? (start = objKind.length, length = _substr2.length, objKind += _substr2) : objKind = 10 > _substr2.length && 40 > objKind.length + _substr2.length ? objKind + _substr2 : objKind + "...";
                }
                objKind += ">";
            } else {
                objKind = "{";
                type = Object.keys(objectOrArray);
                for(i = 0; i < type.length; i++)0 < i && (objKind += ", "), value = type[i], objKind += describeKeyForErrorMessage(value) + ": ", _value2 = objectOrArray[value], _value2 = "object" === typeof _value2 && null !== _value2 ? describeObjectForErrorMessage(_value2) : describeValueForErrorMessage(_value2), value === expandedName ? (start = objKind.length, length = _value2.length, objKind += _value2) : objKind = 10 > _value2.length && 40 > objKind.length + _value2.length ? objKind + _value2 : objKind + "...";
                objKind += "}";
            }
        }
        return void 0 === expandedName ? objKind : -1 < start && 0 < length ? (objectOrArray = " ".repeat(start) + "^".repeat(length), "\n  " + objKind + "\n  " + objectOrArray) : "\n  " + objKind;
    }
    function serializeNumber(number) {
        return Number.isFinite(number) ? 0 === number && -Infinity === 1 / number ? "$-0" : number : Infinity === number ? "$Infinity" : -Infinity === number ? "$-Infinity" : "$NaN";
    }
    function processReply(root, formFieldPrefix, temporaryReferences, resolve, reject) {
        function serializeTypedArray(tag, typedArray) {
            typedArray = new Blob([
                new Uint8Array(typedArray.buffer, typedArray.byteOffset, typedArray.byteLength)
            ]);
            var blobId = nextPartId++;
            null === formData && (formData = new FormData());
            formData.append(formFieldPrefix + blobId, typedArray);
            return "$" + tag + blobId.toString(16);
        }
        function serializeBinaryReader(reader) {
            function progress(entry) {
                entry.done ? (entry = nextPartId++, data.append(formFieldPrefix + entry, new Blob(buffer)), data.append(formFieldPrefix + streamId, '"$o' + entry.toString(16) + '"'), data.append(formFieldPrefix + streamId, "C"), pendingParts--, 0 === pendingParts && resolve(data)) : (buffer.push(entry.value), reader.read(new Uint8Array(1024)).then(progress, reject));
            }
            null === formData && (formData = new FormData());
            var data = formData;
            pendingParts++;
            var streamId = nextPartId++, buffer = [];
            reader.read(new Uint8Array(1024)).then(progress, reject);
            return "$r" + streamId.toString(16);
        }
        function serializeReader(reader) {
            function progress(entry) {
                if (entry.done) data.append(formFieldPrefix + streamId, "C"), pendingParts--, 0 === pendingParts && resolve(data);
                else try {
                    var partJSON = JSON.stringify(entry.value, resolveToJSON);
                    data.append(formFieldPrefix + streamId, partJSON);
                    reader.read().then(progress, reject);
                } catch (x) {
                    reject(x);
                }
            }
            null === formData && (formData = new FormData());
            var data = formData;
            pendingParts++;
            var streamId = nextPartId++;
            reader.read().then(progress, reject);
            return "$R" + streamId.toString(16);
        }
        function serializeReadableStream(stream) {
            try {
                var binaryReader = stream.getReader({
                    mode: "byob"
                });
            } catch (x) {
                return serializeReader(stream.getReader());
            }
            return serializeBinaryReader(binaryReader);
        }
        function serializeAsyncIterable(iterable, iterator) {
            function progress(entry) {
                if (entry.done) {
                    if (void 0 === entry.value) data.append(formFieldPrefix + streamId, "C");
                    else try {
                        var partJSON = JSON.stringify(entry.value, resolveToJSON);
                        data.append(formFieldPrefix + streamId, "C" + partJSON);
                    } catch (x) {
                        reject(x);
                        return;
                    }
                    pendingParts--;
                    0 === pendingParts && resolve(data);
                } else try {
                    var _partJSON = JSON.stringify(entry.value, resolveToJSON);
                    data.append(formFieldPrefix + streamId, _partJSON);
                    iterator.next().then(progress, reject);
                } catch (x$0) {
                    reject(x$0);
                }
            }
            null === formData && (formData = new FormData());
            var data = formData;
            pendingParts++;
            var streamId = nextPartId++;
            iterable = iterable === iterator;
            iterator.next().then(progress, reject);
            return "$" + (iterable ? "x" : "X") + streamId.toString(16);
        }
        function resolveToJSON(key, value) {
            "__proto__" === key && console.error("Expected not to serialize an object with own property `__proto__`. When parsed this property will be omitted.%s", describeObjectForErrorMessage(this, key));
            var originalValue = this[key];
            "object" !== typeof originalValue || originalValue === value || originalValue instanceof Date || ("Object" !== objectName(originalValue) ? console.error("Only plain objects can be passed to Server Functions from the Client. %s objects are not supported.%s", objectName(originalValue), describeObjectForErrorMessage(this, key)) : console.error("Only plain objects can be passed to Server Functions from the Client. Objects with toJSON methods are not supported. Convert it manually to a simple value before passing it to props.%s", describeObjectForErrorMessage(this, key)));
            if (null === value) return null;
            if ("object" === typeof value) {
                switch(value.$$typeof){
                    case REACT_ELEMENT_TYPE:
                        if (void 0 !== temporaryReferences && -1 === key.indexOf(":")) {
                            var parentReference = writtenObjects.get(this);
                            if (void 0 !== parentReference) return temporaryReferences.set(parentReference + ":" + key, value), "$T";
                        }
                        if (void 0 !== temporaryReferences && modelRoot === value) return modelRoot = null, "$T";
                        throw Error("React Element cannot be passed to Server Functions from the Client without a temporary reference set. Pass a TemporaryReferenceSet to the options." + describeObjectForErrorMessage(this, key));
                    case REACT_LAZY_TYPE:
                        originalValue = value._payload;
                        var init = value._init;
                        null === formData && (formData = new FormData());
                        pendingParts++;
                        try {
                            parentReference = init(originalValue);
                            var lazyId = nextPartId++, partJSON = serializeModel(parentReference, lazyId);
                            formData.append(formFieldPrefix + lazyId, partJSON);
                            return "$" + lazyId.toString(16);
                        } catch (x) {
                            if ("object" === typeof x && null !== x && "function" === typeof x.then) {
                                pendingParts++;
                                var _lazyId = nextPartId++;
                                parentReference = function() {
                                    try {
                                        var _partJSON2 = serializeModel(value, _lazyId), _data = formData;
                                        _data.append(formFieldPrefix + _lazyId, _partJSON2);
                                        pendingParts--;
                                        0 === pendingParts && resolve(_data);
                                    } catch (reason) {
                                        reject(reason);
                                    }
                                };
                                x.then(parentReference, parentReference);
                                return "$" + _lazyId.toString(16);
                            }
                            reject(x);
                            return null;
                        } finally{
                            pendingParts--;
                        }
                }
                parentReference = writtenObjects.get(value);
                if ("function" === typeof value.then) {
                    if (void 0 !== parentReference) if (modelRoot === value) modelRoot = null;
                    else return parentReference;
                    null === formData && (formData = new FormData());
                    pendingParts++;
                    var promiseId = nextPartId++;
                    key = "$@" + promiseId.toString(16);
                    writtenObjects.set(value, key);
                    value.then(function(partValue) {
                        try {
                            var previousReference = writtenObjects.get(partValue);
                            var _partJSON3 = void 0 !== previousReference ? JSON.stringify(previousReference) : serializeModel(partValue, promiseId);
                            partValue = formData;
                            partValue.append(formFieldPrefix + promiseId, _partJSON3);
                            pendingParts--;
                            0 === pendingParts && resolve(partValue);
                        } catch (reason) {
                            reject(reason);
                        }
                    }, reject);
                    return key;
                }
                if (void 0 !== parentReference) if (modelRoot === value) modelRoot = null;
                else return parentReference;
                else -1 === key.indexOf(":") && (parentReference = writtenObjects.get(this), void 0 !== parentReference && (parentReference = parentReference + ":" + key, writtenObjects.set(value, parentReference), void 0 !== temporaryReferences && temporaryReferences.set(parentReference, value)));
                if (isArrayImpl(value)) return value;
                if (value instanceof FormData) {
                    null === formData && (formData = new FormData());
                    var _data3 = formData;
                    key = nextPartId++;
                    var prefix = formFieldPrefix + "_" + key + "_";
                    value.forEach(function(originalValue, originalKey) {
                        _data3.append(prefix + originalKey, originalValue);
                    });
                    return "$K" + key.toString(16);
                }
                if (value instanceof Map) return key = nextPartId++, parentReference = serializeModel(Array.from(value), key), null === formData && (formData = new FormData()), formData.append(formFieldPrefix + key, parentReference), "$Q" + key.toString(16);
                if (value instanceof Set) return key = nextPartId++, parentReference = serializeModel(Array.from(value), key), null === formData && (formData = new FormData()), formData.append(formFieldPrefix + key, parentReference), "$W" + key.toString(16);
                if (value instanceof ArrayBuffer) return key = new Blob([
                    value
                ]), parentReference = nextPartId++, null === formData && (formData = new FormData()), formData.append(formFieldPrefix + parentReference, key), "$A" + parentReference.toString(16);
                if (value instanceof Int8Array) return serializeTypedArray("O", value);
                if (value instanceof Uint8Array) return serializeTypedArray("o", value);
                if (value instanceof Uint8ClampedArray) return serializeTypedArray("U", value);
                if (value instanceof Int16Array) return serializeTypedArray("S", value);
                if (value instanceof Uint16Array) return serializeTypedArray("s", value);
                if (value instanceof Int32Array) return serializeTypedArray("L", value);
                if (value instanceof Uint32Array) return serializeTypedArray("l", value);
                if (value instanceof Float32Array) return serializeTypedArray("G", value);
                if (value instanceof Float64Array) return serializeTypedArray("g", value);
                if (value instanceof BigInt64Array) return serializeTypedArray("M", value);
                if (value instanceof BigUint64Array) return serializeTypedArray("m", value);
                if (value instanceof DataView) return serializeTypedArray("V", value);
                if ("function" === typeof Blob && value instanceof Blob) return null === formData && (formData = new FormData()), key = nextPartId++, formData.append(formFieldPrefix + key, value), "$B" + key.toString(16);
                if (parentReference = getIteratorFn(value)) return parentReference = parentReference.call(value), parentReference === value ? (key = nextPartId++, parentReference = serializeModel(Array.from(parentReference), key), null === formData && (formData = new FormData()), formData.append(formFieldPrefix + key, parentReference), "$i" + key.toString(16)) : Array.from(parentReference);
                if ("function" === typeof ReadableStream && value instanceof ReadableStream) return serializeReadableStream(value);
                parentReference = value[ASYNC_ITERATOR];
                if ("function" === typeof parentReference) return serializeAsyncIterable(value, parentReference.call(value));
                parentReference = getPrototypeOf(value);
                if (parentReference !== ObjectPrototype && (null === parentReference || null !== getPrototypeOf(parentReference))) {
                    if (void 0 === temporaryReferences) throw Error("Only plain objects, and a few built-ins, can be passed to Server Functions. Classes or null prototypes are not supported." + describeObjectForErrorMessage(this, key));
                    return "$T";
                }
                value.$$typeof === REACT_CONTEXT_TYPE ? console.error("React Context Providers cannot be passed to Server Functions from the Client.%s", describeObjectForErrorMessage(this, key)) : "Object" !== objectName(value) ? console.error("Only plain objects can be passed to Server Functions from the Client. %s objects are not supported.%s", objectName(value), describeObjectForErrorMessage(this, key)) : isSimpleObject(value) ? Object.getOwnPropertySymbols && (parentReference = Object.getOwnPropertySymbols(value), 0 < parentReference.length && console.error("Only plain objects can be passed to Server Functions from the Client. Objects with symbol properties like %s are not supported.%s", parentReference[0].description, describeObjectForErrorMessage(this, key))) : console.error("Only plain objects can be passed to Server Functions from the Client. Classes or other objects with methods are not supported.%s", describeObjectForErrorMessage(this, key));
                return value;
            }
            if ("string" === typeof value) {
                if ("Z" === value[value.length - 1] && this[key] instanceof Date) return "$D" + value;
                key = "$" === value[0] ? "$" + value : value;
                return key;
            }
            if ("boolean" === typeof value) return value;
            if ("number" === typeof value) return serializeNumber(value);
            if ("undefined" === typeof value) return "$undefined";
            if ("function" === typeof value) {
                parentReference = knownServerReferences.get(value);
                if (void 0 !== parentReference) {
                    key = writtenObjects.get(value);
                    if (void 0 !== key) return key;
                    key = JSON.stringify({
                        id: parentReference.id,
                        bound: parentReference.bound
                    }, resolveToJSON);
                    null === formData && (formData = new FormData());
                    parentReference = nextPartId++;
                    formData.set(formFieldPrefix + parentReference, key);
                    key = "$h" + parentReference.toString(16);
                    writtenObjects.set(value, key);
                    return key;
                }
                if (void 0 !== temporaryReferences && -1 === key.indexOf(":") && (parentReference = writtenObjects.get(this), void 0 !== parentReference)) return temporaryReferences.set(parentReference + ":" + key, value), "$T";
                throw Error("Client Functions cannot be passed directly to Server Functions. Only Functions passed from the Server can be passed back again.");
            }
            if ("symbol" === typeof value) {
                if (void 0 !== temporaryReferences && -1 === key.indexOf(":") && (parentReference = writtenObjects.get(this), void 0 !== parentReference)) return temporaryReferences.set(parentReference + ":" + key, value), "$T";
                throw Error("Symbols cannot be passed to a Server Function without a temporary reference set. Pass a TemporaryReferenceSet to the options." + describeObjectForErrorMessage(this, key));
            }
            if ("bigint" === typeof value) return "$n" + value.toString(10);
            throw Error("Type " + typeof value + " is not supported as an argument to a Server Function.");
        }
        function serializeModel(model, id) {
            "object" === typeof model && null !== model && (id = "$" + id.toString(16), writtenObjects.set(model, id), void 0 !== temporaryReferences && temporaryReferences.set(id, model));
            modelRoot = model;
            return JSON.stringify(model, resolveToJSON);
        }
        var nextPartId = 1, pendingParts = 0, formData = null, writtenObjects = new WeakMap(), modelRoot = root;
        checkEvalAvailabilityOnceDev();
        var json = serializeModel(root, 0);
        null === formData ? resolve(json) : (formData.set(formFieldPrefix + "0", json), 0 === pendingParts && resolve(formData));
        return function() {
            0 < pendingParts && (pendingParts = 0, null === formData ? resolve(json) : resolve(formData));
        };
    }
    function encodeFormData(reference) {
        var resolve, reject, thenable = new Promise(function(res, rej) {
            resolve = res;
            reject = rej;
        });
        processReply(reference, "", void 0, function(body) {
            if ("string" === typeof body) {
                var data = new FormData();
                data.append("0", body);
                body = data;
            }
            thenable.status = "fulfilled";
            thenable.value = body;
            resolve(body);
        }, function(e) {
            thenable.status = "rejected";
            thenable.reason = e;
            reject(e);
        });
        return thenable;
    }
    function defaultEncodeFormAction(identifierPrefix) {
        var referenceClosure = knownServerReferences.get(this);
        if (!referenceClosure) throw Error("Tried to encode a Server Action from a different instance than the encoder is from. This is a bug in React.");
        var data = null;
        if (null !== referenceClosure.bound) {
            data = boundCache.get(referenceClosure);
            data || (data = encodeFormData({
                id: referenceClosure.id,
                bound: referenceClosure.bound
            }), boundCache.set(referenceClosure, data));
            if ("rejected" === data.status) throw data.reason;
            if ("fulfilled" !== data.status) throw data;
            referenceClosure = data.value;
            var prefixedData = new FormData();
            referenceClosure.forEach(function(value, key) {
                prefixedData.append("$ACTION_" + identifierPrefix + ":" + key, value);
            });
            data = prefixedData;
            referenceClosure = "$ACTION_REF_" + identifierPrefix;
        } else referenceClosure = "$ACTION_ID_" + referenceClosure.id;
        return {
            name: referenceClosure,
            method: "POST",
            encType: "multipart/form-data",
            data: data
        };
    }
    function isSignatureEqual(referenceId, numberOfBoundArgs) {
        var referenceClosure = knownServerReferences.get(this);
        if (!referenceClosure) throw Error("Tried to encode a Server Action from a different instance than the encoder is from. This is a bug in React.");
        if (referenceClosure.id !== referenceId) return !1;
        var boundPromise = referenceClosure.bound;
        if (null === boundPromise) return 0 === numberOfBoundArgs;
        switch(boundPromise.status){
            case "fulfilled":
                return boundPromise.value.length === numberOfBoundArgs;
            case "pending":
                throw boundPromise;
            case "rejected":
                throw boundPromise.reason;
            default:
                throw "string" !== typeof boundPromise.status && (boundPromise.status = "pending", boundPromise.then(function(boundArgs) {
                    boundPromise.status = "fulfilled";
                    boundPromise.value = boundArgs;
                }, function(error) {
                    boundPromise.status = "rejected";
                    boundPromise.reason = error;
                })), boundPromise;
        }
    }
    function createFakeServerFunction(name, filename, sourceMap, line, col, environmentName, innerFunction) {
        name || (name = "<anonymous>");
        var encodedName = JSON.stringify(name);
        1 >= line ? (line = encodedName.length + 7, col = "s=>({" + encodedName + " ".repeat(col < line ? 0 : col - line) + ":(...args) => s(...args)})\n/* This module is a proxy to a Server Action. Turn on Source Maps to see the server source. */") : col = "/* This module is a proxy to a Server Action. Turn on Source Maps to see the server source. */" + "\n".repeat(line - 2) + "server=>({" + encodedName + ":\n" + " ".repeat(1 > col ? 0 : col - 1) + "(...args) => server(...args)})";
        filename.startsWith("/") && (filename = "file://" + filename);
        sourceMap ? (col += "\n//# sourceURL=about://React/" + encodeURIComponent(environmentName) + "/" + encodeURI(filename) + "?s" + fakeServerFunctionIdx++, col += "\n//# sourceMappingURL=" + sourceMap) : filename && (col += "\n//# sourceURL=" + filename);
        try {
            return (0, eval)(col)(innerFunction)[name];
        } catch (x) {
            return innerFunction;
        }
    }
    function registerBoundServerReference(reference, id, bound, encodeFormAction) {
        knownServerReferences.has(reference) || (knownServerReferences.set(reference, {
            id: id,
            originalBind: reference.bind,
            bound: bound
        }), Object.defineProperties(reference, {
            $$FORM_ACTION: {
                value: void 0 === encodeFormAction ? defaultEncodeFormAction : function() {
                    var referenceClosure = knownServerReferences.get(this);
                    if (!referenceClosure) throw Error("Tried to encode a Server Action from a different instance than the encoder is from. This is a bug in React.");
                    var boundPromise = referenceClosure.bound;
                    null === boundPromise && (boundPromise = Promise.resolve([]));
                    return encodeFormAction(referenceClosure.id, boundPromise);
                }
            },
            $$IS_SIGNATURE_EQUAL: {
                value: isSignatureEqual
            },
            bind: {
                value: bind
            }
        }));
    }
    function bind() {
        var referenceClosure = knownServerReferences.get(this);
        if (!referenceClosure) return FunctionBind.apply(this, arguments);
        var newFn = referenceClosure.originalBind.apply(this, arguments);
        null != arguments[0] && console.error('Cannot bind "this" of a Server Action. Pass null or undefined as the first argument to .bind().');
        var args = ArraySlice.call(arguments, 1), boundPromise = null;
        boundPromise = null !== referenceClosure.bound ? Promise.resolve(referenceClosure.bound).then(function(boundArgs) {
            return boundArgs.concat(args);
        }) : Promise.resolve(args);
        knownServerReferences.set(newFn, {
            id: referenceClosure.id,
            originalBind: newFn.bind,
            bound: boundPromise
        });
        Object.defineProperties(newFn, {
            $$FORM_ACTION: {
                value: this.$$FORM_ACTION
            },
            $$IS_SIGNATURE_EQUAL: {
                value: isSignatureEqual
            },
            bind: {
                value: bind
            }
        });
        return newFn;
    }
    function createBoundServerReference(metaData, callServer, encodeFormAction, findSourceMapURL) {
        function action() {
            var args = Array.prototype.slice.call(arguments);
            return bound ? "fulfilled" === bound.status ? callServer(id, bound.value.concat(args)) : Promise.resolve(bound).then(function(boundArgs) {
                return callServer(id, boundArgs.concat(args));
            }) : callServer(id, args);
        }
        var id = metaData.id, bound = metaData.bound, location = metaData.location;
        if (location) {
            var functionName = metaData.name || "", filename = location[1], line = location[2];
            location = location[3];
            metaData = metaData.env || "Server";
            findSourceMapURL = null == findSourceMapURL ? null : findSourceMapURL(filename, metaData);
            action = createFakeServerFunction(functionName, filename, findSourceMapURL, line, location, metaData, action);
        }
        registerBoundServerReference(action, id, bound, encodeFormAction);
        return action;
    }
    function parseStackLocation(error) {
        error = error.stack;
        error.startsWith("Error: react-stack-top-frame\n") && (error = error.slice(29));
        var endOfFirst = error.indexOf("\n");
        if (-1 !== endOfFirst) {
            var endOfSecond = error.indexOf("\n", endOfFirst + 1);
            endOfFirst = -1 === endOfSecond ? error.slice(endOfFirst + 1) : error.slice(endOfFirst + 1, endOfSecond);
        } else endOfFirst = error;
        error = v8FrameRegExp.exec(endOfFirst);
        if (!error && (error = jscSpiderMonkeyFrameRegExp.exec(endOfFirst), !error)) return null;
        endOfFirst = error[1] || "";
        "<anonymous>" === endOfFirst && (endOfFirst = "");
        endOfSecond = error[2] || error[5] || "";
        "<anonymous>" === endOfSecond && (endOfSecond = "");
        return [
            endOfFirst,
            endOfSecond,
            +(error[3] || error[6]),
            +(error[4] || error[7])
        ];
    }
    function createServerReference$1(id, callServer, encodeFormAction, findSourceMapURL, functionName) {
        function action() {
            var args = Array.prototype.slice.call(arguments);
            return callServer(id, args);
        }
        var location = parseStackLocation(Error("react-stack-top-frame"));
        if (null !== location) {
            var filename = location[1], line = location[2];
            location = location[3];
            findSourceMapURL = null == findSourceMapURL ? null : findSourceMapURL(filename, "Client");
            action = createFakeServerFunction(functionName || "", filename, findSourceMapURL, line, location, "Client", action);
        }
        registerBoundServerReference(action, id, null, encodeFormAction);
        return action;
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
    function getArrayKind(array) {
        for(var kind = 0, i = 0; i < array.length && 100 > i; i++){
            var value = array[i];
            if ("object" === typeof value && null !== value) if (isArrayImpl(value) && 2 === value.length && "string" === typeof value[0]) {
                if (0 !== kind && 3 !== kind) return 1;
                kind = 3;
            } else return 1;
            else {
                if ("function" === typeof value || "string" === typeof value && 50 < value.length || 0 !== kind && 2 !== kind || "bigint" === typeof value) return 1;
                kind = 2;
            }
        }
        return kind;
    }
    function addObjectToProperties(object, properties, indent, prefix) {
        var addedProperties = 0, key;
        for(key in object)if (hasOwnProperty.call(object, key) && "_" !== key[0] && (addedProperties++, addValueToProperties(key, object[key], properties, indent, prefix), 100 <= addedProperties)) {
            properties.push([
                prefix + "\u00a0\u00a0".repeat(indent) + "Only 100 properties are shown. React will not log more properties of this object.",
                ""
            ]);
            break;
        }
    }
    function addValueToProperties(propertyName, value, properties, indent, prefix) {
        switch(typeof value){
            case "object":
                if (null === value) {
                    value = "null";
                    break;
                } else {
                    if (("$$typeof" in value && hasOwnProperty.call(value, "$$typeof") ? value.$$typeof : void 0) === REACT_ELEMENT_TYPE) {
                        var typeName = getComponentNameFromType(value.type) || "\u2026", key = value.key;
                        value = value.props;
                        var propsKeys = Object.keys(value), propsLength = propsKeys.length;
                        if (null == key && 0 === propsLength) {
                            value = "<" + typeName + " />";
                            break;
                        }
                        if (3 > indent || 1 === propsLength && "children" === propsKeys[0] && null == key) {
                            value = "<" + typeName + " \u2026 />";
                            break;
                        }
                        properties.push([
                            prefix + "\u00a0\u00a0".repeat(indent) + propertyName,
                            "<" + typeName
                        ]);
                        null !== key && addValueToProperties("key", key, properties, indent + 1, prefix);
                        propertyName = !1;
                        key = 0;
                        for(var propKey in value)if (key++, "children" === propKey ? null != value.children && (!isArrayImpl(value.children) || 0 < value.children.length) && (propertyName = !0) : hasOwnProperty.call(value, propKey) && "_" !== propKey[0] && addValueToProperties(propKey, value[propKey], properties, indent + 1, prefix), 100 <= key) break;
                        properties.push([
                            "",
                            propertyName ? ">\u2026</" + typeName + ">" : "/>"
                        ]);
                        return;
                    }
                    typeName = Object.prototype.toString.call(value);
                    propKey = typeName.slice(8, typeName.length - 1);
                    if ("Array" === propKey) {
                        if (typeName = 100 < value.length, key = getArrayKind(value), 2 === key || 0 === key) {
                            value = JSON.stringify(typeName ? value.slice(0, 100).concat("\u2026") : value);
                            break;
                        } else if (3 === key) {
                            properties.push([
                                prefix + "\u00a0\u00a0".repeat(indent) + propertyName,
                                ""
                            ]);
                            for(propertyName = 0; propertyName < value.length && 100 > propertyName; propertyName++)propKey = value[propertyName], addValueToProperties(propKey[0], propKey[1], properties, indent + 1, prefix);
                            typeName && addValueToProperties(100..toString(), "\u2026", properties, indent + 1, prefix);
                            return;
                        }
                    }
                    if ("Promise" === propKey) {
                        if ("fulfilled" === value.status) {
                            if (typeName = properties.length, addValueToProperties(propertyName, value.value, properties, indent, prefix), properties.length > typeName) {
                                properties = properties[typeName];
                                properties[1] = "Promise<" + (properties[1] || "Object") + ">";
                                return;
                            }
                        } else if ("rejected" === value.status && (typeName = properties.length, addValueToProperties(propertyName, value.reason, properties, indent, prefix), properties.length > typeName)) {
                            properties = properties[typeName];
                            properties[1] = "Rejected Promise<" + properties[1] + ">";
                            return;
                        }
                        properties.push([
                            "\u00a0\u00a0".repeat(indent) + propertyName,
                            "Promise"
                        ]);
                        return;
                    }
                    "Object" === propKey && (typeName = Object.getPrototypeOf(value)) && "function" === typeof typeName.constructor && (propKey = typeName.constructor.name);
                    properties.push([
                        prefix + "\u00a0\u00a0".repeat(indent) + propertyName,
                        "Object" === propKey ? 3 > indent ? "" : "\u2026" : propKey
                    ]);
                    3 > indent && addObjectToProperties(value, properties, indent + 1, prefix);
                    return;
                }
            case "function":
                value = value.name;
                value = "" === value || "string" !== typeof value ? "() => {}" : value + "() {}";
                break;
            case "string":
                value = "This object has been omitted by React in the console log to avoid sending too much data from the server. Try logging smaller or more specific objects." === value ? "\u2026" : JSON.stringify(value);
                break;
            case "undefined":
                value = "undefined";
                break;
            case "boolean":
                value = value ? "true" : "false";
                break;
            default:
                value = String(value);
        }
        properties.push([
            prefix + "\u00a0\u00a0".repeat(indent) + propertyName,
            value
        ]);
    }
    function getIODescription(value) {
        try {
            switch(typeof value){
                case "function":
                    return value.name || "";
                case "object":
                    if (null === value) return "";
                    if (value instanceof Error) return String(value.message);
                    if ("string" === typeof value.url) return value.url;
                    if ("string" === typeof value.href) return value.href;
                    if ("string" === typeof value.src) return value.src;
                    if ("string" === typeof value.currentSrc) return value.currentSrc;
                    if ("string" === typeof value.command) return value.command;
                    if ("object" === typeof value.request && null !== value.request && "string" === typeof value.request.url) return value.request.url;
                    if ("object" === typeof value.response && null !== value.response && "string" === typeof value.response.url) return value.response.url;
                    if ("string" === typeof value.id || "number" === typeof value.id || "bigint" === typeof value.id) return String(value.id);
                    if ("string" === typeof value.name) return value.name;
                    var str = value.toString();
                    return str.startsWith("[object ") || 5 > str.length || 500 < str.length ? "" : str;
                case "string":
                    return 5 > value.length || 500 < value.length ? "" : value;
                case "number":
                case "bigint":
                    return String(value);
                default:
                    return "";
            }
        } catch (x) {
            return "";
        }
    }
    function markAllTracksInOrder() {
        supportsUserTiming && (console.timeStamp("Server Requests Track", 0.001, 0.001, "Server Requests \u269b", void 0, "primary-light"), console.timeStamp("Server Components Track", 0.001, 0.001, "Primary", "Server Components \u269b", "primary-light"));
    }
    function getIOColor(functionName) {
        switch(functionName.charCodeAt(0) % 3){
            case 0:
                return "tertiary-light";
            case 1:
                return "tertiary";
            default:
                return "tertiary-dark";
        }
    }
    function getIOLongName(ioInfo, description, env, rootEnv) {
        ioInfo = ioInfo.name;
        description = "" === description ? ioInfo : ioInfo + " (" + description + ")";
        return env === rootEnv || void 0 === env ? description : description + " [" + env + "]";
    }
    function getIOShortName(ioInfo, description, env, rootEnv) {
        ioInfo = ioInfo.name;
        env = env === rootEnv || void 0 === env ? "" : " [" + env + "]";
        var desc = "";
        rootEnv = 30 - ioInfo.length - env.length;
        if (1 < rootEnv) {
            var l = description.length;
            if (0 < l && l <= rootEnv) desc = " (" + description + ")";
            else if (description.startsWith("http://") || description.startsWith("https://") || description.startsWith("/")) {
                var queryIdx = description.indexOf("?");
                -1 === queryIdx && (queryIdx = description.length);
                47 === description.charCodeAt(queryIdx - 1) && queryIdx--;
                desc = description.lastIndexOf("/", queryIdx - 1);
                queryIdx - desc < rootEnv ? desc = " (\u2026" + description.slice(desc, queryIdx) + ")" : (l = description.slice(desc, desc + rootEnv / 2), description = description.slice(queryIdx - rootEnv / 2, queryIdx), desc = " (" + (0 < desc ? "\u2026" : "") + l + "\u2026" + description + ")");
            }
        }
        return ioInfo + desc + env;
    }
    function logComponentAwait(asyncInfo, trackIdx, startTime, endTime, rootEnv, value) {
        if (supportsUserTiming && 0 < endTime) {
            var description = getIODescription(value), name = getIOShortName(asyncInfo.awaited, description, asyncInfo.env, rootEnv), entryName = "await " + name;
            name = getIOColor(name);
            var debugTask = asyncInfo.debugTask || asyncInfo.awaited.debugTask;
            if (debugTask) {
                var properties = [];
                "object" === typeof value && null !== value ? addObjectToProperties(value, properties, 0, "") : void 0 !== value && addValueToProperties("awaited value", value, properties, 0, "");
                asyncInfo = getIOLongName(asyncInfo.awaited, description, asyncInfo.env, rootEnv);
                debugTask.run(performance.measure.bind(performance, entryName, {
                    start: 0 > startTime ? 0 : startTime,
                    end: endTime,
                    detail: {
                        devtools: {
                            color: name,
                            track: trackNames[trackIdx],
                            trackGroup: "Server Components \u269b",
                            properties: properties,
                            tooltipText: asyncInfo
                        }
                    }
                }));
                performance.clearMeasures(entryName);
            } else console.timeStamp(entryName, 0 > startTime ? 0 : startTime, endTime, trackNames[trackIdx], "Server Components \u269b", name);
        }
    }
    function logIOInfoErrored(ioInfo, rootEnv, error) {
        var startTime = ioInfo.start, endTime = ioInfo.end;
        if (supportsUserTiming && 0 <= endTime) {
            var description = getIODescription(error), entryName = getIOShortName(ioInfo, description, ioInfo.env, rootEnv), debugTask = ioInfo.debugTask;
            entryName = "\u200b" + entryName;
            debugTask ? (error = [
                [
                    "rejected with",
                    "object" === typeof error && null !== error && "string" === typeof error.message ? String(error.message) : String(error)
                ]
            ], ioInfo = getIOLongName(ioInfo, description, ioInfo.env, rootEnv) + " Rejected", debugTask.run(performance.measure.bind(performance, entryName, {
                start: 0 > startTime ? 0 : startTime,
                end: endTime,
                detail: {
                    devtools: {
                        color: "error",
                        track: "Server Requests \u269b",
                        properties: error,
                        tooltipText: ioInfo
                    }
                }
            })), performance.clearMeasures(entryName)) : console.timeStamp(entryName, 0 > startTime ? 0 : startTime, endTime, "Server Requests \u269b", void 0, "error");
        }
    }
    function logIOInfo(ioInfo, rootEnv, value) {
        var startTime = ioInfo.start, endTime = ioInfo.end;
        if (supportsUserTiming && 0 <= endTime) {
            var description = getIODescription(value), entryName = getIOShortName(ioInfo, description, ioInfo.env, rootEnv), color = getIOColor(entryName), debugTask = ioInfo.debugTask;
            entryName = "\u200b" + entryName;
            if (debugTask) {
                var properties = [];
                "object" === typeof value && null !== value ? addObjectToProperties(value, properties, 0, "") : void 0 !== value && addValueToProperties("Resolved", value, properties, 0, "");
                ioInfo = getIOLongName(ioInfo, description, ioInfo.env, rootEnv);
                debugTask.run(performance.measure.bind(performance, entryName, {
                    start: 0 > startTime ? 0 : startTime,
                    end: endTime,
                    detail: {
                        devtools: {
                            color: color,
                            track: "Server Requests \u269b",
                            properties: properties,
                            tooltipText: ioInfo
                        }
                    }
                }));
                performance.clearMeasures(entryName);
            } else console.timeStamp(entryName, 0 > startTime ? 0 : startTime, endTime, "Server Requests \u269b", void 0, color);
        }
    }
    function prepareStackTrace(error, structuredStackTrace) {
        error = (error.name || "Error") + ": " + (error.message || "");
        for(var i = 0; i < structuredStackTrace.length; i++)error += "\n    at " + structuredStackTrace[i].toString();
        return error;
    }
    function ReactPromise(status, value, reason) {
        this.status = status;
        this.value = value;
        this.reason = reason;
        this._children = [];
        this._debugChunk = null;
        this._debugInfo = [];
    }
    function hasGCedResponse(weakResponse) {
        return void 0 === weakResponse.weak.deref();
    }
    function unwrapWeakResponse(weakResponse) {
        weakResponse = weakResponse.weak.deref();
        if (void 0 === weakResponse) throw Error("We did not expect to receive new data after GC:ing the response.");
        return weakResponse;
    }
    function closeDebugChannel(debugChannel) {
        debugChannel.callback && debugChannel.callback("");
    }
    function readChunk(chunk) {
        switch(chunk.status){
            case "resolved_model":
                initializeModelChunk(chunk);
                break;
            case "resolved_module":
                initializeModuleChunk(chunk);
        }
        switch(chunk.status){
            case "fulfilled":
                return chunk.value;
            case "pending":
            case "blocked":
            case "halted":
                throw chunk;
            default:
                throw chunk.reason;
        }
    }
    function getRoot(weakResponse) {
        weakResponse = unwrapWeakResponse(weakResponse);
        return getChunk(weakResponse, 0);
    }
    function createPendingChunk(response) {
        0 === response._pendingChunks++ && (response._weakResponse.response = response, null !== response._pendingInitialRender && (clearTimeout(response._pendingInitialRender), response._pendingInitialRender = null));
        return new ReactPromise("pending", null, null);
    }
    function releasePendingChunk(response, chunk) {
        "pending" === chunk.status && 0 === --response._pendingChunks && (response._weakResponse.response = null, response._pendingInitialRender = setTimeout(flushInitialRenderPerformance.bind(null, response), 100));
    }
    function filterDebugInfo(response, value) {
        if (null !== response._debugEndTime) {
            response = response._debugEndTime - performance.timeOrigin;
            for(var debugInfo = [], i = 0; i < value._debugInfo.length; i++){
                var info = value._debugInfo[i];
                if ("number" === typeof info.time && info.time > response) break;
                debugInfo.push(info);
            }
            value._debugInfo = debugInfo;
        }
    }
    function moveDebugInfoFromChunkToInnerValue(chunk, value) {
        value = resolveLazy(value);
        "object" !== typeof value || null === value || !isArrayImpl(value) && "function" !== typeof value[ASYNC_ITERATOR] && value.$$typeof !== REACT_ELEMENT_TYPE && value.$$typeof !== REACT_LAZY_TYPE || (chunk = chunk._debugInfo.splice(0), isArrayImpl(value._debugInfo) ? value._debugInfo.unshift.apply(value._debugInfo, chunk) : Object.isFrozen(value) || Object.defineProperty(value, "_debugInfo", {
            configurable: !1,
            enumerable: !1,
            writable: !0,
            value: chunk
        }));
    }
    function wakeChunk(response, listeners, value, chunk) {
        for(var i = 0; i < listeners.length; i++){
            var listener = listeners[i];
            "function" === typeof listener ? listener(value) : fulfillReference(response, listener, value, chunk);
        }
        filterDebugInfo(response, chunk);
        moveDebugInfoFromChunkToInnerValue(chunk, value);
    }
    function rejectChunk(response, listeners, error) {
        for(var i = 0; i < listeners.length; i++){
            var listener = listeners[i];
            "function" === typeof listener ? listener(error) : rejectReference(response, listener.handler, error);
        }
    }
    function resolveBlockedCycle(resolvedChunk, reference) {
        var referencedChunk = reference.handler.chunk;
        if (null === referencedChunk) return null;
        if (referencedChunk === resolvedChunk) return reference.handler;
        reference = referencedChunk.value;
        if (null !== reference) for(referencedChunk = 0; referencedChunk < reference.length; referencedChunk++){
            var listener = reference[referencedChunk];
            if ("function" !== typeof listener && (listener = resolveBlockedCycle(resolvedChunk, listener), null !== listener)) return listener;
        }
        return null;
    }
    function wakeChunkIfInitialized(response, chunk, resolveListeners, rejectListeners) {
        switch(chunk.status){
            case "fulfilled":
                wakeChunk(response, resolveListeners, chunk.value, chunk);
                break;
            case "blocked":
                for(var i = 0; i < resolveListeners.length; i++){
                    var listener = resolveListeners[i];
                    if ("function" !== typeof listener) {
                        var cyclicHandler = resolveBlockedCycle(chunk, listener);
                        if (null !== cyclicHandler) switch(fulfillReference(response, listener, cyclicHandler.value, chunk), resolveListeners.splice(i, 1), i--, null !== rejectListeners && (listener = rejectListeners.indexOf(listener), -1 !== listener && rejectListeners.splice(listener, 1)), chunk.status){
                            case "fulfilled":
                                wakeChunk(response, resolveListeners, chunk.value, chunk);
                                return;
                            case "rejected":
                                null !== rejectListeners && rejectChunk(response, rejectListeners, chunk.reason);
                                return;
                        }
                    }
                }
            case "pending":
                if (chunk.value) for(response = 0; response < resolveListeners.length; response++)chunk.value.push(resolveListeners[response]);
                else chunk.value = resolveListeners;
                if (chunk.reason) {
                    if (rejectListeners) for(resolveListeners = 0; resolveListeners < rejectListeners.length; resolveListeners++)chunk.reason.push(rejectListeners[resolveListeners]);
                } else chunk.reason = rejectListeners;
                break;
            case "rejected":
                rejectListeners && rejectChunk(response, rejectListeners, chunk.reason);
        }
    }
    function triggerErrorOnChunk(response, chunk, error) {
        if ("pending" !== chunk.status && "blocked" !== chunk.status) chunk.reason.error(error);
        else {
            releasePendingChunk(response, chunk);
            var listeners = chunk.reason;
            if ("pending" === chunk.status && null != chunk._debugChunk) {
                var prevHandler = initializingHandler, prevChunk = initializingChunk;
                initializingHandler = null;
                chunk.status = "blocked";
                chunk.value = null;
                chunk.reason = null;
                initializingChunk = chunk;
                try {
                    initializeDebugChunk(response, chunk);
                } finally{
                    initializingHandler = prevHandler, initializingChunk = prevChunk;
                }
            }
            chunk.status = "rejected";
            chunk.reason = error;
            null !== listeners && rejectChunk(response, listeners, error);
        }
    }
    function createResolvedModelChunk(response, value) {
        return new ReactPromise("resolved_model", value, response);
    }
    function createResolvedIteratorResultChunk(response, value, done) {
        return new ReactPromise("resolved_model", (done ? '{"done":true,"value":' : '{"done":false,"value":') + value + "}", response);
    }
    function resolveIteratorResultChunk(response, chunk, value, done) {
        resolveModelChunk(response, chunk, (done ? '{"done":true,"value":' : '{"done":false,"value":') + value + "}");
    }
    function resolveModelChunk(response, chunk, value) {
        if ("pending" !== chunk.status) chunk.reason.enqueueModel(value);
        else {
            releasePendingChunk(response, chunk);
            var resolveListeners = chunk.value, rejectListeners = chunk.reason;
            chunk.status = "resolved_model";
            chunk.value = value;
            chunk.reason = response;
            null !== resolveListeners && (initializeModelChunk(chunk), wakeChunkIfInitialized(response, chunk, resolveListeners, rejectListeners));
        }
    }
    function resolveModuleChunk(response, chunk, value) {
        if ("pending" === chunk.status || "blocked" === chunk.status) {
            releasePendingChunk(response, chunk);
            var resolveListeners = chunk.value, rejectListeners = chunk.reason;
            chunk.status = "resolved_module";
            chunk.value = value;
            chunk.reason = null;
            value = [];
            null !== value && chunk._debugInfo.push.apply(chunk._debugInfo, value);
            null !== resolveListeners && (initializeModuleChunk(chunk), wakeChunkIfInitialized(response, chunk, resolveListeners, rejectListeners));
        }
    }
    function initializeDebugChunk(response, chunk) {
        var debugChunk = chunk._debugChunk;
        if (null !== debugChunk) {
            var debugInfo = chunk._debugInfo, prevIsInitializingDebugInfo = isInitializingDebugInfo;
            isInitializingDebugInfo = !0;
            try {
                if ("resolved_model" === debugChunk.status) {
                    for(var idx = debugInfo.length, c = debugChunk._debugChunk; null !== c;)"fulfilled" !== c.status && idx++, c = c._debugChunk;
                    initializeModelChunk(debugChunk);
                    switch(debugChunk.status){
                        case "fulfilled":
                            debugInfo[idx] = initializeDebugInfo(response, debugChunk.value);
                            break;
                        case "blocked":
                        case "pending":
                            waitForReference(debugChunk, debugInfo, "" + idx, response, initializeDebugInfo, [
                                ""
                            ], !0);
                            break;
                        default:
                            throw debugChunk.reason;
                    }
                } else switch(debugChunk.status){
                    case "fulfilled":
                        break;
                    case "blocked":
                    case "pending":
                        waitForReference(debugChunk, {}, "debug", response, initializeDebugInfo, [
                            ""
                        ], !0);
                        break;
                    default:
                        throw debugChunk.reason;
                }
            } catch (error) {
                triggerErrorOnChunk(response, chunk, error);
            } finally{
                isInitializingDebugInfo = prevIsInitializingDebugInfo;
            }
        }
    }
    function initializeModelChunk(chunk) {
        var prevHandler = initializingHandler, prevChunk = initializingChunk;
        initializingHandler = null;
        var resolvedModel = chunk.value, response = chunk.reason;
        chunk.status = "blocked";
        chunk.value = null;
        chunk.reason = null;
        initializingChunk = chunk;
        initializeDebugChunk(response, chunk);
        try {
            var value = parseModel(response, resolvedModel), resolveListeners = chunk.value;
            if (null !== resolveListeners) for(chunk.value = null, chunk.reason = null, resolvedModel = 0; resolvedModel < resolveListeners.length; resolvedModel++){
                var listener = resolveListeners[resolvedModel];
                "function" === typeof listener ? listener(value) : fulfillReference(response, listener, value, chunk);
            }
            if (null !== initializingHandler) {
                if (initializingHandler.errored) throw initializingHandler.reason;
                if (0 < initializingHandler.deps) {
                    initializingHandler.value = value;
                    initializingHandler.chunk = chunk;
                    return;
                }
            }
            chunk.status = "fulfilled";
            chunk.value = value;
            chunk.reason = null;
            filterDebugInfo(response, chunk);
            moveDebugInfoFromChunkToInnerValue(chunk, value);
        } catch (error) {
            chunk.status = "rejected", chunk.reason = error;
        } finally{
            initializingHandler = prevHandler, initializingChunk = prevChunk;
        }
    }
    function initializeModuleChunk(chunk) {
        try {
            var value = requireModule(chunk.value);
            chunk.status = "fulfilled";
            chunk.value = value;
            chunk.reason = null;
        } catch (error) {
            chunk.status = "rejected", chunk.reason = error;
        }
    }
    function reportGlobalError(weakResponse, error) {
        if (!hasGCedResponse(weakResponse)) {
            var response = unwrapWeakResponse(weakResponse);
            response._closed = !0;
            response._closedReason = error;
            response._chunks.forEach(function(chunk) {
                "pending" === chunk.status ? triggerErrorOnChunk(response, chunk, error) : "fulfilled" === chunk.status && null !== chunk.reason && chunk.reason.error(error);
            });
            weakResponse = response._debugChannel;
            void 0 !== weakResponse && (closeDebugChannel(weakResponse), response._debugChannel = void 0, null !== debugChannelRegistry && debugChannelRegistry.unregister(response));
        }
    }
    function nullRefGetter() {
        return null;
    }
    function getTaskName(type) {
        if (type === REACT_FRAGMENT_TYPE) return "<>";
        if ("function" === typeof type) return '"use client"';
        if ("object" === typeof type && null !== type && type.$$typeof === REACT_LAZY_TYPE) return type._init === readChunk ? '"use client"' : "<...>";
        try {
            var name = getComponentNameFromType(type);
            return name ? "<" + name + ">" : "<...>";
        } catch (x) {
            return "<...>";
        }
    }
    function initializeElement(response, element, lazyNode) {
        var stack = element._debugStack, owner = element._owner;
        null === owner && (element._owner = response._debugRootOwner);
        var env = response._rootEnvironmentName;
        null !== owner && null != owner.env && (env = owner.env);
        var normalizedStackTrace = null;
        null === owner && null != response._debugRootStack ? normalizedStackTrace = response._debugRootStack : null !== stack && (normalizedStackTrace = createFakeJSXCallStackInDEV(response, stack, env));
        element._debugStack = normalizedStackTrace;
        normalizedStackTrace = null;
        supportsCreateTask && null !== stack && (normalizedStackTrace = console.createTask.bind(console, getTaskName(element.type)), stack = buildFakeCallStack(response, stack, env, !1, normalizedStackTrace), env = null === owner ? null : initializeFakeTask(response, owner), null === env ? (env = response._debugRootTask, normalizedStackTrace = null != env ? env.run(stack) : stack()) : normalizedStackTrace = env.run(stack));
        element._debugTask = normalizedStackTrace;
        null !== owner && initializeFakeStack(response, owner);
        null !== lazyNode && (lazyNode._store && lazyNode._store.validated && !element._store.validated && (element._store.validated = lazyNode._store.validated), "fulfilled" === lazyNode._payload.status && lazyNode._debugInfo && (response = lazyNode._debugInfo.splice(0), element._debugInfo ? element._debugInfo.unshift.apply(element._debugInfo, response) : Object.defineProperty(element, "_debugInfo", {
            configurable: !1,
            enumerable: !1,
            writable: !0,
            value: response
        })));
        Object.freeze(element.props);
    }
    function createLazyChunkWrapper(chunk, validated) {
        var lazyType = {
            $$typeof: REACT_LAZY_TYPE,
            _payload: chunk,
            _init: readChunk
        };
        lazyType._debugInfo = chunk._debugInfo;
        lazyType._store = {
            validated: validated
        };
        return lazyType;
    }
    function getChunk(response, id) {
        var chunks = response._chunks, chunk = chunks.get(id);
        chunk || (response._closed ? response._allowPartialStream ? (response = chunk = createPendingChunk(response), response.status = "halted", response.value = null, response.reason = null) : chunk = new ReactPromise("rejected", null, response._closedReason) : chunk = createPendingChunk(response), chunks.set(id, chunk));
        return chunk;
    }
    function fulfillReference(response, reference, value, fulfilledChunk) {
        var handler = reference.handler, parentObject = reference.parentObject, key = reference.key, map = reference.map, path = reference.path;
        try {
            for(var i = 1; i < path.length; i++){
                for(; "object" === typeof value && null !== value && value.$$typeof === REACT_LAZY_TYPE;){
                    var referencedChunk = value._payload;
                    if (referencedChunk === handler.chunk) value = handler.value;
                    else {
                        switch(referencedChunk.status){
                            case "resolved_model":
                                initializeModelChunk(referencedChunk);
                                break;
                            case "resolved_module":
                                initializeModuleChunk(referencedChunk);
                        }
                        switch(referencedChunk.status){
                            case "fulfilled":
                                value = referencedChunk.value;
                                continue;
                            case "blocked":
                                var cyclicHandler = resolveBlockedCycle(referencedChunk, reference);
                                if (null !== cyclicHandler) {
                                    value = cyclicHandler.value;
                                    continue;
                                }
                            case "pending":
                                path.splice(0, i - 1);
                                null === referencedChunk.value ? referencedChunk.value = [
                                    reference
                                ] : referencedChunk.value.push(reference);
                                null === referencedChunk.reason ? referencedChunk.reason = [
                                    reference
                                ] : referencedChunk.reason.push(reference);
                                return;
                            case "halted":
                                return;
                            default:
                                rejectReference(response, reference.handler, referencedChunk.reason);
                                return;
                        }
                    }
                }
                var name = path[i];
                if ("object" === typeof value && null !== value && hasOwnProperty.call(value, name)) value = value[name];
                else throw Error("Invalid reference.");
            }
            for(; "object" === typeof value && null !== value && value.$$typeof === REACT_LAZY_TYPE;){
                var _referencedChunk = value._payload;
                if (_referencedChunk === handler.chunk) value = handler.value;
                else {
                    switch(_referencedChunk.status){
                        case "resolved_model":
                            initializeModelChunk(_referencedChunk);
                            break;
                        case "resolved_module":
                            initializeModuleChunk(_referencedChunk);
                    }
                    switch(_referencedChunk.status){
                        case "fulfilled":
                            value = _referencedChunk.value;
                            continue;
                    }
                    break;
                }
            }
            var mappedValue = map(response, value, parentObject, key);
            "__proto__" !== key && (parentObject[key] = mappedValue);
            "" === key && null === handler.value && (handler.value = mappedValue);
            if (parentObject[0] === REACT_ELEMENT_TYPE && "object" === typeof handler.value && null !== handler.value && handler.value.$$typeof === REACT_ELEMENT_TYPE) {
                var element = handler.value;
                switch(key){
                    case "3":
                        transferReferencedDebugInfo(handler.chunk, fulfilledChunk);
                        element.props = mappedValue;
                        break;
                    case "4":
                        element._owner = mappedValue;
                        break;
                    case "5":
                        element._debugStack = mappedValue;
                        break;
                    default:
                        transferReferencedDebugInfo(handler.chunk, fulfilledChunk);
                }
            } else reference.isDebug || transferReferencedDebugInfo(handler.chunk, fulfilledChunk);
        } catch (error) {
            rejectReference(response, reference.handler, error);
            return;
        }
        handler.deps--;
        0 === handler.deps && (reference = handler.chunk, null !== reference && "blocked" === reference.status && (value = reference.value, reference.status = "fulfilled", reference.value = handler.value, reference.reason = handler.reason, null !== value ? wakeChunk(response, value, handler.value, reference) : (handler = handler.value, filterDebugInfo(response, reference), moveDebugInfoFromChunkToInnerValue(reference, handler))));
    }
    function rejectReference(response, handler, error) {
        if (!handler.errored) {
            var blockedValue = handler.value;
            handler.errored = !0;
            handler.value = null;
            handler.reason = error;
            handler = handler.chunk;
            if (null !== handler && "blocked" === handler.status) {
                if ("object" === typeof blockedValue && null !== blockedValue && blockedValue.$$typeof === REACT_ELEMENT_TYPE) {
                    var erroredComponent = {
                        name: getComponentNameFromType(blockedValue.type) || "",
                        owner: blockedValue._owner
                    };
                    erroredComponent.debugStack = blockedValue._debugStack;
                    supportsCreateTask && (erroredComponent.debugTask = blockedValue._debugTask);
                    handler._debugInfo.push(erroredComponent);
                }
                triggerErrorOnChunk(response, handler, error);
            }
        }
    }
    function waitForReference(referencedChunk, parentObject, key, response, map, path, isAwaitingDebugInfo) {
        if (!(void 0 !== response._debugChannel && response._debugChannel.hasReadable || "pending" !== referencedChunk.status || parentObject[0] !== REACT_ELEMENT_TYPE || "4" !== key && "5" !== key)) return null;
        initializingHandler ? (response = initializingHandler, response.deps++) : response = initializingHandler = {
            parent: null,
            chunk: null,
            value: null,
            reason: null,
            deps: 1,
            errored: !1
        };
        parentObject = {
            handler: response,
            parentObject: parentObject,
            key: key,
            map: map,
            path: path
        };
        parentObject.isDebug = isAwaitingDebugInfo;
        null === referencedChunk.value ? referencedChunk.value = [
            parentObject
        ] : referencedChunk.value.push(parentObject);
        null === referencedChunk.reason ? referencedChunk.reason = [
            parentObject
        ] : referencedChunk.reason.push(parentObject);
        return null;
    }
    function loadServerReference(response, metaData, parentObject, key) {
        if (!response._serverReferenceConfig) return createBoundServerReference(metaData, response._callServer, response._encodeFormAction, response._debugFindSourceMapURL);
        var serverReference = resolveServerReference(response._serverReferenceConfig, metaData.id), promise = preloadModule(serverReference);
        if (promise) metaData.bound && (promise = Promise.all([
            promise,
            metaData.bound
        ]));
        else if (metaData.bound) promise = Promise.resolve(metaData.bound);
        else return promise = requireModule(serverReference), registerBoundServerReference(promise, metaData.id, metaData.bound, response._encodeFormAction), promise;
        if (initializingHandler) {
            var handler = initializingHandler;
            handler.deps++;
        } else handler = initializingHandler = {
            parent: null,
            chunk: null,
            value: null,
            reason: null,
            deps: 1,
            errored: !1
        };
        promise.then(function() {
            var resolvedValue = requireModule(serverReference);
            if (metaData.bound) {
                var boundArgs = metaData.bound.value.slice(0);
                boundArgs.unshift(null);
                resolvedValue = resolvedValue.bind.apply(resolvedValue, boundArgs);
            }
            registerBoundServerReference(resolvedValue, metaData.id, metaData.bound, response._encodeFormAction);
            "__proto__" !== key && (parentObject[key] = resolvedValue);
            "" === key && null === handler.value && (handler.value = resolvedValue);
            if (parentObject[0] === REACT_ELEMENT_TYPE && "object" === typeof handler.value && null !== handler.value && handler.value.$$typeof === REACT_ELEMENT_TYPE) switch(boundArgs = handler.value, key){
                case "3":
                    boundArgs.props = resolvedValue;
                    break;
                case "4":
                    boundArgs._owner = resolvedValue;
            }
            handler.deps--;
            0 === handler.deps && (resolvedValue = handler.chunk, null !== resolvedValue && "blocked" === resolvedValue.status && (boundArgs = resolvedValue.value, resolvedValue.status = "fulfilled", resolvedValue.value = handler.value, resolvedValue.reason = null, null !== boundArgs ? wakeChunk(response, boundArgs, handler.value, resolvedValue) : (boundArgs = handler.value, filterDebugInfo(response, resolvedValue), moveDebugInfoFromChunkToInnerValue(resolvedValue, boundArgs))));
        }, function(error) {
            if (!handler.errored) {
                var blockedValue = handler.value;
                handler.errored = !0;
                handler.value = null;
                handler.reason = error;
                var chunk = handler.chunk;
                if (null !== chunk && "blocked" === chunk.status) {
                    if ("object" === typeof blockedValue && null !== blockedValue && blockedValue.$$typeof === REACT_ELEMENT_TYPE) {
                        var erroredComponent = {
                            name: getComponentNameFromType(blockedValue.type) || "",
                            owner: blockedValue._owner
                        };
                        erroredComponent.debugStack = blockedValue._debugStack;
                        supportsCreateTask && (erroredComponent.debugTask = blockedValue._debugTask);
                        chunk._debugInfo.push(erroredComponent);
                    }
                    triggerErrorOnChunk(response, chunk, error);
                }
            }
        });
        return null;
    }
    function resolveLazy(value) {
        for(; "object" === typeof value && null !== value && value.$$typeof === REACT_LAZY_TYPE;){
            var payload = value._payload;
            if ("fulfilled" === payload.status) value = payload.value;
            else break;
        }
        return value;
    }
    function transferReferencedDebugInfo(parentChunk, referencedChunk) {
        if (null !== parentChunk) {
            referencedChunk = referencedChunk._debugInfo;
            parentChunk = parentChunk._debugInfo;
            for(var i = 0; i < referencedChunk.length; ++i){
                var debugInfoEntry = referencedChunk[i];
                null == debugInfoEntry.name && parentChunk.push(debugInfoEntry);
            }
        }
    }
    function getOutlinedModel(response, reference, parentObject, key, map) {
        var path = reference.split(":");
        reference = parseInt(path[0], 16);
        reference = getChunk(response, reference);
        null !== initializingChunk && isArrayImpl(initializingChunk._children) && initializingChunk._children.push(reference);
        switch(reference.status){
            case "resolved_model":
                initializeModelChunk(reference);
                break;
            case "resolved_module":
                initializeModuleChunk(reference);
        }
        switch(reference.status){
            case "fulfilled":
                for(var value = reference.value, i = 1; i < path.length; i++){
                    for(; "object" === typeof value && null !== value && value.$$typeof === REACT_LAZY_TYPE;){
                        value = value._payload;
                        switch(value.status){
                            case "resolved_model":
                                initializeModelChunk(value);
                                break;
                            case "resolved_module":
                                initializeModuleChunk(value);
                        }
                        switch(value.status){
                            case "fulfilled":
                                value = value.value;
                                break;
                            case "blocked":
                            case "pending":
                                return waitForReference(value, parentObject, key, response, map, path.slice(i - 1), isInitializingDebugInfo);
                            case "halted":
                                return initializingHandler ? (parentObject = initializingHandler, parentObject.deps++) : initializingHandler = {
                                    parent: null,
                                    chunk: null,
                                    value: null,
                                    reason: null,
                                    deps: 1,
                                    errored: !1
                                }, null;
                            default:
                                return initializingHandler ? (initializingHandler.errored = !0, initializingHandler.value = null, initializingHandler.reason = value.reason) : initializingHandler = {
                                    parent: null,
                                    chunk: null,
                                    value: null,
                                    reason: value.reason,
                                    deps: 0,
                                    errored: !0
                                }, null;
                        }
                    }
                    value = value[path[i]];
                }
                for(; "object" === typeof value && null !== value && value.$$typeof === REACT_LAZY_TYPE;){
                    path = value._payload;
                    switch(path.status){
                        case "resolved_model":
                            initializeModelChunk(path);
                            break;
                        case "resolved_module":
                            initializeModuleChunk(path);
                    }
                    switch(path.status){
                        case "fulfilled":
                            value = path.value;
                            continue;
                    }
                    break;
                }
                response = map(response, value, parentObject, key);
                if (parentObject[0] !== REACT_ELEMENT_TYPE || "4" !== key && "5" !== key) isInitializingDebugInfo || transferReferencedDebugInfo(initializingChunk, reference);
                return response;
            case "pending":
            case "blocked":
                return waitForReference(reference, parentObject, key, response, map, path, isInitializingDebugInfo);
            case "halted":
                return initializingHandler ? (parentObject = initializingHandler, parentObject.deps++) : initializingHandler = {
                    parent: null,
                    chunk: null,
                    value: null,
                    reason: null,
                    deps: 1,
                    errored: !1
                }, null;
            default:
                return initializingHandler ? (initializingHandler.errored = !0, initializingHandler.value = null, initializingHandler.reason = reference.reason) : initializingHandler = {
                    parent: null,
                    chunk: null,
                    value: null,
                    reason: reference.reason,
                    deps: 0,
                    errored: !0
                }, null;
        }
    }
    function createMap(response, model) {
        return new Map(model);
    }
    function createSet(response, model) {
        return new Set(model);
    }
    function createBlob(response, model) {
        return new Blob(model.slice(1), {
            type: model[0]
        });
    }
    function createFormData(response, model) {
        response = new FormData();
        for(var i = 0; i < model.length; i++)response.append(model[i][0], model[i][1]);
        return response;
    }
    function applyConstructor(response, model, parentObject) {
        Object.setPrototypeOf(parentObject, model.prototype);
    }
    function defineLazyGetter(response, chunk, parentObject, key) {
        "__proto__" !== key && Object.defineProperty(parentObject, key, {
            get: function() {
                "resolved_model" === chunk.status && initializeModelChunk(chunk);
                switch(chunk.status){
                    case "fulfilled":
                        return chunk.value;
                    case "rejected":
                        throw chunk.reason;
                }
                return "This object has been omitted by React in the console log to avoid sending too much data from the server. Try logging smaller or more specific objects.";
            },
            set: function() {},
            enumerable: !0,
            configurable: !1
        });
        return null;
    }
    function extractIterator(response, model) {
        return model[Symbol.iterator]();
    }
    function createModel(response, model) {
        return model;
    }
    function getInferredFunctionApproximate(code) {
        code = code.startsWith("Object.defineProperty(") ? code.slice(22) : code.startsWith("(") ? code.slice(1) : code;
        if (code.startsWith("async function")) {
            var idx = code.indexOf("(", 14);
            if (-1 !== idx) return code = code.slice(14, idx).trim(), (0, eval)("({" + JSON.stringify(code) + ":async function(){}})")[code];
        } else if (code.startsWith("function")) {
            if (idx = code.indexOf("(", 8), -1 !== idx) return code = code.slice(8, idx).trim(), (0, eval)("({" + JSON.stringify(code) + ":function(){}})")[code];
        } else if (code.startsWith("class") && (idx = code.indexOf("{", 5), -1 !== idx)) return code = code.slice(5, idx).trim(), (0, eval)("({" + JSON.stringify(code) + ":class{}})")[code];
        return function() {};
    }
    function parseModelString(response, parentObject, key, value) {
        if ("$" === value[0]) {
            if ("$" === value) return null !== initializingHandler && "0" === key && (initializingHandler = {
                parent: initializingHandler,
                chunk: null,
                value: null,
                reason: null,
                deps: 0,
                errored: !1
            }), REACT_ELEMENT_TYPE;
            switch(value[1]){
                case "$":
                    return value.slice(1);
                case "L":
                    return parentObject = parseInt(value.slice(2), 16), response = getChunk(response, parentObject), null !== initializingChunk && isArrayImpl(initializingChunk._children) && initializingChunk._children.push(response), createLazyChunkWrapper(response, 0);
                case "@":
                    return parentObject = parseInt(value.slice(2), 16), response = getChunk(response, parentObject), null !== initializingChunk && isArrayImpl(initializingChunk._children) && initializingChunk._children.push(response), response;
                case "S":
                    return Symbol.for(value.slice(2));
                case "h":
                    var ref = value.slice(2);
                    return getOutlinedModel(response, ref, parentObject, key, loadServerReference);
                case "T":
                    parentObject = "$" + value.slice(2);
                    response = response._tempRefs;
                    if (null == response) throw Error("Missing a temporary reference set but the RSC response returned a temporary reference. Pass a temporaryReference option with the set that was used with the reply.");
                    return response.get(parentObject);
                case "Q":
                    return ref = value.slice(2), getOutlinedModel(response, ref, parentObject, key, createMap);
                case "W":
                    return ref = value.slice(2), getOutlinedModel(response, ref, parentObject, key, createSet);
                case "B":
                    return ref = value.slice(2), getOutlinedModel(response, ref, parentObject, key, createBlob);
                case "K":
                    return ref = value.slice(2), getOutlinedModel(response, ref, parentObject, key, createFormData);
                case "Z":
                    return ref = value.slice(2), getOutlinedModel(response, ref, parentObject, key, resolveErrorDev);
                case "i":
                    return ref = value.slice(2), getOutlinedModel(response, ref, parentObject, key, extractIterator);
                case "I":
                    return Infinity;
                case "-":
                    return "$-0" === value ? -0 : -Infinity;
                case "N":
                    return NaN;
                case "u":
                    return;
                case "D":
                    return new Date(Date.parse(value.slice(2)));
                case "n":
                    return BigInt(value.slice(2));
                case "P":
                    return ref = value.slice(2), getOutlinedModel(response, ref, parentObject, key, applyConstructor);
                case "E":
                    response = value.slice(2);
                    try {
                        if (!mightHaveStaticConstructor.test(response)) return (0, eval)(response);
                    } catch (x) {}
                    try {
                        if (ref = getInferredFunctionApproximate(response), response.startsWith("Object.defineProperty(")) {
                            var idx = response.lastIndexOf(',"name",{value:"');
                            if (-1 !== idx) {
                                var name = JSON.parse(response.slice(idx + 16 - 1, response.length - 2));
                                Object.defineProperty(ref, "name", {
                                    value: name
                                });
                            }
                        }
                    } catch (_) {
                        ref = function() {};
                    }
                    return ref;
                case "Y":
                    if (2 < value.length && (ref = response._debugChannel && response._debugChannel.callback)) {
                        if ("@" === value[2]) return parentObject = value.slice(3), key = parseInt(parentObject, 16), response._chunks.has(key) || ref("P:" + parentObject), getChunk(response, key);
                        value = value.slice(2);
                        idx = parseInt(value, 16);
                        response._chunks.has(idx) || ref("Q:" + value);
                        ref = getChunk(response, idx);
                        return "fulfilled" === ref.status ? ref.value : defineLazyGetter(response, ref, parentObject, key);
                    }
                    "__proto__" !== key && Object.defineProperty(parentObject, key, {
                        get: function() {
                            return "This object has been omitted by React in the console log to avoid sending too much data from the server. Try logging smaller or more specific objects.";
                        },
                        set: function() {},
                        enumerable: !0,
                        configurable: !1
                    });
                    return null;
                default:
                    return ref = value.slice(1), getOutlinedModel(response, ref, parentObject, key, createModel);
            }
        }
        return value;
    }
    function missingCall() {
        throw Error('Trying to call a function from "use server" but the callServer option was not implemented in your router runtime.');
    }
    function markIOStarted() {
        this._debugIOStarted = !0;
    }
    function ResponseInstance(bundlerConfig, serverReferenceConfig, moduleLoading, callServer, encodeFormAction, nonce, temporaryReferences, allowPartialStream, findSourceMapURL, replayConsole, environmentName, debugStartTime, debugEndTime, debugChannel) {
        var chunks = new Map();
        this._bundlerConfig = bundlerConfig;
        this._serverReferenceConfig = serverReferenceConfig;
        this._moduleLoading = moduleLoading;
        this._callServer = void 0 !== callServer ? callServer : missingCall;
        this._encodeFormAction = encodeFormAction;
        this._nonce = nonce;
        this._chunks = chunks;
        this._stringDecoder = new util.TextDecoder();
        this._closed = !1;
        this._closedReason = null;
        this._allowPartialStream = allowPartialStream;
        this._tempRefs = temporaryReferences;
        this._timeOrigin = 0;
        this._pendingInitialRender = null;
        this._pendingChunks = 0;
        this._weakResponse = {
            weak: new WeakRef(this),
            response: this
        };
        this._debugRootOwner = bundlerConfig = void 0 === ReactSharedInteralsServer || null === ReactSharedInteralsServer.A ? null : ReactSharedInteralsServer.A.getOwner();
        this._debugRootStack = null !== bundlerConfig ? Error("react-stack-top-frame") : null;
        environmentName = void 0 === environmentName ? "Server" : environmentName;
        supportsCreateTask && (this._debugRootTask = console.createTask('"use ' + environmentName.toLowerCase() + '"'));
        this._debugStartTime = null == debugStartTime ? performance.now() : debugStartTime;
        this._debugIOStarted = !1;
        setTimeout(markIOStarted.bind(this), 0);
        this._debugEndTime = null == debugEndTime ? null : debugEndTime;
        this._debugFindSourceMapURL = findSourceMapURL;
        this._debugChannel = debugChannel;
        this._blockedConsole = null;
        this._replayConsole = replayConsole;
        this._rootEnvironmentName = environmentName;
        debugChannel && (null === debugChannelRegistry ? (closeDebugChannel(debugChannel), this._debugChannel = void 0) : debugChannelRegistry.register(this, debugChannel, this));
        replayConsole && markAllTracksInOrder();
    }
    function createResponse(bundlerConfig, serverReferenceConfig, moduleLoading, callServer, encodeFormAction, nonce, temporaryReferences, allowPartialStream, findSourceMapURL, replayConsole, environmentName, debugStartTime, debugEndTime, debugChannel) {
        checkEvalAvailabilityOnceDev();
        bundlerConfig = new ResponseInstance(bundlerConfig, serverReferenceConfig, moduleLoading, callServer, encodeFormAction, nonce, temporaryReferences, allowPartialStream, findSourceMapURL, replayConsole, environmentName, debugStartTime, debugEndTime, debugChannel)._weakResponse;
        return bundlerConfig;
    }
    function createStreamState(weakResponse, streamDebugValue) {
        var streamState = {
            _rowState: 0,
            _rowID: 0,
            _rowTag: 0,
            _rowLength: 0,
            _buffer: []
        };
        weakResponse = unwrapWeakResponse(weakResponse);
        var debugValuePromise = Promise.resolve(streamDebugValue);
        debugValuePromise.status = "fulfilled";
        debugValuePromise.value = streamDebugValue;
        streamState._debugInfo = {
            name: "rsc stream",
            start: weakResponse._debugStartTime,
            end: weakResponse._debugStartTime,
            byteSize: 0,
            value: debugValuePromise,
            owner: weakResponse._debugRootOwner,
            debugStack: weakResponse._debugRootStack,
            debugTask: weakResponse._debugRootTask
        };
        streamState._debugTargetChunkSize = MIN_CHUNK_SIZE;
        return streamState;
    }
    function incrementChunkDebugInfo(streamState, chunkLength) {
        var debugInfo = streamState._debugInfo, endTime = performance.now(), previousEndTime = debugInfo.end;
        chunkLength = debugInfo.byteSize + chunkLength;
        chunkLength > streamState._debugTargetChunkSize || endTime > previousEndTime + 10 ? (streamState._debugInfo = {
            name: debugInfo.name,
            start: debugInfo.start,
            end: endTime,
            byteSize: chunkLength,
            value: debugInfo.value,
            owner: debugInfo.owner,
            debugStack: debugInfo.debugStack,
            debugTask: debugInfo.debugTask
        }, streamState._debugTargetChunkSize = chunkLength + MIN_CHUNK_SIZE) : (debugInfo.end = endTime, debugInfo.byteSize = chunkLength);
    }
    function addAsyncInfo(chunk, asyncInfo) {
        var value = resolveLazy(chunk.value);
        "object" !== typeof value || null === value || !isArrayImpl(value) && "function" !== typeof value[ASYNC_ITERATOR] && value.$$typeof !== REACT_ELEMENT_TYPE && value.$$typeof !== REACT_LAZY_TYPE ? chunk._debugInfo.push(asyncInfo) : isArrayImpl(value._debugInfo) ? value._debugInfo.push(asyncInfo) : Object.isFrozen(value) || Object.defineProperty(value, "_debugInfo", {
            configurable: !1,
            enumerable: !1,
            writable: !0,
            value: [
                asyncInfo
            ]
        });
    }
    function resolveChunkDebugInfo(response, streamState, chunk) {
        response._debugIOStarted && (response = {
            awaited: streamState._debugInfo
        }, "pending" === chunk.status || "blocked" === chunk.status ? (response = addAsyncInfo.bind(null, chunk, response), chunk.then(response, response)) : addAsyncInfo(chunk, response));
    }
    function resolveBuffer(response, id, buffer, streamState) {
        var chunks = response._chunks, chunk = chunks.get(id);
        chunk && "pending" !== chunk.status ? chunk.reason.enqueueValue(buffer) : (chunk && releasePendingChunk(response, chunk), buffer = new ReactPromise("fulfilled", buffer, null), resolveChunkDebugInfo(response, streamState, buffer), chunks.set(id, buffer));
    }
    function resolveModule(response, id, model, streamState) {
        var chunks = response._chunks, chunk = chunks.get(id);
        model = parseModel(response, model);
        var clientReference = resolveClientReference(response._bundlerConfig, model);
        prepareDestinationWithChunks(response._moduleLoading, model[1], response._nonce);
        if (model = preloadModule(clientReference)) {
            if (chunk) {
                releasePendingChunk(response, chunk);
                var blockedChunk = chunk;
                blockedChunk.status = "blocked";
            } else blockedChunk = new ReactPromise("blocked", null, null), chunks.set(id, blockedChunk);
            resolveChunkDebugInfo(response, streamState, blockedChunk);
            model.then(function() {
                return resolveModuleChunk(response, blockedChunk, clientReference);
            }, function(error) {
                return triggerErrorOnChunk(response, blockedChunk, error);
            });
        } else chunk ? (resolveChunkDebugInfo(response, streamState, chunk), resolveModuleChunk(response, chunk, clientReference)) : (chunk = new ReactPromise("resolved_module", clientReference, null), resolveChunkDebugInfo(response, streamState, chunk), chunks.set(id, chunk));
    }
    function resolveStream(response, id, stream, controller, streamState) {
        var chunks = response._chunks, chunk = chunks.get(id);
        if (chunk) {
            if (resolveChunkDebugInfo(response, streamState, chunk), "pending" === chunk.status) {
                id = chunk.value;
                if (null != chunk._debugChunk) {
                    streamState = initializingHandler;
                    chunks = initializingChunk;
                    initializingHandler = null;
                    chunk.status = "blocked";
                    chunk.value = null;
                    chunk.reason = null;
                    initializingChunk = chunk;
                    try {
                        if (initializeDebugChunk(response, chunk), null !== initializingHandler && !initializingHandler.errored && 0 < initializingHandler.deps) {
                            initializingHandler.value = stream;
                            initializingHandler.reason = controller;
                            initializingHandler.chunk = chunk;
                            return;
                        }
                    } finally{
                        initializingHandler = streamState, initializingChunk = chunks;
                    }
                }
                chunk.status = "fulfilled";
                chunk.value = stream;
                chunk.reason = controller;
                null !== id ? wakeChunk(response, id, chunk.value, chunk) : (filterDebugInfo(response, chunk), moveDebugInfoFromChunkToInnerValue(chunk, stream));
            }
        } else 0 === response._pendingChunks++ && (response._weakResponse.response = response), stream = new ReactPromise("fulfilled", stream, controller), resolveChunkDebugInfo(response, streamState, stream), chunks.set(id, stream);
    }
    function startReadableStream(response, id, type, streamState) {
        var controller = null, closed = !1;
        type = new ReadableStream({
            type: type,
            start: function(c) {
                controller = c;
            }
        });
        var previousBlockedChunk = null;
        resolveStream(response, id, type, {
            enqueueValue: function(value) {
                null === previousBlockedChunk ? controller.enqueue(value) : previousBlockedChunk.then(function() {
                    controller.enqueue(value);
                });
            },
            enqueueModel: function(json) {
                if (null === previousBlockedChunk) {
                    var chunk = createResolvedModelChunk(response, json);
                    initializeModelChunk(chunk);
                    "fulfilled" === chunk.status ? controller.enqueue(chunk.value) : (chunk.then(function(v) {
                        return controller.enqueue(v);
                    }, function(e) {
                        return controller.error(e);
                    }), previousBlockedChunk = chunk);
                } else {
                    chunk = previousBlockedChunk;
                    var _chunk3 = createPendingChunk(response);
                    _chunk3.then(function(v) {
                        return controller.enqueue(v);
                    }, function(e) {
                        return controller.error(e);
                    });
                    previousBlockedChunk = _chunk3;
                    chunk.then(function() {
                        previousBlockedChunk === _chunk3 && (previousBlockedChunk = null);
                        resolveModelChunk(response, _chunk3, json);
                    });
                }
            },
            close: function() {
                if (!closed) if (closed = !0, null === previousBlockedChunk) controller.close();
                else {
                    var blockedChunk = previousBlockedChunk;
                    previousBlockedChunk = null;
                    blockedChunk.then(function() {
                        return controller.close();
                    });
                }
            },
            error: function(error) {
                if (!closed) if (closed = !0, null === previousBlockedChunk) controller.error(error);
                else {
                    var blockedChunk = previousBlockedChunk;
                    previousBlockedChunk = null;
                    blockedChunk.then(function() {
                        return controller.error(error);
                    });
                }
            }
        }, streamState);
    }
    function asyncIterator() {
        return this;
    }
    function createIterator(next) {
        next = {
            next: next
        };
        next[ASYNC_ITERATOR] = asyncIterator;
        return next;
    }
    function startAsyncIterable(response, id, iterator, streamState) {
        var buffer = [], closed = !1, nextWriteIndex = 0, iterable = {};
        iterable[ASYNC_ITERATOR] = function() {
            var nextReadIndex = 0;
            return createIterator(function(arg) {
                if (void 0 !== arg) throw Error("Values cannot be passed to next() of AsyncIterables passed to Client Components.");
                if (nextReadIndex === buffer.length) {
                    if (closed) return new ReactPromise("fulfilled", {
                        done: !0,
                        value: void 0
                    }, null);
                    buffer[nextReadIndex] = createPendingChunk(response);
                }
                return buffer[nextReadIndex++];
            });
        };
        resolveStream(response, id, iterator ? iterable[ASYNC_ITERATOR]() : iterable, {
            enqueueValue: function(value) {
                if (nextWriteIndex === buffer.length) buffer[nextWriteIndex] = new ReactPromise("fulfilled", {
                    done: !1,
                    value: value
                }, null);
                else {
                    var chunk = buffer[nextWriteIndex], resolveListeners = chunk.value, rejectListeners = chunk.reason;
                    chunk.status = "fulfilled";
                    chunk.value = {
                        done: !1,
                        value: value
                    };
                    chunk.reason = null;
                    null !== resolveListeners && wakeChunkIfInitialized(response, chunk, resolveListeners, rejectListeners);
                }
                nextWriteIndex++;
            },
            enqueueModel: function(value) {
                nextWriteIndex === buffer.length ? buffer[nextWriteIndex] = createResolvedIteratorResultChunk(response, value, !1) : resolveIteratorResultChunk(response, buffer[nextWriteIndex], value, !1);
                nextWriteIndex++;
            },
            close: function(value) {
                if (!closed) for(closed = !0, nextWriteIndex === buffer.length ? buffer[nextWriteIndex] = createResolvedIteratorResultChunk(response, value, !0) : resolveIteratorResultChunk(response, buffer[nextWriteIndex], value, !0), nextWriteIndex++; nextWriteIndex < buffer.length;)resolveIteratorResultChunk(response, buffer[nextWriteIndex++], '"$undefined"', !0);
            },
            error: function(error) {
                if (!closed) for(closed = !0, nextWriteIndex === buffer.length && (buffer[nextWriteIndex] = createPendingChunk(response)); nextWriteIndex < buffer.length;)triggerErrorOnChunk(response, buffer[nextWriteIndex++], error);
            }
        }, streamState);
    }
    function resolveErrorDev(response, errorInfo) {
        var name = errorInfo.name, message = errorInfo.message, stack = errorInfo.stack, env = errorInfo.env, errorOptions = "cause" in errorInfo ? {
            cause: reviveModel(response, errorInfo.cause, errorInfo, "cause")
        } : void 0;
        message = buildFakeCallStack(response, stack, env, !1, Error.bind(null, message || "An error occurred in the Server Components render but no message was provided", errorOptions));
        stack = null;
        null != errorInfo.owner && (errorInfo = errorInfo.owner.slice(1), errorInfo = getOutlinedModel(response, errorInfo, {}, "", createModel), null !== errorInfo && (stack = initializeFakeTask(response, errorInfo)));
        null === stack ? (response = getRootTask(response, env), response = null != response ? response.run(message) : message()) : response = stack.run(message);
        response.name = name;
        response.environmentName = env;
        return response;
    }
    function createFakeFunction(name, filename, sourceMap, line, col, enclosingLine, enclosingCol, environmentName) {
        name || (name = "<anonymous>");
        var encodedName = JSON.stringify(name);
        1 > enclosingLine ? enclosingLine = 0 : enclosingLine--;
        1 > enclosingCol ? enclosingCol = 0 : enclosingCol--;
        1 > line ? line = 0 : line--;
        1 > col ? col = 0 : col--;
        if (line < enclosingLine || line === enclosingLine && col < enclosingCol) enclosingCol = enclosingLine = 0;
        1 > line ? (line = encodedName.length + 3, enclosingCol -= line, 0 > enclosingCol && (enclosingCol = 0), col = col - enclosingCol - line - 3, 0 > col && (col = 0), encodedName = "({" + encodedName + ":" + " ".repeat(enclosingCol) + "_=>" + " ".repeat(col) + "_()})") : 1 > enclosingLine ? (enclosingCol -= encodedName.length + 3, 0 > enclosingCol && (enclosingCol = 0), encodedName = "({" + encodedName + ":" + " ".repeat(enclosingCol) + "_=>" + "\n".repeat(line - enclosingLine) + " ".repeat(col) + "_()})") : enclosingLine === line ? (col = col - enclosingCol - 3, 0 > col && (col = 0), encodedName = "\n".repeat(enclosingLine - 1) + "({" + encodedName + ":\n" + " ".repeat(enclosingCol) + "_=>" + " ".repeat(col) + "_()})") : encodedName = "\n".repeat(enclosingLine - 1) + "({" + encodedName + ":\n" + " ".repeat(enclosingCol) + "_=>" + "\n".repeat(line - enclosingLine) + " ".repeat(col) + "_()})";
        encodedName = 1 > enclosingLine ? encodedName + "\n/* This module was rendered by a Server Component. Turn on Source Maps to see the server source. */" : "/* This module was rendered by a Server Component. Turn on Source Maps to see the server source. */" + encodedName;
        filename.startsWith("/") && (filename = "file://" + filename);
        sourceMap ? (encodedName += "\n//# sourceURL=about://React/" + encodeURIComponent(environmentName) + "/" + encodeURI(filename) + "?" + fakeFunctionIdx++, encodedName += "\n//# sourceMappingURL=" + sourceMap) : encodedName = filename ? encodedName + ("\n//# sourceURL=" + encodeURI(filename)) : encodedName + "\n//# sourceURL=<anonymous>";
        try {
            var fn = (0, eval)(encodedName)[name];
        } catch (x) {
            fn = function(_) {
                return _();
            }, Object.defineProperty(fn, "name", {
                value: name
            });
        }
        return fn;
    }
    function buildFakeCallStack(response, stack, environmentName, useEnclosingLine, innerCall) {
        for(var i = 0; i < stack.length; i++){
            var frame = stack[i], frameKey = frame.join("-") + "-" + environmentName + (useEnclosingLine ? "-e" : "-n"), fn = fakeFunctionCache.get(frameKey);
            if (void 0 === fn) {
                fn = frame[0];
                var filename = frame[1], line = frame[2], col = frame[3], enclosingLine = frame[4];
                frame = frame[5];
                var findSourceMapURL = response._debugFindSourceMapURL;
                findSourceMapURL = findSourceMapURL ? findSourceMapURL(filename, environmentName) : null;
                fn = createFakeFunction(fn, filename, findSourceMapURL, line, col, useEnclosingLine ? line : enclosingLine, useEnclosingLine ? col : frame, environmentName);
                fakeFunctionCache.set(frameKey, fn);
            }
            innerCall = fn.bind(null, innerCall);
        }
        return innerCall;
    }
    function getRootTask(response, childEnvironmentName) {
        var rootTask = response._debugRootTask;
        return rootTask ? response._rootEnvironmentName !== childEnvironmentName ? (response = console.createTask.bind(console, '"use ' + childEnvironmentName.toLowerCase() + '"'), rootTask.run(response)) : rootTask : null;
    }
    function initializeFakeTask(response, debugInfo) {
        if (!supportsCreateTask || null == debugInfo.stack) return null;
        var cachedEntry = debugInfo.debugTask;
        if (void 0 !== cachedEntry) return cachedEntry;
        var useEnclosingLine = void 0 === debugInfo.key, stack = debugInfo.stack, env = null == debugInfo.env ? response._rootEnvironmentName : debugInfo.env;
        cachedEntry = null == debugInfo.owner || null == debugInfo.owner.env ? response._rootEnvironmentName : debugInfo.owner.env;
        var ownerTask = null == debugInfo.owner ? null : initializeFakeTask(response, debugInfo.owner);
        env = env !== cachedEntry ? '"use ' + env.toLowerCase() + '"' : void 0 !== debugInfo.key ? "<" + (debugInfo.name || "...") + ">" : void 0 !== debugInfo.name ? debugInfo.name || "unknown" : "await " + (debugInfo.awaited.name || "unknown");
        env = console.createTask.bind(console, env);
        useEnclosingLine = buildFakeCallStack(response, stack, cachedEntry, useEnclosingLine, env);
        null === ownerTask ? (response = getRootTask(response, cachedEntry), response = null != response ? response.run(useEnclosingLine) : useEnclosingLine()) : response = ownerTask.run(useEnclosingLine);
        return debugInfo.debugTask = response;
    }
    function fakeJSXCallSite() {
        return Error("react-stack-top-frame");
    }
    function initializeFakeStack(response, debugInfo) {
        if (void 0 === debugInfo.debugStack) {
            null != debugInfo.stack && (debugInfo.debugStack = createFakeJSXCallStackInDEV(response, debugInfo.stack, null == debugInfo.env ? "" : debugInfo.env));
            var owner = debugInfo.owner;
            null != owner && (initializeFakeStack(response, owner), void 0 === owner.debugLocation && null != debugInfo.debugStack && (owner.debugLocation = debugInfo.debugStack));
        }
    }
    function initializeDebugInfo(response, debugInfo) {
        void 0 !== debugInfo.stack && initializeFakeTask(response, debugInfo);
        if (null == debugInfo.owner && null != response._debugRootOwner) {
            var _componentInfoOrAsyncInfo = debugInfo;
            _componentInfoOrAsyncInfo.owner = response._debugRootOwner;
            _componentInfoOrAsyncInfo.stack = null;
            _componentInfoOrAsyncInfo.debugStack = response._debugRootStack;
            _componentInfoOrAsyncInfo.debugTask = response._debugRootTask;
        } else void 0 !== debugInfo.stack && initializeFakeStack(response, debugInfo);
        "number" === typeof debugInfo.time && (debugInfo = {
            time: debugInfo.time + response._timeOrigin
        });
        return debugInfo;
    }
    function getCurrentStackInDEV() {
        var owner = currentOwnerInDEV;
        if (null === owner) return "";
        try {
            var info = "";
            if (owner.owner || "string" !== typeof owner.name) {
                for(; owner;){
                    var ownerStack = owner.debugStack;
                    if (null != ownerStack) {
                        if (owner = owner.owner) {
                            var JSCompiler_temp_const = info;
                            var error = ownerStack, prevPrepareStackTrace = Error.prepareStackTrace;
                            Error.prepareStackTrace = prepareStackTrace;
                            var stack = error.stack;
                            Error.prepareStackTrace = prevPrepareStackTrace;
                            stack.startsWith("Error: react-stack-top-frame\n") && (stack = stack.slice(29));
                            var idx = stack.indexOf("\n");
                            -1 !== idx && (stack = stack.slice(idx + 1));
                            idx = stack.indexOf("react_stack_bottom_frame");
                            -1 !== idx && (idx = stack.lastIndexOf("\n", idx));
                            var JSCompiler_inline_result = -1 !== idx ? stack = stack.slice(0, idx) : "";
                            info = JSCompiler_temp_const + ("\n" + JSCompiler_inline_result);
                        }
                    } else break;
                }
                var JSCompiler_inline_result$jscomp$0 = info;
            } else {
                JSCompiler_temp_const = owner.name;
                if (void 0 === prefix) try {
                    throw Error();
                } catch (x) {
                    prefix = (error = x.stack.trim().match(/\n( *(at )?)/)) && error[1] || "", suffix = -1 < x.stack.indexOf("\n    at") ? " (<anonymous>)" : -1 < x.stack.indexOf("@") ? "@unknown:0:0" : "";
                }
                JSCompiler_inline_result$jscomp$0 = "\n" + prefix + JSCompiler_temp_const + suffix;
            }
        } catch (x) {
            JSCompiler_inline_result$jscomp$0 = "\nError generating stack: " + x.message + "\n" + x.stack;
        }
        return JSCompiler_inline_result$jscomp$0;
    }
    function resolveConsoleEntry(response, json) {
        if (response._replayConsole) {
            var blockedChunk = response._blockedConsole;
            if (null == blockedChunk) blockedChunk = createResolvedModelChunk(response, json), initializeModelChunk(blockedChunk), "fulfilled" === blockedChunk.status ? replayConsoleWithCallStackInDEV(response, blockedChunk.value) : (blockedChunk.then(function(v) {
                return replayConsoleWithCallStackInDEV(response, v);
            }, function() {}), response._blockedConsole = blockedChunk);
            else {
                var _chunk4 = createPendingChunk(response);
                _chunk4.then(function(v) {
                    return replayConsoleWithCallStackInDEV(response, v);
                }, function() {});
                response._blockedConsole = _chunk4;
                var unblock = function() {
                    response._blockedConsole === _chunk4 && (response._blockedConsole = null);
                    resolveModelChunk(response, _chunk4, json);
                };
                blockedChunk.then(unblock, unblock);
            }
        }
    }
    function initializeIOInfo(response, ioInfo) {
        void 0 !== ioInfo.stack && (initializeFakeTask(response, ioInfo), initializeFakeStack(response, ioInfo));
        ioInfo.start += response._timeOrigin;
        ioInfo.end += response._timeOrigin;
        if (response._replayConsole) {
            response = response._rootEnvironmentName;
            var promise = ioInfo.value;
            if (promise) switch(promise.status){
                case "fulfilled":
                    logIOInfo(ioInfo, response, promise.value);
                    break;
                case "rejected":
                    logIOInfoErrored(ioInfo, response, promise.reason);
                    break;
                default:
                    promise.then(logIOInfo.bind(null, ioInfo, response), logIOInfoErrored.bind(null, ioInfo, response));
            }
            else logIOInfo(ioInfo, response, void 0);
        }
    }
    function resolveIOInfo(response, id, model) {
        var chunks = response._chunks, chunk = chunks.get(id), prevIsInitializingDebugInfo = isInitializingDebugInfo;
        isInitializingDebugInfo = !0;
        try {
            chunk ? (resolveModelChunk(response, chunk, model), "resolved_model" === chunk.status && initializeModelChunk(chunk)) : (chunk = createResolvedModelChunk(response, model), chunks.set(id, chunk), initializeModelChunk(chunk));
        } finally{
            isInitializingDebugInfo = prevIsInitializingDebugInfo;
        }
        "fulfilled" === chunk.status ? initializeIOInfo(response, chunk.value) : chunk.then(function(v) {
            initializeIOInfo(response, v);
        }, function() {});
    }
    function mergeBuffer(buffer, lastChunk) {
        for(var l = buffer.length, byteLength = lastChunk.length, i = 0; i < l; i++)byteLength += buffer[i].byteLength;
        byteLength = new Uint8Array(byteLength);
        for(var _i3 = i = 0; _i3 < l; _i3++){
            var chunk = buffer[_i3];
            byteLength.set(chunk, i);
            i += chunk.byteLength;
        }
        byteLength.set(lastChunk, i);
        return byteLength;
    }
    function resolveTypedArray(response, id, buffer, lastChunk, constructor, bytesPerElement, streamState) {
        buffer = 0 === buffer.length && 0 === lastChunk.byteOffset % bytesPerElement ? lastChunk : mergeBuffer(buffer, lastChunk);
        constructor = new constructor(buffer.buffer, buffer.byteOffset, buffer.byteLength / bytesPerElement);
        resolveBuffer(response, id, constructor, streamState);
    }
    function flushComponentPerformance(response$jscomp$0, root, trackIdx$jscomp$6, trackTime, parentEndTime) {
        if (!isArrayImpl(root._children)) {
            var previousResult = root._children, previousEndTime = previousResult.endTime;
            if (-Infinity < parentEndTime && parentEndTime < previousEndTime && null !== previousResult.component) {
                var componentInfo = previousResult.component, trackIdx = trackIdx$jscomp$6, startTime = parentEndTime;
                if (supportsUserTiming && 0 <= previousEndTime && 10 > trackIdx) {
                    var color = componentInfo.env === response$jscomp$0._rootEnvironmentName ? "primary-light" : "secondary-light", entryName = componentInfo.name + " [deduped]", debugTask = componentInfo.debugTask;
                    debugTask ? debugTask.run(console.timeStamp.bind(console, entryName, 0 > startTime ? 0 : startTime, previousEndTime, trackNames[trackIdx], "Server Components \u269b", color)) : console.timeStamp(entryName, 0 > startTime ? 0 : startTime, previousEndTime, trackNames[trackIdx], "Server Components \u269b", color);
                }
            }
            previousResult.track = trackIdx$jscomp$6;
            return previousResult;
        }
        var children = root._children;
        var debugInfo = root._debugInfo;
        if (0 === debugInfo.length && "fulfilled" === root.status) {
            var resolvedValue = resolveLazy(root.value);
            "object" === typeof resolvedValue && null !== resolvedValue && (isArrayImpl(resolvedValue) || "function" === typeof resolvedValue[ASYNC_ITERATOR] || resolvedValue.$$typeof === REACT_ELEMENT_TYPE || resolvedValue.$$typeof === REACT_LAZY_TYPE) && isArrayImpl(resolvedValue._debugInfo) && (debugInfo = resolvedValue._debugInfo);
        }
        if (debugInfo) {
            for(var startTime$jscomp$0 = 0, i = 0; i < debugInfo.length; i++){
                var info = debugInfo[i];
                "number" === typeof info.time && (startTime$jscomp$0 = info.time);
                if ("string" === typeof info.name) {
                    startTime$jscomp$0 < trackTime && trackIdx$jscomp$6++;
                    trackTime = startTime$jscomp$0;
                    break;
                }
            }
            for(var _i4 = debugInfo.length - 1; 0 <= _i4; _i4--){
                var _info = debugInfo[_i4];
                if ("number" === typeof _info.time && _info.time > parentEndTime) {
                    parentEndTime = _info.time;
                    break;
                }
            }
        }
        var result = {
            track: trackIdx$jscomp$6,
            endTime: -Infinity,
            component: null
        };
        root._children = result;
        for(var childrenEndTime = -Infinity, childTrackIdx = trackIdx$jscomp$6, childTrackTime = trackTime, _i5 = 0; _i5 < children.length; _i5++){
            var childResult = flushComponentPerformance(response$jscomp$0, children[_i5], childTrackIdx, childTrackTime, parentEndTime);
            null !== childResult.component && (result.component = childResult.component);
            childTrackIdx = childResult.track;
            var childEndTime = childResult.endTime;
            childEndTime > childTrackTime && (childTrackTime = childEndTime);
            childEndTime > childrenEndTime && (childrenEndTime = childEndTime);
        }
        if (debugInfo) for(var componentEndTime = 0, isLastComponent = !0, endTime = -1, endTimeIdx = -1, _i6 = debugInfo.length - 1; 0 <= _i6; _i6--){
            var _info2 = debugInfo[_i6];
            if ("number" === typeof _info2.time) {
                0 === componentEndTime && (componentEndTime = _info2.time);
                var time = _info2.time;
                if (-1 < endTimeIdx) for(var j = endTimeIdx - 1; j > _i6; j--){
                    var candidateInfo = debugInfo[j];
                    if ("string" === typeof candidateInfo.name) {
                        componentEndTime > childrenEndTime && (childrenEndTime = componentEndTime);
                        var componentInfo$jscomp$0 = candidateInfo, response = response$jscomp$0, componentInfo$jscomp$1 = componentInfo$jscomp$0, trackIdx$jscomp$0 = trackIdx$jscomp$6, startTime$jscomp$1 = time, componentEndTime$jscomp$0 = componentEndTime, childrenEndTime$jscomp$0 = childrenEndTime;
                        if (isLastComponent && "rejected" === root.status && root.reason !== response._closedReason) {
                            var componentInfo$jscomp$2 = componentInfo$jscomp$1, trackIdx$jscomp$1 = trackIdx$jscomp$0, startTime$jscomp$2 = startTime$jscomp$1, childrenEndTime$jscomp$1 = childrenEndTime$jscomp$0, error = root.reason;
                            if (supportsUserTiming) {
                                var env = componentInfo$jscomp$2.env, name = componentInfo$jscomp$2.name, entryName$jscomp$0 = env === response._rootEnvironmentName || void 0 === env ? name : name + " [" + env + "]", measureName = "\u200b" + entryName$jscomp$0, properties = [
                                    [
                                        "Error",
                                        "object" === typeof error && null !== error && "string" === typeof error.message ? String(error.message) : String(error)
                                    ]
                                ];
                                null != componentInfo$jscomp$2.key && addValueToProperties("key", componentInfo$jscomp$2.key, properties, 0, "");
                                null != componentInfo$jscomp$2.props && addObjectToProperties(componentInfo$jscomp$2.props, properties, 0, "");
                                performance.measure(measureName, {
                                    start: 0 > startTime$jscomp$2 ? 0 : startTime$jscomp$2,
                                    end: childrenEndTime$jscomp$1,
                                    detail: {
                                        devtools: {
                                            color: "error",
                                            track: trackNames[trackIdx$jscomp$1],
                                            trackGroup: "Server Components \u269b",
                                            tooltipText: entryName$jscomp$0 + " Errored",
                                            properties: properties
                                        }
                                    }
                                });
                                performance.clearMeasures(measureName);
                            }
                        } else {
                            var componentInfo$jscomp$3 = componentInfo$jscomp$1, trackIdx$jscomp$2 = trackIdx$jscomp$0, startTime$jscomp$3 = startTime$jscomp$1, childrenEndTime$jscomp$2 = childrenEndTime$jscomp$0;
                            if (supportsUserTiming && 0 <= childrenEndTime$jscomp$2 && 10 > trackIdx$jscomp$2) {
                                var env$jscomp$0 = componentInfo$jscomp$3.env, name$jscomp$0 = componentInfo$jscomp$3.name, isPrimaryEnv = env$jscomp$0 === response._rootEnvironmentName, selfTime = componentEndTime$jscomp$0 - startTime$jscomp$3, color$jscomp$0 = 0.5 > selfTime ? isPrimaryEnv ? "primary-light" : "secondary-light" : 50 > selfTime ? isPrimaryEnv ? "primary" : "secondary" : 500 > selfTime ? isPrimaryEnv ? "primary-dark" : "secondary-dark" : "error", debugTask$jscomp$0 = componentInfo$jscomp$3.debugTask, measureName$jscomp$0 = "\u200b" + (isPrimaryEnv || void 0 === env$jscomp$0 ? name$jscomp$0 : name$jscomp$0 + " [" + env$jscomp$0 + "]");
                                if (debugTask$jscomp$0) {
                                    var properties$jscomp$0 = [];
                                    null != componentInfo$jscomp$3.key && addValueToProperties("key", componentInfo$jscomp$3.key, properties$jscomp$0, 0, "");
                                    null != componentInfo$jscomp$3.props && addObjectToProperties(componentInfo$jscomp$3.props, properties$jscomp$0, 0, "");
                                    debugTask$jscomp$0.run(performance.measure.bind(performance, measureName$jscomp$0, {
                                        start: 0 > startTime$jscomp$3 ? 0 : startTime$jscomp$3,
                                        end: childrenEndTime$jscomp$2,
                                        detail: {
                                            devtools: {
                                                color: color$jscomp$0,
                                                track: trackNames[trackIdx$jscomp$2],
                                                trackGroup: "Server Components \u269b",
                                                properties: properties$jscomp$0
                                            }
                                        }
                                    }));
                                    performance.clearMeasures(measureName$jscomp$0);
                                } else console.timeStamp(measureName$jscomp$0, 0 > startTime$jscomp$3 ? 0 : startTime$jscomp$3, childrenEndTime$jscomp$2, trackNames[trackIdx$jscomp$2], "Server Components \u269b", color$jscomp$0);
                            }
                        }
                        componentEndTime = time;
                        result.component = componentInfo$jscomp$0;
                        isLastComponent = !1;
                    } else if (candidateInfo.awaited && null != candidateInfo.awaited.env) {
                        endTime > childrenEndTime && (childrenEndTime = endTime);
                        var asyncInfo = candidateInfo, env$jscomp$1 = response$jscomp$0._rootEnvironmentName, promise = asyncInfo.awaited.value;
                        if (promise) {
                            var thenable = promise;
                            switch(thenable.status){
                                case "fulfilled":
                                    logComponentAwait(asyncInfo, trackIdx$jscomp$6, time, endTime, env$jscomp$1, thenable.value);
                                    break;
                                case "rejected":
                                    var asyncInfo$jscomp$0 = asyncInfo, trackIdx$jscomp$3 = trackIdx$jscomp$6, startTime$jscomp$4 = time, endTime$jscomp$0 = endTime, rootEnv = env$jscomp$1, error$jscomp$0 = thenable.reason;
                                    if (supportsUserTiming && 0 < endTime$jscomp$0) {
                                        var description = getIODescription(error$jscomp$0), entryName$jscomp$1 = "await " + getIOShortName(asyncInfo$jscomp$0.awaited, description, asyncInfo$jscomp$0.env, rootEnv), debugTask$jscomp$1 = asyncInfo$jscomp$0.debugTask || asyncInfo$jscomp$0.awaited.debugTask;
                                        if (debugTask$jscomp$1) {
                                            var properties$jscomp$1 = [
                                                [
                                                    "Rejected",
                                                    "object" === typeof error$jscomp$0 && null !== error$jscomp$0 && "string" === typeof error$jscomp$0.message ? String(error$jscomp$0.message) : String(error$jscomp$0)
                                                ]
                                            ], tooltipText = getIOLongName(asyncInfo$jscomp$0.awaited, description, asyncInfo$jscomp$0.env, rootEnv) + " Rejected";
                                            debugTask$jscomp$1.run(performance.measure.bind(performance, entryName$jscomp$1, {
                                                start: 0 > startTime$jscomp$4 ? 0 : startTime$jscomp$4,
                                                end: endTime$jscomp$0,
                                                detail: {
                                                    devtools: {
                                                        color: "error",
                                                        track: trackNames[trackIdx$jscomp$3],
                                                        trackGroup: "Server Components \u269b",
                                                        properties: properties$jscomp$1,
                                                        tooltipText: tooltipText
                                                    }
                                                }
                                            }));
                                            performance.clearMeasures(entryName$jscomp$1);
                                        } else console.timeStamp(entryName$jscomp$1, 0 > startTime$jscomp$4 ? 0 : startTime$jscomp$4, endTime$jscomp$0, trackNames[trackIdx$jscomp$3], "Server Components \u269b", "error");
                                    }
                                    break;
                                default:
                                    logComponentAwait(asyncInfo, trackIdx$jscomp$6, time, endTime, env$jscomp$1, void 0);
                            }
                        } else logComponentAwait(asyncInfo, trackIdx$jscomp$6, time, endTime, env$jscomp$1, void 0);
                    }
                }
                else {
                    endTime = time;
                    for(var _j = debugInfo.length - 1; _j > _i6; _j--){
                        var _candidateInfo = debugInfo[_j];
                        if ("string" === typeof _candidateInfo.name) {
                            componentEndTime > childrenEndTime && (childrenEndTime = componentEndTime);
                            var _componentInfo = _candidateInfo, _env = response$jscomp$0._rootEnvironmentName, componentInfo$jscomp$4 = _componentInfo, trackIdx$jscomp$4 = trackIdx$jscomp$6, startTime$jscomp$5 = time, childrenEndTime$jscomp$3 = childrenEndTime;
                            if (supportsUserTiming) {
                                var env$jscomp$2 = componentInfo$jscomp$4.env, name$jscomp$1 = componentInfo$jscomp$4.name, entryName$jscomp$2 = env$jscomp$2 === _env || void 0 === env$jscomp$2 ? name$jscomp$1 : name$jscomp$1 + " [" + env$jscomp$2 + "]", measureName$jscomp$1 = "\u200b" + entryName$jscomp$2, properties$jscomp$2 = [
                                    [
                                        "Aborted",
                                        "The stream was aborted before this Component finished rendering."
                                    ]
                                ];
                                null != componentInfo$jscomp$4.key && addValueToProperties("key", componentInfo$jscomp$4.key, properties$jscomp$2, 0, "");
                                null != componentInfo$jscomp$4.props && addObjectToProperties(componentInfo$jscomp$4.props, properties$jscomp$2, 0, "");
                                performance.measure(measureName$jscomp$1, {
                                    start: 0 > startTime$jscomp$5 ? 0 : startTime$jscomp$5,
                                    end: childrenEndTime$jscomp$3,
                                    detail: {
                                        devtools: {
                                            color: "warning",
                                            track: trackNames[trackIdx$jscomp$4],
                                            trackGroup: "Server Components \u269b",
                                            tooltipText: entryName$jscomp$2 + " Aborted",
                                            properties: properties$jscomp$2
                                        }
                                    }
                                });
                                performance.clearMeasures(measureName$jscomp$1);
                            }
                            componentEndTime = time;
                            result.component = _componentInfo;
                            isLastComponent = !1;
                        } else if (_candidateInfo.awaited && null != _candidateInfo.awaited.env) {
                            var _asyncInfo = _candidateInfo, _env2 = response$jscomp$0._rootEnvironmentName;
                            _asyncInfo.awaited.end > endTime && (endTime = _asyncInfo.awaited.end);
                            endTime > childrenEndTime && (childrenEndTime = endTime);
                            var asyncInfo$jscomp$1 = _asyncInfo, trackIdx$jscomp$5 = trackIdx$jscomp$6, startTime$jscomp$6 = time, endTime$jscomp$1 = endTime, rootEnv$jscomp$0 = _env2;
                            if (supportsUserTiming && 0 < endTime$jscomp$1) {
                                var entryName$jscomp$3 = "await " + getIOShortName(asyncInfo$jscomp$1.awaited, "", asyncInfo$jscomp$1.env, rootEnv$jscomp$0), debugTask$jscomp$2 = asyncInfo$jscomp$1.debugTask || asyncInfo$jscomp$1.awaited.debugTask;
                                if (debugTask$jscomp$2) {
                                    var tooltipText$jscomp$0 = getIOLongName(asyncInfo$jscomp$1.awaited, "", asyncInfo$jscomp$1.env, rootEnv$jscomp$0) + " Aborted";
                                    debugTask$jscomp$2.run(performance.measure.bind(performance, entryName$jscomp$3, {
                                        start: 0 > startTime$jscomp$6 ? 0 : startTime$jscomp$6,
                                        end: endTime$jscomp$1,
                                        detail: {
                                            devtools: {
                                                color: "warning",
                                                track: trackNames[trackIdx$jscomp$5],
                                                trackGroup: "Server Components \u269b",
                                                properties: [
                                                    [
                                                        "Aborted",
                                                        "The stream was aborted before this Promise resolved."
                                                    ]
                                                ],
                                                tooltipText: tooltipText$jscomp$0
                                            }
                                        }
                                    }));
                                    performance.clearMeasures(entryName$jscomp$3);
                                } else console.timeStamp(entryName$jscomp$3, 0 > startTime$jscomp$6 ? 0 : startTime$jscomp$6, endTime$jscomp$1, trackNames[trackIdx$jscomp$5], "Server Components \u269b", "warning");
                            }
                        }
                    }
                }
                endTime = time;
                endTimeIdx = _i6;
            }
        }
        result.endTime = childrenEndTime;
        return result;
    }
    function flushInitialRenderPerformance(response) {
        if (response._replayConsole) {
            var rootChunk = getChunk(response, 0);
            isArrayImpl(rootChunk._children) && (markAllTracksInOrder(), flushComponentPerformance(response, rootChunk, 0, -Infinity, -Infinity));
        }
    }
    function processFullBinaryRow(response, streamState, id, tag, buffer, chunk) {
        switch(tag){
            case 65:
                resolveBuffer(response, id, mergeBuffer(buffer, chunk).buffer, streamState);
                return;
            case 79:
                resolveTypedArray(response, id, buffer, chunk, Int8Array, 1, streamState);
                return;
            case 111:
                resolveBuffer(response, id, 0 === buffer.length ? chunk : mergeBuffer(buffer, chunk), streamState);
                return;
            case 85:
                resolveTypedArray(response, id, buffer, chunk, Uint8ClampedArray, 1, streamState);
                return;
            case 83:
                resolveTypedArray(response, id, buffer, chunk, Int16Array, 2, streamState);
                return;
            case 115:
                resolveTypedArray(response, id, buffer, chunk, Uint16Array, 2, streamState);
                return;
            case 76:
                resolveTypedArray(response, id, buffer, chunk, Int32Array, 4, streamState);
                return;
            case 108:
                resolveTypedArray(response, id, buffer, chunk, Uint32Array, 4, streamState);
                return;
            case 71:
                resolveTypedArray(response, id, buffer, chunk, Float32Array, 4, streamState);
                return;
            case 103:
                resolveTypedArray(response, id, buffer, chunk, Float64Array, 8, streamState);
                return;
            case 77:
                resolveTypedArray(response, id, buffer, chunk, BigInt64Array, 8, streamState);
                return;
            case 109:
                resolveTypedArray(response, id, buffer, chunk, BigUint64Array, 8, streamState);
                return;
            case 86:
                resolveTypedArray(response, id, buffer, chunk, DataView, 1, streamState);
                return;
        }
        for(var stringDecoder = response._stringDecoder, row = "", i = 0; i < buffer.length; i++)row += stringDecoder.decode(buffer[i], decoderOptions);
        row += stringDecoder.decode(chunk);
        processFullStringRow(response, streamState, id, tag, row);
    }
    function processFullStringRow(response, streamState, id, tag, row) {
        switch(tag){
            case 73:
                resolveModule(response, id, row, streamState);
                break;
            case 72:
                id = row[0];
                streamState = row.slice(1);
                response = parseModel(response, streamState);
                streamState = ReactDOMSharedInternals.d;
                switch(id){
                    case "D":
                        streamState.D(response);
                        break;
                    case "C":
                        "string" === typeof response ? streamState.C(response) : streamState.C(response[0], response[1]);
                        break;
                    case "L":
                        id = response[0];
                        row = response[1];
                        3 === response.length ? streamState.L(id, row, response[2]) : streamState.L(id, row);
                        break;
                    case "m":
                        "string" === typeof response ? streamState.m(response) : streamState.m(response[0], response[1]);
                        break;
                    case "X":
                        "string" === typeof response ? streamState.X(response) : streamState.X(response[0], response[1]);
                        break;
                    case "S":
                        "string" === typeof response ? streamState.S(response) : streamState.S(response[0], 0 === response[1] ? void 0 : response[1], 3 === response.length ? response[2] : void 0);
                        break;
                    case "M":
                        "string" === typeof response ? streamState.M(response) : streamState.M(response[0], response[1]);
                }
                break;
            case 69:
                tag = response._chunks;
                var chunk = tag.get(id);
                row = JSON.parse(row);
                var error = resolveErrorDev(response, row);
                error.digest = row.digest;
                chunk ? (resolveChunkDebugInfo(response, streamState, chunk), triggerErrorOnChunk(response, chunk, error)) : (row = new ReactPromise("rejected", null, error), resolveChunkDebugInfo(response, streamState, row), tag.set(id, row));
                break;
            case 84:
                tag = response._chunks;
                (chunk = tag.get(id)) && "pending" !== chunk.status ? chunk.reason.enqueueValue(row) : (chunk && releasePendingChunk(response, chunk), row = new ReactPromise("fulfilled", row, null), resolveChunkDebugInfo(response, streamState, row), tag.set(id, row));
                break;
            case 78:
                response._timeOrigin = +row - performance.timeOrigin;
                break;
            case 68:
                id = getChunk(response, id);
                "fulfilled" !== id.status && "rejected" !== id.status && "halted" !== id.status && "blocked" !== id.status && "resolved_module" !== id.status && (streamState = id._debugChunk, tag = createResolvedModelChunk(response, row), tag._debugChunk = streamState, id._debugChunk = tag, initializeDebugChunk(response, id), "blocked" !== tag.status || void 0 !== response._debugChannel && response._debugChannel.hasReadable || '"' !== row[0] || "$" !== row[1] || (streamState = row.slice(2, row.length - 1).split(":"), streamState = parseInt(streamState[0], 16), "pending" === getChunk(response, streamState).status && (id._debugChunk = null)));
                break;
            case 74:
                resolveIOInfo(response, id, row);
                break;
            case 87:
                resolveConsoleEntry(response, row);
                break;
            case 82:
                startReadableStream(response, id, void 0, streamState);
                break;
            case 114:
                startReadableStream(response, id, "bytes", streamState);
                break;
            case 88:
                startAsyncIterable(response, id, !1, streamState);
                break;
            case 120:
                startAsyncIterable(response, id, !0, streamState);
                break;
            case 67:
                (id = response._chunks.get(id)) && "fulfilled" === id.status && (0 === --response._pendingChunks && (response._weakResponse.response = null), id.reason.close("" === row ? '"$undefined"' : row));
                break;
            default:
                if ("" === row) {
                    if (streamState = response._chunks, (row = streamState.get(id)) || streamState.set(id, row = createPendingChunk(response)), "pending" === row.status || "blocked" === row.status) releasePendingChunk(response, row), response = row, response.status = "halted", response.value = null, response.reason = null;
                } else tag = response._chunks, (chunk = tag.get(id)) ? (resolveChunkDebugInfo(response, streamState, chunk), resolveModelChunk(response, chunk, row)) : (row = createResolvedModelChunk(response, row), resolveChunkDebugInfo(response, streamState, row), tag.set(id, row));
        }
    }
    function processBinaryChunk(weakResponse, streamState, chunk) {
        if (!hasGCedResponse(weakResponse)) {
            weakResponse = unwrapWeakResponse(weakResponse);
            var i = 0, rowState = streamState._rowState, rowID = streamState._rowID, rowTag = streamState._rowTag, rowLength = streamState._rowLength, buffer = streamState._buffer, chunkLength = chunk.length;
            for(incrementChunkDebugInfo(streamState, chunkLength); i < chunkLength;){
                var lastIdx = -1;
                switch(rowState){
                    case 0:
                        lastIdx = chunk[i++];
                        58 === lastIdx ? rowState = 1 : rowID = rowID << 4 | (96 < lastIdx ? lastIdx - 87 : lastIdx - 48);
                        continue;
                    case 1:
                        rowState = chunk[i];
                        84 === rowState || 65 === rowState || 79 === rowState || 111 === rowState || 98 === rowState || 85 === rowState || 83 === rowState || 115 === rowState || 76 === rowState || 108 === rowState || 71 === rowState || 103 === rowState || 77 === rowState || 109 === rowState || 86 === rowState ? (rowTag = rowState, rowState = 2, i++) : 64 < rowState && 91 > rowState || 35 === rowState || 114 === rowState || 120 === rowState ? (rowTag = rowState, rowState = 3, i++) : (rowTag = 0, rowState = 3);
                        continue;
                    case 2:
                        lastIdx = chunk[i++];
                        44 === lastIdx ? rowState = 4 : rowLength = rowLength << 4 | (96 < lastIdx ? lastIdx - 87 : lastIdx - 48);
                        continue;
                    case 3:
                        lastIdx = chunk.indexOf(10, i);
                        break;
                    case 4:
                        lastIdx = i + rowLength, lastIdx > chunk.length && (lastIdx = -1);
                }
                var offset = chunk.byteOffset + i;
                if (-1 < lastIdx) rowLength = new Uint8Array(chunk.buffer, offset, lastIdx - i), 98 === rowTag ? resolveBuffer(weakResponse, rowID, lastIdx === chunkLength ? rowLength : rowLength.slice(), streamState) : processFullBinaryRow(weakResponse, streamState, rowID, rowTag, buffer, rowLength), i = lastIdx, 3 === rowState && i++, rowLength = rowID = rowTag = rowState = 0, buffer.length = 0;
                else {
                    chunk = new Uint8Array(chunk.buffer, offset, chunk.byteLength - i);
                    98 === rowTag ? (rowLength -= chunk.byteLength, resolveBuffer(weakResponse, rowID, chunk, streamState)) : (buffer.push(chunk), rowLength -= chunk.byteLength);
                    break;
                }
            }
            streamState._rowState = rowState;
            streamState._rowID = rowID;
            streamState._rowTag = rowTag;
            streamState._rowLength = rowLength;
        }
    }
    function parseModel(response, json) {
        json = JSON.parse(json);
        return reviveModel(response, json, {
            "": json
        }, "");
    }
    function reviveModel(response, value, parentObject, key) {
        if ("string" === typeof value) return "$" === value[0] ? parseModelString(response, parentObject, key, value) : value;
        if ("object" !== typeof value || null === value) return value;
        if (isArrayImpl(value)) {
            for(var i = 0; i < value.length; i++)value[i] = reviveModel(response, value[i], value, "" + i);
            if (value[0] === REACT_ELEMENT_TYPE) {
                if (value[0] === REACT_ELEMENT_TYPE) b: {
                    key = value[4];
                    parentObject = value[5];
                    i = value[6];
                    value = {
                        $$typeof: REACT_ELEMENT_TYPE,
                        type: value[1],
                        key: value[2],
                        props: value[3],
                        _owner: void 0 === key ? null : key
                    };
                    Object.defineProperty(value, "ref", {
                        enumerable: !1,
                        get: nullRefGetter
                    });
                    value._store = {};
                    Object.defineProperty(value._store, "validated", {
                        configurable: !1,
                        enumerable: !1,
                        writable: !0,
                        value: i
                    });
                    Object.defineProperty(value, "_debugInfo", {
                        configurable: !1,
                        enumerable: !1,
                        writable: !0,
                        value: null
                    });
                    Object.defineProperty(value, "_debugStack", {
                        configurable: !1,
                        enumerable: !1,
                        writable: !0,
                        value: void 0 === parentObject ? null : parentObject
                    });
                    Object.defineProperty(value, "_debugTask", {
                        configurable: !1,
                        enumerable: !1,
                        writable: !0,
                        value: null
                    });
                    if (null !== initializingHandler) {
                        key = initializingHandler;
                        initializingHandler = key.parent;
                        if (key.errored) {
                            parentObject = new ReactPromise("rejected", null, key.reason);
                            initializeElement(response, value, null);
                            response = {
                                name: getComponentNameFromType(value.type) || "",
                                owner: value._owner
                            };
                            response.debugStack = value._debugStack;
                            supportsCreateTask && (response.debugTask = value._debugTask);
                            parentObject._debugInfo = [
                                response
                            ];
                            response = createLazyChunkWrapper(parentObject, i);
                            break b;
                        }
                        if (0 < key.deps) {
                            parentObject = new ReactPromise("blocked", null, null);
                            key.value = value;
                            key.chunk = parentObject;
                            i = createLazyChunkWrapper(parentObject, i);
                            response = initializeElement.bind(null, response, value, i);
                            parentObject.then(response, response);
                            response = i;
                            break b;
                        }
                    }
                    initializeElement(response, value, null);
                    response = value;
                }
                else response = value;
                return response;
            }
            return value;
        }
        for(i in value)"__proto__" === i ? delete value[i] : (parentObject = reviveModel(response, value[i], value, i), void 0 !== parentObject ? value[i] = parentObject : delete value[i]);
        return value;
    }
    function close(weakResponse) {
        if (!hasGCedResponse(weakResponse)) {
            var response = unwrapWeakResponse(weakResponse);
            response._allowPartialStream ? (response._closed = !0, response._chunks.forEach(function(chunk) {
                "pending" === chunk.status ? (releasePendingChunk(response, chunk), chunk.status = "halted", chunk.value = null, chunk.reason = null) : "fulfilled" === chunk.status && null !== chunk.reason && chunk.reason.close('"$undefined"');
            }), weakResponse = response._debugChannel, void 0 !== weakResponse && (closeDebugChannel(weakResponse), response._debugChannel = void 0, null !== debugChannelRegistry && debugChannelRegistry.unregister(response))) : reportGlobalError(weakResponse, Error("Connection closed."));
        }
    }
    function noServerCall$1() {
        throw Error("Server Functions cannot be called during initial render. This would create a fetch waterfall. Try to use a Server Component to pass data to Client Components instead.");
    }
    function createResponseFromOptions(options) {
        return createResponse(options.serverConsumerManifest.moduleMap, options.serverConsumerManifest.serverModuleMap, options.serverConsumerManifest.moduleLoading, noServerCall$1, options.encodeFormAction, "string" === typeof options.nonce ? options.nonce : void 0, options && options.temporaryReferences ? options.temporaryReferences : void 0, options && options.unstable_allowPartialStream ? options.unstable_allowPartialStream : !1, options && options.findSourceMapURL ? options.findSourceMapURL : void 0, options ? !0 === options.replayConsoleLogs : !1, options && options.environmentName ? options.environmentName : void 0, options && null != options.startTime ? options.startTime : void 0, options && null != options.endTime ? options.endTime : void 0, options && void 0 !== options.debugChannel ? {
            hasReadable: void 0 !== options.debugChannel.readable,
            callback: null
        } : void 0);
    }
    function startReadingFromStream$1(response, stream, onDone, debugValue) {
        function progress(_ref) {
            var value = _ref.value;
            if (_ref.done) return onDone();
            processBinaryChunk(response, streamState, value);
            return reader.read().then(progress).catch(error);
        }
        function error(e) {
            reportGlobalError(response, e);
        }
        var streamState = createStreamState(response, debugValue), reader = stream.getReader();
        reader.read().then(progress).catch(error);
    }
    function noServerCall() {
        throw Error("Server Functions cannot be called during initial render. This would create a fetch waterfall. Try to use a Server Component to pass data to Client Components instead.");
    }
    function startReadingFromStream(response$jscomp$0, stream, onEnd) {
        var streamState = createStreamState(response$jscomp$0, stream);
        stream.on("data", function(chunk) {
            if ("string" === typeof chunk) {
                if (!hasGCedResponse(response$jscomp$0)) {
                    var response = unwrapWeakResponse(response$jscomp$0), i = 0, rowState = streamState._rowState, rowID = streamState._rowID, rowTag = streamState._rowTag, rowLength = streamState._rowLength, buffer = streamState._buffer, chunkLength = chunk.length;
                    for(incrementChunkDebugInfo(streamState, chunkLength); i < chunkLength;){
                        var lastIdx = -1;
                        switch(rowState){
                            case 0:
                                lastIdx = chunk.charCodeAt(i++);
                                58 === lastIdx ? rowState = 1 : rowID = rowID << 4 | (96 < lastIdx ? lastIdx - 87 : lastIdx - 48);
                                continue;
                            case 1:
                                rowState = chunk.charCodeAt(i);
                                84 === rowState || 65 === rowState || 79 === rowState || 111 === rowState || 85 === rowState || 83 === rowState || 115 === rowState || 76 === rowState || 108 === rowState || 71 === rowState || 103 === rowState || 77 === rowState || 109 === rowState || 86 === rowState ? (rowTag = rowState, rowState = 2, i++) : 64 < rowState && 91 > rowState || 114 === rowState || 120 === rowState ? (rowTag = rowState, rowState = 3, i++) : (rowTag = 0, rowState = 3);
                                continue;
                            case 2:
                                lastIdx = chunk.charCodeAt(i++);
                                44 === lastIdx ? rowState = 4 : rowLength = rowLength << 4 | (96 < lastIdx ? lastIdx - 87 : lastIdx - 48);
                                continue;
                            case 3:
                                lastIdx = chunk.indexOf("\n", i);
                                break;
                            case 4:
                                if (84 !== rowTag) throw Error("Binary RSC chunks cannot be encoded as strings. This is a bug in the wiring of the React streams.");
                                if (rowLength < chunk.length || chunk.length > 3 * rowLength) throw Error("String chunks need to be passed in their original shape. Not split into smaller string chunks. This is a bug in the wiring of the React streams.");
                                lastIdx = chunk.length;
                        }
                        if (-1 < lastIdx) {
                            if (0 < buffer.length) throw Error("String chunks need to be passed in their original shape. Not split into smaller string chunks. This is a bug in the wiring of the React streams.");
                            i = chunk.slice(i, lastIdx);
                            processFullStringRow(response, streamState, rowID, rowTag, i);
                            i = lastIdx;
                            3 === rowState && i++;
                            rowLength = rowID = rowTag = rowState = 0;
                            buffer.length = 0;
                        } else if (chunk.length !== i) throw Error("String chunks need to be passed in their original shape. Not split into smaller string chunks. This is a bug in the wiring of the React streams.");
                    }
                    streamState._rowState = rowState;
                    streamState._rowID = rowID;
                    streamState._rowTag = rowTag;
                    streamState._rowLength = rowLength;
                }
            } else processBinaryChunk(response$jscomp$0, streamState, chunk);
        });
        stream.on("error", function(error) {
            reportGlobalError(response$jscomp$0, error);
        });
        stream.on("end", onEnd);
    }
    var util = __turbopack_context__.r("[externals]/util [external] (util, cjs)"), ReactDOM = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/server/route-modules/app-page/vendored/rsc/react-dom.js [app-rsc] (ecmascript)"), React = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/server/route-modules/app-page/vendored/rsc/react.js [app-rsc] (ecmascript)"), decoderOptions = {
        stream: !0
    }, bind$1 = Function.prototype.bind, hasConfirmedEval = !1, hasOwnProperty = Object.prototype.hasOwnProperty, instrumentedChunks = new WeakSet(), loadedChunks = new WeakSet(), ReactDOMSharedInternals = ReactDOM.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE, REACT_ELEMENT_TYPE = Symbol.for("react.transitional.element"), REACT_PORTAL_TYPE = Symbol.for("react.portal"), REACT_FRAGMENT_TYPE = Symbol.for("react.fragment"), REACT_STRICT_MODE_TYPE = Symbol.for("react.strict_mode"), REACT_PROFILER_TYPE = Symbol.for("react.profiler"), REACT_CONSUMER_TYPE = Symbol.for("react.consumer"), REACT_CONTEXT_TYPE = Symbol.for("react.context"), REACT_FORWARD_REF_TYPE = Symbol.for("react.forward_ref"), REACT_SUSPENSE_TYPE = Symbol.for("react.suspense"), REACT_SUSPENSE_LIST_TYPE = Symbol.for("react.suspense_list"), REACT_MEMO_TYPE = Symbol.for("react.memo"), REACT_LAZY_TYPE = Symbol.for("react.lazy"), REACT_ACTIVITY_TYPE = Symbol.for("react.activity"), REACT_VIEW_TRANSITION_TYPE = Symbol.for("react.view_transition"), MAYBE_ITERATOR_SYMBOL = Symbol.iterator, ASYNC_ITERATOR = Symbol.asyncIterator, isArrayImpl = Array.isArray, getPrototypeOf = Object.getPrototypeOf, jsxPropsParents = new WeakMap(), jsxChildrenParents = new WeakMap(), CLIENT_REFERENCE_TAG = Symbol.for("react.client.reference"), ObjectPrototype = Object.prototype, knownServerReferences = new WeakMap(), boundCache = new WeakMap(), fakeServerFunctionIdx = 0, FunctionBind = Function.prototype.bind, ArraySlice = Array.prototype.slice, v8FrameRegExp = /^ {3} at (?:(.+) \((.+):(\d+):(\d+)\)|(?:async )?(.+):(\d+):(\d+))$/, jscSpiderMonkeyFrameRegExp = /(?:(.*)@)?(.*):(\d+):(\d+)/, REACT_CLIENT_REFERENCE = Symbol.for("react.client.reference"), supportsUserTiming = "undefined" !== typeof console && "function" === typeof console.timeStamp && "undefined" !== typeof performance && "function" === typeof performance.measure, trackNames = "Primary Parallel Parallel\u200b Parallel\u200b\u200b Parallel\u200b\u200b\u200b Parallel\u200b\u200b\u200b\u200b Parallel\u200b\u200b\u200b\u200b\u200b Parallel\u200b\u200b\u200b\u200b\u200b\u200b Parallel\u200b\u200b\u200b\u200b\u200b\u200b\u200b Parallel\u200b\u200b\u200b\u200b\u200b\u200b\u200b\u200b".split(" "), prefix, suffix;
    new ("function" === typeof WeakMap ? WeakMap : Map)();
    var ReactSharedInteralsServer = React.__SERVER_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE, ReactSharedInternals = React.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE || ReactSharedInteralsServer;
    ReactPromise.prototype = Object.create(Promise.prototype);
    ReactPromise.prototype.then = function(resolve, reject) {
        var _this = this;
        switch(this.status){
            case "resolved_model":
                initializeModelChunk(this);
                break;
            case "resolved_module":
                initializeModuleChunk(this);
        }
        var resolveCallback = resolve, rejectCallback = reject, wrapperPromise = new Promise(function(res, rej) {
            resolve = function(value) {
                wrapperPromise._debugInfo = _this._debugInfo;
                res(value);
            };
            reject = function(reason) {
                wrapperPromise._debugInfo = _this._debugInfo;
                rej(reason);
            };
        });
        wrapperPromise.then(resolveCallback, rejectCallback);
        switch(this.status){
            case "fulfilled":
                "function" === typeof resolve && resolve(this.value);
                break;
            case "pending":
            case "blocked":
                "function" === typeof resolve && (null === this.value && (this.value = []), this.value.push(resolve));
                "function" === typeof reject && (null === this.reason && (this.reason = []), this.reason.push(reject));
                break;
            case "halted":
                break;
            default:
                "function" === typeof reject && reject(this.reason);
        }
    };
    var debugChannelRegistry = "function" === typeof FinalizationRegistry ? new FinalizationRegistry(closeDebugChannel) : null, initializingHandler = null, initializingChunk = null, isInitializingDebugInfo = !1, mightHaveStaticConstructor = /\bclass\b.*\bstatic\b/, MIN_CHUNK_SIZE = 65536, supportsCreateTask = !!console.createTask, fakeFunctionCache = new Map(), fakeFunctionIdx = 0, createFakeJSXCallStack = {
        react_stack_bottom_frame: function(response, stack, environmentName) {
            return buildFakeCallStack(response, stack, environmentName, !1, fakeJSXCallSite)();
        }
    }, createFakeJSXCallStackInDEV = createFakeJSXCallStack.react_stack_bottom_frame.bind(createFakeJSXCallStack), currentOwnerInDEV = null, replayConsoleWithCallStack = {
        react_stack_bottom_frame: function(response, payload) {
            var methodName = payload[0], stackTrace = payload[1], owner = payload[2], env = payload[3];
            payload = payload.slice(4);
            var prevStack = ReactSharedInternals.getCurrentStack;
            ReactSharedInternals.getCurrentStack = getCurrentStackInDEV;
            currentOwnerInDEV = null === owner ? response._debugRootOwner : owner;
            try {
                a: {
                    var offset = 0;
                    switch(methodName){
                        case "dir":
                        case "dirxml":
                        case "groupEnd":
                        case "table":
                            var JSCompiler_inline_result = bind$1.apply(console[methodName], [
                                console
                            ].concat(payload));
                            break a;
                        case "assert":
                            offset = 1;
                    }
                    var newArgs = payload.slice(0);
                    "string" === typeof newArgs[offset] ? newArgs.splice(offset, 1, "\u001b[0m\u001b[7m%c%s\u001b[0m%c " + newArgs[offset], "background: #e6e6e6;background: light-dark(rgba(0,0,0,0.1), rgba(255,255,255,0.25));color: #000000;color: light-dark(#000000, #ffffff);border-radius: 2px", " " + env + " ", "") : newArgs.splice(offset, 0, "\u001b[0m\u001b[7m%c%s\u001b[0m%c", "background: #e6e6e6;background: light-dark(rgba(0,0,0,0.1), rgba(255,255,255,0.25));color: #000000;color: light-dark(#000000, #ffffff);border-radius: 2px", " " + env + " ", "");
                    newArgs.unshift(console);
                    JSCompiler_inline_result = bind$1.apply(console[methodName], newArgs);
                }
                var callStack = buildFakeCallStack(response, stackTrace, env, !1, JSCompiler_inline_result);
                if (null != owner) {
                    var task = initializeFakeTask(response, owner);
                    initializeFakeStack(response, owner);
                    if (null !== task) {
                        task.run(callStack);
                        return;
                    }
                }
                var rootTask = getRootTask(response, env);
                null != rootTask ? rootTask.run(callStack) : callStack();
            } finally{
                currentOwnerInDEV = null, ReactSharedInternals.getCurrentStack = prevStack;
            }
        }
    }, replayConsoleWithCallStackInDEV = replayConsoleWithCallStack.react_stack_bottom_frame.bind(replayConsoleWithCallStack);
    exports.createFromFetch = function(promiseForResponse, options) {
        var response = createResponseFromOptions(options);
        promiseForResponse.then(function(r) {
            if (options && options.debugChannel && options.debugChannel.readable) {
                var streamDoneCount = 0, handleDone = function() {
                    2 === ++streamDoneCount && close(response);
                };
                startReadingFromStream$1(response, options.debugChannel.readable, handleDone);
                startReadingFromStream$1(response, r.body, handleDone, r);
            } else startReadingFromStream$1(response, r.body, close.bind(null, response), r);
        }, function(e) {
            reportGlobalError(response, e);
        });
        return getRoot(response);
    };
    exports.createFromNodeStream = function(stream, serverConsumerManifest, options) {
        var response = createResponse(serverConsumerManifest.moduleMap, serverConsumerManifest.serverModuleMap, serverConsumerManifest.moduleLoading, noServerCall, options ? options.encodeFormAction : void 0, options && "string" === typeof options.nonce ? options.nonce : void 0, void 0, options && options.unstable_allowPartialStream ? options.unstable_allowPartialStream : !1, options && options.findSourceMapURL ? options.findSourceMapURL : void 0, options ? !0 === options.replayConsoleLogs : !1, options && options.environmentName ? options.environmentName : void 0, options && null != options.startTime ? options.startTime : void 0, options && null != options.endTime ? options.endTime : void 0, options && void 0 !== options.debugChannel ? {
            hasReadable: !0,
            callback: null
        } : void 0);
        if (options && options.debugChannel) {
            var streamEndedCount = 0;
            serverConsumerManifest = function() {
                2 === ++streamEndedCount && close(response);
            };
            startReadingFromStream(response, options.debugChannel, serverConsumerManifest);
            startReadingFromStream(response, stream, serverConsumerManifest);
        } else startReadingFromStream(response, stream, close.bind(null, response));
        return getRoot(response);
    };
    exports.createFromReadableStream = function(stream, options) {
        var response = createResponseFromOptions(options);
        if (options && options.debugChannel && options.debugChannel.readable) {
            var streamDoneCount = 0, handleDone = function() {
                2 === ++streamDoneCount && close(response);
            };
            startReadingFromStream$1(response, options.debugChannel.readable, handleDone);
            startReadingFromStream$1(response, stream, handleDone, stream);
        } else startReadingFromStream$1(response, stream, close.bind(null, response), stream);
        return getRoot(response);
    };
    exports.createServerReference = function(id) {
        return createServerReference$1(id, noServerCall$1);
    };
    exports.createTemporaryReferenceSet = function() {
        return new Map();
    };
    exports.encodeReply = function(value, options) {
        return new Promise(function(resolve, reject) {
            var abort = processReply(value, "", options && options.temporaryReferences ? options.temporaryReferences : void 0, resolve, reject);
            if (options && options.signal) {
                var signal = options.signal;
                if (signal.aborted) abort(signal.reason);
                else {
                    var listener = function() {
                        abort(signal.reason);
                        signal.removeEventListener("abort", listener);
                    };
                    signal.addEventListener("abort", listener);
                }
            }
        });
    };
    exports.registerServerReference = function(reference, id, encodeFormAction) {
        registerBoundServerReference(reference, id, null, encodeFormAction);
        return reference;
    };
}();
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-server-dom-turbopack/client.node.js [app-rsc] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
;
else {
    module.exports = __turbopack_context__.r("[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/react-server-dom-turbopack/cjs/react-server-dom-turbopack-client.node.development.js [app-rsc] (ecmascript)");
}
}),
"[project]/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/string-hash/index.js [app-rsc] (ecmascript)", ((__turbopack_context__, module, exports) => {

(()=>{
    "use strict";
    var e = {
        328: (e)=>{
            function hash(e) {
                var r = 5381, _ = e.length;
                while(_){
                    r = r * 33 ^ e.charCodeAt(--_);
                }
                return r >>> 0;
            }
            e.exports = hash;
        }
    };
    var r = {};
    function __nccwpck_require__(_) {
        var a = r[_];
        if (a !== undefined) {
            return a.exports;
        }
        var t = r[_] = {
            exports: {}
        };
        var i = true;
        try {
            e[_](t, t.exports, __nccwpck_require__);
            i = false;
        } finally{
            if (i) delete r[_];
        }
        return t.exports;
    }
    if (typeof __nccwpck_require__ !== "undefined") __nccwpck_require__.ab = ("TURBOPACK compile-time value", "/ROOT/node_modules/.pnpm/next@16.2.6_react-dom@19.2.6_react@19.2.6__react@19.2.6/node_modules/next/dist/compiled/string-hash") + "/";
    var _ = __nccwpck_require__(328);
    module.exports = _;
})();
}),
];

//# sourceMappingURL=08c5_next_dist_compiled_0q92v_o._.js.map