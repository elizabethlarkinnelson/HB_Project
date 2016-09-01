
$(document).ready(function(){


    function updateCompletions(result){
        if (result.remove_button === true){
            $('#'+result.goal_id).html('<div id="complete_message">' + result.message + '</div>');

        } else {
            // $('#'+result.goal_id).html('<input type="radio" name="one_completion" value='+result.goal_id+'>I did it!<br>');
            $('#complete_message').remove();
            $('input[name="one_completion"]').prop('checked', false);
            $('#'+result.goal_id).append('<div id="complete_message">' + result.message + '</div>');

        }


    }

    function reminderUpdated(result){
        $("input[name*='"+result.goal_id+"'][value='"+result.week_day+"']").remove();
        $("#"+result.goal_id+"."+result.week_day).remove();
    }




    function updateGoals (evt){

        var formInput = {
            "goal_id": $(this).val()
        };

        $.post("/update_completions.json",
                formInput,
                updateCompletions);

    }


    function updateReminders(evt){
        evt.stopImmediatePropagation();

        var formInput = {
            "goal_id": $(this).attr("name"),
            "week_day": $(this).val(),
        };

        $.post("/update_reminders.json",
                formInput,
                reminderUpdated);

    }



    $('input:radio').on('change', updateGoals);
    $('input:checkbox').on('change', updateReminders);


});