from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint


db = SQLAlchemy()



class Section(db.Model):  #Section class name ---> section
    
    sec_id = db.Column(db.Integer(), primary_key =True)
    sec_name = db.Column(db.String(50), nullable = False)
    books = db.relationship("Book",backref = "section", cascade = "all,delete")

    def __repr__(self):
        return "<Section %r>" %self.sec_name
        

class Book(db.Model):
    
    book_id = db.Column(db.Integer(), primary_key =True)
    book_name = db.Column(db.String(50), nullable = False)
    sect = db.Column(db.Integer(), db.ForeignKey("section.sec_id"), nullable = False)

  
    def __repr__(self):
        return "<Books %r>" %self.book_name
        
