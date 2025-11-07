// setup_env2.js

function get_enviroment(proxy_array, context) {
    for(var i=0; i<proxy_array.length; i++){
        let objName = proxy_array[i];
        let handler = {
            get: function(target, property, receiver) { return Reflect.get(...arguments); },
            set: function(target, property, value, receiver) { return Reflect.set(...arguments); }
        };
        if (context[objName]) {
            context[objName] = new Proxy(context[objName], handler);
        } else {
            context[objName] = new Proxy({}, handler);
        }
    }
}

const meta1 = {
    id: "9DhefwqGPrzGxEp9hPaoag",
    content: '',
    parentNode: {
        removeChild: function(element) {
            console.log("removeChild called", element);
        }
    }
};

const i1 = {length: 0};
const div1 = {
    getElementsByTagName: function(tagName) {
        if (tagName === 'i'){ return i1; }
        console.log("getElementsByTagName", tagName);
    }
};

const script1 = {
    "0": {},
    "1": {}
};

const a1 = {
    href: "/main/news/getHotNewsList",
    protocol: "https:",
    host: "www.cde.org.cn",
    pathname: "/main/news/getHotNewsList",
    port: '',
    hostname: "www.cde.org.cn",
    search: "",
    hash: "",
};

const document = {};
document.getElementById = function(tagName) {
    if (tagName === "9DhefwqGPrzGxEp9hPaoag") { return meta1; }
    console.log("getElementById", tagName);
};
document.createElement = function(tagName) {
    if (tagName === "div"){ return div1; }
    if (tagName === "a"){ return a1; }
    console.log("createElement", tagName);
};
document.getElementsByTagName = function(tagName) {
    if (tagName === 'script'){return script1;}
    console.log("getElementsByTagName", tagName);
};
document.cookie = 'FSSBBIl1UgzbN7N80T=3X1UOJpEigdcBOpVi3e8cmHm.uZDZs3ni8N_CuB2q2b57etjDerXnU721myoRcUjxonVgUP4uuwuYiT3fMKlOPmntqWfbtmK837wcOmqB3MmV4tDyYNtcUJ9Fk4hu9NSKxpq0wrsBCnfemhweClK3ItyKFaCjulGxrJ0LSP2PQzf2i45vLVakiz2n5MZWJm1XQp.1tJZ_BV8IXEwtUov6t0RI';

const storageMock = {
    getItem: function(key) { return this[key] || null; },
    setItem: function(key, value) { this[key] = value.toString(); },
    removeItem: function(key) { delete this[key]; },
    clear: function() { for (var key in this) { delete this[key]; } }
};

document.addEventListener = function(event, callback) {
    console.log(`document.addEventListener called for event: ${event}`);
};

// ============= XMLHttpRequest =============
// 🔥 关键修改：在外部声明 req_param
var req_param = undefined;

const XMLHttpRequest = function() {};

XMLHttpRequest.prototype.open = function(method, url, args) {
    console.log('XMLHttpRequest.open:', method, url);
    req_param = url;  // 🔥 直接赋值给外部变量
    return {};
};

const context = {
    document: document,
    navigator: {
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        appCodeName: "Mozilla",
        appName: "Netscape",
        appVersion: "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        platform: 'Win32',
        language: 'zh-CN',
        languages: ['zh-CN', 'zh'],
    },
    location: {
        "ancestorOrigins": {},
        "href": "https://www.cde.org.cn/main/news/listpage/1e0a362d64015ebcbf32d6949acbba11",
        "origin": "https://www.cde.org.cn",
        "protocol": "https:",
        "host": "www.cde.org.cn",
        "hostname": "www.cde.org.cn",
        "port": "",
        "pathname": "/main/news/listpage/1e0a362d64015ebcbf32d6949acbba11",
        "search": "",
        "hash": "",
        reload: function() {
            console.log('location.reload called');
        },
    },
    screen: {
        width: 1920,
        height: 1080,
        availWidth: 1920,
        availHeight: 1040,
        colorDepth: 24,
        pixelDepth: 24,
    },
    console: console,
    Math: Math,
    Date: Date,
    Array: Array,
    Object: Object,
    Function: Function,
    Error: Error,
    String: String,
    Number: Number,
    RegExp: RegExp,
    parseInt: parseInt,
    unescape: unescape,
    encodeURIComponent: encodeURIComponent,
    setTimeout: function (){},
    setInterval: function (){},
    escape: escape,
    decodeURIComponent: decodeURIComponent,
    isNaN: isNaN,
    JSON: JSON,
    localStorage: storageMock,
    sessionStorage: storageMock,
    XMLHttpRequest: XMLHttpRequest,
    addEventListener: function(event, callback) {
        console.log(`window.addEventListener called for event: ${event}`);
    },
};

Object.assign(this, context);
this.window = this;
this.window.top = this.window;

// 🔥 关键：暴露到全局
this.meta1 = meta1;
this.req_param = req_param;  // 暴露外部的 req_param

const proxy_array = ['window', 'document', 'navigator', 'location'];
get_enviroment(proxy_array, this);

this.eval = eval;
