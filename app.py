from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
app = Flask(__name__)

app.secret_key = "abcde"
session = {}

@app.route("/",methods=['GET'])
def index():
    isLogin = False
    if "username" in session:
        isLogin = True
    return render_template("index.html", isLogin=isLogin)

@app.route("/dashboard/",methods=['GET'])
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/chat",methods=['GET'])
def chat():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("chat.html")
@app.route("/about",methods=['GET','POST'])
def about():
    return render_template('about.html')

@app.route("/bsurvey",methods=['GET','POST'])
def bsurvey():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template('before_survey.html')

@app.route("/assistants",methods=['GET','POST'])
def assistants():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template('assistants.html')
@app.route("/result/<int:score>",methods=['GET','POST'])
def result(score):
    return render_template('result.html', score=score)
@app.route("/statistics",methods=['GET','POST'])
def statistics():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template('statistics.html')
@app.route("/survey",methods=['GET','POST'])
def survey():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template('survey.html')

@app.route("/survey_d",methods=['GET','POST'])
def survey_d():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template('survey_d.html')

@app.route("/survey_g",methods=['GET','POST'])
def survey_g():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template('survey_g.html')
@app.route("/result_d/<int:score>",methods=['GET','POST'])
def result_d(score):
    return render_template('result_d.html', score=score)
@app.route('/calculate_d', methods=['POST'])
def calculate_score_d():
    total_score = 0
    for key in request.form:
        total_score += int(request.form[key])

    return redirect(url_for('result_d', score=total_score))
@app.route("/result_g/<int:score>",methods=['GET','POST'])
def result_g(score):
    return render_template('result_g.html', score=score)
@app.route('/calculate_g', methods=['POST'])
def calculate_score_g():
    total_score = 0
    for key in request.form:
        total_score += int(request.form[key])

    return redirect(url_for('result_g', score=total_score))
@app.route('/calculate', methods=['POST'])
def calculate_score():
    total_score = 0
    for key in request.form:
        total_score += int(request.form[key])

    return redirect(url_for('result', score=total_score))


@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == "POST": #submitting
		username = request.form.get("username")
		password = request.form.get("password")

		input_password = password.encode('utf-8')

		conn = sqlite3.connect('static/database.db')
		cursor = conn.cursor()
		cursor.execute("Select password from Users where username=?", (username,)) # cursor -> ()
		hashed_password = cursor.fetchone() # (1234,)
		if hashed_password is None: # when input username is x in DB
			flash("Invalid username or password!")
			return render_template('login.html')

		hashed_password = hashed_password[0]
		conn.close()

		if hashed_password == password: # 1010 == 1010
			session["username"] = username # session = {"username": test1}
			return redirect(url_for('index')) #index = homepage
		else:
			flash("Invalid username or password!")
			return render_template('login.html')
	else: #if method == GET #accessing login page
		if "username" in session:
			return redirect(url_for('index'))
		return render_template('login.html')
@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == "POST":  # submitting the registration form
        username = request.form.get("username")
        password = request.form.get("password")
        gender = request.form.get("gender")
        age = request.form.get("age")

        # Connect to the database
        conn = sqlite3.connect('static/database.db')
        cursor = conn.cursor()

        # Check if the username already exists in the database
        cursor.execute("SELECT * FROM Users WHERE username=?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:  # If the username already exists
            flash("Username already exists. Please choose a different username.")
            conn.close()
            return render_template('register.html')


        cursor.execute("INSERT INTO Users (username, password, gender, age) VALUES (?, ?, ?, ?)",
                       (username, password, gender, age))
        conn.commit()
        conn.close()

        flash("Registration successful! You can now log in.")
        return redirect(url_for('login'))

    else:  # Accessing the registration page via GET request
        if "username" in session:  # If user is already logged in, redirect to index/homepage
            return redirect(url_for('index'))
        return render_template('register.html')
@app.route("/logout",methods=['GET'])
def logout():
    session.clear() # remove everything in session
    return render_template("index.html")

if __name__=="__main__":
    app.run(host="127.0.0.1",port=8000,debug=True)
