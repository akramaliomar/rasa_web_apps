function load_temperature_chart() {

    // Set the default dates
    var startDate = Date.create().addDays(-6), // 7 days ago
            endDate = Date.create(); 				// today

    var range = $('#range');

    // Show the dates in the range input
    range.val(startDate.format('{MM}/{dd}/{yyyy}') + ' - ' + endDate.format('{MM}/{dd}/{yyyy}'));

    // Load chart
    ajaxLoadChart(startDate, endDate);

    range.daterangepicker({
        startDate: startDate,
        endDate: endDate,
        ranges: {
            'Today': ['today', 'today'],
            'Yesterday': ['yesterday', 'yesterday'],
            'Last 7 Days': [Date.create().addDays(-6), 'today'],
            'Last 30 Days': [Date.create().addDays(-29), 'today']
        }
    }, function(start, end) {

        ajaxLoadChart(start, end);

    });

    // The tooltip shown over the chart
    var tt = $('<div class="ex-tooltip">').appendTo('body'),
            topOffset = -32;

    var data = {
        "xScale": "time",
        "yScale": "linear",
        "main": [{
                className: ".stats",
                "data": []
            }]
    };

    var opts = {
        paddingLeft: 50,
        paddingTop: 20,
        paddingRight: 10,
        axisPaddingLeft: 25,
        tickHintX: 9, // How many ticks to show horizontally

        dataFormatX: function(x) {

            // This turns converts the timestamps coming from
            // ajax.php into a proper JavaScript Date object

            return Date.create(x);
        },
        tickFormatX: function(x) {

            // Provide formatting for the x-axis tick labels.
            // This uses sugar's format method of the date object. 

            return x.format('{MM}/{dd}');
        },
        "mouseover": function(d, i) {
            var pos = $(this).offset();

            tt.text(d.x.format('{Month} {ord}') + ', No. of visits: ' + d.y).css({
                top: topOffset + pos.top,
                left: pos.left

            }).show();
        },
        "mouseout": function(x) {
            tt.hide();
        }
    };

    // Create a new xChart instance, passing the type
    // of chart a data set and the options object

    var chart = new xChart('line-dotted', data, '#temp_chart', opts);

    // Function for loading data via AJAX and showing it on the chart
    function ajaxLoadChart(startDate, endDate) {

        // If no data is passed (the chart was cleared)

        if (!startDate || !endDate) {
            chart.setData({
                "xScale": "time",
                "yScale": "linear",
                "main": [{
                        className: ".stats",
                        data: []
                    }]
            });

            return;
        }

        // Otherwise, issue an AJAX request		
		$.ajax({
			method: "POST",
			url: '/temp_xchart',
			contentType: 'application/json;charset=UTF-8',
			data: JSON.stringify({'deviceNo':$("#device_no").val(),'start': startDate.format('{yyyy}-{MM}-{dd}'), 'end': endDate.format('{yyyy}-{MM}-{dd}')}),
			dataType: "json",
			success: function(data) {
				if ((data.indexOf("No record found") > -1) || (data.indexOf("Date must be selected.") > -1)) {
					$('#temp_msg').html('<span style="color:red;">' + data + '</span>');
					$('#temp_placeholder').hide();
					chart.setData({
						"xScale": "time",
						"yScale": "linear",
						"main": [{
								className: ".stats",
								data: []
							}]
					});
				} else {


					$('#temp_msg').empty();
					$('#temp_placeholder').show();
					var set = [];
					$.each(data, function() {
						set.push({
							x: this.label,
							y: parseInt(this.value, 10)
						});
					});
					chart.setData({
						"xScale": "time",
						"yScale": "linear",
						"main": [{
								className: ".stats",
								data: set
							}]
					});
					//alert("temp check chart");


				}
			},
			error: function(err) {
				console.log(err);
			}
		});
    }
}

