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
    
    # One-to-one relationship with service professional profile 
    professional_profile = db.relationship(
        'ServiceProfessionalProfile', 
        backref='user', 
        uselist=False
    )

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
    
    # A service can be linked to many service requests.
    service_requests = db.relationship('ServiceRequest', backref='service', lazy=True)

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
    
    date_of_request = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    date_of_completion = db.Column(db.DateTime, nullable=True)
    
    # Track status ('requested', 'assigned', 'closed')
    status = db.Column(db.String(50), nullable=False, default='requested')

# ----------------------------------------------------
# 4. Service Professional Profile Model
# ----------------------------------------------------

class ServiceProfessionalProfile(db.Model):
    __tablename__ = 'service_professional_profile'
    
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    
    description = db.Column(db.Text, nullable=True)
    experience_years = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    # To access details of the service they offer.
    service = db.relationship('Service', backref='professionals')
