var canvas;
var ctx;

var color = Chart.helpers.color;

var done = false ; 

var bubbleChartData = {
	animation: {
		duration: 10000
	},
	datasets: [{
		backgroundColor: color(window.chartColors.red).alpha(0.5).rgbString(),
		borderColor: window.chartColors.red,
		borderWidth: 1,
		label : 'Points (distance, calories)', 
		data: []
	}, {
		
		backgroundColor: color(window.chartColors.blue).alpha(0.5).rgbString(),
		borderColor: window.chartColors.blue,
		borderWidth: 1,
		type : 'line', 
		fill: false,
		label : 'Line of best fit', 
		data: [{
			x: 0,
			y: 0,
			r: 1,
		}, {
			x: 1,
			y: 0,
			r: 1,
		
		}, {
			x : 90, 
			y : 0, 
			r : 1
		}]
	}]
};


// mX + b ---> Line of best fit 
var m = 0; 
var b = 0; 
// points (distance, calories)
var points;

var learningRate = 0.0001;

// Saving the error values
var errorC = 0; 

// Compute error : calculate the distance between the line of best fit and each point of the graph. 
function compute_error(){
	var error = 0; 
	for (var i = 0; i <  points.length ; i++) {
		x = points[i].x; 
		y = points[i].y; 
		error += Math.pow(y - (m *x + b), 2 ); 

	}
 
	errorC = error/points.length; 
	return error/points.length; 
}

// Minimize the error function 
function next_mb(m_current, b_current, points, learningRate){
	var deriv_m = 0; 
	var deriv_b = 0; 

	for (var i = 0; i <  points.length ; i++) {
		x = points[i].x; 
		y = points[i].y; 
		deriv_m += -(2/points.length) * x * (y - ((m_current * x) + b_current)); 
		deriv_b += -(2/points.length) * (y - ((m_current * x) + b_current)); 
	}
	var next_m = m_current - (learningRate * deriv_m); 
	var next_b = b_current - (learningRate * deriv_b); 
	return [next_b, next_m]; 
}


$(document).ready(function() {

	canvas = document.getElementById("canvas");
	ctx = canvas.getContext("2d");

	// Getting the csv data using ajax. 
	$.ajax({
        type: "GET",
        url: "./Data.csv",
        dataType: "text",
        success: function (data) { processData(data); }
    });
	
    function processData(allText) {
		
		var allLinesArray = allText.split('\n');
        if (allLinesArray.length > 0) {
            var dataPoints = [];
            for (var i = 0; i <= allLinesArray.length - 1; i++) {
	        var rowData = allLinesArray[i].split(',');
	        if(rowData && rowData.length > 1)
	            dataPoints.push({ x: rowData[0], y: rowData[1], r : 4 });
			}
			points = dataPoints; 
			console.log(dataPoints); 
			bubbleChartData.datasets[0].data = dataPoints; 
		}

		console.log("m = " , m ," b = ", b);

		window.myChart = new Chart(ctx, {
			type: 'bubble',
			data: bubbleChartData,
			animationEnabled: true, 
			options: {
				maintainAspectRatio: false,
				responsive: true,
				title: {
					display: true,
					text: ''
				},
				tooltips: {
					mode: 'point'
				}
			}
		});

		 
	}



	/* setInterval(function (){	if (done ){
		console.log(errors); 
		graph3d(); 
	}}, 1000); */
}); 

function run(){
	
	var t = next_mb(m , b , points, learningRate); 
	b = t[0]; 
	m = t[1];
	
	changeData(); 
	compute_error(); 
}

function changeData(){

	bubbleChartData.datasets[1].data.pop(); 
	bubbleChartData.datasets[1].data.pop();
	bubbleChartData.datasets[1].data.pop();

	bubbleChartData.datasets[1].data.push({x : 0,y : b,r : 1}); 
	bubbleChartData.datasets[1].data.push({x : 1,y : m+b,r : 1}); 
	bubbleChartData.datasets[1].data.push({x : 90 , y : m*90+b , r : 1});
	
	window.myChart.update(); 
}

// UI Updates
$('input').change(function() {
	$('h2[id = result]').text(Math.trunc(m * $('input').val() + b)); 
}); 

document.getElementById('runIter').addEventListener('click', function() {
	console.log("Run iter 1"); 
	if (bubbleChartData.datasets.length > 0) {
		run(); 
		updateExplanation(); 
	}
});

document.getElementById('runAll').addEventListener('click', function() {
	if (bubbleChartData.datasets.length > 0) {
		for(var i = 0 ; i < 1000 ; i++){
			run();
			
		}
		compute_error(); 
		updateExplanation(); 
		done = true; 
	}
});

function updateExplanation(){
	document.getElementById('explanation').innerHTML = " m = "+ m + "<br> b = " + b +"<br> error = " + errorC; 
}


// Need to be fixed
function graph3d(){
	Plotly.d3.csv('Data.csv', function(err, rows){
		function unpack(rows, key) {
		  return rows.map(function(row) { return row[key]; });
		}
		  
		var z_data = errors ; 
		
		var data = [{
				   z: z_data,
				   type: 'surface'
				}];
		  
		var layout = {
		  title: 'Error - Distance - Calories',
		  autosize: false,
		  width: 500,
		  height: 500,
		  margin: {
			l: 65,
			r: 50,
			b: 65,
			t: 90,
		  }
		};
		Plotly.newPlot('myDiv', data, layout);
		});
}