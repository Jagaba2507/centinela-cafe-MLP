"""Descarga las fuentes del Proyecto Centinela del Café desde su productor primario.

- RoCoLe v2 (Mendeley Data, DOI 10.17632/c5yvn32dzg.2, CC BY 4.0)
- NASA POWER, clima mensual del sitio de colecta (CIIDEA, Calceta, Manabí, Ecuador)

Uso: python scripts/descargar_datos.py
Los archivos quedan en datos/, carpeta excluida del repositorio por .gitignore.
"""
import hashlib
import os
import zipfile

import pandas as pd
import requests

DATA_DIR = "datos"
URL_ROCOLE = "https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com/c5yvn32dzg-2.zip"
URL_POWER = "https://power.larc.nasa.gov/api/temporal/monthly/point"
LAT, LON = -0.834206, -80.177159


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def descargar_rocole():
    destino = os.path.join(DATA_DIR, "c5yvn32dzg-2.zip")
    if not os.path.exists(destino):
        r = requests.get(URL_ROCOLE, timeout=300)
        r.raise_for_status()
        with open(destino, "wb") as f:
            f.write(r.content)
    with zipfile.ZipFile(destino) as z:
        z.extractall(os.path.join(DATA_DIR, "rocole"))
    print("RoCoLe:", destino, "SHA-256:", sha256(destino))


def descargar_power(inicio=2018, fin=2019):
    params = dict(parameters="T2M,RH2M,PRECTOTCORR", community="AG",
                  latitude=LAT, longitude=LON, start=inicio, end=fin, format="JSON")
    r = requests.get(URL_POWER, params=params, timeout=120)
    r.raise_for_status()
    clima = pd.DataFrame(r.json()["properties"]["parameter"]).reset_index()
    clima = clima.rename(columns={"index": "periodo"})
    clima = clima[~clima["periodo"].str.endswith("13")]
    destino = os.path.join(DATA_DIR, "nasa_power_ciidea_mensual.csv")
    clima.to_csv(destino, index=False)
    print("NASA POWER:", destino, "SHA-256:", sha256(destino))


if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    descargar_rocole()
    descargar_power()
