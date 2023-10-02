$(document).ready(function(){


	$(function() {
	  $('#month').on('change', function(){
	    var value = $(this).val();
	    var i;
	    if (value == '0'){
			i = 2490.0;
		}else if (value == '1'){
			i = 1690.0;
		}else if (value == '2') {
			i = 1890.0;
		}else if (value == '3'){
			i = 2190.0;
		}else{
			i = 0.0;
		};
	    $('.myprice').text(i);
//	    $('input[name="rp"]').val(i);
	    //$('#id_rp').value= i
	    console.log(value);
//	    console.log($('input[name="rp"]').val(i));
	  });
	});

	//console.log(u);


	//console.log($("#id_rouse").val());

	//console.log($("#id_rouse option:selected").text());




});

