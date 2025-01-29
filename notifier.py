from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime
import pandas as pd
import mysql.connector

def extracting(**kwargs):
    file = '/home/ana/airflow/dags/vendas.csv'
    df = pd.read_csv(file, encoding='utf-8')

    #Convertendo o df para um objeto serializável
    df_serial = df.to_dict()
    kwargs['ti'].xcom_push(key='df', value=df_serial)

def transforming(**kwargs):
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

def loading(**kwargs):
    data = kwargs['ti'].xcom_pull(task_ids='Transform', key = 'df')
    df = pd.DataFrame(data)

    bd = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '16092005Dn!',
        database = 'vendas_dataco'
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
    end = DummyOperator(task_id='End')

start >> extract >> transform >> load >> end

