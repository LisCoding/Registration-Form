from flask import Flask, render_template, request, redirect, flash
import re
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = 'KeepItSecretKeepItSafe'
@app.route('/')
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    time = datetime.datetime.today().strftime("%Y-%m-%d")
    print time.split("-")
    info = {}
    info["First Name"] = request.form["f_name"]
    info["Last Name"] = request.form["l_name"]
    info["Email"] = request.form["email"]
    info["Password"] = request.form["pwd"]
    info["Confirmation password"] = request.form["confi_pwd"]
    info["Birth Date"] = request.form["birth_date"]
    date = info["Birth Date"].split("-")
    valid_date = True
    for i in range(0,3):
        if int(date[i]) > int(time[i]):
            valid_date = False
    print valid_date
    message = []
    for key in info.iterkeys():
        if info[key] == "":
            message += [key]
    if not len(message) == 0:
        flash((", ").join(message) + " can't be blank. Try again")
    elif info["First Name"].isalpha() == False or info["Last Name"].isalpha() == False:
        flash("Name and Last name should contain only alpha characters")
    elif not len(info["Password"]) > 8:
        flash("Password has to be a least 8 characters")
    elif not re.search("\d", info["Password"]):
        flash("Password need to have a least one digit")
    elif  bool(re.match(r'[A-Z]+$', info["Password"])):
        flash("Password need to have a least one uppercase letter")
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
    elif not info["Password"] == info["Confirmation password"]:
        flash("Password and confirmation password does not match")
    elif not valid_date:
        flash("Birth Date can't be in the future")
    else:
        flash("Thanks you for submitting your information")
    return redirect("/")

app.run(debug=True)
