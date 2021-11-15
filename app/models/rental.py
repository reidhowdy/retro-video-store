from app import db

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)


    due_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime, nullable=True)


    #play around with making a rental_id as primary key 
    #play around w branching 

