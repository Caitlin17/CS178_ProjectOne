# CS178_ProjectOne

## Summary
My project uses teh Movies database provided along with a non-relational database created using DynamoDB. I chose to focus my website around the genres of the movies inside the database. The options to "Add User," "Delete User," "Update User," and "Display User" all connect to the Dynamo database which records the user's name and favorite genre. The "Show Movies" option shows 10 movies from the Movies database. The "Recommend Movies" option pulls the favorite genre of a user from the Users Dynamo database and uses that to recommend movies in that genre in the Movies database. 

## Technologies Used
AI was used to help complete this project. I asked AI to help me create the html files to create the displays and options on the website. I also used AI to troubleshoot when I ran into problems getting my code to run. 

## Setup and Run Instructions 
I have the code set up to run from my EC2 instance. It can be accessed using the public IP address: http://54.226.48.7:8080/
When using the Delete User, Update User, and Recommend Movies link, the name input should be whatever was used to add the user. 
