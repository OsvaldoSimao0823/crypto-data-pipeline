import requests
import pandas as pd
def buscar_historico(moeda):
    url = f"https://api.coingecko.com/api/v3/coins/{moeda}/market_chart"
    parametros = {
        "vs_currency": "usd",
        "days": "90"
    }
    resposta = requests.get(url, params=parametros)
    dados = resposta.json()
    precos = dados["prices"]

    tabela = pd.DataFrame(precos, columns=["timestamp", "preco_usd"])
    tabela["moeda"] = moeda
    return tabela

bitcoin = buscar_historico("bitcoin")
ethereum = buscar_historico("ethereum")

tudo = pd.concat([bitcoin, ethereum])

print(tudo.shape)
print(tudo.head())
print(tudo.tail())

tudo.to_csv("dados_brutos.csv", index=False)
print("Guardado com sucesso.")