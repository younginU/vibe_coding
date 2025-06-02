import asyncio
import os
from dotenv import load_dotenv
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

async def test_email():
    try:
        # 환경 변수 로드
        load_dotenv()
        
        # 이메일 메시지 생성
        message = MIMEMultipart()
        message["From"] = os.getenv("SMTP_USERNAME")
        message["To"] = os.getenv("CONTACT_EMAIL")
        message["Subject"] = "테스트 이메일"

        body = "이것은 테스트 이메일입니다."
        message.attach(MIMEText(body, "plain"))

        # SMTP 클라이언트 생성
        smtp = aiosmtplib.SMTP(hostname=os.getenv("SMTP_SERVER"), port=465, use_tls=True)
        
        # 연결 및 로그인
        await smtp.connect()
        await smtp.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
        
        # 이메일 전송
        await smtp.send_message(message)
        
        # 연결 종료
        await smtp.quit()
        
        print("테스트 이메일이 성공적으로 전송되었습니다!")

    except Exception as e:
        print(f"에러 발생: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_email()) 