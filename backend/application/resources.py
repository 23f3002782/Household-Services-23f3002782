from flask_restful import Resource, reqparse
from .models import *
from flask_security import auth_required, roles_required, roles_accepted, hash_password, login_user,current_user, logout_user
from flask import request, jsonify
from flask import current_app as app
from datetime import datetime
from flask_security.utils import verify_password

def register_resources(api):
    api.add_resource(UsersResource, '/api/users')
    api.add_resource(CustomerSignupResource, '/api/signup/customer')
    api.add_resource(ServiceProfessionalSignupResource, '/api/signup/service_professional')
    api.add_resource(ServiceListResource, '/api/services')
    api.add_resource(ServiceResource, '/api/services/<int:service_id>')
    api.add_resource(ServiceRequestListResource, '/api/service-requests')
    api.add_resource(ServiceRequestResource, '/api/service-requests/<int:request_id>')
    api.add_resource(UserServiceRequestsResource, '/api/users/me/service-requests')
    api.add_resource(ProfessionalServiceRequestsResource, '/api/professionals/me/service-requests')
    api.add_resource(LoginResource, '/api/login')
    api.add_resource(LogoutResource, '/api/logout')
    api.add_resource(ProfessionalApprovalResource, '/api/professionals/<int:user_id>/approval')
    api.add_resource(BlockUserResource, '/api/users/<int:user_id>/block')
    api.add_resource(UnblockUserResource, '/api/users/<int:user_id>/unblock')

class UsersResource(Resource):
    @auth_required('token')
    @roles_required('admin')
    def get(self):
        try:
            users = User.query.all()
            return jsonify([{
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'role': user.roles[0].name if user.roles else None,
                'active': user.active,
                'status': user.status,
                'address': user.address,
                'about': user.about,
                'experience_years': user.experience_years,
                'service_id': user.service_id
            } for user in users])
        except Exception as e:
            return {'message': str(e)}, 500

class LoginResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', type=str, required=True, help='Email is required')
        self.parser.add_argument('password', type=str, required=True, help='Password is required')

    def post(self):
        args = self.parser.parse_args()
        user = app.security.datastore.find_user(email=args['email'])
        
        if not user:
            return {"message": "Invalid email or password"}, 401
            
        if not verify_password(args['password'], user.password):
            return {"message": "Invalid email or password"}, 401
            
        if not user.active:
            return {"message": "Account is deactivated"}, 401
        login_user(user)
        auth_token = user.get_auth_token()
        
        return {
            "message": "Login successful",
            "token": auth_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "role": user.roles[0].name if user.roles else None
            }
        }, 200
  
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
            
            user = app.security.datastore.find_user(email=email)
            login_user(user)
            auth_token = user.get_auth_token()

            return {
                "message": "Customer registered successfully",
                "token": auth_token,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "address": user.address,
                    "role": user.roles[0].name
                }
            }, 201
            
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
                active=False,
                status="pending"
            )

            db.session.commit()
            return {"message": "Request sent to admin for approval"}, 201
            
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error during registration: {str(e)}"}, 500
        
# GET: For list of services
# POST: For adding a new service
class ServiceListResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help='Name is required')
        self.parser.add_argument('base_price', type=float, required=True, help='Base price is required')
        self.parser.add_argument('time_required', type=int)
        self.parser.add_argument('description', type=str)

    def get(self):
        services = Service.query.all()
        return jsonify([{
            'id': service.id,
            'name': service.name,
            'base_price': service.base_price,
            'time_required': service.time_required,
            'description': service.description
        } for service in services])

    @auth_required('token')
    @roles_required('admin')
    def post(self):
        args = self.parser.parse_args()
        print(args)
        
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
        
        return jsonify({
            'id': service.id,
            'name': service.name,
            'base_price': service.base_price,
            'time_required': service.time_required,
            'description': service.description
        })

# GET: For getting a service by id
# PUT: For updating a service by id
# DELETE: For deleting a service by id
class ServiceResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('base_price', type=float)
        self.parser.add_argument('time_required', type=int)
        self.parser.add_argument('description', type=str)

    def get(self, service_id):
        service = Service.query.get_or_404(service_id)
        return {
            'id': service.id,
            'name': service.name,
            'base_price': service.base_price,
            'time_required': service.time_required,
            'description': service.description
        }
        

    @auth_required('token')
    @roles_required('admin')
    def put(self, service_id):
        service = Service.query.get_or_404(service_id)
        args = self.parser.parse_args()
        
        if args['name']:
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

    @auth_required('token')
    @roles_required('admin')
    def delete(self, service_id):
        service = Service.query.get_or_404(service_id)
        db.session.delete(service)
        db.session.commit()
        return {'message': 'Service deleted successfully'}, 204

