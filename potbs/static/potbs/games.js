function submit_new_game(){
    document.querySelector("#content").style.display = "none";
    document.querySelector("#new_game_form").style.display = "block";
}

function cancel_game(){
    document.querySelector("#content").style.display = "block";
    document.querySelector("#new_game_form").style.display = "none";
}

document.addEventListener("DOMContentLoaded", function(){

    document.addEventListener('click', event => {
        const element = event.target;

        if (element.id.startsWith('new_game')) {
            submit_new_game();
        }
        
        //If form is cancelled
        if (element.id.startsWith('cancel')) {
            cancel_game();
        }
    });
})