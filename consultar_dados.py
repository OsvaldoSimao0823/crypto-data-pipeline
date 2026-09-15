import sqlite3
import pandas as pd

conexao = sqlite3.connect("data/crypto.db")

query = "SELECT * FROM precos_diarios LIMIT 5"

resultado = pd.read_sql(query, conexao)

print(resultado)

conexao.close()