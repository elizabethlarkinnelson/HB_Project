$(document).ready(function(){


    var goalInfo = null;

// AJAX code to grab user's goal data

    // FIXME
    function setUserInfo(result){
        percentComplete = result.percentage_complete;
        initialize(percentComplete);
    }

    function retrieveGoalCompletionInfo(){
        $.get("/goal_completion_data.json", setUserInfo);
    }

    retrieveGoalCompletionInfo();

    // FIX ME!!!! Need to add goals through jason that have no completions!


});


function initialize(percentComplete){

    div1 = d3.select("#div1");
    
    viz1 = vizuly.component.radial_progress(document.getElementById("div1"));

    theme1 = theme1 = vizuly.theme.radial_progress(viz1).skin(vizuly.skin.RADIAL_PROGRESS_FIRE);

    viz1.data(percentComplete)
            .height(600)
            .min(0)
            .max(100)
            .capRadius(1)
            .startAngle(180)
            .endAngle(180)
            .arcThickness(0.04)
            .label(function(d,i) { return d3.format(".0f")(d) + "%";});

    viz1.update();
}
