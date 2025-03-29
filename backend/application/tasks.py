import csv
import datetime
from io import StringIO
import os
from application.models import *
from celery import shared_task # type: ignore 
from .mail import send_email
from .utils import google_space, format_report

@shared_task(ignore_result=False, name="download_request_details")
def download_request_details():
    try:
        # Create a string buffer to store CSV data
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        
        # Write headers
        headers = [
            'Request ID', 
            'Service ID', 
            'Service Name',
            'Customer ID', 
            'Customer Name',
            'Professional ID', 
            'Professional Name',
            'Date of Request', 
            'Date of Completion',
            'Status',
            'Review'
        ]
        writer.writerow(headers)
        
        requests = ServiceRequest.query.filter_by(status = 'closed').all()
        
        # Write data rows
        for req in requests:
            writer.writerow([
                req.id,
                req.service_id,
                req.service.name,
                req.customer_id,
                req.customer.username,
                req.professional_id,
                req.professional.username if req.professional else 'Not Assigned',
                req.date_of_request.strftime('%Y-%m-%d %H:%M:%S'),
                req.date_of_completion.strftime('%Y-%m-%d %H:%M:%S') if req.date_of_completion else 'Not Completed',
                req.status,
                req.review or 'No Review'
            ])
        
        # Create exports directory if it doesn't exist
        os.makedirs('exports', exist_ok=True)
        
        # Generate filename with timestamp
        filename = f'service_requests_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        filepath = os.path.join('exports', filename)
        
        # Write to file
        with open(filepath, 'w', newline='') as f:
            f.write(csv_buffer.getvalue())
            
        return {
            'status': 'success',
            'filename': filename,
            'message': f'Export completed successfully. File saved as {filename}'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Export failed: {str(e)}'
        }

@shared_task(ignore_result=False, name="remind_professional")
def remind_professional():
    requests = ServiceRequest.query.filter_by(status = 'assigned').all()
    for req in requests:
        text = f"Hi {req.professional.username}, please note that the service request for {req.customer.username} is still pending. Please check the app for more details."
        send_email(req.professional.email, subject='Service Request Reminder', message=text)
        google_space(text)
    return "Reminders sent to all professionals"

@shared_task(ignore_result=False, name="send_mails")
def monthly_report():
    customer_role = Role.query.filter_by(name = 'customer').first()
    users = customer_role.bearer
    for user in users:
        requests = ServiceRequest.query.filter_by(customer_id = user.id, status="closed").all()
        if len(requests) == 0:
            message = f"Hi {user.username}, you have not made any service requests this month. Please check the app for more details."
            send_email(user.email, subject='Monthly Report - Havenly', message=message)
        else:
            data = {
            'user': user.to_dict(),
            'requests': [req.to_dict() for req in requests]
            }
            message = format_report('templates/mail_details.html', data)
            send_email(user.email, subject='Monthly Report - Havenly', message=message)
    return "Sent emails to all users"

@shared_task(ignore_result = False, name = "status_update")
def status_update(text):
    google_space(text)
    return "Message sent successfully"