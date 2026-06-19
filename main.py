import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from bs4 import BeautifulSoup

# ==============================
# 🔗 상품 리스트 (여기에 추가하면 됨)
# ==============================
PRODUCTS = [
    {
        "name": "앤 레이스팬츠 블랙",
        "url": "https://chouchoushasha.com/product/%EC%95%A4-%EB%A0%88%EC%9D%B4%EC%8A%A4%ED%8C%AC%EC%B8%A0-%EB%B8%94%EB%9E%99/4185/category/62/display/1/",
    },
    {
        "name": "레이스 체크 프릴탑 블루",
        "url": "https://chouchoushasha.com/product/%EB%A0%88%EC%9D%B4%EC%8A%A4-%EC%B2%B4%ED%81%AC-%ED%94%84%EB%A6%B4%ED%83%91-%EB%B8%94%EB%A3%A8/4399/category/53/display/1/",
    }
]

# ==============================
# 🔑 GitHub Secrets (환경 변수)
# ==============================
YOUR_EMAIL = os.getenv("YOUR_EMAIL")
YOUR_APP_PASSWORD = os.getenv("YOUR_APP_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

SMTP_SERVER = "smtp.naver.com"
SMTP_PORT = 465


# ==============================
# 🔍 세일 여부 체크
# ==============================
def check_sale(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    # 🔥 핵심: 취소선 가격 (정가) 있으면 세일
    if soup.select_one("del"):
        return True

    return False


# ==============================
# ✉️ 이메일 전송
# ==============================
def send_email(html_content):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🔥 세일 상품 발견!"
    msg["From"] = YOUR_EMAIL
    msg["To"] = TO_EMAIL

    html = f"""
    <html>
      <body>
        <h3>🛍️ 세일 상품 알림</h3>
        {html_content}
      </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(YOUR_EMAIL, YOUR_APP_PASSWORD)
        smtp.send_message(msg)


# ==============================
# 🚀 메인 실행
# ==============================
def main():
    sale_items = []

    for p in PRODUCTS:
        try:
            on_sale = check_sale(p["url"])

            if on_sale:
                sale_items.append(
                    f"""
                    <div style="margin-bottom:15px;">
                        <b>🔥 세일 중!</b><br>
                        {p['name']}<br>
                        <a href="{p['url']}">상품 보러가기</a>
                    </div>
                    """
                )

        except Exception as e:
            print(f"에러 발생: {p['name']} / {e}")

    # 🔥 세일 상품 있을 때만 메일 발송
    if sale_items:
        send_email("".join(sale_items))
        print("✅ 세일 알림 메일 발송 완료")
    else:
        print("세일 상품 없음")


# ==============================
# ▶ 실행
# ==============================
if __name__ == "__main__":
    main()
