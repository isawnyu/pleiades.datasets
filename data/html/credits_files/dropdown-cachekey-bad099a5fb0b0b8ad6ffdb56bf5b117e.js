
/* Merged Plone Javascript file
 * This file is dynamically assembled from separate parts.
 * Some of these parts have 3rd party licenses or copyright information attached
 * Such information is valid for that section,
 * not for the entire composite file
 * originating files are separated by - filename.js -
 */

/* - dropdown.js - */
// https://pleiades.stoa.org/portal_javascripts/dropdown.js?original=1
function hideAllMenus(){jQuery('dl.actionMenu').removeClass('activated').addClass('deactivated')}
function toggleMenuHandler(event){jQuery(this).parents('.actionMenu:first').toggleClass('deactivated').toggleClass('activated');return false}
function actionMenuDocumentMouseDown(event){if(jQuery(event.target).parents('.actionMenu:first').length){return true}
hideAllMenus()}
function actionMenuMouseOver(event){var menu_id=jQuery(this).parents('.actionMenu:first').attr('id'),switch_menu;if(!menu_id){return true}
switch_menu=jQuery('dl.actionMenu.activated').length>0;jQuery('dl.actionMenu').removeClass('activated').addClass('deactivated');if(switch_menu){jQuery('#'+menu_id).removeClass('deactivated').addClass('activated')}}
function initializeMenus(){jQuery(document).mousedown(actionMenuDocumentMouseDown);hideAllMenus();jQuery('dl.actionMenu dt.actionMenuHeader a').click(toggleMenuHandler).mouseover(actionMenuMouseOver);jQuery('dl.actionMenu > dd.actionMenuContent').click(hideAllMenus)}
jQuery(initializeMenus);

/* - table_sorter.js - */
// https://pleiades.stoa.org/portal_javascripts/table_sorter.js?original=1
(function($){
function sortabledataclass(cell){var re,matches;re=new RegExp("sortabledata-([^ ]*)","g");matches=re.exec(cell.attr('class'));if(matches){return matches[1]}
else{return null}}
function sortable(cell){var text=sortabledataclass(cell);if(text===null){text=cell.text()}
if(text.charAt(4)!=='-'&&text.charAt(7)!=='-'&&!isNaN(parseFloat(text))){return parseFloat(text)}
return text.toLowerCase()}
function sort(){var th,colnum,table,tbody,reverse,index,data,usenumbers,tsorted;th=$(this).closest('th');colnum=$('th',$(this).closest('thead')).index(th);table=$(this).parents('table:first');tbody=table.find('tbody:first');tsorted=parseInt(table.attr('sorted')||'-1',10);reverse=tsorted===colnum;$(this).parent().find('th:not(.nosort) .sortdirection').html('&#x2003;');$(this).children('.sortdirection').html(reverse?'&#x25b2;':'&#x25bc;');index=$(this).parent().children('th').index(this),data=[],usenumbers=true;tbody.find('tr').each(function(){var cells,sortableitem;cells=$(this).children('td');sortableitem=sortable(cells.slice(index,index+1));if(isNaN(sortableitem)){usenumbers=false}
data.push([sortableitem,sortable(cells.slice(1,2)),sortable(cells.slice(0,1)),this])});if(data.length){if(usenumbers){data.sort(function(a,b){return a[0]-b[0]})} else{data.sort()}
if(reverse){data.reverse()}
table.attr('sorted',reverse?'':colnum);tbody.append($.map(data, function(a){return a[3]}));tbody.each(setoddeven)}}
function setoddeven(){var tbody=$(this);tbody.find('tr').removeClass('odd').removeClass('even').filter(':odd').addClass('even').end().filter(':even').addClass('odd')}
$(function(){var blankarrow=$('<span>&#x2003;</span>').addClass('sortdirection');$('table.listing:not(.nosort) thead th:not(.nosort)').append(blankarrow.clone()).css('cursor','pointer').click(sort);$('table.listing:not(.nosort) tbody').each(setoddeven)})})(jQuery);

