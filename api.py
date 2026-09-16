from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI(title="Previsão de Direção de Criptomoedas")

modelo = joblib.load("data/modelo_lgbm.pkl")

@app.get("/")
def raiz():
    return {"mensagem": "API de previsão de direção de preço de criptomoedas"}

@app.post("/prever")
def prever(retorno_1d: float, retorno_medio_3d: float, retorno_medio_7d: float,
           volatilidade_7d: float, retorno_bitcoin: float, retorno_ethereum: float):

    entrada = pd.DataFrame([{
        "retorno_1d": retorno_1d,
        "retorno_medio_3d": retorno_medio_3d,
        "retorno_medio_7d": retorno_medio_7d,
        "volatilidade_7d": volatilidade_7d,
        "retorno_bitcoin": retorno_bitcoin,
        "retorno_ethereum": retorno_ethereum,
    }])

    previsao = modelo.predict(entrada)[0]
    probabilidade = modelo.predict_proba(entrada)[0].max()

    return {
        "previsao": "sobe" if previsao == 1 else "desce",
        "confianca": round(float(probabilidade), 3),
        "aviso": "Modelo com sinal preditivo fraco (ver README) — usar apenas como demonstração técnica, não como conselho financeiro."
    }