// setup_env.js

// 这里不再需要 const fs = require('fs'); 和 const vm = require('vm');

function get_enviroment(proxy_array, context) {
    // ... (这个函数保持不变)
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

const meta1 = { id: "9DhefwqGPrzGxEp9hPaoag", content: '', parentNode:{ removeChild: function(element) {} } };
const i1 = {length: 0};
const div1 = { getElementsByTagName: function(tagName) { if (tagName === 'i'){ return i1; } } };
const script1 = { "0": {}, "1": {} };
const document = {};
document.getElementById = function(tagName) { if (tagName === "9DhefwqGPrzGxEp9hPaoag") { return meta1; } };
document.createElement = function(tagName) { if (tagName === "div"){ return div1; } };
document.getElementsByTagName = function(tagName) {if (tagName === 'script'){return script1;} };
const storageMock = {
    _data: {},
    getItem: function(key) { return this._data[key] || null; },
    setItem: function(key, value) { this._data[key] = value.toString(); },
    removeItem: function(key) { delete this._data[key]; },
    clear: function() { this._data = {}; }
};
document.addEventListener = function(event, callback) {};
document.documentElement = {};

const context = {
    document: document,
    navigator: { userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', appCodeName: "Mozilla", appName: "Netscape", appVersion: "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36", platform: 'Win32', language: 'zh-CN', languages: ['zh-CN', 'zh'] },
    location: { "href": "https://www.cde.org.cn/main/news/listpage/1e0a362d64015ebcbf32d6949acbba11", "origin": "https://www.cde.org.cn", "protocol": "https:", "host": "www.cde.org.cn" },
    screen: { width: 1920, height: 1080 },
    console: { log: function() {} },
    Math: Math, Date: Date, Array: Array, Object: Object, setTimeout: function (){}, setInterval: function (){}, escape: escape, unescape: unescape, encodeURIComponent: encodeURIComponent, decodeURIComponent: decodeURIComponent, parseInt: parseInt, isNaN: isNaN, JSON: JSON,
    localStorage: storageMock, sessionStorage: storageMock,
    addEventListener: function(event, callback) {},
};

// 将所有环境对象挂载到全局作用域 (this)
Object.assign(this, context);
this.window = this;
this.window.top = this.window;

const proxy_array = ['window', 'document', 'navigator', 'location'];
get_enviroment(proxy_array, this);

this.eval = eval;
