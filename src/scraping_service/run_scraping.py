# порядок очень важен 
# setdefault DJANGO_SETTINGS_MODULE must be moved to the top of the script file.
import asyncio
import os
import sys
import pandas as pd


proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()

from scraping.hh_ru import *
from scraping.models import STG_HH_Vacancy, Error, URL
from django.contrib.auth import get_user_model
from typing import Dict, List, Set, Tuple

User = get_user_model()

def get_user_settings():
    """Получаем настройки пользователей, которые 
    дали согласие на отправку сообщений на почту.
    Парсинг происодит ТОЛЬКО по этим значениям

    Returns:
        Set(Tuple): множество пар город - язык программирования для каждого из пользователей, кто просил отсылать на почту
    """
    qs = User.objects.filter(send_email = True).values()
    settings_lists = set( (q['city_id'], q['language_id']) for q in qs )
    return settings_lists

def get_urls(_settings) -> List:
    """Отбираем те ссылки URL из на на которые нужно сходить 

    Args:
        _settings (Set): множество пар (город - язык программирования)

    Returns:
        List: _description_
    """
    # все url, которые есть в бд
    qs = URL.objects.all().values()
    url_dict : Dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls: List = []
    # отбирает только те пары (город- язык программирования)
    # которые мы умеем парсить
    for pair in _settings:
        if pair in url_dict:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            url_data = url_dict.get(pair)
            if url_data:
                tmp['url_data'] = url_dict.get(pair)
                urls.append(tmp)
    return urls  

ALL_ACTUAL_CLIENTS = get_user_settings()
search_data = get_urls(_settings = ALL_ACTUAL_CLIENTS)


async def main_hh(value):
    page,vacancy, area =  value
    await loop.run_in_executor(None, send_data_to_db, page, vacancy, area)

import time
start = time.time()
for row in search_data:
    urls = row['url_data']
    if urls.get('hh_ru', None) is not None:
        city = row['city']
        language = row['language']
        # перенести блок маппинга на уровень БД
        if city == 2:
            area = 1
        if language == 1:
            name_lg = 'Python'
            vacancy = 'Программист ' + name_lg

        loop = asyncio.get_event_loop()
        tmp_tasks = [(i, vacancy, area)  for i in  range(10)]
        if tmp_tasks:
            tasks = asyncio.wait([loop.create_task(main_hh(f)) for f in tmp_tasks])
            loop.run_until_complete(tasks)
            loop.close()
print(time.time() - start)


#  выделить отдельную схему 
#  сделать линк по  языку и городу
# перейди на посгрес
# понять как работать с добавлением записей, которые уже есть в таблице (в  stg слое): как вариант время добавления 


# insert into Vacancy(url, title, company, description, date_create, city_id, language_id)
# select alternate_url as url
# 	, name as title
# 	, employer_name as company
# 	, snippet_requirement as description
# 	, created_at as date_create
# 	, 1 as city_id
# 	,  1 as language_id
# FROM STG_Vacancy_hh_ru svhr on conflict