/* - calendar_formfield.js - */
// https://pleiades.stoa.org/portal_javascripts/calendar_formfield.js?original=1
if(typeof(plone)==='undefined'){var plone={}}(function($){plone.jscalendar={_calendar:null,_current_input:null,_field_names:['year','month','day','hour','minute','ampm'],_fields: function(selector){if(selector===undefined){selector=plone.jscalendar._current_input}
var fields={field:$(selector)};$.each(plone.jscalendar._field_names, function(){fields[this]=$(selector+'_'+this)});return fields},init: function(){$('.plone_jscalendar').find('input:hidden').each(function(){var selector='#'+this.id;$.each(plone.jscalendar._fields(selector), function(){this.filter('select').bind('change.plone.jscalendar',{selector:selector},plone.jscalendar.update_hidden)})})},show: function(input_id,yearStart,yearEnd){var cal=plone.jscalendar._cal,fields,anchor;if(!cal){cal=plone.jscalendar._cal=new Calendar(1,null,plone.jscalendar.handle_select,plone.jscalendar.handle_close);cal.create()} else{cal.hide()}
plone.jscalendar._current_input=input_id;fields=plone.jscalendar._fields();anchor=fields.month;cal.setRange(yearStart,yearEnd);if(fields.year.val()>0){cal.date.setFullYear(fields.year.val())}
if(fields.month.val()>0){cal.date.setMonth(fields.month.val()-1)}
if(fields.day.val()>0){cal.date.setDate(fields.day.val())}
cal.refresh();cal.showAtElement(anchor.get(0),null);return false},handle_select: function(cal,date){var fields=plone.jscalendar._fields(),yearValue=date.substring(0,4),options,i;if($.nodeName(fields.year.get(0),'select')&&!fields.year.children('option[value='+yearValue+']').length){options=fields.year.get(0).options;for(i=options.length;i>0;i=i-1){if(options[i].value>yearValue){options[i+1]=new Option(options[i].value,options[i].text)} else{options[i+1]=new Option(yearValue,yearValue);break}}}
fields.year.val(yearValue);fields.month.val(date.substring(5,7));fields.day.val(date.substring(8,10));plone.jscalendar.update_hidden()},handle_close: function(cal){cal.hide()},update_hidden: function(e){var val='',f=plone.jscalendar._fields(e&&e.data.selector),type,filter,date;if(e&&e.target.selectedIndex===0){type=e.target.id.substr(e.data.selector.length);filter=$.inArray(type,['hour','minute','ampm'])>-1?'select[id$=hour],select[id$=minute],select[id$=ampm]':'select';$.each(f, function(){this.filter(filter).attr('selectedIndex',0)})} else if(f.year.val()>0&&f.month.val()>0&&f.day.val()>0){val=[f.year.val(),f.month.val(),f.day.val()].join('-');date=new Date(val.replace(/-/g,'/'));if(date.print('%Y-%m-%d')!==val){val=date.print('%Y-%m-%d');f.year.val(val.substring(0,4));f.month.val(val.substring(5,7));f.day.val(val.substring(8,10))}
if(f.hour.length&&f.minute.length){val+=" "+[f.hour.val(),f.minute.val()].join(':');if(f.ampm.length){val+=" "+f.ampm.val()}}}
f.field.val(val)}}}(jQuery));jQuery(function($){$(plone.jscalendar.init);$('.plone-jscalendar-popup').each(function(){var jqt=$(this),widget_id=this.id.replace('_popup',''),year_start=$('#'+widget_id+'_yearStart').val(),year_end=$('#'+widget_id+'_yearEnd').val();if(year_start&&year_end){jqt.css('cursor','pointer').show().click(function(e){return plone.jscalendar.show('#'+widget_id,year_start,year_end)})}})});

