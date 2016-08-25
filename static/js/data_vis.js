$(document).ready(function(){

//variables for user's data accessible to D3 JS, set by
// document.ready function below.

    var goal_info = {};
    var completion_info = {};


// AJAX code to grab user's goal data

    function setUserInfo(result){
        console.log(result.hi);
    }

    function retrieveGoalCompletionInfo(){
        $.get("/goal_completion_data.json", setUserInfo);
    }

    retrieveGoalCompletionInfo();

    // });



// D3 goal visualization code  

    var data = [6, 22, 15, 16, 23, 42];

    var width = 420,
        barHeight = 20;

    var x = d3.scale.linear()
        .domain([0, d3.max(data)])
        .range([0, width]);

    var chart = d3.select(".chart")
        .attr("width", width)
        .attr("height", barHeight * data.length);

    var bar = chart.selectAll("g")
        .data(data)
      .enter().append("g")
        .attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; });

    bar.append("rect")
        .attr("width", x)
        .attr("height", barHeight - 1);

    bar.append("text")
        .attr("x", function(d) { return x(d) - 3; })
        .attr("y", barHeight / 2)
        .attr("dy", ".35em")
        .text(function(d) { return d; });

});