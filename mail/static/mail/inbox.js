document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#display-email').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Send an Email
  document.querySelector("#compose-form").onsubmit = function(event){
    event.preventDefault();
    const recipients = document.querySelector("#compose-recipients").value;
    const subject = document.querySelector("#compose-subject").value;
    const body = document.querySelector("#compose-body").value;

    if(recipients.length === 0){
      alert(`At least one recipient is required`);
    }
    else{
      fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body,
          read: false
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        if(result[`error`]){
          alert(`User with email ${recipients} does not exist`)
        }
        else{
          load_mailbox("sent");
        }
    })
    return false;
    }
  }
}

function load_mailbox(mailbox) {

  const emails_view = document.querySelector("#emails-view")
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#display-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


  // GET the mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);

    // ... do something else with emails ...
    emails.forEach(email => {
      let div = document.createElement("div");
      div.className = "frame";

      if(email.read === true){
        div.style.backgroundColor = "#f1f1f1";
      }
      else{
        div.style.backgroundColor = "white";
      }

      if(mailbox === `sent`){
        const recipients = document.createElement("p");
        recipients.className = "bold";
        recipients.innerHTML = email.recipients;
        div.appendChild(recipients);
      }
      else{
        const sender = document.createElement("p");
        sender.className = "bold";
        sender.innerHTML = email.sender;
        div.appendChild(sender);
      }
      
      const subject = document.createElement("p");
      subject.className = "subject";
      const timestamp = document.createElement("p");
      timestamp.className = "time";

      
      subject.innerHTML = email.subject;
      timestamp.innerHTML = email.timestamp;

      
      emails_view.appendChild(div);
      div.appendChild(subject);
      div.appendChild(timestamp);
      
      // What to do when email is clicked
      div.addEventListener('click',() => display_email(email.id));
      
    });    
  });
}

function display_email(id){
  // Show display view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#display-email').style.display = 'block';

  document.querySelector("#display-email").innerHTML = "";

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
  
  // Get the email content
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    // Print email
    console.log(email);

    // ... do something else with email ...
    const display_email = document.querySelector("#display-email");

    const display_from = document.createElement("div");
    const display_to = document.createElement("div");
    const display_subject = document.createElement("div");
    const display_timestamp = document.createElement("div");
    const display_body = document.createElement("div");

    const reply = document.createElement("button");
    reply.innerHTML  = `Reply`;
    reply.className = "btn btn-sm btn-outline-primary";

    var arch_check = email.archived;
    const archive = document.createElement("button");
    archive.className = "btn btn-sm btn-outline-primary";
    archive.style.margin = "5px";
    if(arch_check){
      archive.innerHTML = "Unarchive";
    }
    else{
      archive.innerHTML = "Archive";
    }

    display_from.innerHTML = `<strong>From: </strong>${email.sender}`;
    display_to.innerHTML = `<strong>To: </strong>${email.recipients}`;
    display_subject.innerHTML = `<strong>Subject: </strong>${email.subject}`;
    display_timestamp.innerHTML = `<strong>Timestamp: </strong>${email.timestamp}`;
    display_body.innerHTML = `<hr> ${email.body}`;

    display_email.appendChild(display_from);
    display_email.appendChild(display_to);
    display_email.appendChild(display_subject);
    display_email.appendChild(display_timestamp);
    display_email.appendChild(reply);
    display_email.appendChild(archive);
    display_email.appendChild(display_body);

    // What to do when Archive/Unarchive is clicked
    archive.addEventListener('click',function(){
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: !arch_check
        })
      })
      .then(response => load_mailbox('inbox'))
    });

    // What to do when Reply button is clicked
    reply.addEventListener('click',() => {
      compose_email();
      document.querySelector('#compose-recipients').value = email.sender;
      subject = email.subject;
      if(!subject.includes("Re:")){
        subject = `Re: ${email.subject}`
      }
      else{
        subject = `${email.subject}`
      }
      document.querySelector('#compose-subject').value = subject;
      body = document.querySelector("#compose-body").value = `On ${email.timestamp} ${email.sender} wrote: 
      ${email.body}`;
    })

  });
}
