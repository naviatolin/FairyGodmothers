""" Gives ability to make Log in and Create Account forms""" 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField


class LoginForm(FlaskForm):
    """ 
    A form for users to fill out in order to Log in 
    """
    username = StringField('Username', validators=[DataRequired()]) #This is the form for username
    password = PasswordField('Password', validators=[DataRequired()]) #This is the form for passwords
    remember_me = BooleanField('Remember Me') #This is the box for "Remember Me" option
    submit = SubmitField('Sign In') 

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])#this is the form for the title (summary in create_event)
    #due_date = DateTimeField('Due Date', validators=[DataRequired()])
    due_date = DateField('Due Date', format='%Y-%m-%d')
    time_est = SelectField('Estimated Time', choices=[('1', '1 hour'), ('2', '2 hours'), ('3', '3 hours'), ('4', '4 hours'), ('5', '5 hours'), ('6', '6 hours'), ('7', '7 hours'),
    ('8', '8 hours'), ('9', '9 hours'), ('9', '9 hours'), ('10', '10 hours'), ('11', '11 hours'), ('12', '12 hours'), ('13', '13 hours'), ('14', '14 hours'), ('15', '15 hours'),
    ('16', '16 hours'), ('17', '17 hours'), ('18', '18 hours'), ('19', '19 hours'), ('20', '20 hours'), ('21', '21 hours'), ('22', '22 hours'), ('23', '23 hours'), ('24', '24 hours')])
    stress = SelectField('Stress Level', choices=[('1', 'Level 1'), ('2', 'Level 2'), ('3', 'Level 3')])
    submit = SubmitField('Submit')

class EventForm(FlaskForm):
    eventname = StringField('Title', validators=[DataRequired()])
    dayofweek = SelectField('Day of the Week', choices=[('sun', 'Sunday'), ('mon', 'Monday'), ('tue', 'Tuesday'),
    ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday')])
    shour = SelectField('Start Hour', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')])
    smin = SelectField('Start Minute', choices=[(':00', ':00'), (':05', ':05'), (':10', ':10'), (':15', ':15'), (':20', ':20'), (':25', ':25'), (':30', ':30'), (':35', ':35'), (':40', ':40'), (':45', ':45'),
    (':50', ':50'), (':55', ':55')])
    day1 = SelectField('AM/PM', choices=[('am', 'am'), ('pm', 'pm')])
    ehour =  SelectField('Start Hour', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')])
    emin = SelectField('Start Minute', choices=[(':00', ':00'), (':05', ':05'), (':10', ':10'), (':15', ':15'), (':20', ':20'), (':25', ':25'), (':30', ':30'), (':35', ':35'), (':40', ':40'), (':45', ':45'),
    (':50', ':50'), (':55', ':55')])
    day2 = SelectField('AM/PM', choices=[('am', 'am'), ('pm', 'pm')])
    submit = SubmitField('Submit')

# class eventform(FlaskForm):
#     """ 
#     A form for users to fill out in order to Log in 
#     """
#     event_name= StringField('Event Name', validators=[DataRequired()]) #This is the form for username
#     password = PasswordField('Password', validators=[DataRequired()]) #This is the form for passwords
#     remember_me = BooleanField('Remember Me') #This is the box for "Remember Me" option
#     submit = SubmitField('Submit') 