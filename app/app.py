from flask import Flask, render_template, request
import sqlite3
import pandas as pd
from math import ceil
from .configuration.config import Config

def create_app():
    app = Flask(__name__)

    db_path = Config.db_path
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM jobs", conn)


    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/vacancies')
    def vacancies():
        experience_filter = request.args.get('experience', type=int)
        page = request.args.get('page', 1, type=int)
        per_page = 30

        filtered_df = df
        if experience_filter is not None:
            filtered_df = df[df['year_experience'] <= experience_filter]

        total_pages = ceil(len(filtered_df) / per_page)
        start = (page - 1) * per_page
        end = start + per_page

        vacancies = filtered_df.iloc[start:end].to_dict(orient='records')

        return render_template('vacancies.html', 
                           vacancies=vacancies, 
                           total_pages=total_pages, 
                           current_page=page, 
                           experience_filter=experience_filter)

    return app