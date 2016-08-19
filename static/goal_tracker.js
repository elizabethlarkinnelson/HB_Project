function checkPass(){


    var pass1 = document.getElementById('pass1');
    var pass2= document.getElementById('pass2');

    var message = document.getElementById('confirmMessage');

    if (pass1.value == pass2.value){
        message.innerHTML = "Passwords Match!";
    } else{
        message.innerHTML = "Passwords Do Not Match!";
    }
}

