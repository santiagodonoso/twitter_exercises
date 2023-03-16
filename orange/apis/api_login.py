from bottle import post, request, response
import x
import bcrypt

##############################
@post("/api-login")
def _():
	try:
		# if user is logged, return message to the API
		user = request.get_cookie("user", secret=x.COOKIE_SECRET)
		if user: return {"info":"success login", "user_name":user["user_name"]}
		# Validate
		user_email = x.validate_user_email()
		user_password = x.validate_user_password()
		# Connect to database
		db = x.db()
		user = db.execute("SELECT * FROM users WHERE user_email = ? LIMIT 1", (user_email,)).fetchone()
		print("#"*30)
		print(user)
		if not user: raise Exception(400, "Cannot login")
		if not bcrypt.checkpw(user_password.encode("utf-8"), user["user_password"]):
			raise Exception(400, "Invalid credentials")
		try:
			import production
			is_cookie_https = True
		except:
			is_cookie_https = False
		user.pop("user_password") # Do not put the password in the cookie
		response.set_cookie("user", user, secret=x.COOKIE_SECRET, httponly=True, secure=is_cookie_https)
		return {"info":"success login", "user_name":user["user_name"]}
	except Exception as e:
		print(e)
		try: # Controlled exception, usually comming from the x file
			response.status = e.args[0]
			return {"info":e.args[1]}
		except: # Something unknown went wrong
			response.status = 500
			return {"info":str(e)}
	finally:
		if "db" in locals(): db.close()


