How to Run the Website


Open Windows Powershell or Windows Terminal
	
	Navigate to the project directory
	cd path\to\capapool-backend_views
	
	Example
	cd C:\Users\YourName\Desktop\CSIT314\Project\capapool-backend_views

--------------------------------------------------------------------------------------------
		
Activate the Virtual Environment

	.\.venv\Scripts\Activate
	
	If successful, the terminal prompt will display and begin with (.venv)

--------------------------------------------------------------------------------------------

Start the Django Development Server

	python manage.py runserver

--------------------------------------------------------------------------------------------

Open the Website

	Open a web browser and visit:
	
	http://127.0.0.1:8000/

--------------------------------------------------------------------------------------------

Stop the Server

	To end the run press:
	ctrl + c
	inside the terminal