"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import pandas as pd
from textblob import TextBlob
from datetime import datetime
import os


def limp_str_simp(df, col):
    df[col] = df[col].str.lower()
    return df

def limp_str_comp(df, col):

    df['raw_keyword'] = df[col].copy()

    df['raw_keyword'] = (
        df['raw_keyword']
        .str.lower()
        .str.replace(r'[-._]', ' ', regex=True)
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
    )

    df['raw_keyword'] = df['raw_keyword'].str.replace(r'\bde\b', '', regex=True)
    df['raw_keyword'] = df['raw_keyword'].str.replace(r'\s+', ' ', regex=True).str.strip()

    df['key'] = df['raw_keyword'].apply(
        lambda x: " ".join(sorted([word.lemmatize("v") for word in TextBlob(x).words]))
    )

    grupos = df.groupby("key")["raw_keyword"].apply(list).reset_index()
    mapping = {}
    for _, row in grupos.iterrows():
        for palabra in row['raw_keyword']:
            mapping[palabra] = row['raw_keyword'][0]

    df[col] = df['raw_keyword'].map(mapping)
    df.drop(columns=['raw_keyword', 'key'], inplace=True)

    return df

def parse_fecha(fecha):
    formatos = [
        '%d/%m/%Y',
        '%Y-%m-%d',
        '%d-%m-%Y',
        '%Y/%m/%d',
        '%d %b %Y',
        '%d %B %Y',
        '%Y.%m.%d', 
    ]
    
    for fmt in formatos:
        try:
            return datetime.strptime(fecha, fmt)
        except:
            continue
    return pd.NaT

def limpiar_fecha(df, col):
    df[col] = df[col].astype(str).str.strip()
    df[col] = df[col].apply(parse_fecha)
    return df

def limpiar_monto(df, col):
    df[col] = (
        df[col].astype(str)
        .str.replace(r'[^0-9.,]', '', regex=True)  # conserva números, comas y puntos
        .str.replace(',', '')                     # elimina las comas (miles)
        .str.replace(r'\.00$', '', regex=True)    # elimina .00 si está al final
        .astype(float)
        .astype(int)
    )
    return df

def pregunta_01():

    os.makedirs('files/output', exist_ok=True)

    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    df = pd.read_csv('files/input/solicitudes_de_credito.csv', sep=';')

    df.drop(['Unnamed: 0'], axis=1, inplace=True)
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    limp_str_simp(df, 'sexo')
    limp_str_simp(df, 'tipo_de_emprendimiento')
    limp_str_comp(df, 'idea_negocio')

    df['barrio'] = df['barrio'].str.lower().replace(['-', '_'], ' ', regex=True) 

    df = limpiar_fecha(df, 'fecha_de_beneficio')
    df = limpiar_monto(df, 'monto_del_credito')
    limp_str_comp(df, 'línea_credito')

    df.drop_duplicates(inplace=True)
    df.to_csv('files/output/solicitudes_de_credito.csv', index=False, sep=';')

    return df.sexo.value_counts().to_list()

print(pregunta_01())