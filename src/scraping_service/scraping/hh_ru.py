import json
import pandas as pd
import requests

from typing import Optional
from random import randint
from datetime import datetime

from sqlalchemy import create_engine

from .models import STG_HH_Vacancy

# используется для того, чтобы импортировать через * только эти функции
# __all__ = ('send_data_to_db')

# браузеры
headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]

# https://www.youtube.com/watch?v=_12U6Zfi5ik
proxies = {
    # 'https': 'http://proxy_ip:proxy_port'
    # 'https': f"http://{login}:{password}@proxy_ip:proxy_port"
}



def get_page_on_hh(page: int, vacancy: str, area:int, date_from = None, date_to= None)->Optional[str]:
    """Функция которая парсит первую страницу в опредленном городе и по опредленной вакансии
        Сайт с параметрами: https://github.com/hhru/api/blob/master/docs/vacancies.md#search
    Args:
        * page (int): порядковый номер странице в выдаче
        * vacancy (srt): название вакасии
        * area (int): город, по вакансиям которого осуществляется поиск
        * date_from (date): дата, которая ограничивает снизу диапазон дат публикации вакансий.
        * date_to (date): дата, которая ограничивает сверху диапазон дат публикации вакансий.

    Returns:
         str(): json c параметрами"""

    params = {
        'text': 'NAME:' + vacancy, 
        'area': area, 
        'page': page, # номер страницы
        'per_page': 100, 
        'date_from' : '2022-10-10', 
        'date_to' : '2022-10-22'
    }
    global proxies
    if proxies:
        proxies =proxies[randint(0, len(proxies) -1)]
    else:
        proxies = None

    req = requests.get(url = 'https://api.hh.ru/vacancies',
                        params = params,
                        headers=headers[randint(0, len(headers)-1)], 
                        proxies =proxies
                        ) 
    data = req.content.decode()
    req.close()
    return data


def modify_data(data):
    """Получение сырых данных и отправка их в stg слой базы данных

    Args:
        * data (str): _description_
        * schema (str): _description_
        * name (str): _description_
        * conn (str): движок базы данных
        Returns:
         str(): json c параметрами
    Returns:
        None
    """

    column_mapping ={'id': 'vacancy_id',
                    'premium': 'premium',
                    'name': 'name',
                    'has_test': 'has_test',
                    'response_letter_required': 'response_letter_required',
                    'published_at': 'published_at',
                    'created_at': 'created_at',
                    'archived': 'archived',
                    'alternate_url': 'alternate_url',
                    'area.id': 'area_id',
                    'area.name': 'area_name',
                    'salary.from': 'salary_from',
                    'salary.to': 'salary_to',
                    'salary.currency': 'salary_currency',
                    'salary.gross': 'salary_gross',
                    'type.id': 'type_id',
                    'type.name': 'type_name',
                    'employer.id': 'employer_id',
                    'employer.name': 'employer_name',
                    'employer.alternate_url': 'employer_alternate_url',
                    'employer.logo_urls.original': 'employer_logo_urls_original',
                    'employer.vacancies_url': 'employer_vacancies_url',
                    'employer.trusted': 'employer_trusted',
                    'snippet.requirement': 'snippet_requirement',
                    'snippet.responsibility': 'snippet_responsibility',
                    'schedule.id': 'schedule_id',
                    'schedule.name': 'schedule_name',
                    'address.city': 'address_city',
                    'address.street': 'address_street',
                    'address.building': 'address_building',
                    'address.lat': 'address_lat',
                    'address.lng': 'address_lng',
                    'address.raw': 'address_raw',
                    'address.metro.station_name': 'address_metro_station_name',
                    'address.metro.line_name': 'address_metro_line_name',
                    'address.metro.lat': 'address_metro_lat',
                    'address.metro.lng': 'address_metro_lng'}

    jsObj = json.loads(data)
    df = pd.json_normalize(jsObj['items'])
    truncated_df = pd.DataFrame()
    for old_name, new_name in column_mapping.items():
        try:
            truncated_df[new_name] = df[old_name]
        except:
            truncated_df[new_name] = None
    truncated_df = truncated_df.where(truncated_df.notnull(), None)
    truncated_df['created'] = datetime.now()
    return truncated_df

def send_data_to_db(page, vacancy, area):
    raw_data_from_hh = get_page_on_hh(page=page, vacancy=vacancy, area=area )
    df_from_hh = modify_data(raw_data_from_hh)
    engine = create_engine('sqlite:////Users/krivonos.no/Desktop/Иван/Scraping service/src/scraping_service/db.sqlite3')
    df_from_hh.to_sql(STG_HH_Vacancy._meta.db_table, if_exists='append', con=engine, index=False)