from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from crawl_x_post import scrape_cz_binance

default_args = {
    'owner': 'airflow',
    'depend_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def save_data_to_file():
    data = scrape_cz_binance()
    with open('/tmp/cz_binance_posts.json', 'w', encoding='utf-8') as f:
        import json
        json.dump(data, f, ensure_ascii=False, indent=4)
with DAG('cz_binance_scraper', 
        default_args=default_args,
        schedule='@daily',
        catchup=False) as dag:
    task_scrape = PythonOperator(
        task_id='scrape_and_save',
        python_callable=save_data_to_file
    )
    task_scrape

