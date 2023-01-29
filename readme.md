# Random MD File Selector
Imagine that you have taken a lot of notes in a folder, typically md files here, but you never have time to review them. This script allows you to randomly select a certain number of notes and send their content to you directly in daily emails. This idea was inspired by a paid feature of the Readwise app.

This script allows you to select a specified number of random .md files from a given directory and its subdirectories, and format the results into a string then send it by email to some inbox.


# How to use
1. Clone the repository to your local machine
2. Install the necessary dependencies
3. Update the json file with your credentials, files path and other parameters you want such as the number of files to select, excluded subfolders...
4. Run the script
6. You can deployed this project on a local machine such as a Raspberri Pi or a remote server such as AWS Lambda or Google Cloud Functions in order to be run automatically and periodically using a cron.


# Note
The script uses python smtplib to send email so make sure your system is configured to use smtp.


Please feel free to submit any issues or pull requests if you encounter any problems or have suggestions for improvements.