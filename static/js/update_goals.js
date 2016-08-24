
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




    function updateGoals (evt){

        var formInput = {
            "goal_id": $(this).val()
        };

        $.post("/update_completions.json",
                formInput,
                updateCompletions);

    }



    $('input:radio').on('change', updateGoals);


});