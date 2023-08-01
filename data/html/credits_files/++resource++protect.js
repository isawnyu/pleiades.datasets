/* jshint undef: true, unused: true */
/* globals tinymce, jQuery, kukit */

"use strict";

var script = document.getElementById('protect-script');

if(script){
  var base_url = script.getAttribute('data-site-url');
  var token = script.getAttribute('data-token');

  if(window.jQuery !== undefined){
    jQuery.ajaxSetup({
      beforeSend: function (xhr, options){
        if(options === undefined){
          return;
        }
        if(!options.url){
          return;
        }
        if(options.url.indexOf('_authenticator') !== -1){
          return;
        }
        if(options.url.indexOf(base_url) === 0 || options.url.indexOf('//') === -1){
          // only urls that start with the site url
          // Extra compared to plone4.csrffixes: also for relative urls, like @@my-view.
          xhr.setRequestHeader("X-CSRF-TOKEN", token);
        }
      }
    });
  }
  if(window.tinymce && window.tinymce.util.XHR._send === undefined){
    window.tinymce.util.XHR._send = window.tinymce.util.XHR.send;
    var xhr = window.tinymce.util.XHR;
    var _send = xhr.send;
    window.tinymce.util.XHR.send = function(){
      var args = Array.prototype.slice.call(arguments);
      if(args[0]){
        var config = args[0];
        if(config.data && typeof(config.data) === 'string' &&
            config.url && config.url.indexOf(base_url) === 0){
          config.data = config.data + '&_authenticator=' + token;
        }
      }
     _send.apply(xhr, args);
    };
  }
  if(window.kukit && window.kukit.sa){
    kukit.sa.ServerAction.prototype.reallyNotifyServer = function() {
      // make a deferred callback
      var domDoc = new XMLHttpRequest();
      var self = this;
      var notifyServer_done  = function() {
          self.notifyServer_done(domDoc);
      };
      // convert params
      var query = new kukit.fo.FormQuery();
      for (var key in this.oper.parms) {
          query.appendElem(key, this.oper.parms[key]);
      }
      // also add the parms that result from submitting an entire form.
      // This is, unlike the normal parms, is a list. Keys and values are
      // added at the end of the query, without mangling names.
      var submitForm = this.oper.kssParms.kssSubmitForm;
      if (submitForm) {
          for (var i=0; i<submitForm.length; i++) {
              var item = submitForm[i];
              query.appendElem(item[0], item[1]);
          }
      }
      query.appendElem('_authenticator', token);
      // encode the query
      var encoded = query.encode();
      // sending form
      var ts = new Date().getTime();
      //kukit.logDebug('TS: '+ts);
      var tsurl = this.url + "?kukitTimeStamp=" + ts;
      domDoc.open("POST", tsurl, true);
      domDoc.onreadystatechange = notifyServer_done;
      domDoc.setRequestHeader("Content-Type",
          "application/x-www-form-urlencoded");
      domDoc.send(encoded);
    };
  }
}
