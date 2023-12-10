function submit_new_event(){
    document.querySelector("#content").style.display = "none";
    document.querySelector("#new_event_form").style.display = "block";
}
function cancel_event(){
    document.querySelector("#content").style.display = "block";
    document.querySelector("#new_event_form").style.display = "none";
}

document.addEventListener("DOMContentLoaded", function(){

    document.addEventListener('click', event => {
        const element = event.target;

        if (element.id.startsWith('new_event')) {
            submit_new_event();
        }

        //If form is cancelled
        if (element.id.startsWith('cancel')) {
            cancel_event();
        }
    });
  
})