function load_heart_chart() {

    // Set the default dates
    var startDate = Date.create().addDays(-6), // 7 days ago
            endDate = Date.create(); 				// today

    var range = $('#range');

    // Show the dates in the range input
    range.val(startDate.format('{MM}/{dd}/{yyyy}') + ' - ' + endDate.format('{MM}/{dd}/{yyyy}'));

    // Load chart
    ajaxLoadChart1(startDate, endDate);

    range.daterangepicker({
        startDate: startDate,
        endDate: endDate,
        ranges: {
            'Today': ['today', 'today'],
            'Yesterday': ['yesterday', 'yesterday'],
            'Last 7 Days': [Date.create().addDays(-6), 'today'],
            'Last 30 Days': [Date.create().addDays(-29), 'today']
        }
    }, function(start, end) {

        ajaxLoadChart1(start, end);

    });

    // The tooltip shown over the chart
    var tt = $('<div class="ex-tooltip">').appendTo('body'),
            topOffset = -32;

    var data = {
        "xScale": "time",
        "yScale": "linear",
        "main": [{
                className: ".stats1",
                "data": []
            }]
    };

    var opts = {
        paddingLeft: 50,
        paddingTop: 20,
        paddingRight: 10,
        axisPaddingLeft: 25,
        tickHintX: 9, // How many ticks to show horizontally

        dataFormatX: function(x) {

            // This turns converts the timestamps coming from
            // ajax.php into a proper JavaScript Date object

            return Date.create(x);
        },
        tickFormatX: function(x) {

            // Provide formatting for the x-axis tick labels.
            // This uses sugar's format method of the date object.

            return x.format('{MM}/{dd}');
        },
        "mouseover": function(d, i) {
            var pos = $(this).offset();

            tt.text(d.x.format('{Month} {ord}') + ', No. of visits: ' + d.y).css({
                top: topOffset + pos.top,
                left: pos.left

            }).show();
        },
        "mouseout": function(x) {
            tt.hide();
        }
    };

    // Create a new xChart instance, passing the type
    // of chart a data set and the options object

    var chart = new xChart('line-dotted', data, '#heart_chart', opts);

    // Function for loading data via AJAX and showing it on the chart
    function ajaxLoadChart1(startDate, endDate) {

        // If no data is passed (the chart was cleared)

        if (!startDate || !endDate) {
            chart.setData({
                "xScale": "time",
                "yScale": "linear",
                "main": [{
                        className: ".stats1",
                        data: []
                    }]
            });

            return;
        }

        // Otherwise, issue an AJAX request
		$.ajax({
			method: "POST",
			url: '/heart_xchart',
			contentType: 'application/json;charset=UTF-8',
			data: JSON.stringify({'deviceNo':$("#device_no").val(), 'start': startDate.format('{yyyy}-{MM}-{dd}'), 'end': endDate.format('{yyyy}-{MM}-{dd}')}),
			dataType: "json",
			success: function(data) {
				if ((data.indexOf("No record found") > -1) || (data.indexOf("Date must be selected.") > -1)) {
					$('#heart_msg').html('<span style="color:red;">' + data + '</span>');
					$('#heart_placeholder').hide();
					chart.setData({
						"xScale": "time",
						"yScale": "linear",
						"main": [{
								className: ".stats1",
								data: []
							}]
					});
				} else {


					$('#heart_msg').empty();
					$('#heart_placeholder').show();
					var set = [];
					$.each(data, function() {
						set.push({
							x: this.label,
							y: parseInt(this.value, 10)
						});
					});
					//alert("before heart check chart");

					chart.setData({
						"xScale": "time",
						"yScale": "linear",
						"main": [{
								className: ".stats1",
								data: set
							}]
					});
						//alert("heart check chart");


				}
			},
			error: function(err) {
				console.log(err);
			}
		});
    }
}


