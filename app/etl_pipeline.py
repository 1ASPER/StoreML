import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from utils.string_handlers import get_year_of_exp, parse_salary
from configuration.config import Config


# config.py

def extract(page_start = 1, page_end = 1) -> pd.DataFrame:

    df = pd.DataFrame(columns=['title', 'company', 'salary_from', 'salary_to', 'currency', 'is_net', 'year_experience', 'link'])

    for page in range(page_start, page_end + 1):

        url = Config.get_url_page(page)
        response = requests.get(url, headers=Config.anti_scrapping_destroy).text
        soup = BeautifulSoup(response, 'html.parser')

        cards = soup.find_all('div', class_='vacancy-card--n77Dj8TY8VIUF0yM font-inter')

        for card in cards:
            title = card.find('span', class_='magritte-text___tkzIl_4-3-14').text
            link_tag = card.find('a', class_='magritte-link___b4rEM_4-3-14 magritte-link_style_neutral___iqoW0_4-3-14 magritte-link_enable-visited___Biyib_4-3-14')
            link = link_tag['href']

            subtitle = card.find('span', class_='magritte-text___pbpft_3-0-20 magritte-text_style-primary___AQ7MW_3-0-20 magritte-text_typography-label-1-regular___pi3R-_3-0-20')
            handled_salary = parse_salary(subtitle)
            salary_from = handled_salary['salary_from']
            salary_to = handled_salary['salary_to']
            currency = handled_salary['currency']
            is_net = handled_salary['is_net']

            tags = card.find_all('div', class_='compensation-labels--vwum2s12fQUurc2J compensation-labels_magritte--pbBIkJ7Ww24ZILKz')

            year_experience = None

            for tag in tags:
                tag_solo = tag.find('div', class_='magritte-tag___WdGxk_3-0-23 magritte-tag_style-neutral___cw1Bt_3-0-23 magritte-tag_size-medium___Splpy_3-0-23')
                if tag_solo is None or 'опыт' not in tag_solo.text.lower():
                    continue
            
                year_experience = get_year_of_exp(tag_solo.text)

            company = card.find('a', class_='magritte-link___b4rEM_4-3-14 magritte-link_style_neutral___iqoW0_4-3-14')
            if (company is not None):
                company = company.text
            else:
                company = None

            if all([title, company, salary_from, salary_to, currency, is_net, year_experience, link]):
                df.loc[len(df)] = [title, company, salary_from, salary_to, currency, is_net, year_experience, link]

        print(f"Page {page} is done")
            
    return df

def transform(df: pd.DataFrame) -> pd.DataFrame:
    df['salary_from'] = df['salary_from'].astype(int)
    df['salary_to'] = df['salary_to'].astype(int)
    df['year_experience'] = df['year_experience'].astype(int)
    df['is_net'] = df['is_net'].astype(bool)
    return df

def load(df: pd.DataFrame, db_name: str, table_name: str) -> None:
    path = f"data/{db_name}"

    with sqlite3.connect(path) as conn:
        df.to_sql(table_name, conn, if_exists='replace', index=False)


def etl_pipeline(page_start: int, page_end: int, db_name: str, table_name: str) -> None:
    df = extract(page_start, page_end)
    df = transform(df)
    load(df, db_name, table_name)

if __name__ == '__main__':    
     etl_pipeline(1, 27, 'jobs.db', 'jobs')