function cancel(memberID){
    document.getElementById(`remove_${memberID}`).style.display = "block";
    document.getElementById(`edit_button_${memberID}`).style.display = "block";
    document.getElementById(`edit_username_${memberID}`).remove();
    document.getElementById(`edit_skills_${memberID}`).remove();
    document.getElementById(`edit_bio_${memberID}`).remove();
    document.getElementById(`edit_instagram_${memberID}`).remove();
    document.getElementById(`edit_itch_${memberID}`).remove();
    document.getElementById(`cancelButton_${memberID}`).remove();
    document.getElementById(`saveButton_${memberID}`).remove();
}


document.addEventListener("DOMContentLoaded", function(){

    const button = document.querySelectorAll("#edit_profile")
    button.forEach(function(button){
        button.onclick = function(){
            
            const memberID = button.dataset.id;
            const usernameID = button.dataset.username;
            const username = document.getElementById(`username_${memberID}`);
            const secusername = document.getElementById(`secusername_${memberID}`);
            const skills = document.getElementById(`skills_${memberID}`);
            const bio = document.getElementById(`bio_${memberID}`);

            var instagram = document.getElementById(`instagram_${memberID}`);
            var itch_profile = document.getElementById(`itch_${memberID}`);


            //Create textareas for editable fields
            let edit_username = document.createElement("textarea");
            edit_username.setAttribute("rows", "1");
            edit_username.innerHTML = username.innerHTML
            edit_username.id = `edit_username_${memberID}`;
            edit_username.className = `form-control username ${usernameID}`;

            let edit_skills = document.createElement("textarea");
            edit_skills.setAttribute("rows", "1");
            edit_skills.innerHTML = skills.innerHTML;
            edit_skills.id = `edit_skills_${memberID}`;
            edit_skills.className = "form-control skills";

            let edit_bio = document.createElement("textarea");
            edit_bio.setAttribute("rows", "5");
            edit_bio.innerHTML = bio.innerHTML;
            edit_bio.id = `edit_bio_${memberID}`;
            edit_bio.className = "form-control bio";
            edit_bio.style.borderRadius = "15px";

            let edit_instagram = document.createElement("textarea");
            edit_instagram.setAttribute("rows","1");
            edit_instagram.innerHTML = instagram;
            edit_instagram.id = `edit_instagram_${memberID}`;
            edit_instagram.className = "form-control social-media";

            let edit_itch = document.createElement("textarea");
            edit_itch.setAttribute("rows","1");
            edit_itch.innerHTML = itch_profile;
            edit_itch.id = `edit_itch_${memberID}`;
            edit_itch.className = "form-control social-media";
      
            //Create cancel button
            const cancelButton = document.createElement("button");
            cancelButton.innerHTML = "Cancel";
            cancelButton.id = `cancelButton_${memberID}`;
            cancelButton.className = "btn btn-danger col-3";
            cancelButton.style.margin = "10px";

            //Create save button
            const saveButton = document.createElement("button");
            saveButton.innerHTML = "Save";
            saveButton.id = `saveButton_${memberID}`;
            saveButton.className = "btn btn-success col-3";
            saveButton.style.margin = "10px";

            //Hide the edit button and current content
            document.getElementById(`edit_button_${memberID}`).style.display = "none";
            document.getElementById(`remove_${memberID}`).style.display = "none";
        
            //Add textarea fields to the div
            document.getElementById(`edit_${memberID}`).append(edit_username);
            document.getElementById(`edit_${memberID}`).append(edit_skills);
            document.getElementById(`edit_${memberID}`).append(edit_instagram);
            document.getElementById(`edit_${memberID}`).append(edit_itch);
            document.getElementById(`edit_${memberID}`).append(edit_bio);
            document.getElementById(`edit_${memberID}`).append(saveButton);
            document.getElementById(`edit_${memberID}`).append(cancelButton);

            //When the cancel button is clicked
            cancelButton.addEventListener("click",function(){
                cancel(memberID);
            })

            //When the save button is clicked
            saveButton.addEventListener("click", function(){
                edit_username = document.getElementById(`edit_username_${memberID}`);
                edit_skills = document.getElementById(`edit_skills_${memberID}`);
                edit_instagram = document.getElementById(`edit_instagram_${memberID}`);
                edit_itch = document.getElementById(`edit_itch_${memberID}`);
                edit_bio = document.getElementById(`edit_bio_${memberID}`);

                fetch(`/edit_profile/${memberID}`,{
                    method: "POST",
                    body: JSON.stringify({
                        username: edit_username.value,
                        skills: edit_skills.value,
                        instagram: edit_instagram.value,
                        itch_profile: edit_itch.value,
                        bio: edit_bio.value,
                    })
                   
                })
                .then(response => response.json())
                .then(result => {
                    console.log(result);
                    if(result[`error`]){
                    cancel(memberID)
                    } 
                    else {
                        username.innerHTML = result.username;
                        secusername.innerHTML = result.username;
                        skills.innerHTML = result.skills;
                        instagram.href = result.instagram;
                        itch_profile.href = result.itch_profile;
                        bio.innerHTML = result.bio;
                        console.log(instagram);
                        cancel(memberID) 
                        
                    }
                })
                .catch(error => {
                    console.error(error);
                }) 
            })
        }
    });
})

