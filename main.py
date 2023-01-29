import os
import random
import json
import smtplib
from email.mime.text import MIMEText

def random_notes(directory, number_of_files, excluded_folders=None, include_hidden=False, excluded_files=None):
    md_files = []
    # Walk through all subdirectories
    for dirpath, dirnames, filenames in os.walk(directory):
        # Skip excluded folders
        if excluded_folders is not None:
            dirnames[:] = [d for d in dirnames if d not in excluded_folders]
        # Skip hidden folders if specified
        if not include_hidden:
            dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        # Append the path of all .md files to the list
        for f in filenames:
            if f.endswith('.md'):
                md_files.append(os.path.join(dirpath, f))
    # Exclude certain files
    if excluded_files is not None:
        md_files = [f for f in md_files if os.path.basename(f) not in excluded_files]

    if len(md_files) < number_of_files:
        return None
    else:
        # Select specified number of random files from the list
        random_files = random.sample(md_files, number_of_files)
        # Read the contents of the files
        notes = []
        for file in random_files:
            with open(file, 'r') as f:
                content = f.read()
                # remove lines with ".mp3"
                content = '\n'.join([line for line in content.split('\n') if ".mp3" not in line])
                notes.append((file, content))
        return notes


def send_email(smtp_server, smtp_port, sender_email, password, receiver_email,subject_email,content):
     # Create the email message
    message             = MIMEText(content)
    message["From"]     = sender_email
    message["To"]       = receiver_email
    message["Subject"]  = subject_email

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


def format_notes(notes):
    final_result = ""
    
    # Iterate through the list of notes and format the output
    for note in notes:
        filename = os.path.basename(note[0])
        final_result += f"{'='*len(filename)}\n"
        final_result += f"{filename}\n"
        final_result += f"{'='*len(filename)}\n"
        #final_result += f"Location: {note[0]}\n"
        final_result += f"Location: {os.path.basename(os.path.dirname(note[0]))}/\n"
        final_result += f"{note[1]}\n\n\n"
    return final_result


if __name__ == "__main__":
    # Script Parameters from json file
    with open("my_configuration.json", "r") as json_file:
        my_configuration = json.load(json_file)

    # Script parameters
    number_of_files     = my_configuration["number_of_files"]
    directory           = my_configuration["directory"]
    excluded_folders    = my_configuration["excluded_folders"]
    include_hidden      = my_configuration["include_hidden"]
    excluded_files      = my_configuration["excluded_files"]

    # Email credentials
    sender_email    = my_configuration["sender_email"]
    receiver_email  = my_configuration["receiver_email"]
    subject_email   = my_configuration["subject_email"]
    password        = my_configuration["email_password"]
    smtp_server     = my_configuration["smtp_server"]
    smtp_port       = my_configuration["smtp_port"]

    # Pick random notes
    notes = random_notes(directory, number_of_files, excluded_folders, include_hidden, excluded_files)

    if notes:
        # Format
        final_result = format_notes(notes)
        print(final_result)

        # Send email
        send_email(smtp_server, smtp_port, sender_email, password, receiver_email, subject_email, final_result) 

    else:
        print(f"Not enough files found.")
