from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import random
import logging

app = Flask(__name__)

# CORS 설정 (특정 도메인만 허용)
CORS(app, origins=["http://localhost:3000", "https://hyundai-chatbot.vercel.app"])

# /keyboard 엔드포인트 정의
@app.route('/keyboard', methods=['GET'])
def keyboard():
    return jsonify({
        'type': 'buttons',
        'buttons': ['차량 정보', '자주 묻는 질문', '상담원 연결']
    })

# /message 엔드포인트 정의
@app.route('/message', methods=['POST', 'OPTIONS'])
def message():
    # OPTIONS 요청 처리 (preflight 요청)
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        # CORS 헤더가 중복되게 추가되지 않도록 설정
        response.headers['Access-Control-Allow-Origin'] = 'https://hyundai-chatbot.vercel.app'  # 여기에 정확한 출처만 추가
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
    import os
    port = int(os.environ.get("PORT", 3001))
    app.run(host="0.0.0.0", port=port, debug=True)
