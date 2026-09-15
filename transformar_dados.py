import pandas as pd


tabela = pd.read_csv("data/dados_brutos.csv")

tabela["data"] = pd.to_datetime(tabela["timestamp"], unit="ms")

print(tabela.head())
print(tabela.dtypes)

tabela["dia"] = tabela["data"].dt.date

diario = tabela.groupby(["moeda", "dia"])["preco_usd"].mean().reset_index()

print(diario.head())
print(diario.shape)

print(diario.columns)
print(diario.shape)

diario.to_csv("data/dados_processados.csv", index=False)
print("Dados processados guardados com sucesso.")