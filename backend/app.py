from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import random

app = Flask(__name__)
# 특정 프론트엔드 도메인만 허용하는 CORS 설정
CORS(app)  # 모든 도메인 허용
# CORS(app, resources={r"/*": {"origins": "https://hyundai-chatbot.vercel.app"}})

# after_request 핸들러 (모든 응답에 CORS 헤더 추가)
@app.after_request
def after_request(response):
    logging.info("after_request 호출됨")
    response.headers.add('Access-Control-Allow-Origin', 'https://hyundai-chatbot.vercel.app')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

# 현대자동차 모델 리스트
car_models = {
    "승용": ["아반떼", "쏘나타", "그랜저", "아이오닉5", "아이오닉6"],
    "SUV": ["베뉴", "코나", "투싼", "싼타페", "팰리세이드"],
    "MPV": ["스타리아", "캐스퍼"],
}

# 자주 묻는 질문과 답변
faq = {
    "영업시간": "평일: 09:00-18:00\n토요일: 09:00-15:00\n일요일/공휴일: 휴무",
    "위치": "가까운 현대자동차 지점은 홈페이지(https://www.hyundai.com)에서 확인하실 수 있습니다.",
    "시승": "시승 예약은 현대자동차 홈페이지 또는 가까운 지점에서 가능합니다.",
}

@app.route('/keyboard', methods=['GET'])
def keyboard():
    return jsonify({
        'type': 'buttons',
        'buttons': ['차량 정보', '자주 묻는 질문', '상담원 연결']
    })

# /message 엔드포인트에 POST와 OPTIONS 메소드를 모두 허용
@app.route('/message', methods=['POST', 'OPTIONS'])
def message():
    # OPTIONS (preflight) 요청 처리
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = 'https://hyundai-chatbot.vercel.app'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
        return response

    # POST 요청 처리
    content = request.get_json()
    user_message = content.get('content', '')

    response_message = "죄송합니다. 이해하지 못했습니다."
    response_buttons = ['차량 정보', '자주 묻는 질문', '상담원 연결']

    if user_message == "차량 정보":
        response_message = "어떤 차종에 관심이 있으신가요?"
        response_buttons = list(car_models.keys()) + ['처음으로']
    elif user_message in car_models:
        cars = car_models[user_message]
        response_message = f"{user_message} 차량 라인업입니다:\n" + "\n".join(cars)
        response_buttons = ['다른 차종 보기', '처음으로']
    elif user_message == "자주 묻는 질문":
        response_message = "어떤 내용이 궁금하신가요?"
        response_buttons = list(faq.keys()) + ['처음으로']
    elif user_message in faq:
        response_message = faq[user_message]
        response_buttons = ['다른 질문 보기', '처음으로']
    elif user_message == "상담원 연결":
        response_message = "상담원과 연결을 원하시면 1588-5678로 전화주시기 바랍니다."
        response_buttons = ['처음으로']
    elif user_message == "처음으로":
        response_message = "무엇을 도와드릴까요?"
        response_buttons = ['차량 정보', '자주 묻는 질문', '상담원 연결']

    response = {
        'message': {
            'text': response_message
        },
        'keyboard': {
            'type': 'buttons',
            'buttons': response_buttons
        }
    }
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
