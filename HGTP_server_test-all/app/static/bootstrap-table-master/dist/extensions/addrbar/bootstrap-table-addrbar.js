(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define([], factory);
  } else if (typeof exports !== "undefined") {
    factory();
  } else {
    var mod = {
      exports: {}
    };
    factory();
    global.bootstrapTableAddrbar = mod.exports;
  }
})(this, function () {
  'use strict';

  function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) {
      throw new TypeError("Cannot call a class as a function");
    }
  }

  var _createClass = function () {
    function defineProperties(target, props) {
      for (var i = 0; i < props.length; i++) {
        var descriptor = props[i];
        descriptor.enumerable = descriptor.enumerable || false;
        descriptor.configurable = true;
        if ("value" in descriptor) descriptor.writable = true;
        Object.defineProperty(target, descriptor.key, descriptor);
      }
    }

    return function (Constructor, protoProps, staticProps) {
      if (protoProps) defineProperties(Constructor.prototype, protoProps);
      if (staticProps) defineProperties(Constructor, staticProps);
      return Constructor;
    };
  }();

  function _possibleConstructorReturn(self, call) {
    if (!self) {
      throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
    }

    return call && (typeof call === "object" || typeof call === "function") ? call : self;
  }

  var _get = function get(object, property, receiver) {
    if (object === null) object = Function.prototype;
    var desc = Object.getOwnPropertyDescriptor(object, property);

    if (desc === undefined) {
      var parent = Object.getPrototypeOf(object);

      if (parent === null) {
        return undefined;
      } else {
        return get(parent, property, receiver);
      }
    } else if ("value" in desc) {
      return desc.value;
    } else {
      var getter = desc.get;

      if (getter === undefined) {
        return undefined;
      }

      return getter.call(receiver);
    }
  };

  function _inherits(subClass, superClass) {
    if (typeof superClass !== "function" && superClass !== null) {
      throw new TypeError("Super expression must either be null or a function, not " + typeof superClass);
    }

    subClass.prototype = Object.create(superClass && superClass.prototype, {
      constructor: {
        value: subClass,
        enumerable: false,
        writable: true,
        configurable: true
      }
    });
    if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
  }

  var _slicedToArray = function () {
    function sliceIterator(arr, i) {
      var _arr = [];
      var _n = true;
      var _d = false;
      var _e = undefined;

      try {
        for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) {
          _arr.push(_s.value);

          if (i && _arr.length === i) break;
        }
      } catch (err) {
        _d = true;
        _e = err;
      } finally {
        try {
          if (!_n && _i["return"]) _i["return"]();
        } finally {
          if (_d) throw _e;
        }
      }

      return _arr;
    }

    return function (arr, i) {
      if (Array.isArray(arr)) {
        return arr;
      } else if (Symbol.iterator in Object(arr)) {
        return sliceIterator(arr, i);
      } else {
        throw new TypeError("Invalid attempt to destructure non-iterable instance");
      }
    };
  }();

  /**
   * @author: general
   * @website: note.generals.space
   * @email: generals.space@gmail.com
   * @github: https://github.com/generals-space/bootstrap-table-addrbar
   * @update: zhixin wen <wenzhixin2010@gmail.com>
   */

  (function ($) {
    /*
       * function: ??????????????????????????????????????????.
       * key: ?????????
       * url: ????????????????????????
       */
    function _GET(key) {
      var url = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : window.location.search;

      /*
       * ??????????????????????????????????????????
       * (^|&)key??????: ?????????key????????????&key??????????????????
       * ??????(&|$)?????????&????????????????????????????????????
       * ...??????, ???????????????????????????.
       */
      var reg = new RegExp('(^|&)' + key + '=([^&]*)(&|$)');
      var result = url.substr(1).match(reg);

      if (result) {
        return decodeURIComponent(result[2]);
      }
      return null;
    }

    /*
      * function: ????????????????????????url??????
      * var dic = {name: 'genreal', age: 24}
      * var url = 'https://www.baidu.com?age=22';
      * _buildUrl(dic, url);
      * ?????????"https://www.baidu.com?age=24&name=genreal"
      * ???, ?????????????????????...
      *
      * ??????: ?????????????????????URLSearchParams??????, ?????????????????????.
      * ??????????????????, ???????????????????????????.
      */

    function _buildUrl(dict) {
      var url = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : window.location.search;
      var _iteratorNormalCompletion = true;
      var _didIteratorError = false;
      var _iteratorError = undefined;

      try {
        for (var _iterator = Object.entries(dict)[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
          var _ref = _step.value;

          var _ref2 = _slicedToArray(_ref, 2);

          var key = _ref2[0];
          var val = _ref2[1];

          // ??????name=general????????????????????????(&????????????)
          var pattern = key + '=([^&]*)';
          var targetStr = key + '=' + val;

          /*
           * ????????????url????????????key???, ??????????????????????????????????????????val
           * ???????????????????????????.
           */
          if (url.match(pattern)) {
            var tmp = new RegExp('(' + key + '=)([^&]*)', 'gi');
            url = url.replace(tmp, targetStr);
          } else {
            var seperator = url.match('[?]') ? '&' : '?';
            url = url + seperator + targetStr;
          }
        }
      } catch (err) {
        _didIteratorError = true;
        _iteratorError = err;
      } finally {
        try {
          if (!_iteratorNormalCompletion && _iterator.return) {
            _iterator.return();
          }
        } finally {
          if (_didIteratorError) {
            throw _iteratorError;
          }
        }
      }

      return url;
    }

    $.BootstrapTable = function (_$$BootstrapTable) {
      _inherits(_class, _$$BootstrapTable);

      function _class() {
        _classCallCheck(this, _class);

        return _possibleConstructorReturn(this, (_class.__proto__ || Object.getPrototypeOf(_class)).apply(this, arguments));
      }

      _createClass(_class, [{
        key: 'init',
        value: function init() {
          var _this2 = this;

          // ??????addrbar?????????????????????true?????????????????????
          if (this.options.addrbar) {
            // ?????????, ?????????????????????
            this.addrbarInit = true;
            var _prefix = this.options.addrPrefix || '';

            // ???????????????: ????????????????????????, ??????????????????????????????, ??????????????????????????????
            this.options.pageSize = this.options.pageSize || (_GET(_prefix + 'limit') ? parseInt(_GET(_prefix + 'limit')) : $.BootstrapTable.DEFAULTS.pageSize);
            this.options.pageNumber = this.options.pageNumber || (_GET(_prefix + 'page') ? parseInt(_GET(_prefix + 'page')) : $.BootstrapTable.DEFAULTS.pageNumber);
            this.options.sortOrder = this.options.sortOrder || (_GET(_prefix + 'order') ? _GET(_prefix + 'order') : $.BootstrapTable.DEFAULTS.sortOrder);
            this.options.sortName = this.options.sortName || (_GET(_prefix + 'sort') ? _GET(_prefix + 'sort') : 'id');
            this.options.searchText = this.options.searchText || (_GET(_prefix + 'search') ? _GET(_prefix + 'search') : $.BootstrapTable.DEFAULTS.searchText);

            var _onLoadSuccess = this.options.onLoadSuccess;

            this.options.onLoadSuccess = function (data) {
              if (_this2.addrbarInit) {
                _this2.addrbarInit = false;
              } else {
                var params = {};
                params[_prefix + 'page'] = _this2.options.pageNumber, params[_prefix + 'limit'] = _this2.options.pageSize, params[_prefix + 'order'] = _this2.options.sortOrder, params[_prefix + 'sort'] = _this2.options.sortName, params[_prefix + 'search'] = _this2.options.searchText;
                // h5??????????????????????????????????????????
                window.history.pushState({}, '', _buildUrl(params));
              }

              if (_onLoadSuccess) {
                _onLoadSuccess.call(_this2, data);
              }
            };
          }
          _get(_class.prototype.__proto__ || Object.getPrototypeOf(_class.prototype), 'init', this).call(this);
        }
      }]);

      return _class;
    }($.BootstrapTable);
  })(jQuery);
});