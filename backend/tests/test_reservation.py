import pytest
import json
from datetime import datetime, timedelta
from app import app, db
from models.database import Reservation

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_reservation_success(client):
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    test_data = {
        "pet_type": "犬",
        "service_type": "トリミング",
        "desired_date": tomorrow,
        "desired_time": "14:00",
        "owner_name": "テスト太郎",
        "owner_email": "test@example.com",
        "owner_phone": "090-1234-5678"
    }
    
    response = client.post('/api/reservation',
                         data=json.dumps(test_data),
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['message'] == '予約を受け付けました'
    assert 'reservation_id' in data

def test_reservation_past_date(client):
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    test_data = {
        "pet_type": "犬",
        "service_type": "トリミング",
        "desired_date": yesterday,
        "desired_time": "14:00",
        "owner_name": "テスト太郎",
        "owner_email": "test@example.com"
    }
    
    response = client.post('/api/reservation',
                         data=json.dumps(test_data),
                         content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert '過去の日付は予約できません' in data['message']

def test_reservation_invalid_date_format(client):
    test_data = {
        "pet_type": "犬",
        "service_type": "トリミング",
        "desired_date": "2024/12/31",
        "desired_time": "14:00",
        "owner_name": "テスト太郎",
        "owner_email": "test@example.com"
    }
    
    response = client.post('/api/reservation',
                         data=json.dumps(test_data),
                         content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert '日付の形式が正しくありません' in data['message']

def test_reservation_invalid_time_format(client):
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    test_data = {
        "pet_type": "犬",
        "service_type": "トリミング",
        "desired_date": tomorrow,
        "desired_time": "14時00分",
        "owner_name": "テスト太郎",
        "owner_email": "test@example.com"
    }
    
    response = client.post('/api/reservation',
                         data=json.dumps(test_data),
                         content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert '時間の形式が正しくありません' in data['message']