from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
chat_id = 0
app.secret_key = "abcde"
session = {}
def create_connection():
    conn = sqlite3.connect('static/database.db')
    return conn
@app.route("/",methods=['GET'])
def index():
    isLogin = False
    isAdmin = False
    if "username" in session:
        isLogin = True
        if session["username"] == "test123":
            isAdmin = True
    return render_template("index.html", isLogin=isLogin,isAdmin = isAdmin)

@app.route("/dashboard/",methods=['GET'])
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/chat",methods=['GET','POST'])
def chat():
    if request.method == "POST":
        global chat_id
        username = session["username"]
        age = request.form.get('age')
        gender = request.form.get('gender')
        location = request.form.get('location')
        symptom = request.form.get('symptom')
        date = datetime.now().strftime('%Y-%m-%d')
        chat_id += 1

        content = request.form.get('message')  # Assuming the message field is for content

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO chats (username, date, content, id, read,symptom,location,age,gender) VALUES (?, ?, ?, ?,?,?,?,?,?)',
                       (username, date, content, chat_id,0,symptom,location,age,gender))
        conn.commit()
        conn.close()
        return render_template("chat.html", submitted=True)
    else:
        isLogin = False
        if "username" not in session:
            return redirect(url_for("login"))
        else:
            isLogin=True
        return render_template("chat.html",isLogin=isLogin)
@app.route("/about",methods=['GET','POST'])
def about():
    isLogin = False
    isAdmin = False
    if "username" in session:
        isLogin = True
        if session["username"] == "test123":
            isAdmin = True
    return render_template('about.html',isLogin=isLogin,isAdmin=isAdmin)

@app.route("/bsurvey",methods=['GET','POST'])
def bsurvey():
    isLogin = False
    if "username" not in session:
        return redirect(url_for("login"))
    isLogin = True
    return render_template('before_survey.html',isLogin=isLogin)

@app.route("/assistants",methods=['GET','POST'])
def assistants():
    isLogin = False
    if "username" not in session:
        return redirect(url_for("login"))
    isLogin = True
    return render_template('assistants.html',isLogin=isLogin)
@app.route("/result/<int:score>",methods=['GET','POST'])
def result(score):
    isLogin = False
    if "username" in session:
        isLogin = True
    return render_template('result.html', score=score,isLogin=isLogin)
@app.route("/statistics",methods=['GET','POST'])
def statistics():
    isLogin = False
    if "username" not in session:
        return redirect(url_for("login"))
    isLogin=True
    return render_template('statistics.html',isLogin=isLogin)
@app.route("/survey",methods=['GET','POST'])
def survey():
    isLogin = False
    if "username" not in session:
        return redirect(url_for("login"))
    isLogin = True
    return render_template('survey.html',isLogin=isLogin)

@app.route("/survey_d",methods=['GET','POST'])
def survey_d():
    isLogin = False
    if "username" not in session:
        return redirect(url_for("login"))
    isLogin = True
    return render_template('survey_d.html',isLogin=isLogin)

@app.route("/survey_g",methods=['GET','POST'])
def survey_g():
    isLogin = False
    if "username" not in session:
        return redirect(url_for("login"))
    isLogin = True
    return render_template('survey_g.html',isLogin=isLogin)
@app.route("/result_d/<int:score>",methods=['GET','POST'])
def result_d(score):
    isLogin = False
    if "username" in session:
        isLogin = True
    return render_template('result_d.html', score=score,isLogin=isLogin)
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

        # flash("Registration successful! You can now log in.")
        return redirect(url_for('login'))

    else:  # Accessing the registration page via GET request
        if "username" in session:  # If user is already logged in, redirect to index/homepage
            return redirect(url_for('index'))
        return render_template('register.html')

@app.route("/chat_admin",methods=['GET'])
def chat_admin():
    conn = sqlite3.connect('static/database.db')  # Replace 'your_database.db' with your database file
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM chats")  # Fetch all chats from the 'chats' table
    chats = cursor.fetchall()  # Get all fetched chats
    print("AAAAA",chats)
    if "username" in session:
        isLogin = True
    conn.close()

    return render_template("chat_admin.html",chats=chats,isLogin=isLogin)

chat_messages = {}
@app.route('/reply-message', methods=['POST'])
def reply_message():
    if request.method == 'POST':
        conn = sqlite3.connect('static/database.db')  # Replace 'your_database.db' with your database file
        cursor = conn.cursor()
        data = request.get_json()

        # Extract data from the request
        username = data.get('username')
        date = datetime.now().strftime('%Y-%m-%d')
        content = data.get('message')

        # Save chat into the 'replay' table
        cursor.execute('INSERT INTO reply (toUsername, date, content) VALUES (?, ?, ?)', (username, date, content))
        conn.commit()

        return jsonify({'success': True, 'message': 'Message saved successfully'})

@app.route("/chat_user",methods=['GET'])
def chat_user():
    conn = sqlite3.connect('static/database.db')  # Replace 'your_database.db' with your database file
    cursor = conn.cursor()
    username = session["username"]
    cursor.execute("SELECT * FROM reply where toUsername =?",(username,))  # Fetch all chats from the 'chats' table
    chats = cursor.fetchall()  # Get all fetched chats
    print("AAAAA",chats)
    if "username" in session:
        isLogin = True
    conn.close()

    return render_template("chat_user.html",chats=chats,isLogin=isLogin)

@app.route("/logout",methods=['GET'])
def logout():
    session.clear() # remove everything in session
    return render_template("index.html")

if __name__=="__main__":
    app.run(host="127.0.0.1",port=8000,debug=True)
