from flask import current_app as app, jsonify, send_from_directory
from flask_restful import Resource, reqparse
from flask_security import auth_required, roles_required, roles_accepted, hash_password, login_user, current_user, logout_user
from flask_security.utils import verify_password
from celery.result import AsyncResult
from datetime import datetime
from .models import *
from .tasks import *
from .mail import send_email

from flask_caching import Cache
cache = Cache(app)

def register_resources(api):
    api.add_resource(CustomerSignupResource, '/api/signup/customer')
    api.add_resource(ServiceProfessionalSignupResource, '/api/signup/service_professional')
    api.add_resource(LoginResource, '/api/login')
    api.add_resource(LogoutResource, '/api/logout')
    api.add_resource(ServiceResource, '/api/services', '/api/services/<int:service_id>')
    api.add_resource(CustomerServiceRequestsResource, '/api/customer/service-requests', '/api/customer/service-requests/<int:request_id>')
    api.add_resource(ProfessionalServiceRequestsResource, '/api/professional/service-requests', '/api/professional/service-requests/<int:request_id>')
    api.add_resource(UsersResource, '/api/users', '/api/users/<int:user_id>')
    api.add_resource(ServiceRequestsResource, '/api/service-requests', '/api/service-requests/<int:request_id>')
    api.add_resource(ProfessionalApprovalResource, '/api/professionals/<int:user_id>/approval')
    api.add_resource(BlockUserResource, '/api/users/<int:user_id>/block')
    api.add_resource(UnblockUserResource, '/api/users/<int:user_id>/unblock')
    api.add_resource(UserProfileResource, '/api/users/me/profile')
    api.add_resource(ExportServiceRequestsResource, '/api/export/request_details', '/api/export/status/<id>')


        
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
            "user": user.to_dict()
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
                "user": user.to_dict()
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
 
class LogoutResource(Resource):
    @auth_required('token')
    def post(self):
        logout_user()
        return {"message": "Logged out successfully"}, 200       

class ServiceResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('base_price', type=float)
        self.parser.add_argument('time_required', type=int)
        self.parser.add_argument('description', type=str)

    @cache.cached(timeout=300, key_prefix='services')
    def get(self, service_id=None):
        if service_id is None:
            services = Service.query.all()
            return jsonify([service.to_dict() for service in services])
        service = Service.query.get_or_404(service_id)
        return jsonify(service.to_dict())
        
    @auth_required('token')
    @roles_required('admin')
    def post(self):
        args = self.parser.parse_args()
        
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
        cache.delete('services')
        return jsonify(service.to_dict())
    
    
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
        cache.delete('services')
        return jsonify(service.to_dict())

    @auth_required('token')
    @roles_required('admin')
    def delete(self, service_id):
        service = Service.query.get_or_404(service_id)
        db.session.delete(service)
        db.session.commit()
        cache.delete('services')
        return jsonify({'message': 'Service deleted successfully'})

class CustomerServiceRequestsResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()   
        self.parser.add_argument('review', type=str)
        self.parser.add_argument('service_id', type=int)
        self.parser.add_argument('date_of_request', type=str)
    
    @auth_required('token')
    @roles_required('customer')
    def get(self, request_id=None):
        if request_id:
            request = ServiceRequest.query.get_or_404(request_id)
            return jsonify(request.to_dict())
        else:
            requests = ServiceRequest.query.filter_by(customer_id=current_user.id).all()
            return jsonify([req.to_dict() for req in requests])
        
    @auth_required('token')
    @roles_required('customer')
    def post(self):
        args = self.parser.parse_args()

        request = ServiceRequest(
            service_id=args['service_id'],
            customer_id=current_user.id,
            date_of_request=datetime.fromisoformat(args['date_of_request'])
        )
        
        db.session.add(request)
        db.session.commit()
        
        professionals = User.query.filter_by(service_id=request.service_id).all()
        for professional in professionals:
            send_email(professional.email, 'New Service Request', f"Hi {professional.username}, a new service request has been created.")
        
        return jsonify({
            'message': 'Service request created successfully'
        })
        
    @auth_required('token')
    @roles_required('customer')
    def put(self, request_id):
        args = self.parser.parse_args()
        request = ServiceRequest.query.get_or_404(request_id)
        
        if request.status == 'requested':
            if args['date_of_request']:
                request.date_of_request = datetime.fromisoformat(args['date_of_request'])
        else:
            if args['review']:
                request.review = args['review']
            if request.status == 'closed by professional':
                request.status = "closed"
            else:
                status_update.delay(f"Hi {request.professional.username}, customer has closed the service request.")
                send_email(request.professional.email, 'Service Request Closed', f"Hi {request.professional.username}, {request.customer.username} has closed the service request.")
                request.status = "closed by customer"
                request.date_of_completion = datetime.now()
                request.service.no_of_bookings += 1
            
        db.session.commit()
        return jsonify({'message': 'Service request updated successfully'})
    
    @auth_required('token')
    @roles_required('customer')
    def delete(self, request_id):
        request = ServiceRequest.query.get_or_404(request_id)
        db.session.delete(request)
        db.session.commit()
        return jsonify({'message': 'Service request deleted successfully'})

