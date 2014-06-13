function reload(){
	location.reload();
}


function visualization(content){
		document.getElementById('date-chart').innerHTML = '';
		callmap(content);
}

function drawpoints(listmarkers, content, map){
		a = new Date()
		if (content.length==0){
			for (i in listmarkers){
					listmarkers[i].setVisible(false);
				};
		}
		else{
				for (i in listmarkers){
					date1=(content[content.length-1].timestamp)*1000
					date2=(content[0].timestamp)*1000
					if ((listmarkers[i].date.getTime()>date1)&&(listmarkers[i].date.getTime()<date2)){
						listmarkers[i].setVisible(true);
					}
					else
					{
						listmarkers[i].setVisible(false);
					}
				}
		}
	}

//This function displays the map and the location points
function callmap(content){
		var map;
		var marker;
		var listmarkers=[];
		var infowindow= null;
		var mapOptions = {
		    zoom: 11,
		    center: new google.maps.LatLng(55.763516,12.494943),
		    mapTypeId: google.maps.MapTypeId.ROADMAP
		};
		$('#map-canvas').css('display', 'block'); 
		$('#results').css('display', 'none'); 			

		map = new google.maps.Map(document.getElementById('map-canvas'),mapOptions);

		infowindow = new google.maps.InfoWindow({
			content: "holding..."
		});
		
		for (var i=0; i<content.length; i++)
				{
					date=new Date(content[i]['timestamp']);
					longitude=content[i]['lat'];
					latitude=content[i]['lon'];
					point_new = new google.maps.LatLng(latitude,longitude);
					marker = new google.maps.Marker({
				            date:new Date(content[i]['timestamp']),
					    map:map,
					    draggable:false,
					    position: point_new,
					    clickable: true
					});
					var contentString='<div id="note">'+
							'<div id="Info">' +
								'<p id=dateinfo>Date: '+ 
								date.getFullYear() + '/' + 
								(date.getMonth()+1) + '/' + 
								date.getDate() + ' ' +
								date.getHours() + ':' +
								(date.getMinutes()+1) + ':' +
								date.getSeconds() +
								'</p>'+
								'<p id=locationinfo>Location: '+ longitude + ', ' + latitude + '</p>'+
							'</div>'+
							'</div>';

					marker.note = contentString;

					google.maps.event.addListener(marker, 'mouseover', function() {
						infowindow.content=this.note;
						infowindow.open(map, this);
   					});
					listmarkers.push(marker)
				}
		callchart(content,listmarkers,map);
}


	function callchart(flights,markers,map){
	$('#totals').css('display','block');
	$('#date-chart').css('display', 'block'); 
	
	  // Various formatters.
	var formatNumber = d3.format(",d");
	var indexes=new Array();

	//There are no valid Timestamps in the dataset so we remove them
	//First we find their indexes
	for (var i=0;  i<flights.length; i++)
		{
			dia=flights[i]['timestamp']
			if (dia<1375308000000){
				indexes.push(i)
			}
		}
	//Second, we delete them from the dataset
	for (var m=0; m<indexes.length; m++)
		{
			flights.splice(indexes[m]-m,1);
		}	


	flights.forEach(function(d, i) {
			d.index = i;
	    		d.date = new Date(d.timestamp*1000);
	  });

	
	  // A nest operator, for grouping the flight list.
	  var nestByDate = d3.nest()
	      .key(function(d) {return d.date; });
	  

	  // Create the crossfilter for the relevant dimensions and groups.
	      var flight = crossfilter(flights),
	      all = flight.groupAll(),
		  hour = flight.dimension(function(d) { return d.date.getHours() + d.date.getMinutes() / 60; }),
      	      hours = hour.group(Math.floor),
	      date = flight.dimension(function(d) { return d.date; }),
	      dates = date.group(d3.time.day);
	
	// Create this variables for the chart domain and filter
	firstdatedomain=new Date((date.top(flight.size())[flight.size()-1].timestamp)*1000)
	lastdatedomain=new Date((date.top(1)[0].timestamp)*1000)

	var margin = {top: 40, right: 40, bottom: 40, left:40},
	    width = 900;

	//If in the dataset of the request we only have date from one day, we show a 24hours chart  
		if (dates.size()==1){
			var charts = [
			      barChart()
				.dimension(hour)
				.group(hours)
			      .x(d3.scale.linear()
				.domain([0, 24])
				.rangeRound([0, 240]))
				.filter([4,22])
			  ];
		}
	//If we have more than one day data, we show a more than one day chart
		else {
			var charts = [
				    barChart()
					.dimension(date)
					.group(dates)
					.round(d3.time.day.round)
				      .x(d3.time.scale()
					.domain([firstdatedomain, d3.time.day.offset(lastdatedomain, 1)])
					.rangeRound([0, width - margin.left - margin.right]))
					.filter([firstdatedomain,lastdatedomain])
				      
			];
		}
	

	  // Given our array of charts, which we assume are in the same order as the
	  // .chart elements in the DOM, bind the charts to the DOM and render them.
	  // We also listen to the chart's brush events to update the display.
	  var chart = d3.selectAll(".chart")
	      .data(charts)
	      .each(function(chart) { chart.on("brush", renderAll).on("brushend", renderAll); });

	  // Render the total.
	  d3.selectAll("#total")
	      .text(formatNumber(flight.size()));
	
	  renderAll();

	  // Renders the specified chart or list.
	  function render(method) {
	    d3.select(this).call(method);
	  }

	  // Whenever the brush moves, re-rendering everything.
	  function renderAll() {
		a = new Date();
		chart.each(render);
	    	d3.select("#active").text(formatNumber(all.value()));
		content=JSON.parse(JSON.stringify(date.top(Infinity)))
		//console.log(JSON.stringify(date.top(Infinity)))
	    	drawpoints(markers, content, map);
		//console.log('renderAll: ' + (new Date().getTime() - a.getTime()) + ' ms');  
	  }

	  window.filter = function(filters) {
	    filters.forEach(function(d, i) { charts[i].filter(d); });
	    renderAll();
	  };

	  window.reset = function(i) {
	    charts[i].filter(null);
	    renderAll();
	  };

	  function barChart() {
	    if (!barChart.id) barChart.id = 0;

	    var margin = {top: 10, right: 10, bottom: 20, left: 10},
		x,
		y = d3.scale.linear().range([100, 0]),
		id = barChart.id++,
		axis = d3.svg.axis().orient("bottom"),
		brush = d3.svg.brush(),
		brushDirty,
		dimension,
		group,
		round;

	    function chart(div) {
	      var width = x.range()[1],
		  height = y.range()[0];

	      y.domain([0, group.top(1)[0].value]);

	      div.each(function() {
		var div = d3.select(this),
		    g = div.select("g");

		// Create the skeletal chart.
		if (g.empty()) {
		  div.select(".title").append("a")
		      .attr("href", "javascript:reset(" + id + ")")
		      .attr("class", "reset")
		      .text("reset")
		      .style("display", "none");

		  g = div.append("svg")
		      .attr("width", width + margin.left + margin.right)
		      .attr("height", height + margin.top + margin.bottom)
		    .append("g")
		      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		  g.append("clipPath")
		      .attr("id", "clip-" + id)
		    .append("rect")
		      .attr("width", width)
		      .attr("height", height);

		  g.selectAll(".bar")
		      .data(["background", "foreground"])
		    .enter().append("path")
		      .attr("class", function(d) { return d + " bar"; })
		      .datum(group.all());

		  g.selectAll(".foreground.bar")
		      .attr("clip-path", "url(#clip-" + id + ")");

		  g.append("g")
		      .attr("class", "axis")
		      .attr("transform", "translate(0," + height + ")")
		      .call(axis);

		  // Initialize the brush component with pretty resize handles.
		  var gBrush = g.append("g").attr("class", "brush").call(brush);
		  gBrush.selectAll("rect").attr("height", height);
		  gBrush.selectAll(".resize").append("path").attr("d", resizePath);
		}

		// Only redraw the brush if set externally.
		if (brushDirty) {
		  brushDirty = false;
		  g.selectAll(".brush").call(brush);
		  div.select(".title a").style("display", brush.empty() ? "none" : null);
		  if (brush.empty()) {
		    g.selectAll("#clip-" + id + " rect")
		        .attr("x", 0)
		        .attr("width", width);
		  } else {
		    var extent = brush.extent();
		    g.selectAll("#clip-" + id + " rect")
		        .attr("x", x(extent[0]))
		        .attr("width", x(extent[1]) - x(extent[0]));
		  }
		}

		g.selectAll(".bar").attr("d", barPath);
	      });

	      function barPath(groups) {
		var path = [],
		    i = -1,
		    n = groups.length,
		    d;
		while (++i < n) {
		  d = groups[i];
		  path.push("M", x(d.key), ",", height, "V", y(d.value), "h9V", height);
		}
		return path.join("");
	      }

	      function resizePath(d) {
		var e = +(d == "e"),
		    x = e ? 1 : -1,
		    y = height / 3;
		return "M" + (.5 * x) + "," + y
		    + "A6,6 0 0 " + e + " " + (6.5 * x) + "," + (y + 6)
		    + "V" + (2 * y - 6)
		    + "A6,6 0 0 " + e + " " + (.5 * x) + "," + (2 * y)
		    + "Z"
		    + "M" + (2.5 * x) + "," + (y + 8)
		    + "V" + (2 * y - 8)
		    + "M" + (4.5 * x) + "," + (y + 8)
		    + "V" + (2 * y - 8);
	      }
	    }

	    brush.on("brushstart.chart", function() {
	      var div = d3.select(this.parentNode.parentNode.parentNode);
	      div.select(".title a").style("display", null);
	    });

	    brush.on("brush.chart", function() {
	      var g = d3.select(this.parentNode),
		  extent = brush.extent();
	      if (round) g.select(".brush")
		  .call(brush.extent(extent = extent.map(round)))
		.selectAll(".resize")
		  .style("display", null);
	      g.select("#clip-" + id + " rect")
		  .attr("x", x(extent[0]))
		  .attr("width", x(extent[1]) - x(extent[0]));
	      dimension.filterRange(extent);
	    });

	    brush.on("brushend.chart", function() {
	      if (brush.empty()) {
		var div = d3.select(this.parentNode.parentNode.parentNode);
		div.select(".title a").style("display", "none");
		div.select("#clip-" + id + " rect").attr("x", null).attr("width", "100%");
		dimension.filterAll();
	      }
	    });

	    chart.margin = function(_) {
	      if (!arguments.length) return margin;
	      margin = _;
	      return chart;
	    };

	    chart.x = function(_) {
	      if (!arguments.length) return x;
	      x = _;
	      axis.scale(x);
	      brush.x(x);
	      return chart;
	    };

	    chart.y = function(_) {
	      if (!arguments.length) return y;
	      y = _;
	      return chart;
	    };

	    chart.dimension = function(_) {
	      if (!arguments.length) return dimension;
	      dimension = _;
	      return chart;
	    };

	    chart.filter = function(_) {
	      if (_) {
		brush.extent(_);
		dimension.filterRange(_);
	      } else {
		brush.clear();
		dimension.filterAll();
	      }
	      brushDirty = true;
	      return chart;
	    };

	    chart.group = function(_) {
	      if (!arguments.length) return group;
	      group = _;
	      return chart;
	    };

	    chart.round = function(_) {
	      if (!arguments.length) return round;
	      round = _;
	      return chart;
	    };

	    return d3.rebind(chart, brush, "on");
	  }		
	}
