""" Creates routes """

from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, TaskForm, EventForm, SurveyForm
import os
import apiclient
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle 
import json
from datetime import datetime, timedelta
import datefinder
import requests
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

credentials = pickle.load(open("token.pkl", "rb"))
service = apiclient.discovery.build("calendar", "v3", credentials=credentials)

""" Connecting to my calendar """ 
result = service.calendarList().list().execute()
calendar_id = result['items'][0]['id']

""" Making New Event! """

def create_event(start_time_str, summary, duration=1, description=None, location=None):
    matches=list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=duration)
        
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start':{
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/New_York'
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/Chicago'
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10},
            ],
        },
        'recurrence': [
            'RRULE:FREQ=WEEKLY',
        ],
    }

def create_task(start_time_str, summary, duration=1, description=None, location=None):
    matches=list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=duration)
        
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start':{
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/New_York'
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/Chicago'
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    return service.events().insert(calendarId='primary', body=event).execute()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    """ Using LoginForm class, implements the structure of a create account page"""
    form = LoginForm()
    if form.validate_on_submit():
        #flash('Login requested for user {}, remember_me={}'.format(
            #form.username.data, form.remember_me.data))
        return redirect(url_for('survey'))
    return render_template('create_account.html',  title='Create Account', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Using LoginForm class, implements the structure of a log in page """
    form = LoginForm()
    if form.validate_on_submit():
        #flash('Login requested for user {}, remember_me={}'.format(
            #form.username.data, form.remember_me.data))
        return redirect(url_for('calendar'))
    return render_template('login.html',  title='Sign In', form=form)
    
@app.route('/calendar')
def calendar():
    return render_template('calendar.html', title='Calendar')

@app.route('/event', methods=['GET', 'POST'])
def event():
    form = EventForm()
    #print(due_date)
    if form.validate_on_submit():
        summary = request.form['eventname']
        day_of_week = request.form['dayofweek']
        start_hour = request.form['shour']
        start_min = request.form['smin']
        am1 = request.form['day1']
        end_hour = request.form['ehour']
        end_min = request.form['emin']
        am2 = request.form['day2'] 

        #print(summary, day_of_week, start_hour, start_min, am1)
        
        s = day_of_week + start_hour + start_min + am1 
        duration = ""
        if am1 == "am" and am2 == "pm":
            two = int(end_hour) + 12
            duration_hour = two - int(start_hour)
            duration_minute = int(end_min.strip(":")) - int(start_min.strip(":"))
            minutes = duration_minute/60
            duration = duration_hour + minutes
            duration = duration - 1

        elif am1 == "am" and am2 == "am":
            duration_hour = int(end_hour) - int(start_hour)
            duration_minute = int(end_min.strip(":")) - int(start_min.strip(":"))
            minutes = duration_minute/60
            duration = duration_hour + minutes
            duration = duration - 1

        elif am1 == "pm" and am2 == "pm":
            one = int(start_hour) + 12
            two = int(end_hour) + 12
            duration_hour = two - one
            duration_minute = int(end_min.strip(":")) - int(start_min.strip(":"))
            minutes = duration_minute/60
            duration = duration_hour + minutes           
            duration = duration - 1

        elif am1 == "pm" and am2 == "am":
            one = int(end_hour) + 12
            duration_hour = int(end_hour) - one
            duration_minute = int(end_min.strip(":")) - int(start_min.strip(":"))
            minutes = duration_minute/60
            duration = duration_hour + minutes
            duration = duration - 1
        
        create_event(s, summary, duration)
        return redirect(url_for('calendar'))
    return render_template('event.html', title= 'Events', form=form)
    

@app.route('/task', methods=['GET', 'POST'])
def task():
    form = TaskForm()
    if form.validate_on_submit():
        task_summary = request.form['title']
        due_date = request.form['due_date']
        time_est = request.form['time_est']
        stress = request.form['stress']
        is_placed = False

        with open('tasks.json', 'rb') as file:
            task_database = json.load(file)    

        task = {'task_summary' : task_summary,
                    'due_date' : due_date, 
                    'time_est': time_est,
                    'stress' : stress,
                    'is_placed' : is_placed}
        index = task_summary.strip()
        index = task_summary.replace(" ", "")
        index = index + str(due_date) + str(time_est)
        task_database[index] = task
                                                    
        with open('tasks.json', 'w') as f:
            json.dump(task_database, f)

        return redirect(url_for('calendar'))
    return render_template('task.html', title= 'Tasks', form=form)

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    form = SurveyForm()
    if form.validate_on_submit():
        one = request.form['level_one']
        two = request.form['level_two']
        three = request.form['level_three']
        start = request.form['start_day_hour']
        end = request.form['end_day_hour']
        lunch = request.form['lunch_hour']
        dinner = request.form['dinner_hour']

        user_info = {'level_one' : one,
                    'level_two' : two,
                    'level_three' : three}
        user_preference = {'start_day_hour' : start,
                            'end_day_hour' : end,
                            'lunch_hour' : lunch,
                            'dinner_hour' : dinner}
        with open('user_info.json', 'w') as f:
            json.dump(user_info, f)
        with open('user_preference.json', 'w') as f:
            json.dump(user_preference, f)
        return redirect(url_for('calendar'))    
    return render_template('survey.html', title='Survey', form=form)
        
        
        