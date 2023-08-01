
/* Merged Plone Javascript file
 * This file is dynamically assembled from separate parts.
 * Some of these parts have 3rd party licenses or copyright information attached
 * Such information is valid for that section,
 * not for the entire composite file
 * originating files are separated by - filename.js -
 */

/* - referencebrowser.js - */
// https://pleiades.stoa.org/portal_javascripts/referencebrowser.js?original=1
jQuery(function($){$('[id^=atrb_]').detach().appendTo("body");var _loadOverlay=function(){if(!$.fn.overlay){setTimeout(_loadOverlay,50);return}
$('.addreference').overlay({onBeforeLoad: function(){ov=$('div#content').data('overlay');if(ov){ov.close()}
var wrap=this.getOverlay().find('.overlaycontent');var src=this.getTrigger().attr('src');var srcfilter=src+' >*';wrap.data('srcfilter',srcfilter);$('div#content').data('overlay',this);resetHistory();wrap.load(srcfilter, function(){var fieldname=wrap.find('input[name=fieldName]').attr('value');check_referenced_items(fieldname)})},onLoad: function(){widget_id=this.getTrigger().attr('rel').substring(6);disablecurrentrelations(widget_id)}})};_loadOverlay();$(document).on('click','[id^=atrb_] a.browsesite', function(event){var target=$(this);var src=target.attr('href');var wrap=target.parents('.overlaycontent');var srcfilter=src+' >*';pushToHistory(wrap.data('srcfilter'));wrap.data('srcfilter',srcfilter);var newoption='<option value="'+src+'">'+target.attr('rel')+'</option>';refreshOverlay(wrap,srcfilter,newoption);return false});$(document).on('click','[id^=atrb_] input.insertreference', function(event){var target=$(this);var wrap=target.parents('.overlaycontent');var fieldname=wrap.find('input[name=fieldName]').attr('value');var multi=wrap.find('input[name=multiValued]').attr('value');var close_window=wrap.find('input[name=close_window]').attr('value');var tablerow=target.parent().parent();var title=tablerow.find('label').html();var uid=target.attr('rel');var messageId;var widget_id_base='ref_browser_';if(multi!=='0'){widget_id_base='ref_browser_items_'}
if(this.checked===true){refbrowser_setReference(widget_id_base+fieldname,uid,title,parseInt(multi));messageId='#messageAdded'} else{refbrowser_delReference(fieldname,uid);messageId='#messageRemoved'}
if(close_window==='1'&&multi!=='1'){overlay=$('div#content').data('overlay');overlay.close()} else{showMessage(messageId,title)}});$(document).on('change','[id^=atrb_] form#history select[name=path]', function(event){var target=$(this);var wrap=target.parents('.overlaycontent');var src_selector='[id^=atrb_] form#history '+'select[name=path] :selected';var src=$(src_selector).attr('value');var srcfilter=src+' >*';refreshOverlay(wrap,srcfilter,'');return false});$(document).on('click','[id^=atrb_] .listingBar a, [id^=atrb_] .pagination a', function(event){var target=$(this);var src=target.attr('href');var wrap=target.parents('.overlaycontent');var srcfilter=src+' >*';refreshOverlay(wrap,srcfilter,'');return false});
function do_atref_search(event){event.preventDefault();var target=$(event.target);var src=target.parents('form').attr('action');var wrap=target.parents('.overlaycontent');var fieldname=wrap.find('input[name=fieldName]').attr('value');var fieldrealname=wrap.find('input[name=fieldRealName]').attr('value');var at_url=wrap.find('input[name=at_url]').attr('value');var searchvalue=encodeURI(wrap.find('input[name=searchValue]').attr('value'));var search_index=wrap.find('select[name=search_index]').attr('value');var multi=wrap.find('input[name=multiValued]').attr('value');var close_window=wrap.find('input[name=close_window]').attr('value');qs='searchValue='+searchvalue;if(search_index){qs+='&search_index='+search_index}
qs+='&fieldRealName='+fieldrealname+'&fieldName='+fieldname+'&multiValued='+multi+'&close_window'+close_window+'&at_url='+at_url;var srcfilter=src+'?'+qs+' >*';pushToHistory(wrap.data('srcfilter'));wrap.data('srcfilter',srcfilter);refreshOverlay(wrap,srcfilter,'');return false}
$(document).on('submit','[id^=atrb_] form#search',do_atref_search);$(document).on('click','[id^=atrb_] form#search input[name=submit]',do_atref_search);
function disablecurrentrelations(widget_id){$('ul#'+widget_id+' :input').each(
function(intIndex){uid=$(this).attr('value');cb=$('input[rel='+uid+']');cb.attr('disabled','disabled');cb.attr('checked','checked')})}
function refbrowser_setReference(widget_id,uid,label,multi){var element=null,label_element=null,current_values=null,i=null,list=null,li=null,input=null,up_element=null,down_element=null,container=null,fieldname=null;if(multi===0){$('#'+widget_id).attr('value',uid);$('#'+widget_id+'_label').attr('value',label)} else{current_values=$('#'+widget_id+' input');for(i=0;i<current_values.length;i++){if(current_values[i].value===uid){return false}}
fieldname=widget_id.substr('ref_browser_items_'.length);list=document.getElementById(widget_id);if(list===null){container=$('#archetypes-fieldname-'+fieldname+' input + div');if(!container.length){container=$('#archetypes-fieldname-value input + div')}
container.after('<ul class="visualNoMarker" id="'+widget_id+'"></ul>');list=document.getElementById(widget_id)}
li=document.createElement('li');label_element=document.createElement('label');input=document.createElement('input');input.type='checkbox';input.value=uid;input.checked=true;input.name=fieldname+':list';label_element.appendChild(input);label_element.appendChild(document.createTextNode(' '+label));li.appendChild(label_element);li.id='ref-'+fieldname+'-'+current_values.length;sortable=$('input[name='+fieldname+'-sortable]').attr('value');if(sortable==='1'){up_element=document.createElement('a');up_element.title='Move Up';up_element.href='';up_element.innerHTML='&#x25b2;';up_element.onclick=function(){refbrowser_moveReferenceUp(this);return false};li.appendChild(up_element);down_element=document.createElement('a');down_element.title='Move Down';down_element.href='';down_element.innerHTML='&#x25bc;';down_element.onclick=function(){refbrowser_moveReferenceDown(this);return false};li.appendChild(down_element)}
list.appendChild(li);input.checked=true}}
function refbrowser_delReference(fieldname,uid){var selector='input[value="'+uid+'"][name="'+fieldname+':list"]',inputs=$(selector);inputs.closest('li').remove()}
function refbrowser_removeReference(widget_id,multi){var x=null,element=null,label_element=null,list=null;if(multi){list=document.getElementById(widget_id);for(x=list.length-1;x>=0;x--){if(list[x].selected){list[x]=null}}
for(x=0;x<list.length;x++){list[x].selected='selected'}} else{$('#'+widget_id).attr('value',"");$('#'+widget_id+'_label').attr('value',"")}}
function refbrowser_moveReferenceUp(self){var elem=self.parentNode,eid=null,pos=null,widget_id=null,newelem=null,prevelem=null,arrows=null,cbs=null;if(elem===null){return false}
eid=elem.id.split('-');pos=eid.pop();if(pos==="0"){return false}
widget_id=eid.pop();newelem=elem.cloneNode(true);cbs=newelem.getElementsByTagName("input");if(cbs.length>0){cbs[0].checked=elem.getElementsByTagName("input")[0].checked}
prevelem=document.getElementById('ref-'+widget_id+'-'+(pos-1));arrows=newelem.getElementsByTagName("a");arrows[0].onclick=function(){refbrowser_moveReferenceUp(this);return false};arrows[1].onclick=function(){refbrowser_moveReferenceDown(this);return false};elem.parentNode.insertBefore(newelem,prevelem);elem.parentNode.removeChild(elem);newelem.id='ref-'+widget_id+'-'+(pos-1);prevelem.id='ref-'+widget_id+'-'+pos}
function refbrowser_moveReferenceDown(self){var elem=self.parentNode,eid=null,pos=null,widget_id=null,current_values=null,newelem=null,nextelem=null,cbs=null,arrows=null;if(elem===null){return false}
eid=elem.id.split('-');pos=parseInt(eid.pop(),10);widget_id=eid.pop();current_values=$('#ref_browser_items_'+widget_id+' input');if((pos+1)===current_values.length){return false}
newelem=elem.cloneNode(true);cbs=newelem.getElementsByTagName("input");if(cbs.length>0){cbs[0].checked=elem.getElementsByTagName("input")[0].checked}
arrows=newelem.getElementsByTagName("a");arrows[0].onclick=function(){refbrowser_moveReferenceUp(this);return false};arrows[1].onclick=function(){refbrowser_moveReferenceDown(this);return false};nextelem=document.getElementById('ref-'+widget_id+'-'+(pos+1));elem.parentNode.insertBefore(newelem,nextelem.nextSibling);elem.parentNode.removeChild(elem);newelem.id='ref-'+widget_id+'-'+(pos+1);nextelem.id='ref-'+widget_id+'-'+pos}
function showMessage(messageId,text){var template=$(messageId).parent(),message_div=template.clone(),message=message_div.children(),old_message=$('#message'),message_wrapper=$('#messageWrapper');message_wrapper.prepend(message_div);message.find('dd').text(text);message.css({opacity:0}).show();message.attr('id','message');message_wrapper.animate({height:message.height()+20},400);message.fadeTo(400,1);old_message.fadeTo(400,0, function(){old_message.parent().remove()})}
function submitHistoryForm(){var form=document.history;var path=form.path.options[form.path.selectedIndex].value;form.action=path;form.submit()}
function pushToHistory(url){var history=$(document).data('atrb_history');history.push(url);$(document).data('atrb_history',history)}
function resetHistory(){$(document).data('atrb_history',[])}
function popFromHistory(){var history=$(document).data('atrb_history');value=history.pop();$(document).data('atrb_history',history);return value}
function refreshOverlay(wrap,srcfilter,newoption){var oldhistory=$('[id^=atrb_] form#history select');wrap.load(srcfilter, function(){$('[id^=atrb_] form#history select').append(newoption+oldhistory.html());ov=$('div#content').data('overlay');widget_id=ov.getTrigger().attr('rel').substring(6);disablecurrentrelations(widget_id);var fieldname=wrap.find('input[name=fieldName]').attr('value');check_referenced_items(fieldname)})}
function check_referenced_items(fieldname){var refs_in_overlay=$('input.insertreference'),uid_selector="input[name='"+fieldname+":list']",current=$(uid_selector),current_uids=current.map(function(){if(this.checked===true){return $(this).attr('value')}
return null});refs_in_overlay.each(function(){var overlay_ref=$(this),uid=$(overlay_ref).attr('rel'),i;for(i=0;i<current_uids.length;i++){if(uid===current_uids[i]){overlay_ref.attr('checked',true);return true}}})}
$(document).on('change','#indexSelector', function(event){if($.inArray(this.value,$('#searchWildcardHelp').data()['wildcardableindexes'])===-1){$('#searchWildcardHelp').css("display","none")}
else{$('#searchWildcardHelp').css("display","")}});$(document).ready(function(){$('input.removereference').click(function(event){event.preventDefault();var fieldname=$(this).data('fieldname'),multivalued=$(this).data('multivalued');refbrowser_removeReference('ref_browser_'+fieldname,multivalued)});$('a[data-move-direction]').click(function(event){event.preventDefault();var direction=$(this).attr('data-move-direction');if(direction=='up'){refbrowser_moveReferenceUp(this)} else{refbrowser_moveReferenceDown(this)}})})});

