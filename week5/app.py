from flask_sqlalchemy import SQLAlchemy as sa
from flask_sqlalchemy import sqlalchemy 
import os
from flask import Flask, request, redirect, url_for
from flask import render_template as rt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'

db = sa(app)
db.init_app(app)
app.app_context().push()

## Database Model Classes

class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String) 
 
class Enrollments(db.Model):
    __tablename__ = "enrollments"
    enrollment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    estudent_id = db.Column(db.Integer,db.ForeignKey("student.student_id"), nullable=False)
    ecourse_id = db.Column(db.Integer,db.ForeignKey("student.student_id"), nullable=False)
   

@app.route("/", methods=["GET"])
def index():
    sts = Student.query.all()
    if sts == []:
        return rt("index.html", no_data_display='inline', data_display='none', sts = sts)
    else:
        return rt("index.html", no_data_display='none', data_display='table', sts = sts)


@app.route("/student/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return rt("c_.html")
    if request.method == "POST":
        rolln = request.form["roll"]
        fname = request.form["f_name"]
        lname = request.form["l_name"]
        courses = request.form.getlist("courses")
        try:
            db.session.add(Student(roll_number=rolln, first_name=fname,last_name=lname))
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return rt("err_.html")
        for c in courses:
            enroll = Enrollments(estudent_id = Student.query.filter_by(roll_number=rolln).first().student_id, ecourse_id=int(c[-1]))
            db.session.add(enroll)
            db.session.commit()
            
        return redirect(url_for("index"))


@app.route("/student/<int:student_id>/update", methods=["GET", "POST"])
def update(student_id):
    if request.method == "GET":
        student = Student.query.filter_by(student_id = student_id).first()
        return rt("u_.html", student = student)
    if request.method == "POST":
        fname = request.form["f_name"]
        lname = request.form["l_name"]
        courses = request.form.getlist("courses")
        c_id = []
        for c in courses:
            c_id.append(int(c[-1]))
        student = Student.query.filter_by(student_id = student_id).first()
        student.first_name = fname
        db.session.commit()
        student.last_name = lname
        db.session.commit()
        old_enrolls = Enrollments.query.filter_by(estudent_id = student_id).all()
        for enroll in old_enrolls:
            if enroll.enrollment_id in c_id:
                c_id.remove(enroll.enrollment_id) 
                
            if enroll.enrollment_id not in c_id:
                db.session.delete(enroll)
                db.session.commit()
        
        for c in c_id:
            db.session.add(Enrollments(estudent_id=student_id, ecourse_id = c))
            db.session.commit()
        
        return  redirect(url_for("index"))  
 
 
        
@app.route("/student/<int:student_id>/delete", methods=["GET"])    
def delete(student_id):
    student_details = Student.query.filter_by(student_id = student_id).delete()
    db.session.commit()
    enroll_details = Enrollments.query.filter_by(estudent_id=student_id).delete()
    db.session.commit()
    return redirect(url_for("index"))
      
      
@app.route("/student/<int:student_id>", methods=["GET"])
def display(student_id):
    student_details = Student.query.filter_by(student_id = student_id).first()
    course_details = db.engine.execute(f"""
                    select * 
                    from Course 
                    where course_id in 
                    (select ecourse_id 
                    from Enrollments
                    where estudent_id = {student_id})
                    """)
    return rt("display.html", student=student_details, courses=course_details)
         
if __name__ == '__main__':
    app.run()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   
