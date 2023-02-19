# Quantified Self - All in one habit tracker!
Daily tracker for users to add customizable trackers and log values at any time of the day. All CRUD operations are possible on trackers and logs. It also enables users to export tracker details as and when needed. 

The app also sends daily reminders to users on the registered email to log for the trackers they haven’t 
updated in the day. 

Additionally, it also sends monthly reports to all users with the summary 
of their trackers.


## Project setup
To install all the required dependencies
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Flask
```
cd .\src\
python app.py
```

### Celery
```
cd .\src\
celery -A tasks.celery worker -P gevent -l INFO
```

### Celery Beat
```
cd .\src\
celery -A tasks.celery beat --max-interval 1 -l INFO
```

### Redis
```
redis-server
```

### MailHog
Open the application to recieve mails

## Features

- Multiple User Login
- Dashboard / Tracker-List
- Tracker Details Page/ Logs 
- Add New Tracker
- Add New Log
- Update Tracker and Log
- Email Updates for Daily Reminder
- Email Reports for Monthly Report
- Export as CSV

## Credits

This project was made for IITM BS Degree in Data Science and Programming for Modern Application Developement - 2 Course by Soumya Vaidya 
