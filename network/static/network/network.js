function reset(postId) {
  document.getElementById(`textarea_${postId}`).remove()
  document.getElementById(`save_${postId}`).remove()
  document.getElementById(`cancel_${postId}`).remove()

  document.getElementById(`content_${postId}`).style.display = 'block';
  document.getElementById(`edit_${postId}`).style.display = 'inline-block';
}

function like_update(id, likes) {
    let count = document.getElementById(`post_likecount_${id}`);
    count.innerHTML = likes;

}


document.addEventListener('DOMContentLoaded', function() {

  document.addEventListener('click', event => {
      
      const element = event.target;

      //If the edit button is clicked
      if (element.id.startsWith('edit_')) {
          
          const editButton = element;
          const postId = editButton.dataset.id;
          const content = document.getElementById(`content_${postId}`);

          let textArea = document.createElement('textarea');
          textArea.innerHTML = content.innerHTML;
          textArea.id = `textarea_${postId}`;
          textArea.className = 'form-control';

          const saveButton = document.createElement('button');
          saveButton.innerHTML = 'Save';
          saveButton.className = 'badge badge-pill badge-success';
          saveButton.id = `save_${postId}`

          const cancelButton = document.createElement('button');
          cancelButton.innerHTML = 'Cancel';
          cancelButton.id = `cancel_${postId}`
          cancelButton.className = 'badge badge-pill badge-danger ml-1';

          document.getElementById(`edit_form_${postId}`).append(textArea);
          document.getElementById(`edit_form_${postId}`).append(saveButton);
          document.getElementById(`edit_form_${postId}`).append(cancelButton);
      

          content.style.display = 'none';
          editButton.style.display = 'none';

          //If the cancel button is clicked
          cancelButton.addEventListener('click', function() {
              reset(postId)
          })

          //If the save button is clicked
          saveButton.addEventListener('click', function() {
              
              textArea = document.getElementById(`textarea_${postId}`);
              fetch(`/edit/${postId}`, {
                  method: 'POST',
                  body: JSON.stringify({
                      content: textArea.value,
                  })
              })
              .then(response => response.json())
              .then(result => {
                console.log(result);
                if(result[`error`]){
                  reset(postId)
                  editButton.style.display = 'none';
                } 
                else {
                    content.innerHTML = result.content;
                    reset(postId)   
                }
              })
              .catch(error => {
                  console.error(error);
              })
          })
      }
      //If the like button is clicked
      if (element.id.startsWith('like_')) {
        let id = element.dataset.id;
        
        fetch(`/like/${id}`, {
            method: "POST"
        })
        .then(response => response.json())
        .then(function(data) {
            
            const likes = data.likesCount;
            const likesPost = data.likesPost;

            // Like icon on page
            let heart = document.getElementById(`like_${id}`);
            like_update(id, likes)

            // Updates like icon correctly according to whether user likes post or not
            if (likesPost) {
                heart.className = 'likeicon fa-heart fas';
                heart.style = "color:red";
            } else {
                heart.className = 'likeicon fa-heart far';
                heart.style = "color:red";
            }
            
        });
    }
  })
})