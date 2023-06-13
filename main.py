import requests
import bs4
from fake_headers import Headers
from pprint import pprint
import json

headers = Headers(browser='Chrome', os='win')
headers_data = headers.generate()
response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=headers_data)
html_data = response.text
soup = bs4.BeautifulSoup(html_data, 'lxml')

tag_div_list_of_articles = soup.find('div', id='a11y-main-content')
tag_resume_title = soup.find_all("a", attrs={"class": "serp-item__title"})
professions = []
info = {}
for t in list(tag_resume_title):
    title = str(t.text)
    if "Django" in title or "Flask" in title:
        title = title
        href = t["href"]
        info["href"] = href
        tag_city = tag_div_list_of_articles.find_all(attrs={"data-qa": "vacancy-serp__vacancy-address"})
        cities = []
        for city in list(tag_city):
            city = city.text
            info["city"] = city
        tag_company = soup.find_all(attrs={"vacancy-serp-item__meta-info-company"})
        for company in list(tag_company):
            company = company.text
            info["company"] = company
        tag_salary = tag_div_list_of_articles.find_all(attrs={"data-qa": "vacancy-serp__vacancy-compensation"})
        for salary in list(tag_salary):
            salary = salary.text
            info["salary"] = salary
        professions.append(f'Vacancy: {title}, information: {info}')
        for item in professions:
            with open('info.txt', 'w', encoding="UTF-8") as f:
                json.dump(item, f)
