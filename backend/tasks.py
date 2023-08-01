from celery import Celery
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Template
from celery.schedules import crontab

import sqlalchemy
import pandas as pd

import requests


# Celery Config

celery = Celery(broker="redis://localhost:6379")
celery.conf.update(timezone="Asia/Kolkata")


# SMTP Server details
SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "email@soumya.com"
SENDER_PASSWORD = ""


# Gets the email list from the endpoint
email_list = requests.request("GET", "http://127.0.0.1:8000/mail")
emails = list(eval(email_list.text))


# Mail Sending
def send_email(to_address, subject, message, content="text"):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    if content == "html":
        msg.attach(MIMEText(message, "html"))
    else:
        msg.attach(MIMEText(message, "plain"))
    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True


def format_message(template_file, data={}, trackers={}):
    with open(template_file) as file_:
        template = Template(file_.read())
        return template.render(data=data, trackers=trackers)


def send_welcome_message(data, trackers):
    message = format_message("monthly_email.html", data=data, trackers=trackers)

    send_email(
        to_address=data["email"],
        subject="QuantifiedSelf: Monthly Report",
        message=message,
        content="html",
    )


def send_daily_reminder(data, trackers):
    message = format_message("reminder_email.html", data=data, trackers=trackers)

    send_email(
        to_address=data["email"],
        subject="QuantifiedSelf: Daily Reminder",
        message=message,
        content="html",
    )


# Celery Tasks Start Here


@celery.task(name="tasks.send")
def send(emails):
    print("Inside monthly emails")

    for email in emails:
        url = "http://127.0.0.1:8000/tracker_report/{}".format(email["user_id"])
        tracker_response = requests.request("GET", url)
        trackers = list(list(eval(tracker_response.text)))
        send_welcome_message(data=email, trackers=trackers)

    return "Monthly Report mail has been sent!"


@celery.task(name="tasks.reminders")
def reminders(emails):
    print("Inside daily reminder")

    for email in emails:
        url = "http://127.0.0.1:8000/daily_reminder/{}".format(email["user_id"])
        tracker_response = requests.request("GET", url)
        trackers = list(eval(tracker_response.text))
        send_daily_reminder(data=email, trackers=trackers)

    return "Daily Reminder mail has been sent!"


@celery.task(name="tasks.test")
def test():
    return "this is just a test"


# Celery Beat


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(),
        # crontab(hour=22, minute=30),
        reminders.s(emails),
        name="Daily Reminder at 10:30pm",
    )
    sender.add_periodic_task(
        crontab(),
        # crontab(0, 0, day_of_month="1"),
        send.s(emails),
        name="Monthly Report on the 1st of every month",
    )


# Celery Task for Exporting as CSV

# @celery.task(name="tasks.export")
# def export():
#     engine = sqlalchemy.create_engine(
#         "sqlite:///D:/Soumya/IITM Data Science/2AppDev/hello/src/project.sqlite3"
#     )
#     query = "select * from log where ltracker_id={}".format(tracker_id)
#     df = pd.read_sql(query, engine)
#     name = "./export/{}_logs.csv".format(tracker_id)
#     df.to_csv(name)
#     return "File has been created!"