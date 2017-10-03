from flask import Flask, request, render_template
from cgi import escape
from re import match
regex_string = """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/",methods=["POST"])
def sign_up():
    #Where user fills out form
    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']

    username = escape(username)
    password = escape(password)
    verify = escape(verify)
    email = escape(email)

    email_regex_result = match(regex_string, email)
    print(email_regex_result)

    username_error = ""
    password_error = ""
    verify_error = ""
    email_error = ""

    if username == "" or " " in username or len(username) < 3 or len(username) > 20:
        username_error = "Invalid username"

    if password == "" or " " in password or len(password) < 3 or len(password) > 20:
        password_error = "Invalid password"

    if verify == "" or verify != password:
        verify_error = "invalid verification"

    if email != "":
        if "@" not in email or "." not in email or " " in email or len(email) < 3 or len(email) > 20:
            email_error = "Invalid email"


    if email_error == "" and username_error == "" and verify_error == "" and email_error == "":
        return render_template("welcome.html", username = username)
    else:
        return render_template("index.html" , username_error = username_error
                                            , password_error = password_error
                                            , verify_error = verify_error
                                            , email_error = email_error
                                            , username = username
                                            , email = email)


@app.route("/")
def index():
    return render_template("index.html")

app.run()