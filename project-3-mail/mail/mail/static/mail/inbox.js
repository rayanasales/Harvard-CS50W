document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

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
        emailDiv.style.backgroundColor = email.read ? 'gray' : 'white';
        emailDiv.innerHTML = `
          <div style="display: flex;">
            <div style="font-weight: bold;">${email.sender}</div>
            <div style="margin-left: 15px; white-space: nowrap; max-width: 500px; overflow: hidden; text-overflow: ellipsis;">${email.subject}</div>
          </div>
          <div style="display: flex;">
            <div style="color: grey;">${email.timestamp}</div>
            <div class="archive-content" style="margin-left: 15px;">
              ${mailbox !== 'sent' ? `<button onclick="archive_email(event, ${email.id}, ${email.archived})">${email.archived ? 'Unarchive' : 'Archive'}</button>` : ''}
            </div>
          </div>
        `;
        emailDiv.addEventListener('click', () => display_email(email.id));
        document.querySelector('#emails-view').append(emailDiv);
      });
    } else {
      throw new Error('Failed to load emails');
    }
  } catch (error) {
    console.error('Error:', error);
    alert(`Failed to load ${mailbox}: ${error.message}`);
  }
}

async function display_email(email_id) {
  try {
    await mark_email_as_read(email_id);
    const response = await fetch(`/emails/${email_id}`);
    const email = await response.json();
    if (response.ok) {
      document.querySelector('#emails-view').innerHTML = `
        <div class="email-details">
          <b>From:</b> ${email.sender}<br>
          <b>To:</b> ${email.recipients.join(', ')}<br>
          <b>Subject:</b> ${email.subject}<br>
          <b>Timestamp:</b> ${email.timestamp}<br>
          <button onclick="mark_email_as_unread(${email_id})">Mark as Unread</button>
          <button onclick="reply_email(${email_id})">Reply</button>
          <hr>
          ${email.body}<br>
        </div>
      `;
    } else {
      throw new Error('Email not found');
    }
  } catch (error) {
    throw new Error(error); 
  }
}

async function mark_email_as_read(email_id) {
  try {
    const response = await fetch(`/emails/${email_id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        read: true
      })
    });
    if (!response.ok) {
      throw new Error(`Failed to mark email as read: Error status code: ${response.status}`);
    }
  } catch (error) {
    throw new Error(error);
  }
}

async function mark_email_as_unread(email_id) {
  try {
    const response = await fetch(`/emails/${email_id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        read: false
      })
    });
    if (!response.ok) throw new Error(`Failed to mark email as unread: Error status code: ${response.status}`);
    else load_mailbox('inbox');
  } catch (error) {
    throw new Error(error);
  }
}

async function send_email(event) {
  event.preventDefault();

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

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
    await response.json();
    if (response.ok) {
      load_mailbox('sent');
    }
  } catch (error) {
    alert("We got an error while sending the email.");
  }
}

function reply_email(email_id) {
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      document.querySelector('#compose-view').style.display = 'block';
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-recipients').value = email.sender;
      document.querySelector('#compose-subject').value = email.subject.startsWith('Re:') ? email.subject : `Re: ${email.subject}`;
      document.querySelector('#compose-body').value = `\n\nOn ${email.timestamp}, ${email.sender} wrote:\n>${email.body}`;
    })
    .catch(error => console.error('Reply Email Error:', error));
}

async function archive_email(event, email_id, archived) {
  event.stopPropagation();
  try {
    const response = await fetch(`/emails/${email_id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        archived: !archived
      })
    });

    if (response.ok) {
      load_mailbox('inbox');
    } else {
      alert(`Failed to update email status: Error status code: ${response.status}`);
    }
  } catch (error) {
    alert(`We encountered an error while updating the email status. Error: ${error.message}`);
  }
}