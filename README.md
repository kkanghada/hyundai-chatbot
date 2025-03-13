# 현대자동차 챗봇

현대자동차의 차량 정보와 자주 묻는 질문에 대답하는 챗봇 서비스입니다.

## 기능

1. 차량 정보 제공
   - 승용, SUV, MPV 등 차종별 모델 정보
   - 각 차량의 기본 정보

2. 자주 묻는 질문 (FAQ)
   - 영업시간 안내
   - 지점 위치 안내
   - 시승 관련 정보

3. 상담원 연결
   - 전화 상담 연결 안내

## 기술 스택

### 프론트엔드
- React
- Material-UI
- Axios

### 백엔드
- Python
- Flask
- Flask-CORS

## 실행 방법

### 백엔드 실행
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 프론트엔드 실행
```bash
cd frontend
npm install
npm start
```

## 배포 URL

- 프론트엔드: [https://hyundai-chatbot.vercel.app](https://hyundai-chatbot.vercel.app)
- 백엔드: [https://hyundai-chatbot-api.onrender.com](https://hyundai-chatbot-api.onrender.com)

## 개발자

이 프로젝트는 현대자동차 챗봇 서비스를 위해 개발되었습니다.

## 개발 환경
- Python 3.7+
- Flask 2.0.1
- requests 2.26.0

## 사용 방법
1. 카카오톡 플러스친구에서 "현대자동차" 검색
2. 친구 추가
3. 채팅방에서 기능 버튼을 선택하여 원하는 정보 확인

## 주의사항
- 이 챗봇은 데모 버전으로, 실제 현대자동차의 공식 챗봇이 아닙니다.
- 제공되는 정보는 예시이며, 실제 정보와 다를 수 있습니다. 