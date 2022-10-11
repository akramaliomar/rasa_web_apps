

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
	if(!$("#maxvalue").val()) {fetch_anomaly_recommendations
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
function validate_recommendation(){
    var valid = true;
	$(".InputBox").css('background-color','');
	$(".info").html('');
	if(!$("#description").val() ) {
		$("#description-info").html("(*)");
		$("#description").css('background-color','#FFFFDF');
		$("#description-info").css('color','#F00');
		valid = false;
	}
	if(!$("#reco_type").val()) {
		$("#reco_type-info").html("(*)");
		$("#reco_type").css('background-color','#FFFFDF');
		$("#reco_type-info").css('color','#F00');
		valid = false;
	}
	if(!$("#context").val()) {
		$("#context-info").html("(*)");
		$("#context").css('background-color','#FFFFDF');
		$("#context-info").css('color','#F00');
		valid = false;
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

function save_recommendation_form(){
        var valid = validate_recommendation();
        if (valid){
          $.ajax({
            url:"/save_reco_form",
            type:"POST",
            data:{reco_type:$("#reco_type").val(), description:$("#description").val(), context:$("#context").val(), health:JSON.stringify($("#health").val()) },
            success:function(data){
                if(data=="success"){
                    alert("Success");
                    load_recommendations();
                    $("#exampleModal").modal('hide').animate;
                }else if(data=="exist"){
                    $("#description-info").html("(Already Exist)");
                    $("#age_range_name-info").html("(Already Exist)");
		            $("#description").css('background-color','#FFFFDF');
		            $("#description-info").css('color','#F00');
                }else if(data=="error"){
                    alert("Error");
                }else{
                    alert("Error");
                }
            }
            });
    }
}


function save_anomaly_recommendation(diagnID){
        var valid = validate_recommendation();
        if (valid){
          $.ajax({
            url:"/save_new_reco_form",
            type:"POST",
            data:{diagnID:diagnID, reco_type:$("#reco_type").val(), description:$("#description").val(), context:$("#context").val(), health:JSON.stringify($("#health").val()) },
            success:function(data){
                if(data=="success"){
                    alert("Success");
                    fetch_anomaly_recommendations(diagnID);
                    fetch_recommendation_from(diagnID);
                }else if(data=="exist"){
                    $("#description-info").html("(Already Exist)");
                    $("#age_range_name-info").html("(Already Exist)");
		            $("#description").css('background-color','#FFFFDF');
		            $("#description-info").css('color','#F00');
                }else if(data=="error"){
                    alert("Error");
                }else{
                    alert("Error");
                }
            }
            });
    }
}



function update_medication(diagnID){
     var yourArray=[];
	$("input:checkbox[name=recommendationID]:checked").each(function(){
            yourArray.push($(this).val());
        });
        if(yourArray.length>0){
             recolist = JSON.stringify(yourArray);
            $.ajax({
            url:"/update_medication",
            type:"POST",
            data:{diagnID:diagnID, recolist:recolist},
            success:function(data){
                      alert(data);
                if(data=="success"){
                    alert("Success");
                    fetch_anomaly_recommendations(diagnID);
                    fetch_recommendation_from(diagnID);
                }

            }
            });
	    }else{
	        alert("Please tick at least one record");
	    }
}



function load_recommendation_form(){
		$.ajax({
		url:"/load_reco_form",
		type:"POST",
		data:{},
		success:function(data){
			$("#form_content").html(data);
			//$('#example').DataTable();
			$(".InputBox").css('background-color','');
			$(".info").html('');
		}
	    });
}

function load_recommendations(){
$.ajax({
	method: "POST",
	url: '/load_recommendations',
	data: {},
	success: function(data) {
	        no_medicated_abnormalities();
			$('#main_pannel').html(data);
            $('#example').DataTable();
	},
	error: function(err) {
	    alert(err)
		//console.log(err);
	}
});
}
function load_patient_abnormalities(){
$.ajax({
	method: "POST",
	url: '/load_abnormalities',
	data: {},
	success: function(data) {
	        no_medicated_abnormalities();
			$('#main_pannel').html(data);
            $('#abnormalities').DataTable();

	},
	error: function(err) {
	    alert(err)
		//console.log(err);
	}
});
}

function load_from_sensor(){
$.ajax({
	method: "POST",
	url: '/load_from_sensor',
	data: {},
	success: function(data) {
	        alert(data);
	        load_patient_abnormalities();
	},
	error: function(err) {
	    alert(err)
		//console.log(err);
	}
});
}

function no_medicated_abnormalities(){
$.ajax({
	method: "POST",
	url: '/abnormalities',
	data: {},
	success: function(data) {
			$('#non_ab').html("("+data+")");
	},
	error: function(err) {
	    alert(err)
		//console.log(err);
	}
});
}


function provide_medications(diagnID, age, tempr, hr, resp, sp, pr){
$.ajax({
	method: "POST",
	url: '/medication_panel',
	data: {diagnID:diagnID},
	success: function(data) {
			$('#med_content').html(data);
			var str = "Age["+ age+"] <----> Temperature["+tempr+"] <----> Breathing Rate["+hr+"] <----> Respiration["+resp+"] <----> Spo2["+sp+"] <----> Pressure ["+pr+"]";
			$('#medModalLabel').html(str);
			fetch_recommendation_from(diagnID);
			fetch_anomaly_recommendations(diagnID);
			// $('#example1').DataTable();
			// $('#example2').DataTable();
	},
	error: function(err) {
	    alert(err)
		//console.log(err);
	}
});
}

function fetch_recommendation_from(diagnID){
//health:JSON.stringify($("#health").val())
        if($("#from_reco").val()==1){
            var url = "/from_medication";
        }else if ($("#from_reco").val()==2){
            var url = "/new_recommendations";
        }else{
            var url = "/from_recommendations";
        }
$.ajax({
	method: "POST",
	url: url,
	data: {diagnID:diagnID, context:"Any"},
	success: function(data) {
			$('#loadFromID').html(data);
			$('#example2').DataTable();
	},
	error: function(err) {
	    alert(err)
		//console.log(err);
	}
});
}

function fetch_anomaly_recommendations(diagnID){
$.ajax({
	method: "POST",
	url: "/anomaly_recommendations",
	data: {diagnID:diagnID},
	success: function(data) {
			$('#loadAssignedID').html(data);
			$('#example1').DataTable();
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