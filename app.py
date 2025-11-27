from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/test/', methods=["GET", "POST"])
def test():
    if request.method == "POST":
        if "helfer" in request.form:
            action = request.form["helfer"]
            if action == "login":
                return "Helfer Login ausgewählt"
            elif action == "register":
                return "Helfer Registrierung ausgewählt"

        if "kunde" in request.form:
            action = request.form["kunde"]
            if action == "login":
                return "Kunde Login ausgewählt"
            elif action == "register":
                return "Kunde Registrierung ausgewählt"
    
    return render_template('test.html')
