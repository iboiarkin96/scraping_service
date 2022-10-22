# порядок очень важен 
# setdefault DJANGO_SETTINGS_MODULE must be moved to the top of the script file.

import json
import os
import sys
import pandas as pd

from sqlalchemy import create_engine

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()

from scraping.hh_ru import *
from scraping.models import STG_HH_Vacancy

# сделать это в многопоточном режиме
raw_data_from_hh = get_page_on_hh(page=0, vacancy='Аналитик', area=1, )
df_from_hh = send_hh_data_to_db(raw_data_from_hh)
engine = create_engine('sqlite:////Users/krivonos.no/Desktop/Иван/Scraping service/src/scraping_service/db.sqlite3')
df_from_hh.to_sql(STG_HH_Vacancy._meta.db_table, if_exists='append', con=engine, index=False)

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
