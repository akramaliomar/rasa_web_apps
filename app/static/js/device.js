

function validate_device(){
    var valid = true;
	$(".InputBox").css('background-color','');
	$(".info").html('');
	if(!$("#device_no").val() ) {
		$("#device_no-info").html("(*)");
		$("#device_no").css('background-color','#FFFFDF');
		$("#device_no-info").css('color','#F00');
		valid = false;
	}
	if(!$("#device_code").val()) {
		$("#device_code-info").html("(*)");
		$("#device_code").css('background-color','#FFFFDF');
		$("#device_code-info").css('color','#F00');
		valid = false;
	}
		return valid;
}


function save_device_form(){
        var valid = validate_device();

        if (valid){
        alert("valid");
          $.ajax({
            url:"/save_device_form",
            type:"POST",
            data:{device_no:$("#device_no").val(), device_code:$("#device_code").val() },
            success:function(data){
            alert(data);
                if(data=="success"){
                    alert("Success");
                    load_device_list();
                }else if(data=="exist"){
                    $("#device_no-info").html("(Already Exist)");
		            $("#device_no").css('background-color','#FFFFDF');
		            $("#device_no-info").css('color','#F00');
                }else if(data=="error"){
                    alert("Error");
                }else{
                    alert("Error");
                }
            }
            });
    }
}


function load_device_form(){
		$.ajax({
		url:"/load_device_form",
		type:"POST",
		data:{},
		success:function(data){
			$("#device_panel").html(data);
			//$('#example').DataTable();
			$(".InputBox").css('background-color','');
			$(".info").html('');
		}
	    });
}

function load_device_list(){
		$.ajax({
		url:"/load_device_list",
		type:"POST",
		data:{},
		success:function(data){
			$("#device_panel").html(data);
			$('#example').DataTable();
			//$('#example').DataTable();
		}
	    });
}

function load_device_logs(){
		$.ajax({
		url:"/load_device_logs",
		type:"POST",
		data:{},
		success:function(data){
			$("#device_panel").html(data);
			$('#example').DataTable();
			//$('#example').DataTable();
		}
	    });
}
function load_specific_device_logs(){
		$.ajax({
		url:"/load_specific_device_logs",
		type:"POST",
		data:{deviceID:$("#deviceID").val()},
		success:function(data){
			$("#device_logs").html(data);
			$('#example').DataTable();
			//$('#example').DataTable();
		}
	    });
}

$(function(){
	$('div[onload]').trigger('onload');
});
//$('#vital_signs_content').bind('MyAddEvent', function(){
//    alert('Was added');
//});