AI Task Manager
AI Task Manager is a Flask-based task management application that allows users to create, manage, and schedule tasks efficiently. It integrates AI capabilities for task handling and Google Calendar for scheduling.

Features:

.Task creation, update, and deletion

.Task prioritization using High, Medium, and Low levels

.API for task management

.Google Calendar integration for scheduling tasks

.Interactive AI assistant for task-related queries

Installation

1. Set Up a Virtual Environment
```
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```
2. Install Dependencies
```
pip install -r requirements.txt
```
3. Set Up the Database
```
python
>>> from database import db
>>> from app import app
>>> with app.app_context():
...     db.create_all()
...
>>> exit()
```
4. Configure Google Calendar API

Go to Google Cloud Console

Create a new project and enable Google Calendar API

Generate OAuth 2.0 credentials and download credentials.json

Place credentials.json in the project root

Authenticate using:
```
python google_calendar.py
```
5. Running the Application
```
python app.py
```
The application will run on http://127.0.0.1:5001/

API Endpoints:

GET /tasks - Retrieve all tasks

POST /tasks - Add a new task

PUT /tasks/<task_id> - Update an existing task

DELETE /tasks/<task_id> - Delete a task

POST /ask-ai - Interact with the AI assistant

NOW FOR ADD TASK RUN IN THE TERMINAL:
```
python add_task.py
```
OR FROM BY USING THE POST FUNCTION THROUGH:
step .1
```
python app.py
```
step .2
Ex:Invoke-RestMethod -Uri "http://127.0.0.1:5001/tasks" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{
    "title": "Doctor Appointment",
    "description": "Visit the doctor for a check-up",
    "status": "pending",
    "priority": "high",
    "start_time": "2025-03-10T10:00:00Z",
    "end_time": "2025-03-10T11:00:00Z"
}'
                                                   
