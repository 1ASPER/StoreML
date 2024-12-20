import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET')
    
    def get_url_page(page: int) -> str:
        return f"https://bishkek.headhunter.kg/search/vacancy?resume=056a0788ff0e1708f00039ed1f4e4b64466153&page={page}&searchSessionId=5485e1b6-490f-4c2c-be2e-7a01be3e2f98"

    anti_scrapping_destroy = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }