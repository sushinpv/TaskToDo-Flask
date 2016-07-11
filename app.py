from flask import Flask,render_template
from flask import request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Task1(db.Model):#creating a table called task
	id = db.Column(db.Integer,primary_key=True)
	taskname = db.Column(db.Text)
	taskdes = db.Column(db.Text)
	taskproirity = db.Column(db.Text)
	taskdate = db.Column(db.Text)
	taskproject = db.Column(db.Text)
	taskstatus = db.Column(db.Text)
	status = db.Column(db.Boolean,default=False)

	def __init__(self,taskname,taskdes,taskproirity,taskdate,taskproject,taskstatus):
		self.taskname = taskname
		self.taskdes = taskdes
		self.taskproirity = taskproirity
		self.taskdate = taskdate
		self.taskproject = taskproject
		self.taskstatus = taskstatus
		self.status = False

db.create_all()#git commit -a -m "Created database"

@app.route("/")#for one url we can have only one function
def hello_world():
	tasks = Task1.query.all()
	return render_template('list.html',tasks=tasks)

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
	tasks =  Task1.query.get(task_id)
	db.session.delete(tasks)
	#print(task_id)
	#if task:
	#	return redirect("/")
	db.session.commit()
	return redirect("/")

@app.route("/edit/<int:task_id>")
def edit_task(task_id):
	tasks =  Task1.query.get(task_id)
	#tasks.status = True
	#db.session.add(tasks)
	#db.session.commit()
	return render_template('edit.html',task=tasks)

@app.route("/finish/<int:task_id>")
def finish_task(task_id):
	tasks =  Task1.query.get(task_id)
	tasks.status = True
	db.session.add(tasks)
	db.session.commit()
	return redirect("/")

@app.route("/add/",methods=["POST"])
def add_task():
	taskname = request.form["taskname"]
	taskdes = request.form["taskdes"]
	taskproirity = request.form["taskproirity"]
	taskdate = request.form["taskdate"]
	taskproject = request.form["taskproject"]
	taskstatus = request.form["taskstatus"]
	task = Task1(taskname,taskdes,taskproirity,taskdate,taskproject,taskstatus)
	db.session.add(task)
	db.session.commit()

	return redirect("/")

@app.route("/edit/",methods=["POST"])
def save_edit_task():
	#task = Task1()
	task =  Task1.query.get(request.form["id"])
	task.taskname = request.form["taskname"]
	task.taskdes = request.form["taskdes"]
	task.taskproirity = request.form["taskproirity"]
	task.taskdate = request.form["taskdate"]
	task.taskproject = request.form["taskproject"]
	task.taskstatus = request.form["taskstatus"]
	#task = Task1(taskname,taskdes,taskproirity,taskdate,taskproject,taskstatus)
	db.session.add(task)
	db.session.commit()

	return redirect("/")

if __name__=="__main__":
	app.run()