class ProfessionalServiceRequestsResource(Resource):
    @auth_required('token')
    @roles_required('service_professional')
    def get(self, request_id=None):
        if request_id:
            request = ServiceRequest.query.get_or_404(request_id)
            return jsonify(request.to_dict())
        requests = ServiceRequest.query.filter_by(professional_id=current_user.id).all()
        return jsonify([req.to_dict() for req in requests])
    
    @auth_required('token')
    @roles_required('service_professional')
    def post(self, request_id):
        request = ServiceRequest.query.get_or_404(request_id)
        request.professional_id = current_user.id
        request.status = 'assigned'
        db.session.commit()
        send_email(request.customer.email, 'Service Request Assigned', f"Hi {request.customer.username}, our service professional has been assigned to your service request.")
        return jsonify({'message': 'Service request assigned successfully'})
    
    @auth_required('token')
    @roles_required('service_professional')
    def put(self, request_id):
        request = ServiceRequest.query.get_or_404(request_id)
        if request.status == 'closed by customer':
            request.status = 'closed'
        else:
            request.status = 'closed by professional'
            status_update.delay(f"Hi {request.customer.username}, our service professional has closed the service request.")
            send_email(request.customer.email, 'Service Request Closed', f"Hi {request.customer.username}, our service professional has closed the service request.")
            request.date_of_completion = datetime.now()
            request.service.no_of_bookings += 1
        db.session.commit()
        return jsonify({'message': 'Service request updated successfully'})

class ServiceRequestsResource(Resource):
    @auth_required('token')
    @roles_accepted('admin', 'service_professional', 'customer')  
    def get(self, request_id=None):
        if request_id:
            request = ServiceRequest.query.get_or_404(request_id)
            return jsonify(request.to_dict())
        else:
            requests = ServiceRequest.query.all()
            return jsonify([req.to_dict() for req in requests])

class UsersResource(Resource):
    @auth_required('token')
    @roles_accepted('admin', 'customer')
    def get(self, user_id=None):
        try:
            if user_id:
                user = User.query.get_or_404(user_id)
                return jsonify(user.to_dict())
            else:
                users = User.query.all()
                return jsonify([user.to_dict() for user in users])
        except Exception as e:
            return {'message': str(e)}, 500

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
        send_email(user.email, 'Account Blocked', f"Hi {user.username}, your account has been blocked.")
        user.active = False
        user.status = 'blocked'
        db.session.commit()
        return {'message': 'User blocked successfully'}, 200

class UnblockUserResource(Resource):
    @auth_required('token')
    @roles_required('admin')
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        send_email(user.email, 'Account Unblocked', f"Hi {user.username}, your account has been unblocked.")
        user.active = True
        user.status = 'approved'
        db.session.commit()
        return {'message': 'User unblocked successfully'}, 200

class UserProfileResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=int)
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('address', type=str)
        self.parser.add_argument('about', type=str)
        self.parser.add_argument('experience_years', type=int)

    @auth_required('token')
    @roles_accepted('customer', 'service_professional')
    def put(self):
        args = self.parser.parse_args()
        
        try:
            user = User.query.get(args['id'])
            if args['username'] is not None:
                user.username = args['username']
            if args['address'] is not None:
                user.address = args['address']
            
            if 'service_professional' in [role.name for role in user.roles]:
                if args['about'] is not None:
                    user.about = args['about']
                if args['experience_years'] is not None:
                    user.experience_years = args['experience_years']
            
            db.session.commit()
            
            return jsonify({
                'message': 'Profile updated successfully',
                'user': user.to_dict()
            })
            
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error updating profile: {str(e)}'}, 500      
        
class ExportServiceRequestsResource(Resource):
    @auth_required('token')
    @roles_required('admin')
    def post(self):
        res = download_request_details.delay()
        return jsonify({'message': 'Sent to celery', 'id':res.id});
            
    # @auth_required('token')
    # @roles_required('admin')
    def get(self, id):
        res = AsyncResult(id)
        return send_from_directory('exports', res.result["filename"], as_attachment=True)


