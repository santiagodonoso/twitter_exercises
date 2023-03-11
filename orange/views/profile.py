from bottle import get, response, template
import x

##############################
@get("/<username:re:[a-zA-z]{2,20}>")
def _(username):
  try:
    # Fully disable caching 
    x.disable_cache()
    # if logged, then utilize the user
    user = x.validate_user_logged()
    db = x.db()
    profile = db.execute("SELECT * FROM users WHERE user_name = ? LIMIT 1", (username,)).fetchone()
    print("#"*30)
    print("profile", profile)    
    if profile is None: raise Exception("profile not found")
    tweets = db.execute("SELECT * FROM tweets JOIN users ON tweet_user_fk = user_id WHERE tweet_user_fk = ? LIMIT 10", (profile["user_id"],)).fetchall()
    people = db.execute("SELECT * FROM users LIMIT 4").fetchall()
    trends = db.execute("SELECT * FROM trends LIMIT 5").fetchall()
    return template("profile", user=user, profile=profile, tweets=tweets, people=people, trends=trends)
  except Exception as ex:
    print(ex)
    response.status = 303
    response.set_header("Location", "/")
    return
  finally:
    if "db" in locals(): db.close()


