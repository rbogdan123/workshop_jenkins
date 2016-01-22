var hidden = true;
$("#toggle_form").click(function(){
	if(hidden) {
		$("#hidden_form").show();
		hidden = false;
	}else {
		$("#hidden_form").hide();
		hidden = true;
	}
	
});


$("#menu-toggle").click(function (e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
});


$(function() {
    $( "#datepicker" ).datepicker({
        minDate: 0, 
        dateFormat: 'yy-mm-dd',
    });
});


$(function() {
    $( ".datepicker" ).datepicker({
        minDate: 0, 
        dateFormat: 'yy-mm-dd',
    });
});


$(document).ready(function(){
    $('[data-toggle="popover"]').popover(); 
});
