from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

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

        # SMTP 서버 설정 및 이메일 전송
        await aiosmtplib.send(
            message,
            hostname=os.getenv("SMTP_SERVER"),
            port=int(os.getenv("SMTP_PORT", "587")),
            username=os.getenv("SMTP_USERNAME"),
            password=os.getenv("SMTP_PASSWORD"),
            use_tls=True
        )

        return {"status": "success", "message": "문의가 성공적으로 전송되었습니다."}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="이메일 전송 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        )

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"} 