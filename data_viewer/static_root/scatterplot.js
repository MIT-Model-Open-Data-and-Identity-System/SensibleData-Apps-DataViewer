function reload(){
	scatterplot.reload();
}


function plot(results,questions){
	document.getElementById('scatterplot').innerHTML = '';
	document.getElementById('histogram').innerHTML = '';
	users=[]
	question0=[]
	question1=[]
	answers0=new Array()
	answers1=new Array()
	
	if (results.length>0){
		for (i=0;i<results.length;i++){
			if (!(results[i].user in users)){
				users[results[i].user]=1;				
			}
			if(results[i].variable_name==questions[0]){
					question0[results[i].user]=results[i].human_readable_response.replace(",",".");
					if (!(results[i].human_readable_response.replace(",",".") in answers0)){
						answers0[results[i].human_readable_response.replace(",",".")]=1
					}
				}
			else if(results[i].variable_name==questions[1]){
					question1[results[i].user]=results[i].human_readable_response.replace(",",".");
					if (!(results[i].human_readable_response.replace(",",".") in answers1)){
						answers1[results[i].human_readable_response.replace(",",".")]=1
					}
			}
		}
	}
	
	newlist=users
	keysusers=Object.keys(newlist);
	pairs=[]
	final=[]
	for (i=0;i<keysusers.length;i++){
		if((!(question0[keysusers[i]]==null))&&(!(question1[keysusers[i]]==null))){
			if ([question0[keysusers[i]],question1[keysusers[i]]] in pairs){
				pairs[[question0[keysusers[i]],question1[keysusers[i]]]]=pairs[[question0[keysusers[i]],question1[keysusers[i]]]]+1;
			}
			else{
				pairs[[question0[keysusers[i]],question1[keysusers[i]]]]=1
			}
		}
	}

	newpairs=pairs
	keyspairs=Object.keys(newpairs);
	names=[]
	for (m=0;m<keyspairs.length;m++){
		names=keyspairs[m].split(',');
		final.push({'question0':names[0], 'question1':names[1], 'value':pairs[[names[0],names[1]]]})
	}

	percent=0;
	if (results.length<=10){percent=100}
	else if(results.length>10 && results.length<=100){percent=10}
	else if(results.length>100 && results.length<=1000){percent=1}

	BuildDataPlot(final,questions,answers0,answers1,percent)
}

function BuildDataPlot(data,ques,answers0,answers1,percent){

	$('#scatterplot').css('display', 'block');

	ans0=[];
	ans1=[];
	keys0=Object.keys(answers0)
	keys1=Object.keys(answers1)
	for (i=0;i<keys0.length;i++){
		ans0.push({'answer':keys0[i]})
	}	
	for (j=0;j<keys1.length;j++){
		ans1.push({'answer':keys1[j]})
	}

	var margin = {top: 20, right: 40, bottom:40, left:40},
	    width = 75*keys0.length- margin.right-margin.left,
	    height = 75*keys1.length - margin.top-margin.bottom;

	var x = d3.scale.ordinal()
	    .rangePoints([0, width], .2);

	var y = d3.scale.ordinal()
	    .rangePoints([height,0], .2);

	var color = d3.scale.category10();

	var xAxis = d3.svg.axis()
	    .scale(x)
	    .orient("bottom");

	var yAxis = d3.svg.axis()
	    .scale(y)
	    .orient("left");

	var svg = d3.select("#scatterplot").append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	  x.domain(Object.keys(answers0));
	  y.domain(Object.keys(answers1));

	var div = d3.select("#scatterplot").append("div")   
	    .attr("class", "tooltip")               
	    .style("opacity", 0);

	svg.selectAll("circle")
	      .data(data)
	    .enter().append("circle")
	      .attr("class", "dot")
	      .attr("r", function(d) { return Math.sqrt(d.value*percent)})
	      .attr("cx", function(d) { return x(d.question0); })
	      .attr("cy", function(d) { return y(d.question1); });

	svg.selectAll("text")
		.data(data)
		.enter().append("text")
	     		.text(function(d) {
        			return d.value;
   			})
			.attr("x", function(d) {
				return x(d.question0)+10; 
			})
			.attr("y", function(d) {
				return y(d.question1); 
			})
			.attr("font-family", "sans-serif")
			.attr("font-size", "15px")
			.attr("fill", "red");
	 
	 svg.append("g")
	      .attr("class", "x axis")
	      .attr("transform", "translate(0," + height + ")")
	      .call(xAxis)
	     .selectAll("text")  
		.data(ans0) 
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
			})
	      .append("text")
		      .attr("class", "label")
		      .attr("x", width + 68)
		      .attr("y", -6)
		      .style("text-anchor", "end")
		      .text(ques[0]);
	   

	  svg.append("g")
	      .attr("class", "y axis")
	      .call(yAxis)
	      .selectAll("text")  
			.data(ans1) 
			.html(function(d){
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

		
}

