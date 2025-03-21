from .database import db
from flask_security import UserMixin, RoleMixin
from datetime import datetime, timezone

# ----------------------------------------------------
# 1. Basic User and Role Models (for authentication)
# ----------------------------------------------------

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    status = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(500), nullable=True)
    
    # Service Professional specific fields
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=True)
    about = db.Column(db.Text, nullable=True)
    experience_years = db.Column(db.Integer, nullable=True)
    professional_since = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=True)
    
    # Many-to-many relationship to roles
    roles = db.relationship('Role', backref='bearer', secondary='users_roles')
    
    # Relationships for service requests.
    # A user can be a customer who creates many requests...
    customer_requests = db.relationship(
        'ServiceRequest', 
        backref='customer', 
        foreign_keys='ServiceRequest.customer_id'
    )
    # ...and can also be assigned as a service professional for many requests.
    professional_requests = db.relationship(
        'ServiceRequest', 
        backref='professional', 
        foreign_keys='ServiceRequest.professional_id'
    )
    
    # Relationship with service (for professionals)
    service = db.relationship('Service', backref='professionals')
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'address': self.address,
            'about': self.about,
            'experience_years': self.experience_years,
            'service_id': self.service_id,
            'status': self.status,
            'professional_since': self.professional_since.isoformat() if self.professional_since else None,
            'active': self.active,
            'role': self.roles[0].name
        }

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

# ----------------------------------------------------
# 2. Service Model
# ----------------------------------------------------
# This table represents the different types of services offered 
# (e.g., AC servicing, plumbing, etc.)

class Service(db.Model):
    __tablename__ = 'service'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    no_of_bookings = db.Column(db.Integer, nullable=True)
    
    # A service can be linked to many service requests.
    service_requests = db.relationship('ServiceRequest', backref='service', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'base_price': self.base_price,
            'time_required': self.time_required,
            'description': self.description,
            'no_of_bookings': self.no_of_bookings
        }

# ----------------------------------------------------
# 3. Service Request Model
# ----------------------------------------------------
# This table holds the service requests that customers create.
# It links to the Service, the Customer who made the request,
# and the Service Professional (if assigned).

class ServiceRequest(db.Model):
    __tablename__ = 'service_request'
    
    id = db.Column(db.Integer, primary_key=True)
    
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # NULL until a professional is assigned.
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    date_of_request = db.Column(db.DateTime, nullable=False)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    
    # Track status ('requested', 'assigned', 'closed')
    status = db.Column(db.String(50), nullable=False, default='requested')
    
    review = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'service_id': self.service_id,
            'customer_id': self.customer_id,
            'professional_id': self.professional_id,
            'date_of_request': self.date_of_request,
            'date_of_completion': self.date_of_completion,
            'status': self.status,
            'review': self.review,
            'service': self.service.to_dict(),
            'professional': self.professional.to_dict() if self.professional else None,
            'customer': self.customer.to_dict()
        }
