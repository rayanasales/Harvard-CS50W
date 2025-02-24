document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Send email: event listener for form submission
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  load_mailbox('inbox');
});

function compose_email() {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

async function load_mailbox(mailbox) {
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  try {
      const response = await fetch(`/emails/${mailbox}`);
      const emails = await response.json();
      if (response.ok) {
          emails.forEach(email => {
              const emailDiv = document.createElement('div');
              emailDiv.className = 'email-summary';
              emailDiv.style.cursor = 'pointer';
              emailDiv.style.border = '1px solid grey';
              emailDiv.style.padding = '10px';
              emailDiv.style.margin = '5px 0';
              emailDiv.style.display = 'flex';
              emailDiv.style.justifyContent = 'space-between';
              emailDiv.innerHTML = `
                  <div style="display: flex;">
                      <div style="font-weight: bold;">${email.sender}</div>
                      <div style="margin-left: 15px; white-space: nowrap; max-width: 500px; overflow: hidden; text-overflow: ellipsis;">${email.subject}</div>
                  </div>
                  <div style="color: grey;">${email.timestamp}</div>
              `;
              emailDiv.addEventListener('click', () => display_email(email.id));
              document.querySelector('#emails-view').append(emailDiv);
          });
      } else {
          throw new Error('Failed to load emails');
      }
  } catch (error) {
      console.error('Error:', error);
  }
}

async function display_email(email_id) {
  try {
      const response = await fetch(`/emails/${email_id}`);
      const email = await response.json();
      if (response.ok) {
          document.querySelector('#emails-view').innerHTML = `
              <div class="email-details">
                  <b>From:</b> ${email.sender}<br>
                  <b>To:</b> ${email.recipients.join(', ')}<br>
                  <b>Subject:</b> ${email.subject}<br>
                  <b>Timestamp:</b> ${email.timestamp}<br>
                  <button onclick="archive_email(${email.id}, ${email.archived})">${email.archived ? 'Unarchive' : 'Archive'}</button>
                  <button onclick="mark_read(${email.id}, ${email.read})">${email.read ? 'Mark as Unread' : 'Mark as Read'}</button>
                  <hr>
                  ${email.body}<br>

              </div>
          `;
      } else {
          throw new Error('Email not found');
      }
  } catch (error) {
      console.error('Error:', error);
  }
}

async function send_email(event) {
  event.preventDefault();

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  console.log("Sending email...");
  console.log({recipients, subject, body});

  try {
      const response = await fetch('/emails', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              recipients: recipients,
              subject: subject,
              body: body
          })
      });

      const result = await response.json();

      if (response.ok) {
          console.log({result});
          alert("Email sent successfully.");
          // Load the sent mailbox
          load_mailbox('sent');
      } else {
          console.log({result});
          alert("Error: " + result.error);
      }
  } catch (error) {
      console.error('Error:', error);
      alert("We got an error while sending the email.");
  }
}

function archive_email(email_id, archived) {
  // Code to archive or unarchive an email
}

function mark_read(email_id, read) {
  // Code to mark an email as read or unread
}
