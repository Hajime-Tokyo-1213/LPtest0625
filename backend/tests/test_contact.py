import pytest
import json
from app import app, db
from models.database import Contact

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

def test_contact_success(client):
    test_data = {
        "name": "テスト太郎",
        "email": "test@example.com",
        "phone": "090-1234-5678",
        "message": "テストメッセージ"
    }
    
    response = client.post('/api/contact',
                         data=json.dumps(test_data),
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['message'] == 'お問い合わせを受け付けました'

def test_contact_missing_required_field(client):
    test_data = {
        "name": "テスト太郎",
        "email": "test@example.com"
    }
    
    response = client.post('/api/contact',
                         data=json.dumps(test_data),
                         content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert 'messageは必須項目です' in data['message']

def test_contact_invalid_email(client):
    test_data = {
        "name": "テスト太郎",
        "email": "invalid-email",
        "message": "テストメッセージ"
    }
    
    response = client.post('/api/contact',
                         data=json.dumps(test_data),
                         content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert 'メールアドレスの形式が正しくありません' in data['message']

def test_contact_invalid_phone(client):
    test_data = {
        "name": "テスト太郎",
        "email": "test@example.com",
        "phone": "invalid-phone-number",
        "message": "テストメッセージ"
    }
    
    response = client.post('/api/contact',
                         data=json.dumps(test_data),
                         content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert '電話番号の形式が正しくありません' in data['message']