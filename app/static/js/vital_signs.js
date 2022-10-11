

function validateVs(){
    var valid = true;
	$(".InputBox").css('background-color','');
	$(".info").html('');
	if(!$("#description").val() ) {
		$("#description-info").html("(*)");
		$("#description").css('background-color','#FFFFDF');
		$("#description-info").css('color','#F00');
		valid = false;
	}
	if(!$("#minvalue").val()) {
		$("#minvalue-info").html("(*)");
		$("#minvalue").css('background-color','#FFFFDF');
		$("#minvalue-info").css('color','#F00');
		valid = false;
	}
	if(!$("#maxvalue").val()) {
		$("#maxvalue-info").html("(*)");
		$("#maxvalue").css('background-color','#FFFFDF');
		$("#maxvalue-info").css('color','#F00');
		valid = false;
	}
	if(!$("#age_range_name").val()) {
		$("#age_range_name-info").html("(*)");
		$("#age_range_name").css('background-color','#FFFFDF');
		$("#age_range_name-info").css('color','#F00');
		valid = false;
	}else if ($("#age_range_name").val()=="new"){
        if(!$("#new_age_range").val()) {
            $("#new_age_range-info").html("(*)");
            $("#new_age_range").css('background-color','#FFFFDF');
            $("#new_age_range-info").css('color','#F00');
            valid = false;
        }
        if(!$("#min_age").val()) {
            $("#min_age-info").html("(*)");
            $("#min_age").css('background-color','#FFFFDF');
            $("#min_age-info").css('color','#F00');
            valid = false;
        }
        if(!$("#maxage_type").val()) {
             $("#min_age-info").html("(*)");
             $("#min_age-info").css('color','#F00');
            $("#maxage_type").css('background-color','#FFFFDF');
            valid = false;
        }
        if(!$("#minage_type").val()) {
            $("#min_age-info").html("(*)");
            $("#min_age-info").css('color','#F00');
            $("#minage_type").css('background-color','#FFFFDF');
            valid = false;
        }
        if(!$("#max_age").val()) {
            $("#max_age-info").html("(*)");
            $("#max_age").css('background-color','#FFFFDF');
            $("#max_age-info").css('color','#F00');
            valid = false;
        }
	}
		return valid;
}

function checkNewAge(){
if($("#age_range_name").val()=="new"){
		$(".new_age").show();
	}else{
		$(".new_age").hide();

	}

}

function save_vital_sign_form(){
        var valid = validateVs();
        if (valid){
                if($("#minage_type").val()=="year"){
                    min_age = $("#min_age").val()*12;
                }else{
                    min_age = $("#min_age").val();
                }
                if($("#maxage_type").val()=="year"){
                    max_age = $("#max_age").val()*12;
                }else{
                    max_age = $("#max_age").val();
                }
            $.ajax({
            url:"/save_vs_form",
            type:"POST",
            data:{tag:$("#tag").val(), description:$("#description").val(), minvalue:$("#minvalue").val(), maxvalue:$("#maxvalue").val(), new_age_range:$("#new_age_range").val(), age_range_name:$("#age_range_name").val(), min_age:min_age, max_age:max_age },
            success:function(data){
                if(data=="success"){
                    alert("Success");
                    load_vital_signs($("#tag").val());
                    $("#exampleModal").modal('hide').animate;
                }else if(data=="v-exist"){
                    $("#description-info").html("(Already Exist)");
                    $("#age_range_name-info").html("(Already Exist)");
		            $("#description").css('background-color','#FFFFDF');
		            $("#description-info").css('color','#F00');
                }else if(data=="exist"){
                    $("#new_age_range-info").html("(Already Exist)");
		            $("#new_age_range").css('background-color','#FFFFDF');
		            $("#new_age_range-info").css('color','#F00');
                }else if(data=="error"){
                    alert("Error");
                }else{
                    alert("Error");
                }
            }
            });
    }
}





function load_vital_sign_form(tab){

		$.ajax({
		url:"/load_vs_form",
		type:"POST",
		data:{tab:tab},
		success:function(data){
			$("#form_content").html(data);
		    $(".new_age").hide();
		    $("#tag").val(tab);

//			$("#btnSave").show();
//			$("#btnSave2").hide();
			$(".InputBox").css('background-color','');
			$(".info").html('');

            // $("#exampleModal").modal();
//				$("#danger-alert").hide();

		}
	    });



}

function load_vital_signs(vital_signs){
$.ajax({
	method: "POST",
	url: '/vital_sign',
	data: {vital_signs:vital_signs},
	success: function(data) {
		//if ((data.indexOf("No record found") > -1) || (data.indexOf("Date must be selected.") > -1)) {
			$('#vital_sign_panel').html(data);
			//$('#placeholder').hide();



//			chart.setData({
//				"xScale": "time",
//				"yScale": "linear",
//				"main": [{
//						className: ".stats",
//						data: []
//					}]
//			});
		//} else {
//			$('#msg').empty();
//			$('#placeholder').show();
//			var set = [];
//			$.each(data, function() {
//				set.push({
//					x: this.label,
//					y: parseInt(this.value, 10)
//				});
//			});
//			chart.setData({
//				"xScale": "time",
//				"yScale": "linear",
//				"main": [{
//						className: ".stats",
//						data: set
//					}]
//			});
		//}
	},
	error: function(err) {
	    alert(err)
		//console.log(err);
	}
});

}
$(function(){
	$('div[onload]').trigger('onload');
});
//$('#vital_signs_content').bind('MyAddEvent', function(){
//    alert('Was added');
//});