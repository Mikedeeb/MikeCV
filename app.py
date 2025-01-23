from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///work.db'
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    email_subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "email_subject": self.email_subject,
            "message": self.message
        }


# Create Database Tables
with app.app_context():
    db.create_all()
    

@app.route("/")
def send_email():
    return render_template("index.html")


@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        name = request.json.get("name")
        email = request.json.get("email")
        phone_number = request.json.get("phone_number")
        email_subject = request.json.get("email_subject")
        message = request.json.get("message")
        
        if not name or not email or not phone_number or not message:
            return(
                 jsonify({"message": "You must include name, email, phone_number, and message"}), 400,
            )
        
        new_message = Contact(name=name, email=email, phone_number=phone_number, email_subject=email_subject, message=message)
        try:
            db.session.add(new_message)
            db.session.commit()
        except Exception as e:
            return jsonify({"message": str(e)}), 400
        
        return jsonify({"message": "Message received"}), 201


if __name__ == "__main__":
    app.run(debug=True)