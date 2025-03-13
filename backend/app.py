from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)  # CORS 활성화

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
    """
    처음에 채팅방에 들어왔을 때 보여줄 버튼들을 설정합니다.
    """
    return jsonify({
        'type': 'buttons',
        'buttons': ['차량 정보', '자주 묻는 질문', '상담원 연결']
    })

@app.route('/message', methods=['POST'])
def message():
    """
    사용자가 보낸 메시지를 처리하고 응답을 생성합니다.
    """
    # 사용자가 보낸 메시지 받기
    content = request.get_json()
    user_message = content['content']

    # 응답 메시지 초기화
    response_message = "죄송합니다. 이해하지 못했습니다."
    response_buttons = ['차량 정보', '자주 묻는 질문', '상담원 연결']

    # 사용자 메시지에 따른 응답 처리
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

    # 응답 생성
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