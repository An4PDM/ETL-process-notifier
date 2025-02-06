from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime
import pandas as pd
import mysql.connector
from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER, SLACK_TOKEN, SLACK_CHANNEL, EMAIL

def extracting(**kwargs):
    try:
        file = '/home/ana/airflow/dags/vendas.csv'
        df = pd.read_csv(file, encoding='utf-8')

        #Convertendo o df para um objeto serializável
        df_serial = df.to_dict()
        kwargs['ti'].xcom_push(key='df', value=df_serial)

    except Exception as e:
        raise ValueError(f'Error on extracting data: {e}')

def transforming(**kwargs):
    try:
        data = kwargs['ti'].xcom_pull(task_ids='Extract', key ='df')
        
        #Convertendo para DataFrame para realizar transformações
        df = pd.DataFrame(data)
        
        #Soma dos produtos em uma única linha para cada
        df_grouped = df.groupby('produto').agg({
            'quantidade': 'sum',
            'preco_unitario': 'first'
        } ).reset_index() # Reseta os índices para a nova tabela

        #Adiciona comissão
        df_grouped['Comissão'] = df_grouped['preco_unitario'] * 0.10

        # Conversão para serializável e push
        df_serial = df_grouped.to_dict()
        kwargs['ti'].xcom_push(key='df',value=df_serial)

    except Exception as e:
        raise ValueError(f'Error on transforming data: {e}')

def loading(**kwargs):
    try:
        data = kwargs['ti'].xcom_pull(task_ids='Transform', key = 'df')
        df = pd.DataFrame(data)

        bd = mysql.connector.connect(
            host = DB_HOST,
            user = DB_USER,
            password = DB_PASSWORD,
            database = DB_NAME
        )
        cursor = bd.cursor()
        
        query = '''INSERT INTO vendas (produto,quantidade,preco_unitario,Comissão)
                    VALUES (%s,%s,%s,%s);'''
        
        # Iterando no DataFrame para inserção no BD
        for _, row in df.iterrows():
            cursor.execute(query,(row['produto'],
                            row['quantidade'],
                            row['preco_unitario'],
                            row['Comissão']))
        bd.commit()
        cursor.close()
        bd.close()

    except Exception as e:
        raise ValueError(f'Error on loading data: {e}')
        
def slack_connection(token,channel,message):
    client = WebClient(token=token)

    try:
        response = client.chat_postMessage(
            channel=channel,
            text=message
        )
    except SlackApiError as e:
        print(f"Error in connection with Slack: {e.response['error']}")

def success_notif(context):
    message = 'The ETL process was completed successfully.'
    slack_connection(SLACK_TOKEN,SLACK_CHANNEL,message)

def fail_notif(context):
    message = 'The ETL process failed. Check the LOGs for more information.'
    slack_connection(SLACK_TOKEN,SLACK_CHANNEL,message)

with DAG (
    dag_id='Notifier',
    schedule_interval='@daily',
    start_date=datetime(2025,1,20),
    catchup=True
) as dag:
    
    start = DummyOperator(task_id='Start')
    extract = PythonOperator(task_id='Extract',python_callable=extracting)
    transform = PythonOperator(task_id='Transform',python_callable=transforming)
    load = PythonOperator(task_id='Load',python_callable=loading)
    success = EmailOperator(task_id='Success', 
                            to=EMAIL,
                            subject='Successful ETL process',
                            html_content='The ETL process was completed successfully.',
                            trigger_rule='all_success')
    fail = EmailOperator(task_id='Fail', 
                            to=EMAIL,
                            subject='Failed ETL process',
                            html_content='The ETL process failed. Check the LOGs for more information.',
                            trigger_rule='one_failed')
    end = DummyOperator(task_id='End')

start >> extract >> transform >> load >> [success, fail] >> end