/* - kss-bbb.js - */
// https://pleiades.stoa.org/portal_javascripts/kss-bbb.js?original=1
(function($){$(function(){if(typeof($('body').attr('data-portal-url'))!=='undefined'&&typeof($('body').attr('data-base-url'))!=='undefined'){return}
$('body').attr('data-portal-url',portal_url);$('body').attr('data-base-url',base_url)});
function refreshPortlet(hash,_options){var options={data:{},success: function(){},error: function(){},ajaxOptions:{}};$.extend(options,_options);options.data.portlethash=hash;ajaxOptions=options.ajaxOptions;ajaxOptions.url=$('body').attr('data-base-url')+'/@@render-portlet';ajaxOptions.success=function(data){var container=$('[data-portlethash="'+hash+'"]');var portlet=$(data);container.html(portlet);options.success(data,portlet)}
ajaxOptions.error=function(){options.error()}
ajaxOptions.data=options.data;$.ajax(ajaxOptions)}
function applyPortletTimeout(portlet){var timeout=portlet.data('timeout');if(timeout==undefined){timeout=30}else{timeout=parseInt(timeout)}
timeout=timeout * 1000;setTimeout($.proxy(function(){refreshPortlet(this.parents('.portletWrapper').data('portlethash'),{success: function(data,portlet){apply_timeout(portlet)}})},portlet),timeout)}
$(document).ready(function(){var spinner=$('<div id="ajax-spinner"><img src="'+portal_url+'/spinner.gif" alt=""/></div>');spinner.appendTo('body').hide();$(document).ajaxStart(function(){spinner.show()});$(document).ajaxStop(function(){spinner.hide()});$('body').delegate('#calendar-next,#calendar-previous','click', function(e){e.preventDefault();var el=$(this);var container=el.parents('.portletWrapper');refreshPortlet(container.data('portlethash'),{data:{month:el.data('month'),year:el.data('year')}});return false});$('.kssPortletRefresh,.refreshPortlet').each(function(){applyPortletTimeout($(this))});$('.portlet-deferred').each(function(){refreshPortlet($(this).parents('.portletWrapper').data('portlethash'))});
function updateSharing(data){var sharing=data.body;var messages=$(data.messages).filter(function(){return this.tagName=='DL'});$('.portalMessage').remove();$('#user-group-sharing').replaceWith(sharing);$('#content').prepend(messages)}
var search_timeout=null;$('#content-core').delegate('#sharing-user-group-search','input', function(){var text=$(this);if(search_timeout!=null){clearTimeout(search_timeout)}
if(text.val().length>3){search_timeout=setTimeout($.proxy(function(){$('#sharing-search-button').trigger('click')},text),300)}});$('#content-core').delegate('#sharing-search-button','click', function(){$.ajax({url:$('body').attr('data-base-url')+'/@@updateSharingInfo',data:{search_term:$('#sharing-user-group-search').val(),'form.button.Search':'Search'},type:'GET',dataType:'json',success:updateSharing});return false});$('#content-core').delegate('#sharing-save-button','click', function(){var btn=$(this);var form=btn.parents('form');var data=form.serializeArray();data.push({name:'form.button.Save',value:'Save'});$.ajax({url:$('body').attr('data-base-url')+'/@@updateSharingInfo',data:data,type:'POST',dataType:'json',success:updateSharing});return false})})})(jQuery);

