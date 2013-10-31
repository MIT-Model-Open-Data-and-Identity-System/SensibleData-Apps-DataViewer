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
	percent=0;
	maxval=0

	if (results.length<=10){percent=10}
	else if(results.length>10 && results.length<=100){percent=10}
	else if(results.length>100 && results.length<=1000){percent=1000}

	for (i=0;i<keysanswers.length;i++){
		val=countlist[keysanswers[i]];
		freq=val/results.length
		data.push({'letter':keysanswers[i], 'frequency':freq})
		if (freq>maxval){maxval=freq}
	}

	BuildData(data,keysanswers,maxval)

}

function BuildData(data,answers,maxval){
	document.getElementById('histogram').innerHTML = '';
	document.getElementById('scatterplot').innerHTML = '';
				
	$('#histogram').css('display', 'block');
	var margin = {top: 40, right: 40, bottom: 40, left: 40},
	    width = 75*answers.length - margin.left - margin.right,
	   height = 500 - margin.top - margin.bottom;

	var formatPercent = d3.format(".00%");

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

	var div = d3.select("#histogram").append("div")   
	    .attr("class", "tooltip")               
	    .style("opacity", 0);


	ans=[];
	for (i=0;i<answers.length;i++){
		ans.push({'answer':answers[i]})
	}	

	
	  x.domain(answers);
	  y.domain([0,maxval])

	  svg.append("g")
	      .attr("class", "x axis")
	      .attr("transform", "translate(0," + height + ")")
	      .call(xAxis)
	      .selectAll("text")  
		.data(ans) 
              	.style("text-anchor", "end")
            	.attr("x", -6)
            	.attr("dx", ".50em")
            	.attr("transform", function(d) {
                	return "rotate(-90)" 
                }).html(function(d){
			return d.answer.substring(0,3)
		})
		.on("mouseover", function(d) {      
			    div.transition()        
				.style("opacity", .99);      
			    div .html(d.answer)  
				.style("left", (d3.event.pageX) + "px")     
				.style("top", (d3.event.pageY - 28) + "px");    
			    })                  
		.on("mouseout", function(d) {       
			    div.transition()        
				.duration(500)      
				.style("opacity", 0);   
			});

	  svg.append("g")
	      .attr("class", "y axis")
	      .call(yAxis)
	    .append("text")
	      .attr("y", -20)
	      .attr("x",15)
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

