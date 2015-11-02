//write some code you!

_taskTable = null;

$(document).ready(function() {
	initLinksTable();
});

function initLinksTable() {
	_taskTable = $('#task_table').DataTable( {
		"paging":   false,
		"ordering": false,
		"info":     false,
		"filter" : false
    });

    $('#task_table tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        } else {
            _taskTable.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    } );

    $('#task_table tbody').on( 'dblclick', 'tr', function () {
    	editRow(_taskTable.row(this));
    } );
}