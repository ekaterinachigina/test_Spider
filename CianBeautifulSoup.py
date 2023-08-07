from bs4 import BeautifulSoup
import requests
import json


url = "https://kazan.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=1&region=4777&room1=1"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
names = soup.find_all("span", class_ = "_93444fe79c--color_primary_100--mNATk _93444fe79c--lineHeight_28px--whmWV _93444fe79c--fontWeight_bold--ePDnv _93444fe79c--fontSize_22px--viEqA _93444fe79c--display_block--pDAEx _93444fe79c--text--g9xAG _93444fe79c--text_letterSpacing__normal--xbqP6")
address = soup.find_all("div", class_ = "_93444fe79c--labels--L8WyJ")
price = soup.find_all("span", class_ = "_93444fe79c--color_black_100--kPHhJ _93444fe79c--lineHeight_28px--whmWV _93444fe79c--fontWeight_bold--ePDnv _93444fe79c--fontSize_22px--viEqA _93444fe79c--display_block--pDAEx _93444fe79c--text--g9xAG _93444fe79c--text_letterSpacing__normal--xbqP6")
link = soup.find_all("div", class_ = "_93444fe79c--container--kZeLu _93444fe79c--link--DqDOy")
page_number = soup.find_all("li", class_ = "_93444fe79c--page--tTWIr")
date = []
for name in names:
    a = name.find("span")
    name = a.text
    dictionary = {"name": name}
    date.append(dictionary)
for ad in address:
    a = ad.find_all("a")
    x = ""
    for i in a:
        x += i.text + " "
        print(x)
    dictionary = {"adres": x}
    date.append(dictionary)
for p in price:
    a = p.get_text()
    price = a
    dictionary = {"price": price}
    date.append(dictionary)
    print(dictionary)
# for l in link:
#     url = i.find("a", href = True)["href"]
#     dictionary = {"link": url}
#     date.append(dictionary)
#     print(url)
for page_num in page_number:
    if page_num.find("button"):
        page = page_num.find("button").find("span").get_text()
dictionary = {"page": page}
date.append(dictionary)
print(link)
    
json_string = json.dumps(date, ensure_ascii=False, separators = (",", ":"), indent = 4)
with open('json_data.json', 'w', encoding='utf-8') as file:
    file.write(json_string)
