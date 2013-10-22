function reload(){
	bluetooth.reload();
}

function visualization(content){
		document.getElementById('network').innerHTML = '';
		graph=createnodes(content);
		callnetwork(graph);
}

function callnetwork(graph) {
	$('#network').css('display', 'block');

	var 	width = 960,
		height = 400;
	 
	var 	color = d3.scale.category20();
	 
	var 	force = d3.layout.force()
		.charge(-220)
		.linkDistance(70)
		.size([width, height]);
	 
	var 	svg = d3.select("#network").append('svg')
		.attr("width", width)
		.attr("height", height);
	 
		force
			.nodes(graph.nodes)
			.links(graph.links)
			.start();
	 
		var link = svg.selectAll(".link")
			.data(graph.links)
			.enter().append("line")
			.attr("class", "link")
			.style("stroke-width", function(d) { return Math.sqrt(d.value); });
	 
		var node = svg.selectAll(".node")
			.data(graph.nodes)
		.enter().append("circle")
			.attr("class", "node")
			.attr("r", function(d) {return 2 + 2*Math.round(Math.log(d.size));})
			.style("fill", function(d) { return color(d.group); })
			.call(force.drag);
		 
		node.append("title")
			.text(function(d) { return d.name; });

	 
		force.on("tick", function() {
			link.attr("x1", function(d) { return d.source.x; })
				.attr("y1", function(d) { return d.source.y; })
				.attr("x2", function(d) { return d.target.x; })
				.attr("y2", function(d) { return d.target.y; });
		 
		node.attr("cx", function(d) { return d.x; })
			.attr("cy", function(d) { return d.y; });
		});
}



function createnodes(content){
	
	var nodes=[];
	var linkslist=[];
	var jsonnodes=[];
	var jsonlinks=[];
	var keyslists=[];
	var count=0;
	var count2=0;
	var graph=[]

	$('#totals').css('display','block');
	$('#totallinks').css('display','block');

	for(i=0;i<content.length;i++){
		devices=content[i].data.DEVICES.sort(function(a,b){
							if (a.android_bluetooth_device_extra_DEVICE.mAddress > b.android_bluetooth_device_extra_DEVICE.mAddress)
							      return 1;
							if (a.android_bluetooth_device_extra_DEVICE.mAddress < b.android_bluetooth_device_extra_DEVICE.mAddress)
							      return -1;
							    // a must be equal to b
							    return 0;
							});
		if (devices.length>1){
			for (j=0;j<devices.length;j++){
				name_source=devices[j].android_bluetooth_device_extra_DEVICE.mAddress
				
				for (m=j+1; m<devices.length;m++){
					name_target=devices[m].android_bluetooth_device_extra_DEVICE.mAddress;
					
					if (name_source!=name_target){
						if ([name_source,name_target] in linkslist) {
							linkslist[[name_source,name_target]]=linkslist[[name_source,name_target]]+1;
						}
						else {//new link
							linkslist[[name_source,name_target]]=1;
						}
					}
				}
			}
		}
		else{}
	}

	loslinks=linkslist;
	keyslist=Object.keys(loslinks); 
	valueslist=[]

	for (i=0;i<keyslist.length;i++){
		val=loslinks[keyslist[i]];
		valueslist.push(val)
	}

	valueslist=valueslist.sort(function (a, b) {
		    return b-a
		});

	
	percentage=Math.round(valueslist.length*0.1)
	
	for (z=0;z<keyslist.length;z++){
		if (loslinks[keyslist[z]]>valueslist[percentage]) {
			names=keyslist[z].split(',');
			if ((nodes.indexOf(names[0]))==-1){//newnode
				nodes.push(names[0]);
				jsonnodes.push({'name':names[0],'group':0, 'size':3}); 
			} else {
				jsonnodes[nodes.indexOf(names[0])].size+=1;	
			}
			if (nodes.indexOf(names[1])==-1){//newnode
				nodes.push(names[1]);
				jsonnodes.push({'name':names[1],'group':0, 'size':3}); 
			} else {
				jsonnodes[nodes.indexOf(names[1])].size+=1;	
			}

			jsonlinks.push({'source': nodes.indexOf(names[0]), 'target': nodes.indexOf(names[1]), 'value':loslinks[keyslist[z]]})
			
		}	
	}

	$("#active").text(jsonnodes.length);
	$("#total").text(valueslist.length);
	$("#links").text(jsonlinks.length);		

	graph['nodes']=jsonnodes
	graph['links']=jsonlinks

	return graph;
}
