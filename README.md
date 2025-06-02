# Vibe Coding Website

AI 시대의 개발 혁신을 선도하는 Vibe Coding의 공식 웹사이트입니다.

## 프로젝트 구조
```
vibe_01/
├── about/          # 회사 소개 페이지
├── assets/         # 정적 자원 (CSS, JS, 이미지)
├── blog/           # 블로그 포스트
├── docs/          # 문서
├── api/           # 백엔드 API
└── index.html     # 메인 페이지
```

## 백엔드 API 설정

1. Python 가상환경 생성 및 활성화:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. 의존성 설치:
```bash
uv pip install -r requirements.txt
```

3. 환경 변수 설정:
`api/.env` 파일을 생성하고 다음 변수들을 설정하세요:
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
CONTACT_EMAIL=contact@your-domain.com
```

4. API 서버 실행:
```bash
uvicorn api.main:app --reload
```

## API 엔드포인트

- `POST /api/contact`: 문의 이메일 전송
- `GET /api/health`: 서버 상태 확인

## 보안 설정

1. Gmail을 SMTP 서버로 사용하는 경우:
   - Google 계정의 2단계 인증을 활성화
   - 앱 비밀번호를 생성하여 `SMTP_PASSWORD`로 사용

2. 프로덕션 환경에서는:
   - CORS 설정을 실제 도메인으로 제한
   - 환경 변수를 안전하게 관리
   - HTTPS 사용 필수