/* - formUnload.js - */
// https://pleiades.stoa.org/portal_javascripts/formUnload.js?original=1
if(!window.beforeunload){(function($){var BeforeUnloadHandler,Class,form,c;BeforeUnloadHandler=function(){var self=this,message;this.message=window.form_modified_message||"Discard changes? If you click OK, any changes you have made will be lost.";this.forms=[];this.chkId=[];this.chkType=new this.CheckType();this.handlers=[this.isAnyFormChanged];this.submitting=false;this.execute=function(event){var domforms=$('form');self.forms=$.grep(self.forms, function(form){return domforms.index(form)>-1});if(self.submitting){return}
$.each(self.handlers, function(i,fn){message=message||fn.apply(self)});if(message===true){message=self.message}
if(message===false){message=undefined}
if(event&&message){event.returnValue=message}
return message};this.execute.tool=this};Class=BeforeUnloadHandler.prototype;Class.isAnyFormChanged=function(){var i;for(i=0;i<this.forms.length;i+=1){form=this.forms[i];if(this.isElementChanged(form)){return true}}
return false};Class.addHandler=function(fn){this.handlers.push(fn)};Class.onsubmit=function(){var tool=window.onbeforeunload&&window.onbeforeunload.tool;tool.submitting=true;plone.UnlockHandler.submitting=true};Class.addForm=function(form){if($.inArray(form,this.forms)>-1){return}
this.forms.push(form);$(form).submit(this.onsubmit);$(form).find('input:hidden').each(function(){var value=this.defaultValue;if(value!==undefined&&value!==null){$(this).attr('originalValue',value.replace(/\r\n?/g,'\n'))}})};Class.addForms=function(){var self=this;$.each(arguments, function(){if(this.tagName.toLowerCase()==='form'){self.addForm(this)} else{self.addForms.apply(self,$(this).find('form').get())}})};Class.removeForms=function(){var self=this;$.each(arguments, function(){if(this.tagName.toLowerCase()==='form'){var formElement=this;self.forms=$.grep(self.forms, function(form){return form!==formElement});$(formElement).unbind('submit',self.onsubmit)} else{self.removeForms.apply(self,$(this).find('form').get())}})};Class.CheckType=function(){};c=Class.CheckType.prototype;c.checkbox=c.radio=function(ele){return ele.checked!==ele.defaultChecked};c.file=c.password=function(ele){return ele.value!==ele.defaultValue};c.text=c.textarea=function(ele){if($(ele).hasClass('mce_editable')&&typeof(tinyMCE)!="undefined"){return tinyMCE.get(ele.id).getContent()!=ele.defaultValue} else if($(ele).hasClass('ckeditor_plone')&&typeof(CKEDITOR)!="undefined"){return CKEDITOR.instances[ele.id].getData()!=ele.defaultValue} else{return ele.value!==ele.defaultValue}};c.hidden=function(ele){var orig=$(ele).attr('originalValue');if(orig===undefined||orig===null){return false}
return $(ele).val().replace(/\r\n?/g,'\n')!==orig};c['select-one']=function(ele){var i,opt;for(i=0;i<ele.length;i+=1){opt=ele[i];if(opt.selected!==opt.defaultSelected){if(i===0&&opt.selected){continue}
return true}}
return false};c['select-multiple']=function(ele){var i,opt;for(i=0;i<ele.length;i+=1){opt=ele[i];if(opt.selected!==opt.defaultSelected){return true}}
return false};Class.chk_form=function(form){var elems=$(form).find('> :input:not(.noUnloadProtection),'+':not(.noUnloadProtection) :input:not(.noUnloadProtection)'),i;for(i=0;i<elems.length;i+=1){if(this.isElementChanged(elems.get(i))){return true}}
return false};Class.isElementChanged=function(ele){var method=ele.id&&this.chkId[ele.id];if(!method&&ele.type&&ele.name){method=this.chkType[ele.type]}
if(!method&&ele.tagName){method=this['chk_'+ele.tagName.toLowerCase()]}
return method?method.call(this,ele):false};window.onbeforeunload=new BeforeUnloadHandler().execute;$(function(){var tool=window.onbeforeunload&&window.onbeforeunload.tool;if(tool&&$('#region-content,#content').length){tool.addForms.apply(tool,$('form.enableUnloadProtection').get())}})}(jQuery))}


