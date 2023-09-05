from flask import Flask
from flask_mail import Mail, Message
from flask_restx import Api, Resource, fields
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
api = Api(app, version='1.0', title='Event API', description='API for managing events')

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Update with your email provider's SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'dandekarakshy13@gmail.com'
app.config['MAIL_PASSWORD'] = '*********'

mail = Mail(app)

event_model = api.model('Event', {
    'event_name': fields.String(required=True, description='Event name'),
    'event_date': fields.String(required=True, description='Event date (YYYY-MM-DD)'),
})

def send_email_wishes(events, mail, subject):
    try:
        subject = subject
        recipient = "dandekarakshay51@gmail.com"  # Replace with the recipient's email address

        msg = Message(subject=subject, recipients=[recipient])
        msg.body = "\n".join([f"Event: {event['event_name']}, Date: {event['event_date']}" for event in events])

        mail.send(msg)

        return "Email sent successfully!"
    except Exception as e:
        return f"Error sending email: {str(e)}"

def fetch_data_from_source_system():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["Events"]
        collection = db["events_KDB"]
        data = list(collection.find({}))
        today = datetime.now().date()
        today_events = [event for event in data if datetime.strptime(event['event_date'], '%Y-%m-%d').date() == today]

        return today_events
    except Exception as error:
        # Handle exceptions here if needed
        raise error

@api.route('/send_email')
class SendEmailResource(Resource):
    @api.doc('send_email')
    def get(self):
        try:
            events = fetch_data_from_source_system()
            if events:
                subject = [event['event_name'] for event in events]
                response = send_email_wishes(events, mail, subject)
                return {'message': response}
            else:
                return {'message': "No events found for today."}
        except Exception as e:
            return {'error': str(e)}

if __name__ == '__main__':
    app.run(debug=True, port=5000)
