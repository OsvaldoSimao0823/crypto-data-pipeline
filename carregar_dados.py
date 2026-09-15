import pandas as pd
import sqlite3

diario = pd.read_csv("data/dados_processados.csv")
conexao = sqlite3.connect("data/crypto.db")

diario.to_sql("precos_diarios", conexao, if_exists="replace", index=False)

conexao.close()

print("Dados carregados na base de dados com sucesso.")