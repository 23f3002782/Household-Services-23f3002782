from flask import Flask 
from application.database import db 
from application.models import User, Role, Service
from application.config import LocalDevelopmentConfig
from flask_security import Security, SQLAlchemyUserDatastore, hash_password
from application.celery_init import celery_init_app
from flask_restful import Api
from flask_cors import CORS
from celery.schedules import crontab # type: ignore
from application.tasks import *

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
celery = celery_init_app(app)
celery.autodiscover_tasks()
api = Api(app)

with app.app_context():
    db.create_all()

    app.security.datastore.find_or_create_role(name = "admin", description = "Superuser of app")
    app.security.datastore.find_or_create_role(name = "service_professional", description = "Provide service to customers")
    app.security.datastore.find_or_create_role(name = "customer", description = "Receive service from service professionals")
    db.session.commit()

    if not app.security.datastore.find_user(email = "admin@email.com"):
        app.security.datastore.create_user(email = "admin@email.com",
                                           username = "admin",
                                           status="approved",
                                           password = hash_password("1234"),
                                           roles = ['admin'])

    db.session.commit()

    # Create dummy services
    services = [
        Service(
            name="Home Cleaning",
            description="Professional home cleaning service including dusting, vacuuming, and sanitization",
            base_price=80.00,
            time_required=3,
            no_of_bookings=2
        ),
        Service(
            name="Plumbing Repair",
            description="Expert plumbing services including leak repair, pipe installation, and drain cleaning",
            base_price=120.00,
            time_required=2,
            no_of_bookings=4
        ),
        Service(
            name="Electrical Work",
            description="Licensed electrical services for installations, repairs, and maintenance",
            base_price=150.00,
            time_required=4,
            no_of_bookings=3
        ),
        Service(
            name="Pest Control",
            description="Comprehensive pest control treatment for all types of infestations",
            base_price=200.00,
            time_required=2,
            no_of_bookings=1
        ),
        Service(
            name="Carpet Cleaning",
            description="Deep carpet cleaning and stain removal using professional equipment",
            base_price=100.00,
            time_required=3,
            no_of_bookings=3
        )
    ]

    for service in services:
        if not Service.query.filter_by(name=service.name).first():
            db.session.add(service)

    db.session.commit()

    # Service Professionals
    service_professionals = [
        {
            "email": "john.plumber@email.com",
            "username": "John Smith",
            "password": hash_password("1234"),
            "experience_years": 8,
            "status": "approved",
            "service_id": 2,  # Plumbing
            "about": "Licensed plumber with 8 years of experience. Specialized in residential plumbing repairs and installations. Available 24/7 for emergency services.",
            "active": True
        },
        {
            "email": "mike.electrician@email.com",
            "username": "Mike Johnson",
            "password": hash_password("1234"),
            "experience_years": 12,
            "status": "approved",
            "service_id": 3,  # Electrical
            "about": "Master electrician with extensive experience in both residential and commercial electrical work. Certified in modern electrical systems and smart home installations.",
            "active": True
        },
        {
            "email": "sarah.cleaner@email.com",
            "username": "Sarah Wilson",
            "password": hash_password("1234"),
            "experience_years": 5,
            "status": "approved",
            "service_id": 1,  # Home Cleaning
            "about": "Professional house cleaner specializing in deep cleaning and organization. Eco-friendly cleaning products used. Great attention to detail.",
            "active": True
        },
        {
            "email": "david.pest@email.com",
            "username": "David Brown",
            "password": hash_password("1234"),
            "experience_years": 15,
            "status": "approved",
            "service_id": 4,  # Pest Control
            "about": "Certified pest control specialist with 15 years of experience. Expert in handling all types of pest infestations. Environment-friendly treatment methods.",
            "active": True
        },
        {
            "email": "lisa.carpet@email.com",
            "username": "Lisa Davis",
            "password": hash_password("1234"),
            "experience_years": 7,
            "status": "approved",
            "service_id": 5,  # Carpet Cleaning
            "about": "Specialized in carpet and upholstery cleaning. Using latest steam cleaning technology. Stain removal expert with attention to fabric care.",
            "active": True
        }
    ]

    # Customers
    customers = [
        {
            "email": "emma.parker@email.com",
            "username": "Emma Parker",
            "password": hash_password("1234"),
            "status": "approved",
            "address": "42 Oak Street, Riverside Gardens, Building C, Apt 301",
            "active": True
        },
        {
            "email": "robert.chen@email.com",
            "username": "Robert Chen",
            "password": hash_password("1234"),
            "status": "approved",
            "address": "157 Maple Avenue, Silver Lake Heights, House 12",
            "active": True
        },
        {
            "email": "agrim@email.com",
            "username": "Agrim Srivastava",
            "password": hash_password("1234"),
            "status": "approved",
            "address": "89 Pine Road, Greenview Estate, Tower B, Flat 1204",
            "active": True
        }
    ]

    # Create service professionals
    for sp in service_professionals:
        if not app.security.datastore.find_user(email=sp["email"]):
            app.security.datastore.create_user(
                email=sp["email"],
                username=sp["username"],
                password=sp["password"],
                experience_years=sp["experience_years"],
                status=sp["status"],
                service_id=sp["service_id"],
                about=sp["about"],
                active=sp["active"],
                roles=['service_professional']
            )

    # Create customers
    for customer in customers:
        if not app.security.datastore.find_user(email=customer["email"]):
            app.security.datastore.create_user(
                email=customer["email"],
                username=customer["username"],
                password=customer["password"],
                status=customer["status"],
                address=customer["address"],
                active=customer["active"],
                roles=['customer']
            )

    db.session.commit()

from application.resources import register_resources
register_resources(api)

@celery.on_after_finalize.connect 
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute = '*/5'),
        monthly_report.s(),
    )
    sender.add_periodic_task(
        crontab(minute = '*/1'),
        remind_professional.s()
    )


if __name__ == "__main__":
    app.run()
