from flask_restful import Resource, reqparse
from .models import *
from flask_security import auth_required, roles_required, hash_password
from flask import request, jsonify
from flask import current_app as app

def register_resources(api):
    api.add_resource(CustomerSignupResource, '/api/signup/customer')
    api.add_resource(ServiceProfessionalSignupResource, '/api/signup/service_professional')
    api.add_resource(ServiceListResource, '/api/services')
    api.add_resource(ServiceResource, '/api/services/<int:service_id>')
    
# Use http://127.0.0.1:5000/login?include_auth_token for login
  
class CustomerSignupResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', type=str, required=True, help='Email is required')
        self.parser.add_argument('username', type=str, required=True, help='Username is required')
        self.parser.add_argument('password', type=str, required=True, help='Password is required')
        self.parser.add_argument('address', type=str)

    def post(self):
        args = self.parser.parse_args()
        email = args['email']
        username = args['username']
        password = args['password']
        address = args['address']
        
        if app.security.datastore.find_user(email=email):
            return {"message": "User already exists"}, 400

        try:
            customer_role = app.security.datastore.find_role('customer')

            app.security.datastore.create_user(
                email=email,
                username=username,
                password=hash_password(str(password)),
                roles=[customer_role],
                address=address
            )
            db.session.commit()

            return {"message": "Customer registered successfully"}, 201
            
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error during registration: {str(e)}"}, 500

class ServiceProfessionalSignupResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', type=str, required=True, help='Email is required')
        self.parser.add_argument('username', type=str, required=True, help='Username is required')
        self.parser.add_argument('password', type=str, required=True, help='Password is required')
        self.parser.add_argument('service_id', type=int, required=True, help='Service ID is required')
        self.parser.add_argument('about', type=str)
        self.parser.add_argument('experience_years', type=int)

    def post(self):
        try:
            args = self.parser.parse_args()
            
            if app.security.datastore.find_user(email=args['email']):
                return {"message": "User already exists"}, 400
            
            service_prof_role = app.security.datastore.find_role('service_professional')

            app.security.datastore.create_user(
                email=args['email'],
                username=args['username'],
                password=hash_password(str(args['password'])),
                roles=[service_prof_role],
                service_id=args['service_id'],
                about=args['about'],
                experience_years=args['experience_years'],
            )

            db.session.commit()
            return {"message": "Service Professional registered successfully"}, 201
            
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error during registration: {str(e)}"}, 500
        
class ServiceListResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help='Name is required')
        self.parser.add_argument('base_price', type=float, required=True, help='Base price is required')
        self.parser.add_argument('time_required', type=int)
        self.parser.add_argument('description', type=str)

    def get(self):
        """Get all services"""
        services = Service.query.all()
        return jsonify([{
            'id': service.id,
            'name': service.name,
            'base_price': service.base_price,
            'time_required': service.time_required,
            'description': service.description
        } for service in services])

    def post(self):
        """Create a new service"""
        args = self.parser.parse_args()
        
        # Check if service with same name already exists
        if Service.query.filter_by(name=args['name']).first():
            return {'message': 'Service with this name already exists'}, 400
        
        service = Service(
            name=args['name'],
            base_price=args['base_price'],
            time_required=args['time_required'],
            description=args['description']
        )
        
        db.session.add(service)
        db.session.commit()
        
        return {
            'id': service.id,
            'name': service.name,
            'base_price': service.base_price,
            'time_required': service.time_required,
            'description': service.description
        }, 201

class ServiceResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('base_price', type=float)
        self.parser.add_argument('time_required', type=int)
        self.parser.add_argument('description', type=str)

    def get(self, service_id):
        """Get a specific service"""
        service = Service.query.get_or_404(service_id)
        return {
            'id': service.id,
            'name': service.name,
            'base_price': service.base_price,
            'time_required': service.time_required,
            'description': service.description
        }

    def put(self, service_id):
        """Update a specific service"""
        service = Service.query.get_or_404(service_id)
        args = self.parser.parse_args()
        
        # Update only provided fields
        if args['name']:
            # Check if new name conflicts with existing service (excluding current service)
            existing = Service.query.filter(Service.name == args['name'], Service.id != service_id).first()
            if existing:
                return {'message': 'Service with this name already exists'}, 400
            service.name = args['name']
            
        if args['base_price'] is not None:
            service.base_price = args['base_price']
        if args['time_required'] is not None:
            service.time_required = args['time_required']
        if args['description'] is not None:
            service.description = args['description']
            
        db.session.commit()
        
        return {
            'id': service.id,
            'name': service.name,
            'base_price': service.base_price,
            'time_required': service.time_required,
            'description': service.description
        }

    def delete(self, service_id):
        """Delete a specific service"""
        service = Service.query.get_or_404(service_id)
        db.session.delete(service)
        db.session.commit()
        return '', 204