document.addEventListener("DOMContentLoaded", function(){

    const startButton = document.getElementById("start-button");
    const stickman = document.getElementById("stickman");
    const phoneBooth = document.getElementById("phone-booth");
    const phoneNumber = document.getElementById("phone-number");
    const wasd = document.getElementById("wasd");
    const gameBox = document.getElementById("game-box");
    const gameOne = document.getElementById("game1");


    startButton.addEventListener("click", function() {
        startButton.style.display = "none";
        stickman.style.display = "block";
        stickman.style.opacity = "1";
        wasd.style.display = "block";

    });

    document.addEventListener("keydown", function(event) {
    if (stickman.style.opacity === "1") {
        if (event.key === "w") {
            if(stickman.offsetTop > stickman.offsetHeight % gameBox.offsetTop){
                stickman.style.top = stickman.offsetTop - 12 + "px";
            }
        }

        if (event.key === "a") {
            if (stickman.offsetLeft > phoneBooth.offsetLeft + phoneBooth.offsetWidth) {
                stickman.style.left = stickman.offsetLeft - 12 + "px";
            }
        }

        if (event.key === "s") {
            if (stickman.offsetTop + stickman.offsetHeight < phoneBooth.offsetTop + phoneBooth.offsetHeight) {
                stickman.style.top = stickman.offsetTop + 12 + "px";
            }
        }

        if (event.key === "d") {
            if (stickman.offsetLeft + stickman.offsetWidth < gameBox.offsetWidth) {
                stickman.style.left = stickman.offsetLeft + 12 + "px";
            }
        }

        if (
            stickman.offsetLeft <= phoneBooth.offsetLeft + phoneBooth.offsetWidth &&
            stickman.offsetTop + stickman.offsetHeight == phoneBooth.offsetTop + phoneBooth.offsetHeight){
            stickman.style.opacity = "0.3";
            phoneBooth.style.opacity = "0.3";
            wasd.style.opacity = "0.3";
            gameOne.style.opacity = "0.3";
            phoneNumber.style.display = "block";
            }
    }
    });

    const startButton2 = document.getElementById("start-button2");
    const emailIcon = document.getElementById("email-icon");
    const computer = document.getElementById("computer");
    const emailAddress = document.getElementById("email-address");
    const arrowButtons = document.getElementById("arrow-buttons");
    const leftArrow = document.getElementById("left-arrow");
    const rightArrow = document.getElementById("right-arrow");
    const upArrow = document.getElementById("up-arrow");
    const downArrow = document.getElementById("down-arrow");
    const spikyWalls = document.getElementsByClassName("spiky-wall");
    const gameBox2 = document.getElementById("game-box2");

    let moveDirection = "up";

    function moveSpikyWall() {
        const gameBox2Height = gameBox2.offsetHeight;
        const spikyWall = document.getElementById("spiky-wall-3");
        const spikyWallHeight = spikyWall.offsetHeight;
        const maxY = gameBox2Height - spikyWallHeight;
      
        //Get the current y position
        let currentY = parseInt(spikyWall.style.top, 10) || 0;
      
        let newY;
      
        if (moveDirection === "up") {
            newY = currentY - 3;
            if (newY <= 0) {
                moveDirection = "down";
            }
        } else {
            newY = currentY + 3;
            if (newY >= maxY) {
                moveDirection = "up";
            }
        }
      
        //Set the new y position
        spikyWall.style.top = newY + "px";
    }
    
    function animateSpikyWall() {
        moveSpikyWall();
        requestAnimationFrame(animateSpikyWall);
    }
    
    startButton2.addEventListener("click", function() {
        startButton2.style.display = "none";
        emailIcon.style.display = "block";
        emailIcon.style.opacity = "1";
        arrowButtons.style.display = "block";

        //Start moving spikey wall like an elevator
        requestAnimationFrame(animateSpikyWall);
    });

    function resetEmailIconPosition() {
        emailIcon.style.left = "10px";
        emailIcon.style.top = "50%";
    }

    function checkCollision() {
        for (const spikyWall of spikyWalls) {
            const wallRect = spikyWall.getBoundingClientRect();
            const emailIconRect = emailIcon.getBoundingClientRect();

            if (wallRect.left < emailIconRect.right &&
                wallRect.right > emailIconRect.left &&
                wallRect.top < emailIconRect.bottom &&
                wallRect.bottom > emailIconRect.top) {
                resetEmailIconPosition();
                break;
            }
        }
    }

    function moveEmailIcon(dx, dy) {
        const newLeft = emailIcon.offsetLeft + dx;
        const newTop = emailIcon.offsetTop + dy;
        const gameBox2Rect = gameBox2.getBoundingClientRect();

        if (newLeft >= 0 && newLeft + emailIcon.offsetWidth <= gameBox2Rect.width) {
            emailIcon.style.left = newLeft + "px";
        }

        if (newTop >= 0 && newTop + emailIcon.offsetHeight <= gameBox2Rect.height) {
            emailIcon.style.top = newTop + "px";
        }

        checkCollision();
    }
    
    let moveEmailInterval;

    function startMoveEmailIcon(dx, dy) {
    clearInterval(moveEmailInterval);
    moveEmailInterval = setInterval(() => {
        moveEmailIcon(dx, dy);
    }, 10);
    }

    function stopMoveEmailIcon() {
        clearInterval(moveEmailInterval);
    }

    leftArrow.addEventListener("mousedown", () => startMoveEmailIcon(-2, 0));
    leftArrow.addEventListener("mouseup", stopMoveEmailIcon);
    leftArrow.addEventListener("mouseout", stopMoveEmailIcon);

    rightArrow.addEventListener("mousedown", () => startMoveEmailIcon(2, 0));
    rightArrow.addEventListener("mouseup", stopMoveEmailIcon);
    rightArrow.addEventListener("mouseout", stopMoveEmailIcon);

    upArrow.addEventListener("mousedown", () => startMoveEmailIcon(0, -2));
    upArrow.addEventListener("mouseup", stopMoveEmailIcon);
    upArrow.addEventListener("mouseout", stopMoveEmailIcon);

    downArrow.addEventListener("mousedown", () => startMoveEmailIcon(0, 2));
    downArrow.addEventListener("mouseup", stopMoveEmailIcon);
    downArrow.addEventListener("mouseout", stopMoveEmailIcon);


    function endGame() {
        emailIcon.style.opacity = "0.3";
        computer.style.opacity = "0.3";
        arrowButtons.style.opacity = "0.3";
        emailAddress.style.display = "block";

        leftArrow.disabled = true;
        rightArrow.disabled = true;
        upArrow.disabled = true;
        downArrow.disabled = true;

        for (const spikyWall of spikyWalls) {
            spikyWall.style.opacity = "0.3";
        }
        // Stop the elevator animation
        cancelAnimationFrame(animationFrameId);
    }

    function checkEmailIconReachedComputer() {
        const computerRect = computer.getBoundingClientRect();
        const emailIconRect = emailIcon.getBoundingClientRect();

        if (computerRect.left < emailIconRect.right &&
            computerRect.right > emailIconRect.left &&
            computerRect.top < emailIconRect.bottom &&
            computerRect.bottom > emailIconRect.top) {
            endGame();
        }
    }

    let animationFrameId;

    function animateSpikyWall() {
        moveSpikyWall();
        animationFrameId = requestAnimationFrame(animateSpikyWall);
    }

    document.addEventListener("mouseup", function() {
        checkEmailIconReachedComputer();
    });
})