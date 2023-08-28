import requests
from bs4 import BeautifulSoup
from pprint import pprint
import lxml
import smtplib

url = "https://www.amazon.co.uk/Redragon-M908-Precision-Programmable-Buttons/dp/B07FK9PKSM/ref=sr_1_1_sspa?crid=MO6GAHQA7O0U&keywords=redragon+mouse&qid=1693200534&s=computers&sprefix=redragon+mo%2Ccomputers%2C263&sr=1-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(url=url, headers=headers)
contents = response.content

soup = BeautifulSoup(contents, "lxml")

whole_price = float(soup.select_one(selector=".a-price-whole").getText())
fraction_price = float(soup.select_one(selector=".a-price-fraction").getText())/100
price = whole_price + fraction_price

target_price = 50
if price <= target_price:
    product_title = soup.select_one(selector="#productTitle").getText().strip()
    my_email = ""
    password = ""
    message = f"{product_title} is now below ${target_price}, selling at ${price}\n{url}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=f"Subject:Amazon Price Alert!\n\n{message}"
            .encode('utf-8')
        )
