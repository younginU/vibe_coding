from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 환경 변수 로드
load_dotenv()

# 환경 변수 확인
required_env_vars = ["SMTP_SERVER", "SMTP_PORT", "SMTP_USERNAME", "SMTP_PASSWORD", "CONTACT_EMAIL"]
for var in required_env_vars:
    if not os.getenv(var):
        logger.error(f"Missing required environment variable: {var}")

app = FastAPI(title="Vibe Coding Contact API")

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://younginu.github.io",
        "http://localhost:3000",  # 로컬 개발용
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContactForm(BaseModel):
    name: str
    company: Optional[str] = None
    email: EmailStr
    inquiry_type: str
    message: str

@app.post("/api/contact")
async def send_contact_email(contact: ContactForm):
    try:
        # 환경 변수 로깅
        logger.info("Attempting to send email with following configuration:")
        logger.info(f"SMTP Server: {os.getenv('SMTP_SERVER')}")
        logger.info(f"From: {os.getenv('SMTP_USERNAME')}")
        logger.info(f"To: {os.getenv('CONTACT_EMAIL')}")

        # 이메일 메시지 생성
        message = MIMEMultipart()
        message["From"] = os.getenv("SMTP_USERNAME")
        message["To"] = os.getenv("CONTACT_EMAIL")
        message["Subject"] = f"[문의] {contact.inquiry_type} - {contact.name}"

        # 이메일 본문 생성
        body = f"""
        이름: {contact.name}
        회사: {contact.company or '미입력'}
        이메일: {contact.email}
        문의 유형: {contact.inquiry_type}
        
        메시지:
        {contact.message}
        """
        
        message.attach(MIMEText(body, "plain"))

        try:
            # SMTP 클라이언트 생성
            smtp = aiosmtplib.SMTP(hostname=os.getenv("SMTP_SERVER"), port=465, use_tls=True)
            
            # 연결 및 로그인
            await smtp.connect()
            await smtp.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
            
            # 이메일 전송
            await smtp.send_message(message)
            
            # 연결 종료
            await smtp.quit()
            
            logger.info("Email sent successfully")
            return {"status": "success", "message": "문의가 성공적으로 전송되었습니다."}

        except aiosmtplib.SMTPException as smtp_error:
            logger.error(f"SMTP Error: {str(smtp_error)}")
            raise HTTPException(
                status_code=500,
                detail=f"SMTP 오류: {str(smtp_error)}"
            )

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"이메일 전송 중 오류가 발생했습니다: {str(e)}"
        )

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"} 