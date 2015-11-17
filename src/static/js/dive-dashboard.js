_collectionId = null;

$(document).ready(function(){
    loadUrlParams();
    initTabs();
});

function initTabs(){
    /*$('#collection_tabs a').click(function(a) {
        if(a && a.target && a.target.href) {
            document.location.href = a.target.href;
        }
    });*/
    $('#collection_tabs li:eq(0)').addClass('active');
    $('.tab-content .tab-pane:eq(0)').addClass('active');
}

function loadUrlParams() {
    var match,
        pl     = /\+/g,  // Regex for replacing addition symbol with a space
        search = /([^&=]+)=?([^&]*)/g,
        decode = function (s) { return decodeURIComponent(s.replace(pl, " ")); },
        query  = window.location.search.substring(1);

        urlParams = {};
    while (match = search.exec(query))
        urlParams[decode(match[1])] = decode(match[2]);
    console.debug(urlParams);
    _collectionId = urlParams['c'];
}

function setCollection(elm) {
    var uid = $(elm).attr('id');
    var c = $('#' + uid + ' option:selected').val();
    console.debug('uid=' + uid);
    console.debug('collection=' + c);
    var url = document.location.href;
    if(url.indexOf('c=') == -1) {
        document.location.href = url + '?c=' + c;
    } else {
        document.location.href = url.substring(0, url.indexOf('c=')) + 'c=' + c;
    }

}


function gotoPage(page) {
    var url = document.location.protocol + '//' + document.location.host;
    url += '/'+page+'?c=' + _collectionId;
    document.location.href = url;
}