/* - ++resource++collective.z3cform.datagridfield/datagridfield.js - */
/*global window, console*/

jQuery(function($) {

    // No globals, dude!
    "use strict";

    // Local singleton object containing our functions
    var dataGridField2Functions = {};

    dataGridField2Functions.getInputOrSelect = function(node) {
        /* Get the (first) input or select form element under the given node */

        var inputs = node.getElementsByTagName("input");
        if(inputs.length > 0) {
            return inputs[0];
        }

        var selects = node.getElementsByTagName("select");
        if(selects.length > 0) {
            return selects[0];
        }

        return null;
    };

    dataGridField2Functions.getWidgetRows = function(currnode) {
        /* Return primary nodes with class of datagridwidget-row,
           they can be any tag: tr, div, etc. */
        var tbody = this.getParentByClass(currnode, "datagridwidget-body");
        return this.getRows(tbody);
    };

    dataGridField2Functions.getRows = function(tbody) {
        /* Return primary nodes with class of datagridwidget-row,
           they can be any tag: tr, div, etc. */

        var rows = $(tbody).children('.datagridwidget-row');

        return rows;
    };


    /**
     * Get all visible rows of DGF
     *
     * Incl. normal rows + AA row
     */
    dataGridField2Functions.getVisibleRows = function(tbody) {

        var rows = this.getRows(tbody);
        // We rape jQuery.filter here, because of
        // IE8 Array.filter http://kangax.github.com/es5-compat-table/

        // Consider "real" rows only
        var filteredRows = $(rows).filter(function() {
            var $tr = $(this);
            return !$tr.hasClass("datagridwidget-empty-row");
        });

        return filteredRows;
    };

    /**
     * Handle auto insert events by auto append
     */
    dataGridField2Functions.onInsert = function(e) {
        var currnode = e.currentTarget;
        this.autoInsertRow(currnode);
    },

    /**
     * Add a new row when changing the last row
     *
     * @param {Boolean} ensureMinimumRows we insert a special minimum row so the widget is not empty
     */
    dataGridField2Functions.autoInsertRow = function(currnode, ensureMinimumRows) {

        // fetch required data structure
        var dgf = $(dataGridField2Functions.getParentByClass(currnode, "datagridwidget-table-view"));
        var tbody = dataGridField2Functions.getParentByClass(currnode, "datagridwidget-body");
        var thisRow = dataGridField2Functions.getParentRow(currnode); // The new row we are working on
        var $thisRow = $(thisRow);

        var autoAppendMode = $(tbody).data("auto-append");

        if($thisRow.hasClass("minimum-row")) {
            // The change event was not triggered on real AA row,
            // but on a minimum ensured row (row 0).
            // 1. Don't add new row
            // 2. Make widget to "normal" state now as the user has edited the empty row so we assume it's a real row
            this.supressEnsureMinimum(tbody);
            return;
        }

        // Remove the auto-append functionality from the all rows in this widget
        var autoAppendHandlers = dgf.find('.auto-append .datagridwidget-cell, .auto-append .datagridwidget-block-edit-cell');
        autoAppendHandlers.unbind('change.dgf');
        $thisRow.removeClass('auto-append');

        // Create a new row
        var newtr = dataGridField2Functions.createNewRow(thisRow), $newtr = $(newtr);
        // Add auto-append functionality to our new row
        $newtr.addClass('auto-append');

        /* Put new row to DOM tree after our current row.  Do this before
         * reindexing to ensure that any Javascript we insert that depends on
         * DOM element IDs (such as plone.formwidget.autocomplete) will
         * pick up this row before any IDs get changed.  At this point,
         * we techinically have duplicate TT IDs in our document
         * (one for this new row, one for the hidden row), but jQuery
         * selectors will pick up elements in this new row first.
         */

        dgf.trigger("beforeaddrowauto", [dgf, newtr]);

        if(ensureMinimumRows) {
            // Add a special class so we can later deal with it
            $newtr.addClass("minimum-row");
            $newtr.insertBefore(thisRow);
        } else {
            $newtr.insertAfter(thisRow);
        }

        // Re-enable auto-append change handler feature on the new auto-appended row
        if(autoAppendMode) {
            $(dgf).find('.auto-append .datagridwidget-cell, .auto-append .datagridwidget-block-edit-cell').bind("change.dgf", $.proxy(dataGridField2Functions.onInsert, dataGridField2Functions));
        }

        dataGridField2Functions.reindexRow(tbody, newtr, 'AA');

        // Update order index to give rows correct values
        dataGridField2Functions.updateOrderIndex(tbody, true, ensureMinimumRows);

        dgf.trigger("afteraddrowauto", [dgf, newtr]);
    };

    /**
     * Creates a new row after the the target row.
     *
     * @param {Object} currnode DOM <tr>
     */
    dataGridField2Functions.addRowAfter = function(currnode) {

        // fetch required data structure
        var tbody = this.getParentByClass(currnode, "datagridwidget-body");
        var dgf = $(dataGridField2Functions.getParentByClass(currnode, "datagridwidget-table-view"));

        var thisRow = this.getParentRow(currnode);

        var newtr = this.createNewRow(thisRow);

        dgf.trigger("beforeaddrow", [dgf, newtr]);

        var filteredRows = this.getVisibleRows(currnode);

        // If using auto-append we add the "real" row before AA
        // We have a special case when there is only one visible in the gid
        if (thisRow.hasClass('auto-append') && !thisRow.hasClass("minimum-row")) {
            $(newtr).insertBefore(thisRow);
        } else {
            $(newtr).insertAfter(thisRow);
        }

        // Ensure minimum special behavior is no longer needed as we have now at least 2 rows
        if(thisRow.hasClass("minimum-row")) {
            this.supressEnsureMinimum(tbody);
        }

        // update orderindex hidden fields
        this.updateOrderIndex(tbody, true);

        dgf.trigger("afteraddrow", [dgf, newtr]);

    };

    /**
     * Creates a new row.
     *
     * The row is not inserted to the table, but is returned.
     *
     * @param {Object} <tr> or <tbody> DOM node in a table where we'll be adding the new row
     */
    dataGridField2Functions.createNewRow = function(node) {

        var tbody = this.getParentByClass(node, "datagridwidget-body");

        // hidden template row
        var emptyRow = $(tbody).children('.datagridwidget-empty-row').first();

        if(emptyRow.size() === 0) {
            // Ghetto assert()
            throw new Error("Could not locate empty template row in DGF");
        }

        var new_row = emptyRow.clone(true).removeClass('datagridwidget-empty-row');

        return new_row;
    };


    dataGridField2Functions.removeFieldRow = function(node) {
        /* Remove the row in which the given node is found */
        var tbody = this.getParentByClass(node, "datagridwidget-body");
        var row = this.getParentRow(node);
        $(row).remove();
        this.updateOrderIndex(tbody,false);
    };

    dataGridField2Functions.moveRow = function(currnode, direction){
        /* Move the given row down one */
        var nextRow;

        var dgf = $(dataGridField2Functions.getParentByClass(currnode, "datagridwidget-table-view"));

        var tbody = this.getParentByClass(currnode, "datagridwidget-body");

        var rows = this.getWidgetRows(currnode);

        var row = this.getParentRow(currnode);
        if(!row) {
            throw new Error("Couldn't find DataGridWidget row");
        }

        var idx = null;

        // We can't use nextSibling because of blank text nodes in some browsers
        // Need to find the index of the row

        rows.each(function (i) {
            if (this == row[0]) {
                idx = i;
            }
        });

        // Abort if the current row wasn't found
        if (idx == null)
            return;


        // The up and down should cycle through the rows, excluding the auto-append and
        // empty-row rows.
        var validrows = 0;
        rows.each(function (i) {
            if (!$(this).hasClass('datagridwidget-empty-row') && !$(this).hasClass('auto-append')) {
                validrows+=1;
            }
        });

        if (idx+1 == validrows) {
            if (direction == "down") {
                this.moveRowToTop(row);
            } else {
                nextRow = rows[idx-1];
                this.shiftRow(nextRow, row);
            }

        } else if (idx === 0) {
            if (direction == "up") {
                this.moveRowToBottom(row);
            } else {
                nextRow = rows[parseInt(idx+1, 10)];
                this.shiftRow(row, nextRow);
            }

        } else {
            if (direction == "up") {
                nextRow = rows[idx-1];
                this.shiftRow(nextRow, row);
            } else {
                nextRow = rows[parseInt(idx+1, 10)];
                this.shiftRow(row, nextRow);
            }
        }

        this.updateOrderIndex(tbody);

        dgf.trigger("aftermoverow", [dgf, row]);
    };

    dataGridField2Functions.moveRowDown = function(currnode){
        this.moveRow(currnode, "down");
    };

    dataGridField2Functions.moveRowUp = function(currnode){
        this.moveRow(currnode, "up");
    };

    dataGridField2Functions.shiftRow = function(bottom, top){
        /* Put node top before node bottom */
        $(top).insertBefore(bottom);
    };

    dataGridField2Functions.moveRowToTop = function (row) {
        var rows = this.getWidgetRows(row);
        $(row).insertBefore(rows[0]);
    };

    dataGridField2Functions.moveRowToBottom = function (row) {
        var rows = this.getWidgetRows(row);

        // make sure we insert the directly above any auto appended rows
        var insert_after = 0;
        rows.each(function (i) {
            if (!$(this).hasClass('datagridwidget-empty-row')  && !$(this).hasClass('auto-append')) {
                insert_after = i;
            }
        });
        $(row).insertAfter(rows[insert_after]);
    };

    /**
     * Fixup all attributes on all child elements that contain
     * the row index. The following attributes are scanned:
     * - name
     * - id
     * - for
     * - href
     * - data-fieldname
     *
     * On the server side, the DGF logic will rebuild rows based
     * on this information.
     *
     * If indexing for some reasons fails you'll get double
     * input values and Zope converts inputs to list, failing
     * in funny ways.
     *
     * @param  {DOM} tbody
     * @param  {DOM} row
     * @param  {Number} newindex
     */
    dataGridField2Functions.reindexRow = function (tbody, row, newindex) {
        var name_prefix = $(tbody).data('name_prefix') + '.';
        var id_prefix = $(tbody).data('id_prefix') + '-';
        var $row = $(row);
        var oldindex = $row.data('index');

        function replaceIndex(el, attr, prefix) {
            if (el.attr(attr)) {
                var val = el.attr(attr);
                var pattern = new RegExp('^' + prefix + oldindex);
                el.attr(attr, val.replace(pattern, prefix + newindex));
                if (attr.indexOf('data-') === 0) {
                    var key = attr.substr(5);
                    var data = el.data(key);
                    el.data(key, data.replace(pattern, prefix + newindex));
                }
            }
        }

        // update index data
        $row.data('index', newindex);
        $row.attr('data-index', newindex);

        $row.find('[id^="formfield-' + id_prefix + '"]').each(function(i, el) {
            replaceIndex($(el), 'id', 'formfield-' + id_prefix);
        });

        $row.find('[name^="' + name_prefix +'"]').each(function(i, el) {
            replaceIndex($(el), 'name', name_prefix);
        });

        $row.find('[id^="' + id_prefix +'"]').each(function(i, el) {
            replaceIndex($(el), 'id', id_prefix);
        });

        $row.find('[for^="' + id_prefix +'"]').each(function(i, el) {
            replaceIndex($(el), 'for', id_prefix);
        });

        $row.find('[href*="#' + id_prefix +'"]').each(function(i, el){
            replaceIndex($(el), 'href', '#' + id_prefix);
        });

        $row.find('[data-fieldname^="' + name_prefix + '"]').each(function(i, el) {
            replaceIndex($(el), 'data-fieldname', name_prefix);
        });
    };

    /**
     * Stop ensure miminum special behavior.
     *
     * The caller is responsible to check there was one and only one minimum-row in the table.
     *
     * Call when data is edited for the first time or a row added.
     */
    dataGridField2Functions.supressEnsureMinimum = function(tbody) {

        var autoAppendHandlers = $(tbody).find('.auto-append .datagridwidget-cell, .auto-append .datagridwidget-block-edit-cell');
        autoAppendHandlers.unbind('change.dgf');

        tbody.children().removeClass("auto-append");
        tbody.children().removeClass("minimum-row");


        dataGridField2Functions.updateOrderIndex(tbody, true, false);
    };

    /**
     * Update all row indexes on a DGF table.
     *
     * Each <tr> and input widget has recalculated row index number in its name,
     * so that the server can then parsit the submitted data in the correct order.
     *
     * @param  {Object} tbody     DOM of DGF <tbody>
     * @param  {Boolean} backwards iterate rows backwards
     * @param  {Boolean} ensureMinimumRows We have inserted a special auto-append row
     */
    dataGridField2Functions.updateOrderIndex = function (tbody, backwards, ensureMinimumRows) {

        var $tbody = $(tbody);
        var name_prefix = $tbody.attr('data-name_prefix') + '.';
        var i, idx, row, $row, $nextRow;

        // Was this auto-append table
        var autoAppend = false;

        var rows = this.getRows(tbody);
        for (i=0; i<rows.length; i++) {
            idx = backwards ? rows.length-i-1 : i;
            row = rows[idx], $row = $(row);

            if ($row.hasClass('datagridwidget-empty-row')) {
                continue;
            }

            if($row.hasClass('auto-append')) {
                autoAppend = true;
            }

            this.reindexRow(tbody, row, idx);
        }

        // Handle a special case where
        // 1. Widget is empty
        // 2. We don't have AA mode turned on
        // 3. We need to have minimum editable row count of 1
        if(ensureMinimumRows) {
            this.reindexRow(tbody, rows[0], "AA");
            autoAppend = true;
        }

        // Add a special first and class row classes
        // to hide manipulation handles
        // AA handling is different once again
        var visibleRows = this.getVisibleRows(tbody);

        for (i=0; i<visibleRows.length; i++) {
            row = visibleRows[i], $row = $(row);

            if(i<visibleRows.length-2) {
                $nextRow = $(visibleRows[i+1]);
            }

            if(i===0) {
                $row.addClass("datagridfield-first-filled-row");
            } else {
                $row.removeClass("datagridfield-first-filled-row");
            }

            // Last visible before AA
            if(autoAppend) {
                if($nextRow && $nextRow.hasClass("auto-append")) {
                    $row.addClass("datagridfield-last-filled-row");
                } else {
                    $row.removeClass("datagridfield-last-filled-row");
                }
            } else {
                if(i==visibleRows.length-1) {
                    $row.addClass("datagridfield-last-filled-row");
                } else {
                    $row.removeClass("datagridfield-last-filled-row");
                }
            }
        }


        // Set total visible row counts and such and hint CSS
        var vis = this.getVisibleRows(tbody).length;
        $tbody.attr("data-count", this.getRows(tbody).length);
        $tbody.attr("data-visible-count", this.getVisibleRows(tbody).length);
        $tbody.attr("data-many-rows", vis >= 2 ? "true" : "false");

        $(document).find('input[name="' + name_prefix + 'count"]').each(function(){
            // do not include the TT and the AA rows in the count
            var count = rows.length;
            if ($(rows[count-1]).hasClass('datagridwidget-empty-row')) {
                count--;
            }
            if ($(rows[count-1]).hasClass('auto-append')) {
                count--;
            }
            this.value = count;
        });
    };

    dataGridField2Functions.getParentElement = function(currnode, tagname) {
        /* Find the first parent node with the given tag name */

        tagname = tagname.toUpperCase();
        var parent = currnode.parentNode;

        while(parent.tagName.toUpperCase() != tagname) {
            parent = parent.parentNode;
            // Next line is a safety belt
            if(parent.tagName.toUpperCase() == "BODY")
                return null;
        }

        return parent;
    };

    dataGridField2Functions.getParentRow = function (node) {
        return this.getParentByClass(node, 'datagridwidget-row');
    };

    dataGridField2Functions.getParentByClass = function(node, klass) {
        var parent = $(node).closest("." + klass);

        if (parent.length) {
            return parent;
        }

        return null;
    };

    /**
     * Find the first parent node with the given id
     *
     * Id is partially matched: the beginning of
     * an element id matches parameter id string.
     *
     * @param  {DOM} currnode Node where ascending in DOM tree beings
     * @param  {String} id       Id string to look for.
     * @return {DOM} Found node or null
     */
    dataGridField2Functions.getParentElementById = function(currnode, id) {
        /*
        */

        id = id.toLowerCase();
        var parent = currnode.parentNode;

        while(true) {

            var parentId = parent.getAttribute("id");
            if(parentId) {
                 if(parentId.toLowerCase().substring(0, id.length) == id) break;
            }

            parent = parent.parentNode;
            // Next line is a safety belt
            if(parent.tagName.toUpperCase() == "BODY")
                return null;
        }

        return parent;
    };


    /**
     * Make sure there is at least one visible row available in DGF
     * to edit in all the time.
     *
     * We need a lot of special logic for the case where
     * we have empty datagridfield and need to have one OPTIONAL
     * row present there for the editing when the user opens
     * the form for the first time.
     *
     * There are cases where one doesn't want to have the count of DGF
     * rows to go down to zero. Otherwise there no insert handle left
     * on the edit mode and the user cannot add any more rows.
     *
     * One should case is when
     *
     * - DGF is empty on new form
     *
     * - Auto append is set to false (initial row is not visible)
     *
     * We fix this situation by checking the available rows
     * and generating one empty AA row if needed.
     *
     * ... or simply when the user removes all the rows
     *
     * @param {Object} tbody DOM object of <tbody>
     */
    dataGridField2Functions.ensureMinimumRows = function(tbody) {
        var rows = this.getRows(tbody);
        var filteredRows = this.getVisibleRows(tbody);
        var self = this;

        // Rows = 0 -> make one AA row available
        if(filteredRows.length === 0) {
            // XXX: make the function call signatures more sane
            var child = rows[0];
            this.autoInsertRow(child, true);

        }
    },


    /**
     * When DOM model is ready execute this actions to wire up page logic.
     */
    dataGridField2Functions.init = function() {

        // Reindex all rows to get proper row classes on them
        $(".datagridwidget-body").each(function() {

            // Initialize widget data on <tbody>
            // We keep some mode attributes around
            var $this = $(this);
            var aa;

            // Check if this widget is in auto-append mode
            // and store for later usage
            aa = $this.children(".auto-append").size() > 0;
            $this.data("auto-append", aa);

            // Hint CSS
            if(aa) {
                $this.addClass("datagridwidget-body-auto-append");
            } else {
                $this.addClass("datagridwidget-body-non-auto-append");
            }

            dataGridField2Functions.updateOrderIndex(this, false);

            if(!aa) {
                dataGridField2Functions.ensureMinimumRows(this);
            }
        });

        // Bind the handlers to the auto append rows
        // Use namespaced jQuery events to avoid unbind() conflicts later on
        $('.auto-append .datagridwidget-cell, .auto-append .datagridwidget-block-edit-cell').bind("change.dgf", $.proxy(dataGridField2Functions.onInsert, dataGridField2Functions));

        $(document).trigger("afterdatagridfieldinit");
    };


    $(document).ready(dataGridField2Functions.init);

    // Export module for customizers to mess around
    window.dataGridField2Functions = dataGridField2Functions;


});

