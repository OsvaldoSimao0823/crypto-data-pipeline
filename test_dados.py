import pandas as pd
import pytest

@pytest.fixture
def dados():
    return pd.read_csv("dags/dados_processados.csv")

def test_nao_esta_vazio(dados):
    assert len(dados) > 0

def test_precos_positivos(dados):
    assert (dados["preco_usd"] > 0).all()

def test_tem_as_duas_moedas(dados):
    moedas = set(dados["moeda"].unique())
    assert moedas == {"bitcoin", "ethereum"}

def test_sem_dias_duplicados(dados):
    duplicados = dados.duplicated(subset=["moeda", "dia"]).sum()
    assert duplicados == 0