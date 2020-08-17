// Basic DataTable
$(function(){
	$('.program-table').DataTable({
		language: { search: '', searchPlaceholder: "Search..." },
		"scrollX": true,
		"scrollCollapse": true,
		'iDisplayLength': 18,
		"ordering": true,
		"lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
		dom: 'Bfrtip',
        buttons: [
            'excelHtml5',
            'csvHtml5',
        ]
		
	});
});

$(function(){
	$('.dataTable').DataTable({
		language: { search: '', searchPlaceholder: "Search..." },
		"scrollX": true,
		"scrollCollapse": true,
		'iDisplayLength': 3,
		'paging': true,
		dom: 'Bfrtip',
        buttons: [
            'excelHtml5',
            'csvHtml5',
        ]
		
	});
});

$(function(){
	$('.dataTablePartner').DataTable({
		language: { search: '', searchPlaceholder: "Search..." },
		"scrollX": true,
		"scrollCollapse": true,
//		'iDisplayLength': 100,
		"ordering": true,
		"bInfo" : false,
		"paging": false,
//		"lengthMenu": [[100, 200, 300, -1], [100, 200, 300, "All"]],
		dom: 'lBfrtip',
        buttons: [
            'excelHtml5',
            'csvHtml5',
        ]

	});
});


// Vertical Scroll
$(function(){
	$('#scrollVertical').DataTable({
		"scrollY": "200px",
		"scrollCollapse": true,
		"paging": false,
		'iDisplayLength': 3,
	});
});




// Row Selection
$(function(){
	$('#rowSelection').DataTable({
		'iDisplayLength': 3,
	});
	var table = $('#rowSelection').DataTable();

	$('#rowSelection tbody').on( 'click', 'tr', function () {
		$(this).toggleClass('selected');
	});

	$('#button').on('click', function () {
		alert( table.rows('.selected').data().length +' row(s) selected' );
	});
});


// Highlighting rows and columns
$(function(){
	$('#highlightRowColumn').DataTable({
		'iDisplayLength': 3,
	});
	var table = $('#highlightRowColumn').DataTable();  
	$('#highlightRowColumn tbody').on('mouseenter', 'td', function (){
		var colIdx = table.cell(this).index().column;
		$(table.cells().nodes()).removeClass('highlight');
		$(table.column(colIdx).nodes()).addClass('highlight');
	});
});


// Using API in callbacks
$(function(){
  $('#apiCallbacks').DataTable({
  	'iDisplayLength': 3,
    "initComplete": function(){
      var api = this.api();
      api.$('td').on('click', function(){
        api.search(this.innerHTML).draw();
      });
    }
  });
});


// Fixed Header
$(document).ready(function(){
	var table = $('#fixedHeader').DataTable({
	  fixedHeader: true,
	  'iDisplayLength': 3,
	});
});