/* - formsubmithelpers.js - */
// https://pleiades.stoa.org/portal_javascripts/formsubmithelpers.js?original=1
function inputSubmitOnClick(event){if(jQuery(this).hasClass('submitting')&&!jQuery(this).hasClass('allowMultiSubmit'))
return confirm(window.form_resubmit_message);else
jQuery(this).addClass('submitting')}(function($){$(function(){$('input:submit,input:image').each(function(){if(!this.onclick)
$(this).click(inputSubmitOnClick)})})})(jQuery);

/* - unlockOnFormUnload.js - */
// https://pleiades.stoa.org/portal_javascripts/unlockOnFormUnload.js?original=1
if(typeof(plone)==='undefined'){var plone={}}(function($){plone.UnlockHandler={init: function(){if($('form.enableUnlockProtection').length){$(window).unload(plone.UnlockHandler.execute);plone.UnlockHandler._refresher=setInterval(plone.UnlockHandler.refresh,300000)}},cleanup: function(){$(window).unbind('unload',plone.UnlockHandler.execute);clearInterval(plone.UnlockHandler._refresher)},execute: function(){if(plone.UnlockHandler.submitting){return}
$.ajax({url:$('body').attr('data-base-url')+'/@@plone_lock_operations/safe_unlock',async:false})},refresh: function(){if(plone.UnlockHandler.submitting){return}
$.get($('body').attr('data-base-url')+'/@@plone_lock_operations/refresh_lock')}};$(plone.UnlockHandler.init)})(jQuery);

