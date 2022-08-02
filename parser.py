import requests
from bs4 import BeautifulSoup


headers = {
    'Host': 'hh.ru',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Version/14.1.2 Safari/605.1.15',
    'Accept': '*/*'
    }
session = requests.Session()


def extract_max_page(url):
    hh_request = session.get(url, headers=headers)
    hh_soup = BeautifulSoup(hh_request.text, 'html.parser')
    pages = []
    pagi = hh_soup.find_all('span', {'class': 'pager-item-not-in-short-range'})
    for page in pagi:
        pages.append(int(page.find('a').text))
        print(pages)
    return pages[-1]


def extract_job(html):
    title = html.find('a').text
    link = html.find('a')['href']
    company = html.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).text
    company = company.strip()
    location = html.find('span', {'data-qa': 'vacancy-serp__vacancy-address'}).text
    location = location.partition(',')[0]
    date = html.find('span', {'class': 'vacancy-serp-item__publication-date '
                                       'vacancy-serp-item__publication-date_short'}).text
    return {'title': title, 'company': company, 'location': location, 'date': date, 'link': link}


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f'hh парсинг страницы {page}')
        result = session.get(f'{url}&page={page}', headers=headers)
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('div', {'class': 'vacancy-serp-item'})
        for res in results:
            job = extract_job(res)
            jobs.append(job)
    return jobs


def get_job(keyword):
    url = f'https://hh.ru/search/vacancy?st=searchVacancy&text={keyword}&items_on_page=100'
    max_page = extract_max_page(url)
    jobs = extract_jobs(max_page, url)
    return jobs


get_job('java')
