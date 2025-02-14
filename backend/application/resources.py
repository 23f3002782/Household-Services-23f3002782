from flask_restful import Resource
from .models import *
from flask_security import auth_required, roles_required, hash_password
from flask import request
from flask import current_app as app

def register_resources(api):
    api.add_resource(CustomerSignupResource, '/api/signup/customer')
    api.add_resource(ServiceProfessionalSignupResource, '/api/signup/service_professional')
    
# Use http://127.0.0.1:5000/login?include_auth_token for login
  
class CustomerSignupResource(Resource):
    def post(self):
        data = request.get_json(force=True) or {}
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        
        if not email or not username or not password:
            return {"message": "Missing required fields"}, 400
        
        if app.security.datastore.find_user(email = email):
            return {"message": "User already exists"}, 400

        customer_role = app.security.datastore.find_role('customer')

        app.security.datastore.create_user(
            email=email,
            username=username,
            password=hash_password(str(password)),
            roles=[customer_role]
        )
        db.session.commit()

        return {"message": "Customer registered successfully"}, 201

class ServiceProfessionalSignupResource(Resource):
    def post(self):
        data = request.get_json(force=True) or {}
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        service_id = data.get('service_id')  # The ID of the service they specialize in
        about = data.get('about', '')
        experience_years = data.get('experience_years', None)
        
        if not email or not username or not password or not service_id:
            return {"message": "Missing required fields. Required: email, username, password, service_id"}, 400

        if app.security.datastore.find_user(email=email):
            return {"message": "User already exists"}, 400
        
        service_prof_role = app.security.datastore.find_role('service_professional')

        new_user = app.security.datastore.create_user(
            email=email,
            username=username,
            password=hash_password(str(password)),
            roles=[service_prof_role]
        )

        db.session.commit()
        
        # Creating the associated service professional profile
        profile = ServiceProfessionalProfile(
            user_id=new_user.id,
            service_id=int(service_id),
            about=about if about else '',
            experience_years=int(experience_years) if experience_years else None
        )
        db.session.add(profile)
        db.session.commit()

        return {"message": "Service Professional registered successfully"}, 201