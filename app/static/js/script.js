
/* module for importing other js files */
function include(file) {
  const script = document.createElement('script');
  script.src = file;
  script.type = 'text/javascript';
  script.defer = true;

  document.getElementsByTagName('head').item(0).appendChild(script);
}


// Bot pop-up intro
document.addEventListener("DOMContentLoaded", () => {
  const elemsTap = document.querySelector(".tap-target");
  // eslint-disable-next-line no-undef
  const instancesTap = M.TapTarget.init(elemsTap, {});
  instancesTap.open();
  setTimeout(() => {
    instancesTap.close();
  }, 4000);
});

/* import components */
include('./static/js/components/index.js');

window.addEventListener('load', () => {
  // initialization
  $(document).ready(() => {
    // Bot pop-up intro
    $("div").removeClass("tap-target-origin");

    // drop down menu for close, restart conversation & clear the chats.
    $(".dropdown-trigger").dropdown();

    // initiate the modal for displaying the charts,
    // if you dont have charts, then you comment the below line
    $(".modal").modal();

    // enable this if u have configured the bot to start the conversation.
    // showBotTyping();
    // $("#userInput").prop('disabled', true);

    // if you want the bot to start the conversation
    // customActionTrigger();
  });
  // Toggle the chatbot screen
  $("#profile_div").click(() => {
    $(".profile_div").toggle();
    $(".widget").toggle();
  });

  // clear function to clear the chat contents of the widget.
  $("#clear").click(() => {
    $(".chats").fadeOut("normal", () => {
      $(".chats").html("");
      $(".chats").fadeIn();
    });
  });

  // close function to close the widget.
  $("#close").click(() => {
    $(".profile_div").toggle();
    $(".widget").toggle();
    scrollToBottomOfResults();
  });
});


function load_vital_signs(){
    alert("hello")
$.ajax({
	method: "POST",
	url: '/fetch_vital_sign',
	contentType: 'application/json;charset=UTF-8',
	data: JSON.stringify({'data':"hello world"}),
	dataType: "json",
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
		console.log(err);
	}
});

}