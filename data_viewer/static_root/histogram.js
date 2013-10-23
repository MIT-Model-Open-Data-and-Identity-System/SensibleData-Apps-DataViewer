function reload(){
	histogram.reload();
}


function visualization(results){
	countlist=[]
	answers=[]
	data=[]
	
	if (results.length>0){
		for (i=0;i<results.length;i++){
			if (results[i].human_readable_response in countlist){
				countlist[results[i].human_readable_response]=countlist[results[i].human_readable_response]+1;
			}
			else {
				countlist[results[i].human_readable_response]=1;
				
			}
		}
	}
	
	newlist=countlist
	keysanswers=Object.keys(newlist);
	maxval=0

	for (i=0;i<keysanswers.length;i++){
		val=countlist[keysanswers[i]]/1000;
		data.push({'letter':keysanswers[i], 'frequency':val})
		if (val>maxval){maxval=val}
	}

	BuildData(data,keysanswers,maxval)

}

function BuildData(data,answers,maxval){
	document.getElementById('histogram').innerHTML = '';

	$('#histogram').css('display', 'block');
	var margin = {top: 20, right: 20, bottom: 400, left: 40},
	    width = 560 - margin.left - margin.right,
	   height = 1000 - margin.top - margin.bottom;

	var formatPercent = d3.format(".0%");

	var x = d3.scale.ordinal()
	    .rangeRoundBands([0, width], .1);

	var y = d3.scale.linear()
	    .range([height, 0]);

	var xAxis = d3.svg.axis()
	    .scale(x)
	    .orient("bottom");

	var yAxis = d3.svg.axis()
	    .scale(y)
	    .orient("left")
	    .tickFormat(formatPercent);

	var svg = d3.select("#histogram").append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	
	  x.domain(answers);
	  y.domain([0,maxval])

	  svg.append("g")
	      .attr("class", "x axis")
	      .attr("transform", "translate(0," + height + ")")
	      .call(xAxis)
	      .selectAll("text")  
              	.style("text-anchor", "end")
            	.attr("x", -6)
            	.attr("dx", ".50em")
            	.attr("transform", function(d) {
                	return "rotate(-90)" 
                });

	  svg.append("g")
	      .attr("class", "y axis")
	      .call(yAxis)
	    .append("text")
	      .attr("transform", "rotate(-90)")
	      .attr("y", 6)
	      .attr("dy", ".71em")
	      .style("text-anchor", "end")
	      .text("Percent");

	  svg.selectAll(".bar")
	      .data(data)
	    .enter().append("rect")
	      .attr("class", "bar")
	      .attr("x", function(d) { return x(d.letter); })
	      .attr("width", x.rangeBand())
	      .attr("y", function(d) { return y(d.frequency); })
	      .attr("height", function(d) { return (height - y(d.frequency)); });

	function type(d) {
	  d.frequency = +d.frequency;
	  return d;
	}
}

