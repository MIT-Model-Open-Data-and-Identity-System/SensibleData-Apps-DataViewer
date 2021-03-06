function createQualityChartFromJSON(data, chartId, rawUrl) {
    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = 900 - margin.left - margin.right,
        height = 380 - margin.top - margin.bottom;

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
        ;

    var svg = d3.select(".chart-".concat(chartId))
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    x.domain(data.map(function (d) {
        return d['month'];
    }));
    y.domain([0, d3.max(data, function (d) {
        return d['quality'];
    })]);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Quality");

    svg.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function (d) {
            return x(d['month']);
        })
        .attr("width", x.rangeBand())
        .attr("y", function (d) {
            return y(d['quality']);
        })
        .attr("height", function (d) {
            return height - y(d['quality']);
        }).on("click", click);

    svg.selectAll(".bar text")
        .data(data).enter()
        .append("text")
        .attr("class", "bar_text")
        .attr("x", function (d) {
            return x(d['month']) + x.rangeBand()/2 - 10;
        })
        .attr("y", function (d) {
            return y(d['quality']) + 15;
        })

        .text(function (d) {
            return d['quality'];
        });

    function click(d)
    {
        params = "?users_to_return=" + d['good_users'].join() + "&start_date=" + d["month_start"] + "&end_date=" + d["month_end"];
        window.location.replace(rawUrl + params)
    }

}
