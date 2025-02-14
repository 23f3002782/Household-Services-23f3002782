from flask import current_app as app, request, jsonify
from flask_security import auth_required, roles_required

@app.route('/admin')
@auth_required('token')
@roles_required('admin')
def admin():
    return "Admin Page"


@app.route('/customer')
@auth_required('token')
@roles_required('customer')
def customer():
    return "Customer Page"

@app.route('/service_professional')
@auth_required('token')
@roles_required('service_professional')
def service_professional():
    return "Service Professional Page"