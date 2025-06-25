from flask import Flask, request, jsonify, Response
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

from models.database import db, Contact, Reservation
db.init_app(app)
from routes.contact import contact_bp
from routes.reservation import reservation_bp

app.register_blueprint(contact_bp, url_prefix='/api')
app.register_blueprint(reservation_bp, url_prefix='/api')

@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'status': 'error',
        'code': 400,
        'message': 'バリデーションエラー'
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'code': 404,
        'message': 'リソースが見つかりません'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'code': 500,
        'message': 'サーバー内部エラー'
    }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)