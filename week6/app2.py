from flask import Flask, render_template
from model import *


app = Flask(__name__)

db.init_app(app)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabomo.sqlite3"

@app.route('/sections', methods = ['GET','POST'])

def all_sections():
    sections = Section.query.all()
    return render_template("all_sec.html")

if __name__=="__main__":
    app.run(debug=True)