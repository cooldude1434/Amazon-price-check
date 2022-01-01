import requests
from bs4 import BeautifulSoup
import lxml
import smtplib

BUY_PRICE = 200

my_email = "birthday.source@gmail.com"
password = "Birthday@123!"
receive_email = "birthday.destination@yahoo.com"


url = "https://www.amazon.com/Instant-Pot-Pressure-Steamer-Sterilizer/dp/B08PQ2KWHS/ref=dp_prsubs_2?pd_rd_i=B08PQ2KWHS&psc=1"
response = requests.get(
    url=url,
    headers={"Accept-Language":"en-US,en;q=0.9",
             "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
             ,"Accept-Encoding":"gzip, deflate",
             "Connection":"keep-alive"})
response.raise_for_status()

soup = BeautifulSoup(response.content,"lxml")
print(soup.prettify())

price = soup.find(name="span", class_="a-offscreen").get_text()
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)
print(price_as_float)
title = soup.find(id="productTitle").get_text().encode('utf-8').strip()
print(title)

if price_as_float < BUY_PRICE:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
         connection.starttls()   #*make it secure connection */
         connection.login(user=my_email,password=password)
         connection.sendmail(from_addr=my_email,
                         to_addrs=receive_email,
                         msg=f"Subject: Price Matches {title} \n\nThe price is {price_as_float}")
