from flask import current_app as app, request, jsonify
from flask_security import auth_required, roles_required

@app.route('/admin')
@auth_required('token')
@roles_required('admin')
def admin():
    return "Admin Page"