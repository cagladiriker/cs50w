# READ ME: Pat On The Back Studios Website

This project is dedicated to an indie game studio called Pat On The Back Studios (POTBS) and developed using Python's Django framework, JavaScript, HTML, and CSS. The aim of this website is to create a team space for the POTBS team that enables them to share who they are, what they do and to communicate with the world. It is a website that mostly focuses on administrative controls and flexibility instead of regular user actions. If a user is an administrator, they can add or edit databases from the website itself instead of visiting /admin. 

The website is comprised of 5 pages: Home, Games, Events, About Us and Contact Us.

Homepage serves as a summary page where the visitors can see all the games and events as a slideshow. This enables the POTBS team to showcase their published games and to promote their events. Another aim of this website is to engage with the users and meet their wishes. This engagement begins with the games table on the homepage that displays game assets that are uploaded by the POTBS team for their upcoming games. The team can submit new assets from the homepage itself if they have admin accounts. The users then can vote which idea(s) they like the best so that the POTBS team can decide which game they will work on based on the wishes of their community. Once the team decide which game to choose, they can close that game for voting but it stays visible to the users so that they can see the past data as well.

Games and Events pages have similar purposes and structures. They contain the published games and events of the POTBS team. Each game or event are displayed as a card that contains name, descrpition and other details such as a link to the game itself/event location, the publish date/the event date, etc. In these pages, the users can easily access all the games and events publisheed by the POTBS and explore them further. Whenever a new game is published or a new event is in the works, POTBS team is able to submit a new game/event from the related pages.

About Us page is an informative page about the POTBS team members cotaining their username, skills within the team, their short bio, and links to their social profiles. POTBS team can edit all fields within this page with their admin accounts.

Finally, the Contact Us page contains two interactive games that displays the contact information upon completion.

## Distinctiveness and Complexity

As mentioned in the introduction, this project focuses on the superuser access. There are many forms that superusers can submit to add an element to the database or edits they can make to alter the existing records. None of these changes require a new URL or page reload. The voting process and the process of closing the most voted games are also handled with JavaScript. This is a project that contains many combinations of server-side rendering with Django templates and client-side scripting with JavaScript that handles various fetch requests which alters different parts of the application. The most distinct feature of this project, the “Contact Us” page also uses JavaScript for its interactivity. The page contains two interactive games that are both played with different actions. 

## Files in the Project

- `models.py`: This Python file defines the Django models for the application. It includes the following models:
    - User: registered users of the website.
    - Member: the members of the Pat On The Back Studios team.
    - Game: published games by the Pat On The Back Studios
    - Event: planned events by the Pat On The Back Studios.
    - Idea: game ideas that the Pat On The Back Studios submits for voting by the website users.
- `views.py`: This Python file contains the Django views for the application. It includes views for different url paths as well as for handling edit and submit requests.
- `layout.html:` contains the default structure of the project, including the navbar and relations.
- `index.html`: The homepage that is divided into two parts. The first part includes two slide boards; the first board displays all game objects and the second board displays all event objects. The second part displays a table that is filled with the game ideas of the Pat On The Back Studios that haven’t been published yet but are open for voting. When the Pat On The Back Studios team decides that the idea has enough likes they can close it by clicking on the related buttons. They are also able to submit a form to publish a new idea. All of these actions are handled with JavaScript.
- `games.html`: Displays all published games and contains a new game form that is only visible to admins which uses JavaScript.
- `events.html`: Displays all planned events and contains a new event form that is only visible to admins which uses JavaScript.
- `about.html`:  Displays each team member's information and includes an edit button for admins. When the edit button is clikced, related textareas that are pre-filled with the existing data are created by using JavaScript.
- `contact.html`: Contains two interactive games that display the contact information upon completion - created using JavaScript.
- `index.js:` This JavaScript file is responsible for handling user interactions on the homepage, including button clicks, game and event slides, and updates on the page after the new idea form submission.
- `games.js`: Shows the new game form submission and handles the updates after the form is submitted.
- `events.js`: Shows the new event form submission and handles the updates after the form is submitted.
- `about.js`: This JavaScript file handles the editing of team member information. It sends the changes to the server and updates the page without a reload.
- `contact.js`: Used for creating the interactive games on the contact page.
- `styles.css:` Handles the page styles that are not handled with Bootstrap.

## How to Run the Application

1. Ensure you have Python 3.8 or later installed.
2. Clone the repository to your local machine.
3. Navigate to the repository folder using your terminal or command prompt.
4. Install the necessary dependencies with `pip install -r requirements.txt`
5. Make sure to apply the migrations with `python manage.py migrate` and then `python manage.py makemigrations`. 
6. Run the application with the command `python manage.py runserver`.
7. Open your web browser and navigate to `http://127.0.0.1:8000/`

## Additional Information

If the project is not working as expected, ensure that your Python version is up to date. If any issues persist, please contact the project maintainer.

## Python Packages

This application was built with Django and uses SQLite3 for storing data. Additional python package installation is not required but please check the requirements.txt file for further information.
