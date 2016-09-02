
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
    

    // $.ajax({
    //       type: "POST",
    //       username: "AC6dd1ef6816c2db5b40f3067d623d6818",
    //       password: "f38c20243b571437e85bc7f2fbc42ed8",
    //       url: "https://api.twilio.com/2010-04-01/Accounts/AC6dd1ef6816c2db5b40f3067d623d6818/Messages",
    //       // xhrFields: {
    //       //   withCredentials: true
    //       // },
    //       data: {
    //         "To" : "+19493156013",
    //         "From" : "+19495417040",
    //         "Body" : "Work"
    //       },
    //       success: function(data) {
    //         console.log(data);
    //       },
    //       error: function(data) {
    //         console.log(data);
    //       }
    // });


});