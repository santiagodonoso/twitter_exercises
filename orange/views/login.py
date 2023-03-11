from bottle import get, template, request, response
import x
##############################
@get("/login")
def _():
	x.disable_cache()
	# if user is logged, go to the profile page of that user
	user = request.get_cookie("user", secret=x.COOKIE_SECRET)
	if user:
		response.status = 303
		response.set_header("Location", f"/{user['user_name']}")
		return
	return template("login")












