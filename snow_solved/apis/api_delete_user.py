from bottle import delete, request, response
import sqlite3

def dict_factory(cursor, row):
  col_names = [col[0] for col in cursor.description]
  return {key: value for key, value in zip(col_names, row)}


@delete("/user")
def _():
    try:
        user_id = request.forms.get("user_id", "")
        if not user_id: raise Exception(400, "Could not delete user")
        print(user_id)
        db = sqlite3.connect("company.db")
        db.row_factory = dict_factory
        deleted_rows = db.execute("DELETE FROM users WHERE user_id=?", (user_id,)).rowcount
        if not deleted_rows: raise Exception(400, "user not found")
        db.commit()

        return {"info":"ok", "user_id" : user_id}
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
