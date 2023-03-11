from bottle import post, request, response
import x
import uuid

##############################
@post("/api-tweet")
def _():
    try:
        user = x.validate_user_logged()
        x.validate_tweet_message()
        tweet_id = str(uuid.uuid4()).replace("-", "")
        db = x.db()
        db.execute("INSERT INTO usersx VALUES(?,?)")
        return {"info":"tweet created", "tweet_id":tweet_id}
    except Exception as e:
        print(e)
        try: # Controlled exception, usually comming from the x file
            response.status = e.args[0]
            return {"info":e.args[1]}
        except: # Something unknown went wrong
            response.status = 500
            return {"info":str(e)}
    finally:
        print("closing db")
        if "db" in locals(): db.close()













