from airflow import DAG  # type: ignore
from airflow.operators.python import PythonOperator  # type: ignore
from datetime import datetime
import requests
import pandas as pd
import sqlite3

def extrair():
    def buscar_historico(moeda):
        url = f"https://api.coingecko.com/api/v3/coins/{moeda}/market_chart"
        parametros = {"vs_currency": "usd", "days": "90"}
        resposta = requests.get(url, params=parametros)
        dados = resposta.json()
        precos = dados["prices"]
        tabela = pd.DataFrame(precos, columns=["timestamp", "preco_usd"])
        tabela["moeda"] = moeda
        return tabela

    bitcoin = buscar_historico("bitcoin")
    ethereum = buscar_historico("ethereum")
    tudo = pd.concat([bitcoin, ethereum])
    tudo.to_csv("/opt/airflow/dags/dados_brutos.csv", index=False)

def transformar():
    tabela = pd.read_csv("/opt/airflow/dags/dados_brutos.csv")
    tabela["data"] = pd.to_datetime(tabela["timestamp"], unit="ms")
    tabela["dia"] = tabela["data"].dt.date
    diario = tabela.groupby(["moeda", "dia"])["preco_usd"].mean().reset_index()
    diario.to_csv("/opt/airflow/dags/dados_processados.csv", index=False)

def carregar():
    diario = pd.read_csv("/opt/airflow/dags/dados_processados.csv")
    conexao = sqlite3.connect("/opt/airflow/dags/crypto.db")
    diario.to_sql("precos_diarios", conexao, if_exists="replace", index=False)
    conexao.close()

with DAG(
    dag_id="crypto_pipeline",
    start_date=datetime(2026, 9, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    task_extrair = PythonOperator(
        task_id="extrair",
        python_callable=extrair,
    )

    task_transformar = PythonOperator(
        task_id="transformar",
        python_callable=transformar,
    )

    task_carregar = PythonOperator(
        task_id="carregar",
        python_callable=carregar,
    )

    task_extrair >> task_transformar >> task_carregar