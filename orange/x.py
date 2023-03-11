from bottle import request, response
import sqlite3
import re
import pathlib

COOKIE_SECRET = "41ebeca46feb-4d77-a8e2-554659074C6319a2fbfb-9a2D-4fb6-Afcad32abb26a5e0"

##############################
def dict_factory(cursor, row):
  col_names = [col[0] for col in cursor.description]
  return {key: value for key, value in zip(col_names, row)}

##############################
def db():
  try:
    db = sqlite3.connect(str(pathlib.Path(__file__).parent.resolve())+"/twitter.db") 
    db.row_factory = dict_factory
    return db
  except Exception as ex:
    print(ex)
  finally:
    pass

##############################
def disable_cache():
    response.add_header("Cache-Control", "no-cache, no-store, must-revalidate")
    response.add_header("Pragma", "no-cache")
    response.add_header("Expires", 0)    

##############################
def validate_user_logged():
    user = request.get_cookie("user", secret=COOKIE_SECRET)
    if user is None: raise Exception(400, "user must login")
    return user


##############################

USER_EMAIL_MIN = 6
USER_EMAIL_MAX = 100
USER_EMAIL_REGEX = "^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"

def validate_user_email():
	error = f"user_email invalid"
	request.forms.user_email = request.forms.user_email.strip()
	if len(request.forms.user_email) < USER_EMAIL_MIN : raise Exception(400, error)
	if len(request.forms.user_email) > USER_EMAIL_MAX : raise Exception(400, error)  
	if not re.match(USER_EMAIL_REGEX, request.forms.user_email): raise Exception(400, error)
	return request.forms.user_email

##############################

USER_NAME_MIN = 2
USER_NAME_MAX = 20
USER_NAME_REGEX = "^[a-z]{2,20}$"

def validate_user_name():
	error = f"user_name {USER_NAME_MIN} to {USER_NAME_MAX} lowercased english letters"
	request.forms.user_name = request.forms.user_name.strip()
	if not re.match(USER_NAME_REGEX, request.forms.user_name): raise Exception(400, error)
	return request.forms.user_name

##############################

USER_PASSWORD_MIN = 6
USER_PASSWORD_MAX = 50

def validate_user_password():
	error = f"user_password {USER_PASSWORD_MIN} to {USER_PASSWORD_MAX} characters"
	request.forms.user_password = request.forms.user_password.strip()
	if len(request.forms.user_password) < USER_PASSWORD_MIN : raise Exception(400, error)
	if len(request.forms.user_password) > USER_PASSWORD_MAX : raise Exception(400, error)
	return request.forms.user_password

def validate_user_confirm_password():
	error = f"user_password and user_confirm_password do not match"
	request.forms.user_password = request.forms.user_password.strip()
	request.forms.user_confirm_password = request.forms.user_confirm_password.strip()
	if request.forms.user_confirm_password != request.forms.user_password: raise Exception(400, error)
	return request.forms.user_confirm_password

##############################

TWEET_MIN = 2
TWEET_MAX = 20

def validate_tweet_message():
	error = f"tweet_message {TWEET_MIN} to {TWEET_MAX} characters"
	request.forms.tweet_message = request.forms.tweet_message.strip()
	if len(request.forms.tweet_message) < TWEET_MIN : raise Exception(400, error)
	if len(request.forms.tweet_message) > TWEET_MAX : raise Exception(400, error)
	return request.forms.tweet_message

##############################






