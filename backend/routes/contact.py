from flask import Blueprint, request, jsonify
from models.database import db, Contact
from datetime import datetime
import re

contact_bp = Blueprint('contact', __name__)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    if not phone:
        return True
    pattern = r'^[\d\-\+\(\)\s]+$'
    return re.match(pattern, phone) is not None

@contact_bp.route('/contact', methods=['POST'])
def create_contact():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'リクエストデータがありません'
            }), 400
        
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'status': 'error',
                    'message': f'{field}は必須項目です'
                }), 400
        
        if not validate_email(data['email']):
            return jsonify({
                'status': 'error',
                'message': 'メールアドレスの形式が正しくありません'
            }), 400
        
        if 'phone' in data and data['phone'] and not validate_phone(data['phone']):
            return jsonify({
                'status': 'error',
                'message': '電話番号の形式が正しくありません'
            }), 400
        
        contact = Contact(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            message=data['message']
        )
        
        db.session.add(contact)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'お問い合わせを受け付けました'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': 'サーバーエラーが発生しました'
        }), 500