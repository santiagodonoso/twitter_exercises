
# Tailwind
# Inside the tailwindcss folder, run: 
# npx tailwindcss -i ./input.css -o ../app.css --watch 

from bottle import default_app, get, post, request, response, run, static_file, template
import git
import x

##############################
# Github will trigger this link in AWS
@post('/5cb8bb80eaaf4710bd477710fb1afd91300c5dea23f7447a9aa41b04d9959057')
def git_update():
  repo = git.Repo('./mysite')
  origin = repo.remotes.origin
  repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
  origin.pull()
  return ""
 
##############################
@get("/images/<filename>")
def _(filename):
  return static_file(filename, root="./images")

##############################
@get("/avatars/<filename>")
def _(filename):
  return static_file(filename, root="./avatars")

##############################
@get("/banners/<filename>")
def _(filename):
  return static_file(filename, root="./banners")

##############################
@get("/favicon.png")
def _():
  return static_file("favicon.png", root=".")

##############################
@get("/app.css")
def _():
  return static_file("app.css", root=".")

##############################
@get("/js/<filename>")
def _(filename):
  return static_file(filename, root="js")

##############################
@post("/test")
def _():
  print("#"*30)
  print(request.forms.get("user_name"))
  return "ok"

##############################
@get("/logout")
def _():
  response.add_header("Cache-Control", "no-cache, no-store, must-revalidate")
  response.add_header("Pragma", "no-cache")
  response.add_header("Expires", 0)    
  response.delete_cookie("user")
  response.status = 303
  response.set_header("Location", "/login")
  return

##############################
import views.index
import views.login
import views.profile
import views.test

##############################
import apis.api_login
import apis.api_tweet
import apis.api_sign_up
import apis.api_follow

##############################
try:
  import production
  application = default_app()
except Exception as ex:
  print("Running local server")
  run(host="127.0.0.1", port=80, debug=True, reloader=True)
 
