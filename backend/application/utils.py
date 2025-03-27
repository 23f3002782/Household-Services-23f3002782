from json import dumps
from httplib2 import Http
from jinja2 import Template

def google_space(text):
    url = "https://chat.googleapis.com/v1/spaces/AAAA3UN0e88/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=ySuo4yY60LgYhS-dNCIa_3QzBl1IhXMOQA0VWjtoqLs"
    app_message = {"text": text}
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method="POST",
        headers=message_headers,
        body=dumps(app_message),
    )
    return {
        "status": "success"
    }
    
def format_report(html_template, data):
     with open(html_template) as file:
         template = Template(file.read())
         return template.render(data = data)