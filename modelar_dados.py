import pandas as pd
import sqlite3

diario = pd.read_csv("dados_processados.csv")

dim_moeda = pd.DataFrame({
    "moeda": ["bitcoin", "ethereum"],
    "nome_completo": ["Bitcoin", "Ethereum"],
    "categoria": ["moeda", "moeda"]
})
dim_moeda["moeda_id"] = dim_moeda.index + 1

fato_precos = diario.merge(dim_moeda[["moeda", "moeda_id"]], on="moeda")
fato_precos = fato_precos[["moeda_id", "dia", "preco_usd"]]

conexao = sqlite3.connect("crypto.db")
dim_moeda.to_sql("dim_moeda", conexao, if_exists="replace", index=False)
fato_precos.to_sql("fato_precos", conexao, if_exists="replace", index=False)
conexao.close()

print(dim_moeda)
print(fato_precos.head())
print("Modelo dimensional carregado com sucesso.")