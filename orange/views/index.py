from bottle import get, template, request
import x


##############################
@get("/")
def _():
  try:
    x.disable_cache()
    # Get logged user
    user = request.get_cookie("user", secret=x.COOKIE_SECRET)
    print("#"*30)
    print("user", user)
    # is_logged = False if user is None else True
    db = x.db()
    # user = db.execute("SELECT * FROM users WHERE user_name = ? LIMIT 1", ("elonmusk",)).fetchone()
    people = db.execute("SELECT * FROM users LIMIT 4").fetchall()
    tweets = db.execute("SELECT * FROM tweets JOIN users ON tweet_user_fk = user_id ORDER BY RANDOM() LIMIT 5").fetchall()
    print(tweets)
    trends = db.execute("SELECT * FROM trends LIMIT 5").fetchall()
    # user = {"user_first_name":"Twitter", "user_last_name":""}
    return template("index", title="Twitter", user=user, tweets=tweets, trends=trends, people=people)
  except Exception as ex:
    print(ex)
    return str(ex)
  finally:
    if "db" in locals(): db.close()