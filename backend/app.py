from flask import Flask 
from application.database import db 
from application.models import User, Role, Service
from application.config import LocalDevelopmentConfig
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security import hash_password
from flask_restful import Api
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore)
    app.app_context().push()

    CORS(app)

    return app

app = create_app()
api = Api(app)

with app.app_context():
    db.create_all()

    app.security.datastore.find_or_create_role(name = "admin", description = "Superuser of app")
    app.security.datastore.find_or_create_role(name = "service_professional", description = "Provide service to customers")
    app.security.datastore.find_or_create_role(name = "customer", description = "Receive service from service professionals")
    db.session.commit()

    if not app.security.datastore.find_user(email = "admin@user.com"):
        app.security.datastore.create_user(email = "admin@user.com",
                                           username = "admin",
                                           password = hash_password("1234"),
                                           roles = ['admin'])
        
    if not app.security.datastore.find_user(email = "sp1@user.com"):
        app.security.datastore.create_user(email = "sp1@user.com",
                                           username = "Sp1",
                                           password = hash_password("1234"),
                                           experience_years = 10,
                                           about = "I am a service professional. I have 10 years of experience in the field. I am very good at my job.",
                                           roles = ['service_professional'])
    if not app.security.datastore.find_user(email="cus1@user.com"):
        app.security.datastore.create_user(email="cus1@user.com",
                                        username="Cus1",
                                         password=hash_password("1234"),
                                         address="3/456, Sector-A, Vikas Nagar",
                                         roles=['customer'])

    db.session.commit()

    # Create dummy services
    services = [
        Service(
            name="Home Cleaning",
            description="Professional home cleaning service including dusting, vacuuming, and sanitization",
            base_price=80.00,
            time_required=3
        ),
        Service(
            name="Plumbing Repair",
            description="Expert plumbing services including leak repair, pipe installation, and drain cleaning",
            base_price=120.00,
            time_required=2
        ),
        Service(
            name="Electrical Work",
            description="Licensed electrical services for installations, repairs, and maintenance",
            base_price=150.00,
            time_required=4
        ),
        Service(
            name="Pest Control",
            description="Comprehensive pest control treatment for all types of infestations",
            base_price=200.00,
            time_required=2
        ),
        Service(
            name="Carpet Cleaning",
            description="Deep carpet cleaning and stain removal using professional equipment",
            base_price=100.00,
            time_required=3
        )
    ]

    for service in services:
        if not Service.query.filter_by(name=service.name).first():
            db.session.add(service)

    db.session.commit()

from application.routes import *

from application.resources import register_resources
register_resources(api)

if __name__ == "__main__":
    app.run()
