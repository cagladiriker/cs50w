function like_update(id, likes) {
  let count = document.getElementById(`idea_likecount_${id}`);
  count.innerHTML = likes;
}

function submit_new_idea(){
  document.querySelector("#new_idea").style.display = "none";
  document.querySelector("#new_idea_form").style.display = "block";
}

function cancel_idea(){
  document.querySelector("#new_idea").style.display = "block";
  document.querySelector("#new_idea_form").style.display = "none";
}

document.addEventListener('DOMContentLoaded', function () {

  document.addEventListener('click', event => {
    const element = event.target;

    //If submit new idea
    if (element.id.startsWith('new_idea')) {
      submit_new_idea();
    }

    //If form is cancelled
    if (element.id.startsWith('cancel')) {
      cancel_idea();
    }

    //If the close button is clicked
    if (element.id.startsWith('close_')) {
      let id = element.dataset.id;
      
      fetch(`/close/${id}`, {
          method: "POST"
      })
      .then(response => response.json())
      .then(function(data) {
          
          const status = data.status;
          if(status){
              element.textContent = "Closed";
              element.disabled = true;

              let row = element.closest('tr');
              let table = row.closest('tbody');
              table.appendChild(row);
          }
          
      });
    }

    //If the like button is clicked
    if (element.id.startsWith('like_')) {
      if (!element.disabled) {
        let id = element.dataset.id;
        
        fetch(`/like/${id}`, {
            method: "POST"
        })
        .then(response => response.json())
        .then(function(data) {
            
            const likes = data.likesCount;
            const likesIdea = data.likesIdea;

            // Like icon on page
            let heart = document.getElementById(`like_${id}`);
            like_update(id, likes)

            // Updates like icon correctly according to whether user likes post or not
            if (likesIdea) {
                heart.className = 'likeicon fa-heart fas';
            } else {
                heart.className = 'likeicon fa-heart far';
            }    
        });
      }
    }
  })

  const gameSlides = document.querySelectorAll('.game-slide');
  const eventSlides = document.querySelectorAll('.event-slide');
  const gameCircles = document.querySelectorAll('.game-circle');
  const eventCircles = document.querySelectorAll('.event-circle');
  const seeAllButton = document.getElementById('see_all');

  let currentGameIndex = 0;
  let currentEventIndex = 0;

  function showGameSlide() {
    gameSlides.forEach((slide, index) => {
      slide.style.display = index === currentGameIndex ? 'block' : 'none';
    });

    gameCircles.forEach((circle, index) => {
      circle.style.backgroundColor = index === currentGameIndex ? '#d95a28ff' : '#e6e2c2';
    });
  }

  function showEventSlide() {
    eventSlides.forEach((slide, index) => {
      slide.style.display = index === currentEventIndex ? 'block' : 'none';
    });

    eventCircles.forEach((circle, index) => {
      circle.style.backgroundColor = index === currentEventIndex ? '#d95a28ff' : '#e6e2c2';
    });
  }

  showGameSlide();
  showEventSlide();

  function changeGameSlide() {
    currentGameIndex = (currentGameIndex + 1) % gameSlides.length;
    showGameSlide();
  }

  function changeEventSlide() {
    currentEventIndex = (currentEventIndex + 1) % eventSlides.length;
    showEventSlide();
  }

  setInterval(changeGameSlide, 5000);
  setInterval(changeEventSlide, 5000);

  gameCircles.forEach((circle, index) => {
    circle.addEventListener('click', () => {
      currentGameIndex = index;
      showGameSlide();
    });
  });

  eventCircles.forEach((circle, index) => {
    circle.addEventListener('click', () => {
      currentEventIndex = index;
      showEventSlide();
    });
  });

  seeAllButton.addEventListener('click', () => {
    window.location.href = '/games';
  });
});
