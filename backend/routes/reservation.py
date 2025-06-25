from flask import Blueprint, request, jsonify
from models.database import db, Reservation
from datetime import datetime, date, time
import re

reservation_bp = Blueprint('reservation', __name__)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    if not phone:
        return True
    pattern = r'^[\d\-\+\(\)\s]+$'
    return re.match(pattern, phone) is not None

@reservation_bp.route('/reservation', methods=['POST'])
def create_reservation():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'リクエストデータがありません'
            }), 400
        
        required_fields = ['pet_type', 'service_type', 'desired_date', 'desired_time', 
                         'owner_name', 'owner_email']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'status': 'error',
                    'message': f'{field}は必須項目です'
                }), 400
        
        if not validate_email(data['owner_email']):
            return jsonify({
                'status': 'error',
                'message': 'メールアドレスの形式が正しくありません'
            }), 400
        
        if 'owner_phone' in data and data['owner_phone'] and not validate_phone(data['owner_phone']):
            return jsonify({
                'status': 'error',
                'message': '電話番号の形式が正しくありません'
            }), 400
        
        try:
            desired_date = datetime.strptime(data['desired_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': '日付の形式が正しくありません (YYYY-MM-DD)'
            }), 400
        
        try:
            desired_time = datetime.strptime(data['desired_time'], '%H:%M').time()
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': '時間の形式が正しくありません (HH:MM)'
            }), 400
        
        if desired_date < date.today():
            return jsonify({
                'status': 'error',
                'message': '過去の日付は予約できません'
            }), 400
        
        existing_reservation = Reservation.query.filter_by(
            desired_date=desired_date,
            desired_time=desired_time,
            status='pending'
        ).first()
        
        if existing_reservation:
            return jsonify({
                'status': 'error',
                'code': 409,
                'message': 'その時間帯は既に予約が入っています'
            }), 409
        
        reservation = Reservation(
            pet_type=data['pet_type'],
            service_type=data['service_type'],
            desired_date=desired_date,
            desired_time=desired_time,
            owner_name=data['owner_name'],
            owner_email=data['owner_email'],
            owner_phone=data.get('owner_phone', ''),
            status='pending'
        )
        
        db.session.add(reservation)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '予約を受け付けました',
            'reservation_id': reservation.id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': 'サーバーエラーが発生しました'
        }), 500