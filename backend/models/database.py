from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Reservation(db.Model):
    __tablename__ = 'reservations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pet_type = db.Column(db.String(50), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    desired_date = db.Column(db.Date, nullable=False)
    desired_time = db.Column(db.Time, nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    owner_email = db.Column(db.String(100), nullable=False)
    owner_phone = db.Column(db.String(20))
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'pet_type': self.pet_type,
            'service_type': self.service_type,
            'desired_date': self.desired_date.isoformat() if self.desired_date else None,
            'desired_time': self.desired_time.isoformat() if self.desired_time else None,
            'owner_name': self.owner_name,
            'owner_email': self.owner_email,
            'owner_phone': self.owner_phone,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }