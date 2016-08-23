function updateCompletions(result){
    if (remove_button === True){
        $(#goal_id).remove();
        
    }

}




function updateGoals (evt){

    var formInput = {
        "goal_id": $(this).val()
    };

    $.post("/update_completions.json",
            formInput,
            updateCompletions);

}



$('.one_completion').click(updateGoals);