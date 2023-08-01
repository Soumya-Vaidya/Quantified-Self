
# Quantified Self - All-In-One habit tracker!
Quantified Self is a web-based habit tracker that allows users to track their daily habits and monitor their progress. The app provides users with the flexibility to add customizable trackers and log values at any time of the day. It also enables users to export tracker details as and when needed.

The app sends daily reminders to users on the registered email to log for the trackers they haven’t updated in the day. Additionally, it also sends monthly reports to all users with the summary of their trackers.

## Getting Started

To run the project on your local machine, please follow these steps:

1. Clone this repository on your machine.
2. Open a terminal and navigate to the root directory of the project.
3. Run the following command to install all the required dependencies:


```
npm install
```

4. Run the following command to compile and hot-reload for development:

```
npm run serve
```
5. Open another terminal and navigate to the src directory.
6. Run the following command to start the Flask server:

```
python app.py
```

7. Open another terminal and navigate to the src directory.
8. Run the following command to start the Celery worker:

```
celery -A tasks.celery worker -P gevent -l INFO
```
9. Open another terminal and navigate to the src directory.
10. Run the following command to start the Celery beat:
css

```
celery -A tasks.celery beat --max-interval 1 -l INFO
```

11. Make sure you have Redis installed and running. If not, run the following command:

```
redis-server
```

12. Make sure you have MailHog installed and running. If not, open the MailHog application to receive emails.

13. Visit http://localhost:8080/ in your browser to access the app.

## Features
Quantified Self has the following features:

- Multiple User Login: Users can create an account and login to the app.
- Dashboard / Tracker-List: Users can view all their trackers on the dashboard.
- Tracker Details Page/ Logs: Users can view the details of each tracker and the logs associated with it.
- Add New Tracker: Users can create a new tracker and customize it as per their requirements.
- Add New Log: Users can add a new log to their tracker.
- Update Tracker and Log: Users can update their tracker and log details.
- RESTful API to perform CRUD operations
- Email Updates for Daily Reminder: The app sends daily reminders to users on their registered email to log for the trackers they haven't updated in the day.
- Email Reports for Monthly Report: The app sends monthly reports to all users with the summary of their trackers.
- Export as CSV: Users can export their tracker details as a CSV file.


## Technology Stack
Quantified Self is built using the following technologies:

- Front-end: HTML, CSS, JavaScript, Vue.js
- Back-end: Python Flask
- Task Queue: Celery
- Message Broker: Redis
- Email Server: MailHog

Libraries used:
- Bootstrap
- ChartJS
- JWT-Extended 
- BCrypt
- SMTPlib

## Credits

This project was made for IITM BS Degree in Data Science and Programming for Modern Application Developement - 2 Course by Soumya Vaidya 