class ServiceRequestListResource(Resource):
    @auth_required('token')
    @roles_accepted('admin', 'customer', 'service_professional')  
    def get(self):
        requests = ServiceRequest.query.all()
        return jsonify([{
            'id': req.id,
            'service_id': req.service_id,
            'customer_id': req.customer_id,
            'professional_id': req.professional_id,
            'status': req.status,
            'date_of_request': req.date_of_request.isoformat(),
            'date_of_completion': req.date_of_completion.isoformat() if req.date_of_completion else None,
            'review': req.review
        } for req in requests])

    @auth_required('token')
    @roles_required('customer')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service_id', type=int, required=True)
        args = parser.parse_args()
        
        request = ServiceRequest(
            service_id=args['service_id'],
            customer_id=current_user.id, 
            status='requested'
        )
        db.session.add(request)
        db.session.commit()
        return {'message': 'Service request created successfully'}, 201

class ServiceRequestResource(Resource):
    @auth_required('token')
    @roles_accepted('admin', 'customer', 'service_professional')
    def get(self, request_id):
        request = ServiceRequest.query.get_or_404(request_id)
        return {
            'id': request.id,
            'service_id': request.service_id,
            'customer_id': request.customer_id,
            'professional_id': request.professional_id,
            'status': request.status,
            'date_of_request': request.date_of_request.isoformat(),
            'date_of_completion': request.date_of_completion.isoformat() if request.date_of_completion else None,
            'review': request.review
        }

    @auth_required('token')
    @roles_accepted('admin', 'service_professional')
    def put(self, request_id):
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str)
        parser.add_argument('professional_id', type=int)
        parser.add_argument('review', type=str)
        parser.add_argument('date_of_completion', type=str)
        args = parser.parse_args()

        request = ServiceRequest.query.get_or_404(request_id)
        
        if args['status']:
            request.status = args['status']
        if args['professional_id']:
            request.professional_id = args['professional_id']
        if args['review']:
            request.review = args['review']
        if args['date_of_completion']:
            request.date_of_completion = datetime.fromisoformat(args['date_of_completion'])

        db.session.commit()
        return {'message': 'Service request updated successfully'}

class UserServiceRequestsResource(Resource):
    @auth_required('token')
    @roles_required('customer')
    def get(self):
        requests = ServiceRequest.query.filter_by(customer_id=current_user.id).all()
        return jsonify([{
            'id': req.id,
            'service_id': req.service_id,
            'status': req.status,
            'professional_id': req.professional_id,
            'date_of_request': req.date_of_request.isoformat(),
            'date_of_completion': req.date_of_completion.isoformat() if req.date_of_completion else None,
            'review': req.review
        } for req in requests])

class ProfessionalServiceRequestsResource(Resource):
    @auth_required('token')
    @roles_required('service_professional')
    def get(self):
        requests = ServiceRequest.query.filter_by(professional_id=current_user.id).all()
        return jsonify([{
            'id': req.id,
            'service_id': req.service_id,
            'customer_id': req.customer_id,
            'status': req.status,
            'date_of_request': req.date_of_request.isoformat(),
            'date_of_completion': req.date_of_completion.isoformat() if req.date_of_completion else None,
            'review': req.review
        } for req in requests])
        
class LogoutResource(Resource):
    @auth_required('token')
    def post(self):
        logout_user()
        return {"message": "Logged out successfully"}, 200

class ProfessionalApprovalResource(Resource):
    @auth_required('token')
    @roles_required('admin')
    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('action', type=str, required=True, help='Action (approve/reject) is required')
        args = parser.parse_args()

        user = User.query.get_or_404(user_id)
        
        if 'service_professional' not in [role.name for role in user.roles]:
            return {'message': 'User is not a service professional'}, 400

        try:
            if args['action'] == 'approve':
                user.active = True
                user.status = 'approved'
                message = 'Professional approved successfully'
            elif args['action'] == 'reject':
                user.status = 'rejected'
                message = 'Professional rejected'
            else:
                return {'message': 'Invalid action'}, 400
                
            db.session.commit()
            return {'message': message}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error processing approval: {str(e)}'}, 500

class BlockUserResource(Resource):
    @auth_required('token')
    @roles_required('admin')
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        user.active = False
        user.status = 'blocked'
        db.session.commit()
        return {'message': 'User blocked successfully'}, 200

class UnblockUserResource(Resource):
    @auth_required('token')
    @roles_required('admin')
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        user.active = True
        db.session.commit()
        return {'message': 'User unblocked successfully'}, 200
