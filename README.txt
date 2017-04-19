to test the application:

1. pip install any missing modules
	(you can determine these as you go if need be)

2. navigate in your command prompt to this directory

3. use commands:
	pip install --editable .
	set FLASK_APP=whiteboard
	flask initdb
	flask run

4. Open the web app on the indicated port
   i.e.:
	http://127/0/0/1:5000/