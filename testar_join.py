import sqlite3
import pandas as pd

conexao = sqlite3.connect("crypto.db")

query = """
SELECT dim_moeda.nome_completo, fato_precos.dia, fato_precos.preco_usd
FROM fato_precos
JOIN dim_moeda ON fato_precos.moeda_id = dim_moeda.moeda_id
LIMIT 5
"""

resultado = pd.read_sql(query, conexao)
print(resultado)

conexao.close()