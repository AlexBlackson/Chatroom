"""
Written by Alex Blackson
For CS1520 with Todd Waits
Last Editted: 11/1/17
"""

import json
from flask import Flask, request, abort, url_for, redirect, session, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
db = SQLAlchemy(app)

app.secret_key = "securityIsOverrated"

userChatrooms = db.Table('userChatrooms', 
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('chatroom_id', db.Integer, db.ForeignKey('chatroom.id'), primary_key=True)
)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80), unique=False)
	chatrooms = db.relationship('Chatroom', secondary=userChatrooms, backref = db.backref("user", lazy=True))

	def __init__(self, username, password):
		self.username = username
		self.password = password

class Chatroom(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	room = db.Column(db.String(80), unique=True)
	creator = db.Column(db.String(80), unique=False)
	messages = db.relationship("Message", backref="chatroom")

	def __init__(self, room, creator):
		self.room = room
		self.creator = creator

class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(700), unique=False)
	user = db.Column(db.String(80), unique=False)
	chatroom_id = db.Column(db.Integer, db.ForeignKey('chatroom.id'))

	def __init__(self, text, user):
		self.text = text
		self.user = user

@app.cli.command('initdb')
def initdb_command():

	db.drop_all()
	db.create_all()

	db.session.commit()
	print("Initialized the database")

@app.route('/')
def default():
	return redirect(url_for("login"))

@app.route("/login/", methods=["GET", "POST"])
def login():

	if "username" in session:
		return redirect(url_for("profile", username=session["username"]))

	if request.method == "POST":
		attempt = User.query.filter_by(username = request.form["username"]).first() 
		if attempt is not None:
			if attempt.username == request.form["username"] and attempt.password == request.form["password"]:
				session["username"] = attempt.username
				return redirect(url_for("profile", username=session["username"]))

	return render_template("loginPage.html")

@app.route("/newAccount/", methods=["GET", "POST"])
def addUser():
	if request.method == "POST":
		if isUsernameUnique(request.form["username"]):
			db.session.add(User(request.form["username"], request.form["password"]))
			db.session.commit()

			session["username"] = request.form["username"]
			return redirect(url_for("profile", username=session["username"]))

	return render_template("addUser.html")

@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username = None):

	session.pop("chatroom", None)
	
	if not username:
		return redirect(url_for("login"))

	if request.method == "POST":
		if isChatNameUnique(request.form["chatName"]):
			newChatroom = Chatroom(request.form["chatName"], session["username"])
			db.session.add(newChatroom)

			db.session.commit()

	return render_template("profile.html", username=session["username"], chatrooms=Chatroom.query.all())

@app.route("/chatroom/<room>", methods=["GET", "POST"])
def chat(room = None):

	if room is None:
		return redirect(url_for("profile", username=session["username"]))

	session["chatroom"] = room
	return render_template("chatroom.html", chatroom=room, username=session["username"], messages=Chatroom.query.filter_by(room=room).first().messages)


@app.route("/logout/")
def logout():
	# if logged in, log out, otherwise offer to log in
	if "username" in session:
		session.clear()
		return render_template("logoutPage.html")
	else:
		return redirect(url_for("login"))

@app.route("/send_message", methods=["POST"])
def addMessage():

	newMessage = Message(request.form["message"], session["username"])

	db.session.add(newMessage)

	currRoom = Chatroom.query.filter_by(room=request.form["chatroom"]).first()
	currRoom.messages.append(newMessage)

	newMessage.chatroom_id = currRoom
	db.session.commit()

	return "OK!"

@app.route("/messages")
def getMessages():
	if Chatroom.query.filter_by(room=session["chatroom"]).first() is None:
		return json.dumps(1)

	roomMessages = Chatroom.query.filter_by(room=session["chatroom"]).first().messages
	userMessages = []
	for m in roomMessages:
		userMessages.append([m.user, m.text])

	return json.dumps(userMessages)

@app.route("/deleteRoom/<chatName>")
def deleteChat(chatName = None):
	if chatName is None:
		return redirect(url_for("profile", username=session["username"]))
	
	db.session.delete(Chatroom.query.filter_by(room=chatName).first())
	
	db.session.commit()

	return redirect(url_for("profile", username=session["username"]))

def isUsernameUnique(name):
	if User.query.filter_by(username=name).first():
		return False
	else:
		return True

def isChatNameUnique(chatName):
	if Chatroom.query.filter_by(room=chatName).first():
		return False
	else:
		return True

if __name__ == '__main__':
	app.run(debug=True)