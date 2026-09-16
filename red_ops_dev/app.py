from flask import Flask, render_template, request, redirect, make_response
import jwt, base64, datetime, os

app = Flask(__name__)
SECRET_KEY = os.environ.get("SECRET_KEY", "phantom123")
FLAG = os.environ.get("FLAG", "GHOST{classified_note_flag}")

@app.route("/")
def home():
    return render_template("portal.html")

@app.route("/shadow_portal")
def shadow_portal():
    payload = {
        "role": "user",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return f"Your JWT: {token}"

@app.route("/admin")
def admin():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if decoded.get("role") == "admin":
            cookie_val = base64.b64encode(FLAG.encode()).decode()
            resp = make_response("Welcome Admin! Cookie set.")
            resp.set_cookie("classified_note", cookie_val)
            return resp
        else:
            return "Access denied."
    except Exception as e:
        return f"Invalid token: {e}"
    
# TODO: replace weak secret '   ' before production

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