/* - jquery.tinymce.js - */
// https://pleiades.stoa.org/portal_javascripts/jquery.tinymce.js?original=1
(function(c){var b,e,a=[],d=window;c.fn.tinymce=function(j){var p=this,g,k,h,m,i,l="",n="";if(!p.length){return p}if(!j){return tinyMCE.get(p[0].id)}p.css("visibility","hidden");function o(){var r=[],q=0;if(f){f();f=null}p.each(function(t,u){var s,w=u.id,v=j.oninit;if(!w){u.id=w=tinymce.DOM.uniqueId()}s=new tinymce.Editor(w,j);r.push(s);s.onInit.add(function(){var x,y=v;p.css("visibility","");if(v){if(++q==r.length){if(tinymce.is(y,"string")){x=(y.indexOf(".")===-1)?null:tinymce.resolve(y.replace(/\.\w+$/,""));y=tinymce.resolve(y)}y.apply(x||tinymce,r)}}})});c.each(r,function(t,s){s.render()})}if(!d.tinymce&&!e&&(g=j.script_url)){e=1;h=g.substring(0,g.lastIndexOf("/"));if(/_(src|dev)\.js/g.test(g)){n="_src"}m=g.lastIndexOf("?");if(m!=-1){l=g.substring(m+1)}d.tinyMCEPreInit=d.tinyMCEPreInit||{base:h,suffix:n,query:l};if(g.indexOf("gzip")!=-1){i=j.language||"en";g=g+(/\?/.test(g)?"&":"?")+"js=true&core=true&suffix="+escape(n)+"&themes="+escape(j.theme)+"&plugins="+escape(j.plugins)+"&languages="+i;if(!d.tinyMCE_GZ){tinyMCE_GZ={start:function(){tinymce.suffix=n;function q(r){tinymce.ScriptLoader.markDone(tinyMCE.baseURI.toAbsolute(r))}q("langs/"+i+".js");q("themes/"+j.theme+"/editor_template"+n+".js");q("themes/"+j.theme+"/langs/"+i+".js");c.each(j.plugins.split(","),function(s,r){if(r){q("plugins/"+r+"/editor_plugin"+n+".js");q("plugins/"+r+"/langs/"+i+".js")}})},end:function(){}}}}c.ajax({type:"GET",url:g,dataType:"script",cache:true,success:function(){tinymce.dom.Event.domLoaded=1;e=2;if(j.script_loaded){j.script_loaded()}o();c.each(a,function(q,r){r()})}})}else{if(e===1){a.push(o)}else{o()}}return p};c.extend(c.expr[":"],{tinymce:function(g){return !!(g.id&&"tinyMCE" in window&&tinyMCE.get(g.id))}});function f(){function i(l){if(l==="remove"){this.each(function(n,o){var m=h(o);if(m){m.remove()}})}this.find("span.mceEditor,div.mceEditor").each(function(n,o){var m=tinyMCE.get(o.id.replace(/_parent$/,""));if(m){m.remove()}})}function k(n){var m=this,l;if(n!==b){i.call(m);m.each(function(p,q){var o;if(o=tinyMCE.get(q.id)){o.setContent(n)}})}else{if(m.length>0){if(l=tinyMCE.get(m[0].id)){return l.getContent()}}}}function h(m){var l=null;(m)&&(m.id)&&(d.tinymce)&&(l=tinyMCE.get(m.id));return l}function g(l){return !!((l)&&(l.length)&&(d.tinymce)&&(l.is(":tinymce")))}var j={};c.each(["text","html","val"],function(n,l){var o=j[l]=c.fn[l],m=(l==="text");c.fn[l]=function(s){var p=this;if(!g(p)){return o.apply(p,arguments)}if(s!==b){k.call(p.filter(":tinymce"),s);o.apply(p.not(":tinymce"),arguments);return p}else{var r="";var q=arguments;(m?p:p.eq(0)).each(function(u,v){var t=h(v);r+=t?(m?t.getContent().replace(/<(?:"[^"]*"|'[^']*'|[^'">])*>/g,""):t.getContent({save:true})):o.apply(c(v),q)});return r}}});c.each(["append","prepend"],function(n,m){var o=j[m]=c.fn[m],l=(m==="prepend");c.fn[m]=function(q){var p=this;if(!g(p)){return o.apply(p,arguments)}if(q!==b){p.filter(":tinymce").each(function(s,t){var r=h(t);r&&r.setContent(l?q+r.getContent():r.getContent()+q)});o.apply(p.not(":tinymce"),arguments);return p}}});c.each(["remove","replaceWith","replaceAll","empty"],function(m,l){var n=j[l]=c.fn[l];c.fn[l]=function(){i.call(this,l);return n.apply(this,arguments)}});j.attr=c.fn.attr;c.fn.attr=function(o,q){var m=this,n=arguments;if((!o)||(o!=="value")||(!g(m))){if(q!==b){return j.attr.apply(m,n)}else{return j.attr.apply(m,n)}}if(q!==b){k.call(m.filter(":tinymce"),q);j.attr.apply(m.not(":tinymce"),n);return m}else{var p=m[0],l=h(p);return l?l.getContent({save:true}):j.attr.apply(c(p),n)}}}})(jQuery);

/* - tiny_mce_gzip.js - */
// https://pleiades.stoa.org/portal_javascripts/tiny_mce_gzip.js?original=1
(function($,undefined){window.initTinyMCE=function(context,customConfig){customConfig=customConfig||{};$('textarea.mce_editable',context).each(function(){var $el=$(this),$field=$el.parents('.field'),tinymceActive=false,$textFormatSelector=$('.fieldTextFormat > select',$field),config=$.extend(true,{},$.parseJSON($el.attr('data-mce-config')),customConfig);$('.suppressVisualEditor',$field).hide();$textFormatSelector.bind('change', function(e){e.stopPropagation();if($(e.target).val()==='text/html'){if(!tinymceActive){$el.tinymce(config);tinymceActive=true}} else if(tinymceActive){tinyMCE.execCommand('mceRemoveControl',false,$el.attr('id'));tinymceActive=false}}).attr('tabindex','-1');if(!$textFormatSelector.length){$el.tinymce(config);tinymceActive=true} else if($textFormatSelector.val()==='text/html'){$el.tinymce(config);tinymceActive=true}})};$(document).ready(function(){window.initTinyMCE(document)})}(window.jQuery));
