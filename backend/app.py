from flask import Flask, jsonify, request
import json
import random
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 모든 응답에 CORS 헤더 추가
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

# 차량 모델 데이터
car_models = {
    "승용": ["아반떼", "쏘나타", "그랜저", "아이오닉 5", "아이오닉 6"],
    "SUV": ["베뉴", "코나", "투싼", "싼타페", "팰리세이드"],
    "MPV": ["스타리아", "캐스퍼"],
    "상용": ["포터", "마이티", "쏠라티"],
    "제네시스": ["G70", "G80", "G90", "GV60", "GV70", "GV80"]
}

# 자주 묻는 질문 데이터
faq = {
    "보증 기간은 얼마인가요?": "현대자동차의 일반 보증 기간은 신차 출고일로부터 3년 또는 주행거리 60,000km 중 먼저 도래한 것을 적용합니다. 엔진 및 동력전달 계통 주요 부품은 5년 또는 100,000km입니다.",
    "정기점검은 언제 해야 하나요?": "일반적으로 신차는 1,000km 주행 후 첫 정기점검을 받고, 이후 매 10,000km 또는 6개월마다 정기점검을 받는 것이 좋습니다.",
    "타이어 공기압은 얼마로 유지해야 하나요?": "일반적으로 승용차는 32~35 PSI, SUV는 35~38 PSI를 권장합니다. 정확한 수치는 운전석 도어 프레임에 부착된 라벨을 참고하세요.",
    "엔진 오일은 얼마나 자주 교체해야 하나요?": "일반적으로 7,500~10,000km 주행 후 또는 6개월마다 교체를 권장합니다. 주행 조건에 따라 더 자주 교체가 필요할 수 있습니다.",
    "에어컨 필터는 얼마나 자주 교체해야 하나요?": "에어컨 필터(공조 필터)는 일반적으로 10,000~15,000km 주행 후 또는 1년마다 교체를 권장합니다."
}

# /keyboard 엔드포인트 정의
@app.route('/keyboard', methods=['GET'])
def keyboard():
    logger.info("GET /keyboard 요청 받음")
    response = jsonify({
        'type': 'buttons',
        'buttons': ['차량 정보', '자주 묻는 질문', '상담원 연결']
    })
    return add_cors_headers(response)

# /message 엔드포인트 정의
@app.route('/message', methods=['POST', 'OPTIONS'])
def message():
    # OPTIONS 요청 처리
    if request.method == 'OPTIONS':
        logger.info("OPTIONS /message 요청 받음")
        return '', 200
        
    # POST 요청 처리
    logger.info("POST /message 요청 받음")
    try:
        content = request.get_json()
        user_message = content.get('content', '')
        logger.info(f"사용자 메시지: {user_message}")

        response_message = "죄송합니다. 이해하지 못했습니다."
        response_buttons = ['차량 정보', '자주 묻는 질문', '상담원 연결']

        if user_message == "차량 정보":
            response_message = "어떤 차종에 관심이 있으신가요?"
            response_buttons = list(car_models.keys()) + ['처음으로']
        elif user_message in car_models:
            cars = car_models[user_message]
            response_message = f"{user_message} 차량 라인업입니다:\n" + "\n".join(cars)
            response_buttons = ['다른 차종 보기', '처음으로']
        elif user_message == "다른 차종 보기":
            response_message = "어떤 차종에 관심이 있으신가요?"
            response_buttons = list(car_models.keys()) + ['처음으로']
        elif user_message == "자주 묻는 질문":
            response_message = "어떤 내용이 궁금하신가요?"
            response_buttons = list(faq.keys()) + ['처음으로']
        elif user_message in faq:
            response_message = faq[user_message]
            response_buttons = ['다른 질문 보기', '처음으로']
        elif user_message == "다른 질문 보기":
            response_message = "어떤 내용이 궁금하신가요?"
            response_buttons = list(faq.keys()) + ['처음으로']
        elif user_message == "상담원 연결":
            response_message = "상담원과 연결을 원하시면 1588-5678로 전화주시기 바랍니다."
            response_buttons = ['처음으로']
        elif user_message == "처음으로":
            response_message = "무엇을 도와드릴까요?"
            response_buttons = ['차량 정보', '자주 묻는 질문', '상담원 연결']

        response_data = {
            'message': {
                'text': response_message
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': response_buttons
            }
        }

        logger.info(f"응답: {response_data}")
        return jsonify(response_data)
    except Exception as e:
        logger.error(f"오류 발생: {str(e)}")
        return jsonify({
            'message': {
                'text': '죄송합니다. 서버 오류가 발생했습니다.'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['차량 정보', '자주 묻는 질문', '상담원 연결']
            }
        })

# 루트 경로 추가
@app.route('/', methods=['GET'])
def index():
    logger.info("GET / 요청 받음")
    return jsonify({"status": "ok", "message": "현대자동차 챗봇 API 서버가 실행 중입니다."})

# 상태 확인 엔드포인트 추가
@app.route('/health', methods=['GET'])
def health():
    logger.info("GET /health 요청 받음")
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"서버 시작: 포트 {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
