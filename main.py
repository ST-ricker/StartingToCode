from flask import Flask, render_template, request, session, abort
import csv
import socket
from mailor import otp

from os import urandom

app = Flask(__name__)
app.secret_key = urandom(24)


trusted_ip: list[str] = ['49.36.223.50', '127.0.0.1', '165.225.124.177','27.63.162.177','49.36.221.226','165.225.124.172']
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
@app.before_request
def limit_remote_addr():
    if request.remote_addr not in trusted_ip:
     abort(404)  # Not Found


@app.route('/',methods=['GET'])
def home():
    session['attempt'] = 3
    # https: // stackoverflow.com / questions / 38825111 / counting - login - attempts - in -flask
    return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    while session['attempt'] > 0:
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            # *********** To add new users add the name and provide password in Login.csv file**********#
            with open('templates/login.csv', mode='r') as f:
                reader = csv.reader(f, delimiter=',')
                for row in reader:
                    if row == [email, password]:

                        session['login'] = email  # user session started//#
                        exec("otp(email)")
                        msg = "Enter otp which is sent to your registered email address"
                        return render_template('verify.html', msg=msg)

                    else:
                        # msg = "invalid username/password"
                        attempt=session.get('attempt')
                        attempt-=1
                        session['attempt']=attempt
                        msg= "Invalid Credentials Entered " \
                             " Attempts Remaining:"
                        attempt=attempt


                        return render_template("index.html", msg=msg, attempt=attempt)

    else:
        abort(404)


@app.route("/verify", methods=["Post", "Get"])
def verify():
    if request.method == "POST":
        oTp = request.form["oTp"]
        with open('file.csv', mode='r') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row == [oTp]:
                    return render_template("welcome.html")
                else:
                 msg = "enter valid otp"
                 return render_template('verify.html', msg=msg)
    else:
        abort(404,"method not allowed")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