function load_resp_chart() {

    // Set the default dates
    var startDate = Date.create().addDays(-6), // 7 days ago
            endDate = Date.create(); 				// today

    var range = $('#range');

    // Show the dates in the range input
    range.val(startDate.format('{MM}/{dd}/{yyyy}') + ' - ' + endDate.format('{MM}/{dd}/{yyyy}'));

    // Load chart
    ajaxLoadChart1(startDate, endDate);

    range.daterangepicker({
        startDate: startDate,
        endDate: endDate,
        ranges: {
            'Today': ['today', 'today'],
            'Yesterday': ['yesterday', 'yesterday'],
            'Last 7 Days': [Date.create().addDays(-6), 'today'],
            'Last 30 Days': [Date.create().addDays(-29), 'today']
        }
    }, function(start, end) {

        ajaxLoadChart1(start, end);

    });

    // The tooltip shown over the chart
    var tt = $('<div class="ex-tooltip">').appendTo('body'),
            topOffset = -32;

    var data = {
        "xScale": "time",
        "yScale": "linear",
        "main": [{
                className: ".stats1",
                "data": []
            }]
    };

    var opts = {
        paddingLeft: 50,
        paddingTop: 20,
        paddingRight: 10,
        axisPaddingLeft: 25,
        tickHintX: 9, // How many ticks to show horizontally

        dataFormatX: function(x) {

            // This turns converts the timestamps coming from
            // ajax.php into a proper JavaScript Date object

            return Date.create(x);
        },
        tickFormatX: function(x) {

            // Provide formatting for the x-axis tick labels.
            // This uses sugar's format method of the date object.

            return x.format('{MM}/{dd}');
        },
        "mouseover": function(d, i) {
            var pos = $(this).offset();

            tt.text(d.x.format('{Month} {ord}') + ', No. of visits: ' + d.y).css({
                top: topOffset + pos.top,
                left: pos.left

            }).show();
        },
        "mouseout": function(x) {
            tt.hide();
        }
    };

    // Create a new xChart instance, passing the type
    // of chart a data set and the options object

    var chart = new xChart('line-dotted', data, '#resp_chart', opts);

    // Function for loading data via AJAX and showing it on the chart
    function ajaxLoadChart1(startDate, endDate) {

        // If no data is passed (the chart was cleared)

        if (!startDate || !endDate) {
            chart.setData({
                "xScale": "time",
                "yScale": "linear",
                "main": [{
                        className: ".stats1",
                        data: []
                    }]
            });

            return;
        }

        // Otherwise, issue an AJAX request
		$.ajax({
			method: "POST",
			url: '/resp_xchart',
			contentType: 'application/json;charset=UTF-8',
			data: JSON.stringify({'deviceNo':$("#device_no").val(), 'start': startDate.format('{yyyy}-{MM}-{dd}'), 'end': endDate.format('{yyyy}-{MM}-{dd}')}),
			dataType: "json",
			success: function(data) {
				if ((data.indexOf("No record found") > -1) || (data.indexOf("Date must be selected.") > -1)) {
					$('#resp_msg').html('<span style="color:red;">' + data + '</span>');
					$('#resp_placeholder').hide();
					chart.setData({
						"xScale": "time",
						"yScale": "linear",
						"main": [{
								className: ".stats1",
								data: []
							}]
					});
				} else {


					$('#resp_msg').empty();
					$('#resp_placeholder').show();
					var set = [];
					$.each(data, function() {
						set.push({
							x: this.label,
							y: parseInt(this.value, 10)
						});
					});

					chart.setData({
						"xScale": "time",
						"yScale": "linear",
						"main": [{
								className: ".stats1",
								data: set
							}]
					});


				}
			},
			error: function(err) {
				console.log(err);
			}
		});
    }
}

