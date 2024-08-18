from flask import Flask,render_template,request,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key="jkdbnsu7f8234c86rb4h3i64"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///studenaData.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Command to create db after this code
# >>> from app import app, db
# >>> app.app_context().push()
# >>> db.create_all()

class Students(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    class_ = db.Column(db.String(100), nullable=False)
    sec = db.Column(db.String(100), nullable=False)
    rollNo = db.Column(db.Integer, nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    admissionNo = db.Column(db.String(200), nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def home():
    allStudentData = Students.query.all()
    return render_template("home.html", data=allStudentData)

@app.route("/add",methods=['GET','POST'])
def add():
    if request.method == "POST":
        name = request.form["name"]
        class_ = request.form["class"]
        sec = request.form["section"]
        rollNo = request.form["rollNo"]
        marks = request.form["marks"]
        admissionNo = request.form["admissionNo"]

        if len(name) > 0 and len(class_)>0 and len(sec) >0 and len(rollNo)>0 and len(marks)>0 and len(admissionNo)>0:
            student = Students(name=name,class_ =class_,sec=sec,rollNo=rollNo,marks=marks,admissionNo=admissionNo)
            db.session.add(student)
            db.session.commit()
            print("add to db")
            flash("Successfully ! , data added to database.", "success")
            return redirect("/")
        else:
            flash("Error ! , Maybe some field is empty.", "danger")
        
    return render_template("add.html")

@app.route("/update/<int:sno>", methods=["GET","POST"])
def update(sno):

    student = Students.query.filter_by(sno=sno).first()

    if request.method == "POST":
        name = request.form["name"]
        class_ = request.form["class"]
        sec = request.form["section"]
        rollNo = request.form["rollNo"]
        marks = request.form["marks"]
        admissionNo = request.form["admissionNo"]

        if len(name) > 0 and len(class_)>0 and len(sec) >0 and len(rollNo)>0 and len(marks)>0 and len(admissionNo)>0:
            student.name = name
            student.class_ = class_
            student.sec = sec
            student.rollNo = rollNo 
            student.marks = marks
            student.admissionNo = admissionNo
            db.session.add(student)
            db.session.commit()
            print("add to db")
            flash("Successfully ! , data updated to database.", "success")
            return redirect("/")
        else:
            flash("Error ! , Maybe some field is empty.", "danger")
            
    return render_template("update.html", student=student)

@app.route("/delete/<int:sno>")
def delete(sno):
    student = Students.query.filter_by(sno=sno).first()
    db.session.delete(student)
    db.session.commit()
    flash("Successfully !, Deleted student data" , "success")
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True, port=8000)