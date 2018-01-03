# Chatty Kathy By Alex Blackson

Name: Alex Blackson

## Installation 

1. Open Command Prompt in Administrator mode and create a virtual environment for Python

2. Install Flask, Flask-SQLAlchemy, and Flask-Restful to your environment with the following commands:

  [1] pip install Flask
  
  [2] pip install Flask-SQLAlchemy
  
  [3] pip install flask-restful

3. Add the "FLASK_APP" variable to your path using the command:

	set FLASK_APP=chat.py

4. Initialize database with the command:
	
	flask initdb

## Running

1. Simply execute "flask run" from the command line 

2. Navigate to http://127.0.0.1:5000/ and explore!

## Notes

Note that pressing "Enter" on the keyboard does not work to send message. Instead, you must click 
the actual "Send" button. Pressing "Enter" will only refresh the page. 