function load_spo2_chart() {

    // Set the default dates
    var startDate = Date.create().addDays(-6), // 7 days ago
            endDate = Date.create(); 				// today

    var range = $('#range');

    // Show the dates in the range input
    range.val(startDate.format('{MM}/{dd}/{yyyy}') + ' - ' + endDate.format('{MM}/{dd}/{yyyy}'));

    // Load chart
    ajaxLoadChart1(startDate, endDate);

    range.daterangepicker({
        startDate: startDate,
        endDate: endDate,
        ranges: {
            'Today': ['today', 'today'],
            'Yesterday': ['yesterday', 'yesterday'],
            'Last 7 Days': [Date.create().addDays(-6), 'today'],
            'Last 30 Days': [Date.create().addDays(-29), 'today']
        }
    }, function(start, end) {

        ajaxLoadChart1(start, end);

    });

    // The tooltip shown over the chart
    var tt = $('<div class="ex-tooltip">').appendTo('body'),
            topOffset = -32;

    var data = {
        "xScale": "time",
        "yScale": "linear",
        "main": [{
                className: ".stats1",
                "data": []
            }]
    };

    var opts = {
        paddingLeft: 50,
        paddingTop: 20,
        paddingRight: 10,
        axisPaddingLeft: 25,
        tickHintX: 9, // How many ticks to show horizontally

        dataFormatX: function(x) {

            // This turns converts the timestamps coming from
            // ajax.php into a proper JavaScript Date object

            return Date.create(x);
        },
        tickFormatX: function(x) {

            // Provide formatting for the x-axis tick labels.
            // This uses sugar's format method of the date object.

            return x.format('{MM}/{dd}');
        },
        "mouseover": function(d, i) {
            var pos = $(this).offset();

            tt.text(d.x.format('{Month} {ord}') + ', No. of visits: ' + d.y).css({
                top: topOffset + pos.top,
                left: pos.left

            }).show();
        },
        "mouseout": function(x) {
            tt.hide();
        }
    };

    // Create a new xChart instance, passing the type
    // of chart a data set and the options object

    var chart = new xChart('line-dotted', data, '#spo2_chart', opts);

    // Function for loading data via AJAX and showing it on the chart
    function ajaxLoadChart1(startDate, endDate) {

        // If no data is passed (the chart was cleared)

        if (!startDate || !endDate) {
            chart.setData({
                "xScale": "time",
                "yScale": "linear",
                "main": [{
                        className: ".stats1",
                        data: []
                    }]
            });

            return;
        }

        // Otherwise, issue an AJAX request
		$.ajax({
			method: "POST",
			url: '/spo2_xchart',
			contentType: 'application/json;charset=UTF-8',
			data: JSON.stringify({'deviceNo':$("#device_no").val(), 'start': startDate.format('{yyyy}-{MM}-{dd}'), 'end': endDate.format('{yyyy}-{MM}-{dd}')}),
			dataType: "json",
			success: function(data) {
				if ((data.indexOf("No record found") > -1) || (data.indexOf("Date must be selected.") > -1)) {
					$('#spo2_msg').html('<span style="color:red;">' + data + '</span>');
					$('#spo2_placeholder').hide();
					chart.setData({
						"xScale": "time",
						"yScale": "linear",
						"main": [{
								className: ".stats1",
								data: []
							}]
					});
				} else {


					$('#spo2_msg').empty();
					$('#spo2_placeholder').show();
					var set = [];
					$.each(data, function() {
						set.push({
							x: this.label,
							y: parseInt(this.value, 10)
						});
					});

					chart.setData({
						"xScale": "time",
						"yScale": "linear",
						"main": [{
								className: ".stats1",
								data: set
							}]
					});


				}
			},
			error: function(err) {
				console.log(err);
			}
		});
    }
}

function load_vital_signs_chart(){
        $(".v_sign").hide();
         $("#temp").show();

        load_temperature_chart();

        setTimeout(function(){
                     $("#heart").show();

             load_heart_chart();

        },100);

        setTimeout(function(){
                 $("#resp").show();

             load_resp_chart();

        },200);

        setTimeout(function(){
                 $("#spo2").show();

             load_spo2_chart();

        },300);
}

function load_device_data(){
$.ajax({
	method: "POST",
	url: "/load_device_data",
	data: {'device_no':$("#device_no").val()},
	success: function(data) {
                  $("#current_vs").html(data);
			}

			});
    load_vital_signs_chart();
}
